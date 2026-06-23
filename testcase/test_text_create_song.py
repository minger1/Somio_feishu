import pytest
from pages.text_page import TextPage
from config.locators import Locators
from utils import logger, get_song
from data.test_data import TEST_TEXT_PROMPT, TEST_TEXT_EASY_PROMPT


class TestTextCreateSong:
    """文本模式(Prompt Tab)生成歌曲功能测试用例"""

    # ==================================================================
    # 简单输入 → AI 分析弹窗流程
    # ==================================================================

    # def test_text_simple_ai_analysis_original(self, logged_in_page):
    #     """
    #     [用例描述]：输入简单文本触发 AI 分析弹窗，在弹窗中选择 Original Version 生成。
    #     """
    #     logger.info("开始测试：简单文本 → AI分析弹窗 → Original Version")
    #     text_page = TextPage(logged_in_page)
    #     song_title = get_song(prefix="TEXT", model="SIMPLE-ORIGINAL")

    #     success = text_page.run_generation_flow(
    #         text=TEST_TEXT_EASY_PROMPT,
    #         song_title=song_title,
    #         action="original",
    #         timeout=360000
    #     )
    #     assert success, f"歌曲 '{song_title}' 生成失败或超时"
    #     logger.success("简单文本 → AI分析 → Original Version 用例测试完毕")

    def test_text_simple_ai_analysis_create_now(self, logged_in_page):
        """
        [用例描述]：输入简单文本触发 AI 分析弹窗，在弹窗中点击 Create Now (AI增强) 生成。
        """
        logger.info("开始测试：简单文本 → AI分析弹窗 → Create Now (AI)")
        text_page = TextPage(logged_in_page)
        song_title = get_song(prefix="TEXT", model="SIMPLE-AI")

        success = text_page.run_generation_flow(
            text=TEST_TEXT_EASY_PROMPT,
            song_title=song_title,
            action="ai",
            timeout=360000
        )
        assert success, f"歌曲 '{song_title}' 生成失败或超时"
        logger.success("简单文本 → AI分析 → Create Now 用例测试完毕")

    # def test_text_simple_ai_analysis_view_lyrics(self, logged_in_page):
    #     """
    #     [用例描述]：输入简单文本触发 AI 分析弹窗，进入 View Lyrics 查看并生成歌词，最终创建音乐。
    #     Text 模式独有：可从 AI 分析弹窗进入歌词编辑页面，生成歌词后再创建。
    #     """
    #     logger.info("开始测试：简单文本 → AI分析弹窗 → View Lyrics → 生成歌词 → 创建")
    #     text_page = TextPage(logged_in_page)
    #     song_title = get_song(prefix="TEXT", model="SIMPLE-VIEWLYRICS")

    #     success = text_page.run_generation_flow(
    #         text=TEST_TEXT_EASY_PROMPT,
    #         song_title=song_title,
    #         action="view_lyrics",
    #         timeout=600000
    #     )
    #     assert success, f"歌曲 '{song_title}' 生成失败或超时"
    #     logger.success("简单文本 → View Lyrics 链路用例测试完毕")

    # # ==================================================================
    # # 标准文本 → 直接生成（不触发 AI 分析弹窗）
    # # ==================================================================

    # def test_text_standard_direct_generation(self, logged_in_page):
    #     """
    #     [用例描述]：输入标准描述词，系统判断无需 AI 分析，直接跳过弹窗完成生成。
    #     """
    #     logger.info("开始测试：标准文本 → 直接生成（跳过 AI 分析）")
    #     text_page = TextPage(logged_in_page)
    #     song_title = get_song(prefix="TEXT", model="STANDARD-DIRECT")

    #     success = text_page.run_standard_generation_flow(
    #         text=TEST_TEXT_PROMPT,
    #         song_title=song_title,
    #         timeout=360000
    #     )
    #     assert success, f"标准文本直接生成歌曲 '{song_title}' 失败或超时"
    #     logger.success("标准文本直接生成用例测试完毕")

    # ==================================================================
    # 所有模型切换测试（标准文本直接生成）
    # ==================================================================

    # --- Somio.ai 模型 ---

    def test_text_mode_v5_5(self, logged_in_page):
        """Somio V5.5 模型生成"""
        text_page = TextPage(logged_in_page)
        success, song_title = text_page.run_model_generation_flow(
            "V5.5", Locators.MODEL_VERSION_V5_5,
            provider_locator=Locators.MODEL_PROVIDER_SOMIO
        )
        assert success, f"纯文本模式 Somio V5.5 模型生成 '{song_title}' 超时或失败"
        logger.success("纯文本模式 Somio V5.5 模型生成用例测试完毕")

    def test_text_mode_v5(self, logged_in_page):
        """Somio V5 模型生成"""
        text_page = TextPage(logged_in_page)
        success, song_title = text_page.run_model_generation_flow(
            "V5", Locators.MODEL_VERSION_V5,
            provider_locator=Locators.MODEL_PROVIDER_SOMIO
        )
        assert success, f"纯文本模式 Somio V5 模型生成 '{song_title}' 超时或失败"
        logger.success("纯文本模式 Somio V5 模型生成用例测试完毕")

    # def test_text_mode_v4_5_plus(self, logged_in_page):
    #     """Somio V4.5+ 模型生成"""
    #     text_page = TextPage(logged_in_page)
    #     success, song_title = text_page.run_model_generation_flow(
    #         "V4.5+", Locators.MODEL_VERSION_V4_5_PLUS,
    #         provider_locator=Locators.MODEL_PROVIDER_SOMIO
    #     )
    #     assert success, f"纯文本模式 Somio V4.5+ 模型生成 '{song_title}' 超时或失败"
    #     logger.success("纯文本模式 Somio V4.5+ 模型生成用例测试完毕")

    # def test_text_mode_v4_5(self, logged_in_page):
    #     """Somio V4.5 模型生成"""
    #     text_page = TextPage(logged_in_page)
    #     success, song_title = text_page.run_model_generation_flow(
    #         "V4.5", Locators.MODEL_VERSION_V4_5,
    #         provider_locator=Locators.MODEL_PROVIDER_SOMIO
    #     )
    #     assert success, f"纯文本模式 Somio V4.5 模型生成 '{song_title}' 超时或失败"
    #     logger.success("纯文本模式 Somio V4.5 模型生成用例测试完毕")

    # def test_text_mode_v4(self, logged_in_page):
    #     """Somio V4 模型生成"""
    #     text_page = TextPage(logged_in_page)
    #     success, song_title = text_page.run_model_generation_flow(
    #         "V4", Locators.MODEL_VERSION_V4,
    #         provider_locator=Locators.MODEL_PROVIDER_SOMIO
    #     )
    #     assert success, f"纯文本模式 Somio V4 模型生成 '{song_title}' 超时或失败"
    #     logger.success("纯文本模式 Somio V4 模型生成用例测试完毕")

    # def test_text_mode_v3_5(self, logged_in_page):
    #     """Somio V3.5 模型生成"""
    #     text_page = TextPage(logged_in_page)
    #     success, song_title = text_page.run_model_generation_flow(
    #         "V3.5", Locators.MODEL_VERSION_V3_5,
    #         provider_locator=Locators.MODEL_PROVIDER_SOMIO
    #     )
    #     assert success, f"纯文本模式 Somio V3.5 模型生成 '{song_title}' 超时或失败"
    #     logger.success("纯文本模式 Somio V3.5 模型生成用例测试完毕")

    # --- Google 模型 ---

    def test_text_mode_lyria3(self, logged_in_page):
        """Google Lyria3 模型生成"""
        text_page = TextPage(logged_in_page)
        success, song_title = text_page.run_model_generation_flow(
            "Lyria3",
            Locators.MODEL_VERSION_LYRICS3,
            provider_locator=Locators.MODEL_PROVIDER_GOOGLE
        )
        assert success, f"纯文本模式 Google Lyria3 模型生成 '{song_title}' 超时或失败"
        logger.success("纯文本模式 Google Lyria3 模型生成用例测试完毕")

    # --- MINIMAX 模型 ---

    def test_text_mode_minimax_v2_6(self, logged_in_page):
        """MINIMAX V2.6 模型生成"""
        text_page = TextPage(logged_in_page)
        success, song_title = text_page.run_model_generation_flow(
            "Minimax-V2.6",
            Locators.MODEL_VERSION_MINIMAX_V2_6,
            provider_locator=Locators.MODEL_PROVIDER_MINIMAX
        )
        assert success, f"纯文本模式 MINIMAX V2.6 模型生成 '{song_title}' 超时或失败"
        logger.success("纯文本模式 MINIMAX V2.6 模型生成用例测试完毕")

    # def test_text_mode_minimax_v2_5_plus(self, logged_in_page):
    #     """MINIMAX V2.5+ 模型生成"""
    #     text_page = TextPage(logged_in_page)
    #     success, song_title = text_page.run_model_generation_flow(
    #         "Minimax-V2.5+",
    #         Locators.MODEL_VERSION_MINIMAX_V2_5_PLUS,
    #         provider_locator=Locators.MODEL_PROVIDER_MINIMAX
    #     )
    #     assert success, f"纯文本模式 MINIMAX V2.5+ 模型生成 '{song_title}' 超时或失败"
    #     logger.success("纯文本模式 MINIMAX V2.5+ 模型生成用例测试完毕")

    # def test_text_mode_minimax_v2_5(self, logged_in_page):
    #     """MINIMAX V2.5 模型生成"""
    #     text_page = TextPage(logged_in_page)
    #     success, song_title = text_page.run_model_generation_flow(
    #         "Minimax-V2.5",
    #         Locators.MODEL_VERSION_MINIMAX_V2_5,
    #         provider_locator=Locators.MODEL_PROVIDER_MINIMAX
    #     )
    #     assert success, f"纯文本模式 MINIMAX V2.5 模型生成 '{song_title}' 超时或失败"
    #     logger.success("纯文本模式 MINIMAX V2.5 模型生成用例测试完毕")
