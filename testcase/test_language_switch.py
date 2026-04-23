import pytest
from pages.language_page import LanguagePage

class TestLanguageSwitch:
    """顶部导航/侧边栏语言切换测试，分离每个语言为一个独立的测试用例"""

    # ==================== 13 个独立的语言切换测试用例 ====================
    # 通过引入 lang_urls fixture 仅仅是为了从中获取命令行配置的 env 环境。

    def test_switch_to_en(self, page, lang_urls):
        LanguagePage(page).switch_and_assert("en", lang_urls["env"])

    def test_switch_to_de(self, page, lang_urls):
        LanguagePage(page).switch_and_assert("de", lang_urls["env"])

    def test_switch_to_it(self, page, lang_urls):
        LanguagePage(page).switch_and_assert("it", lang_urls["env"])

    def test_switch_to_es(self, page, lang_urls):
        LanguagePage(page).switch_and_assert("es", lang_urls["env"])

    def test_switch_to_pt(self, page, lang_urls):
        LanguagePage(page).switch_and_assert("pt", lang_urls["env"])

    def test_switch_to_fr(self, page, lang_urls):
        LanguagePage(page).switch_and_assert("fr", lang_urls["env"])

    def test_switch_to_nl(self, page, lang_urls):
        LanguagePage(page).switch_and_assert("nl", lang_urls["env"])

    def test_switch_to_ko(self, page, lang_urls):
        LanguagePage(page).switch_and_assert("ko", lang_urls["env"])

    def test_switch_to_ja(self, page, lang_urls):
        LanguagePage(page).switch_and_assert("ja", lang_urls["env"])

    def test_switch_to_zh_cn(self, page, lang_urls):
        LanguagePage(page).switch_and_assert("zh-cn", lang_urls["env"])

    def test_switch_to_zh_tw(self, page, lang_urls):
        LanguagePage(page).switch_and_assert("zh-tw", lang_urls["env"])

    def test_switch_to_ro(self, page, lang_urls):
        LanguagePage(page).switch_and_assert("ro", lang_urls["env"])

    def test_switch_to_pl(self, page, lang_urls):
        LanguagePage(page).switch_and_assert("pl", lang_urls["env"])
