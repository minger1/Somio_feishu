from playwright.sync_api import expect
from config.locators import Locators
from utils import logger
import time

class RemixPage:
    """封装 Remix (音乐混音) 模式相关的页面操作"""

    def __init__(self, page):
        self.page = page

    def switch_to_remix_tab(self):
        """直接导航或切换到音乐混音分页"""
        base_url = self.page.url.split("/generate")[0]
        target_url = f"{base_url}/generate/?target=CREATE_REMIX"
        logger.info(f"导航至音乐混音分页: {target_url}")
        self.page.goto(target_url)
        self.page.locator(Locators.MUSIC_REMIX_UPLOAD_FILE).wait_for(state="visible", timeout=15000)
        logger.info("成功切换至 Remix 音乐混音页面")

    def upload_local_file(self, file_path: str):
        """导入本地音频文件进行混音"""
        logger.info(f"开始导入本地音频文件: {file_path}")
        self.page.locator(Locators.MUSIC_REMIX_INPUT_FILE).set_input_files(file_path)
        # 等待文件操作状态区域渲染显示
        self.page.locator(Locators.MUSIC_REMIX_UPLOADED_STATUS_WRAPPER).wait_for(state="visible", timeout=20000)
        # 等待音频解析加载完成
        logger.info("等待音频解析加载完成...")
        self.page.locator(".loading-overlay").wait_for(state="hidden", timeout=30000)
        logger.success("本地音频文件导入成功！")

    def select_from_library(self):
        """从已有的 Library 列表中选择音乐进行混音"""
        logger.info("点击 'From Library' 选择库中文件...")
        self.page.locator(Locators.MUSIC_REMIX_UPLOAD_LIBRARY).click()
        
        # 等待选择音乐库弹窗可见
        logger.info("等待 Select My Music 弹窗显示...")
        self.page.locator(Locators.MUSIC_REMIX_LIBRARY_DIALOG).wait_for(state="visible", timeout=15000)
        
        # 点击库中第一首歌曲的 Select 按钮
        logger.info("选择音乐库第一首歌曲项目...")
        self.page.locator(Locators.MUSIC_REMIX_LIBRARY_SELECT_BTN).first.click()
        
        # 等待文件操作状态区域渲染显示
        self.page.locator(Locators.MUSIC_REMIX_UPLOADED_STATUS_WRAPPER).wait_for(state="visible", timeout=20000)
        # 等待音频解析加载完成
        logger.info("等待音频解析加载完成...")
        self.page.locator(".loading-overlay").wait_for(state="hidden", timeout=30000)
        logger.success("已成功从 Library 载入目标音频！")

    def select_model_version(self, version: str):
        """选择模型版本 (V5.5, V5, V4.5+, V4.5)"""
        logger.info(f"正在选择模型版本: {version}")
        # 点击下拉菜单触发器
        self.page.locator(Locators.MUSIC_REMIX_MODEL_VERSION).click()
        self.page.wait_for_timeout(500)
        
        ver_lower = version.lower()
        if "5.5" in ver_lower:
            opt_locator = Locators.MUSIC_REMIX_MODEL_VERSION_V5_5
        elif "4.5+" in ver_lower:
            opt_locator = Locators.MUSIC_REMIX_MODEL_VERSION_V4_5_PLUS
        elif "4.5" in ver_lower:
            opt_locator = Locators.MUSIC_REMIX_MODEL_VERSION_V4_5
        else:
            opt_locator = Locators.MUSIC_REMIX_MODEL_VERSION_V5
            
        self.page.locator(opt_locator).click()
        self.page.wait_for_timeout(500)
        logger.success(f"已选择模型版本: {version}")

    def toggle_lyrics(self, enable: bool = True):
        """设置 Custom Lyrics 歌词开关状态"""
        logger.info(f"设置 Custom Lyrics 模式为: {enable}")
        switch = self.page.locator(Locators.MUSIC_REMIX_LYRIC_SWITCH)
        
        # 获取开关的状态。这里如果包含 'active' class 则视为启用
        is_active = "active" in (switch.get_attribute("class") or "")
        if enable != is_active:
            switch.click()
            self.page.wait_for_timeout(500)
        logger.success("Custom Lyrics 开关状态匹配完成")

    def toggle_instrumental(self, enable: bool = True):
        """设置 Instrumental 纯音乐开关状态"""
        logger.info(f"设置 Instrumental 模式为: {enable}")
        switch = self.page.locator(Locators.MUSIC_REMIX_INSTRUMENTAL_SWITCH)
        
        is_active = "active" in (switch.get_attribute("class") or "")
        if enable != is_active:
            switch.click()
            self.page.wait_for_timeout(500)
        logger.success("Instrumental 开关状态匹配完成")

    def input_lyrics(self, lyrics: str):
        """输入混音歌词"""
        self.toggle_lyrics(True)
        logger.info("输入混音歌词内容")
        textarea = self.page.locator(Locators.MUSIC_REMIX_LYRICS_TEXTAREA)
        textarea.fill(lyrics)
        expect(textarea).to_have_value(lyrics, timeout=5000)

    def input_music_style(self, style: str):
        """输入混音音乐的风格/主题描述"""
        logger.info(f"输入混音风格描述: {style}")
        textarea = self.page.locator(Locators.MUSIC_REMIX_STYLE_TEXTAREA)
        textarea.fill(style)
        expect(textarea).to_have_value(style, timeout=5000)

    def expand_advanced_options(self):
        """如果高级选项折叠则展开之"""
        input_el = self.page.locator(Locators.MUSIC_REMIX_SONG_NAME_INPUT)
        if not input_el.is_visible():
            logger.info("点击展开 Advanced Options 高级选项...")
            # Remix 页面高级选项容器头部通常包含 'Advanced' 文本
            self.page.locator("//div[contains(text(), 'Advanced Options')]").click()
            self.page.wait_for_timeout(500)

    def set_song_name(self, name: str):
        """设置混音后新歌曲的名称"""
        self.expand_advanced_options()
        logger.info(f"设置混音新歌曲名称: {name}")
        self.page.locator(Locators.MUSIC_REMIX_SONG_NAME_INPUT).fill(name)

    def select_vocal_gender(self, gender: str):
        """选择混音人声音色性别 (Male, Female, Random)"""
        self.expand_advanced_options()
        logger.info(f"选择人声音色性别: {gender}")
        
        g_lower = gender.lower()
        if g_lower == "male":
            opt_locator = Locators.MUSIC_REMIX_MALE_VOICE
        elif g_lower == "female":
            opt_locator = Locators.MUSIC_REMIX_FEMALE_VOICE
        else:
            opt_locator = Locators.MUSIC_REMIX_RAMDON_VOICE
            
        self.page.locator(opt_locator).click()
        self.page.wait_for_timeout(300)

    def click_create(self):
        """点击立即创作按钮提交生成"""
        logger.info("点击 Create 按钮开始生成混音歌曲...")
        self.page.locator(Locators.MUSIC_REMIX_CREATE_BTN).click()

    def wait_for_generation_success(self, title: str = None, timeout: int = 600000):
        """在页面右侧历史列表中等待本条混音歌曲生成成功"""
        from pages.library_page import LibraryPage
        lib_page = LibraryPage(self.page)
        return lib_page.wait_for_generation_success(title=title, timeout=timeout)
