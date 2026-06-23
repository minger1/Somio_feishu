from pages.bgm_page import BgmPage
from utils import get_song, logger
from data.test_data import TEST_BGM_PROMPT


class TestBgmCreateSong:
    """BGM 背景音乐(纯音乐)模式生成歌曲功能测试用例"""

    def test_bgm_standard_direct_generation(self, logged_in_page):
        """
        [用例描述]：BGM 模式输入标准描述词，系统判断无需 AI 分析，
        直接跳过弹窗完成纯音乐生成的快审流程。
        [业务环节]：
        1. 路由切换：主动切分至 BGM Tab 引擎
        2. 数据装配：埋入 BGM 专属标准长文本描述词 + 提取一次性 Title 追踪码
        3. 发起请求：点击生成
        4. 标准路线：不触发 AI 分析弹窗，直接处理扣费确认
        5. 落盘验证：等待列表展示完成
        """
        logger.info("开始测试 BGM 标准文案直接生成用例")
        bp = BgmPage(logged_in_page)
        song_title = get_song(prefix="BGM", model="STANDARD-DIRECT")

        success = bp.run_standard_generation_flow(
            prompt=TEST_BGM_PROMPT,
            song_title=song_title,
            timeout=360000
        )
        assert success, f"BGM 标准直接生成歌曲 '{song_title}' 失败或超时"
        logger.success("BGM 标准文案直接生成用例测试完毕")
