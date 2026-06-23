from playwright.sync_api import expect
from config.locators import Locators
from utils import logger


# ==============================================================================
# 单乐器分轨模式测试 (Drums / Bass / Piano / Guitar)
# ==============================================================================


# =============================================
# Drums 鼓
# =============================================

class TestStemDrumsMode:

    def test_drums_upload(self, stem_drums_page):
        """处理完成后，鼓轨和去鼓伴奏两个下载按钮均可见"""
        logger.info("验证上传并处理成功: 预期出现 Drums Solo 和 No Drums 下载按钮")
        drums_solo = stem_drums_page.INSTRUMENT_MODES["drums"]["solo_btn"]
        drums_no   = stem_drums_page.INSTRUMENT_MODES["drums"]["no_inst_btn"]
        expect(stem_drums_page.page.locator(drums_solo)).to_be_visible(timeout=360000)
        expect(stem_drums_page.page.locator(drums_no)).to_be_visible(timeout=360000)
        logger.success("验证通过: 相关下载按钮已显示")

    def test_drums_download_all_mp3(self, stem_drums_page):
        """一键下载全部 — MP3 (44.1kHz)"""
        stem_drums_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_44_1)
        all_btn = stem_drums_page.INSTRUMENT_MODES["drums"]["all_btn"]
        stem_drums_page.download_single_mode_all(all_btn, expected_suffix=".zip")

    def test_drums_download_all_wav(self, stem_drums_page):
        """一键下载全部 — WAV (44.1kHz - 16-bit)"""
        stem_drums_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        all_btn = stem_drums_page.INSTRUMENT_MODES["drums"]["all_btn"]
        stem_drums_page.download_single_mode_all(all_btn, expected_suffix=".zip")

    def test_drums_download_drums_mp3(self, stem_drums_page):
        """单独下载鼓轨 — MP3 (44.1kHz)"""
        stem_drums_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_44_1)
        solo_btn = stem_drums_page.INSTRUMENT_MODES["drums"]["solo_btn"]
        stem_drums_page.do_download(solo_btn, expected_suffix=".mp3")

    def test_drums_download_drums_wav(self, stem_drums_page):
        """单独下载鼓轨 — WAV (44.1kHz - 16-bit)"""
        stem_drums_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        solo_btn = stem_drums_page.INSTRUMENT_MODES["drums"]["solo_btn"]
        stem_drums_page.do_download(solo_btn, expected_suffix=".wav")

    def test_drums_download_no_drums_mp3(self, stem_drums_page):
        """单独下载去鼓伴奏 — MP3 (44.1kHz)"""
        stem_drums_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_44_1)
        no_inst_btn = stem_drums_page.INSTRUMENT_MODES["drums"]["no_inst_btn"]
        stem_drums_page.do_download(no_inst_btn, expected_suffix=".mp3")

    def test_drums_download_no_drums_wav(self, stem_drums_page):
        """单独下载去鼓伴奏 — WAV (44.1kHz - 16-bit)"""
        stem_drums_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        no_inst_btn = stem_drums_page.INSTRUMENT_MODES["drums"]["no_inst_btn"]
        stem_drums_page.do_download(no_inst_btn, expected_suffix=".wav")


# =============================================
# Bass 贝司
# =============================================

