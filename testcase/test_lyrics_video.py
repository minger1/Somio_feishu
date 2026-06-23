import pytest
from pages.lyrics_video_page import LyricsVideoPage
from utils import logger
from config.settings import TEST_AUDIO_PATH_3, TEST_IMAGE_PATH, TEST_IMAGE_PROMPT

class TestLyricsVideo:
    """AI歌词视频功能测试集"""

    def test_lyrics_video_local_audio_and_image(self, logged_in_page):
        """
        [用例 1]：导入本地音乐baby.mp3和女巫图片进行处理
        1. 切换到歌词视频生成页面
        2. 上传本地音乐 baby.mp3
        3. 上传本地背景图 女巫.jpg
        4. 点击立即创作，生成歌词视频
        5. 在当前页面视频播放器区域校验视频生成成功
        """
        logger.info("开始测试：导入本地音乐和图片处理歌词视频")
        page_obj = LyricsVideoPage(logged_in_page)
        page_obj.switch_to_lyrics_video()

        # 1. 导入音频文件与背景图 (直接导入 settings 中定义的文件路径)
        page_obj.upload_local_audio(TEST_AUDIO_PATH_3)
        page_obj.upload_background_image(TEST_IMAGE_PATH)

        # 2. 提交生成并处理积分扣减确认
        page_obj.click_create()

        # 3. 轮询等待视频生成成功
        success = page_obj.wait_for_generation_success(timeout=360000)
        assert success, "测试用例1：歌词视频生成超时或失败"
        logger.success("测试用例1：导入本地音乐和女巫图片生成成功！")

    def test_lyrics_video_local_audio_and_prompt_image(self, logged_in_page):
        """
        [用例 2]：导入本地音乐，和输入图片prompt生成图片，图片生成成功
        1. 切换到歌词视频生成页面
        2. 上传本地音乐 baby.mp3
        3. 输入图片 Prompt，点击魔棒生成背景图片，等待背景图生成成功
        4. 点击立即创作，生成歌词视频
        5. 在当前页面视频播放器区域校验视频生成成功
        """
        logger.info("开始测试：导入本地音乐加提示词生成背景图片歌词视频")
        page_obj = LyricsVideoPage(logged_in_page)
        page_obj.switch_to_lyrics_video()

        # 1. 导入音频文件 (直接导入 settings 中定义的文件路径)
        page_obj.upload_local_audio(TEST_AUDIO_PATH_3)

        # 2. 填写 Prompt 并点击魔棒生成图片 (使用 settings 中的配置值)
        page_obj.generate_background_image(TEST_IMAGE_PROMPT)

        # 3. 提交生成并处理积分扣减确认
        page_obj.click_create()

        # 4. 轮询等待视频生成成功
        success = page_obj.wait_for_generation_success(timeout=360000)
        assert success, "测试用例2：歌词视频生成超时或失败"
        logger.success("测试用例2：本地音乐配合Prompt生成背景图视频成功！")

    def test_lyrics_video_library_audio_and_image(self, logged_in_page):
        """
        [用例 3]：从库选择音乐，导入女巫图片进行处理
        1. 切换到歌词视频生成页面
        2. 从我的音乐库中导入第一首音频
        3. 上传本地背景图 女巫.jpg
        4. 点击立即创作，生成歌词视频
        5. 在当前页面视频播放器区域校验视频生成成功
        """
        logger.info("开始测试：从库选择音乐加图片处理歌词视频")
        page_obj = LyricsVideoPage(logged_in_page)
        page_obj.switch_to_lyrics_video()

        # 1. 从库导入音乐
        page_obj.select_audio_from_library()

        # 2. 导入本地背景图 (直接导入 settings 中定义的文件路径)
        page_obj.upload_background_image(TEST_IMAGE_PATH)

        # 3. 提交生成并处理积分扣减确认
        page_obj.click_create()

        # 4. 轮询等待视频生成成功
        success = page_obj.wait_for_generation_success(timeout=360000)
        assert success, "测试用例3：库音乐配合本地图片生成视频成功！"
        logger.success("测试用例3：库音乐配合本地图片生成视频成功！")




