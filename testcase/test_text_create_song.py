import pytest
from pages.text_page import TextPage
from logger import logger
from utils import get_song

class TestTextCreateSong:
    """文本模式生成歌曲功能测试用例"""

    def test_text_mode_generation_original(self, logged_in_page, lang_urls):
        """
        测试文本模式下，使用原始数据生成歌曲的流程。
        1. 输入文本
        2. 点击创建
        3. 在AI分析弹窗选择'Original Version'
        4. 在确认弹窗点击'Continue'
        5. 等待音乐库显示生成成功
        """
        page = logged_in_page
        text_page = TextPage(page)
        
        # 针对当前语言，确保在正确的 URL
        logger.info(f"导航至生成页面: {lang_urls['base_url']}")
        page.goto(lang_urls["base_url"])
        
        # 1. 输入文本
        test_text = "A futuristic city at night, synthwave style, bright neon lights, high energy."
        text_page.text_input(test_text)
        
        # 1.5 输入唯一歌名
        song_title = get_song()
        text_page.song_title_input(song_title)
        
        # 2. 点击创建
        text_page.click_create()

        # 3. 等待ai分析成功
        text_page.text_ai_analysis_popup()
        
        # 4. 处理 AI 分析弹窗 (选择原始版本)
        text_page.text_select_original()
        
        # 5. 确认生成
        text_page.confirm_generation()
        
        # 6. 验证生成成功 (根据歌名追踪)
        success = text_page.wait_for_generation_success(title=song_title, timeout=300000) 
        
        assert success, f"歌曲 '{song_title}' 生成失败或超时"
        logger.success("文本模式生成歌曲测试用例执行完成并通过。")

    def test_text_mode_generation_ai(self, logged_in_page, lang_urls):
        """
        测试文本模式下，使用AI生成歌曲的流程。
        1. 输入文本
        2. 点击创建
        3. 在AI分析弹窗选择'Create Now'
        4. 在确认弹窗点击'Continue'
        5. 等待音乐库显示生成成功
        """
        page = logged_in_page
        text_page = TextPage(page)
        
        # 针对当前语言，确保在正确的 URL
        logger.info(f"导航至生成页面: {lang_urls['base_url']}")
        page.goto(lang_urls["base_url"])
        
        # 1. 输入文本
        test_text = "A futuristic city at night, synthwave style, bright neon lights, high energy."
        text_page.text_input(test_text)
        
        # 1.5 输入唯一歌名
        song_title = get_song()
        text_page.song_title_input(song_title)
        
        # 2. 点击创建
        text_page.click_create()
        
        # 3. 等待ai分析成功
        text_page.text_ai_analysis_popup()
        
        # 4. 处理 AI 分析弹窗 (选择AI生成)
        text_page.text_select_create_now()
        
        # 5. 确认生成
        text_page.confirm_generation()
        
        # 6. 验证生成成功 (根据歌名追踪)
        success = text_page.wait_for_generation_success(title=song_title, timeout=300000)
        
        assert success, f"歌曲 '{song_title}' 生成失败或超时"
        logger.success("文本模式生成歌曲测试用例执行完成并通过。")


    def test_text_mode_generation_view_lyrics(self, logged_in_page, lang_urls):
        """
        测试文本模式下，使用AI生成歌曲的流程。
        1. 输入文本
        2. 点击创建
        3. 在AI分析弹窗选择'Create Now'
        4. 在确认弹窗点击'Continue'
        5. 等待音乐库显示生成成功
        """
        page = logged_in_page
        text_page = TextPage(page)
        
        # 针对当前语言，确保在正确的 URL
        logger.info(f"导航至生成页面: {lang_urls['base_url']}")
        page.goto(lang_urls["base_url"])
        
        # 1. 输入文本
        test_text = "A futuristic city at night, synthwave style, bright neon lights, high energy."
        text_page.text_input(test_text)
        
        # 1.5 输入唯一歌名
        song_title = get_song()
        text_page.song_title_input(song_title)
        
        # 2. 点击创建
        text_page.click_create()

        # 3. 等待ai分析成功
        text_page.text_ai_analysis_popup()
        
        # 4. 处理 AI 分析弹窗 (选择查看歌词)
        text_page.text_select_view_lyrics()

        # 5. 点击生成歌词
        text_page.text_select_view_lyrics_generate()
        
        # 6. 验证生成成功 (根据歌名追踪)
        success = text_page.wait_for_generation_success(title=song_title, timeout=300000)
        
        assert success, f"歌曲 '{song_title}' 生成失败或超时"
        logger.success("文本模式生成歌曲测试用例执行完成并通过。")