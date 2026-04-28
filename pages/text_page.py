from playwright.sync_api import expect
from config.locators import Locators
from utils import logger
import time
import re

class TextPage:
    """封装文本/歌词模式相关的页面操作"""

    def __init__(self, page):
        self.page = page

    def switch_to_lyrics_tab(self):
        """点击顶部 Tab 切换到歌词(Lyrics)特征生成模式"""
        logger.info("切换到 Lyrics 选项卡")
        self.page.locator(Locators.LYRICS_TAB).click()
        self.page.wait_for_timeout(1000)

    def text_input(self, text: str, timeout: int = 10000):
        """在区域内输入文本提示词"""
        logger.info(f"输入文本提示词: {text[:15]}...")
        textarea = self.page.locator(Locators.TEXTAREA_INPUT).first
        textarea.fill(text)
        expect(textarea).to_have_value(text, timeout=timeout)

    def lyrics_input(self, lyrics: str, timeout: int = 10000):
        """输入歌词"""
        logger.info(f"输入歌词文本: {lyrics[:15]}...")
        textarea = self.page.locator(Locators.LYRICS_CONTENT_TEXTAREA).first
        textarea.fill(lyrics)
        expect(textarea).to_have_value(lyrics, timeout=timeout)

    def model_version(self, locator: str, timeout: int = 10000):
        """打开模型下拉并选择指定的版本"""
        # 第一步：点击下拉框标题以展开
        self.page.locator(Locators.MODEL_VERSION_DROPDOWN).click()
        # 增加一小段等待，确保下拉动画完成
        self.page.wait_for_timeout(500)
        # 第二步：点击指定的选项
        self.page.locator(locator).click(force=True)
        logger.success(f"模型版本选择指令发送成功: {locator}")

    def is_limit_dialog_visible(self, timeout: int = 5000) -> bool:
        """检查限制弹窗是否可见"""
        return self.page.locator(Locators.LIMIT_DIALOG).is_visible(timeout=timeout)

    def assert_limit_dialog_visible(self, timeout: int = 5000):
        """断言限制弹窗可见"""
        expect(self.page.locator(Locators.LIMIT_DIALOG)).to_be_visible(timeout=timeout)
        logger.success("验证通过：限制弹窗已弹出")

    def assert_login_modal_visible(self, timeout: int = 5000):
        """断言登录窗口可见"""
        expect(self.page.locator(Locators.LOGIN_MODAL)).to_be_visible(timeout=timeout)
        logger.success("验证通过：登录窗口已弹出")

    def close_limit_dialog(self):
        """关闭限制弹窗"""
        self.page.locator(Locators.LIMIT_DIALOG_CLOSE).click()
        expect(self.page.locator(Locators.LIMIT_DIALOG)).to_be_hidden()
        logger.success("限制弹窗已关闭")

    def click_limit_upgrade(self):
        """点击限制弹窗中的升级按钮"""
        self.page.locator(Locators.LIMIT_UPGRADE_BTN).click(force=True)
        logger.info("点击了限制弹窗中的升级/购买按钮")

    def click_limit_login(self):
        """点击限制弹窗中的登录按钮"""
        self.page.locator(Locators.LIMIT_LOGIN_BTN).click(force=True)
        logger.info("点击了限制弹窗中的登录按钮")

    def click_create(self):
        """点击底部 Create 按钮生成"""
        logger.info("点击 Create 按钮")
        self.page.locator(Locators.CREATE_BTN).click()

    def song_title_input(self, title: str):
        """输入歌曲名称"""
        logger.info(f"输入歌曲名称: '{title}'")
        self.page.locator(Locators.SONG_TITLE_INPUT).fill(title)
        time.sleep(1)

    def text_ai_analysis_popup(self):
        """等待 AI 分析弹窗"""
        logger.info("等待 AI 分析弹窗出现...")
        expect(self.page.locator(Locators.AI_ANALYSIS_MODAL)).to_be_visible(timeout=60000)
        expect(self.page.locator(Locators.AI_CREATE_NOW_BTN).first).to_be_visible(timeout=120000)
        expect(self.page.locator(Locators.AI_ORIGINAL_VERSION_BTN).first).to_be_visible(timeout=120000)

    def switch_ai_analysis_tab(self, tab_name: str):
        """
        AI分析页面切换分页
        tab_name: 'Lyrics Formatting' 或 'Lyrics Refinement'
        """
        tabs = self.page.locator(Locators.LYRICS_AI_ANALYSIS_TABS)
        if tab_name.lower() == "formatting":
            tabs.nth(0).click()
        elif tab_name.lower() == "refinement":
            tabs.nth(1).click()
        else:
            # 或者直接按文本匹配
            tabs.filter(has_text=tab_name).click()
        logger.info(f"AI分析页面切换到分页: {tab_name}")


    def text_select_original(self):
        """选择 Original Version"""
        logger.info("选择 Original Version")
        self.page.locator(Locators.AI_ORIGINAL_VERSION_BTN).first.dispatch_event("click")

    def text_select_create_now(self):
        """选择 Create Now"""
        logger.info("选择 Create Now (AI)")
        self.page.locator(Locators.AI_CREATE_NOW_BTN).first.dispatch_event("click")


    def text_select_view_lyrics(self):
        """
        文本模式下ai分析窗口-查看歌词
        """
        self.page.locator(Locators.AI_VIEW_LYRICS_BTN).dispatch_event("click")
        logger.info("点击了查看歌词按钮")
    
    def text_select_view_lyrics_generate(self):
        """
        文本模式下ai分析窗口-查看歌词-生成歌词
        """
        self.page.locator(Locators.LYRICS_GENERATE_BTN).dispatch_event("click")
        logger.info("点击了歌词生成按钮")
    
    def text_select_view_lyrics_edit(self):
        """
        文本模式下ai分析窗口-查看歌词-编辑歌词
        """
        self.page.locator(Locators.LYRICS_EDIT_BTN).dispatch_event("click")
        logger.info("点击了歌词编辑按钮")

    def edit_generated_lyrics_title(self, new_title: str):
        """
        在歌词生成窗口修改被 AI 覆盖的歌名
        """
        # 点击编辑按钮
        self.page.locator(Locators.LYRICS_EDIT_BTN).dispatch_event("click")
        logger.info("点击编辑按钮，准备修改被AI覆盖的歌名")
        
        # 输入新的歌名
        self.page.locator(Locators.LYRICS_TITLE_INPUT).fill(new_title)
        
        # 保存编辑
        self.page.locator(Locators.LYRICS_EDIT_SAVE_BTN).dispatch_event("click")
        logger.info(f"保存了修改后的歌名: {new_title}")
        self.page.wait_for_timeout(500)

    def text_select_view_lyrics_edit_cancel(self):
        """
        文本模式下ai分析窗口-查看歌词-编辑歌词-取消编辑
        """
        self.page.locator(Locators.LYRICS_EDIT_CANCEL_BTN).dispatch_event("click")
        logger.info("点击了歌词编辑取消按钮")

    def text_select_view_lyrics_edit_save(self):
        """
        文本模式下ai分析窗口-查看歌词-编辑歌词-保存编辑
        """
        self.page.locator(Locators.LYRICS_EDIT_SAVE_BTN).dispatch_event("click")
        logger.info("点击了歌词编辑保存按钮")

    def text_select_view_lyrics_edit_clear(self):
        """
        文本模式下ai分析窗口-查看歌词-编辑歌词-清除歌词
        """
        self.page.locator(Locators.LYRICS_CLEAR_BTN).dispatch_event("click")
        logger.info("点击了歌词清除按钮")

    def confirm_generation(self):
        """弹窗确认扣费生成"""
        logger.info("检查并确认扣费系统弹窗...")
        if self.page.locator(Locators.CONFIRM_DIALOG).is_visible(timeout=5000):
            logger.info("点击 Continue 确认生成")
            self.page.locator(Locators.CONFIRM_CONTINUE_BTN).dispatch_event("click")

    def confirm_cancel(self):
        """取消生成"""
        logger.info("检查积分弹窗...")
        if self.page.locator(Locators.CONFIRM_DIALOG).is_visible(timeout=5000):
            logger.info("点击 Cancel 取消生成")
            self.page.locator(Locators.CONFIRM_CANCEL_BTN).dispatch_event("click")

    def wait_for_generation_success(self, title: str = None, timeout: int = 600000):
        """
        判断歌曲生成成功（适配新版列表 UI）：
        1. 通过 span.text 精准过滤任务（避免匹配 span.model 等其他 span）
        2. 同名任务取 .first（一次生成产出多个版本时不误判）
        3. 轮询：loading class 消失 且 .cover .duration 出现（新 UI 下载按钮已移入三点菜单）
        """
        logger.info(f"开始等待歌曲生成（监控歌曲: {title if title else '最新任务'}）...")

        def _make_locator(t):
            """按 span.text 精准过滤，返回 li.item 集合（.first 在外层统一取）"""
            return self.page.locator("li.item").filter(
                has=self.page.locator(Locators.LIBRARY_ITEM_TITLE_SPAN,
                                      has_text=re.compile(re.escape(t), re.IGNORECASE))
            )

        if title:
            task_locator = _make_locator(title)
        else:
            task_locator = self.page.locator(Locators.LOADING_TASK)

        start_time = time.time()
        found_loading = False
        using_fallback = False

        while time.time() - start_time < timeout / 1000:
            try:
                # 超过 30s 还找不到指定 title，尝试回退追踪最新 loading 任务
                if title and not using_fallback and time.time() - start_time > 30:
                    if task_locator.count() == 0:
                        temp_latest = self.page.locator(Locators.LOADING_TASK)
                        if temp_latest.count() > 0:
                            try:
                                new_title = temp_latest.first.locator(
                                    Locators.LIBRARY_ITEM_TITLE_SPAN
                                ).first.text_content(timeout=3000).strip()
                                if new_title:
                                    logger.warning(f"未找到 '{title}'，切换追踪最新任务 '{new_title}'")
                                    title = new_title
                                    task_locator = _make_locator(title)
                                    using_fallback = True
                            except:
                                logger.warning(f"未找到 '{title}'，回退至第一个 loading 任务")
                                task_locator = temp_latest
                                using_fallback = True
                        else:
                            logger.debug("尚未发现任何生成中的任务...")

                # 关闭随机弹窗
                close_btn = self.page.locator(
                    "//div[contains(@class, 'close') or contains(@class, 'icon-close')]"
                ).first
                if close_btn.is_visible():
                    close_btn.click()
                    logger.debug("检测到并关闭了随机弹窗")

                cnt = task_locator.count()
                if cnt > 0:
                    item = task_locator.first
                    current_class = item.get_attribute("class") or ""

                    if "loading" in current_class:
                        if not found_loading:
                            logger.info(f"歌曲持续生成中 (匹配到 {cnt} 条)")
                            found_loading = True
                    else:
                        # 新 UI：下载按钮已移入三点菜单，改用封面时长标签判断生成成功
                        duration = item.locator(Locators.LIBRARY_ITEM_DURATION)
                        if duration.count() > 0 and duration.first.is_visible():
                            logger.info(f"歌曲生成完成: {title}")
                            return True
                        else:
                            logger.info("等待页面状态刷新...")
                else:
                    if time.time() - start_time > 20:
                        logger.warning(f"尚未在列表中找到标题为 '{title}' 的任务...")

            except Exception as e:
                logger.debug(f"轮询中遇到异常 (可能正在刷新): {e}")

            time.sleep(10)

        logger.error(f"歌曲生成等待超时 ({timeout/1000}s)")
        return False


    def run_model_generation_flow(self, model_name: str, model_locator: str):
        """通用底层模型切换生成辅助方法"""
        from utils import get_song
        from data.test_data import TEST_TEXT_PROMPT
        logger.info(f"开始执行纯文本模式下的模型切换生成操作: {model_name}")
        
        # 1. 先切换模型
        self.model_version(model_locator)

        # 2. 输入歌词/文本提示
        test_text = TEST_TEXT_PROMPT
        self.text_input(test_text)
        
        # 3. 输入歌名
        song_title = get_song()
        self.song_title_input(song_title)
        
        # 4. 点击创建
        self.click_create()

        # 5. ai分析窗口出现，断言特定元素
        logger.info("等待 AI 分析弹窗就绪...")
        self.text_ai_analysis_popup()

        # 6. 最后点击创建 (这里用 Original Version 作为最终创建)
        self.text_select_original()
        self.confirm_generation()
        
        success = self.wait_for_generation_success(title=song_title, timeout=600000)
        return success, song_title
