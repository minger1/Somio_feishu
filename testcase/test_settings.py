import pytest
from playwright.sync_api import expect
from pages.settings_page import SettingsPage
from config.locators import Locators
from utils.logger import logger

class TestSettings:
    """测试右上角设置 (Settings) 下拉菜单的各项功能"""

    @pytest.fixture(autouse=True)
    def setup_settings(self, logged_in_page):
        """每个测试前，加载页面并初始化 SettingsPage"""
        self.page = logged_in_page
        self.settings = SettingsPage(self.page)

    def test_open_close_settings_dropdown(self):
        """测试设置下拉菜单的打开和关闭"""
        logger.info("测试打开设置下拉菜单")
        self.settings.open_settings()
        assert self.settings.is_settings_dropdown_visible(), "设置下拉菜单未正常展示"
        
        logger.info("测试使用 Escape 键关闭设置下拉菜单")
        self.settings.close_settings_by_escape()
        assert not self.settings.is_settings_dropdown_visible(), "设置下拉菜单未关闭"

    def test_invite_and_earn_modal(self):
        """测试 Invite & Earn 弹窗的打开与关闭"""
        logger.info("测试 Invite & Earn 弹窗功能")
        self.settings.open_settings()
        self.settings.click_invite_earn()
        
        # 验证弹窗出现
        self.settings.wait_for_invite_modal()
        assert self.page.locator(Locators.SETTING_INVITE_MODAL).is_visible(), "Invite & Earn 弹窗未显示"
        
        # 测试复制链接按钮 (验证元素存在即可)
        copy_btn = self.page.locator(Locators.SETTING_INVITE_COPY_BTN).first
        assert copy_btn.is_visible(), "Invite & Earn 弹窗中的复制按钮未找到"

        # 关闭弹窗
        self.settings.close_invite_modal()
        self.page.wait_for_selector(Locators.SETTING_INVITE_MODAL, state="hidden", timeout=3000)
        logger.success("Invite & Earn 弹窗测试完毕")

    def test_feedback_modal_options(self):
        """测试 Feedback 弹窗及反馈选项"""
        logger.info("测试 Feedback 弹窗及选项")
        self.settings.open_settings()
        self.settings.click_feedback()
        
        # 验证弹窗出现
        self.settings.wait_for_feedback_modal()
        assert self.settings.is_feedback_modal_visible(), "Feedback 弹窗未显示"
        
        # 验证选项数量 (至少要有选项)
        count = self.settings.get_feedback_option_count()
        assert count > 0, "Feedback 弹窗中没有找到反馈选项"
        
        # 点击某个选项作为测试 (例如第 1 个)
        self.settings.select_feedback_option(1)
        
        # 关闭弹窗
        self.settings.close_feedback_modal()
        self.page.wait_for_selector(Locators.SETTING_FEEDBACK_MODAL, state="hidden", timeout=3000)
        logger.success("Feedback 弹窗选项测试完毕")

    def test_feedback_modal_email_prefill(self):
        """测试 Feedback 弹窗邮箱是否已预填（针对已登录用户）"""
        logger.info("测试 Feedback 弹窗预填邮箱")
        self.settings.open_settings()
        self.settings.click_feedback()
        self.settings.wait_for_feedback_modal()
        
        # 验证邮箱是否预填且包含 @
        email_val = self.settings.get_feedback_email_value()
        logger.info(f"预填的邮箱值为: {email_val}")
        assert "@" in email_val, f"未正确预填登录邮箱，当前值为: '{email_val}'"
        
        self.settings.close_feedback_modal()
        logger.success("Feedback 弹窗预填邮箱测试完毕")

    def test_contact_us_external_link(self):
        """测试 Contact Us 点击后打开新页面"""
        logger.info("测试 Contact Us 跳转")
        self.settings.open_settings()
        new_page = self.settings.click_contact_us()
        
        logger.info(f"新页面 URL: {new_page.url}")
        assert new_page.url, "Contact Us 未能成功打开新页面"
        new_page.close()
        logger.success("Contact Us 跳转测试完毕")

    def test_faq_external_link(self):
        """测试 FAQ 点击后打开新页面"""
        logger.info("测试 FAQ 跳转")
        self.settings.open_settings()
        new_page = self.settings.click_faq()
        
        logger.info(f"新页面 URL: {new_page.url}")
        assert new_page.url, "FAQ 未能成功打开新页面"
        new_page.close()
        logger.success("FAQ 跳转测试完毕")

    def test_privacy_policy_external_link(self):
        """测试 Privacy Policy 点击后打开新页面"""
        logger.info("测试 Privacy Policy 跳转")
        self.settings.open_settings()
        new_page = self.settings.click_privacy_policy()
        
        logger.info(f"新页面 URL: {new_page.url}")
        assert new_page.url, "Privacy Policy 未能成功打开新页面"
        new_page.close()
        logger.success("Privacy Policy 跳转测试完毕")

    def test_terms_of_service_external_link(self):
        """测试 Terms of Service 点击后打开新页面"""
        logger.info("测试 Terms of Service 跳转")
        self.settings.open_settings()
        new_page = self.settings.click_terms_of_service()
        
        logger.info(f"新页面 URL: {new_page.url}")
        assert new_page.url, "Terms of Service 未能成功打开新页面"
        new_page.close()
        logger.success("Terms of Service 跳转测试完毕")
