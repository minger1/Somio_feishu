"""
飞书长连接（WebSocket）告警监听服务
- 通过 lark-oapi 与飞书建立长连接
- 无需公网 IP，无需 ngrok，无需 Flask
"""

import json
import logging
import os
import subprocess
import threading
import time
from datetime import datetime

import requests
import lark_oapi as lark
from lark_oapi.api.im.v1 import P2ImMessageReceiveV1

# 配置区域
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
FEISHU_WEBHOOK_URL = os.getenv("FEISHU_WEBHOOK_URL", "")
ALERT_KEYWORDS = os.getenv("ALERT_KEYWORDS", "告警,MusicGPT告警,music_request_fail,生成失败").split(",")
TEST_SCRIPT_PATH = os.getenv("TEST_SCRIPT_PATH", "./test_script.py")
DEBOUNCE_SECONDS = int(os.getenv("DEBOUNCE_SECONDS", "60"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

_last_trigger = {}
_is_running = False
_lock = threading.Lock()

def match_alert_keywords(text: str) -> str | None:
    for kw in ALERT_KEYWORDS:
        if kw.strip() and kw.strip() in text:
            return kw.strip()
    return None

def should_trigger(keyword: str) -> bool:
    global _is_running
    with _lock:
        if _is_running:
            logger.info("⚠️ 测试正在进行中，已自动忽略本次重复触发")
            return False
            
        last = _last_trigger.get(keyword, 0)
        now = time.time()
        if now - last < DEBOUNCE_SECONDS:
            logger.info(f"防抖跳过，关键词「{keyword}」冷却中")
            return False
            
        _is_running = True # 锁定
        _last_trigger[keyword] = now
        return True

def upload_feishu_image(image_path: str) -> str:
    from lark_oapi.api.im.v1 import CreateImageRequest, CreateImageRequestBody
    logger.info(f"正在上传测试截图以供展示: {image_path}")
    cli = lark.Client.builder().app_id(FEISHU_APP_ID).app_secret(FEISHU_APP_SECRET).build()
    with open(image_path, "rb") as f:
        request = CreateImageRequest.builder() \
            .request_body(CreateImageRequestBody.builder()
                .image_type("message")
                .image(f)
                .build()) \
            .build()
        response = cli.im.v1.image.create(request)
        if not response.success():
            logger.error(f"图片上传失败: [{response.code}] {response.msg}")
            return ""
        return response.data.image_key

def send_feishu_message(content: str, title: str = "🧪 自动化测试"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    card = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {"title": {"tag": "plain_text", "content": title}, "template": "blue"},
            "elements": [
                {"tag": "div", "text": {"tag": "lark_md", "content": content}},
                {"tag": "note", "elements": [{"tag": "plain_text", "content": f"触发时间：{now}"}]},
            ],
        },
    }
    try:
        requests.post(FEISHU_WEBHOOK_URL, json=card, timeout=10)
    except:
        pass

def format_duration(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m}分{s}秒" if m > 0 else f"{s}秒"

def send_feishu_report_card(start_time_str, end_time_str, elapsed, results):
    total_cases = len(results)
    success_cases = len([r for r in results if r.get('status') == 'PASS'])
    
    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**执行总数:**  {total_cases}    |    **成功:**  {success_cases}    |    **失败:**  {total_cases - success_cases}\n\n**开始时间:**  {start_time_str}\n**结束时间:**  {end_time_str}\n**总共耗时:**  {format_duration(elapsed)}"
            }
        },
        {"tag": "hr"}
    ]
    
    for idx, r in enumerate(results, 1):
        name = r.get("name", "Unknown Case")
        status = r.get("status", "UNKNOWN")
        duration = r.get("duration", 0)
        
        icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⏭️"
        
        case_md = f"**{idx}. {name}**\n状态：{icon} {status}    |    耗时：{format_duration(duration)}"
        elements.append({
            "tag": "div",
            "text": {"tag": "lark_md", "content": case_md}
        })
        
        if status == "FAIL" and r.get("screenshot"):
            img_key = upload_feishu_image(r["screenshot"])
            if img_key:
                elements.append({
                    "tag": "img",
                    "img_key": img_key,
                    "alt": {"tag": "plain_text", "content": "错误截图"}
                })
    
    elements.append({"tag": "hr"})
    elements.append({
        "tag": "note",
        "elements": [{"tag": "plain_text", "content": "自动化测试报告"}]
    })
    
    card = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": "测试报告"}, 
                "template": "turquoise" if success_cases > 0 and success_cases == total_cases else "red"
            },
            "elements": elements
        }
    }
    try:
        requests.post(FEISHU_WEBHOOK_URL, json=card, timeout=15)
    except Exception as e:
        logger.error(f"发送测试报告失败: {e}")

