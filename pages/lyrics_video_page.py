from playwright.sync_api import expect
from config.locators import Locators
from utils import logger
import time
import os

class LyricsVideoPage:
    """封装 AI 歌词视频 (Lyrics Video) 页面相关的操作"""

    def __init__(self, page):
        self.page = page

    def switch_to_lyrics_video(self):
        """通过侧边栏导航切换到歌词视频生成页面并等待加载完成"""
        logger.info("点击左侧导航栏的 AI Lyrics Video 按钮...")
        self.page.locator(Locators.NAV_LYRICS_AI).click()
        
        # 等待页面加载完成 (等待输入框变为可见，以确保页面元素渲染稳定)
        logger.info("等待 AI 歌词视频页面加载完成...")
        self.page.locator(Locators.LYRICS_VIDEO_PROMPT_TEXTAREA).wait_for(state="visible", timeout=30000)
        
        # 关闭页面可能弹出的营销弹窗
        self.close_marketing_popup()
        logger.info("成功切换至 Lyrics Video 歌词视频页面")

    def close_marketing_popup(self):
        """关闭任何阻碍操作的全局营销弹窗/推广弹窗"""
        modal_wraper = self.page.locator(Locators.LYRICS_VIDEO_MARKETING_MODAL)
        if modal_wraper.count() > 0:
            for i in range(modal_wraper.count()):
                m = modal_wraper.nth(i)
                if m.is_visible():
                    logger.info(f"发现营销弹窗: {m.inner_text().strip()[:100]}")
                    close_btn = m.locator(Locators.LYRICS_VIDEO_MARKETING_CLOSE).first
                    if close_btn.count() > 0 and close_btn.is_visible():
                        close_btn.click()
                        logger.info("已关闭营销弹窗")
                        self.page.wait_for_timeout(1000)

    def upload_local_audio(self, file_path: str):
        """导入本地音频文件"""
        # 如果当前有已经导入的音频，先清理/删除
        delete_btn = self.page.locator(Locators.LYRICS_VIDEO_AUDIO_DELETE_BTN).first
        if delete_btn.count() > 0 and delete_btn.is_visible():
            logger.info("检测到已存在音频，点击垃圾桶图标清理以开启本地上传...")
            delete_btn.click()
            self.page.wait_for_timeout(1000)

        abs_path = os.path.abspath(file_path)
        logger.info(f"开始导入本地音频文件: {abs_path}")
        self.page.locator(Locators.LYRICS_VIDEO_INPUT_FILE).set_input_files(abs_path)
        self.page.wait_for_timeout(2000)

    def select_audio_from_library(self):
        """从已有的 Library 列表中选择音乐"""
        # 如果当前有已经导入的音频，先清理/删除
        delete_btn = self.page.locator(Locators.LYRICS_VIDEO_AUDIO_DELETE_BTN).first
        if delete_btn.count() > 0 and delete_btn.is_visible():
            logger.info("检测到已存在音频，点击垃圾桶图标清理以开启音乐库选择...")
            delete_btn.click()
            self.page.wait_for_timeout(1000)

        logger.info("点击 From My Music 从库中选择文件...")
        self.page.locator(Locators.LYRICS_VIDEO_UPLOAD_LIBRARY).click()
        
        # 等待选择音乐库弹窗中的 Select 按钮可见
        logger.info("等待选择音乐库弹窗显示...")
        select_btn = self.page.locator(Locators.LYRICS_VIDEO_LIBRARY_SELECT_BTN).first
        select_btn.wait_for(state="visible", timeout=15000)
        
        # 点击第一个歌曲的 Select 按钮
        logger.info("选择音乐库第一首歌曲项目...")
        select_btn.click()
        self.page.wait_for_timeout(2000)
        logger.success("已成功从 Library 载入目标音频！")

    def upload_background_image(self, file_path: str):
        """导入本地背景图片"""
        abs_path = os.path.abspath(file_path)
        logger.info(f"开始导入本地背景图片: {abs_path}")
        self.page.locator(Locators.LYRICS_VIDEO_INPUT_IMAGE).set_input_files(abs_path)
        self.page.wait_for_timeout(2000)
        logger.success("背景图片导入成功！")

    def generate_background_image(self, prompt: str):
        """输入图片 prompt 生成背景图片"""
        logger.info(f"输入提示词生成背景图片: {prompt}")
        textarea = self.page.locator(Locators.LYRICS_VIDEO_PROMPT_TEXTAREA)
        textarea.fill(prompt)
        self.page.wait_for_timeout(500)
        
        # 等待生成魔棒按钮变为启用状态
        gen_btn = self.page.locator(Locators.LYRICS_VIDEO_PROMPT_GEN_BTN)
        expect(gen_btn).to_be_enabled(timeout=5000)
        
        # 点击生成按钮
        logger.info("点击魔棒按钮开始生成背景图...")
        gen_btn.click()
        self.page.wait_for_timeout(2000)
        
        # 等待魔棒按钮重新恢复为启用状态，即表示生成结束
        logger.info("等待背景图生成完成 (等待按钮重新启用)...")
        expect(gen_btn).to_be_enabled(timeout=60000)
        logger.success("背景图生成成功！")


    def click_create(self):
        """点击 Create 按钮开始生成，并处理可能出现的确认/扣积分弹窗"""
        # 确保没有任何弹窗阻碍点击
        self.close_marketing_popup()
        
        logger.info("点击 Create Lyrics Video 按钮提交任务...")
        create_btn = self.page.locator(Locators.LYRICS_VIDEO_CREATE_BTN)
        # 等待按钮可点击
        expect(create_btn).to_be_enabled(timeout=15000)
        create_btn.click()
        self.page.wait_for_timeout(2000)
        
        # 处理可能出现的扣减积分确认弹窗
        logger.info("检查是否弹出扣减积分确认弹窗...")
        continue_btn = self.page.locator(Locators.CONFIRM_CONTINUE_BTN)
        try:
            continue_btn.wait_for(state="visible", timeout=5000)
            logger.info("检测到 Continue 确认按钮，点击以继续扣除积分生成...")
            continue_btn.dispatch_event("click")
            continue_btn.wait_for(state="hidden", timeout=5000)
            logger.info("积分扣减确认弹窗已关闭")
        except Exception:
            logger.info("未检测到积分扣减确认弹窗或已自动处理")
            
        # 任务创建提交后，必须等待成功 Toast 提示或安全等待 5 秒，以确保后台接口请求处理完成，防止立即切换页面导致接口请求中断而创建失败
        logger.info("等待任务提交接口响应与处理完成...")
        try:
            self.page.locator(Locators.LYRICS_VIDEO_SUCCESS_TOAST).wait_for(state="visible", timeout=3000)
            logger.info("检测到成功提示信息")
        except Exception:
            logger.info("未检测到明显 Toast 提示，使用安全延时")
            
        self.page.wait_for_timeout(5000)

    def wait_for_generation_success(self, timeout: int = 600000):
        """等待当前页面的视频生成成功并显示在视频预览区域"""
        logger.info("在当前页面等待视频生成并渲染完成...")
        
        # 定位视频播放器元素 (Playwright 会自动穿透 Shadow DOM 寻找 video)
        video_locator = self.page.locator(Locators.LYRICS_VIDEO_VIDEO_PLAYER)
        try:
            # 等待视频元素变为可见
            video_locator.wait_for(state="visible", timeout=timeout)
            logger.success("视频生成成功，已在当前页面预览区渲染显示！")
            return True
        except Exception as e:
            logger.error(f"等待视频生成显示超时或失败: {str(e)}")
            return False
