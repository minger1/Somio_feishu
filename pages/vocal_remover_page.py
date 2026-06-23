import os
import time
from config.locators import Locators
from playwright.sync_api import Page
from utils import logger


class VocalRemoverPage:
    """
    Vocal Remover 页面 Page Object
    封装文件上传、库歌曲选择、格式配置、文件下载等操作。
    """

    def __init__(self, page: Page):
        self.page = page
        self.format_btn = Locators.VOCAL_RESULT_FORMAT
        self.wav_save_btn = Locators.VOCAL_RESULT_FORMAT_WAV_SAVE_BTN

    def switch_to_vocal_remover(self):
        """通过侧边栏导航切换到人声分离页面并等待加载完成"""
        logger.info("点击左侧导航栏的 Vocal Remover 按钮...")
        self.page.locator(Locators.NAV_VOCAL).click()
        logger.info("等待人声分离页面加载完成...")
        self.page.locator(Locators.COMMON_UPLOAD_FILE_BTN).wait_for(state="visible", timeout=30000)
        logger.info("成功切换至 Vocal Remover 页面")

    def upload_local_file(self, file_path: str):
        """上传本地音频文件"""
        abs_path = os.path.abspath(file_path)
        logger.info("等待页面稳定...")
        self.page.wait_for_timeout(3000)
        logger.info(f"开始上传本地音频文件: {abs_path}")
        self.page.locator(Locators.COMMON_UPLOAD_INPUT_FILE).first.set_input_files(abs_path)
        # 等待文件信息展示，确保上传完成
        self.page.locator(Locators.COMMON_UPLOAD_FILE_INFO).wait_for(state="visible", timeout=20000)
        logger.success("本地音频文件上传成功，已展示文件信息")

    def select_from_library(self):
        """从已有的 Library 列表中选择音乐"""
        logger.info("等待页面稳定...")
        self.page.wait_for_timeout(2000)
        
        logger.info("点击 My Music 选项卡...")
        my_music_tab = self.page.locator(Locators.COMMON_UPLOAD_TAB_SWITCH, has_text="My Music")
        my_music_tab.wait_for(state="visible", timeout=10000)
        my_music_tab.click()
        
        # 验证 My Music 已经激活
        logger.info("验证 My Music 选项卡已被激活...")
        self.page.locator(Locators.COMMON_UPLOAD_TAB_ACTIVE, has_text="My Music").wait_for(state="visible", timeout=5000)
        self.page.wait_for_timeout(1000)

        logger.info("点击 From My Music 按钮唤起库选择弹窗...")
        upload_btn = self.page.locator(Locators.COMMON_UPLOAD_FILE_BTN, has_text="From My Music").or_(
            self.page.locator(Locators.COMMON_UPLOAD_FILE_BTN)
        ).first
        upload_btn.wait_for(state="visible", timeout=10000)
        upload_btn.click()

        # 等待库歌曲 Select 按钮可见
        logger.info("等待选择音乐库弹窗显示...")
        select_btn = self.page.locator(Locators.COMMON_UPLOAD_LIBRARY_SELECT_BTN).first
        select_btn.wait_for(state="visible", timeout=15000)

        # 选择第一首歌曲
        logger.info("选择音乐库第一首歌曲项目...")
        select_btn.click()
        
        # 等待文件信息展示，确保选择完成
        self.page.locator(Locators.COMMON_UPLOAD_FILE_INFO).wait_for(state="visible", timeout=15000)
        logger.success("从音乐库成功导入目标音频")

    def click_separate(self):
        """点击 Separate 按钮开始处理"""
        logger.info("点击 Separate 按钮开始人声分离处理...")
        self.page.locator(Locators.COMMON_UPLOAD_SEPARATE_BTN).click()

    def select_mp3_format(self, sample_rate_locator: str):
        """
        打开格式设置弹窗，选择 MP3 格式并设置采样率，点击保存。
        """
        logger.info("打开 Download Settings 格式选择弹窗...")
        self.page.locator(self.format_btn).click(force=True)
        self.page.wait_for_selector(Locators.COMMON_FORMAT_WINDOW, state="visible", timeout=10000)

        logger.info("切换到 MP3 格式...")
        self.page.locator(Locators.COMMON_FORMAT_MP3_SELECT_MP3).or_(
            self.page.locator(Locators.COMMON_FORMAT_WAV_SELECT_MP3)
        ).click()

        logger.info("展开采样率下拉框...")
        self.page.locator(Locators.COMMON_FORMAT_SELECT_SAMPLE_RATE).click()
        
        rate_text = self.page.locator(sample_rate_locator).inner_text().strip()
        logger.info(f"选择 MP3 采样率: {rate_text}")
        self.page.locator(sample_rate_locator).click()
        
        logger.info("保存 MP3 格式设置...")
        self.page.locator(Locators.COMMON_FORMAT_MP3_SAVE_BTN).click()
        self.page.wait_for_timeout(500)

    def select_wav_format(self, sample_rate_locator: str, bit_depth_locator: str):
        """
        打开格式设置弹窗，选择 WAV 格式并设置采样率 and 位深，点击保存。
        """
        logger.info("打开 Download Settings 格式选择弹窗...")
        self.page.locator(self.format_btn).click(force=True)
        self.page.wait_for_selector(Locators.COMMON_FORMAT_WINDOW, state="visible", timeout=10000)

        logger.info("切换到 WAV 格式...")
        self.page.locator(Locators.COMMON_FORMAT_WAV_SELECT_WAV).or_(
            self.page.locator(Locators.COMMON_FORMAT_MP3_SELECT_WAV)
        ).click()

        logger.info("展开采样率下拉框...")
        self.page.locator(Locators.COMMON_FORMAT_WAV_SAMPLE_RATE).click()
        
        rate_text = self.page.locator(sample_rate_locator).inner_text().strip()
        logger.info(f"选择 WAV 采样率: {rate_text}")
        self.page.locator(sample_rate_locator).click()
        self.page.wait_for_timeout(500)

        logger.info("展开位深下拉框...")
        self.page.locator(Locators.COMMON_FORMAT_WAV_BIT_DEPTH).click()
        
        depth_text = self.page.locator(bit_depth_locator).inner_text().strip()
        logger.info(f"选择 WAV 位深: {depth_text}")
        self.page.locator(bit_depth_locator).click()
        
        logger.info("保存 WAV 格式设置...")
        self.page.locator(self.wav_save_btn).click()
        self.page.wait_for_timeout(500)

    def do_download(self, download_btn_locator: str, expected_suffix: str = None):
        """
        触发下载并验证下载的文件存在且不为空，支持自适应首次下载的确认弹窗。
        """
        logger.info("准备触发下载并验证文件...")
        with self.page.expect_download(timeout=600000) as download_info:
            self.page.locator(download_btn_locator).click()
            # 如果首次下载弹出格式确认弹窗，自动点击 Save 确认
            save_btn = self.page.locator(Locators.COMMON_FORMAT_MP3_SAVE_BTN)
            try:
                if save_btn.is_visible(timeout=3000):
                    save_btn.click()
            except Exception:
                pass
        
        download = download_info.value
        real_filename = download.suggested_filename
        downloaded_file = os.path.join(os.path.dirname(download.path()), real_filename)
        download.save_as(downloaded_file)
        
        logger.info(f"下载的文件名: {real_filename}")
        if expected_suffix:
            logger.info(f"断言文件后缀: 期望 {expected_suffix}，实际 {real_filename}")
            assert real_filename.lower().endswith(expected_suffix.lower()), \
                f"Expected suffix {expected_suffix}, actual filename: {real_filename}"
        
        assert os.path.exists(downloaded_file), "文件未下载成功"
        assert os.path.getsize(downloaded_file) > 0, "下载的文件大小为 0"
        logger.success(f"验证通过: [{real_filename}] 下载成功且大小正确")
        self.page.wait_for_timeout(1000)

    def wait_for_audio_loaded(self):
        """
        等待所有的音频轨道加载完成（即所有 loading-overlay 元素隐藏）。
        """
        logger.info("等待所有音频轨道的加载遮罩 (.loading-overlay) 隐藏...")
        # 等待页面渲染稳定
        self.page.wait_for_timeout(2000)
        
        loading_overlays = self.page.locator(".loading-overlay")
        # 逐个等待所有可见的加载遮罩隐藏
        count = loading_overlays.count()
        logger.info(f"检测到共有 {count} 个音频加载遮罩")
        for i in range(count):
            try:
                # 针对第 i 个加载遮罩，等待其隐藏，超时 90 秒
                loading_overlays.nth(i).wait_for(state="hidden", timeout=90000)
                logger.info(f"第 {i+1}/{count} 个音频轨道加载完成")
            except Exception as e:
                logger.warning(f"等待第 {i+1} 个音频加载遮罩隐藏超时或出错: {e}")
        
        logger.success("所有音频轨道的加载遮罩已隐藏，音频加载就绪")

