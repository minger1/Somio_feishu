from playwright.sync_api import expect
from utils import generate_email
from config.settings import LOGIN_EMAIL, LOGIN_PASSWORD
from config.locators import Locators
from pages.login_page import LoginPage
from utils import logger

class TestLoginSuite:
    def test_sign_up_success(self, page, lang_urls):
        """测试新用户注册成功"""
        page.goto(lang_urls['generate_url'])
        email = generate_email()
        login = LoginPage(page)
        login.sign_up(email, "123456")

    def test_login_success(self, page, lang_urls):
        """测试正确账号密码登录成功"""
        page.goto(lang_urls['generate_url'])
        login = LoginPage(page)
        login.login(LOGIN_EMAIL, LOGIN_PASSWORD)

    def test_forgot_password_success(self, page, lang_urls):
        """测试忘记密码发送邮件成功"""
        page.goto(lang_urls['generate_url'])
        login = LoginPage(page)
        login.forgot_password(LOGIN_EMAIL)