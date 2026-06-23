import pytest
from pages.remix_page import RemixPage
from utils import logger, get_song
from data.test_data import TEST_TEXT_PROMPT, STANDARD_LYRICS
from config.settings import TEST_AUDIO_PATH

class TestRemixCreateSong:
    """Remix (音乐混音) 模式生成歌曲的功能测试集"""

    def test_remix_mode_local_file_with_lyrics(self, logged_in_page):
        """
        [用例 1]：本地上传音乐生成（勾选歌词，输入歌词，输入style，songname）
        1. 导航切换到音乐混音 Tab
        2. 导入本地音频文件并验证导入成功
        3. 开启 Custom Lyrics 歌词开关并输入歌词
        4. 输入混音风格描述与歌曲名称
        5. 点击 Create 开始创作，并验证列表生成结果
        """
        logger.info("开始测试本地音频混音（歌词模式）")
        remix = RemixPage(logged_in_page)
        new_song_name = get_song(prefix="RMX-LOC-LYR", model="")

        # 1. 切换 Tab
        remix.switch_to_remix_tab()

        # 2. 导入本地文件并校验成功
        remix.upload_local_file(TEST_AUDIO_PATH)

        # 3. 开启 Custom Lyrics 并输入歌词
        remix.input_lyrics(STANDARD_LYRICS)

        # 4. 输入风格与新歌名
        remix.input_music_style(TEST_TEXT_PROMPT)
        remix.set_song_name(new_song_name)

        # 5. 点击创建并等待生成成功
        remix.click_create()
        success = remix.wait_for_generation_success(title=new_song_name, timeout=600000)
        assert success, f"音乐混音任务 '{new_song_name}' 生成超时或失败"
        logger.success("本地音频混音（歌词模式）测试成功！")

    def test_remix_mode_local_file_instrumental(self, logged_in_page):
        """
        [用例 2]：本地上传音乐生成（勾选instrumental，style，songname）
        1. 导航切换到音乐混音 Tab
        2. 导入本地音频文件并验证导入成功
        3. 开启 Instrumental 纯音乐开关
        4. 输入混音风格描述与歌曲名称
        5. 点击 Create 开始创作，并验证列表生成结果
        """
        logger.info("开始测试本地音频混音（纯音乐模式）")
        remix = RemixPage(logged_in_page)
        new_song_name = get_song(prefix="RMX-LOC-INST", model="")

        # 1. 切换 Tab
        remix.switch_to_remix_tab()

        # 2. 导入本地文件并校验成功
        remix.upload_local_file(TEST_AUDIO_PATH)

        # 3. 开启 Instrumental 纯音乐开关
        remix.toggle_instrumental(True)

        # 4. 输入风格与新歌名
        remix.input_music_style(TEST_TEXT_PROMPT)
        remix.set_song_name(new_song_name)

        # 5. 点击创建并等待生成成功
        remix.click_create()
        success = remix.wait_for_generation_success(title=new_song_name, timeout=600000)
        assert success, f"纯音乐混音任务 '{new_song_name}' 生成超时或失败"
        logger.success("本地音频混音（纯音乐模式）测试成功！")

    def test_remix_mode_library_file_with_lyrics(self, logged_in_page):
        """
        [用例 3]：从library选择音乐进行生成（勾选歌词，输入歌词，输入style，songname）
        1. 导航切换到音乐混音 Tab
        2. 从 Library 弹窗中选择第一首音乐导入并验证成功
        3. 开启 Custom Lyrics 歌词开关并输入歌词
        4. 输入混音风格描述与歌曲名称
        5. 点击 Create 开始创作，并验证列表生成结果
        """
        logger.info("开始测试从 Library 导入音频进行混音（歌词模式）")
        remix = RemixPage(logged_in_page)
        new_song_name = get_song(prefix="RMX-LIB-LYR", model="")

        # 1. 切换 Tab
        remix.switch_to_remix_tab()

        # 2. 从 Library 选择导入并校验成功
        remix.select_from_library()

        # 3. 开启 Custom Lyrics 并输入歌词
        remix.input_lyrics(STANDARD_LYRICS)

        # 4. 输入风格与新歌名
        remix.input_music_style(TEST_TEXT_PROMPT)
        remix.set_song_name(new_song_name)

        # 5. 点击创建并等待生成成功
        remix.click_create()
        success = remix.wait_for_generation_success(title=new_song_name, timeout=600000)
        assert success, f"从 Library 导入音频的混音任务 '{new_song_name}' 生成超时或失败"
        logger.success("从 Library 导入音频混音（歌词模式）测试成功！")

    def test_remix_mode_v5_5_with_lyrics(self, logged_in_page):
        """
        [用例 4]：本地上传音乐生成（选择V5.5,勾选歌词，输入歌词，输入style，songname）
        1. 导航切换到音乐混音 Tab
        2. 导入本地音频文件并验证导入成功
        3. 选择 V5.5 模型版本
        4. 开启 Custom Lyrics 歌词开关并输入歌词
        5. 输入混音风格描述与歌曲名称
        6. 点击 Create 开始创作，并验证列表生成结果
        """
        logger.info("开始测试选择 V5.5 模型混音（歌词模式）")
        remix = RemixPage(logged_in_page)
        new_song_name = get_song(prefix="RMX-V55-LYR", model="")

        # 1. 切换 Tab
        remix.switch_to_remix_tab()

        # 2. 导入本地文件并校验成功
        remix.upload_local_file(TEST_AUDIO_PATH)

        # 3. 选择模型版本为 V5.5
        remix.select_model_version("V5.5")

        # 4. 开启 Custom Lyrics 并输入歌词
        remix.input_lyrics(STANDARD_LYRICS)

        # 5. 输入风格与新歌名
        remix.input_music_style(TEST_TEXT_PROMPT)
        remix.set_song_name(new_song_name)

        # 6. 点击创建并等待生成成功
        remix.click_create()
        success = remix.wait_for_generation_success(title=new_song_name, timeout=600000)
        assert success, f"选择 V5.5 模型的混音任务 '{new_song_name}' 生成超时或失败"
        logger.success("选择 V5.5 模型混音（歌词模式）测试成功！")
