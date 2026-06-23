from pages.lyrics_page import LyricsPage
from config.locators import Locators
from utils import get_song, logger
from data.test_data import NON_STANDARD_LYRICS, STANDARD_LYRICS


class TestLyricsCreateSong:
    """歌词模式(Lyrics Tab)下生成音乐的全量生命周期与弹窗流测试集"""

    # ==================================================================
    # 非标准歌词 → AI 分析弹窗流程
    # ==================================================================

    # --- Lyric Formatting 分页（默认）---

    # def test_lyrics_non_standard_formatting_original(self, logged_in_page):
    #     """
    #     [用例描述]: 非标准歌词触发 AI 分析弹窗(Lyrics Insight)，
    #     在 Lyric Formatting 选项卡下，使用 Original Version 生成音频。
    #     """
    #     logger.info("开始测试：非标准歌词 → [Formatting 面板] → [Original Version]")
    #     lp = LyricsPage(logged_in_page)
    #     song_title = get_song(prefix="LYRICS", model="FORMATTING-ORIGINAL")

    #     lp.run_non_standard_flow(
    #         lyrics=NON_STANDARD_LYRICS,
    #         song_title=song_title,
    #         tab_index=0,
    #         action="original",
    #     )

    #     success = lp.wait_for_generation_success(title=song_title)
    #     assert success, f"Formatting 面板 Original Version 生成歌曲 '{song_title}' 超时或失败"
    #     logger.success("Formatting + Original Version 流程测试通过")

    def test_lyrics_non_standard_formatting_create_now(self, logged_in_page):
        """
        [用例描述]: 非标准歌词触发 AI 分析弹窗(Lyrics Insight)，
        在 Lyric Formatting 面板中点选 Create Now (AI增强) 生成。
        """
        logger.info("开始测试：非标准歌词 → [Formatting 面板] → [Create Now(AI)]")
        lp = LyricsPage(logged_in_page)
        song_title = get_song(prefix="LYRICS", model="FORMATTING-AI")

        lp.run_non_standard_flow(
            lyrics=NON_STANDARD_LYRICS,
            song_title=song_title,
            tab_index=0,
            action="ai",
        )

        success = lp.wait_for_generation_success(title=song_title)
        assert success, f"Formatting 面板 Create Now 生成歌曲 '{song_title}' 超时或失败"
        logger.success("Formatting + Create Now 流程测试通过")

    # --- Lyric Refinement 分页（切换后）---

    # def test_lyrics_non_standard_refinement_create_now(self, logged_in_page):
    #     """
    #     [用例描述]: 非标准歌词触发弹窗后，切换到 Lyric Refinement 选项卡，
    #     点击 Create Now (AI增强) 生成。
    #     """
    #     logger.info("开始测试：非标准歌词 → [Refinement 面板] → [Create Now(AI)]")
    #     lp = LyricsPage(logged_in_page)
    #     song_title = get_song(prefix="LYRICS", model="REFINEMENT-AI")

    #     lp.run_non_standard_flow(
    #         lyrics=NON_STANDARD_LYRICS,
    #         song_title=song_title,
    #         tab_index=1,
    #         action="ai",
    #     )

    #     success = lp.wait_for_generation_success(title=song_title)
    #     assert success, f"Refinement + Create Now 生成 '{song_title}' 失败！"
    #     logger.success("Refinement + Create Now 流程测试通过")

    # ==================================================================
    # 标准歌词 → 直接生成（不触发 AI 分析弹窗）
    # ==================================================================

    # def test_lyrics_standard_direct_creation(self, logged_in_page):
    #     """
    #     [用例描述]: 填入格式规范的标准歌词，系统判断无需 AI 分析，
    #     直接跳过 AI 分析弹窗完成生成。
    #     """
    #     logger.info("开始测试：标准规范歌词 → 直接生成（跳过 AI 分析）")
    #     lp = LyricsPage(logged_in_page)
    #     song_title = get_song(prefix="LYRICS", model="STANDARD-DIRECT")

    #     success = lp.run_standard_direct_flow(
    #         lyrics=STANDARD_LYRICS,
    #         song_title=song_title,
    #         timeout=360000
    #     )
    #     assert success, f"标准歌词直接生成 '{song_title}' 失败或超时"
    #     logger.success("标准歌词免检直通生成链路测试完毕")

    # ==================================================================
    # 所有模型切换测试（标准歌词直接生成）
    # ==================================================================

    # --- Somio.ai 模型 ---

    def test_lyrics_mode_v5_5(self, logged_in_page):
        """Somio V5.5 模型 - 歌词模式生成"""
        lp = LyricsPage(logged_in_page)
        success, song_title = lp.run_model_generation_flow(
            "V5.5", Locators.MODEL_VERSION_V5_5,
            provider_locator=Locators.MODEL_PROVIDER_SOMIO
        )
        assert success, f"歌词模式 Somio V5.5 模型生成 '{song_title}' 超时或失败"
        logger.success("歌词模式 Somio V5.5 模型生成用例测试完毕")

    def test_lyrics_mode_v5(self, logged_in_page):
        """Somio V5 模型 - 歌词模式生成"""
        lp = LyricsPage(logged_in_page)
        success, song_title = lp.run_model_generation_flow(
            "V5", Locators.MODEL_VERSION_V5,
            provider_locator=Locators.MODEL_PROVIDER_SOMIO
        )
        assert success, f"歌词模式 Somio V5 模型生成 '{song_title}' 超时或失败"
        logger.success("歌词模式 Somio V5 模型生成用例测试完毕")

    # def test_lyrics_mode_v4_5_plus(self, logged_in_page):
    #     """Somio V4.5+ 模型 - 歌词模式生成"""
    #     lp = LyricsPage(logged_in_page)
    #     success, song_title = lp.run_model_generation_flow(
    #         "V4.5+", Locators.MODEL_VERSION_V4_5_PLUS,
    #         provider_locator=Locators.MODEL_PROVIDER_SOMIO
    #     )
    #     assert success, f"歌词模式 Somio V4.5+ 模型生成 '{song_title}' 超时或失败"
    #     logger.success("歌词模式 Somio V4.5+ 模型生成用例测试完毕")

    # def test_lyrics_mode_v4_5(self, logged_in_page):
    #     """Somio V4.5 模型 - 歌词模式生成"""
    #     lp = LyricsPage(logged_in_page)
    #     success, song_title = lp.run_model_generation_flow(
    #         "V4.5", Locators.MODEL_VERSION_V4_5,
    #         provider_locator=Locators.MODEL_PROVIDER_SOMIO
    #     )
    #     assert success, f"歌词模式 Somio V4.5 模型生成 '{song_title}' 超时或失败"
    #     logger.success("歌词模式 Somio V4.5 模型生成用例测试完毕")

    # def test_lyrics_mode_v4(self, logged_in_page):
    #     """Somio V4 模型 - 歌词模式生成"""
    #     lp = LyricsPage(logged_in_page)
    #     success, song_title = lp.run_model_generation_flow(
    #         "V4", Locators.MODEL_VERSION_V4,
    #         provider_locator=Locators.MODEL_PROVIDER_SOMIO
    #     )
    #     assert success, f"歌词模式 Somio V4 模型生成 '{song_title}' 超时或失败"
    #     logger.success("歌词模式 Somio V4 模型生成用例测试完毕")

    def test_lyrics_mode_v3_5(self, logged_in_page):
        """Somio V3.5 模型 - 歌词模式生成"""
        lp = LyricsPage(logged_in_page)
        success, song_title = lp.run_model_generation_flow(
            "V3.5", Locators.MODEL_VERSION_V3_5,
            provider_locator=Locators.MODEL_PROVIDER_SOMIO
        )
        assert success, f"歌词模式 Somio V3.5 模型生成 '{song_title}' 超时或失败"
        logger.success("歌词模式 Somio V3.5 模型生成用例测试完毕")

    # --- Google 模型 ---

    # def test_lyrics_mode_lyria3(self, logged_in_page):
    #     """Google Lyria3 模型 - 歌词模式生成"""
    #     lp = LyricsPage(logged_in_page)
    #     success, song_title = lp.run_model_generation_flow(
    #         "Lyria3",
    #         Locators.MODEL_VERSION_LYRICS3,
    #         provider_locator=Locators.MODEL_PROVIDER_GOOGLE
    #     )
    #     assert success, f"歌词模式 Google Lyria3 模型生成 '{song_title}' 超时或失败"
    #     logger.success("歌词模式 Google Lyria3 模型生成用例测试完毕")

    # # --- MINIMAX 模型 ---

    # def test_lyrics_mode_minimax_v2_6(self, logged_in_page):
    #     """MINIMAX V2.6 模型 - 歌词模式生成"""
    #     lp = LyricsPage(logged_in_page)
    #     success, song_title = lp.run_model_generation_flow(
    #         "Minimax-V2.6",
    #         Locators.MODEL_VERSION_MINIMAX_V2_6,
    #         provider_locator=Locators.MODEL_PROVIDER_MINIMAX
    #     )
    #     assert success, f"歌词模式 MINIMAX V2.6 模型生成 '{song_title}' 超时或失败"
    #     logger.success("歌词模式 MINIMAX V2.6 模型生成用例测试完毕")

    # def test_lyrics_mode_minimax_v2_5_plus(self, logged_in_page):
    #     """MINIMAX V2.5+ 模型 - 歌词模式生成"""
    #     lp = LyricsPage(logged_in_page)
    #     success, song_title = lp.run_model_generation_flow(
    #         "Minimax-V2.5+",
    #         Locators.MODEL_VERSION_MINIMAX_V2_5_PLUS,
    #         provider_locator=Locators.MODEL_PROVIDER_MINIMAX
    #     )
    #     assert success, f"歌词模式 MINIMAX V2.5+ 模型生成 '{song_title}' 超时或失败"
    #     logger.success("歌词模式 MINIMAX V2.5+ 模型生成用例测试完毕")

    # def test_lyrics_mode_minimax_v2_5(self, logged_in_page):
    #     """MINIMAX V2.5 模型 - 歌词模式生成"""
    #     lp = LyricsPage(logged_in_page)
    #     success, song_title = lp.run_model_generation_flow(
    #         "Minimax-V2.5",
    #         Locators.MODEL_VERSION_MINIMAX_V2_5,
    #         provider_locator=Locators.MODEL_PROVIDER_MINIMAX
    #     )
    #     assert success, f"歌词模式 MINIMAX V2.5 模型生成 '{song_title}' 超时或失败"
    #     logger.success("歌词模式 MINIMAX V2.5 模型生成用例测试完毕")
