import pytest
from pages.music_video_page import MusicVideoPage
from utils import logger
from config.settings import TEST_AUDIO_PATH_3, TEST_IMAGE_PATH, TEST_IMAGE_PROMPT

class TestMusicVideo:
    """AI音乐视频功能测试集"""

    def test_music_video_local_audio_and_image(self, logged_in_page):
        """
        [用例 1]：导入本地文件2s音频、图片、prompt、进行生成
        1. 切换到音乐视频生成页面
        2. 上传本地 2s 音频 (TEST_AUDIO_PATH_3)
        3. 上传本地背景图 (TEST_IMAGE_PATH)
        4. 输入视频风格 Prompt (TEST_IMAGE_PROMPT)
        5. 点击立即创作，生成音乐视频
        6. 在当前页面视频播放器区域校验视频生成成功
        """
        logger.info("开始测试：导入本地2s音频、图片和提示词生成音乐视频")
        page_obj = MusicVideoPage(logged_in_page)
        page_obj.switch_to_music_video()

        # 1. 导入本地 2s 音频、图片、并输入 Prompt
        page_obj.upload_local_audio(TEST_AUDIO_PATH_3)
        page_obj.upload_background_image(TEST_IMAGE_PATH)
        page_obj.input_prompt(TEST_IMAGE_PROMPT)

        # 2. 提交生成并处理积分扣减确认
        page_obj.click_create()

        # 3. 轮询等待视频生成成功
        success = page_obj.wait_for_generation_success(timeout=360000)
        assert success, "测试用例1：音乐视频生成超时或失败"
        logger.success("测试用例1：导入本地2s音频、图片和提示词生成音乐视频成功！")

    def test_music_video_library_audio_and_image(self, logged_in_page):
        """
        [用例 2]：从库选择音频，剪辑窗口选择10s、导入图片、prompt，进行生成
        1. 切换到音乐视频生成页面
        2. 从我的音乐库中导入第一首音频，并在剪辑时长窗口中选择 10s 并确认
        3. 上传本地背景图 (TEST_IMAGE_PATH)
        4. 输入视频风格 Prompt (TEST_IMAGE_PROMPT)
        5. 点击立即创作，生成音乐视频
        6. 在当前页面视频播放器区域校验视频生成成功
        """
        logger.info("开始测试：库音频选择10s、导入图片和提示词生成音乐视频")
        page_obj = MusicVideoPage(logged_in_page)
        page_obj.switch_to_music_video()

        # 1. 从库导入音乐并剪裁 10s，导入背景图，并输入 Prompt
        page_obj.select_audio_from_library()
        page_obj.upload_background_image(TEST_IMAGE_PATH)
        page_obj.input_prompt(TEST_IMAGE_PROMPT)

        # 2. 提交生成并处理积分扣减确认
        page_obj.click_create()

        # 3. 轮询等待视频生成成功
        success = page_obj.wait_for_generation_success(timeout=360000)
        assert success, "测试用例2：库音乐剪辑10s生成视频超时或失败"
        logger.success("测试用例2：库音乐剪辑10s、配合图片和提示词生成音乐视频成功！")
