import pytest
from pages.text_page import TextPage
from utils import logger
from utils import get_song
from data.test_data import TEST_TEXT_PROMPT

class TestTextCreateSong:
    """文本模式生成歌曲功能测试用例"""

    # def test_text_mode_generation_original(self, logged_in_page):
    #     """
    #     [用例描述]：测试文本模式下，拒绝 AI 修改，坚持使用原始输入数据完成歌曲生成的全生命周期流程。
    #     [业务流程]：
    #     1. 填充文本框 (Prompt)
    #     2. 给定唯一识别歌曲命名并点击创建
    #     3. 在高时延 AI 分析拦截弹窗处耐心等候并强硬选择 'Original Version'
    #     4. 在扣费 Confirm 积分弹窗处确认 'Continue'
    #     5. 对接后台轮询接口直至库中明确展示该歌曲已 Generate 成功完毕
    #     """
    #     logger.info("开始测试纯文本 Original 生成用例")
    #     page = logged_in_page
    #     text_page = TextPage(page)
        
    #     # 1. 输入文本
    #     test_text = TEST_TEXT_PROMPT
    #     logger.info(f"填入剧本提示词: {test_text[:20]}...")
    #     text_page.text_input(test_text)
        
    #     # 1.5 输入唯一歌名
    #     song_title = get_song()
    #     logger.info(f"填入歌曲名称: '{song_title}'")
    #     text_page.song_title_input(song_title)
        
    #     # 2. 点击创建
    #     logger.info("点击 Create")
    #     text_page.click_create()

    #     # 3. 等待ai分析成功
    #     logger.info("等待 AI 分析模态窗")
    #     text_page.text_ai_analysis_popup()
        
    #     # 4. 处理 AI 分析弹窗 (选择原始版本)
    #     logger.info("选择 Original Version")
    #     text_page.text_select_original()
        
    #     # 5. 确认生成
    #     logger.info("确认生成 (Continue)")
    #     text_page.confirm_generation()
        
    #     # 6. 验证生成成功 (根据歌名追踪)
    #     logger.info("轮询等待作品生成...")
    #     success = text_page.wait_for_generation_success(title=song_title, timeout=360000) 
        
    #     assert success, f"歌曲 '{song_title}' 生成失败或超时"
    #     logger.success("纯文本 Original 生成用例测试完毕")

    # def test_text_mode_generation_ai(self, logged_in_page):
    #     """
    #     [用例描述]：测试文本模式下，主动接纳 AI 大模型流派/风格魔改并使用其增强数据生成歌曲的全链路。
    #     [业务流程]：
    #     1. 填充基础文本梗概
    #     2. 给定识别命名并下发创建请求
    #     3. 在 AI 分析弹窗处顺从系统，选择 'Create Now (AI)' 走大模型强化生成路径
    #     4. 确认扣死额度
    #     5. 长轮询等待任务渲染完成
    #     """
    #     logger.info("开始测试纯文本 AI 增强生成用例")
    #     page = logged_in_page
    #     text_page = TextPage(page)
        
    #     # 1. 输入文本
    #     test_text = TEST_TEXT_PROMPT
    #     logger.info(f"填入剧本提示词: {test_text[:20]}...")
    #     text_page.text_input(test_text)
        
    #     # 1.5 输入唯一歌名
    #     song_title = get_song()
    #     logger.info(f"填入歌曲名称: '{song_title}'")
    #     text_page.song_title_input(song_title)
        
    #     # 2. 点击创建
    #     logger.info("点击 Create")
    #     text_page.click_create()
        
    #     # 3. 等待ai分析成功
    #     logger.info("等待 AI 分析模态窗")
    #     text_page.text_ai_analysis_popup()
        
    #     # 4. 处理 AI 分析弹窗 (选择AI生成)
    #     logger.info("选择 Create Now (AI增强)")
    #     text_page.text_select_create_now()
        
    #     # 5. 确认生成
    #     logger.info("确认扣费弹窗 (Continue)")
    #     text_page.confirm_generation()
        
    #     # 6. 验证生成成功 (根据歌名追踪)
    #     logger.info("轮询等待作品生成...")
    #     success = text_page.wait_for_generation_success(title=song_title, timeout=300000)
        
    #     assert success, f"AI 增强歌曲 '{song_title}' 生成失败或超时"
    #     logger.success("纯文本 AI 增强生成用例测试完毕")


    # def test_text_mode_generation_view_lyrics(self, logged_in_page):
    #     """
    #     [用例描述]：测试最复杂的歌词二创链路。从单纯的纯文本启动，流经 AI 分析，并不直接生成而是下钻到歌词编辑器，
    #     手动补丁修改歌名后，最终投递生成的超长工作流体验。
    #     [业务流程]：
    #     1. 填充纯文本梗概 -> 提交 Create
    #     2. 弹窗中选择下钻 'View Lyrics' 进入精细化编辑页
    #     3. 手动洗刷被 AI 覆盖的歌名
    #     4. 再次呼叫底层的 [Generate]
    #     5. 长轮询拦截产物
    #     """
    #     logger.info("开始测试纯文本 -> View Lyrics 生成用例")
    #     page = logged_in_page
    #     text_page = TextPage(page)
        
    #     # 1. 输入文本
    #     test_text = TEST_TEXT_PROMPT
    #     logger.info(f"填入剧本提示词: {test_text[:20]}...")
    #     text_page.text_input(test_text)
        
    #     # 1.5 输入唯一歌名
    #     song_title = get_song()
    #     logger.info(f"填入歌曲名称: '{song_title}'")
    #     text_page.song_title_input(song_title)
        
    #     # 2. 点击创建
    #     logger.info("点击 Create")
    #     text_page.click_create()

    #     # 3. 等待ai分析成功
    #     logger.info("等待 AI 分析模态窗")
    #     text_page.text_ai_analysis_popup()
        
    #     # 4. 处理 AI 分析弹窗 (选择查看歌词)
    #     logger.info("选择 View Lyrics 进入工作室")
    #     text_page.text_select_view_lyrics()

    #     # 4.5 修改被AI覆盖的歌名，保证后续能通过歌名追踪
    #     logger.info(f"恢复歌名标记为 '{song_title}'")
    #     text_page.edit_generated_lyrics_title(song_title)

    #     # 5. 点击生成歌词
    #     logger.info("点击深入面板页面的 Generate 按钮")
    #     text_page.text_select_view_lyrics_generate()
        
    #     # 6. 验证生成成功 (根据歌名追踪)
    #     logger.info("轮询等待作品生成...")
    #     success = text_page.wait_for_generation_success(title=song_title, timeout=600000)
        
    #     assert success, f"深度修改歌曲 '{song_title}' 生成失败或超时"
    #     logger.success("纯文本 View Lyrics 深度修改路线生成用例测试完毕")

    # # ------------------------------------------------------------------
    # # 模型切换测试
    # # ------------------------------------------------------------------

    # def test_text_mode_v5_5(self, logged_in_page):
    #     from config.locators import Locators
    #     text_page = TextPage(logged_in_page)
    #     success, song_title = text_page.run_model_generation_flow("V5.5", Locators.MODEL_VERSION_V5_5)
    #     assert success, f"纯文本模式 V5.5 模型生成歌曲 '{song_title}' 超时或失败"
    #     logger.success("纯文本模式 V5.5 模型生成用例测试完毕")

    def test_text_mode_v5(self, logged_in_page):
        from config.locators import Locators
        text_page = TextPage(logged_in_page)
        success, song_title = text_page.run_model_generation_flow("V5", Locators.MODEL_VERSION_V5)
        assert success, f"纯文本模式 V5 模型生成歌曲 '{song_title}' 超时或失败"
        logger.success("纯文本模式 V5 模型生成用例测试完毕")

    # def test_text_mode_v4_5_plus(self, logged_in_page):
    #     from config.locators import Locators
    #     text_page = TextPage(logged_in_page)
    #     success, song_title = text_page.run_model_generation_flow("V4.5+", Locators.MODEL_VERSION_V4_5_PLUS)
    #     assert success, f"纯文本模式 V4.5+ 模型生成歌曲 '{song_title}' 超时或失败"
    #     logger.success("纯文本模式 V4.5+ 模型生成用例测试完毕")

    # def test_text_mode_v4_5(self, logged_in_page):
    #     from config.locators import Locators
    #     text_page = TextPage(logged_in_page)
    #     success, song_title = text_page.run_model_generation_flow("V4.5", Locators.MODEL_VERSION_V4_5)
    #     assert success, f"纯文本模式 V4.5 模型生成歌曲 '{song_title}' 超时或失败"
    #     logger.success("纯文本模式 V4.5 模型生成用例测试完毕")

    # def test_text_mode_v3_5(self, logged_in_page):
    #     from config.locators import Locators
    #     text_page = TextPage(logged_in_page)
    #     success, song_title = text_page.run_model_generation_flow("V3.5", Locators.MODEL_VERSION_V3_5)
    #     assert success, f"纯文本模式 V3.5 模型生成歌曲 '{song_title}' 超时或失败"
    #     logger.success("纯文本模式 V3.5 模型生成用例测试完毕")
