from playwright.sync_api import expect
from config.locators import Locators
from utils import logger
import time

class EffectPage:
    """封装 Sound Effect Generator (音效生成) 模式相关的页面操作"""

    def __init__(self, page):
        self.page = page

    def switch_to_effect_tab(self):
        """点击侧边栏 Sound Effect Generator 导航，切换到音效生成分页"""
        self.page.locator(Locators.NAV_EFFECT).click()
        # 动态等待：一旦音效提示词输入框可见，说明切换渲染完全稳定
        self.page.locator(Locators.EFFECT_PROMPT_TEXTAREA).wait_for(state="visible", timeout=10000)
        logger.info("切换到 Sound Effect Generator 音效生成分页")

    def select_model(self, model: str):
        """
        选择模型版本，可选值: 'V5.5', 'V5'
        """
        logger.info(f"选择模型版本: {model}")
        dropdown = self.page.locator(Locators.EFFECT_MODEL_DROPDOWN)
        dropdown.click()
        self.page.wait_for_timeout(500)
        
        if model.lower() == "v5.5":
            self.page.locator(Locators.EFFECT_MODEL_OPTION_V5_5).click()
        elif model.lower() == "v5":
            self.page.locator(Locators.EFFECT_MODEL_OPTION_V5).click()
        else:
            raise ValueError(f"不符合预期的模型类型: {model}")
        
        self.page.wait_for_timeout(500)
        logger.success(f"成功选择模型: {model}")

    def input_prompt(self, text: str, timeout: int = 10000):
        """输入音效提示词"""
        textarea = self.page.locator(Locators.EFFECT_PROMPT_TEXTAREA)
        textarea.fill(text)
        expect(textarea).to_have_value(text, timeout=timeout)
        logger.success(f"输入音效描述成功: {text[:30]}...")

    def click_clear_prompt(self):
        """清空提示词输入框"""
        self.page.locator(Locators.EFFECT_CLEAR_BTN).click()
        logger.info("清空音效描述输入框")

    def expand_advanced_options(self):
        """展开高级选项（若已展开则不重复点击）"""
        toggle = self.page.locator(Locators.EFFECT_ADVANCED_TOGGLE)
        # 判断 Song Name 输入框是否可见来推断其折叠状态
        song_name_visible = self.page.locator(Locators.EFFECT_SONG_NAME_INPUT).is_visible()
        if not song_name_visible:
            logger.info("展开高级选项 (Advanced Options)")
            toggle.click()
            self.page.wait_for_timeout(500)
        else:
            logger.debug("高级选项已是展开状态")

    def set_song_name(self, name: str):
        """设置音效/歌曲名称"""
        self.expand_advanced_options()
        self.page.locator(Locators.EFFECT_SONG_NAME_INPUT).fill(name)
        logger.info(f"设置音效名称: {name}")

    def toggle_seamless_loop(self, enable: bool = True):
        """切换无缝循环开关"""
        self.expand_advanced_options()
        switch = self.page.locator(Locators.EFFECT_LOOP_SWITCH)
        switch.click()
        logger.info(f"切换无缝循环状态为: {enable}")
        self.page.wait_for_timeout(300)

    def set_tempo(self, tempo: str):
        """设置速度 (BPM)"""
        self.expand_advanced_options()
        self.page.locator(Locators.EFFECT_TEMPO_INPUT).fill(tempo)
        logger.info(f"设置音效速度 (BPM) 为: {tempo}")

    def select_key(self, key_name: str):
        """
        选择调性 (Key)，例如 'Any', 'Cm', 'C#m', 'Dm' 等
        """
        self.expand_advanced_options()
        logger.info(f"选择音效调性 (Key): {key_name}")
        dropdown = self.page.locator(Locators.EFFECT_KEY_DROPDOWN)
        dropdown.click()
        self.page.wait_for_timeout(500)
        
        # 'Any' 在多语言下可能被翻译，通过 index=0 (第一个选项) 定位最安全
        if key_name.lower() == 'any':
            self.page.locator(Locators.EFFECT_KEY_OPTION).first.click()
        else:
            # 音乐调性（如 Cm, C#m）在任何语言下都保持一致，直接匹配文本
            option_locator = self.page.locator(Locators.EFFECT_KEY_OPTION).filter(has_text=key_name)
            if option_locator.count() > 0:
                option_locator.first.click()
            else:
                self.page.locator(f"//li[contains(text(), '{key_name}')]").first.click()
            
        self.page.wait_for_timeout(500)
        logger.success(f"成功选择调性: {key_name}")

    def click_create(self):
        """点击立即创作按钮"""
        self.page.locator(Locators.EFFECT_CREATE_BTN).click()
        logger.info("点击音效立即创作按钮")



    def wait_for_generation_success(self, title: str = None, timeout: int = 600000):
        """在当前音效生成页面等待生成成功，无需切换至 Library"""
        from pages.library_page import LibraryPage
        lib_page = LibraryPage(self.page)
        
        # 直接在当前页的右侧列表等待生成成功
        return lib_page.wait_for_generation_success(title=title, timeout=timeout)
