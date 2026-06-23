import pytest
from pages.price_page import PricePage
from pages.login_page import LoginPage
from config.settings import (
    LOGIN_EMAIL,
    PROMO_CODE,
    SIGNUP_PASSWORD,
    FREE_EMAIL,
    FREE_PASSWORD,
)
from utils import logger, generate_email


# =====================================================================
# 测试套件一：订阅套餐 → 仅验证能进入 Stripe 收银台
# =====================================================================

class TestSubscribeStripeRedirect:
    """
    订阅套餐（月付 / 年付）购买入口测试。

    每个用例独立持有 logged_in_page（function 作用域），
    通过私有 helper _go_to_subscribe_tab() 统一初始化 PricePage 并导航到价格页。
    不使用 autouse fixture，遵循项目中直接注入 fixture 的编码规范。
    """

    def _go_to_subscribe_tab(self, logged_in_page, yearly: bool = False) -> PricePage:
        """
        公共前置：创建 PricePage → 导航价格页 → 切换到指定订阅 Tab。

        :param logged_in_page: 已登录的 Page 对象
        :param yearly: True 切换年付 Tab，False 切换月付 Tab
        :return: 已处于目标 Tab 的 PricePage 对象
        """
        price_page = PricePage(logged_in_page)
        price_page.navigate_to_pricing_direct()
        if yearly:
            price_page.switch_to_yearly()
        else:
            price_page.switch_to_monthly()
        return price_page

    # ---------- 月付订阅 ----------

    def test_subscribe_monthly_basic_redirects_to_stripe(self, logged_in_page):
        """[订阅-月付] Basic 套餐购买 → 成功跳转 Stripe"""
        price_page = self._go_to_subscribe_tab(logged_in_page)
        price_page.click_subscribe_basic()
        assert price_page.wait_for_stripe_redirect(timeout=20000), \
            "Basic 月付订阅购买后未能成功跳转至 Stripe 结算页"

    def test_subscribe_monthly_standard_redirects_to_stripe(self, logged_in_page):
        """[订阅-月付] Standard 套餐购买 → 成功跳转 Stripe"""
        price_page = self._go_to_subscribe_tab(logged_in_page)
        price_page.click_subscribe_standard()
        assert price_page.wait_for_stripe_redirect(timeout=20000), \
            "Standard 月付订阅购买后未能成功跳转至 Stripe 结算页"

    def test_subscribe_monthly_pro_redirects_to_stripe(self, logged_in_page):
        """[订阅-月付] Pro 套餐购买 → 成功跳转 Stripe"""
        price_page = self._go_to_subscribe_tab(logged_in_page)
        price_page.click_subscribe_pro()
        assert price_page.wait_for_stripe_redirect(timeout=20000), \
            "Pro 月付订阅购买后未能成功跳转至 Stripe 结算页"

    # ---------- 年付订阅 ----------

    def test_subscribe_yearly_basic_redirects_to_stripe(self, logged_in_page):
        """[订阅-年付] Basic 套餐购买 → 成功跳转 Stripe"""
        price_page = self._go_to_subscribe_tab(logged_in_page, yearly=True)
        price_page.click_subscribe_basic()
        assert price_page.wait_for_stripe_redirect(timeout=20000), \
            "Basic 年付订阅购买后未能成功跳转至 Stripe 结算页"

    def test_subscribe_yearly_standard_redirects_to_stripe(self, logged_in_page):
        """[订阅-年付] Standard 套餐购买 → 成功跳转 Stripe"""
        price_page = self._go_to_subscribe_tab(logged_in_page, yearly=True)
        price_page.click_subscribe_standard()
        assert price_page.wait_for_stripe_redirect(timeout=20000), \
            "Standard 年付订阅购买后未能成功跳转至 Stripe 结算页"

    def test_subscribe_yearly_pro_redirects_to_stripe(self, logged_in_page):
        """[订阅-年付] Pro 套餐购买 → 成功跳转 Stripe"""
        price_page = self._go_to_subscribe_tab(logged_in_page, yearly=True)
        price_page.click_subscribe_pro()
        assert price_page.wait_for_stripe_redirect(timeout=20000), \
            "Pro 年付订阅购买后未能成功跳转至 Stripe 结算页"


