from pages.lyrics_page import LyricsPage
from utils import get_song, logger
from data.test_data import NON_STANDARD_LYRICS, STANDARD_LYRICS
from config.locators import Locators

class TestLyricsCreateSong:
    """歌词模式(Lyrics Tab)下生成音乐的全量生命周期与弹窗流测试集"""

    # ------------------------------------------------------------------
    # 不规范歌词 - Lyrics Formatting 分页（默认）
    # ------------------------------------------------------------------

    # def test_lyrics_non_standard_formatting_original(self, logged_in_page):
    #     """
    #     [用例描述]: 测试输入非标准格式杂乱歌词后，系统呼出AI分析弹窗，
    #     在 Formatting (单纯排版格式化) 选项卡下，强行采用 Original Version 生成音频。
    #     """
    #     logger.info("开始测试：乱码歌词 -> [Formatting 修版面板] -> [Original Version]")
    #     lp = LyricsPage(logged_in_page)
    #     song_title = get_song()
        
    #     logger.info(f"输入非标准歌词及标题: '{song_title}', 采取 Original 操作")
    #     lp.run_non_standard_flow(
    #         lyrics=NON_STANDARD_LYRICS,
    #         song_title=song_title,
    #         tab_index=0,
    #         action="original",
    #     )
        
    #     logger.info("轮询等待作品生成...")
    #     success = lp.wait_for_generation_success(title=song_title)
    #     assert success, f"Formatting 面板 Original Version 生成歌曲 '{song_title}' 超时或失败"
    #     logger.success("Formatting + Original 流程测试通过")

    # def test_lyrics_non_standard_formatting_create_now(self, logged_in_page):
    #     """
    #     [用例描述]: 测试在非标乱排歌词呼出 AI 分析弹窗后，
    #     在 Formatting (单纯排版格式化) 面板中点选 'Create Now' 接纳魔改格式。
    #     """
    #     logger.info("开始测试：乱码歌词 -> [Formatting 修版面板] -> [Create Now(AI)]")
    #     lp = LyricsPage(logged_in_page)
    #     song_title = get_song()
        
    #     logger.info(f"输入非标准歌词及标题: '{song_title}', 采取 AI Create 操作")
    #     lp.run_non_standard_flow(
    #         lyrics=NON_STANDARD_LYRICS,
    #         song_title=song_title,
    #         tab_index=0,
    #         action="ai",
    #     )
        
    #     logger.info("轮询等待作品生成...")
    #     success = lp.wait_for_generation_success(title=song_title)
    #     assert success, f"Formatting 面板 Create Now 生成歌曲 '{song_title}' 超时或失败"
    #     logger.success("Formatting + Create Now 流程测试通过")

    # # ------------------------------------------------------------------
    # # 不规范歌词 - Lyrics Refinement 分页（切换后）
    # # ------------------------------------------------------------------

    # def test_lyrics_non_standard_refinement_original(self, logged_in_page):
    #     """
    #     [用例描述]: 测试非标乱排歌词呼出弹窗后，手动切入更加激进的 Refinement (AI润色扩写) 选项卡，
    #     但在最后生成关头反悔，依旧选择 'Original Version' 原始流生成。
    #     """
    #     logger.info("开始测试：乱码歌词 -> [Refinement 深度优化面板] -> [Original Version]")
    #     lp = LyricsPage(logged_in_page)
    #     song_title = get_song()
        
    #     logger.info(f"输入标题: '{song_title}', 切换到 Refinement 面板后采取 Original 操作")
    #     lp.run_non_standard_flow(
    #         lyrics=NON_STANDARD_LYRICS,
    #         song_title=song_title,
    #         tab_index=1,
    #         action="original",
    #     )
        
    #     logger.info("轮询等待作品生成...")
    #     success = lp.wait_for_generation_success(title=song_title)
    #     assert success, f"Refinement 下 Original 生成 '{song_title}' 超时或失败"
    #     logger.success("Refinement + Original 流程测试通过")

    # def test_lyrics_non_standard_refinement_create_now(self, logged_in_page):
    #     """
    #     [用例描述]: 测试非标乱排歌词在弹窗中切入 Refinement (AI润色扩写) 选项页后，
    #     激进地拥抱 AI 大模型改写，点击 'Create Now' 生成出增强修缮版的全量流程。
    #     """
    #     logger.info("开始测试：乱码歌词 -> [Refinement 深度优化面板] -> [Create Now(AI)]")
    #     lp = LyricsPage(logged_in_page)
    #     song_title = get_song()
        
    #     logger.info(f"输入标题 '{song_title}', 切换至 Refinement 面板后采取 AI 操作")
    #     lp.run_non_standard_flow(
    #         lyrics=NON_STANDARD_LYRICS,
    #         song_title=song_title,
    #         tab_index=1,
    #         action="ai",
    #     )
        
    #     logger.info("轮询等待作品生成...")
    #     success = lp.wait_for_generation_success(title=song_title)
    #     assert success, f"Refinement + Create Now 生成单曲 '{song_title}' 失败！"
    #     logger.success("Refinement + Create Now 流程测试通过")

    # # ------------------------------------------------------------------
    # # 规范歌词 - 直接创建（不触发 AI 分析）
    # # ------------------------------------------------------------------

    # def test_lyrics_standard_direct_creation(self, logged_in_page):
    #     """
    #     [用例描述]: 测试填入格式及其极其规整严谨、无破绽的标准结构化体例歌词时，
    #     系统应判断为高质量无须 AI 强干涉，直接绕过 'AI Analysis' 弹窗，直达 Confirm 生成确认的快审流程。
    #     """
    #     logger.info("开始测试：标准规范歌词 [极速直通生成]")
        
    #     lp = LyricsPage(logged_in_page)
    #     page = logged_in_page
        
    #     logger.info("切换到 Lyrics 选项卡")
    #     lp.switch_to_lyrics_tab()
        
    #     logger.info("填入规范排版的歌词")
    #     lp.input_lyrics(STANDARD_LYRICS)
        
    #     song_title = get_song()
    #     logger.info(f"填入歌曲名称 '{song_title}'")
    #     lp.input_song_title(song_title)

    #     logger.info("点击 Create")
    #     lp.click_create()
        
    #     logger.info("验证不会弹出 AI 分析弹窗")
    #     # 规范歌词不应触发 AI 分析弹窗
    #     assert not page.locator(Locators.AI_ANALYSIS_MODAL).is_visible(timeout=5000), \
    #         "规范歌词误触发了 AI 诊断弹窗"
            
    #     logger.info("确认扣费生成")
    #     lp.confirm_generation()

    #     logger.info("轮询等待作品生成...")
    #     success = lp.wait_for_generation_success(title=song_title)
    #     assert success, f"规范歌词生成的歌曲 '{song_title}' 失败或超时"
    #     logger.success("免检直通生成链路测试完毕")

    # ------------------------------------------------------------------
    # 模型切换测试
    # ------------------------------------------------------------------

    def test_lyrics_mode_v5_5(self, logged_in_page):
        lp = LyricsPage(logged_in_page)
        success, song_title = lp.run_model_generation_flow("V5.5", Locators.MODEL_VERSION_V5_5)
        assert success, f"歌词模式 V5.5 模型生成歌曲 '{song_title}' 超时或失败"
        logger.success("歌词模式 V5.5 模型生成用例测试完毕")

    # def test_lyrics_mode_v5(self, logged_in_page):
    #     lp = LyricsPage(logged_in_page)
    #     success, song_title = lp.run_model_generation_flow("V5", Locators.MODEL_VERSION_V5)
    #     assert success, f"歌词模式 V5 模型生成歌曲 '{song_title}' 超时或失败"
    #     logger.success("歌词模式 V5 模型生成用例测试完毕")

    # def test_lyrics_mode_v4_5_plus(self, logged_in_page):
    #     lp = LyricsPage(logged_in_page)
    #     success, song_title = lp.run_model_generation_flow("V4.5+", Locators.MODEL_VERSION_V4_5_PLUS)
    #     assert success, f"歌词模式 V4.5+ 模型生成歌曲 '{song_title}' 超时或失败"
    #     logger.success("歌词模式 V4.5+ 模型生成用例测试完毕")

    # def test_lyrics_mode_v4_5(self, logged_in_page):
    #     lp = LyricsPage(logged_in_page)
    #     success, song_title = lp.run_model_generation_flow("V4.5", Locators.MODEL_VERSION_V4_5)
    #     assert success, f"歌词模式 V4.5 模型生成歌曲 '{song_title}' 超时或失败"
    #     logger.success("歌词模式 V4.5 模型生成用例测试完毕")

    def test_lyrics_mode_v3_5(self, logged_in_page):
        lp = LyricsPage(logged_in_page)
        success, song_title = lp.run_model_generation_flow("V3_5", Locators.MODEL_VERSION_V3_5)
        assert success, f"歌词模式 V3_5 模型生成歌曲 '{song_title}' 超时或失败"
        logger.success("歌词模式 V3_5 模型生成用例测试完毕")
