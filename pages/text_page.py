from playwright.sync_api import expect
from config.locators import Locators
from utils import logger, wait_for_ai_analysis_common
import time
import re

class TextPage:
    """封装文本/歌词模式相关的页面操作"""

    def __init__(self, page):
        self.page = page

    def switch_to_lyrics_tab(self):
        """点击顶部 Tab 切换到歌词(Lyrics)特征生成模式"""
        logger.info("切换到 Lyrics 选项卡")
        self.page.locator(Locators.LYRICS_TAB).click()
        self.page.wait_for_timeout(1000)

    def text_input(self, text: str, timeout: int = 10000):
        """在区域内输入文本提示词"""
        logger.info(f"输入文本提示词: {text[:15]}...")
        textarea = self.page.locator(Locators.TEXTAREA_INPUT).first
        textarea.fill(text)
        expect(textarea).to_have_value(text, timeout=timeout)

    def lyrics_input(self, lyrics: str, timeout: int = 10000):
        """输入歌词"""
        logger.info(f"输入歌词文本: {lyrics[:15]}...")
        textarea = self.page.locator(Locators.LYRICS_CONTENT_TEXTAREA).first
        textarea.fill(lyrics)
        expect(textarea).to_have_value(lyrics, timeout=timeout)

    def model_version(self, model_locator: str, provider_locator: str = None, timeout: int = 10000):
        """打开模型下拉并选择指定的版本
        
        新的两列结构:
        - 先点击 provider_locator 选择 provider（Somio.ai/Google/MINIMAX）
        - 再点击 model_locator 选择具体模型
        - 如果 provider_locator 为 None，表示默认不需要切换 provider
        """
        # 第一步：点击下拉框标题以展开
        self.page.locator(Locators.MODEL_VERSION_DROPDOWN).click()
        # 增加一小段等待，确保下拉动画完成
        self.page.wait_for_timeout(500)
        # 第二步：如果指定了 provider，先切换 provider
        if provider_locator:
            self.page.locator(provider_locator).click(force=True)
            self.page.wait_for_timeout(400)
        # 第三步：点击具体的模型选项
        self.page.locator(model_locator).click(force=True)
        logger.success(f"模型版本选择指令发送成功: {model_locator}")

    def is_limit_dialog_visible(self, timeout: int = 5000) -> bool:
        """检查限制弹窗是否可见"""
        return self.page.locator(Locators.LIMIT_DIALOG).is_visible(timeout=timeout)

    def assert_limit_dialog_visible(self, timeout: int = 5000):
        """断言限制弹窗可见"""
        expect(self.page.locator(Locators.LIMIT_DIALOG)).to_be_visible(timeout=timeout)
        logger.success("验证通过：限制弹窗已弹出")

    def assert_login_modal_visible(self, timeout: int = 5000):
        """断言登录窗口可见"""
        expect(self.page.locator(Locators.LOGIN_MODAL)).to_be_visible(timeout=timeout)
        logger.success("验证通过：登录窗口已弹出")

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
        """点击底部 Create 按钮生成"""
        logger.info("点击 Create 按钮")
        self.page.locator(Locators.CREATE_BTN).click()

    def song_title_input(self, title: str):
        """输入歌曲名称"""
        logger.info(f"输入歌曲名称: '{title}'")
        self.page.locator(Locators.SONG_TITLE_INPUT).fill(title)
        time.sleep(1)

    def text_ai_analysis_popup(self):
        """等待 AI 分析弹窗"""
        wait_for_ai_analysis_common(
            page=self.page,
            modal_locators=[Locators.REFERENCE_AI_LOADING, Locators.AI_ANALYSIS_MODAL],
            success_locators=[Locators.AI_CREATE_NOW_BTN, Locators.AI_ORIGINAL_VERSION_BTN],
            success_message="AI 分析完成，Create Now 和 Original Version 按钮可见"
        )

    def switch_ai_analysis_tab(self, tab_name: str):
        """
        AI分析页面切换分页
        tab_name: 'Lyrics Formatting' 或 'Lyrics Refinement'
        """
        tabs = self.page.locator(Locators.LYRICS_AI_ANALYSIS_TABS)
        if tab_name.lower() == "formatting":
            tabs.nth(0).click()
        elif tab_name.lower() == "refinement":
            tabs.nth(1).click()
        else:
            # 或者直接按文本匹配
            tabs.filter(has_text=tab_name).click()
        logger.info(f"AI分析页面切换到分页: {tab_name}")


    def text_select_original(self):
        """选择 Original Version"""
        logger.info("选择 Original Version")
        self.page.locator(Locators.AI_ORIGINAL_VERSION_BTN).first.dispatch_event("click")

    def text_select_create_now(self):
        """选择 Create Now"""
        logger.info("选择 Create Now (AI)")
        self.page.locator(Locators.AI_CREATE_NOW_BTN).first.dispatch_event("click")


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

    def edit_generated_lyrics_title(self, new_title: str):
        """
        在歌词生成窗口修改被 AI 覆盖的歌名
        """
        # 点击编辑按钮
        self.page.locator(Locators.LYRICS_EDIT_BTN).dispatch_event("click")
        logger.info("点击编辑按钮，准备修改被AI覆盖的歌名")
        
        # 输入新的歌名
        self.page.locator(Locators.LYRICS_TITLE_INPUT).fill(new_title)
        
        # 保存编辑
        self.page.locator(Locators.LYRICS_EDIT_SAVE_BTN).dispatch_event("click")
        logger.info(f"保存了修改后的歌名: {new_title}")
        self.page.wait_for_timeout(500)

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
        """弹窗确认扣费生成"""
        logger.info("检查并确认扣费系统弹窗...")
        if self.page.locator(Locators.CONFIRM_DIALOG).is_visible(timeout=5000):
            logger.info("点击 Continue 确认生成")
            self.page.locator(Locators.CONFIRM_CONTINUE_BTN).dispatch_event("click")

    def confirm_cancel(self):
        """取消生成"""
        logger.info("检查积分弹窗...")
        if self.page.locator(Locators.CONFIRM_DIALOG).is_visible(timeout=5000):
            logger.info("点击 Cancel 取消生成")
            self.page.locator(Locators.CONFIRM_CANCEL_BTN).dispatch_event("click")

    def wait_for_generation_success(self, title: str = None, timeout: int = 600000):
        """等待生成成功 (委托给 LibraryPage)"""
        from pages.library_page import LibraryPage
        lib_page = LibraryPage(self.page)
        return lib_page.wait_for_generation_success(title=title, timeout=timeout)


    def run_model_generation_flow(self, model_name: str, model_locator: str, provider_locator: str = None):
        """通用底层模型切换生成辅助方法（用标准文本直接生成）"""
        from utils import get_song
        from data.test_data import TEST_TEXT_PROMPT
        logger.info(f"开始执行纯文本模式下的模型切换生成操作: {model_name}")
        
        # 1. 先切换模型
        self.model_version(model_locator, provider_locator)

        # 2. 输入歌词/文本提示
        self.text_input(TEST_TEXT_PROMPT)
        
        # 3. 输入歌名
        song_title = get_song(prefix="TEXT", model=model_name)
        self.song_title_input(song_title)
        
        # 4. 点击创建
        self.click_create()

        # 5. 标准文本直接生成（不展示 AI 分析弹窗），确认扭费弹窗
        self.confirm_generation()
        
        success = self.wait_for_generation_success(title=song_title, timeout=600000)
        return success, song_title

    def run_generation_flow(self, text: str, song_title: str, action: str = "original", timeout: int = 600000) -> bool:
        """
        纯文本模式下的通用创作生成流程封装（简单输入 → AI分析弹窗流程）
        action 可选: "original" (原始版本), "ai" (AI增强), "view_lyrics" (查看歌词并深度二创)
        """
        logger.info(f"执行纯文本通用创作流程(简单输入-AI分析), 生成动作: {action}")
        # 1. 输入文本和歌名
        self.text_input(text)
        self.song_title_input(song_title)
        
        # 2. 点击创建
        self.click_create()
        
        # 3. 等待 AI 分析弹窗就绪
        self.text_ai_analysis_popup()
        
        # 4. 依据 action 分流处理
        if action == "original":
            self.text_select_original()
            self.confirm_generation()
        elif action == "ai":
            self.text_select_create_now()
            self.confirm_generation()
        elif action == "view_lyrics":
            self.text_select_view_lyrics()
            # 恢复歌名标记，保证后续能通过歌名追踪
            self.edit_generated_lyrics_title(song_title)
            # 点击歌词视图面板的 Generate 按钮生成歌词
            self.text_select_view_lyrics_generate()
            # 生成歌词后处理扭费确认弹窗
            self.confirm_generation()
            
        # 5. 验证并等待生成结果
        return self.wait_for_generation_success(title=song_title, timeout=timeout)

    def run_standard_generation_flow(self, text: str, song_title: str, timeout: int = 600000) -> bool:
        """
        纯文本模式 - 标准输入直接生成流程（跳过 AI 分析，直接到扣费确认弹窗）
        """
        logger.info("执行纯文本通用创作流程(标准输入-直接生成)")
        # 1. 输入文本和歌名
        self.text_input(text)
        self.song_title_input(song_title)
        
        # 2. 点击创建
        self.click_create()
        
        # 3. 直接处理扭费确认弹窗（标准输入不会弹出 AI 分析）
        self.confirm_generation()
            
        # 4. 验证并等待生成结果
        return self.wait_for_generation_success(title=song_title, timeout=timeout)
