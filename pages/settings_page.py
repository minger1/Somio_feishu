from playwright.sync_api import Page, expect
from config.locators import Locators
from utils.logger import logger


class SettingsPage:
    """封装右上角设置下拉菜单及各子功能的操作"""

    def __init__(self, page: Page):
        self.page = page

    # ====== 设置下拉菜单 ======

    def open_settings(self):
        """点击设置齿轮图标，展开设置下拉菜单"""
        logger.info("点击设置齿轮图标")
        self.page.locator(Locators.SETTING_BTN).click()
        self.page.wait_for_timeout(400)

    def close_settings_by_escape(self):
        """按 Escape 键关闭设置下拉菜单"""
        logger.info("按 Escape 关闭设置下拉菜单")
        self.page.keyboard.press("Escape")
        self.page.wait_for_timeout(300)

    def close_settings_by_clicking_outside(self):
        """点击页面空白处关闭设置下拉菜单"""
        logger.info("点击页面空白区域关闭设置菜单")
        self.page.mouse.click(10, 10)
        self.page.wait_for_timeout(300)

    def is_settings_dropdown_visible(self) -> bool:
        """判断设置下拉菜单是否可见"""
        return self.page.locator(Locators.SETTING_DROPDOWN).is_visible()

    # ====== 语言切换入口 ======

    def hover_language_menu(self):
        """悬停在 Language 子菜单入口，等待子菜单展开"""
        logger.info("悬停在 Language 子菜单入口")
        self.page.locator(Locators.SETTING_LANGUAGE).hover()
        self.page.wait_for_timeout(400)

    # ====== Invite & Earn ======

    def click_invite_earn(self):
        """点击 Invite & Earn 菜单项"""
        logger.info("点击 Invite & Earn")
        self.page.locator(Locators.SETTING_INVITE).click()
        self.page.wait_for_timeout(800)

    def wait_for_invite_modal(self, timeout: int = 5000):
        """等待 Invite & Earn 弹窗出现（支持多种 class 名变体）"""
        logger.info("等待 Invite & Earn 弹窗出现")
        self.page.wait_for_selector(
            Locators.SETTING_INVITE_MODAL,
            state="visible", timeout=timeout
        )

    def close_invite_modal(self):
        """点击 ✕ 关闭 Invite & Earn 弹窗"""
        logger.info("关闭 Invite & Earn 弹窗")
        self.page.locator(Locators.SETTING_INVITE_MODAL_CLOSE).first.click()
        self.page.wait_for_timeout(400)

    # ====== Feedback ======

    def click_feedback(self):
        """打开设置菜单并点击 Feedback 菜单项"""
        logger.info("点击 Feedback 菜单项")
        self.page.locator(Locators.SETTING_FEEDBACK).click()
        self.page.wait_for_timeout(800)

    def wait_for_feedback_modal(self, timeout: int = 5000):
        """等待 Feedback 弹窗出现"""
        logger.info("等待 Feedback 弹窗出现")
        self.page.wait_for_selector(
            Locators.SETTING_FEEDBACK_MODAL,
            state="visible", timeout=timeout
        )

    def is_feedback_modal_visible(self) -> bool:
        """判断 Feedback 弹窗是否可见"""
        return self.page.locator(Locators.SETTING_FEEDBACK_MODAL).first.is_visible()

    def close_feedback_modal(self):
        """点击 ✕ 关闭 Feedback 弹窗"""
        logger.info("关闭 Feedback 弹窗")
        self.page.locator(Locators.SETTING_FEEDBACK_MODAL_CLOSE).first.click()
        self.page.wait_for_timeout(400)

    def get_feedback_option_count(self) -> int:
        """获取 Feedback 弹窗中反馈类型选项数量"""
        count = self.page.locator(Locators.SETTING_FEEDBACK_OPTION_ITEMS).count()
        logger.info(f"Feedback 选项数量: {count}")
        return count

    def select_feedback_option(self, index: int):
        """选择 Feedback 弹窗中的第 index 个选项（1-based）"""
        logger.info(f"选择 Feedback 选项 [{index}]")
        options = self.page.locator(Locators.SETTING_FEEDBACK_OPTION_ITEMS)
        count = options.count()
        assert count >= index, f"选项数量不足，期望 >= {index}，实际 {count}"
        options.nth(index - 1).click()
        self.page.wait_for_timeout(300)

    def fill_feedback_description(self, text: str):
        """填写 Feedback 详细描述文本框"""
        logger.info(f"填写 Feedback 描述: {text}")
        self.page.locator(Locators.SETTING_FEEDBACK_TEXTAREA).fill(text)

    def fill_feedback_email(self, email: str):
        """填写 Feedback 联系邮箱"""
        logger.info(f"填写 Feedback 邮箱: {email}")
        self.page.locator(Locators.SETTING_FEEDBACK_EMAIL_INPUT).fill(email)

    def get_feedback_email_value(self) -> str:
        """获取 Feedback 邮箱输入框当前值"""
        return self.page.locator(Locators.SETTING_FEEDBACK_EMAIL_INPUT).input_value()

    def submit_feedback(self):
        """点击 Submit 提交 Feedback"""
        logger.info("提交 Feedback")
        self.page.locator(Locators.SETTING_FEEDBACK_SUBMIT_BTN).click()
        self.page.wait_for_timeout(1500)

    # ====== 外链跳转菜单项 ======

    def click_contact_us(self):
        """点击 Contact Us（将在新标签页打开外部链接）"""
        logger.info("点击 Contact Us")
        with self.page.context.expect_page() as new_page_info:
            self.page.locator(Locators.SETTING_CONTACT_US).click()
        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded", timeout=15000)
        return new_page

    def click_faq(self):
        """点击 FAQ（将在新标签页打开外部链接）"""
        logger.info("点击 FAQ")
        with self.page.context.expect_page() as new_page_info:
            self.page.locator(Locators.SETTING_FAQ).click()
        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded", timeout=15000)
        return new_page

    def click_privacy_policy(self):
        """点击 Privacy Policy（将在新标签页打开外部链接）"""
        logger.info("点击 Privacy Policy")
        with self.page.context.expect_page() as new_page_info:
            self.page.locator(Locators.SETTING_PRIVACY).click()
        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded", timeout=15000)
        return new_page

    def click_terms_of_service(self):
        """点击 Terms of Service（将在新标签页打开外部链接）"""
        logger.info("点击 Terms of Service")
        with self.page.context.expect_page() as new_page_info:
            self.page.locator(Locators.SETTING_TERMS).click()
        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded", timeout=15000)
        return new_page