class TestStemBassMode:

    def test_bass_upload(self, stem_bass_page):
        """处理完成后，贝司轨和去贝司伴奏两个下载按钮均可见"""
        logger.info("验证上传并处理成功: 预期出现 Bass Solo 和 No Bass 下载按钮")
        bass_solo = stem_bass_page.INSTRUMENT_MODES["bass"]["solo_btn"]
        bass_no   = stem_bass_page.INSTRUMENT_MODES["bass"]["no_inst_btn"]
        expect(stem_bass_page.page.locator(bass_solo)).to_be_visible(timeout=360000)
        expect(stem_bass_page.page.locator(bass_no)).to_be_visible(timeout=360000)
        logger.success("验证通过: 相关下载按钮已显示")

    def test_bass_download_all_mp3(self, stem_bass_page):
        """一键下载全部 — MP3 (44.1kHz)"""
        stem_bass_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_44_1)
        all_btn = stem_bass_page.INSTRUMENT_MODES["bass"]["all_btn"]
        stem_bass_page.download_single_mode_all(all_btn, expected_suffix=".zip")

    def test_bass_download_all_wav(self, stem_bass_page):
        """一键下载全部 — WAV (44.1kHz - 16-bit)"""
        stem_bass_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        all_btn = stem_bass_page.INSTRUMENT_MODES["bass"]["all_btn"]
        stem_bass_page.download_single_mode_all(all_btn, expected_suffix=".zip")

    def test_bass_download_bass_mp3(self, stem_bass_page):
        """单独下载贝司轨 — MP3 (44.1kHz)"""
        stem_bass_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_44_1)
        solo_btn = stem_bass_page.INSTRUMENT_MODES["bass"]["solo_btn"]
        stem_bass_page.do_download(solo_btn, expected_suffix=".mp3")

    def test_bass_download_bass_wav(self, stem_bass_page):
        """单独下载贝司轨 — WAV (44.1kHz - 16-bit)"""
        stem_bass_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        solo_btn = stem_bass_page.INSTRUMENT_MODES["bass"]["solo_btn"]
        stem_bass_page.do_download(solo_btn, expected_suffix=".wav")

    def test_bass_download_no_bass_mp3(self, stem_bass_page):
        """单独下载去贝司伴奏 — MP3 (44.1kHz)"""
        stem_bass_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_44_1)
        no_inst_btn = stem_bass_page.INSTRUMENT_MODES["bass"]["no_inst_btn"]
        stem_bass_page.do_download(no_inst_btn, expected_suffix=".mp3")

    def test_bass_download_no_bass_wav(self, stem_bass_page):
        """单独下载去贝司伴奏 — WAV (44.1kHz - 16-bit)"""
        stem_bass_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        no_inst_btn = stem_bass_page.INSTRUMENT_MODES["bass"]["no_inst_btn"]
        stem_bass_page.do_download(no_inst_btn, expected_suffix=".wav")


# =============================================
# Piano 钢琴
# =============================================

class TestStemPianoMode:

    def test_piano_upload(self, stem_piano_page):
        """处理完成后，钢琴轨和去钢琴伴奏两个下载按钮均可见"""
        logger.info("验证上传并处理成功: 预期出现 Piano Solo 和 No Piano 下载按钮")
        piano_solo = stem_piano_page.INSTRUMENT_MODES["piano"]["solo_btn"]
        piano_no   = stem_piano_page.INSTRUMENT_MODES["piano"]["no_inst_btn"]
        expect(stem_piano_page.page.locator(piano_solo)).to_be_visible(timeout=360000)
        expect(stem_piano_page.page.locator(piano_no)).to_be_visible(timeout=360000)
        logger.success("验证通过: 相关下载按钮已显示")

    def test_piano_download_all_mp3(self, stem_piano_page):
        """一键下载全部 — MP3 (44.1kHz)"""
        stem_piano_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_44_1)
        all_btn = stem_piano_page.INSTRUMENT_MODES["piano"]["all_btn"]
        stem_piano_page.download_single_mode_all(all_btn, expected_suffix=".zip")

    def test_piano_download_all_wav(self, stem_piano_page):
        """一键下载全部 — WAV (44.1kHz - 16-bit)"""
        stem_piano_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        all_btn = stem_piano_page.INSTRUMENT_MODES["piano"]["all_btn"]
        stem_piano_page.download_single_mode_all(all_btn, expected_suffix=".zip")

    def test_piano_download_piano_mp3(self, stem_piano_page):
        """单独下载钢琴轨 — MP3 (44.1kHz)"""
        stem_piano_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_44_1)
        solo_btn = stem_piano_page.INSTRUMENT_MODES["piano"]["solo_btn"]
        stem_piano_page.do_download(solo_btn, expected_suffix=".mp3")

    def test_piano_download_piano_wav(self, stem_piano_page):
        """单独下载钢琴轨 — WAV (44.1kHz - 16-bit)"""
        stem_piano_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        solo_btn = stem_piano_page.INSTRUMENT_MODES["piano"]["solo_btn"]
        stem_piano_page.do_download(solo_btn, expected_suffix=".wav")

    def test_piano_download_no_piano_mp3(self, stem_piano_page):
        """单独下载去钢琴伴奏 — MP3 (44.1kHz)"""
        stem_piano_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_44_1)
        no_inst_btn = stem_piano_page.INSTRUMENT_MODES["piano"]["no_inst_btn"]
        stem_piano_page.do_download(no_inst_btn, expected_suffix=".mp3")

    def test_piano_download_no_piano_wav(self, stem_piano_page):
        """单独下载去钢琴伴奏 — WAV (44.1kHz - 16-bit)"""
        stem_piano_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        no_inst_btn = stem_piano_page.INSTRUMENT_MODES["piano"]["no_inst_btn"]
        stem_piano_page.do_download(no_inst_btn, expected_suffix=".wav")