# =====================================================================
# 测试套件二：一次性套餐 Pro 完整购买流程
# =====================================================================

class TestOnetimePurchaseFlow:
    """
    一次性套餐 Pro 完整购买流程测试。

    使用 price_page.go_to_onetime_pro_stripe() 封装进入 Stripe 的操作，
    使用 stripe.complete_purchase() 封装填邮箱 + 优惠码 + 提交支付的操作，
    各场景只需关注「邮箱填写策略」和「感谢页断言差异」。
    """

    def test_onetime_pro_logged_in_new_account(self, page, lang_urls):
        """
        [场景 A] 已登录新注册账号购买一次性 Pro 套餐

        注册全新邮箱账号后立即购买。通过注册流程创建的账号已有密码，
        也需要在 Stripe 中填写注册邮箱，感谢页不返回初始密码（密码框隐藏）。
        """
        logger.info("=== 场景 A: 已登录新注册账号购买 ===")
        new_email = generate_email()
        logger.info(f"注册新账号: {new_email}")

        # 注册并自动登录
        LoginPage(page).sign_up(new_email, SIGNUP_PASSWORD)

        # 进入 Stripe 并购买（传入已登录的新账号邮箱）
        stripe = PricePage(page).go_to_onetime_pro_stripe()
        stripe.complete_purchase(PROMO_CODE, email=new_email)
        stripe.assert_thank_you_page()
        stripe.assert_billing_email(new_email)
        stripe.assert_password_hidden()
        logger.success("=== 场景 A 通过 ===")

    def test_onetime_pro_unlogged_registered_email(self, page, lang_urls):
        """
        [场景 B] 未登录，在 Stripe 中填写已注册邮箱购买

        未登录状态直接进入价格页，在 Stripe 邮箱框填写已注册账号的邮箱。
        Somio 识别到邮箱已有账号，感谢页密码框隐藏（无需返回初始密码）。
        使用主测试账号 LOGIN_EMAIL 作为「已注册邮箱」。
        """
        logger.info("=== 场景 B: 未登录，用已注册邮箱购买 ===")

        # 未登录状态进入 Stripe（传入已注册邮箱）
        stripe = PricePage(page).go_to_onetime_pro_stripe()
        stripe.complete_purchase(PROMO_CODE, email=LOGIN_EMAIL)
        stripe.assert_thank_you_page()
        stripe.assert_billing_email(LOGIN_EMAIL)
        stripe.assert_password_hidden()
        logger.success("=== 场景 B 通过 ===")

    def test_onetime_pro_unlogged_new_email(self, page, lang_urls):
        """
        [场景 C] 未登录，在 Stripe 中填写全新未注册邮箱购买

        未登录状态用从未在 Somio 注册过的邮箱购买。
        Somio 自动创建该邮箱账号，感谢页密码框可见，
        并显示以 'somioai' 开头的系统生成初始密码。
        """
        logger.info("=== 场景 C: 未登录，用未注册邮箱购买 ===")
        brand_new_email = generate_email()
        logger.info(f"使用全新邮箱: {brand_new_email}")

        stripe = PricePage(page).go_to_onetime_pro_stripe()
        stripe.complete_purchase(PROMO_CODE, email=brand_new_email)
        stripe.assert_thank_you_page()
        stripe.assert_billing_email(brand_new_email)
        # 全新邮箱首次购买：Somio 自动注册并在感谢页返回初始密码
        stripe.assert_password_visible()
        logger.info(f"系统为新用户生成的初始密码: {stripe.get_initial_password()}")
        logger.success("=== 场景 C 通过 ===")



