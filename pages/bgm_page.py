from playwright.sync_api import expect
from config.locators import Locators
from utils import logger


class BgmPage:
    """封装 BGM 背景音乐模式相关的页面操作"""

    def __init__(self, page):
        self.page = page

    # ------------------------------------------------------------------
    # 基础操作
    # ------------------------------------------------------------------

    def switch_to_bgm_tab(self):
        """点击切换到 BGM 分页"""
        self.page.locator(Locators.BGM_TAB).click()
        self.page.wait_for_timeout(1000)
        logger.info("切换到 BGM 模式分页")

    def input_prompt(self, text: str, timeout: int = 10000):
        """在 BGM 文本输入框输入描述内容"""
        textarea = self.page.locator(Locators.BGM_CONTENT_TEXTAREA).first
        textarea.fill(text)
        expect(textarea).to_have_value(text, timeout=timeout)
        logger.success(f"BGM 描述输入验证成功: {text[:30]}...")

    def input_song_title(self, title: str):
        """输入歌曲名称"""
        self.page.locator(Locators.SONG_TITLE_INPUT).fill(title)
        logger.info(f"输入歌曲名称: {title}")

    def click_create(self):
        """点击立即创作按钮"""
        self.page.locator(Locators.CREATE_BTN).click()
        logger.info("点击了立即创作按钮")

    # ------------------------------------------------------------------
    # AI 分析弹窗操作（BGM 模式与文本模式相同，无查看歌词按钮）
    # ------------------------------------------------------------------

    def wait_for_ai_analysis(self):
        """等待 AI 分析页面出现，断言 Original Version 和 Create Now 按钮可见"""
        logger.info("等待 AI 分析页面...")
        expect(self.page.locator(Locators.AI_CREATE_NOW_BTN).first).to_be_visible(timeout=120000)
        expect(self.page.locator(Locators.AI_ORIGINAL_VERSION_BTN).first).to_be_visible(timeout=120000)
        logger.success("AI 分析页面显示正常，包含 Original Version 和 Create Now 按钮")

    def select_original_version(self):
        """点击用原始数据生成"""
        self.page.locator(Locators.AI_ORIGINAL_VERSION_BTN).first.dispatch_event("click")
        logger.info("点击了原始数据生成按钮")

    def select_create_now(self):
        """点击 Create Now（AI 生成）"""
        self.page.locator(Locators.AI_CREATE_NOW_BTN).first.dispatch_event("click")
        logger.info("点击了 AI 生成按钮 (Create Now)")

    def confirm_generation(self):
        """处理确认弹窗（如出现则点击继续）"""
        try:
            if self.page.locator(Locators.CONFIRM_DIALOG).is_visible(timeout=5000):
                self.page.locator(Locators.CONFIRM_CONTINUE_BTN).dispatch_event("click")
                logger.info("确认生成弹窗: 点击继续")
        except Exception:
            pass

    # ------------------------------------------------------------------
    # 等待生成结果
    # ------------------------------------------------------------------

    def wait_for_generation_success(self, title: str, timeout: int = 600000):
        """等待歌曲生成成功（复用 TextPage 的轮询逻辑）"""
        from pages.text_page import TextPage
        tp = TextPage(self.page)
        return tp.wait_for_generation_success(title=title, timeout=timeout)
