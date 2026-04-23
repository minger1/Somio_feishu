from playwright.sync_api import expect
from config.locators import Locators
from utils import logger
import time
import re
from utils import get_song
from data.test_data import STANDARD_LYRICS


class LyricsPage:
    """封装歌词模式相关的页面操作"""

    def __init__(self, page):
        self.page = page

    # ------------------------------------------------------------------
    # 基础操作
    # ------------------------------------------------------------------

    def switch_to_lyrics_tab(self):
        """点击切换到歌词分页"""
        self.page.locator(Locators.LYRICS_TAB).click()
        self.page.wait_for_timeout(1000)
        logger.info("切换到歌词模式分页")

    def input_lyrics(self, lyrics: str, timeout: int = 10000):
        """在歌词输入框输入内容"""
        textarea = self.page.locator(Locators.LYRICS_CONTENT_TEXTAREA).first
        textarea.fill(lyrics)
        expect(textarea).to_have_value(lyrics, timeout=timeout)
        logger.success("歌词输入验证成功")

    def input_song_title(self, title: str):
        """输入歌曲名称"""
        self.page.locator(Locators.SONG_TITLE_INPUT).fill(title)
        logger.info(f"输入歌曲名称: {title}")

    def model_version(self, locator: str, timeout: int = 10000):
        """打开模型下拉并选择指定的版本"""
        self.page.locator(Locators.MODEL_VERSION_DROPDOWN).click()
        self.page.wait_for_timeout(500)
        self.page.locator(locator).click(force=True)
        logger.success(f"模型版本选择指令发送成功: {locator}")

    def click_create(self):
        """点击立即创作按钮"""
        self.page.locator(Locators.CREATE_BTN).click()
        logger.info("点击了立即创作按钮")

    def confirm_generation(self):
        """处理确认弹窗（如出现则点击继续）"""
        try:
            if self.page.locator(Locators.CONFIRM_DIALOG).is_visible(timeout=5000):
                self.page.locator(Locators.CONFIRM_CONTINUE_BTN).dispatch_event("click")
                logger.info("确认生成弹窗: 点击继续")
        except Exception:
            pass  # 弹窗未出现，忽略

    # ------------------------------------------------------------------
    # AI 分析弹窗操作
    # ------------------------------------------------------------------

    def wait_for_ai_analysis(self):
        """
        等待 AI 分析页面出现，并断言 Original Version 和 Create Now 按钮可见。
        注意：点击创建后可能先出现确认弹窗，需先调用 confirm_generation。
        """
        logger.info("等待 AI 分析页面...")
        expect(self.page.locator(Locators.AI_CREATE_NOW_BTN).first).to_be_visible(timeout=120000)
        expect(self.page.locator(Locators.AI_ORIGINAL_VERSION_BTN).first).to_be_visible(timeout=120000)
        logger.success("AI 分析页面显示正常，包含 Original Version 和 Create Now 按钮")

    def switch_ai_tab(self, tab_index: int):
        """
        切换 AI 分析页面的分页
        0: Lyrics Formatting (默认，无需点击)
        1: Lyrics Refinement (需要点击切换)
        """
        if tab_index == 0:
            logger.info("AI 分析分页保持默认: Lyrics Formatting")
            return
        self.page.locator(Locators.LYRICS_AI_ANALYSIS_REFINEMENT_TAB).click()
        logger.info("切换 AI 分析分页到: Lyrics Refinement")
        self.page.wait_for_timeout(500)

    def select_original_version(self):
        """点击用原始数据生成"""
        self.page.locator(Locators.AI_ORIGINAL_VERSION_BTN).first.dispatch_event("click")
        logger.info("点击了原始数据生成按钮")

    def select_create_now(self):
        """点击 Create Now 生成"""
        self.page.locator(Locators.AI_CREATE_NOW_BTN).first.dispatch_event("click")
        logger.info("点击了 AI 生成按钮 (Create Now)")

    def edit_generated_lyrics_title(self, new_title: str):
        """
        在歌词AI分析窗口修改被 AI 覆盖的歌名
        """
        self.page.locator(Locators.LYRICS_EDIT_BTN).dispatch_event("click")
        logger.info("点击编辑按钮，准备修改被AI覆盖的歌名")
        
        self.page.locator(Locators.LYRICS_TITLE_INPUT).fill(new_title)
        
        self.page.locator(Locators.LYRICS_EDIT_SAVE_BTN).dispatch_event("click")
        logger.info(f"保存了修改后的歌名: {new_title}")
        self.page.wait_for_timeout(500)

    def lyrics_go_to_generate_lyrics(self):
        """
        歌词模式下，点击生成歌词按钮
        """
        self.page.locator(Locators.GENNERATE_LYRICS_TIP_BTN).dispatch_event("click")
        logger.info("点击了生成歌词按钮")
        expect(self.page.locator(Locators.GENNERATE_LYRICS_TIP_BTN)).to_be_hidden()
        logger.success("生成歌词按钮已消失")

    

    # ------------------------------------------------------------------
    # 完整业务流程
    # ------------------------------------------------------------------

    def run_non_standard_flow(self, lyrics: str, song_title: str,
                              tab_index: int, action: str):
        """
        不规范歌词 AI 分析完整流程：
        1. 进入歌词模式，输入歌词和歌曲名
        2. 点击创建，处理可能出现的确认弹窗
        3. 等待 AI 分析弹窗（断言两个按钮可见）
        4. 切换分页（0=Formatting默认, 1=Refinement）
        5. 点击生成按钮（original / ai）
        6. 处理可能出现的确认弹窗

        :param lyrics:      歌词内容
        :param song_title:  歌曲名称
        :param tab_index:   0=Lyrics Formatting, 1=Lyrics Refinement
        :param action:      "original" 或 "ai"
        """
        self.switch_to_lyrics_tab()
        self.input_lyrics(lyrics)
        self.input_song_title(song_title)

        # 点击创建 → 先处理可能的确认弹窗 → 再等 AI 分析
        self.click_create()
        self.confirm_generation()
        self.wait_for_ai_analysis()

        # 切换分页
        self.switch_ai_tab(tab_index)

        # 修改被AI覆盖的歌名
        self.edit_generated_lyrics_title(song_title)

        # 选择生成方式
        if action == "original":
            self.select_original_version()
        else:
            self.select_create_now()

        # 点击生成后再次处理确认弹窗
        self.confirm_generation()

    # ------------------------------------------------------------------
    # 等待生成结果
    # ------------------------------------------------------------------

    def wait_for_generation_success(self, title: str, timeout: int = 600000):
        """等待歌曲生成成功（复用 TextPage 的轮询逻辑）"""
        from pages.text_page import TextPage
        tp = TextPage(self.page)
        return tp.wait_for_generation_success(title=title, timeout=timeout)

    def edit_ai_analysis_title(self, new_title: str):
        """在 AI 分析弹窗中直接修改被 AI 覆盖的歌名"""
        from config.locators import Locators
        logger.info("准备在 AI 分析弹窗中修改歌名")
        
        # 1. 点击编辑按钮
        self.page.locator(Locators.LYRICS_EDIT_BTN).dispatch_event("click")
        logger.info("点击了 AI 弹窗内的编辑按钮")
        
        # 2. 填入新歌名
        self.page.locator(Locators.LYRICS_TITLE_INPUT).fill(new_title)
        
        # 3. 点击保存按钮
        self.page.locator(Locators.LYRICS_EDIT_SAVE_BTN).dispatch_event("click")
        logger.info(f"成功在 AI 弹窗中将歌名修改保存为: {new_title}")
        self.page.wait_for_timeout(500)

    def run_model_generation_flow(self, model_name: str, model_locator: str):
        """通用底层模型切换生成辅助方法"""
        from utils import get_song
        from data.test_data import STANDARD_LYRICS
        from config.locators import Locators
        logger.info(f"开始执行歌词模式下的模型切换生成操作: {model_name}")
        
        # 1. 先切换模型
        self.model_version(model_locator)

        # 2. 输入歌词
        self.switch_to_lyrics_tab()
        self.input_lyrics(STANDARD_LYRICS)
        
        # 3. 输入歌名
        song_title = get_song()
        self.input_song_title(song_title)
        
        # 4. 点击创建
        self.click_create()

        # 5. ai分析窗口出现，断言特定元素
        logger.info("等待 AI 分析弹窗就绪...")
        self.wait_for_ai_analysis()

        # 6. 再次改歌名（在 AI 弹窗内）
        self.edit_ai_analysis_title(song_title)

        # 7. 最后点击创建 (这里用 Original Version 作为最终创建)
        self.select_original_version()
        self.confirm_generation()
        
        success = self.wait_for_generation_success(title=new_song_title)
        return success, new_song_title
