from playwright.sync_api import Page, expect
from config.locators import Locators
from loguru import logger
import re
import time


class LibraryPage:
    """封装 Library 页面操作 (新版 UI: Songs/Sounds/Videos 三主 Tab + All/Liked 子过滤器)"""

    def __init__(self, page: Page):
        self.page = page

    # ------------------------------------------------------------------
    # 导航
    # ------------------------------------------------------------------

    def navigate_to_library(self):
        """点击侧边栏 Library 导航，等待歌曲列表加载"""
        logger.info("导航至 Library 页面")
        self.page.locator(Locators.LIBRARY_NAV).click()
        # 等待歌曲列表出现（li.item 为已完成歌曲）
        self.page.wait_for_selector(Locators.LIBRARY_SONG_ITEMS, state="visible", timeout=15000)
        self.page.wait_for_timeout(800)

    # ------------------------------------------------------------------
    # 主 Tab 切换：Songs / Sounds / Videos
    # ------------------------------------------------------------------

    def switch_to_songs_tab(self):
        """切换到 Songs 主 Tab"""
        logger.info("切换到 Songs 主 Tab")
        self.page.locator(Locators.LIBRARY_TAB_SONGS).click()
        self.page.wait_for_timeout(600)

    def switch_to_sounds_tab(self):
        """切换到 Sounds (新版 UI 为 Songs 主 Tab 下的 Sound Effects 子 Tab)"""
        logger.info("切换到 Sounds (Sound Effects) 子 Tab")
        self.switch_to_songs_tab()
        self.page.locator(Locators.LIBRARY_SUB_TAB_SOUNDS).click()
        self.page.wait_for_timeout(600)

    def switch_to_videos_tab(self):
        """切换到 Videos 主 Tab"""
        logger.info("切换到 Videos 主 Tab")
        self.page.locator(Locators.LIBRARY_TAB_VIDEOS).click()
        self.page.wait_for_timeout(600)

    def switch_to_creations_tab(self):
        """切换到 Creations 子 Tab"""
        logger.info("切换到 Creations 子 Tab")
        self.switch_to_songs_tab()
        self.page.locator(Locators.LIBRARY_SUB_TAB_CREATIONS).click()
        self.page.wait_for_timeout(600)

    def switch_to_extensions_tab(self):
        """切换到 Extensions 子 Tab"""
        logger.info("切换到 Extensions 子 Tab")
        self.switch_to_songs_tab()
        self.page.locator(Locators.LIBRARY_SUB_TAB_EXTENSIONS).click()
        self.page.wait_for_timeout(600)

    def switch_to_remixes_tab(self):
        """切换到 Remixes 子 Tab"""
        logger.info("切换到 Remixes 子 Tab")
        self.switch_to_songs_tab()
        self.page.locator(Locators.LIBRARY_SUB_TAB_REMIXES).click()
        self.page.wait_for_timeout(600)

    # ------------------------------------------------------------------
    # 子过滤器切换：All / Liked (新版下拉菜单)
    # ------------------------------------------------------------------

    def switch_to_all_filter(self):
        """切换到 All 子过滤器"""
        logger.info("切换子过滤器到 All")
        current = self.page.locator(Locators.LIBRARY_FILTER_ACTIVE).text_content()
        if "All" not in current:
            self.page.locator(Locators.LIBRARY_FILTER_SELECT).click()
            self.page.wait_for_timeout(300)
            self.page.locator(Locators.LIBRARY_FILTER_ALL).click()
            self.page.wait_for_timeout(500)

    def switch_to_liked_filter(self):
        """切换到 Liked 子过滤器"""
        logger.info("切换子过滤器到 Liked")
        current = self.page.locator(Locators.LIBRARY_FILTER_ACTIVE).text_content()
        if "Liked" not in current:
            self.page.locator(Locators.LIBRARY_FILTER_SELECT).click()
            self.page.wait_for_timeout(300)
            self.page.locator(Locators.LIBRARY_FILTER_LIKED).click()
            self.page.wait_for_timeout(500)

    # 兼容旧接口命名
    def switch_to_my_songs(self):
        """[兼容旧版] 切换到 Songs Tab (原 My Songs)"""
        self.switch_to_songs_tab()

    def switch_to_favorites(self):
        """[兼容旧版] 切换到 Liked 过滤器 (原 Favorites Tab)"""
        self.switch_to_liked_filter()

    # ------------------------------------------------------------------
    # 搜索
    # ------------------------------------------------------------------

    def search_song(self, keyword: str):
        """在搜索框中输入关键字"""
        logger.info(f"搜索歌曲: {keyword}")
        self.page.locator(Locators.LIBRARY_SEARCH_INPUT).fill(keyword)
        self.page.wait_for_timeout(1000)

    # ------------------------------------------------------------------
    # 歌曲列表操作
    # ------------------------------------------------------------------

    def get_song_item(self, index: int = 0):
        """
        获取指定索引的已完成歌曲 item locator。
        通过封面时长标签过滤掉"生成中"任务，取第 index 首。
        """
        return (
            self.page.locator(Locators.LIBRARY_SONG_ITEMS)
            .filter(has=self.page.locator(Locators.LIBRARY_ITEM_DURATION))
            .nth(index)
        )

    def get_song_item_count(self) -> int:
        """获取已完成歌曲的数量"""
        return (
            self.page.locator(Locators.LIBRARY_SONG_ITEMS)
            .filter(has=self.page.locator(Locators.LIBRARY_ITEM_DURATION))
            .count()
        )

    def get_song_info(self, item_locator) -> dict:
        """提取单首歌曲的元数据"""
        title    = item_locator.locator(Locators.LIBRARY_ITEM_TITLE).text_content(timeout=3000)
        duration = item_locator.locator(Locators.LIBRARY_ITEM_DURATION).first.text_content(timeout=3000)
        
        # 优化：先通过 count() 判断元素是否存在，避免无意义的 timeout 等待
        model_loc = item_locator.locator(Locators.LIBRARY_ITEM_MODEL)
        model = model_loc.first.text_content() if model_loc.count() > 0 else ""
        
        time_loc = item_locator.locator(Locators.LIBRARY_ITEM_TIME)
        time_text = time_loc.first.text_content() if time_loc.count() > 0 else ""
        
        tags_loc = item_locator.locator(Locators.LIBRARY_ITEM_TAGS)
        tags = tags_loc.all_text_contents() if tags_loc.count() > 0 else []

        return {
            "title":    title.strip()    if title    else "",
            "duration": duration.strip() if duration else "",
            "model":    model.strip()    if model    else "",
            "time":     time_text.strip() if time_text else "",
            "tags":     tags,
        }


    def get_safe_title(self, item_locator) -> str:
        """获取并过滤非法文件名字符的歌曲标题"""
        song_title = item_locator.locator(Locators.LIBRARY_ITEM_TITLE).text_content()
        return re.sub(r'[\\/:*?"<>|]', '', song_title).strip()

    # ------------------------------------------------------------------
    # 行内操作按钮（始终可见）
    # ------------------------------------------------------------------

    def _get_btn(self, item_locator, btn_locator: str):
        """在 item 范围内定位操作按钮"""
        return item_locator.locator(btn_locator).first

    def click_like(self, item_locator):
        """点击点赞 👍"""
        logger.info("点击点赞按钮")
        btn = self._get_btn(item_locator, Locators.LIBRARY_ITEM_BTN_LIKE)
        btn.click()
        self.page.wait_for_timeout(500)
        return btn

    def click_dislike(self, item_locator):
        """点击踩 👎（确保触发 User Feedback 反馈弹窗）"""
        logger.info("点击踩按钮")
        btn = self._get_btn(item_locator, Locators.LIBRARY_ITEM_BTN_DISLIKE)
        # 自动检测是否已经点亮，若点亮则先点击一次取消，再点击一次以触发弹窗
        btn_class = btn.get_attribute("class") or ""
        svg = btn.locator("svg").first
        svg_class = svg.get_attribute("class") if svg.count() > 0 else ""
        
        is_active = "active" in btn_class or "active" in svg_class or "disliked" in btn_class
        logger.info(f"倒赞状态检测: btn_class='{btn_class}', svg_class='{svg_class}', is_active={is_active}")
        
        if is_active:
            logger.info("倒赞已点亮，先点击一次取消踩，再点击一次以触发反馈弹窗")
            btn.click()
            self.page.wait_for_timeout(500)
            btn.click()
        else:
            logger.info("倒赞未点亮，直接点击触发反馈弹窗")
            btn.click()
            
        self.page.wait_for_timeout(800)
        return btn

    def click_collect(self, item_locator):
        """点击收藏 ❤️"""
        logger.info("点击收藏按钮")
        btn = self._get_btn(item_locator, Locators.LIBRARY_ITEM_BTN_COLLECT)
        btn.click()
        self.page.wait_for_timeout(500)
        return btn

    def click_share(self, item_locator):
        """点击快捷分享按钮并读取剪贴板内容"""
        logger.info("点击快捷分享按钮")
        self._get_btn(item_locator, Locators.LIBRARY_ITEM_BTN_SHARE).click()
        self.page.wait_for_timeout(1000)
        return self.page.evaluate("navigator.clipboard.readText()")

    # ------------------------------------------------------------------
    # More 菜单（三点按钮）
    # ------------------------------------------------------------------

    def open_more_menu(self, item_locator):
        """打开三点 More 菜单"""
        logger.info("打开 More 菜单")
        self._get_btn(item_locator, Locators.LIBRARY_ITEM_BTN_MORE).click()
        self.page.wait_for_timeout(400)

    def _click_more_item(self, item_locator, menu_locator: str, item_log_name: str = ""):
        """打开 More 菜单并点击指定菜单项"""
        self.open_more_menu(item_locator)
        if item_log_name:
            logger.info(f"选择 {item_log_name}")
        self.page.locator(menu_locator).first.click()
        self.page.wait_for_timeout(300)

    def click_more_edit_name(self, item_locator):
        """More → Edit Song Name"""
        self._click_more_item(item_locator, Locators.LIBRARY_MORE_EDIT_NAME, "Edit Song Name")

    def click_more_download(self, item_locator):
        """More → Download（悬停展开子菜单）"""
        self.open_more_menu(item_locator)
        logger.info("悬停展开 Download 子菜单")
        self.page.locator(Locators.LIBRARY_MORE_DOWNLOAD).first.hover()
        self.page.wait_for_timeout(300)

    def click_more_download_video(self, item_locator):
        """More → Download → Video"""
        logger.info("More 菜单下载 Video")
        self.click_more_download(item_locator)
        with self.page.expect_download() as info:
            self.page.locator(Locators.LIBRARY_MORE_DOWNLOAD_VIDEO).first.click()
        return info.value

    def click_more_download_audio(self, item_locator):
        """More → Download → Audio"""
        logger.info("More 菜单下载 Audio")
        self.click_more_download(item_locator)
        with self.page.expect_download() as info:
            self.page.locator(Locators.LIBRARY_MORE_DOWNLOAD_AUDIO).first.click()
        return info.value

    def click_more_vocal(self, item_locator):
        """More → Vocal Remover"""
        self._click_more_item(item_locator, Locators.LIBRARY_MORE_VOCAL, "Vocal Remover")

    def click_more_stem(self, item_locator):
        """More → Stem Splitter"""
        self._click_more_item(item_locator, Locators.LIBRARY_MORE_STEM, "Stem Splitter")

    def click_more_edit_original(self, item_locator):
        """More → Edit Original"""
        self._click_more_item(item_locator, Locators.LIBRARY_MORE_EDIT_ORIGINAL, "Edit Original")

    def click_more_favorite(self, item_locator):
        """More → Add to Favorites"""
        self._click_more_item(item_locator, Locators.LIBRARY_MORE_FAVORITE, "Add to Favorites")

    def click_more_share(self, item_locator):
        """More → Share（外部分享）"""
        self._click_more_item(item_locator, Locators.LIBRARY_MORE_SHARE, "Share (外部分享)")
        self.page.wait_for_timeout(500)

    def click_more_delete(self, item_locator):
        """More → Delete"""
        self._click_more_item(item_locator, Locators.LIBRARY_MORE_DELETE, "Delete")

    # 兼容旧接口
    def click_more_external(self, item_locator):
        """[兼容旧版] More → Share 外部分享"""
        self.click_more_share(item_locator)

    def click_more_download_and_verify_video(self, item_locator):
        """[兼容旧版] More 菜单 → Download → Video，并完成下载断言"""
        safe_title = self.get_safe_title(item_locator)
        logger.info(f"More 菜单下载 Video: {safe_title}")
        dl = self.click_more_download_video(item_locator)
        name = dl.suggested_filename
        assert name.endswith(".mp4"), f"预期 .mp4 后缀，实际: {name}"
        logger.success(f"Video 下载断言成功: {name}")

    def click_more_download_and_verify_audio(self, item_locator):
        """[兼容旧版] More 菜单 → Download → Audio，并完成下载断言"""
        safe_title = self.get_safe_title(item_locator)
        logger.info(f"More 菜单下载 Audio: {safe_title}")
        dl = self.click_more_download_audio(item_locator)
        name = dl.suggested_filename
        assert name.endswith(".mp3"), f"预期 .mp3 后缀，实际: {name}"
        logger.success(f"Audio 下载断言成功: {name}")

    # ------------------------------------------------------------------
    # Edit Song Name 弹窗
    # ------------------------------------------------------------------

    def edit_song_name(self, item_locator, new_name: str):
        """完整修改歌名流程（含保存）"""
        logger.info(f"修改歌名为: {new_name}")
        self.click_more_edit_name(item_locator)
        self.page.wait_for_selector(Locators.LIBRARY_EDIT_NAME_DIALOG, state="visible", timeout=5000)
        self.page.locator(Locators.LIBRARY_EDIT_NAME_INPUT).fill(new_name)
        self.page.locator(Locators.LIBRARY_EDIT_NAME_SAVE_BTN).click()
        self.page.wait_for_selector(Locators.LIBRARY_EDIT_NAME_DIALOG, state="hidden", timeout=5000)
        logger.success(f"歌名已修改为: {new_name}")

    # ------------------------------------------------------------------
    # Delete 弹窗
    # ------------------------------------------------------------------

    def delete_song(self, item_locator):
        """完整删除歌曲流程（含确认弹窗）"""
        logger.info("执行删除歌曲")
        self.click_more_delete(item_locator)
        self.page.wait_for_selector(Locators.LIBRARY_DELETE_DIALOG, state="visible", timeout=5000)
        self.page.locator(Locators.LIBRARY_DELETE_CONFIRM_BTN).click()
        self.page.wait_for_selector(Locators.LIBRARY_DELETE_DIALOG, state="hidden", timeout=5000)
        logger.success("歌曲已删除")

    # ------------------------------------------------------------------
    # User Feedback 弹窗（踩后触发）
    # ------------------------------------------------------------------

    def wait_for_feedback_dialog(self, timeout: int = 5000):
        """等待 User Feedback 弹窗出现"""
        logger.info("等待 User Feedback 弹窗出现")
        self.page.wait_for_selector(
            Locators.DISLIKE_FEEDBACK_DIALOG,
            state="visible", timeout=timeout
        )

    def close_feedback_dialog(self):
        """点击 ✕ 关闭 User Feedback 弹窗"""
        logger.info("关闭 User Feedback 弹窗")
        self.page.locator(Locators.DISLIKE_FEEDBACK_CLOSE_BTN).first.click()
        self.page.wait_for_timeout(500)

    def select_feedback_option(self, index: int):
        """
        选择反馈类型 (1-based):
        1=Generation failed, 2=Result not as expected,
        3=Add more styles, 4=Need more features,
        5=Price/subscription, 6=Others
        """
        logger.info(f"选择反馈选项 [{index}]")
        options = self.page.locator(Locators.DISLIKE_FEEDBACK_OPTION_ITEMS)
        count = options.count()
        assert count >= index, f"反馈选项数量不足，期望 >= {index}，实际 {count}"
        options.nth(index - 1).click()
        self.page.wait_for_timeout(300)

    def fill_feedback_description(self, text: str):
        """填写详细描述"""
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

    def wait_for_generation_success(self, title: str = None, timeout: int = 600000):
        """
        判断歌曲生成成功（适配新版列表 UI）：
        1. 通过 span.text 精准过滤任务（避免匹配 span.model 等其他 span）
        2. 同名任务取 .first（一次生成产出多个版本时不误判）
        3. 轮询：loading class 消失 且 出现收藏/更多按钮（新 UI 下载按钮已移入三点菜单）
        4. 弹性保障：自动记录当前任务生成时间。若因生成失败导致标题被替换为 'Generation failed.'，
           则通过时间精准定位并检测 'Retry' 按钮或失败文本，快速返回失败以避免不必要的等待。
        """
        logger.info(f"开始等待歌曲生成（监控歌曲: {title if title else '最新任务'}）...")

        def _make_locator(t):
            """按 span.text 精准过滤，返回 li.item 集合（.first 在外层统一取）"""
            return self.page.locator("li.item").filter(
                has=self.page.locator(Locators.LIBRARY_ITEM_TITLE_SPAN,
                                      has_text=re.compile(re.escape(t), re.IGNORECASE))
            )

        if title and str(title).lower() in ["none", ""]:
            title = None

        if title:
            task_locator = _make_locator(title)
        else:
            # 弹性等待新提交的任务成功插入到列表顶端
            try:
                self.page.locator(Locators.LOADING_TASK).first.wait_for(state="visible", timeout=15000)
                logger.info("已成功捕获到新提交的生成任务行")
            except Exception:
                logger.warning("等待新生成任务行超时，回退直接捕获库列表首项")
            task_locator = self.page.locator(Locators.LIBRARY_SONG_ITEMS).first

        start_time = time.time()
        found_loading = False
        using_fallback = False
        recorded_time = None

        while time.time() - start_time < timeout / 1000:
            try:
                # 检测是否有发生错误 Toast (如 timeout of 10000ms exceeded 或网络请求失败等错误)
                msg_locator = self.page.locator(Locators.MESSAGE_CONTENT)
                if msg_locator.is_visible():
                    err_msg = msg_locator.inner_text().strip()
                    if any(kw in err_msg.lower() for kw in ["exceeded", "timeout", "failed", "error"]):
                        logger.error(f"【网络或接口请求超时/失败】检测到全局错误 Toast 提示: '{err_msg}'！")
                        raise AssertionError(f"网络请求错误或生成超时: {err_msg}")

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

                # 关闭随机弹窗 (排除音乐库列表项中的删除/关闭图标)
                close_btn = self.page.locator(
                    "//div[not(ancestor::li[contains(@class, 'item')]) and not(ancestor::*[contains(@class, 'library')]) and (contains(@class, 'close') or contains(@class, 'icon-close'))]"
                ).first
                if close_btn.is_visible():
                    close_btn.click()
                    logger.debug("检测到并关闭了随机弹窗")

                cnt = task_locator.count()
                if cnt > 0:
                    item = task_locator.first
                    
                    # 记录任务的生成时间，以防后续因失败改变标题后通过时间追溯
                    if not recorded_time:
                        try:
                            time_elem = item.locator(Locators.LIBRARY_ITEM_TIME)
                            if time_elem.count() > 0:
                                recorded_time = time_elem.first.text_content().strip()
                                logger.info(f"已记录当前歌曲的生成时间: '{recorded_time}'")
                        except Exception as te:
                            logger.debug(f"尝试提取时间失败: {te}")

                    current_class = item.get_attribute("class") or ""

                    if "loading" in current_class:
                        if not found_loading:
                            logger.info(f"歌曲持续生成中 (匹配到 {cnt} 条)")
                            found_loading = True
                    else:
                        # 新 UI：改用收藏/操作按钮的出现判断生成成功
                        collect_btn = item.locator(Locators.LIBRARY_ITEM_BTN_COLLECT)
                        more_btn = item.locator(Locators.LIBRARY_ITEM_BTN_MORE)
                        if (collect_btn.count() > 0 and collect_btn.first.is_visible()) or \
                           (more_btn.count() > 0 and more_btn.first.is_visible()):
                            logger.info(f"歌曲生成完成: {title}")
                            return True
                        else:
                            logger.info("等待收藏/操作按钮渲染...")
                else:
                    # 如果未找到原标题任务，但已记录时间，则通过时间定位歌曲并检查是否失败
                    if recorded_time:
                        logger.warning(f"未能匹配到标题为 '{title}' 的歌曲，正在尝试通过记录的时间 '{recorded_time}' 进行跨项检索...")
                        all_items = self.page.locator("li.item")
                        all_count = all_items.count()
                        matched_item = None
                        
                        for i in range(all_count):
                            candidate = all_items.nth(i)
                            try:
                                candidate_time_elem = candidate.locator(Locators.LIBRARY_ITEM_TIME)
                                if candidate_time_elem.count() > 0:
                                    candidate_time = candidate_time_elem.first.text_content().strip()
                                    if candidate_time == recorded_time:
                                        matched_item = candidate
                                        break
                            except Exception as ce:
                                logger.debug(f"对比候选项时间异常: {ce}")

                        if matched_item:
                            try:
                                current_title = matched_item.locator(Locators.LIBRARY_ITEM_TITLE_SPAN).first.text_content().strip()
                            except:
                                current_title = "未知"
                            
                            logger.info(f"已成功通过时间对齐检索到歌曲 (当前标题: '{current_title}')")
                            
                            # 检测是否包含 Retry 按钮或包含失败关键字
                            retry_btn = matched_item.locator("text=Retry")
                            retry_btn_class = matched_item.locator("[class*='retry']")
                            is_retry_visible = (retry_btn.count() > 0 and retry_btn.first.is_visible()) or \
                                               (retry_btn_class.count() > 0 and retry_btn_class.first.is_visible())
                            
                            has_failed_text = "fail" in current_title.lower()
                            
                            if is_retry_visible or has_failed_text:
                                logger.error(f"【生成失败】经时间 '{recorded_time}' 对齐校对，发现目标歌曲 (当前标题: '{current_title}') 生成已失败 (显示 Retry 按钮或包含 fail 文本)！")
                                return False
                            
                            # 如果它在此期间完成了
                            collect_btn = matched_item.locator(Locators.LIBRARY_ITEM_BTN_COLLECT)
                            more_btn = matched_item.locator(Locators.LIBRARY_ITEM_BTN_MORE)
                            if (collect_btn.count() > 0 and collect_btn.first.is_visible()) or \
                               (more_btn.count() > 0 and more_btn.first.is_visible()):
                                logger.info(f"通过时间对齐发现歌曲已成功生成: '{current_title}'")
                                return True
                        else:
                            logger.warning(f"未能在列表中找到生成时间为 '{recorded_time}' 的歌曲项...")

                    if time.time() - start_time > 20:
                        logger.warning(f"尚未在列表中找到标题为 '{title}' 的任务...")

            except AssertionError as ae:
                raise ae
            except Exception as e:
                logger.debug(f"轮询中遇到异常 (可能正在刷新): {e}")

            time.sleep(10)

        logger.error(f"歌曲生成等待超时 ({timeout/1000}s)")
        return False
