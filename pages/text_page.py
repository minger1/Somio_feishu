from playwright.sync_api import expect
from locators import Locators
from logger import logger
import time
import re
from re import compile

class TextPage:
    """封装文本模式相关的页面操作"""

    def __init__(self, page):
        self.page = page

    def text_input(self, text: str, timeout: int = 10000):
        """输入文本"""
        textarea = self.page.locator(Locators.TEXTAREA_INPUT).first
        textarea.fill(text)
        expect(textarea).to_have_value(text, timeout=timeout)
        logger.success(f"文本输入验证成功: {text}")

    def model_version(self, locator: str, timeout: int = 10000):
        """打开模型下拉并选择指定的版本"""
        # 第一步：点击下拉框标题以展开
        self.page.locator(Locators.MODEL_VERSION_DROPDOWN).click()
        # 增加一小段等待，确保下拉动画完成
        self.page.wait_for_timeout(500)
        # 第二步：点击指定的选项
        self.page.locator(locator).click(force=True)
        logger.success(f"模型版本选择指令发送成功: {locator}")

    def is_limit_dialog_visible(self, timeout: int = 5000) -> bool:
        """检查限制弹窗是否可见"""
        return self.page.locator(Locators.LIMIT_DIALOG).is_visible(timeout=timeout)

    def close_limit_dialog(self):
        """关闭限制弹窗"""
        self.page.locator(Locators.LIMIT_DIALOG_CLOSE).click()
        expect(self.page.locator(Locators.LIMIT_DIALOG)).to_be_hidden()
        logger.success("限制弹窗已关闭")

    def click_limit_upgrade(self):
        """点击限制弹窗中的升级按钮"""
        self.page.locator(Locators.LIMIT_UPGRADE_BTN).click(force=True)
        logger.info("点击了限制弹窗中的升级/购买按钮")

    def click_limit_login(self):
        """点击限制弹窗中的登录按钮"""
        self.page.locator(Locators.LIMIT_LOGIN_BTN).click(force=True)
        logger.info("点击了限制弹窗中的登录按钮")

    def click_create(self):
        """点击主界面立即创作按钮"""
        self.page.locator(Locators.CREATE_BTN).click()
        logger.info("点击了立即创作按钮")

    def song_title_input(self, title: str):
        """输入歌曲名称"""
        self.page.locator(Locators.SONG_TITLE_INPUT).fill(title)
        logger.info(f"输入歌曲名称: {title}")

    def text_ai_analysis_popup(self):
        """
        等待ai分析成功
        """
        logger.info(f"等待 AI 分析弹窗出现...")
        # 使用用户提供的新定位符
        expect(self.page.locator(Locators.AI_ANALYSIS_MODAL)).to_be_visible(timeout=30000)
        expect(self.page.locator(Locators.AI_CREATE_NOW_BTN)).to_be_visible(timeout=120000)
        expect(self.page.locator(Locators.AI_ORIGINAL_VERSION_BTN)).to_be_visible(timeout=120000)
        expect(self.page.locator(Locators.AI_VIEW_LYRICS_BTN)).to_be_visible(timeout=120000)
        logger.success("AI分析成功，返回ai分析结果")


    def text_select_original(self):
        """
        文本模式下ai分析窗口-用原始数据生成
        """
        self.page.locator(Locators.AI_ORIGINAL_VERSION_BTN).dispatch_event("click")
        logger.info("点击了原始数据生成按钮")

    def text_select_create_now(self):
        """
        文本模式下ai分析窗口-直接点击create now生成
        """
        self.page.locator(Locators.AI_CREATE_NOW_BTN).dispatch_event("click")
        logger.info("点击了AI生成按钮")


    """
    查看歌词
    """

    def text_select_view_lyrics(self):
        """
        文本模式下ai分析窗口-查看歌词
        """
        self.page.locator(Locators.AI_VIEW_LYRICS_BTN).dispatch_event("click")
        logger.info("点击了查看歌词按钮")
    
    def text_select_view_lyrics_generate(self):
        """
        文本模式下ai分析窗口-查看歌词-生成歌词
        """
        self.page.locator(Locators.LYRICS_GENERATE_BTN).dispatch_event("click")
        logger.info("点击了歌词生成按钮")
    
    def text_select_view_lyrics_edit(self):
        """
        文本模式下ai分析窗口-查看歌词-编辑歌词
        """
        self.page.locator(Locators.LYRICS_EDIT_BTN).dispatch_event("click")
        logger.info("点击了歌词编辑按钮")

    def text_select_view_lyrics_edit_cancel(self):
        """
        文本模式下ai分析窗口-查看歌词-编辑歌词-取消编辑
        """
        self.page.locator(Locators.LYRICS_EDIT_CANCEL_BTN).dispatch_event("click")
        logger.info("点击了歌词编辑取消按钮")

    def text_select_view_lyrics_edit_save(self):
        """
        文本模式下ai分析窗口-查看歌词-编辑歌词-保存编辑
        """
        self.page.locator(Locators.LYRICS_EDIT_SAVE_BTN).dispatch_event("click")
        logger.info("点击了歌词编辑保存按钮")

    def text_select_view_lyrics_edit_clear(self):
        """
        文本模式下ai分析窗口-查看歌词-编辑歌词-清除歌词
        """
        self.page.locator(Locators.LYRICS_CLEAR_BTN).dispatch_event("click")
        logger.info("点击了歌词清除按钮")



    

    def confirm_generation(self):
        """在确认弹窗中点击继续"""
        if self.page.locator(Locators.CONFIRM_DIALOG).is_visible(timeout=5000):
            self.page.locator(Locators.CONFIRM_CONTINUE_BTN).dispatch_event("click")
            logger.info("确认生成弹窗: 点击继续")

    def confirm_cancel(self):
        """在确认弹窗中点击取消"""
        if self.page.locator(Locators.CONFIRM_DIALOG).is_visible(timeout=5000):
            self.page.locator(Locators.CONFIRM_CANCEL_BTN).dispatch_event("click")
            logger.info("确认生成弹窗: 点击取消")

    def wait_for_generation_success(self, title: str = None, timeout: int = 600000):
        """
        判断歌曲生成成功：
        1. 定位任务 (按 title 或最新的 loading 任务)
        2. 轮询检查 loading 状态是否结束
        """
        logger.info(f"开始等待歌曲生成（监控歌曲: {title if title else '最新任务'}）...")
        
        # 定义任务定位器 - 使用 contains 增强鲁棒性
        if title:
            task_locator = self.page.locator(f"//li[contains(@class, 'item') and .//span[contains(text(), '{title}')]]")
        else:
            task_locator = self.page.locator(Locators.LOADING_TASK).first

        start_time = time.time()
        found_loading = False
        last_screenshot_time = start_time
        using_fallback = False
        
        while time.time() - start_time < timeout / 1000:
            try:
                # 如果有标题但找不着超过 30s，尝试回退到追踪最新任务
                if title and not using_fallback and time.time() - start_time > 30:
                    if task_locator.count() == 0:
                        temp_latest = self.page.locator(Locators.LOADING_TASK).first
                        if temp_latest.count() > 0:
                            # 尝试提取新名字 (假设在 span 中)
                            try:
                                new_title = temp_latest.locator("span").first.text_content(timeout=3000).strip()
                                if new_title:
                                    logger.warning(f"未能找到标题为 '{title}' 的任务，识别到最新任务名为 '{new_title}'。切换追踪...")
                                    title = new_title
                                    task_locator = self.page.locator(f"//li[contains(@class, 'item') and .//span[contains(text(), '{title}')]]")
                                    using_fallback = True
                            except:
                                logger.warning(f"未能找到标题为 '{title}' 的任务，且无法识别新任务名。直接回退至追踪第一个 loading 任务...")
                                task_locator = temp_latest
                                using_fallback = True
                        else:
                            logger.debug("尚未发现任何生成的 loading 任务...")


                # 检查并关闭可能出现的弹窗 (如：帖子赚积分弹窗)
                close_btn = self.page.locator("//div[contains(@class, 'close') or contains(@class, 'icon-close')]").first
                if close_btn.is_visible():
                    close_btn.click()
                    logger.info("检测到并关闭了随机弹窗")

                # 检查元素是否存在且获取其 class
                if task_locator.count() > 0:
                    current_class = task_locator.first.get_attribute("class") or ""
                    
                    if "loading" in current_class:
                        if not found_loading:
                            logger.info(f"检测到歌曲正在生成中 (Class: {current_class})")
                            found_loading = True
                    else:
                        # 如果没有 loading 类，则判断为成功
                        # 注意：需要确保它是我们之前看到的那个 item，或者至少不是空状态
                        logger.success(f"歌曲生成完成! (最终 Class: {current_class})")
                        return True
                else:
                    if time.time() - start_time > 20: 
                        logger.warning(f"尚未在列表中找到标题包含 '{title}' 的任务...")
            except Exception as e:
                logger.debug(f"轮询中遇到异常 (可能正在刷新): {e}")
            
            time.sleep(10) # 延长轮询间隔到 10s
            
        logger.error(f"歌曲生成等待超时 ({timeout/1000}s)")
        # 超时后再截一张图
        self.page.screenshot(path=f"report/img/timeout_state_{int(time.time())}.png")
        return False
