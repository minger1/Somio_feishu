class Locators:
    """
    Somio 项目的定位符管理类
    """

    # 首页
    START_CREATING_BTN = "//a[@data-handle='generate']"  # 首页开始创作按钮

    # =====================================================================
    # 登录 / 注册
    # =====================================================================

    # 登录
    LOGIN_MODAL = ".modal-content"  # 登录窗口模态框
    LOGIN_BTN = "//div[@class='btn_header']//div[@id='appLogin']"  # 右上角唤起登录按钮
    SIGNUP_BTN = "//div[@class='btn btn-register']"  # 右上角唤起注册按钮
    LOGIN_MODAL_CLOSE = ".close-btn"  # 关闭窗口按钮
    EMAIL_INPUT = "input[placeholder='Email']"  # 邮箱输入框
    PASSWORD_INPUT = "input[placeholder*='Password']"  # 密码输入框
    PASSWORD_TOGGLE = ".password-icon"  # 显示/隐藏密码图标
    FORGOT_PWD_LINK = "div.forget > a"  # 忘记密码链接
    FORGOT_EMAIL_INPUT = "input[placeholder='Please enter your registered email']"  # 忘记密码邮箱输入
    SUBMIT_BTN = "div.submit"  # 提交按钮
    SIGNUP_LINK = "div.tip > a"  # 注册链接
    MESSAGE_CONTENT = ".message-content"  # 提示消息
    COPY_SUCCESS_TOAST = "//div[contains(@class,'global-message-success')]//div[@class='message-content']"  # 复制成功 Toast

    REGISTER_EMAIL_VERIFICATION_MODAL = "//div[@class='modal-content']"   #注册邮箱验证窗口
    REGISTER_CODE_INPUT = "//input[@class='code-input active']"  #验证码输入框
    REGISTER_RESEND_BTN = "//div[@class='resend']"  #重新发送验证码按钮
    REGISTER_SUBMIT_BTN_DISABLED = "//div[@class='submit disabled']"  #注册提交按钮-不可点击态
    REGISTER_SUBMIT_BTN = "//div[@class='submit']"  #注册提交按钮-可点击态
    REGISTER_CLOSE_BTN = "//div[@class='close-btn']"  #关闭注册窗口按钮
    REGISTER_EMAIL = "//div[@class='email']"   #验证窗口显示的邮箱
    REGISTER_BACK_BTN = "//div[@class='back']"  #返回按钮


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
    NAV_CREATE = "//a[@class='link-item music']"#侧边栏-创建音乐
    NAV_LIBRARY = "//a[@class='link-item library']"  #侧边栏-音乐库
    NAV_LYRICS_GENERATOR = "//a[@class='link-item lyrics']"  # 歌词生成
    NAV_VOCAL = "//a[@class='link-item vocal']"  #侧边栏-人声
    NAV_STEM = "//a[@class='link-item stem']"  #侧边栏-音轨
    NAV_VIDEO = "//a[@class='link-item video']"  #侧边栏-音乐视频
    NAV_LYRICS_AI = "//a[@class='link-item lyrics_ai']"  #侧边栏-AI歌词视频
    NAV_BPM = "//a[@class='link-item bpm']"  #侧边栏-BPM
    NAV_MID = "//a[@class='link-item mid']"  #侧边栏-MIDI

    # =====================================================================
    # 顶部 Header 区域
    # =====================================================================

    UPGRADE_BTN = "//a[@class='nav-app-item upgrade']"  # 升级专业版按钮
    CREDIT_TOOLTIP = "//div[@class='nav-app-item credit']"  # 积分
    GIFT_BTN = "//div[@class='nav-app-item gift']"  # 礼物
    SIGNUP_HEADER_BTN = "//div[@class='btn btn-register']"  # 顶部注册按钮
    LOGIN_HEADER_BTN = "//div[@class='btn_header']//div[@id='appLogin']"  # 顶部登录按钮

    # =====================================================================
    # 设置下拉菜单 (齿轮图标)
    # =====================================================================

    SETTING_BTN          = "//div[contains(@class,'nav-app-item setting')]"  # 设置齿轮按钮
    SETTING_DROPDOWN     = "//div[contains(@class,'dropdown-menu')]"         # 设置下拉容器
    SETTING_LANGUAGE     = "//div[@class='cell has-sub']"                    # 语言切换 (带子菜单箭头)
    SETTING_INVITE       = "(//div[@class='dropdown-menu']/div[@class='cell'])[1]"  # 邀请奖励 (Invite & Earn)
    SETTING_FEEDBACK     = "(//div[@class='dropdown-menu']/div[@class='cell'])[2]"  # 反馈 (Feedback)
    SETTING_CONTACT_US   = "(//div[@class='dropdown-menu']/div[@class='cell'])[3]"  # 联系我们 (Contact Us)
    SETTING_FAQ          = "(//div[@class='dropdown-menu']/div[@class='cell'])[4]"  # FAQ
    SETTING_PRIVACY      = "(//div[@class='dropdown-menu']/div[@class='cell'])[5]"  # 隐私政策 (Privacy Policy)
    SETTING_TERMS        = "(//div[@class='dropdown-menu']/div[@class='cell'])[6]"  # 服务条款 (Terms of Service)

    # =====================================================================
    # 设置 - Feedback 弹窗
    # =====================================================================
    SETTING_FEEDBACK_MODAL        = ".feedback-dialog, [class*='feedback-dialog'], [class*='feedback-wrapper']"  # Feedback 弹窗容器
    SETTING_FEEDBACK_MODAL_CLOSE  = ".feedback-dialog .close, [class*='feedback-dialog'] .close, [class*='feedback-wrapper'] .close"  # 关闭按钮
    SETTING_FEEDBACK_OPTION_ITEMS = "[class*='feedback'] [class*='option']"   # 反馈选项列表
    SETTING_FEEDBACK_TEXTAREA     = ".feedback-textarea"                      # 详细说明文本框
    SETTING_FEEDBACK_EMAIL_INPUT  = ".feedback-input"                         # 邮箱输入框
    SETTING_FEEDBACK_SUBMIT_BTN   = ".submit-button"                          # 提交按钮

    # =====================================================================
    # 设置 - Invite & Earn 弹窗
    # =====================================================================
    SETTING_INVITE_MODAL          = ".invite-dialog, [class*='invite-dialog'], [class*='invite-wrapper']"  # Invite & Earn 弹窗容器
    SETTING_INVITE_MODAL_CLOSE    = ".invite-dialog .close, [class*='invite-dialog'] .close, [class*='invite-wrapper'] .close"  # 关闭按钮
    SETTING_INVITE_COPY_BTN       = "[class*='invite'] [class*='copy'], [class*='invite'] button"           # 复制邀请链接按钮

    # =====================================================================
    # 语言子菜单 (悬停 Language 后展开)
    # =====================================================================

    LANGUAGE_ENGLISH = "(//div[@class='sub-menu language-menu']/div[@class='cell'])[1]"  # English
    LANGUAGE_DEUTSCH = "(//div[@class='sub-menu language-menu']/div[@class='cell'])[2]"  # Deutsch
    LANGUAGE_ESPANOL = "(//div[@class='sub-menu language-menu']/div[@class='cell'])[3]"  # Español
    LANGUAGE_FRANCAIS = "(//div[@class='sub-menu language-menu']/div[@class='cell'])[4]"  # Français
    LANGUAGE_ITALIANO = "(//div[@class='sub-menu language-menu']/div[@class='cell'])[5]"  # Italiano
    LANGUAGE_JAPANESE = "(//div[@class='sub-menu language-menu']/div[@class='cell'])[6]"  # 日本語
    LANGUAGE_KOREAN = "(//div[@class='sub-menu language-menu']/div[@class='cell'])[7]"  # 한국어
    LANGUAGE_NEDERLANDS = "(//div[@class='sub-menu language-menu']/div[@class='cell'])[8]"  # Nederlands
    LANGUAGE_POLSKI = "(//div[@class='sub-menu language-menu']/div[@class='cell'])[9]"  # Polski
    LANGUAGE_PORTUGUES = "(//div[@class='sub-menu language-menu']/div[@class='cell'])[10]"  # Português
    LANGUAGE_ROMANA = "(//div[@class='sub-menu language-menu']/div[@class='cell'])[11]"  # Română
    LANGUAGE_CHINESE_TRADITIONAL = "(//div[@class='sub-menu language-menu']/div[@class='cell'])[12]"  # 繁體中文
    LANGUAGE_CHINESE_SIMPLIFIED = "(//div[@class='sub-menu language-menu']/div[@class='cell'])[13]"  # 简体中文

    # =====================================================================
    # 生成音乐 (文本模式)
    # =====================================================================

    # 工作台 (音乐生成)
    CONTENT_TYPE_TABS = ".content-type li"  # 标签: 文本、歌词、背景音乐 (索引 1-3)
    FULLSCREEN_BTN = ".btn-fullscreen"  # 全屏按钮
    CREATE_BTN = ".create-btn"  # 立即创作按钮
    SONG_TITLE_INPUT = "//div[@class='song-input']//input[@type='text']"  # 歌曲名称输入框

    # 模型版本
    # DOM 结构：.workbench-wrapper-content > .header > .model-version > ul > li（li 无 class）
    # .model-version 是触发器 div（点击展开 ul）
    # li 顺序固定：1=V5.5, 2=V5, 3=V4.5+, 4=V4.5, 5=V3.5, 6=lyria3（新增）
    MODEL_VERSION_DROPDOWN = ".workbench-wrapper-content .model-version"  # 模型版本下拉触发器
    MODEL_VERSION_V5_5 = ".workbench-wrapper-content .model-version ul li:nth-child(1)"  # V5.5
    MODEL_VERSION_V5   = ".workbench-wrapper-content .model-version ul li:nth-child(2)"  # V5
    MODEL_VERSION_V4_5_PLUS = ".workbench-wrapper-content .model-version ul li:nth-child(3)"  # V4.5+
    MODEL_VERSION_V4_5 = ".workbench-wrapper-content .model-version ul li:nth-child(4)"  # V4.5
    MODEL_VERSION_V3_5 = ".workbench-wrapper-content .model-version ul li:nth-child(5)"  # V3.5
    MODEL_VERSION_LYRIA3 = ".workbench-wrapper-content .model-version ul li:nth-child(6)"  # lyria3（新增）
    MODEL_VERSION_ACTIVE = ".workbench-wrapper-content .model-version li.active"  # 当前选中的模型版本




    # 限制弹窗 (作用域限定在 .workbench-wrapper 以防冲突)
    LIMIT_DIALOG = ".workbench-wrapper .dialog-content"  # 限制弹窗
    LIMIT_DIALOG_CLOSE = ".workbench-wrapper .close"  # 限制弹窗关闭按钮
    LIMIT_UPGRADE_BTN = ".workbench-wrapper .dialog-content .btn"  # 升级/购买按钮
    LIMIT_LOGIN_BTN = ".workbench-wrapper .btn-login"  # 登录按钮


    
    # AI 分析弹窗按钮
    AI_ANALYSIS_MODAL = "//div[@class='ai-dialog-content']" # AI分析弹窗
    AI_CREATE_NOW_BTN = "div[class='btns'] div[class='btn btn-advanced']"  # 点击创建 (AI分析后)
    AI_ORIGINAL_VERSION_BTN = "//div[@class='btns']//div[@class='btn btn-original']//span"  # 点击用原始数据生成
    AI_VIEW_LYRICS_BTN = "//div[@class='btn-lyrics']"  # 点击歌词

    # 确认弹窗(原始数据生成)
    CONFIRM_DIALOG = "//div[@class='dialog-content dialog-content_default']" # 确认弹窗
    CONFIRM_CONTINUE_BTN = "//div[@class='confirm']"  # 确认生成
    CONFIRM_CANCEL_BTN = "//div[@class='cancel']"  # 取消生成
    CONFIRM_DIALOG_CLOSE = "//div[@class='dialog-content dialog-content_default']//div[@class='close']" # 关闭弹窗

    # =====================================================================
    # 音乐库列表
    # =====================================================================
    LIBRARY_LIST = ".library-content"                        # 音乐库列表容器
    LIBRARY_FIRST_ITEM = ".library-content li:first-child"   # 列表第一项
    LIBRARY_ITEM_TITLE_SPAN = "span.text"                    # 标题 span（精准定位，避免匹配 span.model）
    LOADING_TASK = "//li[@class='item loading']"             # 生成中任务行
    LOADING = "div[@class='loading']"                        # 加载中图标
    LIBRARY_ITEM_PROGRESS = ".progress"                      # 进度条 (生成中标志)

    # 生成成功判断依据：封面时长标签出现（新 UI 下载按钮已移入三点菜单）
    LIBRARY_ITEM_DURATION = ".cover .duration"               # 封面上的时长标签（成功标志）
    LIBRARY_ITEM_COVER_IMG = ".cover img"                    # 封面图片（成功标志）

    # 操作按钮区（行右侧图标行，新 UI）
    LIBRARY_ITEM_BTN_LIKE    = ".item-operate .like"         # 点赞
    LIBRARY_ITEM_BTN_DISLIKE = ".item-operate .dislike"      # 踩
    LIBRARY_ITEM_BTN_COLLECT = ".item-operate .collect"      # 收藏
    LIBRARY_ITEM_BTN_SHARE   = ".item-operate .share"        # 分享
    LIBRARY_ITEM_BTN_MORE    = ".item-operate .more"         # 三点菜单按钮

    # 文本模式- 歌词生成窗口
    LYRICS_BACK_BTN = "//div[@class='back']" # 返回按钮
    LYRICS_CLOSE_BTN = "//div[@class='ai-dialog-content']//div[@class='close']" # 关闭按钮
    LYRICS_EDIT_BTN = "//div[@class='btn btn-edit']" # 编辑按钮
    LYRICS_CREATE_NOW_BTN = "//div[@class='btn-create']" # 创建按钮
    LYRICS_TITLE_INPUT = "(//input[@type='text'])[2]" # 标题输入框
    LYRICS_CONTENT_TEXTAREA = "//textarea[contains(@placeholder, 'Verse 1') or contains(@placeholder, 'Lyrics')]" # 歌词内容输入框
    LYRICS_EDIT_UNDO_BTN = "//div[@class='undo disabled']" # 歌词编辑撤销按钮
    LYRICS_EDIT_REDO_BTN = "//div[@class='redo disabled']" # 歌词编辑重做按钮   
    LYRICS_EDIT_CANCEL_BTN = "//div[@class='cancel']" # 歌词编辑取消按钮
    LYRICS_EDIT_SAVE_BTN = "//div[@class='tools tools_bottom']//div[@class='save']" # 歌词编辑保存按钮
    LYRICS_CLEAR_BTN = "//div[@class='btn-clear']" # 清除按钮
    LYRICS_GENERATE_BTN = "//div[@class='btn-create']" # 生成按钮


    # 歌词模式
    LYRICS_AI_DIALOG_CONTENT = "//div[@class='ai-dialog-content lyrics_origin']"    #歌词模式AI分析弹窗
    LYRICS_TAB = ".content-type li:nth-child(2)" # 歌词分页标签
    LYRICS_AI_ANALYSIS_FORMATTING_TAB = "(//div[contains(@class, 'tab-item')])[1]"  # AI分析 - Lyrics Formatting 分页 (默认第1个)
    LYRICS_AI_ANALYSIS_REFINEMENT_TAB = "(//div[contains(@class, 'tab-item')])[2]"  # AI分析 - Lyrics Refinement 分页 (第2个)
    LYRICS_AI_CREATE_NOW_BTN = "//div[@class='btns']//div[@class='btn btn-advanced']" # AI分析页面 Create Now 按钮
    LYRICS_AI_ORIGINAL_VERSION_BTN = "//div[@class='btns']//div[@class='btn btn-original']//span" # AI分析页面 Original 版本按钮
    LYRICS_AI_ANALYSIS_LYRIC_REFINEMENT_TAB = "//div[@class='tab-item'][1]" # AI分析页面 Lyric Refinement 标签
    GENNERATE_LYRICS_TIP_BTN = "//div[@class='generate-lyrics-tip']" # 生成歌词提示按钮

    # BGM 模式
    BGM_TAB = ".content-type li:nth-child(3)"  # BGM 分页标签
    BGM_CONTENT_TEXTAREA = ".textarea textarea:visible"  # BGM 文本输入框 (与文本模式相同)

    # =====================================================================
    # 音乐库 (Library)
    # =====================================================================
    LIBRARY_NAV = ".link-item.library"  # 侧边栏 Library 导航

    # 分页标签
    LIBRARY_TAB_MY_SONGS = "//li[contains(@class, 'library-tab-item') and contains(text(), 'My Songs')]"   # My Songs 标签
    LIBRARY_TAB_FAVORITES = "//li[contains(@class, 'library-tab-item') and contains(text(), 'Favorites')]"  # Favorites 标签

    # 搜索框
    LIBRARY_SEARCH_INPUT = ".library-header input[type='text']"       # 搜索框

    # 歌曲列表容器 (配合 .nth(i) 获取单行)
    LIBRARY_SONG_ITEMS = ".library-content .item"

    # ========= 单首歌曲 Item 内部相对定位 =========
    # 信息区
    LIBRARY_ITEM_COVER    = ".cover"              # 封面容器
    LIBRARY_ITEM_TITLE    = ".info-title .text"   # 歌曲标题
    LIBRARY_ITEM_MODEL    = ".info-title .model"  # 模型标签 (V3.5 / V5 ...)
    LIBRARY_ITEM_DURATION = ".cover .duration"    # 封面上的时长标签 (生成成功标志)
    LIBRARY_ITEM_TIME     = ".info-time"           # 生成时间
    LIBRARY_ITEM_TAGS     = ".info-tag li"         # 风格/情绪标签列表

    # 行内操作按钮区 (新 UI: ul.controls 下)
    LIBRARY_ITEM_BTN_LIKE    = ".controls .like"     # 点赞
    LIBRARY_ITEM_BTN_DISLIKE = ".controls .dislike"  # 踩
    LIBRARY_ITEM_BTN_COLLECT = ".controls .collect"  # 收藏 (心形)
    LIBRARY_ITEM_BTN_SHARE   = ".controls .share"    # 快捷分享
    LIBRARY_ITEM_BTN_MORE    = ".more-btn"     # 三点菜单按钮

    # More 菜单 (点击三点后弹出, 容器为 .more-wrapper)
    LIBRARY_ITEM_MORE_EDIT          = ".more-wrapper .more-item.edit"       # 修改歌名
    LIBRARY_ITEM_MORE_DOWNLOAD      = ".more-wrapper .more-item.download"   # 下载 (带子菜单)
    LIBRARY_ITEM_MORE_DOWNLOAD_VIDEO = ".more-wrapper .more-item.download .submenu-item.video"  # 下载视频 (Video)
    LIBRARY_ITEM_MORE_DOWNLOAD_AUDIO = ".more-wrapper .more-item.download .submenu-item.audio"  # 下载音频 (Audio)
    # 兼容旧命名 (MP3/WAV 已废弃，实际 UI 已变为 Video/Audio)
    LIBRARY_ITEM_MORE_DOWNLOAD_MP3  = ".more-wrapper .more-item.download .submenu-item.mp3"  # 下载 MP3 (旧 UI)
    LIBRARY_ITEM_MORE_DOWNLOAD_WAV  = ".more-wrapper .more-item.download .submenu-item.wav"  # 下载 WAV (旧 UI)
    LIBRARY_ITEM_MORE_VOCAL         = ".more-wrapper .more-item.vocal"      # Vocal Remover
    LIBRARY_ITEM_MORE_STEM          = ".more-wrapper .more-item.stem"       # Stem Splitter
    LIBRARY_ITEM_MORE_EDIT_ORIGINAL = ".more-wrapper .more-item.original"   # 编辑原曲
    LIBRARY_ITEM_MORE_FAVORITE      = ".more-wrapper .more-item.favorite"   # 加入收藏
    LIBRARY_ITEM_MORE_EXTERNAL      = ".more-wrapper .more-item.share"      # 外部分享 (带子菜单)
    LIBRARY_ITEM_MORE_DELETE        = ".more-wrapper .more-item.delete"     # 删除

    # 修改歌名弹窗
    LIBRARY_ITEM_MORE_EDIT_DIALOG      = "//div[@class='dialog-content dialog-content_default']"  # 弹窗容器
    LIBRARY_ITEM_MORE_EDIT_NAME_INPUT  = "input[placeholder='Enter song name']"                   # 输入框
    LIBRARY_ITEM_MORE_EDIT_CANCEL_BTN  = "//div[@class='cancel']"                                 # 取消按钮
    LIBRARY_ITEM_MORE_EDIT_SAVE_BTN    = "//div[@class='confirm']"                                # 保存按钮
    LIBRARY_ITEM_MORE_EDIT_CLOSE_BTN   = "//div[@class='dialog-content dialog-content_default']//div[@class='close']"  # 关闭按钮

    # 删除弹窗
    LIBRARY_ITEM_MORE_DELETE_DIALOG      = "//div[@class='dialog-content dialog-content_default']"  # 弹窗容器
    LIBRARY_ITEM_MORE_DELETE_CANCEL_BTN  = "//div[@class='cancel']"   # 取消按钮
    LIBRARY_ITEM_MORE_DELETE_CONFIRM_BTN = "//div[@class='confirm']"  # 确认删除按钮
    LIBRARY_ITEM_MORE_DELETE_CLOSE_BTN   = "//div[@class='dialog-content dialog-content_default']//div[@class='close']"  # 关闭按钮

    # -------------------------------------------------------------------------
    # 踩(Dislike) → 用户反馈弹窗 (User Feedback)
    # -------------------------------------------------------------------------
    # 弹窗容器：包含 .feedback-dialog / .feedback-wrapper 等，使用通用定位
    DISLIKE_FEEDBACK_DIALOG    = ".feedback-dialog, [class*='feedback-dialog'], [class*='feedback-wrapper']"  # 弹窗容器
    DISLIKE_FEEDBACK_CLOSE_BTN = ".feedback-dialog .close, [class*='feedback-dialog'] .close"                # ✕ 关闭按钮

    # 反馈类型单选项 (6 个，按 1-based 顺序)
    # 每个 option 容器 class 通常为 .feedback-option 或 .option-item 等
    DISLIKE_FEEDBACK_OPTION_ITEMS    = "[class*='feedback'] [class*='option']"   # 所有选项的集合
    DISLIKE_FEEDBACK_OPTION_1        = "[class*='feedback'] [class*='option']:nth-child(1)"  # Generation failed
    DISLIKE_FEEDBACK_OPTION_2        = "[class*='feedback'] [class*='option']:nth-child(2)"  # Result not as expected
    DISLIKE_FEEDBACK_OPTION_3        = "[class*='feedback'] [class*='option']:nth-child(3)"  # Add more styles and music options
    DISLIKE_FEEDBACK_OPTION_4        = "[class*='feedback'] [class*='option']:nth-child(4)"  # Need more features
    DISLIKE_FEEDBACK_OPTION_5        = "[class*='feedback'] [class*='option']:nth-child(5)"  # Price / subscription issues
    DISLIKE_FEEDBACK_OPTION_6        = "[class*='feedback'] [class*='option']:nth-child(6)"  # Others

    # 反馈详细描述输入框
    DISLIKE_FEEDBACK_TEXTAREA  = ".feedback-textarea"                   # 详细说明文本框
    # 联系邮箱输入框
    DISLIKE_FEEDBACK_EMAIL     = ".feedback-input"                      # 邮箱输入框
    # 提交按钮
    DISLIKE_FEEDBACK_SUBMIT    = ".submit-button"                       # 提交按钮






    # 生成歌词

    LYRICS_GENERATOR_ACTIVE = "li.lyrics-generator.active" # 生成歌词-侧边栏选中状态
    LYRICS_GENERATOR_CREATE_BTN = "button.btn-create" # 生成歌词-创建按钮
    LYRICS_GENERATOR_TEXTAREA = ".lyrics-generator-wrapper textarea"  # 歌词输入框
    LYRICS_GENERATOR_CLEAR_BTN = "button.btn-clear" # 生成歌词-清除输入框按钮
    LYRICS_GENERATOR_EDIT_BTN = "div.btn-edit" # 生成歌词-编辑按钮
    LYRICS_GENERATOR_COPY_BTN = "div.btn-copy" # 生成歌词-复制按钮
    LYRICS_GENERATOR_USE_LYRICS_BTN = "div[class='btn btn-create'] span" # 生成歌词-使用歌词按钮







