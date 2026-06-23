import os
import sys

# 强制设置 Python 的 IO 流编码为 UTF-8，彻底解决 Windows 多进程下标准输出写入报告时的中文乱码问题
os.environ["PYTHONIOENCODING"] = "utf-8"

import argparse
import pytest
from datetime import datetime
import threading
import time
from config.settings import GENERATE_HTML_REPORT, GENERATE_API_COMPARE

# ==================== 用户自定义运行配置 (USER CONFIGURATION) ====================
# [配置 1] 默认并发运行的 worker 数量，可选数字 (如 "1", "2") 或 "auto"
DEFAULT_WORKERS = "1"

# 引入 config/settings.py 中的全局配置作为默认值


# [配置 4] 默认运行的测试用例文件或目录路径，可以指定具体文件（如 "testcase/test_login.py"）或整个文件夹（如 "testcase/"）
TEST_TARGET = "testcase/test_lyrics_create_song.py"
# =================================================================================


def run_tests():
    """
    运行测试套件，支持并发执行。
    """
    parser = argparse.ArgumentParser(description="运行 Playwright 测试")
    parser.add_argument("-n", "--workers", type=str, default=DEFAULT_WORKERS, help=f"并发运行的 worker 数量，默认：{DEFAULT_WORKERS}")
    parser.add_argument("-k", "--filter", type=str, default="", help="可选：按名称过滤测试用例")
    parser.add_argument("--no-report", action="store_true", help="不生成标准 HTML 网页测试报告")
    parser.add_argument("--no-api-compare", action="store_true", help="不捕获接口数据且不进行契约对比审计")
    args_parsed, extra_args = parser.parse_known_args()

    # 命令行优先级最高，未在命令行指定时使用顶部的默认配置
    enable_report = not args_parsed.no_report if args_parsed.no_report else GENERATE_HTML_REPORT
    enable_api = not args_parsed.no_api_compare if args_parsed.no_api_compare else GENERATE_API_COMPARE

    # 将接口捕获开关以环境变量贯通传递给用例进程
    os.environ["GENERATE_API_COMPARE"] = "1" if enable_api else "0"

    report_dir = os.path.join("report", "test_reports")
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.environ["API_CAPTURE_RUN_TIMESTAMP"] = timestamp
    report_file = os.path.join(report_dir, f"report_{timestamp}.html")
    
    # 基础运行命令
    pytest_args = [
        "-v",
        f"-n={args_parsed.workers}",  # 并发核心数
        "--dist=load",              # 改为 load
        TEST_TARGET,
    ]

    # 根据配置动态决定是否输出标准 HTML 测试报告
    if enable_report:
        pytest_args.extend([
            f"--html={report_file}",
            "--self-contained-html",
        ])

    if args_parsed.filter:
        pytest_args.extend(["-k", args_parsed.filter])

    # 如果有其他透传参数，也加上
    pytest_args.extend(extra_args)
    
    print(f"正在启动测试 (Workers: {args_parsed.workers})，报告将保存至: {report_file}")
    

    def tail_logs(stop_event):
        log_dir = "logs"
        ts = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(log_dir, f"info_{ts}.log")
        
        while not os.path.exists(log_file) and not stop_event.is_set():
            time.sleep(0.1)
            
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                f.seek(0, 2) # 只看本次运行的新日志
                while not stop_event.is_set():
                     where = f.tell()
                     line = f.readline()
                     if not line:
                         time.sleep(0.1)
                         f.seek(where)
                     else:
                         try:
                             # 绕过 pytest 主进程捕获，强制输出到真实终端
                             sys.__stdout__.write(line)
                             sys.__stdout__.flush()
                         except:
                             pass

    stop_event = threading.Event()
    t = threading.Thread(target=tail_logs, args=(stop_event,), daemon=True)
    t.start()

    try:
        pytest.main(pytest_args)
    finally:
        stop_event.set()
        t.join(timeout=1.0)
        
        # 整个套件执行完后，自动进行全体接口的合并对比
        if enable_api:
            try:
                snapshot_dir = "report/api_snapshots"
                if os.path.exists(snapshot_dir):
                    import glob
                    import re
                    
                    all_files = glob.glob(os.path.join(snapshot_dir, "test_api_data_*.json"))
                    suite_files = []
                    for f in all_files:
                        basename = os.path.basename(f)
                        # 匹配 test_api_data_YYYYMMDD_HHMMSS.json，过滤掉带用例名 test_api_data_test_*.json
                        if re.match(r"^test_api_data_\d{8}_\d{6}\.json$", basename):
                            suite_files.append(f)
                    
                    suite_files.sort()
                    if len(suite_files) >= 2:
                        previous_path = suite_files[-2]
                        latest_path = suite_files[-1]
                        
                        # 确保报告输出文件夹存在
                        os.makedirs("report/api_diff_reports", exist_ok=True)
                        report_path = os.path.join("report/api_diff_reports", f"api_diff_{timestamp}.html")
                        
                        print("\n" + "="*80)
                        print("[APICapturer Global] 正在为本次套件运行生成【全体接口联合对比大报告】...")
                        print(f"   -> 较早套件版本 (数据1): {previous_path}")
                        print(f"   -> 最新套件版本 (数据2): {latest_path}")
                        
                        from utils.api_diff_reporter import generate_visual_diff
                        generate_visual_diff(previous_path, latest_path, report_path)
                        
                        # 显式等待 Loguru 异步日志队列全部消费完毕，杜绝 any I/O 报错警告
                        from loguru import logger
                        try:
                            logger.complete()
                        except Exception:
                            pass
                        
                        print(f"[APICapturer Global] 全体接口联合对比报告已成功生成，请查看：\n{os.path.abspath(report_path)}")
                        print("="*80 + "\n")
                    else:
                        print("\n" + "="*80)
                        print("[APICapturer Global] 首次全体套件捕获完成，再次运行即可自动生成全体接口的可视化比对报告！")
                        print("="*80 + "\n")
            except Exception as e:
                print(f"[APICapturer Global] 生成大对比报告时发生异常: {e}")
        else:
            print("\n" + "="*80)
            print("[APICapturer Global] 契约测试接口捕获与对比已在配置中禁用，本次未采集接口快照。")
            print("="*80 + "\n")

if __name__ == "__main__":
    run_tests()
