import pytest
from playwright.sync_api import expect
from config.locators import Locators
from utils import logger
from pages.vocal_remover_page import VocalRemoverPage


@pytest.mark.usefixtures("processed_vocal_page")
class TestVocalRemoverSuite:
    """人声分离（本地文件上传）与多格式下载测试用例"""

    # ==================== 上传 ====================

    def test_vocal_remover_upload_file(self, processed_vocal_page):
        """测试本地文件上传，断言处理完成后下载按钮出现"""
        logger.info("验证上传并处理成功: 预期出现 一键下载全部 按钮")
        expect(processed_vocal_page.locator(Locators.VOCAL_RESULT_DOWNLOAD_ALL_BTN)).to_be_visible(timeout=5000)
        logger.success("验证通过: 页面成功渲染出一键下载按钮")

    # ==================== 一键下载全部 ====================

    def test_download_all_mp3_44khz(self, vr_page):
        """下载全部 - 设置格式 (MP3 - 44.1kHz)"""
        vr_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_44_1)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_ALL_BTN, expected_suffix=".zip")

    def test_download_all_mp3_48khz(self, vr_page):
        """下载全部 - 设置格式 (MP3 - 48kHz)"""
        vr_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_48)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_ALL_BTN, expected_suffix=".zip")

    def test_download_all_wav_44khz_16bit(self, vr_page):
        """下载全部 - 设置格式 (WAV - 44.1kHz - 16-bit)"""
        vr_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_ALL_BTN, expected_suffix=".zip")

    def test_download_all_wav_44khz_24bit(self, vr_page):
        """下载全部 - 设置格式 (WAV - 44.1kHz - 24-bit)"""
        vr_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_24)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_ALL_BTN, expected_suffix=".zip")

    def test_download_all_wav_48khz_16bit(self, vr_page):
        """下载全部 - 设置格式 (WAV - 48kHz - 16-bit)"""
        vr_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_48, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_ALL_BTN, expected_suffix=".zip")

    def test_download_all_wav_48khz_24bit(self, vr_page):
        """下载全部 - 设置格式 (WAV - 48kHz - 24-bit)"""
        vr_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_48, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_24)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_ALL_BTN, expected_suffix=".zip")

    # ==================== 单独下载人声 (Vocal) ====================

    def test_download_vocal_mp3_44khz(self, vr_page):
        """单独下载人声 - 设置格式 (MP3 - 44.1kHz)"""
        vr_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_44_1)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_VOCAL_BTN, expected_suffix=".mp3")

    def test_download_vocal_mp3_48khz(self, vr_page):
        """单独下载人声 - 设置格式 (MP3 - 48kHz)"""
        vr_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_48)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_VOCAL_BTN, expected_suffix=".mp3")

    def test_download_vocal_wav_44khz_16bit(self, vr_page):
        """单独下载人声 - 设置格式 (WAV - 44.1kHz - 16-bit)"""
        vr_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_VOCAL_BTN, expected_suffix=".wav")

    def test_download_vocal_wav_44khz_24bit(self, vr_page):
        """单独下载人声 - 设置格式 (WAV - 44.1kHz - 24-bit)"""
        vr_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_24)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_VOCAL_BTN, expected_suffix=".wav")

    def test_download_vocal_wav_48khz_16bit(self, vr_page):
        """单独下载人声 - 设置格式 (WAV - 48kHz - 16-bit)"""
        vr_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_48, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_VOCAL_BTN, expected_suffix=".wav")

    def test_download_vocal_wav_48khz_24bit(self, vr_page):
        """单独下载人声 - 设置格式 (WAV - 48kHz - 24-bit)"""
        vr_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_48, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_24)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_VOCAL_BTN, expected_suffix=".wav")

    # ==================== 单独下载伴奏 (Inst) ====================

    def test_download_inst_mp3_44khz(self, vr_page):
        """单独下载伴奏 - 设置格式 (MP3 - 44.1kHz)"""
        vr_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_44_1)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_INSTRUMENTAL_BTN, expected_suffix=".mp3")

    def test_download_inst_mp3_48khz(self, vr_page):
        """单独下载伴奏 - 设置格式 (MP3 - 48kHz)"""
        vr_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_48)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_INSTRUMENTAL_BTN, expected_suffix=".mp3")

    def test_download_inst_wav_44khz_16bit(self, vr_page):
        """单独下载伴奏 - 设置格式 (WAV - 44.1kHz - 16-bit)"""
        vr_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_INSTRUMENTAL_BTN, expected_suffix=".wav")

    def test_download_inst_wav_44khz_24bit(self, vr_page):
        """单独下载伴奏 - 设置格式 (WAV - 44.1kHz - 24-bit)"""
        vr_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_24)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_INSTRUMENTAL_BTN, expected_suffix=".wav")

    def test_download_inst_wav_48khz_16bit(self, vr_page):
        """单独下载伴奏 - 设置格式 (WAV - 48kHz - 16-bit)"""
        vr_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_48, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_INSTRUMENTAL_BTN, expected_suffix=".wav")

    def test_download_inst_wav_48khz_24bit(self, vr_page):
        """单独下载伴奏 - 设置格式 (WAV - 48kHz - 24-bit)"""
        vr_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_48, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_24)
        vr_page.do_download(Locators.VOCAL_RESULT_DOWNLOAD_INSTRUMENTAL_BTN, expected_suffix=".wav")


class TestVocalRemoverLibrary:
    """人声分离（音乐库选择音频）测试用例"""

    def test_vocal_remover_library_file(self, logged_in_page):
        """测试从 My Music 音乐库选择音频文件并分离"""
        logger.info("开始测试从音乐库选择音频进行人声分离...")
        vr_page = VocalRemoverPage(logged_in_page)

        # 切换到人声分离
        vr_page.switch_to_vocal_remover()

        # 从音乐库导入
        vr_page.select_from_library()

        # 分离
        vr_page.click_separate()

        # 验证结果页渲染成功
        logger.info("等待人声分离结果页面加载完成 (最多 360 秒)...")
        expect(logged_in_page.locator(Locators.VOCAL_RESULT_DOWNLOAD_ALL_BTN)).to_be_visible(timeout=360000)
        logger.success("验证通过: 从音乐库选择音频处理成功进入结果页面")

        # 等待音频加载完成
        vr_page.wait_for_audio_loaded()

        expect(logged_in_page.locator(Locators.VOCAL_RESULT_DOWNLOAD_VOCAL_BTN)).to_be_visible(timeout=5000)
        expect(logged_in_page.locator(Locators.VOCAL_RESULT_DOWNLOAD_INSTRUMENTAL_BTN)).to_be_visible(timeout=5000)
