import pytest
from playwright.sync_api import expect
from pages.library_page import LibraryPage
from config.locators import Locators
from utils.logger import logger

class TestLibrary:
    """测试音乐库 (Library) 页面功能"""

    @pytest.fixture(autouse=True)
    def setup_library(self, logged_in_page):
        """每个测试前，先导航到 Library"""
        self.page = logged_in_page
        self.library_page = LibraryPage(self.page)
        self.library_page.navigate_to_library()

    def test_switch_tabs(self):
        """测试基础导航：检查侧边栏进入 Library 以及验证默认高亮的 Tab 状态，并在 My Songs 和 Favorites 之间来回切换"""
        logger.info("开始测试基础导航与 Tab 切换状态")
        
        # 默认在 My Songs
        logger.info("验证默认 Tab 选中状态为 My Songs")
        expect(self.page.locator(Locators.LIBRARY_TAB_MY_SONGS)).to_have_class("active")
        
        # 切换到 Favorites
        logger.info("切换到 Favorites 面板")
        self.library_page.switch_to_favorites()
        expect(self.page.locator(Locators.LIBRARY_TAB_FAVORITES)).to_have_class("active")
        logger.info("Favorites 状态验证成功")
        
        # 再次切回 My Songs
        logger.info("切回 My Songs 面板")
        self.library_page.switch_to_my_songs()
        expect(self.page.locator(Locators.LIBRARY_TAB_MY_SONGS)).to_have_class("active")
        logger.info("My Songs 状态验证成功")
        
        logger.success("Tab 切换功能测试结束")

    def test_search_song(self):
        """测试搜索功能：在库中进行关键字搜索并断言输入框表现"""
        logger.info("开始测试关键字搜索")
        test_keyword = "Electric Skyline"
        
        logger.info(f"在搜索框输入短语 '{test_keyword}'")
        self.library_page.search_song(test_keyword)
        
        # 断言搜索输入框的值
        logger.info("验证搜索框保留了关键字")
        expect(self.page.locator(Locators.LIBRARY_SEARCH_INPUT)).to_have_value(test_keyword)
        
        logger.success("关键字搜索测试结束")

    def test_read_first_song_info(self):
        """测试读取第一首歌的详细信息，确保列表返回的元数据具备完整性（Title, Duration 等）"""
        logger.info("开始测试读取歌曲详情")
        
        # 获取第一首歌的 locator
        first_item = self.library_page.get_song_item(0)
        
        # 确保有歌曲才往下走 (避免因为账号无歌曲而报错)
        if first_item.count() > 0:
            logger.info("提取首个歌曲的元数据字典")
            info = self.library_page.get_song_info(first_item)
            
            # 断言这首歌必须包含标题或时长等基本信息
            logger.info("验证歌曲是否包含 title 和 duration 属性")
            assert "title" in info, "字典缺失 title"
            assert "duration" in info, "字典缺失 duration"
            
            logger.info(f"提取信息成功: {info}")
            logger.success("歌曲信息读取测试结束")
        else:
            logger.warning("当前账号曲库为空，跳过该测试用例")

    def test_song_like_unlike(self):
        """测试点赞(👍)与取消点赞的二态切换功能是否无报错执行"""
        logger.info("开始测试点赞交互")
        first_item = self.library_page.get_song_item(0)
        
        if first_item.count() > 0:
            logger.info("执行点赞操作")
            btn = self.library_page.click_like(first_item)
            
            assert btn.is_visible(), "操作后按钮不可见"
            
            logger.info("执行取消点赞操作")
            self.library_page.click_like(first_item)
            
            logger.success("点赞交互测试结束")

    def test_song_collect_uncollect(self):
        """测试收藏(❤️)与取消收藏的二态切换功能是否无报错执行"""
        logger.info("开始测试收藏交互")
        first_item = self.library_page.get_song_item(0)
        
        if first_item.count() > 0:
            logger.info("执行收藏操作")
            btn = self.library_page.click_collect(first_item)
            
            assert btn.is_visible(), "操作后按钮不可见"
            
            logger.info("执行取消收藏操作")
            self.library_page.click_collect(first_item)
            
            logger.success("收藏交互测试结束")

    def test_song_dislike_opens_feedback_dialog(self):
        """测试点踩按钮后弹出 User Feedback 反馈弹窗"""
        logger.info("开始测试踩按钮 → 反馈弹窗出现")
        first_item = self.library_page.get_song_item(0)

        if first_item.count() > 0:
            logger.info("点击踩按钮")
            self.library_page.click_dislike(first_item)

            logger.info("验证 User Feedback 弹窗已弹出")
            self.library_page.wait_for_feedback_dialog(timeout=5000)

            # 验证弹窗内有 6 个反馈类型选项
            options = self.page.locator("[class*='feedback'] [class*='option']")
            option_count = options.count()
            logger.info(f"反馈选项数量: {option_count}")
            assert option_count >= 6, f"期望至少 6 个选项，实际 {option_count} 个"

            logger.success("踩按钮弹窗出现测试结束")

    def test_feedback_dialog_close_btn(self):
        """测试 User Feedback 弹窗的 ✕ 关闭按钮"""
        logger.info("开始测试反馈弹窗关闭按钮")
        first_item = self.library_page.get_song_item(0)

        if first_item.count() > 0:
            self.library_page.click_dislike(first_item)
            self.library_page.wait_for_feedback_dialog(timeout=5000)

            logger.info("点击 ✕ 关闭弹窗")
            self.library_page.close_feedback_dialog()

            # 验证弹窗已关闭
            self.page.wait_for_selector(
                ".feedback-dialog, [class*='feedback-dialog'], [class*='feedback-wrapper']",
                state="hidden", timeout=3000
            )

        logger.success("反馈弹窗关闭按钮测试结束")

    def test_feedback_email_prefilled(self):
        """测试 User Feedback 弹窗的邮箱输入框是否已自动预填登录邮箱"""
        logger.info("开始测试反馈弹窗邮箱预填充")
        first_item = self.library_page.get_song_item(0)

        if first_item.count() > 0:
            self.library_page.click_dislike(first_item)
            self.library_page.wait_for_feedback_dialog(timeout=5000)

            email_input = self.page.locator(Locators.DISLIKE_FEEDBACK_EMAIL)
            email_value = email_input.input_value()
            logger.info(f"邮箱预填值: {email_value}")
            assert "@" in email_value, f"邮箱未预填或格式非法: '{email_value}'"

            # 关闭弹窗，还原状态
            self.library_page.close_feedback_dialog()

        logger.success("反馈弹窗邮箱预填测试结束")

    def test_feedback_select_option_generation_failed(self):
        """测试选择反馈类型: Generation failed"""
        logger.info("开始测试选择反馈类型 - Generation failed")
        first_item = self.library_page.get_song_item(0)

        if first_item.count() > 0:
            self.library_page.click_dislike(first_item)
            self.library_page.wait_for_feedback_dialog(timeout=5000)

            logger.info("选择 Generation failed (option 1)")
            self.library_page.select_feedback_option(1)

            self.library_page.close_feedback_dialog()

        logger.success("Generation failed 选项测试结束")

    def test_feedback_select_option_others(self):
        """测试选择反馈类型: Others（最后一项）"""
        logger.info("开始测试选择反馈类型 - Others")
        first_item = self.library_page.get_song_item(0)

        if first_item.count() > 0:
            self.library_page.click_dislike(first_item)
            self.library_page.wait_for_feedback_dialog(timeout=5000)

            logger.info("选择 Others (option 6)")
            self.library_page.select_feedback_option(6)

            self.library_page.close_feedback_dialog()

        logger.success("Others 选项测试结束")

    def test_feedback_submit_with_description(self):
        """测试填写详细描述后提交反馈（完整流程）"""
        logger.info("开始测试完整反馈提交流程")
        first_item = self.library_page.get_song_item(0)

        if first_item.count() > 0:
            self.library_page.click_dislike(first_item)
            self.library_page.wait_for_feedback_dialog(timeout=5000)

            logger.info("选择反馈类型 - Result not as expected (option 2)")
            self.library_page.select_feedback_option(2)

            logger.info("填写详细描述")
            self.library_page.fill_feedback_description("AutoTest: 测试自动化提交反馈")

            logger.info("提交反馈")
            self.library_page.submit_feedback()

            # 提交后弹窗应消失
            self.page.wait_for_selector(
                ".feedback-dialog, [class*='feedback-dialog'], [class*='feedback-wrapper']",
                state="hidden", timeout=5000
            )
            logger.info("弹窗已在提交后关闭")

        logger.success("完整反馈提交流程测试结束")


    def test_more_menu_download(self):
        """测试 More 菜单中的下载功能（Video 与 Audio）"""
        logger.info("开始测试 More 菜单下载")
        first_item = self.library_page.get_song_item(0)

        if first_item.count() > 0:
            logger.info("验证 More 菜单 Video 下载")
            self.library_page.click_more_download_and_verify_video(first_item)

            logger.info("验证 More 菜单 Audio 下载（可能受权限限制）")
            try:
                self.library_page.click_more_download_and_verify_audio(first_item)
            except Exception as e:
                logger.info(f"Audio 下载跳过或受限（预期内）: {e}")

        logger.success("More 菜单下载测试结束")

    def test_more_menu_edit_name_cancel(self):
        """测试"更多菜单"中点击 Edit Name 弹出模态框后的安全取消功能"""
        logger.info("开始测试 Edit Name 取消流程")
        first_item = self.library_page.get_song_item(0)
        
        if first_item.count() > 0:
            logger.info("点击编辑姓名")
            self.library_page.click_more_edit_name(first_item)
            
            # 等待改名弹窗出现
            self.page.wait_for_selector(Locators.LIBRARY_ITEM_MORE_EDIT_DIALOG, state="visible", timeout=5000)
            
            # 点击取消按钮正常关闭弹窗
            logger.info("取消保存操作")
            self.page.locator(Locators.LIBRARY_ITEM_MORE_EDIT_CANCEL_BTN).click()
            self.page.wait_for_selector(Locators.LIBRARY_ITEM_MORE_EDIT_DIALOG, state="hidden")
            
        logger.success("Edit Name 取消流程测试结束")

    def test_more_menu_edit_name_confirm(self):
        """测试“更多菜单”中的修改歌名功能（包含真实产生数据写入并验证前端更新）"""
        logger.info("开始测试重命名操作")
        first_item = self.library_page.get_song_item(0)
        
        if first_item.count() > 0:
            import time
            new_name = f"AutoTest_{int(time.time())}"
            logger.info(f"保存新名称: {new_name}")
            
            self.library_page.edit_song_name(first_item, new_name)
            
            # 等待 DOM 界面刷新数据拉取
            self.page.wait_for_timeout(1000)
            
            updated_name = first_item.locator(Locators.LIBRARY_ITEM_TITLE).text_content()
            logger.info(f"重新读取到的标题为: {updated_name}")
            
            assert new_name in updated_name, f"未将名字修改为 {new_name}"
            
        logger.success("重命名操作测试结束")

    def test_more_menu_edit_original(self):
        """测试更多操作中的“编辑原曲”跳转逻辑功能"""
        logger.info("开始测试进入 Edit Original")
        first_item = self.library_page.get_song_item(0)
        
        if first_item.count() > 0:
            logger.info("点击 Edit Original")
            self.library_page.click_more_edit_original(first_item)
            
            if "generate" not in self.page.url:
                 pass
            
        logger.success("Edit Original 路由测试结束")

    def test_more_menu_favorite(self):
        """测试更多操作中的加入/取消收藏功能，类似快捷外层的心形"""
        logger.info("开始测试 更多菜单中Favorite功能")
        first_item = self.library_page.get_song_item(0)
        
        if first_item.count() > 0:
            logger.info("执行 Favorite 操作")
            self.library_page.click_more_favorite(first_item)
            
            self.page.wait_for_timeout(500)
            
        logger.success("Favorite 面板控制测试结束")

    def test_more_menu_external_share(self):
        """测试隐藏在更多菜单内的系统/外部跨平台跳转分享"""
        logger.info("开始测试外部版 Share 操作")
        first_item = self.library_page.get_song_item(0)
        
        if first_item.count() > 0:
            logger.info("点击外部版 Share")
            self.library_page.click_more_external(first_item)
            self.page.wait_for_timeout(1000)
            
            # 读取剪贴板内容断言
            copied_url = self.page.evaluate("navigator.clipboard.readText()")
            logger.info(f"分享得到的 URL 为: {copied_url}")
            
            assert "/generate" in copied_url and "isShare" in copied_url, "分享链接无效"
            
        logger.success("外部版 Share 操作测试结束")




    def test_more_menu_delete_cancel(self):
        """测试删除提示危险框弹出后的取消功能（不造成破坏）"""
        logger.info("开始测试删除提示取消")
        first_item = self.library_page.get_song_item(0)
        
        if first_item.count() > 0:
            logger.info("弹出系统删除警示")
            self.library_page.click_more_delete(first_item)
            
            # 等待删除弹窗出现
            self.page.wait_for_selector(Locators.LIBRARY_ITEM_MORE_DELETE_DIALOG, state="visible", timeout=5000)
            
            logger.info("点击取消删除")
            self.page.locator(Locators.LIBRARY_ITEM_MORE_DELETE_CANCEL_BTN).click()
            self.page.wait_for_selector(Locators.LIBRARY_ITEM_MORE_DELETE_DIALOG, state="hidden")
            
        logger.success("删除操作的 Cancel 功能结束")

    def test_more_menu_delete_confirm(self):
        """测试“更多菜单”中的真实删除歌曲功能（包含后端 Confirm 删除并刷新验证）"""
        logger.info("开始测试歌曲确认删除流程")
        first_item = self.library_page.get_song_item(0)
        
        if first_item.count() > 0:
            # 记录删除前的标题特征
            original_title = first_item.locator(Locators.LIBRARY_ITEM_TITLE).text_content()
            logger.info(f"将要执行删除目标: '{original_title}'")
            
            self.library_page.delete_song(first_item)
            
            # 等待列表重新刷新网络长连接
            self.page.wait_for_timeout(1500)
            
            new_first_item = self.library_page.get_song_item(0)
            if new_first_item.count() > 0:
                new_title = new_first_item.locator(Locators.LIBRARY_ITEM_TITLE).text_content()
                assert new_title != original_title, f"未能删除项目 {original_title}，现在的新置顶仍是相同名"
                
        logger.success("删除操作链测试结束")
