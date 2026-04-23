from playwright.sync_api import expect
from config.locators import Locators
from utils import logger


class LyricsGeneratorPage:
    """封装 AI 歌词生成页（侧边栏 AI Lyrics Generator）的所有操作"""

    def __init__(self, page):
        self.page = page

    # ------------------------------------------------------------------
    # 导航入口
    # ------------------------------------------------------------------

    def navigate_via_sidebar(self):
        """
        通过侧边栏 NAV_LYRICS_GENERATOR 进入歌词生成页，
        断言侧边栏激活状态 + Generate 按钮可见。
        """
        self.page.locator(Locators.NAV_LYRICS_GENERATOR).click()
        self.page.wait_for_timeout(1000)
        expect(self.page.locator(Locators.LYRICS_GENERATOR_ACTIVE)).to_be_visible(timeout=5000)
        expect(self.page.locator(Locators.LYRICS_GENERATOR_CREATE_BTN)).to_be_visible(timeout=5000)
        logger.success("通过侧边栏成功进入 AI 歌词生成页")

    def navigate_via_tip_btn(self):
        """
        通过 Create Music > Lyrics 分页的提示入口（GENNERATE_LYRICS_TIP_BTN）进入歌词生成页，
        断言 Generate 按钮可见。
        """
        # 切换到歌词分页
        self.page.locator(Locators.LYRICS_TAB).click()
        self.page.wait_for_timeout(500)
        # 点击提示入口
        self.page.locator(Locators.GENNERATE_LYRICS_TIP_BTN).click()
        self.page.wait_for_timeout(1000)
        expect(self.page.locator(Locators.LYRICS_GENERATOR_ACTIVE)).to_be_visible(timeout=5000)
        expect(self.page.locator(Locators.LYRICS_GENERATOR_CREATE_BTN)).to_be_visible(timeout=5000)
        logger.success("通过 Create Music > Lyrics 提示入口成功进入 AI 歌词生成页")

    # ------------------------------------------------------------------
    # 输入框操作
    # ------------------------------------------------------------------

    def input_prompt(self, text: str):
        """在歌词生成输入框输入主题内容"""
        textarea = self.page.locator(Locators.LYRICS_GENERATOR_TEXTAREA)
        textarea.fill(text)
        expect(textarea).to_have_value(text, timeout=5000)
        logger.info(f"歌词生成页输入内容: {text[:30]}...")

    def click_clear(self):
        """点击清除按钮，清空输入框内容"""
        self.page.locator(Locators.LYRICS_GENERATOR_CLEAR_BTN).click()
        logger.info("点击了清除按钮")

    def assert_textarea_empty(self):
        """断言输入框内容已清空"""
        expect(self.page.locator(Locators.LYRICS_GENERATOR_TEXTAREA)).to_have_value("", timeout=5000)
        logger.success("断言输入框已清空 ✓")

    # ------------------------------------------------------------------
    # 生成操作
    # ------------------------------------------------------------------

    def click_generate(self):
        """点击 Generate 按钮，触发歌词生成"""
        self.page.locator(Locators.LYRICS_GENERATOR_CREATE_BTN).click()
        logger.info("点击了 Generate 按钮")

    def wait_for_lyrics_result(self, timeout: int = 60000):
        """
        等待歌词生成结果出现。
        结果渲染在 .content_top 区域（blank 提示文字消失，生成内容出现）。
        返回生成的歌词文本内容。
        """
        logger.info("等待歌词生成结果...")
        # 等待生成中状态消失（Generate 按钮可能变成 loading 状态）
        # 等待结果区域出现内容（blank 提示消失）
        result_area = self.page.locator(".lyrics-generator-wrapper .content_top")
        expect(result_area).not_to_contain_text(
            "Enter your creative ideas below", timeout=timeout
        )
        lyrics_text = result_area.inner_text().strip()
        assert lyrics_text, "歌词生成结果为空"
        logger.success(f"歌词生成成功，内容前30字符: {lyrics_text[:30]}...")
        return lyrics_text

    # ------------------------------------------------------------------
    # 结果区域操作
    # ------------------------------------------------------------------

    def click_copy(self):
        """点击复制按钮"""
        self.page.locator(Locators.LYRICS_GENERATOR_COPY_BTN).click()
        logger.info("点击了复制按钮")

    def assert_copy_success(self):
        """断言复制成功的 Toast 消息出现"""
        toast = self.page.locator(Locators.COPY_SUCCESS_TOAST)
        expect(toast).to_be_visible(timeout=5000)
        logger.success("断言复制成功 Toast 已出现 ✓")

    def click_use_lyrics(self):
        """点击使用歌词按钮，跳转到 Create Music Lyrics 分页"""
        self.page.locator(Locators.LYRICS_GENERATOR_USE_LYRICS_BTN).click()
        logger.info("点击了使用歌词按钮")

    def assert_lyrics_pasted_to_create_music(self, expected_lyrics: str):
        """
        断言跳转到 Create Music Lyrics 分页，
        并且生成的歌词已粘贴到 Lyrics 输入框。
        """
        import re
        # 断言 workbench-wrapper 重新显示（Create Music 区域变可见）
        expect(self.page.locator(".workbench-wrapper")).to_be_visible(timeout=5000)
        # 断言当前在 Lyrics 分页（Lyrics tab 含 active class）
        expect(self.page.locator(Locators.LYRICS_TAB)).to_have_class(
            re.compile(r"active"), timeout=5000
        )
        # 断言 Lyrics 输入框有内容
        textarea = self.page.locator(Locators.LYRICS_CONTENT_TEXTAREA).first
        expect(textarea).not_to_have_value("", timeout=5000)
        # 进一步验证歌词内容有实质性内容（至少10个字符）
        lyrics_value = textarea.input_value()
        assert len(lyrics_value) > 10, f"粘贴的歌词内容异常，长度仅为: {len(lyrics_value)}"
        logger.success(f"断言歌词已粘贴到 Create Music Lyrics 输入框 ✓，内容前30字: {lyrics_value[:30]}...")
