import os
import time
from config.locators import Locators
from pages.vocal_remover_page import VocalRemoverPage
from playwright.sync_api import Page
from utils import logger


class StemSplitterPage(VocalRemoverPage):
    """
    Stem Splitter 页面 Page Object，继承自 VocalRemoverPage。
    重写格式入口与 WAV 保存按钮以契合音轨分离页面定位器。
    """

    def __init__(self, page: Page, instrument: str = None):
        super().__init__(page)
        self.instrument = instrument  # 当前单乐器模式名称，如 "drums"/"bass"/"piano"/"guitar"

        # 重写格式入口与保存按钮定位
        self.format_btn = Locators.STEM_FORMAT
        self.wav_save_btn = Locators.STEM_FORMAT_WAV_SAVE_BTN

        # 全乐器模式下的分轨下载按钮映射
        self.vocal_download_btn = Locators.STEM_ALL_VOCAL_DOWNLOAD_BTN
        self.drums_download_btn = Locators.STEM_ALL_DRUM_DOWNLOAD_BTN
        self.bass_download_btn = Locators.STEM_ALL_BASS_DOWNLOAD_BTN
        self.piano_download_btn = Locators.STEM_ALL_PIANO_DOWNLOAD_BTN
        self.guitar_download_btn = Locators.STEM_ALL_GUITAR_DOWNLOAD_BTN
        self.other_download_btn = Locators.STEM_ALL_OTHER_DOWNLOAD_BTN

        # 单乐器模式下的定位器配置映射
        self.INSTRUMENT_MODES = {
            "drums": {
                "mode_btn": Locators.STEM_TAB_DRUMS,
                "all_btn": Locators.DRUMS_DOWNLOAD_ALL,
                "solo_btn": Locators.DRUMS_DOWNLOAD_DRUMS,
                "no_inst_btn": Locators.DRUMS_DOWNLOAD_DRUMS_NO,
            },
            "bass": {
                "mode_btn": Locators.STEM_TAB_BASS,
                "all_btn": Locators.BASS_DOWNLOAD_ALL,
                "solo_btn": Locators.BASS_DOWNLOAD_BASS,
                "no_inst_btn": Locators.BASS_DOWNLOAD_BASS_NO,
            },
            "piano": {
                "mode_btn": Locators.STEM_TAB_PIANO,
                "all_btn": Locators.PIANO_DOWNLOAD_ALL,
                "solo_btn": Locators.PIANO_DOWNLOAD_PIANO,
                "no_inst_btn": Locators.PIANO_DOWNLOAD_PIANO_NO,
            },
            "guitar": {
                "mode_btn": Locators.STEM_TAB_GUITAR,
                "all_btn": Locators.GUITAR_DOWNLOAD_ALL,
                "solo_btn": Locators.GUITAR_DOWNLOAD_GUITAR,
                "no_inst_btn": Locators.GUITAR_DOWNLOAD_GUITAR_NO,
            },
        }

    def switch_to_stem_splitter(self):
        """通过侧边栏导航切换至音轨分离页面并等待加载完成"""
        logger.info("点击左侧导航栏的 Stem Splitter 按钮...")
        self.page.locator(Locators.NAV_STEM).click()
        logger.info("等待音轨分离页面加载完成...")
        self.page.locator(Locators.COMMON_UPLOAD_FILE_BTN).wait_for(state="visible", timeout=30000)
        logger.info("成功切换至 Stem Splitter 页面")

    def select_mode(self, mode_locator: str):
        """切换分轨分离模式 (All / Drums / Bass / Piano / Guitar)"""
        logger.info(f"点击切换分轨模式: {mode_locator}")
        self.page.locator(mode_locator).click(force=True)
        self.page.wait_for_timeout(1000)

    def download_all_stems(self, expected_suffix: str = None):
        """
        全乐器模式：一键打包下载所有分轨文件。
        1. 点击下载全部按钮打开弹窗。
        2. 确认在 ALL 选项卡。
        3. 点击 STEMS 下载。
        """
        logger.info("点击一键下载全部按钮...")
        self.page.locator(Locators.STEM_MIX_DOWNLOAD_BTN).click(force=True)
        self.page.wait_for_selector(Locators.STEM_MIX_DOWNLOAD_WINDOW, state="visible", timeout=10000)

        # 确保切换到 ALL 选项卡
        all_tab = self.page.locator(Locators.STEM_MIX_DOWNLOAD_TAP_ALL)
        if all_tab.is_visible():
            all_tab.click()
            self.page.wait_for_timeout(500)

        logger.info("点击 Stems 触发所有分轨下载...")
        self.do_download(Locators.STEM_MIX_DOWNLOAD_STEMS, expected_suffix=expected_suffix)

    def download_mix(self, expected_suffix: str = None):
        """
        全乐器模式：下载混音文件。
        1. 点击下载全部按钮打开弹窗。
        2. 切换到 MIX 选项卡。
        3. 点击 MIX 下载。
        """
        logger.info("点击一键下载全部按钮...")
        self.page.locator(Locators.STEM_MIX_DOWNLOAD_BTN).click(force=True)
        self.page.wait_for_selector(Locators.STEM_MIX_DOWNLOAD_WINDOW, state="visible", timeout=10000)

        # 切换到 MIX 选项卡
        mix_tab = self.page.locator(Locators.STEM_MIX_DOWNLOAD_TAP_MIX)
        if mix_tab.is_visible():
            mix_tab.click()
            self.page.wait_for_timeout(500)

        logger.info("点击 Mix 触发混音下载...")
        self.do_download(Locators.STEM_MIX_DOWNLOAD_MIX, expected_suffix=expected_suffix)

    def download_single_mode_all(self, download_btn_locator: str, expected_suffix: str = None):
        """
        单乐器模式下的打包下载。
        """
        logger.info("触发单乐器模式打包下载...")
        self.do_download(download_btn_locator, expected_suffix=expected_suffix)

