class Locators:
    """
    Somio 项目的定位符管理类
    """

    # =====================================================================
    # 登录 / 注册
    # =====================================================================

    # 登录
    LOGIN_MODAL = ".modal-content"  # 登录窗口模态框
    LOGIN_BTN = "#appLogin.btn_doremi"  # 右上角唤起登录按钮
    LOGIN_MODAL_CLOSE = ".close-btn"  # 关闭窗口按钮
    EMAIL_INPUT = "input[placeholder='Email']"  # 邮箱输入框
    PASSWORD_INPUT = "input[placeholder*='Password']"  # 密码输入框
    PASSWORD_TOGGLE = ".password-icon"  # 显示/隐藏密码图标
    FORGOT_PWD_LINK = "div.forget > a"  # 忘记密码链接
    FORGOT_EMAIL_INPUT = "input[placeholder='Please enter your registered email']"  # 忘记密码邮箱输入
    SUBMIT_BTN = "div.submit"  # 提交按钮
    SIGNUP_LINK = "div.tip > a"  # 注册链接
    MESSAGE_CONTENT = ".message-content"  # 提示消息

    # 登录成功后的头像
    USER_AVATAR = ".avatar"  # 登录成功后右上角头像

    # 注册窗口
    REGISTER_LOGIN_LINK = ".tip"  # 登录链接 (切换到登录)

    # 忘记密码窗口
    FORGOT_BACK_LINK = ".back"  # 返回登录链接


    # =====================================================================
    # 侧边栏
    # =====================================================================

    # 侧边栏主导航
    TEXTAREA_INPUT = ".textarea textarea:visible"  # 文本模式文本输入框
    NAV_CREATE = ".list_top .create"  # 创作音乐
    NAV_LYRICS_GENERATOR = ".list_top .lyrics-generator"  # AI歌词生成器
    NAV_LIBRARY = ".list_top .library"  # 音乐库

    # 侧边栏用户区域
    UPGRADE_BTN = ".upgrade .btn"  # 升级专业版按钮
    CREDIT_TOOLTIP = ".credit .tooltip-icon"  # 积分提示
    SHARE_BTN = ".share"  # 分享赚积分
    INVITE_BTN = ".invite"  # 邀请赚积分
    LANGUAGE_ITEMS = ".language-wrapper .language-item"  # 语言选项
    MORE_ITEMS = ".more-wrapper .more-item"  # 更多菜单项

    # =====================================================================
    # 生成音乐
    # =====================================================================

    # 工作台 (音乐生成)
    CONTENT_TYPE_TABS = ".content-type li"  # 标签: 文本、歌词、背景音乐 (索引 1-3)
    FULLSCREEN_BTN = ".btn-fullscreen"  # 全屏按钮
    CREATE_BTN = ".create-btn"  # 立即创作按钮
    SONG_TITLE_INPUT = "//div[@class='song-input']//input[@type='text']"  # 歌曲名称输入框

    # 模型版本
    MODEL_VERSION_DROPDOWN = ".model-version"  # 模型版本下拉
    MODEL_VERSION_V5 = ".model-version li:nth-child(1)"  # V5
    MODEL_VERSION_V4_5_PLUS = ".model-version li:nth-child(2)"  # V4.5+
    MODEL_VERSION_V4_5 = ".model-version li:nth-child(3)"  # V4.5
    MODEL_VERSION_V3_5 = ".model-version li:nth-child(4)"  # V3.5
    MODEL_VERSION_ACTIVE = "div[@class='model-version']//li[@class='active']"  # 当前选中的模型版本:未登录默认情况下是选择v3.5

    # 限制弹窗 (作用域限定在 .workbench-wrapper 以防冲突)
    LIMIT_DIALOG = ".workbench-wrapper .dialog-content"  # 限制弹窗
    LIMIT_DIALOG_CLOSE = ".workbench-wrapper .close"  # 限制弹窗关闭按钮
    LIMIT_UPGRADE_BTN = ".workbench-wrapper .dialog-content .btn"  # 升级/购买按钮
    LIMIT_LOGIN_BTN = ".workbench-wrapper .btn-login"  # 登录按钮


    
    # AI 分析弹窗按钮
    AI_ANALYSIS_MODAL = "//div[@class='ai-dialog-content']" # AI分析弹窗柜
    AI_CREATE_NOW_BTN = "//div[@class='btns']//div[@class='btn btn-advanced']"  # 点击创建 (AI分析后)
    AI_ORIGINAL_VERSION_BTN = "//div[@class='btns']//div[@class='btn btn-original']"  # 点击用原始数据生成 (去掉了末尾的 //span)
    AI_VIEW_LYRICS_BTN = "//div[@class='btn-lyrics']"  # 点击歌词

    # 确认弹窗(原始数据生成)
    CONFIRM_DIALOG = "//div[@class='dialog-content dialog-content_default']" # 确认弹窗
    CONFIRM_CONTINUE_BTN = "//div[@class='confirm']"  # 确认生成
    CONFIRM_CANCEL_BTN = "//div[@class='cancel']"  # 取消生成
    CONFIRM_DIALOG_CLOSE = "//div[@class='dialog-content dialog-content_default']//div[@class='close']" # 关闭弹窗

    # 音乐库列表
    LIBRARY_LIST = ".library-content" # 音乐库列表容器
    LIBRARY_FIRST_ITEM = ".library-content li:first-child"  # 列表第一项
    LIBRARY_ITEM_IMG = "img"  # 封面图 (成功标志)
    LIBRARY_ITEM_DURATION = ".duration"  # 时长 (成功标志)
    LIBRARY_ITEM_PROGRESS = ".progress"  # 进度条 (生成中标志)
    LIBRARY_ITEM_TITLE = ".title" # 标题
    LIBRARY_ITEM_GENERATING_TEXT = "text='Generating a song...'" # 生成中提示文本
    LOADING = "div[@class='loading']"  # 加载中图标
    LOADING_TASK = "//li[@class='item loading']"  # 加载中任务

    # 歌词生成器
    LYRICS_BACK_BTN = "//div[@class='back']" # 返回按钮
    LYRICS_CLOSE_BTN = "//div[@class='ai-dialog-content']//div[@class='close']" # 关闭按钮
    LYRICS_EDIT_BTN = "//div[@class='btn-edit']" # 编辑按钮
    LYRICS_CREATE_NOW_BTN = "//div[@class='btn-create']" # 创建按钮
    LYRICS_TITLE_INPUT = "(//input[@type='text'])[2]" # 标题输入框
    LYRICS_CONTENT_TEXTAREA = "//div[@class='textarea active']//textarea" # 歌词内容输入框
    LYRICS_EDIT_UNDO_BTN = "//div[@class='undo disabled']" # 歌词编辑撤销按钮
    LYRICS_EDIT_REDO_BTN = "//div[@class='redo disabled']" # 歌词编辑重做按钮   
    LYRICS_EDIT_CANCEL_BTN = "//div[@class='cancel']" # 歌词编辑取消按钮
    LYRICS_EDIT_SAVE_BTN = "//div[@class='save']" # 歌词编辑保存按钮
    LYRICS_CLEAR_BTN = "//div[@class='btn-clear']" # 清除按钮
    LYRICS_GENERATE_BTN = "//div[@class='btn-create']" # 生成按钮






