def run_test_script(alert_text: str, keyword: str, title: str = "🔔 检测到告警，已触发自动测试"):
    logger.info(f"🚀 开始执行测试脚本，触发关键词：{keyword}")
    
    # 消息内容根据是否是例行任务动态调整标签
    label = "例行任务" if "Schedule" in keyword else "触发告警"
    content = f"**{label}：** `{keyword}`\n\n**详细内容：**\n> {alert_text[:200]}\n\n⏳ 正在执行测试用例，请稍候..."
    
    send_feishu_message(content, title=title)

    start_dt = datetime.now()
    start_time_str = start_dt.strftime("%Y-%m-%d %H:%M:%S")
    start = time.time()
    
    global _is_running
    try:
        import sys
        logger.info(f"正在启动子进程: {sys.executable} {TEST_SCRIPT_PATH}")
        
        # 移除 capture_output，让子进程的输出直接显示在当前终端
        subprocess.run(
            [sys.executable, TEST_SCRIPT_PATH, "--alert", keyword],
            text=True, timeout=1800,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        elapsed = round(time.time() - start, 2)
        end_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        test_results = []
        results_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_results.jsonl")
        if os.path.exists(results_file):
            with open(results_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            test_results.append(json.loads(line))
                        except Exception:
                            pass
                
        send_feishu_report_card(start_time_str, end_time_str, elapsed, test_results)
    except Exception as e:
        send_feishu_message(f"💥 **执行异常**\n{str(e)}", title="测试执行出错")
    finally:
        with _lock:
            _is_running = False
            logger.info("🔓 测试任务结束，已释放运行锁，恢复空闲状态")

def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1) -> None:
    # 加个万能调试：只要受到消息了，哪怕不匹配也先打印一条！
    logger.info("=============== ⚡ 飞书网络推送直达 ===============")
    
    try:
        msg_id = getattr(data.event.message, "message_id", "Unknown")
        logger.info(f"[*] 收到飞书层推流事件, Message_ID= {msg_id}")
        content_str = data.event.message.content
        msg_type = data.event.message.message_type
        
        text = ""
        if msg_type == "text":
             text = json.loads(content_str).get("text", "")
        elif msg_type == "post":
             content_dict = json.loads(content_str)
             texts = []
             for line in content_dict.get("content", []):
                  for seg in line:
                      if seg.get("tag") == "text":
                           texts.append(seg.get("text", ""))
             text = " ".join(texts)
             
        if not text:
             return
             
        logger.info(f"收到飞书事件推送息: {text[:100]}")
        keyword = match_alert_keywords(text)
        
        # 如果没有命中告警词，但检测到有人@了机器人，或者是私聊发给机器人的，强制触发
        if not keyword:
            chat_type = getattr(data.event.message, "chat_type", "group")
            mentions = getattr(data.event.message, "mentions", [])
            if chat_type == "p2p" or mentions:
                keyword = "人工@强制触发"
                
        if keyword:
            if should_trigger(keyword):
                t = threading.Thread(target=run_test_script, args=(text, keyword), daemon=True)
                t.start()
    except Exception as e:
        logger.error(f"处理消息出错: {e}")

event_handler = lark.EventDispatcherHandler.builder("", "") \
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
    .build()

def start_scheduler():
    """
    每天固定时间点执行测试任务
    """
    # 从环境变量读取时间，默认 10:00
    target_time = os.getenv("SCHEDULE_TIME", "10:00")
    logger.info(f"⏰ 定时任务已启动，每天 {target_time} 准时执行测试...")
    
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == target_time:
            logger.info(f"🕒 定时时间 {target_time} 已到，自动触发例行检查...")
            # 传入专用标题
            run_test_script("系统每日例行自动检查", "Daily_Schedule_Task", title="📅 每日例行自动化巡检")
            
            # 触发后休眠 61 秒，防止同一分钟内多次触发
            time.sleep(61)
            
        # 每隔 30 秒轮询一次时间
        time.sleep(30)

def start_ws():
    logger.info("✅ 飞书 WebSocket 长连接客户端即将启动...")
    logger.info(f"📌 监听关键词: {ALERT_KEYWORDS}")

    # 检查是否开启定时任务 (ENABLE_SCHEDULE 默认为 true)
    if os.getenv("ENABLE_SCHEDULE", "true").lower() == "true":
        # 启动定时执行线程 (守护线程，随主线程退出)
        scheduler_thread = threading.Thread(target=start_scheduler, daemon=True)
        scheduler_thread.start()
    else:
        logger.info("⏸️ 定时任务当前处于 [已停用] 状态 (ENABLE_SCHEDULE=false)")
    
    # 建立长连接客户端，这里不需要加密Token，只需要APP_ID和SECRET
    cli = lark.ws.Client(FEISHU_APP_ID, FEISHU_APP_SECRET, event_handler=event_handler, log_level=lark.LogLevel.INFO)
    cli.start()
