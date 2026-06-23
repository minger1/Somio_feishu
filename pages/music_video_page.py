from playwright.sync_api import expect
from config.locators import Locators
from utils import logger
import time
import os

class MusicVideoPage:
    """封装 AI 音乐视频 (Music Video) 页面相关的操作"""

    def __init__(self, page):
        self.page = page

    def switch_to_music_video(self):
        """通过侧边栏导航切换到音乐视频生成页面并等待加载完成"""
        logger.info("点击左侧导航栏的 AI Music Video 按钮...")
        self.page.locator(Locators.NAV_VIDEO).click()
        
        # 等待页面加载完成 (等待风格输入框变为可见，以确保页面元素渲染稳定)
        logger.info("等待 AI 音乐视频页面加载完成...")
        self.page.locator(Locators.MUSIC_VIDEO_STYLE_TEXTAREA).wait_for(state="visible", timeout=30000)
        
        # 关闭页面可能弹出的营销弹窗
        self.close_marketing_popup()
        logger.info("成功切换至 Music Video 音乐视频页面")

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
        delete_btn = self.page.locator(Locators.MUSIC_VIDEO_AUDIO_DELETE_BTN).first
        if delete_btn.count() > 0 and delete_btn.is_visible():
            logger.info("检测到已存在音频，点击垃圾桶图标清理以开启本地上传...")
            delete_btn.click()
            self.page.wait_for_timeout(1000)

        abs_path = os.path.abspath(file_path)
        logger.info(f"开始导入本地音频文件: {abs_path}")
        self.page.locator(Locators.MUSIC_VIDEO_INPUT_FILE).set_input_files(abs_path)
        self.page.wait_for_timeout(2000)

        # 音乐视频具有时长剪辑弹窗，必须进行确认操作以防阻塞后续的“立即创作”流程
        logger.info("检查是否弹出 Set Clip Duration 剪辑时长弹窗...")
        try:
            self.page.locator(Locators.MUSIC_VIDEO_CLIP_DIALOG).wait_for(state="visible", timeout=8000)
            logger.info("检测到剪辑时长弹窗，点击 Confirm Segment 确认按钮关闭弹窗...")
            self.page.locator(Locators.MUSIC_VIDEO_CLIP_CONFIRM_BTN).click()
            self.page.wait_for_timeout(2000)
        except Exception:
            logger.info("未检测到剪辑时长弹窗，继续后续操作")

    def select_audio_from_library(self):
        """从已有的 Library 列表中选择音乐"""
        # 如果当前有已经导入的音频，先清理/删除
        delete_btn = self.page.locator(Locators.MUSIC_VIDEO_AUDIO_DELETE_BTN).first
        if delete_btn.count() > 0 and delete_btn.is_visible():
            logger.info("检测到已存在音频，点击垃圾桶图标清理以开启音乐库选择...")
            delete_btn.click()
            self.page.wait_for_timeout(1000)

        logger.info("点击 From My Music 从库中选择文件...")
        self.page.locator(Locators.MUSIC_VIDEO_UPLOAD_LIBRARY).click()
        
        # 等待选择音乐库弹窗中的 Select 按钮可见
        logger.info("等待选择音乐库弹窗显示...")
        select_btn = self.page.locator(Locators.MUSIC_VIDEO_LIBRARY_SELECT_BTN).first
        select_btn.wait_for(state="visible", timeout=15000)
        
        # 点击第一个歌曲的 Select 按钮
        logger.info("选择音乐库第一首歌曲项目...")
        select_btn.click()
        self.page.wait_for_timeout(2000)

        # 音乐视频具有时长剪辑弹窗，必须进行时长选择操作
        logger.info("等待弹出的 Set Clip Duration 剪辑时长弹窗...")
        self.page.locator(Locators.MUSIC_VIDEO_CLIP_DIALOG).wait_for(state="visible", timeout=10000)

        logger.info("在剪辑时长弹窗中选择 10s 段落...")
        self.page.locator(Locators.MUSIC_VIDEO_CLIP_10S_BTN).click()
        self.page.wait_for_timeout(500)

        logger.info("点击 Confirm Segment 确认按钮关闭弹窗...")
        self.page.locator(Locators.MUSIC_VIDEO_CLIP_CONFIRM_BTN).click()
        self.page.wait_for_timeout(2000)
        
        logger.success("已成功从 Library 导入目标音频并剪辑为 10s！")

    def upload_background_image(self, file_path: str):
        """导入本地背景图片"""
        abs_path = os.path.abspath(file_path)
        logger.info(f"开始导入本地背景图片: {abs_path}")
        self.page.locator(Locators.MUSIC_VIDEO_INPUT_IMAGE).set_input_files(abs_path)
        self.page.wait_for_timeout(2000)
        logger.success("背景图片导入成功！")

    def input_prompt(self, prompt: str):
        """输入风格或故事描述 Prompt"""
        logger.info(f"输入视频风格/故事描述提示词: {prompt}")
        textarea = self.page.locator(Locators.MUSIC_VIDEO_STYLE_TEXTAREA)
        textarea.fill(prompt)
        self.page.wait_for_timeout(500)

    def click_create(self):
        """点击 Create 按钮开始生成，并处理可能出现的确认/扣积分弹窗"""
        # 确保没有任何弹窗阻碍点击
        self.close_marketing_popup()
        
        logger.info("点击 Create Music Video 按钮提交任务...")
        create_btn = self.page.locator(Locators.MUSIC_VIDEO_CREATE_BTN)
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
            
        # 任务创建提交后，必须安全等待以确保后台接口请求处理完成，防止立即切换页面导致创建失败
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
        
        # 定位视频播放器元素与失败报错弹窗
        video_locator = self.page.locator(Locators.MUSIC_VIDEO_VIDEO_PLAYER)
        error_dialog = self.page.locator(Locators.GENERATE_ERROR_DIALOG)
        
        # 使用轮询方式监控生成状态，检测到失败弹窗时立即报错失败
        start_time = time.time()
        poll_interval = 2.0  # 轮询时间间隔(秒)
        
        logger.info(f"开启轮询监控状态，总超时限制: {timeout/1000}秒...")
        while (time.time() - start_time) < (timeout / 1000):
            # 1. 检测视频播放器是否可见并且有有效的视频源
            if video_locator.is_visible():
                logger.success("视频生成成功，已在当前页面预览区渲染显示！")
                return True
                
            # 2. 检测是否出现了失败报错弹窗
            if error_dialog.is_visible():
                err_text = error_dialog.inner_text().strip().replace('\n', ' ')
                logger.error(f"检测到视频生成失败报错弹窗: {err_text}")
                return False
                
            self.page.wait_for_timeout(int(poll_interval * 1000))
            
        logger.error("在当前页面等待视频生成超时！")
        return False
