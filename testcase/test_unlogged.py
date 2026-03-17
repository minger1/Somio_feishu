import pytest
import re
from playwright.sync_api import expect
from locators import Locators
from pages.text_page import TextPage
from logger import logger

class TestUnloggedSuite:
    """未登录状态下的限制与引导测试"""

    @pytest.fixture(autouse=True)
    def setup(self, page, lang_urls):
        """每个用例开始前导航到首页"""
        page.goto(lang_urls['base_url'])
        self.text_page = TextPage(page)

    def test_unlogged_v5_limit(self, page):
        """1、选择V5，弹出限制弹窗"""
        logger.info("测试未登录选择 V5 模型...")
        self.text_page.model_version(Locators.MODEL_VERSION_V5)
        expect(page.locator(Locators.LIMIT_DIALOG)).to_be_visible(timeout=5000)
        logger.success("限制弹窗已弹出")

    def test_unlogged_v4_5_plus_limit(self, page):
        """2、选择V4.5+，弹出限制弹窗"""
        logger.info("测试未登录选择 V4.5+ 模型...")
        self.text_page.model_version(Locators.MODEL_VERSION_V4_5_PLUS)
        expect(page.locator(Locators.LIMIT_DIALOG)).to_be_visible(timeout=5000)
        logger.success("限制弹窗已弹出")

    def test_unlogged_v4_5_limit(self, page):
        """3、选择V4.5，弹出限制弹窗"""
        logger.info("测试未登录选择 V4.5 模型...")
        self.text_page.model_version(Locators.MODEL_VERSION_V4_5)
        expect(page.locator(Locators.LIMIT_DIALOG)).to_be_visible(timeout=5000)
        logger.success("限制弹窗已弹出")

    def test_unlogged_input_create_redirect(self, page):
        """4、文本模式下输入框输入文本，点击创作按钮，弹出登录窗口"""
        logger.info("测试输入文本并点击创作是否弹出登录窗口...")
        self.text_page.text_input("Test unlogged creation")
        page.locator(Locators.CREATE_BTN).click()
        expect(page.locator(Locators.LOGIN_MODAL)).to_be_visible(timeout=5000)
        logger.success("登录窗口已弹出")

    def test_unlogged_v5_limit_close(self, page):
        """5、未登录选择V5，弹出限制弹窗，点击关闭"""
        logger.info("测试关闭限制弹窗...")
        self.text_page.model_version(Locators.MODEL_VERSION_V5)
        expect(page.locator(Locators.LIMIT_DIALOG)).to_be_visible(timeout=5000)
        self.text_page.close_limit_dialog()
        expect(page.locator(Locators.LIMIT_DIALOG)).to_be_hidden()
        logger.success("限制弹窗已成功关闭")

    def test_unlogged_v5_limit_buy(self, page):
        """6、未登录选择V5，弹出限制弹窗，点击购买，进入价格页"""
        logger.info("测试点击升级按钮进入价格页...")
        self.text_page.model_version(Locators.MODEL_VERSION_V5)
        expect(page.locator(Locators.LIMIT_DIALOG)).to_be_visible(timeout=5000)
        
        # 使用 expect_popup 捕获新打开的标签页
        with page.expect_popup() as popup_info:
            self.text_page.click_limit_upgrade()
        new_page = popup_info.value
        
        # 验证新页面的 URL 是否包含 /pricing/music-generator/
        expect(new_page).to_have_url(re.compile(r".*/pricing/music-generator/.*"), timeout=15000)
        logger.success("已成功在新标签页跳转至价格页")

    def test_unlogged_v5_limit_login(self, page):
        """7、未登录选择v5，弹出限制弹窗，点击登录，弹出登录窗口"""
        logger.info("测试点击登录按钮弹出登录窗口...")
        self.text_page.model_version(Locators.MODEL_VERSION_V5)
        expect(page.locator(Locators.LIMIT_DIALOG)).to_be_visible(timeout=5000)
        self.text_page.click_limit_login()
        expect(page.locator(Locators.LOGIN_MODAL)).to_be_visible(timeout=5000)
        logger.success("从限制弹窗成功唤起登录窗口")