# =============================================
# Guitar 吉他
# =============================================

class TestStemGuitarMode:

    def test_guitar_upload(self, stem_guitar_page):
        """处理完成后，吉他轨和去吉他伴奏两个下载按钮均可见"""
        logger.info("验证上传并处理成功: 预期出现 Guitar Solo 和 No Guitar 下载按钮")
        guitar_solo = stem_guitar_page.INSTRUMENT_MODES["guitar"]["solo_btn"]
        guitar_no   = stem_guitar_page.INSTRUMENT_MODES["guitar"]["no_inst_btn"]
        expect(stem_guitar_page.page.locator(guitar_solo)).to_be_visible(timeout=360000)
        expect(stem_guitar_page.page.locator(guitar_no)).to_be_visible(timeout=360000)
        logger.success("验证通过: 相关下载按钮已显示")

    def test_guitar_download_all_mp3(self, stem_guitar_page):
        """一键下载全部 — MP3 (44.1kHz)"""
        stem_guitar_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_44_1)
        all_btn = stem_guitar_page.INSTRUMENT_MODES["guitar"]["all_btn"]
        stem_guitar_page.download_single_mode_all(all_btn, expected_suffix=".zip")

    def test_guitar_download_all_wav(self, stem_guitar_page):
        """一键下载全部 — WAV (44.1kHz - 16-bit)"""
        stem_guitar_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        all_btn = stem_guitar_page.INSTRUMENT_MODES["guitar"]["all_btn"]
        stem_guitar_page.download_single_mode_all(all_btn, expected_suffix=".zip")

    def test_guitar_download_guitar_mp3(self, stem_guitar_page):
        """单独下载吉他轨 — MP3 (44.1kHz)"""
        stem_guitar_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_44_1)
        solo_btn = stem_guitar_page.INSTRUMENT_MODES["guitar"]["solo_btn"]
        stem_guitar_page.do_download(solo_btn, expected_suffix=".mp3")

    def test_guitar_download_guitar_wav(self, stem_guitar_page):
        """单独下载吉他轨 — WAV (44.1kHz - 16-bit)"""
        stem_guitar_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        solo_btn = stem_guitar_page.INSTRUMENT_MODES["guitar"]["solo_btn"]
        stem_guitar_page.do_download(solo_btn, expected_suffix=".wav")

    def test_guitar_download_no_guitar_mp3(self, stem_guitar_page):
        """单独下载去吉他伴奏 — MP3 (44.1kHz)"""
        stem_guitar_page.select_mp3_format(Locators.COMMON_FORMAT_MP3_SAMPLE_RATE_44_1)
        no_inst_btn = stem_guitar_page.INSTRUMENT_MODES["guitar"]["no_inst_btn"]
        stem_guitar_page.do_download(no_inst_btn, expected_suffix=".mp3")

    def test_guitar_download_no_guitar_wav(self, stem_guitar_page):
        """单独下载去吉他伴奏 — WAV (44.1kHz - 16-bit)"""
        stem_guitar_page.select_wav_format(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE_44_1, Locators.COMMON_FORMAT_WAV_BIT_DEPTH_16)
        no_inst_btn = stem_guitar_page.INSTRUMENT_MODES["guitar"]["no_inst_btn"]
        stem_guitar_page.do_download(no_inst_btn, expected_suffix=".wav")
