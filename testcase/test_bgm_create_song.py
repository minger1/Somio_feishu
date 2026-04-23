from pages.bgm_page import BgmPage
from utils import get_song, logger
from data.test_data import TEST_BGM_PROMPT

class TestBgmCreateSong:
    """BGM 背景音乐(纯音乐)模式生成歌曲功能测试用例"""

    def test_bgm_mode_generation_original(self, logged_in_page):
        """
        [用例描述]：测试进入 BGM (无歌词纯音乐) 专属创作模式，并使用原输入描述(Original Version)强推生成的流程。
        [业务环节]：
        1. 路由切换：主动切分至 BGM Tab 引擎
        2. 数据装配：埋入 BGM 专属长文本意境词 + 提取一次性 Title 追踪码
        3. 发起请求：点击生成并等待 AI 云端曲风评估返回
        4. 原始路线：在弹窗中坚决选择 'Original Version'
        5. 落盘验证：支付积分 Confirm 后死守列表展示完成
        """
        logger.info("开始测试 BGM Original 生成用例")
        bp = BgmPage(logged_in_page)

        logger.info("切换 Tab 到 BGM 生成器")
        bp.switch_to_bgm_tab()
        
        logger.info(f"输入 BGM 描述词: {TEST_BGM_PROMPT[:15]}...")
        bp.input_prompt(TEST_BGM_PROMPT)
        
        song_title = get_song()
        logger.info(f"输入歌曲名称: '{song_title}'")
        bp.input_song_title(song_title)

        logger.info("点击 Create")
        bp.click_create()
        
        logger.info("等待 AI分析模态窗...")
        bp.wait_for_ai_analysis()
        
        logger.info("选择 Original Version")
        bp.select_original_version()
        
        logger.info("确认扣费弹窗 (Continue)")
        bp.confirm_generation()

        logger.info("轮询等待作品生成...")
        success = bp.wait_for_generation_success(title=song_title)
        assert success, f"BGM Original 歌曲 '{song_title}' 生成失败或超时"
        logger.success("BGM Original 链路生成用例测试完毕")

    def test_bgm_mode_generation_create_now(self, logged_in_page):
        """
        [用例描述]：测试在 BGM 纯音乐专区，接受 AI 的意境词重构润色，使用 'Create Now' 生成进阶纯音的流程。
        [业务环节]：
        1. 路由切换：主动切分至 BGM Tab 引擎
        2. 数据装配：埋入 BGM 意境描述 + 关联测试专用标题
        3. 接受魔改：生成确认期内，点击 'Create Now (AI)' 接纳平台提示词大模型的意境强化洗稿
        4. 落盘验证：付积分并等待 GPU 返厂下线
        """
        logger.info("开始测试 BGM Create Now (AI增强) 生成用例")
        bp = BgmPage(logged_in_page)

        logger.info("切换 Tab 到 BGM 生成器")
        bp.switch_to_bgm_tab()
        
        logger.info(f"输入 BGM 描述词: {TEST_BGM_PROMPT[:15]}...")
        bp.input_prompt(TEST_BGM_PROMPT)
        
        song_title = get_song()
        logger.info(f"输入歌曲名称: '{song_title}'")
        bp.input_song_title(song_title)

        logger.info("点击 Create")
        bp.click_create()
        
        logger.info("等待 AI分析模态窗...")
        bp.wait_for_ai_analysis()
        
        logger.info("选择 Create Now (AI增强)")
        bp.select_create_now()
        
        logger.info("确认扣费弹窗 (Continue)")
        bp.confirm_generation()

        logger.info("轮询等待作品生成...")
        success = bp.wait_for_generation_success(title=song_title)
        assert success, f"BGM AI 增强歌曲 '{song_title}' 生成失败或超时"
        logger.success("BGM Create Now (AI增强) 生成用例测试完毕")
