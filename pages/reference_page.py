from playwright.sync_api import expect
from config.locators import Locators
from utils import logger, wait_for_ai_analysis_common
import time

class ReferencePage:
    """封装 Reference 模式相关的页面操作"""

    def __init__(self, page):
        self.page = page

    def switch_to_reference_tab(self):
        """点击切换到 Reference 分页"""
        self.page.locator(Locators.REFERENCE_TAB).click()
        # 动态等待：一旦链接输入框变为可见，说明 Reference 面板渲染已完全稳定
        self.page.locator(Locators.REFERENCE_LINK_INPUT).wait_for(state="visible", timeout=10000)
        logger.info("切换到 Reference 模式分页")

    def input_reference_link(self, link: str, timeout: int = 10000):
        """输入 reference 音乐链接"""
        input_el = self.page.locator(Locators.REFERENCE_LINK_INPUT)
        input_el.fill(link)
        expect(input_el).to_have_value(link, timeout=timeout)
        logger.success(f"输入 Reference 链接成功: {link}")

    def input_prompt(self, text: str, timeout: int = 10000):
        """在 Reference 文本输入框输入描述内容"""
        textarea = self.page.locator(Locators.REFERENCE_CONTENT_TEXTAREA).first
        textarea.fill(text)
        expect(textarea).to_have_value(text, timeout=timeout)
        logger.success(f"Reference 提示词输入成功: {text[:30]}...")

    def click_create(self):
        """点击立即创作按钮"""
        self.page.locator(Locators.CREATE_BTN).click()
        logger.info("点击立即创作按钮")

    def wait_for_ai_analysis(self, timeout: int = 120000):
        """等待 AI 分析弹窗并确认按钮可见"""
        wait_for_ai_analysis_common(
            page=self.page,
            modal_locators=[Locators.REFERENCE_AI_LOADING, Locators.AI_ANALYSIS_MODAL],
            success_locators=[Locators.REFERENCE_AI_CREATE_NOW_BTN, Locators.REFERENCE_AI_VIEW_LYRICS_BTN],
            success_message="Reference AI 分析完成，Create Now 和 View Lyrics 按钮可见",
            timeout=timeout
        )

    def select_create_now(self):
        """选择直接生成"""
        logger.info("选择 Reference Create Now 直接生成")
        btn = self.page.locator(Locators.REFERENCE_AI_CREATE_NOW_BTN).first
        try:
            btn.click(timeout=5000)
        except Exception:
            btn.dispatch_event("click")

    def select_view_lyrics(self):
        """选择 View Lyrics"""
        logger.info("选择 Reference View Lyrics 详情")
        btn = self.page.locator(Locators.REFERENCE_AI_VIEW_LYRICS_BTN).first
        try:
            btn.click(timeout=5000)
        except Exception:
            btn.dispatch_event("click")
        self.page.wait_for_timeout(1000)

    def edit_generated_lyrics_title(self, new_title: str):
        """在歌词编辑面板修改歌名，防止被 AI 覆盖"""
        edit_btn = self.page.locator(Locators.LYRICS_EDIT_BTN)
        try:
            edit_btn.click(timeout=5000)
        except Exception:
            edit_btn.dispatch_event("click")
        logger.info("点击歌词编辑按钮，准备修改歌名")
        
        self.page.locator(Locators.LYRICS_TITLE_INPUT).fill(new_title)
        
        save_btn = self.page.locator(Locators.LYRICS_EDIT_SAVE_BTN)
        try:
            save_btn.click(timeout=5000)
        except Exception:
            save_btn.dispatch_event("click")
        logger.info(f"成功保存修改后的歌名: {new_title}")
        self.page.wait_for_timeout(500)

    def click_generate_lyrics(self):
        """点击详情页的生成歌词/音乐按钮"""
        btn = self.page.locator(Locators.LYRICS_GENERATE_BTN)
        try:
            btn.click(timeout=5000)
        except Exception:
            btn.dispatch_event("click")
        logger.info("点击了歌词二创面板的 Generate 按钮")

    def confirm_generation(self):
        """处理确认生成弹窗"""
        try:
            if self.page.locator(Locators.CONFIRM_DIALOG).is_visible(timeout=5000):
                self.page.locator(Locators.CONFIRM_CONTINUE_BTN).dispatch_event("click")
                logger.info("确认生成弹窗: 点击继续")
        except Exception:
            pass

    def wait_for_generation_success(self, title: str = None, timeout: int = 600000):
        """等待生成成功 (委托给 LibraryPage)"""
        from pages.library_page import LibraryPage
        lib_page = LibraryPage(self.page)
        return lib_page.wait_for_generation_success(title=title, timeout=timeout)

    def run_generation_flow(self, link: str, text: str, song_title: str, action: str = "direct", timeout: int = 600000) -> bool:
        """
        Reference 模式下的通用创作生成流程封装
        action 可选: "direct" (直接生成), "view_lyrics" (查看歌词二创)
        """
        logger.info(f"执行 Reference 模式通用创作流程, 动作: {action}")
        # 1. 切换 Tab
        self.switch_to_reference_tab()
        # 2. 输入 URL 和 prompt
        self.input_reference_link(link)
        self.input_prompt(text)
        
        # 3. 点击创建
        self.click_create()
        # 4. 等待 AI 分析
        self.wait_for_ai_analysis()
        
        # 5. 分流处理
        if action == "direct":
            self.select_create_now()
            self.confirm_generation()
            # 直接生成由于无法提前设置标题，故通过 None 去轮询追踪最新那个加载项即可
            return self.wait_for_generation_success(title=None, timeout=timeout)
        elif action == "view_lyrics":
            self.select_view_lyrics()
            # 详情面板修改歌名
            self.edit_generated_lyrics_title(song_title)
            # 点击生成
            self.click_generate_lyrics()
            # 深度修改模式下，已精准重设了歌曲名，用设好的歌曲名精准轮询
            return self.wait_for_generation_success(title=song_title, timeout=timeout)
