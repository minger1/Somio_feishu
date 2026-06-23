import pytest
from pages.reference_page import ReferencePage
from utils import logger, get_song
from data.test_data import TEST_REFERENCE_PROMPT, YTB_URL

class TestReferenceCreateSong:
    """Reference 模式生成音乐的功能测试集"""

    def test_reference_mode_generation_direct(self, logged_in_page):
        """
        [用例描述]：测试 Reference 模式下，输入 URL 链接和提示词后，
        在 AI 分析弹窗中点击 'Create Now' 直接生成音乐的全量流程。
        """
        logger.info("开始测试 Reference 模式直接生成用例")
        rp = ReferencePage(logged_in_page)
        song_title = get_song(prefix="REF", model="DIRECT")

        success = rp.run_generation_flow(
            link=YTB_URL,
            text=TEST_REFERENCE_PROMPT,
            song_title=song_title,
            action="direct",
            timeout=360000
        )
        assert success, f"Reference 直接生成歌曲 '{song_title}' 超时或失败"
        logger.success("Reference 模式直接生成用例测试完毕")

    def test_reference_mode_generation_view_lyrics(self, logged_in_page):
        """
        [用例描述]：测试 Reference 模式下，下钻到 'View Lyrics' 歌词二创面板，
        修改歌名并投递生成的全量流程。
        """
        logger.info("开始测试 Reference 模式 View Lyrics 二创生成用例")
        rp = ReferencePage(logged_in_page)
        song_title = get_song(prefix="REF-LYRIC", model="")

        success = rp.run_generation_flow(
            link=YTB_URL,
            text=TEST_REFERENCE_PROMPT,
            song_title=song_title,
            action="view_lyrics",
            timeout=600000
        )
        assert success, f"Reference View Lyrics 歌曲 '{song_title}' 超时或失败"
        logger.success("Reference 模式 View Lyrics 二创生成用例测试完毕")
