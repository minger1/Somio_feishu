from playwright.sync_api import expect
from config.locators import Locators
from pages.stem_splitter_page import StemSplitterPage
from utils import logger


class TestStemSplitterSuite:
    """
    测试 Stem Splitter (音轨分离) 页面的完整流程：
    - 上传文件并确认处理完成
    - 一键下载全部 (Stems 打包 / Mix 混音) - MP3 / WAV
    - 各声道单独下载 (drums / bass / piano / guitar / vocal / other) - MP3 / WAV
    """

    # ==================== 上传 ====================

    def test_stem_splitter_upload_file(self, processed_stem_page):
        """测试文件上传：断言处理完成后下载全部按钮出现"""
        logger.info("正在验证 Stem Splitter (AI 轨道分离) 文件处理完成: 预期出现下载按钮")
        expect(processed_stem_page.locator(Locators.STEM_MIX_DOWNLOAD_BTN)).to_be_visible(timeout=360000)
        logger.success("验证通过: 文件处理成功，下载全部按钮已显示")

    # ==================== 一键下载全部 (Download ALL) ====================

    def test_download_all_tab_mp3(self, stem_page):
        """测试一键下载全部 - ALL 分页 (MP3 44.1kHz)"""
        # 1. 设置格式为 MP3 44.1kHz
        stem_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_44_1)
        
        # 2. 唤起 MIX 弹窗并打包下载所有 Stems
        stem_page.download_all_stems(expected_suffix=".zip")

    def test_download_mix_tab_wav(self, stem_page):
        """测试一键下载全部 - MIX 分页 (WAV 44.1kHz - 16-bit)"""
        # 1. 设置格式为 WAV 44.1kHz 16-bit
        stem_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        
        # 2. 唤起 MIX 弹窗并下载 Mix 混音文件
        stem_page.download_mix(expected_suffix=".wav")

