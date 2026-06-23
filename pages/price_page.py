from playwright.sync_api import Page, expect
from config.locators import Locators
from utils import logger
import re

class PricePage:
    """封装价格页面的相关操作"""

    def __init__(self, page: Page):
        self.page = page

    # ==================== 进入价格页 ====================

    def navigate_to_pricing_direct(self):
        """
        直接通过 URL 导航到价格页（适用于未登录场景或任意起始页面）。
        相比通过 Upgrade 按钮点击，此方法更稳定，不依赖 Header 按钮状态。
        """
        base_url = self.page.url.split("/generate")[0].split("/pricing")[0].rstrip("/")
        pricing_url = f"{base_url}/pricing/music-generator/"
        logger.info(f"直接导航至价格页: {pricing_url}")
        self.page.goto(pricing_url, wait_until="domcontentloaded")
        # 等待至少一个购买按钮可见，确认页面加载完成
        self.page.locator(Locators.SUBSCRIBE_BASIC_UPGRADE_BTN).first.wait_for(
            state="visible", timeout=15000
        )
        logger.success("价格页已加载完成")

    def navigate_to_pricing_from_header(self):
        """通过顶部 Header 栏的 'Upgrade' 按钮进入价格页"""
        logger.info("通过顶部 Header 'Upgrade' 按钮进入价格页")
        try:
            with self.page.context.expect_page(timeout=5000) as new_page_info:
                self.page.locator(Locators.UPGRADE_BTN).click()
            new_page = new_page_info.value
            logger.info("检测到打开了新标签页，正在切换到新标签页...")
            self.page = new_page
            self.page.wait_for_load_state("domcontentloaded", timeout=15000)
        except Exception as e:
            logger.info(f"未检测到新标签页，在当前页处理跳转: {e}")
            self.page.wait_for_timeout(1000)


    def navigate_to_pricing_from_limit_dialog(self):
        """通过使用限制弹窗中的 'Upgrade' 按钮进入价格页"""
        logger.info("通过限制弹窗中的 'Upgrade' 按钮进入价格页")
        try:
            with self.page.context.expect_page(timeout=5000) as new_page_info:
                self.page.locator(Locators.LIMIT_UPGRADE_BTN).click(force=True)
            new_page = new_page_info.value
            logger.info("检测到限制弹窗打开了新标签页，正在切换到新标签页...")
            self.page = new_page
            self.page.wait_for_load_state("domcontentloaded", timeout=15000)
        except Exception as e:
            logger.info(f"未检测到新标签页，在当前页处理限制弹窗跳转: {e}")
            self.page.wait_for_timeout(1000)

    # ==================== 切换套餐 Tab ====================

    def switch_to_monthly(self):
        """切换到月套餐分页"""
        logger.info("切换到月套餐分页")
        self.page.locator(Locators.PRICE_PAGE_CYCLE_MONTHLY).click()
        self.page.wait_for_timeout(500)

    def switch_to_yearly(self):
        """切换到年套餐分页"""
        logger.info("切换到年套餐分页")
        self.page.locator(Locators.PRICE_PAGE_CYCLE_YEARLY).click()
        self.page.wait_for_timeout(500)

    def switch_to_onetime(self):
        """切换到一次性套餐分页"""
        logger.info("切换到一次性套餐分页")
        self.page.locator(Locators.PRICE_PAGE_CYCLE_ONETIME).click()
        self.page.wait_for_timeout(500)

    # ==================== 订阅套餐购买 ====================

    def click_subscribe_basic(self):
        """点击订阅-BASIC-升级/购买按钮"""
        logger.info("点击订阅 BASIC 升级/购买按钮")
        self.page.locator(Locators.SUBSCRIBE_BASIC_UPGRADE_BTN).click()

    def click_subscribe_standard(self):
        """点击订阅-STANDARD-升级/购买按钮"""
        logger.info("点击订阅 STANDARD 升级/购买按钮")
        self.page.locator(Locators.SUBSCRIBE_STANDARD_UPGRADE_BTN).click()

    def click_subscribe_pro(self):
        """点击订阅-PRO-升级/购买按钮"""
        logger.info("点击订阅 PRO 升级/购买按钮")
        self.page.locator(Locators.SUBSCRIBE_PRO_UPGRADE_BTN).click()

    # ==================== 一次性套餐购买 ====================

    def click_onetime_lite(self):
        """点击一次性-LITE-购买按钮"""
        logger.info("点击一次性 LITE 购买按钮")
        self.page.locator(Locators.ONE_TIME_LITE_BUY_BTN).click()

    def click_onetime_basic(self):
        """点击一次性-BASIC-购买按钮"""
        logger.info("点击一次性 BASIC 购买按钮")
        self.page.locator(Locators.ONE_TIME_BASIC_BUY_BTN).click()

    def click_onetime_standard(self):
        """点击一次性-STANDARD-购买按钮"""
        logger.info("点击一次性 STANDARD 购买按钮")
        self.page.locator(Locators.ONE_TIME_STANDARD_BUY_BTN).click()

    def click_onetime_pro(self):
        """点击一次性-PRO-购买按钮"""
        logger.info("点击一次性 PRO 购买按钮")
        self.page.locator(Locators.ONE_TIME_PRO_BUY_BTN).click()

    # ==================== 验证 Stripe 跳转 ====================

    def wait_for_stripe_redirect(self, timeout: int = 15000) -> bool:
        """
        等待并验证页面是否跳转到了 Stripe 付款页面
        :param timeout: 超时时间(毫秒)
        :return: 是否跳转成功
        """
        logger.info("等待跳转到 Stripe 付款页面...")
        try:
            # 等待当前 URL 变更为包含 stripe.com 的地址
            self.page.wait_for_url(re.compile(r".*stripe\.com.*"), timeout=timeout)
            logger.success(f"成功跳转到 Stripe 支付页: {self.page.url}")
            return True
        except Exception as e:
            logger.error(f"未能成功跳转到 Stripe 支付页: {e}")
            return False

    # ==================== 组合快捷操作 ====================

    def go_to_onetime_pro_stripe(self):
        """
        一次性 Pro 套餐购买快捷入口（组合方法）。

        内部执行：导航价格页 → 切换一次性 Tab → 点击 Pro 购买 → 等待 Stripe 加载。
        返回已就绪的 StripePage 对象，供后续填邮箱、输优惠码、提交支付等操作使用。

        适用于所有需要完整购买一次性 Pro 套餐的测试场景（已登录 / 未登录均可）。
        """
        import time
        from pages.stripe_page import StripePage

        self.navigate_to_pricing_direct()
        self.switch_to_onetime()
        self.click_onetime_pro()
        time.sleep(2)  # 等待页面发起 Stripe 跳转请求
        stripe_page = StripePage(self.page)
        stripe_page.wait_for_stripe_load()
        return stripe_page
