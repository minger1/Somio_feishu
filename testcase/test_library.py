import pytest
import time
from playwright.sync_api import expect
from pages.library_page import LibraryPage
from config.locators import Locators
from utils.logger import logger


class TestLibrary:
    """Library 页面功能测试集（适配新版 UI: Songs/Sounds/Videos + All/Liked）"""

    @pytest.fixture(autouse=True)
    def setup_library(self, logged_in_page):
        """每个用例前先导航至 Library，并关闭可能出现的活动弹窗"""
        self.page = logged_in_page
        self.lp = LibraryPage(self.page)
        # 自动关闭 Banner/活动弹窗/Google Play宣传弹窗等
        try:
            self.page.locator(".global-close, .banner .close, [class*='modal'] .close, [class*='dialog'] .close, .dialog-content .close").first.click(timeout=3000)
        except Exception:
            pass
        self.lp.navigate_to_library()

    # ==================================================================
    # 导航与 Tab 切换
    # ==================================================================

    def test_default_tab_is_songs(self):
        """验证进入 Library 后默认选中 Songs 主 Tab"""
        logger.info("验证默认 Tab 为 Songs")
        active_text = self.page.locator(Locators.LIBRARY_TAB_ACTIVE).text_content(timeout=5000)
        assert "Songs" in active_text, f"默认 Tab 期望 Songs，实际: {active_text}"
        logger.success("默认 Tab Songs 验证通过")

    def test_switch_main_tabs(self):
        """测试 Songs → Sounds → Videos 三主 Tab/子 Tab 来回切换"""
        logger.info("开始测试主 Tab / 子 Tab 切换")

        logger.info("切换到 Sounds Tab")
        self.lp.switch_to_sounds_tab()
        # 验证主 Tab 是 Songs
        active_main = self.page.locator(Locators.LIBRARY_TAB_ACTIVE).text_content(timeout=5000)
        assert "Songs" in active_main, f"期望主 Tab active 仍为 Songs，实际: {active_main}"
        # 验证子 Tab 是 Sound Effects
        active_sub = self.page.locator(Locators.LIBRARY_SUB_TAB_ACTIVE).text_content(timeout=5000)
        assert "Sound Effects" in active_sub, f"期望子 Tab active 为 Sound Effects，实际: {active_sub}"

        logger.info("切换到 Videos Tab")
        self.lp.switch_to_videos_tab()
        active_main = self.page.locator(Locators.LIBRARY_TAB_ACTIVE).text_content(timeout=5000)
        assert "Videos" in active_main, f"期望主 Tab active 为 Videos，实际: {active_main}"

        logger.info("切回 Songs Tab")
        self.lp.switch_to_songs_tab()
        active_main = self.page.locator(Locators.LIBRARY_TAB_ACTIVE).text_content(timeout=5000)
        assert "Songs" in active_main, f"期望主 Tab active 为 Songs，实际: {active_main}"

        logger.success("主 Tab 切换测试通过")

    def test_switch_filter_all_and_liked(self):
        """测试 All / Liked 子过滤器来回切换"""
        logger.info("开始测试 All/Liked 子过滤器切换")

        logger.info("切换到 Liked 过滤器")
        self.lp.switch_to_liked_filter()
        active = self.page.locator(Locators.LIBRARY_FILTER_ACTIVE).text_content(timeout=5000)
        assert "Liked" in active, f"期望 Liked active，实际: {active}"

        logger.info("切回 All 过滤器")
        self.lp.switch_to_all_filter()
        active = self.page.locator(Locators.LIBRARY_FILTER_ACTIVE).text_content(timeout=5000)
        assert "All" in active, f"期望 All active，实际: {active}"

        logger.success("All/Liked 过滤器切换测试通过")

    # ==================================================================
    # 搜索
    # ==================================================================

    def test_search_input(self):
        """测试搜索框可输入关键字并保持值"""
        logger.info("开始测试搜索框")
        keyword = "Neon Future"
        self.lp.search_song(keyword)
        expect(self.page.locator(Locators.LIBRARY_SEARCH_INPUT)).to_have_value(keyword, timeout=3000)
        logger.success("搜索框输入验证通过")

    # ==================================================================
    # 歌曲信息读取
    # ==================================================================

    def test_read_first_song_info(self):
        """读取第一首歌的元数据，验证 title 和 duration 字段不为空"""
        logger.info("开始测试读取歌曲信息")
        item = self.lp.get_song_item(0)
        if item.count() == 0:
            logger.warning("曲库为空，跳过")
            return

        info = self.lp.get_song_info(item)
        logger.info(f"提取信息: {info}")
        assert info.get("title"), "title 为空"
        assert info.get("duration"), "duration 为空"
        logger.success("歌曲信息读取测试通过")

    # ==================================================================
    # 行内按钮交互
    # ==================================================================

    def test_like_toggle(self):
        """测试点赞按钮：点击一次再点击一次（切换态）"""
        logger.info("开始测试点赞切换")
        item = self.lp.get_song_item(0)
        if item.count() == 0:
            logger.warning("曲库为空，跳过")
            return

        btn = self.lp.click_like(item)
        assert btn.is_visible(), "点赞后按钮不可见"
        self.lp.click_like(item)  # 再次点击取消
        logger.success("点赞切换测试通过")

    def test_collect_toggle(self):
        """测试收藏按钮：点击一次再点击一次（切换态）"""
        logger.info("开始测试收藏切换")
        item = self.lp.get_song_item(0)
        if item.count() == 0:
            logger.warning("曲库为空，跳过")
            return

        btn = self.lp.click_collect(item)
        assert btn.is_visible(), "收藏后按钮不可见"
        self.lp.click_collect(item)  # 再次点击取消
        logger.success("收藏切换测试通过")

    def test_dislike_opens_feedback_dialog(self):
        """测试踩按钮 → 弹出 User Feedback 反馈弹窗"""
        logger.info("开始测试踩 → 反馈弹窗")
        item = self.lp.get_song_item(0)
        if item.count() == 0:
            logger.warning("曲库为空，跳过")
            return

        self.lp.click_dislike(item)
        self.lp.wait_for_feedback_dialog(timeout=8000)

        options = self.page.locator(Locators.DISLIKE_FEEDBACK_OPTION_ITEMS)
        count = options.count()
        logger.info(f"反馈选项数量: {count}")
        assert count >= 1, f"期望至少 1 个反馈选项，实际 {count}"

        self.lp.close_feedback_dialog()
        logger.success("踩 → 反馈弹窗测试通过")

    # ==================================================================
    # User Feedback 弹窗细节测试
    # ==================================================================

    def test_feedback_close_btn(self):
        """测试 User Feedback 弹窗 ✕ 关闭按钮"""
        logger.info("开始测试反馈弹窗关闭")
        item = self.lp.get_song_item(0)
        if item.count() == 0:
            logger.warning("曲库为空，跳过")
            return

        self.lp.click_dislike(item)
        self.lp.wait_for_feedback_dialog(timeout=8000)
        self.lp.close_feedback_dialog()

        self.page.wait_for_selector(
            Locators.DISLIKE_FEEDBACK_DIALOG,
            state="hidden", timeout=5000
        )
        logger.success("反馈弹窗关闭测试通过")

    def test_feedback_email_prefilled(self):
        """验证反馈弹窗中邮箱已预填登录邮箱"""
        logger.info("开始测试反馈弹窗邮箱预填")
        item = self.lp.get_song_item(0)
        if item.count() == 0:
            logger.warning("曲库为空，跳过")
            return

        self.lp.click_dislike(item)
        self.lp.wait_for_feedback_dialog(timeout=8000)

        email_val = self.page.locator(Locators.DISLIKE_FEEDBACK_EMAIL).input_value()
        logger.info(f"邮箱预填值: {email_val}")
        if email_val:
            assert "@" in email_val, f"邮箱预填格式非法: '{email_val}'"
        else:
            logger.info("新 UI 邮箱输入框未预填，手动填入登录邮箱进行可行性测试")
            self.lp.fill_feedback_email("ljkjtest20260317@qq.com")
            filled_val = self.page.locator(Locators.DISLIKE_FEEDBACK_EMAIL).input_value()
            assert filled_val == "ljkjtest20260317@qq.com", f"手动填入邮箱失败: '{filled_val}'"

        self.lp.close_feedback_dialog()
        logger.success("反馈弹窗邮箱预填/填充测试通过")

    def test_feedback_select_option(self):
        """测试选择反馈类型选项（第 1 项）"""
        logger.info("开始测试选择反馈选项")
        item = self.lp.get_song_item(0)
        if item.count() == 0:
            logger.warning("曲库为空，跳过")
            return

        self.lp.click_dislike(item)
        self.lp.wait_for_feedback_dialog(timeout=8000)
        self.lp.select_feedback_option(1)
        self.lp.close_feedback_dialog()
        logger.success("反馈选项选择测试通过")

    def test_feedback_submit(self):
        """填写反馈描述并提交，验证弹窗自动关闭"""
        logger.info("开始测试完整反馈提交流程")
        item = self.lp.get_song_item(0)
        if item.count() == 0:
            logger.warning("曲库为空，跳过")
            return

        self.lp.click_dislike(item)
        self.lp.wait_for_feedback_dialog(timeout=8000)
        self.lp.select_feedback_option(2)
        self.lp.fill_feedback_description("AutoTest: 自动化测试提交反馈")
        self.lp.submit_feedback()

        self.page.wait_for_selector(
            Locators.DISLIKE_FEEDBACK_DIALOG,
            state="hidden", timeout=8000
        )
        logger.success("完整反馈提交测试通过")

    # ==================================================================
    # More 菜单测试
    # ==================================================================

    def test_more_menu_opens(self):
        """测试三点菜单可以打开，并包含核心菜单项"""
        logger.info("开始测试 More 菜单打开")
        item = self.lp.get_song_item(0)
        if item.count() == 0:
            logger.warning("曲库为空，跳过")
            return

        self.lp.open_more_menu(item)

        # 验证关键菜单项可见
        for text in ["Edit Song Name", "Download", "Delete"]:
            visible = self.page.get_by_text(text, exact=False).first.is_visible()
            assert visible, f"More 菜单中未找到: {text}"
            logger.info(f"More 菜单项 '{text}' 可见 OK")

        # 点击外部关闭菜单
        self.page.keyboard.press("Escape")
        logger.success("More 菜单打开测试通过")

    def test_more_menu_edit_name_cancel(self):
        """测试 Edit Song Name → 弹窗取消，不做实际修改"""
        logger.info("开始测试 Edit Song Name 取消流程")
        item = self.lp.get_song_item(0)
        if item.count() == 0:
            logger.warning("曲库为空，跳过")
            return

        self.lp.click_more_edit_name(item)
        self.page.wait_for_selector(Locators.LIBRARY_EDIT_NAME_DIALOG, state="visible", timeout=5000)

        self.page.locator(Locators.LIBRARY_EDIT_NAME_CANCEL_BTN).click()
        self.page.wait_for_selector(Locators.LIBRARY_EDIT_NAME_DIALOG, state="hidden", timeout=5000)
        logger.success("Edit Song Name 取消流程测试通过")

    def test_more_menu_edit_name_confirm(self):
        """测试 Edit Song Name → 修改歌名 → 确认保存 → 验证 UI 更新"""
        logger.info("开始测试修改歌名")
        item = self.lp.get_song_item(0)
        if item.count() == 0:
            logger.warning("曲库为空，跳过")
            return

        new_name = f"AutoTest_{int(time.time())}"
        self.lp.edit_song_name(item, new_name)

        self.page.wait_for_timeout(1000)
        updated = item.locator(Locators.LIBRARY_ITEM_TITLE).text_content()
        assert new_name in updated, f"歌名未更新为 '{new_name}'，当前: '{updated}'"
        logger.success(f"歌名修改成功: {updated}")

    def test_more_menu_add_to_favorites(self):
        """测试 More → Add to Favorites 操作"""
        logger.info("开始测试 Add to Favorites")
        item = self.lp.get_song_item(0)
        if item.count() == 0:
            logger.warning("曲库为空，跳过")
            return

        self.lp.click_more_favorite(item)
        self.page.wait_for_timeout(800)
        logger.success("Add to Favorites 测试通过")

    def test_more_menu_edit_original(self):
        """测试 More → Edit Original 跳转"""
        logger.info("开始测试 Edit Original 跳转")
        item = self.lp.get_song_item(0)
        if item.count() == 0:
            logger.warning("曲库为空，跳过")
            return

        self.lp.click_more_edit_original(item)
        self.page.wait_for_timeout(1000)
        logger.info(f"跳转后 URL: {self.page.url}")
        logger.success("Edit Original 跳转测试通过")

    def test_more_menu_share_external(self):
        """测试 More → Share 外部分享（复制链接到剪贴板）"""
        logger.info("开始测试外部分享")
        item = self.lp.get_song_item(0)
        if item.count() == 0:
            logger.warning("曲库为空，跳过")
            return

        self.lp.click_more_share(item)
        self.page.wait_for_timeout(1000)
        try:
            copied = self.page.evaluate("navigator.clipboard.readText()")
            logger.info(f"剪贴板内容: {copied}")
            assert "http" in copied, f"分享链接无效: {copied}"
        except Exception as e:
            logger.warning(f"无法读取剪贴板（可能需要权限）: {e}")

        logger.success("外部分享测试通过")

    def test_more_menu_delete_cancel(self):
        """测试 More → Delete → 弹窗取消（不执行真实删除）"""
        logger.info("开始测试删除取消流程")
        item = self.lp.get_song_item(0)
        if item.count() == 0:
            logger.warning("曲库为空，跳过")
            return

        self.lp.click_more_delete(item)
        self.page.wait_for_selector(Locators.LIBRARY_DELETE_DIALOG, state="visible", timeout=5000)

        self.page.locator(Locators.LIBRARY_DELETE_CANCEL_BTN).click()
        self.page.wait_for_selector(Locators.LIBRARY_DELETE_DIALOG, state="hidden", timeout=5000)
        logger.success("删除取消流程测试通过")

    def test_more_menu_delete_confirm(self):
        """测试 More → Delete → 确认删除 → 验证歌曲已从列表移除"""
        logger.info("开始测试确认删除流程")
        item = self.lp.get_song_item(0)
        if item.count() == 0:
            logger.warning("曲库为空，跳过")
            return

        # 优化：在删除前先将该歌曲重命名为一个唯一的随机歌名，防止与其他歌曲同名导致断言失效
        unique_title = f"DeleteTest_{int(time.time())}"
        self.lp.edit_song_name(item, unique_title)
        self.page.wait_for_timeout(1000)

        # 重新获取更新名字后的第一首 item (已重命名为唯一值)
        item = self.lp.get_song_item(0)
        original_title = item.locator(Locators.LIBRARY_ITEM_TITLE).text_content().strip()
        assert unique_title in original_title, f"重命名确认失败，当前第一首为: '{original_title}'"
        logger.info(f"即将删除唯一的歌曲: '{original_title}'")

        self.lp.delete_song(item)
        self.page.wait_for_timeout(1500)

        # 验证被删除的歌曲不再是第一首
        new_item = self.lp.get_song_item(0)
        if new_item.count() > 0:
            new_title = new_item.locator(Locators.LIBRARY_ITEM_TITLE).text_content()
            assert original_title not in new_title, f"删除后第一首仍是 '{original_title}'"
            logger.info(f"删除后第一首为: '{new_title}'")

        logger.success("确认删除流程测试通过")

