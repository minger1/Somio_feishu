from playwright.sync_api import expect
from config.locators import Locators
from utils import logger
import time

class ExtendPage:
    """封装 Music Extension (音乐扩展) 模式相关的页面操作"""

    def __init__(self, page):
        self.page = page

    def switch_to_extend_tab(self):
        """直接导航或切换到音乐扩展分页"""
        base_url = self.page.url.split("/generate")[0]
        target_url = f"{base_url}/generate/?target=CREATE_EXTEND"
        logger.info(f"导航至音乐扩展分页: {target_url}")
        self.page.goto(target_url)
        self.page.locator(Locators.MUSIC_EXTENSION_UPLOAD_FILE).wait_for(state="visible", timeout=15000)
        logger.info("成功切换至 Music Extension 音乐扩展页面")

    def upload_local_file(self, file_path: str):
        """导入本地音频文件进行扩展"""
        logger.info(f"开始导入本地音频文件: {file_path}")
        self.page.locator(Locators.MUSIC_EXTENSION_INPUT_FILE).set_input_files(file_path)
        # 等待文件操作状态区域渲染显示
        self.page.locator(Locators.MUSIC_EXTENSION_UPLOADED_STATUS_WRAPPER).wait_for(state="visible", timeout=20000)
        # 等待音频解析加载完成
        logger.info("等待音频解析加载完成...")
        self.page.locator(".loading-overlay").first.wait_for(state="hidden", timeout=30000)
        logger.success("本地音频文件导入成功！")

    def select_from_library(self):
        """从已有的 Library 列表中选择音乐进行扩展"""
        logger.info("点击 'From Library' 选择库中文件...")
        self.page.locator(Locators.MUSIC_EXTENSION_UPLOAD_LIBRARY).click()
        
        # 等待选择音乐库弹窗可见
        logger.info("等待 Select My Music 弹窗显示...")
        self.page.locator(Locators.MUSIC_EXTENSION_LIB_DIALOG).wait_for(state="visible", timeout=15000)
        
        # 点击库中第一首歌曲的 Select 按钮
        logger.info("选择音乐库第一首歌曲项目...")
        self.page.locator(Locators.MUSIC_EXTENSION_LIB_SELECT_BTN).first.click()
        
        # 等待文件操作状态区域渲染显示
        self.page.locator(Locators.MUSIC_EXTENSION_UPLOADED_STATUS_WRAPPER).wait_for(state="visible", timeout=20000)
        # 等待音频解析加载完成
        logger.info("等待音频解析加载完成...")
        self.page.locator(".loading-overlay").first.wait_for(state="hidden", timeout=30000)
        logger.success("已成功从 Library 载入目标音频！")

    def set_extend_time(self, minutes: str, seconds: str):
        """设置开始扩展时间 (Extend From)"""
        logger.info(f"修改 Extend From 扩展时刻为: {minutes}:{seconds}")
        
        # 1. 填充分钟数
        min_input = self.page.locator(Locators.MUSIC_EXTENSION_FROM_MINUTES)
        min_input.click()
        min_input.press("Control+A")
        min_input.press("Backspace")
        min_input.type(minutes)
        self.page.wait_for_timeout(200)
        
        # 2. 填充秒数
        sec_input = self.page.locator(Locators.MUSIC_EXTENSION_FROM_SECONDS)
        sec_input.click()
        sec_input.press("Control+A")
        sec_input.press("Backspace")
        sec_input.type(seconds)
        self.page.wait_for_timeout(200)
        
        # 3. 强制在外部元素点击以触发 blur 事件更新 React/Vue 绑定的状态
        self.page.locator(".extend-from").click(position={"x": 5, "y": 5})
        self.page.wait_for_timeout(500)
        
        # 校验页面上的值是否正确
        expect(min_input).to_have_value(minutes, timeout=5000)
        expect(sec_input).to_have_value(seconds, timeout=5000)
        
        logger.success("扩展时刻设定完成")

    def input_lyrics(self, lyrics: str):
        """输入扩展部分歌词"""
        logger.info("输入扩展歌词内容")
        textarea = self.page.locator(Locators.MUSIC_EXTENSION_LYRICS_TEXTAREA)
        textarea.fill(lyrics)
        expect(textarea).to_have_value(lyrics, timeout=5000)

    def input_music_style(self, style: str):
        """输入扩展音乐的风格/主题描述"""
        logger.info(f"输入扩展音乐风格: {style}")
        textarea = self.page.locator(Locators.MUSIC_EXTENSION_STYLE_TEXTAREA)
        textarea.fill(style)
        expect(textarea).to_have_value(style, timeout=5000)

    def expand_advanced_options(self):
        """如果高级选项折叠则展开之"""
        input_el = self.page.locator(Locators.MUSIC_EXTENSION_SONG_NAME_INPUT)
        if not input_el.is_visible():
            logger.info("点击展开 Advanced Options 高级选项...")
            self.page.locator(".advanced-header").click()
            self.page.wait_for_timeout(500)

    def set_song_name(self, name: str):
        """设置扩展后新歌曲的名称"""
        self.expand_advanced_options()
        logger.info(f"设置扩展新歌曲名称: {name}")
        self.page.locator(Locators.MUSIC_EXTENSION_SONG_NAME_INPUT).fill(name)

    def toggle_instrumental(self, enable: bool = True):
        """设置纯音乐开关状态"""
        self.expand_advanced_options()
        logger.info(f"设置纯音乐模式为: {enable}")
        switch = self.page.locator(Locators.MUSIC_EXTENSION_INSTRUMENT_SWITCH)
        is_active = self.page.locator(Locators.MUSIC_EXTENSION_INSTRUMENT_SWITCH_ACTIVE).count() > 0
        
        if enable != is_active:
            switch.click()
            self.page.wait_for_timeout(500)
        logger.success("纯音乐开关状态匹配完成")

    def click_create(self):
        """点击立即创作按钮提交生成"""
        logger.info("点击 Create 按钮开始生成扩展歌曲...")
        self.page.locator(Locators.MUSIC_EXTENSION_CREATE_BTN).click()

    def wait_for_generation_success(self, title: str = None, timeout: int = 600000):
        """在页面右侧历史列表中等待本条扩展歌曲生成成功"""
        from pages.library_page import LibraryPage
        lib_page = LibraryPage(self.page)
        return lib_page.wait_for_generation_success(title=title, timeout=timeout)
