import time
from playwright.sync_api import expect
from config.locators import Locators
from utils import logger

def wait_for_ai_analysis_common(page, modal_locators, success_locators, success_message, timeout=120000):
    """
    通用 AI 分析弹窗等待与错误监测工具函数
    
    :param page: Playwright 页面实例
    :param modal_locators: 弹窗/模态框定位器列表 (可包含备用定位器)
    :param success_locators: AI分析成功判断所依赖的按钮/元素定位器列表 (例如：[Create Now, Original Version])
    :param success_message: 成功时的日志输出内容
    :param timeout: 最大超时等待时间，默认 120 秒
    """
    logger.info("等待 AI 分析弹窗出现...")
    
    # 1. 等待任意一个模态框 locator 可见
    start_wait = time.time()
    opened = False
    while time.time() - start_wait < 60:
        if any(page.locator(modal).is_visible() for modal in modal_locators):
            opened = True
            break
        # 检查是否有发生错误提示
        msg_locator = page.locator(Locators.MESSAGE_CONTENT)
        if msg_locator.is_visible(timeout=500):
            err_msg = msg_locator.inner_text().strip()
            logger.error("ai分析失败")
            logger.error(f"ai分析失败: {err_msg}")
            raise AssertionError(f"ai分析失败: {err_msg}")
        time.sleep(0.5)

    if not opened:
        logger.error("ai分析失败")
        logger.error("ai分析失败: 弹窗未出现")
        raise AssertionError("ai分析失败: 弹窗未出现")

    # 弹窗已出现，等待所有成功按钮可见，且监测窗口关闭与错误提示
    start_time = time.time()
    while time.time() - start_time < timeout / 1000:
        # 1. 检查所有成功按钮是否均已可见
        if all(page.locator(loc).first.is_visible() for loc in success_locators):
            logger.success(success_message)
            return True

        # 2. 检查窗口是否被关闭 (所有传入的 modal 都不显示了)
        if not any(page.locator(modal).is_visible() for modal in modal_locators):
            msg_locator = page.locator(Locators.MESSAGE_CONTENT)
            err_msg = ""
            if msg_locator.is_visible(timeout=2000):
                err_msg = msg_locator.inner_text().strip()
            log_msg = f"ai分析失败: 窗口被关闭 {f'({err_msg})' if err_msg else ''}"
            logger.error("ai分析失败")
            logger.error(log_msg)
            raise AssertionError(log_msg)

        # 3. 检查即使窗口没关闭，是否弹出了错误提示
        msg_locator = page.locator(Locators.MESSAGE_CONTENT)
        if msg_locator.is_visible(timeout=500):
            err_msg = msg_locator.inner_text().strip()
            log_msg = f"ai分析失败: 提示错误: {err_msg}"
            logger.error("ai分析失败")
            logger.error(log_msg)
            raise AssertionError(log_msg)

        time.sleep(0.5)

    # 超时处理
    logger.error("ai分析失败")
    raise AssertionError("ai分析失败: 等待 AI 分析结果超时")


def emulate_3g_network(page, mode: str = "slow_3g"):
    """
    通过 Chrome DevTools Protocol (CDP) 模拟弱网环境 (3G网络)
    
    :param page: Playwright 页面实例
    :param mode: "slow_3g" (慢速3G) 或 "fast_3g" (快速3G)
    """
    logger.warning(f"【网络模拟】正在将网络状态配置为: {mode.upper()} ...")
    client = page.context.new_cdp_session(page)
    
    if mode == "slow_3g":
        # 慢速 3G 常用参数：延迟 2000ms，下载 400kbps (50KB/s)，上传 150kbps (18.75KB/s)
        client.send("Network.emulateNetworkConditions", {
            "offline": False,
            "latency": 2000,
            "downloadThroughput": 50000,
            "uploadThroughput": 18750
        })
    elif mode == "fast_3g":
        # 快速 3G 常用参数：延迟 560ms，下载 1.6Mbps (200KB/s)，上传 768kbps (96KB/s)
        client.send("Network.emulateNetworkConditions", {
            "offline": False,
            "latency": 560,
            "downloadThroughput": 200000,
            "uploadThroughput": 96000
        })
    else:
        logger.error(f"未知的网络模拟模式: {mode}")
        return
        
    logger.success(f"【网络模拟】已成功模拟 {mode.upper()} 弱网状态！")


def disable_network_emulation(page):
    """
    清除所有网络模拟状态，恢复正常高带宽无延迟网络
    """
    logger.info("【网络模拟】正在恢复默认正常网络状态...")
    client = page.context.new_cdp_session(page)
    client.send("Network.emulateNetworkConditions", {
        "offline": False,
        "latency": 0,
        "downloadThroughput": -1,
        "uploadThroughput": -1
    })
    logger.success("【网络模拟】网络已成功恢复正常状态。")
