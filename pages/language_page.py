from playwright.sync_api import expect
from config.locators import Locators
from utils import logger

class LanguagePage:
    """封装语言切换相关的操作"""

    def __init__(self, page):
        self.page = page

    def switch_language(self, language_key: str):
        """
        打开语言菜单并切换到指定语言。
        
        :param language_key: 语言代码缩写，如 'en', 'de', 'zh-cn'，对应 config.py 中的 languages
        """
        # 语言代码到 Locator 的映射
        language_map = {
            "en": Locators.LANGUAGE_ENGLISH,
            "de": Locators.LANGUAGE_DEUTSCH,
            "it": Locators.LANGUAGE_ITALIANO,
            "es": Locators.LANGUAGE_ESPANOL,
            "pt": Locators.LANGUAGE_PORTUGUES,
            "fr": Locators.LANGUAGE_FRANCAIS,
            "nl": Locators.LANGUAGE_NEDERLANDS,
            "ko": Locators.LANGUAGE_KOREAN,
            "ja": Locators.LANGUAGE_JAPANESE,
            "zh-cn": Locators.LANGUAGE_CHINESE_SIMPLIFIED,
            "zh-tw": Locators.LANGUAGE_CHINESE_TRADITIONAL,
            "ro": Locators.LANGUAGE_ROMANA,
            "pl": Locators.LANGUAGE_POLSKI,
        }

        if language_key not in language_map:
            raise ValueError(f"不支持的测试语言键: {language_key}")

        locator = language_map[language_key]

        # 1. 点击设置齿轮按钮，展开下拉菜单
        self.page.locator(Locators.SETTING_BTN).click()
        logger.info("已点击设置齿轮按钮，等待下拉菜单展开")
        
        # 确保下拉菜单弹出并稳定
        self.page.wait_for_timeout(500)
        
        # 2. 点击 Language 子菜单入口（鼠标悬停展开语言子菜单）
        self.page.locator(Locators.SETTING_LANGUAGE).hover()
        logger.info("已悬停在 Language 选项，等待语言子菜单展开")
        self.page.wait_for_timeout(400)
        
        # 3. 点击目标语言选项
        self.page.locator(locator).click()
        logger.info(f"点击了语言切换选项: {language_key}")

        # 4. 等待页面加载（重定向/刷新）
        self.page.wait_for_load_state("networkidle", timeout=30000)
        logger.success(f"已请求切换到语言: {language_key}")

    def switch_and_assert(self, target_lang: str, env: str = "somio"):
        """
        全流程封装：
        1. 在当前页面（page fixture 已导航完成）触发语言切换
        2. 断言最终 URL 符合预期
        """
        from config.settings import get_language_urls, ENVIRONMENTS
        
        language_urls = get_language_urls(ENVIRONMENTS[env], env)
        expected_url = language_urls[target_lang]["generate_url"]

        # 切换语言（page fixture 已导航到 generate 页，直接进行语言切换）
        logger.info(f"开始切换语言 {target_lang}，当前 URL: {self.page.url}")
        self.switch_language(target_lang)

        # 断言页面跳转到正确 URL 前缀
        expect(self.page).to_have_url(expected_url, timeout=30000)

        # 额外正则二次断言
        if target_lang != "en":
            assert f"/{target_lang}/" in self.page.url or self.page.url.startswith(f"{expected_url}"), \
                f"URL 没有包含正确的语言代码: {self.page.url}"
        
        logger.success(f"语言 {target_lang} 切换断言通过 ✓")

