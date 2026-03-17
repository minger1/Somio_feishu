from playwright.sync_api import expect
from utils import generate_email
from config import LOGIN_EMAIL, LOGIN_PASSWORD
from locators import Locators
from pages.login_page import LoginPage
from logger import logger

class TestLoginSuite:
    def test_sign_up_success(self, page, lang_urls):
        """测试新用户注册成功"""
        page.goto(lang_urls['base_url'])
        email = generate_email()
        login = LoginPage(page)
        login.sign_up(email, "123456")

    def test_login_success(self, page, lang_urls):
        """测试正确账号密码登录成功"""
        page.goto(lang_urls['base_url'])
        login = LoginPage(page)
        login.login(LOGIN_EMAIL, LOGIN_PASSWORD)

    def test_forgot_password_success(self, page, lang_urls):
        """测试忘记密码发送邮件成功"""
        page.goto(lang_urls['base_url'])
        page.locator(Locators.LOGIN_BTN).click()
        page.locator(Locators.FORGOT_PWD_LINK).click()
        page.fill(Locators.FORGOT_EMAIL_INPUT, LOGIN_EMAIL)
        page.locator(Locators.SUBMIT_BTN).click()
        logger.info("找回密码表单已提交, 正在验证是否出现成功提示信息...")
        # 注意：这里可能由于邮箱未注册报错，但逻辑是对的
        expect(page.locator(Locators.MESSAGE_CONTENT)).to_be_visible(timeout=5000)
        logger.success("验证通过: 成功提示信息已显示")