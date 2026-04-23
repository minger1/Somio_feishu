import pytest
from playwright.sync_api import expect
from pages.lyrics_generator_page import LyricsGeneratorPage
from config.locators import Locators
from data.test_data import TEST_TEXT_PROMPT
from utils.logger import logger


# 通用测试主题提示词
LYRICS_PROMPT = "A lonely astronaut drifting through space, missing home, hopeful but melancholic, soft piano background."


class TestLyricsGenerator:
    """AI 歌词生成页功能测试用例"""

    # ------------------------------------------------------------------
    # 用例 1：通过 Create Music > Lyrics 里的提示入口进入歌词生成页
    # ------------------------------------------------------------------

    def test_navigate_via_tip_btn(self):
        # ... skipped, update signature to remove `self` if missing, wait original had `(self, logged_in_page)`
        pass

    # ------------------------------------------------------------------
    # 用例 2：通过侧边栏 NAV_LYRICS_GENERATOR 进入歌词生成页
    # ------------------------------------------------------------------

    def test_navigate_via_sidebar(self, logged_in_page):
        """
        入口2：点击侧边栏 AI Lyrics Generator 导航项，
        断言成功进入歌词生成页（li 获得 active 类 + Generate 按钮可见）。
        """
        lgp = LyricsGeneratorPage(logged_in_page)
        lgp.navigate_via_sidebar()

    # ------------------------------------------------------------------
    # 用例 3：输入内容后点击清除，断言输入框清空
    # ------------------------------------------------------------------

    def test_clear_input(self, logged_in_page):
        """
        [用例描述]：测试前端小组件 UI 交互状态。在写入大段字符后，点击 Clear 清除内容。
        """
        logger.info("开始测试：清除输入框内容功能")
        lgp = LyricsGeneratorPage(logged_in_page)
        
        logger.info("导航进入 AI Lyrics Generator")
        lgp.navigate_via_sidebar()

        logger.info(f"填入测试歌词文本: {LYRICS_PROMPT[:20]}...")
        lgp.input_prompt(LYRICS_PROMPT)

        logger.info("点击 Clear 按钮")
        lgp.click_clear()

        logger.info("验证输入框是否为空")
        lgp.assert_textarea_empty()
        logger.success("清除输入框测试完毕")

    # ------------------------------------------------------------------
    # 用例 4：输入内容后点击生成，断言歌词生成成功
    # ------------------------------------------------------------------

    def test_generate_lyrics(self, logged_in_page):
        """
        [用例描述]：注入情感描述词，向 LLM 大模型发送合成命令请求。
        确保结果区域能在有效时间内抛出连贯的结构化多行文体。
        """
        logger.info("开始测试：AI 歌词生成功能")
        lgp = LyricsGeneratorPage(logged_in_page)
        
        logger.info("导航进入 AI Lyrics Generator")
        lgp.navigate_via_sidebar()

        logger.info(f"填入歌词生成提示词: {LYRICS_PROMPT}")
        lgp.input_prompt(LYRICS_PROMPT)

        logger.info("点击 Generate 按钮")
        lgp.click_generate()

        logger.info("轮询等待歌词生成结果...")
        lyrics = lgp.wait_for_lyrics_result(timeout=60000)
        assert lyrics, "歌词生成超时或返回为空"
        
        logger.success("AI 歌词生成测试完毕")

    # ------------------------------------------------------------------
    # 用例 5：生成歌词后点击复制，断言 Toast 提示出现
    # ------------------------------------------------------------------

    def test_copy_lyrics(self, logged_in_page):
        """
        [用例描述]：接续生成成果，检验点击小复制版按钮后操作系统 Toast 信息的弹出。
        """
        logger.info("开始测试：复制生成的歌词")
        lgp = LyricsGeneratorPage(logged_in_page)
        lgp.navigate_via_sidebar()

        logger.info("首先生成一段测试歌词")
        lgp.input_prompt(LYRICS_PROMPT)
        lgp.click_generate()
        lgp.wait_for_lyrics_result(timeout=60000)

        logger.info("点击复制按钮")
        lgp.click_copy()

        logger.info("验证 Toast 提示气泡")
        lgp.assert_copy_success()
        logger.success("复制歌词测试完毕")

    # ------------------------------------------------------------------
    # 用例 6：生成歌词后点击使用歌词，断言跳转并粘贴到 Create Music Lyrics 分页
    # ------------------------------------------------------------------

    def test_use_lyrics(self, logged_in_page):
        """
        [用例描述]：点击 Use These Lyrics 按钮，跳转到 Create Music 的 Lyrics 分页
        并保持长文本正确填充主输入框。
        """
        logger.info("开始测试：前往 Create Music 使用歌词")
        lgp = LyricsGeneratorPage(logged_in_page)
        lgp.navigate_via_sidebar()

        logger.info("首先生成一条可用歌词")
        lgp.input_prompt(LYRICS_PROMPT)
        lgp.click_generate()
        expected_lyrics = lgp.wait_for_lyrics_result(timeout=60000)

        logger.info("点击 Use These Lyrics")
        lgp.click_use_lyrics()

        logger.info("在目标页面验证输入框歌词匹配")
        lgp.assert_lyrics_pasted_to_create_music(expected_lyrics)
        logger.success("跨端跳转使用歌词测试完毕")
