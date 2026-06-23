import re
import time
from playwright.sync_api import Page, expect
from config.locators import Locators
from utils import logger


class StripePage:
    """
    封装 Stripe 付款页面及购买后感谢页的所有操作与断言。
    """

    def __init__(self, page: Page):
        self.page = page

    # ==================== Stripe 页面操作 ====================

    def wait_for_stripe_load(self, timeout: int = 30000):
        """
        等待 Stripe 结算页面加载完成。
        以邮箱输入框出现作为加载完成的信号。
        """
        logger.info("等待 Stripe 结算页面加载完成...")
        expect(self.page.locator(Locators.STRIPE_EMAIL_INPUT)).to_be_visible(timeout=timeout)
        logger.success(f"Stripe 结算页已加载: {self.page.url}")

    def select_currency_usd(self):
        """
        在 Stripe 结算页切换至 USD 货币。
        若按钮不存在或已激活，则静默跳过。
        """
        btn = self.page.locator(Locators.STRIPE_USD_BTN)
        try:
            # 等待按钮附加到 DOM（Stripe 可能稍晚渲染货币切换区域）
            btn.first.wait_for(state="attached", timeout=8000)
            if btn.count() > 0 and btn.first.is_visible():
                class_attr = btn.first.get_attribute("class") or ""
                if "is-active" not in class_attr:
                    logger.info("切换 Stripe 结算货币为 USD")
                    btn.first.click()
                    self.page.wait_for_timeout(2000)  # 等待价格刷新
                else:
                    logger.info("Stripe 当前已是 USD 货币，无需切换")
            else:
                logger.info("Stripe 页面未发现货币切换按钮，跳过")
        except Exception as e:
            logger.warning(f"切换 USD 货币时发生异常（已忽略）: {e}")

    def apply_promo_code(self, code: str, timeout: int = 30000):
        """
        在 Stripe 结算页输入并应用全额优惠码。
        优惠码全额抵扣时，Stripe 会隐藏支付方式区域，以此判断优惠码生效。

        :param code: 优惠码字符串，如 "freec"
        :param timeout: 超时时间（毫秒）
        """
        logger.info(f"正在应用 Stripe 优惠码: {code}")
        # 第一步：等待优惠码入口按鈕出现，并点击展开输入框
        expect(self.page.locator(Locators.STRIPE_PROMO_CODE_BTN)).to_be_visible(timeout=timeout)
        logger.info("点击优惠码入口按鈕，展开输入框...")
        self.page.locator(Locators.STRIPE_PROMO_CODE_BTN).click()
        # 第二步：逐字输入优惠码（模拟真实用户输入，防触发反机器人检测）
        logger.info(f"逐字输入优惠码: {code}")
        self.page.locator(Locators.STRIPE_PROMO_CODE_INPUT).press_sequentially(code, delay=120)
        # 第三步：点击 Apply 按鈕提交优惠码
        apply_btn = self.page.locator(Locators.STRIPE_PROMO_CODE_APPLY_BTN)
        logger.info("点击 Apply 按鈕提交优惠码...")
        apply_btn.click()

        # 第四步：等待支付方式区域消失 = 优惠码 100% 抗扣生效
        logger.info("等待优惠码生效（支付方式区域应消失）...")
        payment_heading = self.page.locator(Locators.STRIPE_PAYMENT_METHOD_HEADING)
        
        # 增加重试机制：如果支付方式没有在短时间内隐藏，则尝试再次点击 Apply 按钮
        import time
        success = False
        for attempt in range(1, 4):
            try:
                expect(payment_heading).to_be_hidden(timeout=3000)
                success = True
                break
            except AssertionError:
                if attempt < 3:
                    logger.warning(f"优惠码未在第 {attempt} 次点击后生效，尝试重新点击 Apply 按钮...")
                    try:
                        # 直接调用 click，利用 Playwright 自身的自动等待与可点击性检查
                        apply_btn.click(timeout=3000)
                    except Exception as click_err:
                        logger.warning(f"尝试重新点击 Apply 按钮出错: {click_err}")
                else:
                    # 最后一次尝试使用常规超时，若仍未消失则让其正常抛出 AssertionError
                    expect(payment_heading).to_be_hidden(timeout=10000)
                    success = True
        
        if success:
            logger.success(f"优惠码 '{code}' 已生效，支付方式区域已隐藏")

    def fill_email(self, email: str):
        """
        在 Stripe 邮箱输入框中填入邮箱（强制清空后重填）。
        已登录账号结账时 Stripe 可能自动预填，此方法强制覆盖。

        :param email: 邮箱地址
        """
        email_input = self.page.locator(Locators.STRIPE_EMAIL_INPUT)
        if email_input.is_visible():
            logger.info(f"填写 Stripe 结算邮箱: {email}")
            email_input.fill("")
            email_input.fill(email)

    def fill_email_if_empty(self, email: str):
        """
        仅当 Stripe 邮箱框为空时才填入邮箱（已登录用户 Stripe 会自动预填，无需干预）。

        :param email: 邮箱地址
        """
        email_input = self.page.locator(Locators.STRIPE_EMAIL_INPUT)
        if email_input.is_visible() and not email_input.input_value():
            logger.info(f"Stripe 邮箱为空，自动填入: {email}")
            email_input.fill(email)
        else:
            logger.info("Stripe 邮箱已自动填充，跳过手动填写")

    def submit_payment(self):
        """
        点击 Stripe 支付按钮提交订单。
        等待 3 秒让 Stripe 完成最终价格计算后再提交。
        """
        logger.info("等待 Stripe 完成计算后提交支付...")
        time.sleep(3)  # Stripe 需要短暂时间渲染最终状态
        self.page.locator(Locators.STRIPE_PAY_BTN).click()
        logger.info("已点击 Stripe 支付按钮，等待跳转感谢页...")

    def complete_purchase(self, promo_code: str, email: str = None):
        """
        完整执行支付流程（组合方法）：[可选填邮箱] → 应用优惠码 → 提交支付。

        当使用全额优惠码时，Stripe 会隐藏鈣行卡区域，无需填写卡号即可完成支付。

        :param promo_code: Stripe 全额优惠码，如 settings.PROMO_CODE ("freec")
        :param email: 在 Stripe 中填写的邮箱。已登录场景传登录邮箱；未登录场景必传。
        """
        logger.info(f"开始执行 Stripe 支付流程 (email={email or '无需填写'})")
        if email:
            # 已登录场景：Stripe 会自动预填登录账号邮箱，如果已填则覆盖；未登录场景：Stripe 邮箱框为空，必须填入
            self.fill_email(email)
        self.apply_promo_code(promo_code)
        self.submit_payment()

    def assert_stripe_price(self, expected_price: str, select_usd: bool = True):
        """
        断言 Stripe 结算页显示的金额包含预期价格数字。
        取最后一个 CurrencyAmount 元素（通常为页面底部的应付总额）。

        :param expected_price: 预期价格字符串，如 "9.99"
        :param select_usd: 是否先切换到 USD（默认 True）
        """
        if select_usd:
            self.select_currency_usd()

        currency_el = self.page.locator(Locators.STRIPE_CURRENCY_AMOUNT).last
        logger.info(f"验证 Stripe 结算金额: 预期包含 '{expected_price}'")
        expect(currency_el).to_be_visible(timeout=15000)
        expect(currency_el).to_contain_text(expected_price)
        logger.success(f"验证通过: Stripe 金额与预期 '{expected_price}' 相符")

    # ==================== 感谢页断言 ====================

    def assert_thank_you_page(self, timeout: int = 60000):
        """
        断言页面已成功跳转到购买感谢页。
        以 URL 包含 'thanks-for-your-order' 且感谢页容器可见为判断依据。

        :param timeout: 最长等待时间（毫秒），支付完成跳转可能需要较长时间
        """
        logger.info("验证是否成功跳转至购买感谢页...")
        # 等待 URL 变更为感谢页
        expect(self.page).to_have_url(
            re.compile(r".*thanks-for-your-order.*"), timeout=timeout
        )
        # 等待感谢页内容渲染完成
        expect(self.page.locator(Locators.THANK_YOU_PAGE)).to_be_visible(timeout=15000)
        expect(self.page.locator(Locators.THANK_YOU_TITLE)).to_be_visible(timeout=10000)
        logger.success(f"验证通过: 已成功跳转至感谢页 ({self.page.url})")

    def assert_billing_email(self, expected_email: str, timeout: int = 10000):
        """
        断言感谢页显示的账单邮箱与预期一致。

        重要：当已登录账号发起购买时，感谢页始终显示**登录账号**的邮箱，
        而非 Stripe 表单中手动填写的邮箱。这是 Somio 的业务逻辑。

        :param expected_email: 预期的账单邮箱地址
        :param timeout: 超时时间（毫秒）
        """
        logger.info(f"验证感谢页账单邮箱: 预期为 '{expected_email}'")
        email_locator = self.page.locator(Locators.THANK_YOU_EMAIL)
        expect(email_locator).to_be_visible(timeout=timeout)
        expect(email_locator).to_have_text(expected_email, timeout=timeout)
        logger.success(f"验证通过: 账单邮箱正确显示为 '{expected_email}'")

    def assert_password_visible(self, timeout: int = 10000):
        """
        断言感谢页显示了初始密码（适用于未注册邮箱首次购买的场景）。
        Somio 会为新注册用户自动生成一个 'somioai' 开头的初始密码。

        :param timeout: 超时时间（毫秒）
        """
        logger.info("验证感谢页是否显示初始密码（新用户场景）...")
        pwd_box = self.page.locator(Locators.THANK_YOU_PASSWORD_BOX)
        pwd_text = self.page.locator(Locators.THANK_YOU_PASSWORD)
        # 密码框容器应可见
        expect(pwd_box).to_be_visible(timeout=timeout)
        # 密码文本应非空且包含 'somioai' 前缀
        expect(pwd_text).to_be_visible(timeout=timeout)
        expect(pwd_text).to_have_text(
            re.compile(r"somioai\w+"), timeout=timeout
        )
        logger.success("验证通过: 感谢页已显示初始密码（新用户）")

    def assert_password_hidden(self, timeout: int = 10000):
        """
        断言感谢页不显示初始密码（适用于已注册账号购买的场景）。
        已注册用户不需要系统生成密码，密码框应处于隐藏状态。

        :param timeout: 超时时间（毫秒）
        """
        logger.info("验证感谢页是否隐藏初始密码（已注册用户场景）...")
        pwd_box = self.page.locator(Locators.THANK_YOU_PASSWORD_BOX)
        expect(pwd_box).to_be_hidden(timeout=timeout)
        logger.success("验证通过: 密码框已隐藏（已注册用户，无需返回初始密码）")

    def get_initial_password(self) -> str:
        """
        获取感谢页显示的初始密码文本（供调试或后续登录使用）。

        :return: 初始密码字符串，不可见时返回空字符串
        """
        try:
            pwd = self.page.locator(Locators.THANK_YOU_PASSWORD).inner_text(timeout=5000)
            logger.info(f"感谢页初始密码: {pwd}")
            return pwd.strip()
        except Exception:
            return ""
