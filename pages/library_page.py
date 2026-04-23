from playwright.sync_api import Page, expect
from config.locators import Locators
from loguru import logger

class LibraryPage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to_library(self):
        """导航至 Library 页面"""
        logger.info("导航至 Library 页面")
        self.page.locator(Locators.LIBRARY_NAV).click()
        self.page.wait_for_selector(Locators.LIBRARY_SONG_ITEMS, state="visible", timeout=10000)

    def switch_to_my_songs(self):
        """切换到 My Songs 面板"""
        self.page.locator(Locators.LIBRARY_TAB_MY_SONGS).click()
        self.page.wait_for_timeout(500)

    def switch_to_favorites(self):
        """切换到 Favorites 面板"""
        self.page.locator(Locators.LIBRARY_TAB_FAVORITES).click()
        self.page.wait_for_timeout(500)

    def search_song(self, keyword: str):
        """在搜索框中搜索歌曲"""
        logger.info(f"搜索歌曲: {keyword}")
        self.page.locator(Locators.LIBRARY_SEARCH_INPUT).fill(keyword)
        self.page.wait_for_timeout(1000)

    def get_song_item(self, index: int):
        """获取指定索引的已完成生成的歌曲 item locator
        (过滤掉没有时长标签的生成中任务，以封面时长标签作为完成标志)"""
        return self.page.locator(Locators.LIBRARY_SONG_ITEMS).filter(
            has=self.page.locator(Locators.LIBRARY_ITEM_DURATION)
        ).nth(index)

    def get_song_info(self, item_locator) -> dict:
        """获取单首歌曲的详细信息"""
        title    = item_locator.locator(Locators.LIBRARY_ITEM_TITLE).text_content()
        model    = item_locator.locator(Locators.LIBRARY_ITEM_MODEL).text_content()
        duration = item_locator.locator(Locators.LIBRARY_ITEM_DURATION).text_content()
        time_text = item_locator.locator(Locators.LIBRARY_ITEM_TIME).text_content()
        tags     = item_locator.locator(Locators.LIBRARY_ITEM_TAGS).all_text_contents()

        return {
            "title":    title.strip()     if title    else "",
            "model":    model.strip()     if model    else "",
            "duration": duration.strip()  if duration else "",
            "time":     time_text.strip() if time_text else "",
            "tags":     tags
        }

    def play_song(self, item_locator):
        """点击封面播放/暂停歌曲"""
        item_locator.locator(Locators.LIBRARY_ITEM_COVER).click()

    def click_like(self, item_locator):
        """点击点赞👍按钮"""
        logger.info("点击歌曲点赞按钮")
        btn = item_locator.locator(Locators.LIBRARY_ITEM_BTN_LIKE)
        btn.click()
        self.page.wait_for_timeout(500)
        return btn

    def click_dislike(self, item_locator):
        """点击踩👎按钮（会弹出 User Feedback 反馈弹窗）"""
        logger.info("点击歌曲踩按钮")
        btn = item_locator.locator(Locators.LIBRARY_ITEM_BTN_DISLIKE)
        btn.click()
        self.page.wait_for_timeout(800)
        return btn

    # ====== 踩后弹出的 User Feedback 弹窗操作 ======

    def _feedback_dialog(self):
        """返回 User Feedback 弹窗 locator（优先用 .feedback-dialog，fallback 用文本定位）"""
        # 优先精确 class 匹配，fallback 用弹窗内标题文字定位其父容器
        dialog = self.page.locator(".feedback-dialog").first
        if dialog.count() == 0:
            dialog = self.page.locator("[class*='feedback-dialog']").first
        if dialog.count() == 0:
            dialog = self.page.locator("[class*='feedback-wrapper']").first
        return dialog

    def wait_for_feedback_dialog(self, timeout: int = 5000):
        """等待 User Feedback 弹窗出现"""
        logger.info("等待 User Feedback 弹窗出现")
        self.page.wait_for_selector(
            ".feedback-dialog, [class*='feedback-dialog'], [class*='feedback-wrapper']",
            state="visible", timeout=timeout
        )

    def close_feedback_dialog(self):
        """点击 ✕ 关闭 User Feedback 弹窗"""
        logger.info("关闭 User Feedback 弹窗")
        self.page.locator(
            ".feedback-dialog .close, [class*='feedback-dialog'] .close, "
            "[class*='feedback-wrapper'] .close"
        ).first.click()
        self.page.wait_for_timeout(500)

    def select_feedback_option(self, index: int):
        """选择反馈类型单选项（index: 1=Generation failed, 2=Result not as expected,
        3=Add more styles, 4=Need more features, 5=Price/subscription, 6=Others）"""
        logger.info(f"选择反馈类型 option[{index}]")
        options = self.page.locator("[class*='feedback'] [class*='option']")
        count = options.count()
        assert count >= index, f"反馈选项数量不足，期望至少 {index} 个，实际 {count} 个"
        options.nth(index - 1).click()
        self.page.wait_for_timeout(300)

    def fill_feedback_description(self, text: str):
        """填写详细描述文本框"""
        logger.info(f"填写反馈描述: {text}")
        self.page.locator(Locators.DISLIKE_FEEDBACK_TEXTAREA).fill(text)

    def fill_feedback_email(self, email: str):
        """填写联系邮箱"""
        logger.info(f"填写联系邮箱: {email}")
        self.page.locator(Locators.DISLIKE_FEEDBACK_EMAIL).fill(email)

    def submit_feedback(self):
        """点击 Submit 提交反馈"""
        logger.info("提交 User Feedback")
        self.page.locator(Locators.DISLIKE_FEEDBACK_SUBMIT).click()
        self.page.wait_for_timeout(1000)


    def click_collect(self, item_locator):
        """点击收藏❤️按钮"""
        logger.info("点击歌曲收藏按钮")
        btn = item_locator.locator(Locators.LIBRARY_ITEM_BTN_COLLECT)
        btn.click()
        self.page.wait_for_timeout(500)
        return btn

    def share_and_verify_clipboard(self, item_locator) -> str:
        """点击行内快捷分享按钮并读取/断言剪贴板内容"""
        logger.info("点击快捷分享按钮")
        item_locator.locator(Locators.LIBRARY_ITEM_BTN_SHARE).click()
        self.page.wait_for_timeout(1000)
        copied_url = self.page.evaluate("navigator.clipboard.readText()")
        assert "/generate" in copied_url and "isShare" in copied_url, f"剪切板链接非法: {copied_url}"
        return copied_url

    def get_safe_title(self, item_locator) -> str:
        """获取并过滤非法文件名字符的歌曲标题"""
        import re
        song_title = item_locator.locator(Locators.LIBRARY_ITEM_TITLE).text_content()
        return re.sub(r'[\\/:*?"<>|]', '', song_title).strip()

    def _verify_download(self, download_obj, expected_ext, safe_title):
        """校验下载文件的后缀和名称"""
        name = download_obj.suggested_filename
        assert name.endswith(expected_ext), f"预期后缀: {expected_ext}, 实际获取: {name}"
        assert safe_title in name, f"期望下载包含歌名: {safe_title}, 实际获取: {name}"
        assert download_obj.path(), f"文件未成功写入: {expected_ext}"
        logger.success(f"文件下载断言成功: {name}")

    # ====== More 菜单操作 ======

    def open_more_menu(self, item_locator):
        """打开该歌曲的 More 菜单（三点图标）"""
        logger.info("打开歌曲的 More 菜单")
        item_locator.locator(Locators.LIBRARY_ITEM_BTN_MORE).click()
        self.page.wait_for_timeout(300)

    def click_more_edit_name(self, item_locator):
        """More 菜单 → Edit Song Name"""
        logger.info("选择 Edit Song Name")
        self.open_more_menu(item_locator)
        self.page.locator(Locators.LIBRARY_ITEM_MORE_EDIT).first.click()

    def edit_song_name(self, item_locator, new_name: str):
        """完整的修改歌名流程（含保存）"""
        logger.info(f"编辑歌名: {new_name}")
        self.click_more_edit_name(item_locator)
        self.page.wait_for_selector(Locators.LIBRARY_ITEM_MORE_EDIT_DIALOG, state="visible", timeout=5000)
        self.page.locator(Locators.LIBRARY_ITEM_MORE_EDIT_NAME_INPUT).fill(new_name)
        self.page.locator(Locators.LIBRARY_ITEM_MORE_EDIT_SAVE_BTN).click()
        self.page.wait_for_selector(Locators.LIBRARY_ITEM_MORE_EDIT_DIALOG, state="hidden")

    def click_more_download_and_verify_video(self, item_locator):
        """More 菜单 → Download → Video，并完成下载断言"""
        safe_title = self.get_safe_title(item_locator)
        logger.info(f"More 菜单下载 Video: {safe_title}")
        self.open_more_menu(item_locator)
        self.page.locator(Locators.LIBRARY_ITEM_MORE_DOWNLOAD).first.hover()
        with self.page.expect_download() as info:
            self.page.locator(Locators.LIBRARY_ITEM_MORE_DOWNLOAD_VIDEO).first.click()
        self._verify_download(info.value, ".mp4", safe_title)

    def click_more_download_and_verify_audio(self, item_locator):
        """More 菜单 → Download → Audio，并完成下载断言"""
        safe_title = self.get_safe_title(item_locator)
        logger.info(f"More 菜单下载 Audio: {safe_title}")
        self.open_more_menu(item_locator)
        self.page.locator(Locators.LIBRARY_ITEM_MORE_DOWNLOAD).first.hover()
        with self.page.expect_download() as info:
            self.page.locator(Locators.LIBRARY_ITEM_MORE_DOWNLOAD_AUDIO).first.click()
        self._verify_download(info.value, ".mp3", safe_title)

    def click_more_vocal(self, item_locator):
        """More 菜单 → Vocal Remover"""
        logger.info("选择 Vocal Remover")
        self.open_more_menu(item_locator)
        self.page.locator(Locators.LIBRARY_ITEM_MORE_VOCAL).first.click()

    def click_more_stem(self, item_locator):
        """More 菜单 → Stem Splitter"""
        logger.info("选择 Stem Splitter")
        self.open_more_menu(item_locator)
        self.page.locator(Locators.LIBRARY_ITEM_MORE_STEM).first.click()

    def click_more_edit_original(self, item_locator):
        """More 菜单 → Edit Original"""
        logger.info("选择 Edit Original")
        self.open_more_menu(item_locator)
        self.page.locator(Locators.LIBRARY_ITEM_MORE_EDIT_ORIGINAL).first.click()

    def click_more_favorite(self, item_locator):
        """More 菜单 → Add to Favorites"""
        logger.info("选择 Add to Favorites")
        self.open_more_menu(item_locator)
        self.page.locator(Locators.LIBRARY_ITEM_MORE_FAVORITE).first.click()

    def click_more_external(self, item_locator):
        """More 菜单 → Share（外部分享，复制链接）"""
        logger.info("选择 Share (外部分享)")
        self.open_more_menu(item_locator)
        self.page.locator(Locators.LIBRARY_ITEM_MORE_EXTERNAL).first.click()

    def click_more_delete(self, item_locator):
        """More 菜单 → Delete"""
        logger.info("选择 Delete")
        self.open_more_menu(item_locator)
        self.page.locator(Locators.LIBRARY_ITEM_MORE_DELETE).first.click()

    def delete_song(self, item_locator):
        """完整的删除歌曲流程（含确认弹窗）"""
        logger.info("执行删除歌曲")
        self.click_more_delete(item_locator)
        self.page.wait_for_selector(Locators.LIBRARY_ITEM_MORE_DELETE_DIALOG, state="visible", timeout=5000)
        self.page.locator(Locators.LIBRARY_ITEM_MORE_DELETE_CONFIRM_BTN).click()
        self.page.wait_for_selector(Locators.LIBRARY_ITEM_MORE_DELETE_DIALOG, state="hidden")
