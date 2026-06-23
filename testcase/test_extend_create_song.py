import pytest
import os
from pages.extend_page import ExtendPage
from utils import logger, get_song
from data.test_data import TEST_TEXT_PROMPT, STANDARD_LYRICS
from utils.ai_helper import emulate_3g_network, disable_network_emulation

from config.settings import TEST_AUDIO_PATH

class TestExtendCreateSong:
    """Music Extension (音乐扩展) 模式生成歌曲的功能测试集"""

    def test_extend_mode_local_file(self, logged_in_page):
        """
        [用例 1]：导入本地文件扩展测试
        1. 导航切换到音乐扩展 Tab
        2. 导入本地音频文件并验证导入成功
        3. 修改扩展开始时刻为 00:50
        4. 输入扩展歌词、扩展风格与歌曲名称
        5. 点击 Create 开始创作，并验证列表生成结果
        """
        logger.info("开始测试本地音频文件扩展功能")
        exp = ExtendPage(logged_in_page)
        new_song_name = get_song(prefix="EXT-LOCAL", model="")

        # 1. 切换 Tab
        exp.switch_to_extend_tab()

        # 2. 导入本地文件并校验成功
        exp.upload_local_file(TEST_AUDIO_PATH)

        # 3. 更改时间输入框为 00:50
        exp.set_extend_time("00", "50")

        # 4. 输入歌词、风格与新歌名
        exp.input_lyrics(STANDARD_LYRICS)
        exp.input_music_style(TEST_TEXT_PROMPT)
        exp.set_song_name(new_song_name)

        # 5. 点击创建并等待生成成功
        exp.click_create()
        success = exp.wait_for_generation_success(title=new_song_name, timeout=360000)
        assert success, f"音乐扩展任务 '{new_song_name}' 生成超时或失败"
        logger.success("本地音频文件扩展测试成功！")

    def test_extend_mode_library_file(self, logged_in_page):
        """
        [用例 2]：导入 Library 库文件扩展测试
        1. 导航切换到音乐扩展 Tab
        2. 从 Library 弹窗中选择第一首音乐导入并验证成功
        3. 修改扩展开始时刻为 00:50
        4. 输入扩展歌词、扩展风格与歌曲名称
        5. 点击 Create 开始创作，并验证列表生成结果
        """
        logger.info("【开始测试从 Library 导入音频进行扩展")
        exp = ExtendPage(logged_in_page)
        new_song_name = get_song(prefix="EXT-LIB", model="")

        # 1. 切换 Tab
        exp.switch_to_extend_tab()

        # 2. 从 Library 选择导入并校验成功
        exp.select_from_library()

        # 3. 更改时间输入框为 00:50
        exp.set_extend_time("00", "50")

        # 4. 输入歌词、风格与新歌名
        exp.input_lyrics(STANDARD_LYRICS)
        exp.input_music_style(TEST_TEXT_PROMPT)
        exp.set_song_name(new_song_name)

        # 5. 点击创建并等待生成成功
        exp.click_create()
        success = exp.wait_for_generation_success(title=new_song_name, timeout=360000)
        assert success, f"从 Library 音乐扩展的任务 '{new_song_name}' 生成超时或失败"
        logger.success("从 Library 导入音频扩展测试成功！")

    def test_extend_mode_instrumental(self, logged_in_page):
        """
        [用例 3]：导入本地文件并开启纯音乐模式扩展测试
        1. 导航切换到音乐扩展 Tab
        2. 导入本地音频文件并验证导入成功
        3. 开启 Instrumental 纯音乐开关
        4. 输入扩展风格与歌曲名称（纯音乐模式下无需输入歌词）
        5. 点击 Create 开始创作，并验证列表生成结果
        """
        logger.info("开始测试本地音频纯音乐扩展功能")
        exp = ExtendPage(logged_in_page)
        new_song_name = get_song(prefix="EXT-INST", model="")

        # 1. 切换 Tab
        exp.switch_to_extend_tab()

        # 2. 导入本地文件并校验成功
        exp.upload_local_file(TEST_AUDIO_PATH)

        # 3. 开启纯音乐开关
        exp.toggle_instrumental(True)

        # 4. 输入风格与新歌名
        exp.input_music_style(TEST_TEXT_PROMPT)
        exp.set_song_name(new_song_name)

        # 5. 点击创建并等待生成成功
        exp.click_create()
        success = exp.wait_for_generation_success(title=new_song_name, timeout=360000)
        assert success, f"纯音乐扩展任务 '{new_song_name}' 生成超时或失败"
        logger.success("本地音频纯音乐扩展测试成功！")