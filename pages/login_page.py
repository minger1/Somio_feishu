from playwright.sync_api import expect
from config.locators import Locators
from utils import logger
import re
from config import settings


class LoginPage:
    """封装登录 / 注册相关的页面操作"""

    def __init__(self, page):
        self.page = page

    def get_error_message(self, timeout: int = 2000) -> str:
        """获取页面显示的错误提示信息"""
        try:
            msg_locator = self.page.locator(Locators.MESSAGE_CONTENT)
            if msg_locator.is_visible(timeout=timeout):
                return msg_locator.inner_text().strip()
        except:
            pass
        return "未发现明显错误提示"

    def sign_up(self, email: str, password: str, timeout: int = 15000):
        """注册新账号并等待登录成功（头像出现）"""
        logger.info(f"正在进行注册流程 (Email: {email})")
        self.page.locator(Locators.LOGIN_BTN).first.click()
        self.page.locator(Locators.SIGNUP_LINK).click()
        self.page.fill(Locators.EMAIL_INPUT, email)
        self.page.fill(Locators.PASSWORD_INPUT, password)
        self.page.locator(Locators.SUBMIT_BTN).click()
        
        logger.info("注册信息已提交, 等待弹出邮箱验证窗口...")
        # Since locators.py uses modal-content, we wait for it.
        expect(self.page.locator(Locators.REGISTER_EMAIL_VERIFICATION_MODAL).last).to_be_visible(timeout=5000)
        logger.info(f"输入验证码: {settings.VERIFICATION_CODE}")
        
        # Check if there are multiple input boxes (e.g., 6 separate inputs)
        inputs = self.page.locator("//input[contains(@class, 'code-input')]")
        inputs.first.wait_for(state="visible", timeout=5000)
        count = inputs.count()
        if count >= 6:
            for i, char in enumerate(settings.VERIFICATION_CODE):
                inputs.nth(i).fill(char)
        else:
            inputs.first.fill(settings.VERIFICATION_CODE)
        
        # Now find the submit button explicitly and wait for it to be enabled.
        # We can use get_by_text or the locator from config.
        submit_btn = self.page.locator(Locators.REGISTER_SUBMIT_BTN).last
        try:
            # wait until it doesn't have the 'disabled' class before clicking
            expect(submit_btn).not_to_have_class(re.compile(r".*disabled.*"), timeout=5000)
            submit_btn.click(timeout=5000)
            logger.info("验证中心提交按钮已点击")
        except Exception as e:
            logger.warning(f"提交按钮点击报错或自动提交了: {e}")

        logger.info("验证码已提交, 正在验证注册并登录成功(预期出现用户头像)...")
        try:
            expect(self.page.locator(Locators.USER_AVATAR)).to_be_visible(timeout=timeout)
            logger.success("验证通过: 注册且登录成功")
        except Exception as e:
            err_msg = self.get_error_message()
            logger.error(f"注册验证失败! 页面提示: {err_msg}")
            raise e

    def login(self, email: str, password: str, timeout: int = 10000):
        """使用已有账号登录并等待登录成功"""
        logger.info(f"正在使用已有账号登录 (Email: {email})")
        self.page.locator(Locators.LOGIN_BTN).click()
        self.page.fill(Locators.EMAIL_INPUT, email)
        self.page.fill(Locators.PASSWORD_INPUT, password)
        self.page.locator(Locators.SUBMIT_BTN).click()
        logger.info("登录表单已提交, 正在验证登录成功(预期出现用户头像)...")
        try:
            expect(self.page.locator(Locators.USER_AVATAR)).to_be_visible(timeout=timeout)
            logger.success("验证通过: 登录成功")
        except Exception as e:
            err_msg = self.get_error_message()
            logger.error(f"登录验证失败! 页面提示: {err_msg}")
            raise e

    def is_logged_in(self, timeout: int = 5000) -> bool:
        """检查当前是否已登录（头像是否可见）"""
        return self.page.locator(Locators.USER_AVATAR).is_visible()

    def forgot_password(self, email: str, timeout: int = 5000):
        """测试忘记密码发送邮件流程"""
        logger.info(f"正在申请找回密码 (Email: {email})")
        self.page.locator(Locators.LOGIN_BTN).click()
        self.page.locator(Locators.FORGOT_PWD_LINK).click()
        self.page.fill(Locators.FORGOT_EMAIL_INPUT, email)
        self.page.locator(Locators.SUBMIT_BTN).click()
        logger.info("找回密码表单已提交, 正在验证是否出现成功提示信息...")
        expect(self.page.locator(Locators.MESSAGE_CONTENT)).to_be_visible(timeout=timeout)
        logger.success("验证通过: 成功提示信息已显示")