# =====================================================================
# 测试套件三：一次性套餐各规格 → 仅验证能进入 Stripe 收银台
# =====================================================================

class TestOnetimeStripeRedirect:
    """
    一次性套餐（Lite / Basic / Standard / Pro）购买入口测试。

    通过私有 helper _go_to_onetime_tab() 统一导航到一次性 Tab，
    各用例只需调用不同规格的购买按钮方法。
    """

    def _go_to_onetime_tab(self, logged_in_page) -> PricePage:
        """公共前置：导航价格页 → 切换到一次性套餐 Tab"""
        price_page = PricePage(logged_in_page)
        price_page.navigate_to_pricing_direct()
        price_page.switch_to_onetime()
        return price_page

    def test_onetime_lite_redirects_to_stripe(self, logged_in_page):
        """[一次性-Lite] 购买入口 → 成功跳转 Stripe"""
        price_page = self._go_to_onetime_tab(logged_in_page)
        price_page.click_onetime_lite()
        assert price_page.wait_for_stripe_redirect(timeout=20000), \
            "一次性 Lite 套餐购买后未能跳转至 Stripe"

    def test_onetime_basic_redirects_to_stripe(self, logged_in_page):
        """[一次性-Basic] 购买入口 → 成功跳转 Stripe"""
        price_page = self._go_to_onetime_tab(logged_in_page)
        price_page.click_onetime_basic()
        assert price_page.wait_for_stripe_redirect(timeout=20000), \
            "一次性 Basic 套餐购买后未能跳转至 Stripe"

    def test_onetime_standard_redirects_to_stripe(self, logged_in_page):
        """[一次性-Standard] 购买入口 → 成功跳转 Stripe"""
        price_page = self._go_to_onetime_tab(logged_in_page)
        price_page.click_onetime_standard()
        assert price_page.wait_for_stripe_redirect(timeout=20000), \
            "一次性 Standard 套餐购买后未能跳转至 Stripe"

    def test_onetime_pro_redirects_to_stripe(self, logged_in_page):
        """[一次性-Pro] 购买入口 → 成功跳转 Stripe"""
        price_page = self._go_to_onetime_tab(logged_in_page)
        price_page.click_onetime_pro()
        assert price_page.wait_for_stripe_redirect(timeout=20000), \
            "一次性 Pro 套餐购买后未能跳转至 Stripe"


# =====================================================================
# 测试套件四：非会员限制与引导跳转测试
# =====================================================================

class TestFreeAccountModelLimit:
    """
    非会员账号（Free Account）模型使用限制与升级引导跳转测试。
    """

    def test_free_account_v5_5_limit_buy(self, page, lang_urls):
        """
        [非会员-V5.5限制] 登录非会员账号在音乐生成页切换到 V5.5 模型时，
        应弹出限制弹窗，点击升级/购买按钮后成功跳转到价格页。
        """
        from pages.text_page import TextPage
        from config.locators import Locators
        from playwright.sync_api import expect
        import re

        logger.info("=== 测试已登录非会员账号选择 V5.5 模型限制与升级跳转 ===")

        # 1. 登录非会员账号
        LoginPage(page).login(FREE_EMAIL, FREE_PASSWORD)

        # 2. 进入音乐生成页后选择 V5.5 模型
        text_page = TextPage(page)
        text_page.model_version(Locators.MODEL_VERSION_V5_5)

        # 3. 验证限制弹窗是否已弹出
        text_page.assert_limit_dialog_visible()

        # 4. 点击购买/升级按钮，并捕获弹出新页面的 URL 是否包含价格页地址
        with page.expect_popup() as popup_info:
            text_page.click_limit_upgrade()
        new_page = popup_info.value

        # 5. 断言新打开的页面是价格页
        expect(new_page).to_have_url(re.compile(r".*/pricing/music-generator/.*"), timeout=15000)
        logger.success("=== 非会员 V5.5 限制与购买跳转测试通过 ===")
