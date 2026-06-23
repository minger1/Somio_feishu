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
    EMAIL_INPUT = ".modal-content input[type='text'], .modal-content input[placeholder='Email']"  # 邮箱输入框
    PASSWORD_INPUT = ".modal-content input[type='password']"  # 密码输入框
    PASSWORD_TOGGLE = ".password-icon"  # 显示/隐藏密码图标
    FORGOT_PWD_LINK = "div.forget > a"  # 忘记密码链接
    FORGOT_EMAIL_INPUT = ".modal-content input[type='text'], .modal-content input[type='email'], .modal-content input[placeholder*='mail']"  # 忘记密码邮箱输入
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
    # 价格页
    # =====================================================================

    # 分页按钮
    PRICE_PAGE_CYCLE_MONTHLY = "//div[@class='cycle-switcher']//div[1]"   #价格页面-月套餐分页按钮
    PRICE_PAGE_CYCLE_YEARLY = "//div[@class='cycle-switcher']//div[2]"   #价格页面-年套餐分页按钮
    PRICE_PAGE_CYCLE_ONETIME = "//div[@class='cycle-switcher']//div[3]"   #价格页-一次性套餐分页按钮

    # 购买入口按钮
    SUBSCRIBE_BASIC_UPGRADE_BTN = "(//div[@class='buy-btn primary'])[1]"   #订阅-BASIC-升级按钮
    SUBSCRIBE_STANDARD_UPGRADE_BTN = "(//div[@class='buy-btn primary'])[2]"   #订阅-STANDARD-升级按钮
    SUBSCRIBE_PRO_UPGRADE_BTN = "(//div[@class='buy-btn primary'])[3]"   #订阅-PRO-升级按钮

    ONE_TIME_LITE_BUY_BTN = "(//div[@class='buy-btn primary'])[1]"   #一次性-LITE-购买按钮
    ONE_TIME_BASIC_BUY_BTN = "(//div[@class='buy-btn primary'])[2]"   #一次性-BASIC-购买按钮
    ONE_TIME_STANDARD_BUY_BTN = "(//div[@class='buy-btn primary'])[3]"   #一次性-STANDARD-购买按钮
    ONE_TIME_PRO_BUY_BTN = "(//div[@class='buy-btn primary'])[4]"   #一次性-PRO-购买按钮


    # =====================================================================
    # Stripe 付款页面
    # =====================================================================

    STRIPE_EMAIL_INPUT          = "css=#email"                                          # 邮箱输入框
    STRIPE_PROMO_CODE_BTN       = "css=#promotionCode"                                  # 优惠码入口按钮
    STRIPE_PROMO_CODE_INPUT     = "css=#promotionCode"                                  # 优惠码输入框
    STRIPE_PROMO_CODE_APPLY_BTN = "css=button[class*='PromotionCodeEntry-applyButton']" # 应用优惠码
    STRIPE_PROMO_CODE_PILL      = "css=.PromotionCodeEntry-pill, .CheckoutInput--invalid" # 优惠码结果（成功/失败）
    STRIPE_PAYMENT_METHOD_HEADING = ".PaymentMethod-Heading"                            # 支付方式标题
    STRIPE_PAY_BTN              = "css=.SubmitButton"                                   # 支付按钮
    STRIPE_USD_BTN              = "xpath=//button[contains(@class, 'CurrencyOptionButton') and (contains(., 'USD') or contains(., '$'))]"
    STRIPE_CNY_BTN              = "xpath=//button[contains(@class, 'CurrencyOptionButton') and (contains(., 'CNY') or contains(., '¥'))]"
    # Stripe 价格校验
    STRIPE_CURRENCY_AMOUNT  = "span.CurrencyAmount"                      # Stripe 付款金额

    # =====================================================================
    # 侧边栏
    # =====================================================================

    # 侧边栏主导航
    TEXTAREA_INPUT = ".textarea-wrapper textarea:visible"  # 文本模式文本输入框(新 UI: .textarea-wrapper)
    NAV_CREATE = "a.link-item.music"  # 侧边栏-创建音乐
    NAV_LIBRARY = "a.link-item.library"  # 侧边栏-音乐库
    NAV_LYRICS_GENERATOR = "a.link-item.lyrics"  # 歌词生成
    NAV_EFFECT = "//a[@class='link-item effect']"  # 音效生成
    NAV_EXTEND = "a.link-item.extend"  # 音乐扩展
    NAV_REMIX = "a.link-item.remix"  # 音乐混音
    NAV_VIDEO = "a.link-item.video"  # 侧边栏-音乐视频
    NAV_LYRICS_AI = "a.link-item.lyrics_ai"  # 侧边栏-AI歌词视频
    NAV_VOCAL = "a.link-item.vocal"  # 侧边栏-人声分离
    NAV_STEM = "a.link-item.stem"  # 侧边栏-音轨分离
    NAV_DRUM = "a.link-item.drum_remover"  # 侧边栏-鼓音分离
    NAV_MID = "a.link-item.mid"  # 侧边栏-MIDI
    NAV_BPM = "a.link-item.bpm"  # 侧边栏-BPM
    NAV_PITCH = "a.link-item.pitch_changer"  # 侧边栏-变调
    NAV_REVERB = "a.link-item.slowed_and_reverb_generator"  # 侧边栏-慢速混响
    NAV_TRIMMER = "a.link-item.audio_trimmer"  # 侧边栏-音频修剪器

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

    # 生成歌词

    LYRICS_GENERATOR_ACTIVE = "li.lyrics-generator.active" # 生成歌词-侧边栏选中状态
    LYRICS_GENERATOR_CREATE_BTN = "button.btn-create" # 生成歌词-创建按钮
    LYRICS_GENERATOR_TEXTAREA = ".lyrics-generator-wrapper textarea"  # 歌词输入框
    LYRICS_GENERATOR_CLEAR_BTN = "button.btn-clear" # 生成歌词-清除输入框按钮
    LYRICS_GENERATOR_EDIT_BTN = "div.btn-edit" # 生成歌词-编辑按钮
    LYRICS_GENERATOR_COPY_BTN = "div.btn-copy" # 生成歌词-复制按钮
    LYRICS_GENERATOR_USE_LYRICS_BTN = "div[class='btn btn-create'] span" # 生成歌词-使用歌词按钮


    # 工作台 (音乐生成)
    CONTENT_TYPE_TABS = ".content-type li"  # 标签: Prompt、Lyrics、BGM、Reference(索引 1-4)
    FULLSCREEN_BTN = ".btn-fullscreen"  # 全屏按钮
    CREATE_BTN = ".create-btn"  # 立即创作按钮
    SONG_TITLE_INPUT = ".options-wrapper .input-wrapper input[type='text']"  # 歌曲名称输入框(结构定位，支持多语言)

    CONTENT_TYPE_INSTRUMENTAL = "//div[normalize-space()='Instrumental']" # 纯音乐
    CONTENT_TYPE_ACAPELLA = "//div[normalize-space()='Acapella']" # 清唱
    CONTENT_TYPE_FULL_SONG = "//div[normalize-space()='Full Song']" # 完整歌曲

    #歌曲语言选择
    LANGUAGE_SELECT = ".select-wrapper.language" # 语言选择
    LANGUAGE_ENGLISH = "div[class='options-wrapper'] li:nth-child(1)" # 语言-英语
    LANGUAGE_DEUTSCH = "div[class='options-wrapper'] li:nth-child(2)" # 语言-德语
    LANGUAGE_ESPANOL = "div[class='options-wrapper'] li:nth-child(3)" # 语言-西班牙语
    LANGUAGE_FRANCAIS = "div[class='options-wrapper'] li:nth-child(4)" # 语言-法语
    LANGUAGE_ITALIANO = "div[class='options-wrapper'] li:nth-child(5)" # 语言-意大利语
    LANGUAGE_JAPANESE = "div[class='options-wrapper'] li:nth-child(6)" # 语言-日语
    LANGUAGE_KOREAN = "div[class='options-wrapper'] li:nth-child(7)" # 语言-韩语
    LANGUAGE_NEDERLANDS = "div[class='options-wrapper'] li:nth-child(8)" # 语言-荷兰语
    LANGUAGE_POLSKI = "div[class='options-wrapper'] li:nth-child(9)" # 语言-波兰语
    LANGUAGE_PORTUGUES = "div[class='options-wrapper'] li:nth-child(10)" # 语言-葡萄牙语
    LANGUAGE_ROMANA = "div[class='options-wrapper'] li:nth-child(11)" # 语言-罗马尼亚语
    LANGUAGE_CHINESE_TRADITIONAL = "div[class='options-wrapper'] li:nth-child(12)" # 语言-繁体中文
    LANGUAGE_CHINESE_SIMPLIFIED = "div[class='options-wrapper'] li:nth-child(13)" # 语言-简体中文

    


    # 模型版本 - 新的两列下拉结构
    # 左列 provider 选择，右列对应的 model-item 列表
    MODEL_VERSION_DROPDOWN = ".model-version"  # 模型版本下拉触发器

    # Provider 切换（左列 .platform-column）
    MODEL_PROVIDER_SOMIO = ".platform-column li:nth-child(1)"   # Somio.ai provider
    MODEL_PROVIDER_GOOGLE = ".platform-column li:nth-child(2)"  # Google provider
    MODEL_PROVIDER_MINIMAX = ".platform-column li:nth-child(3)" # MINIMAX provider

    # Somio.ai 模型（右列 .model-column，选中 Somio.ai 后）
    MODEL_VERSION_V5_5 = ".model-column li.model-item:nth-child(1)"   # Somio V5.5
    MODEL_VERSION_V5 = ".model-column li.model-item:nth-child(2)"     # Somio V5
    MODEL_VERSION_V4_5_PLUS = ".model-column li.model-item:nth-child(3)"  # Somio V4.5+
    MODEL_VERSION_V4_5 = ".model-column li.model-item:nth-child(4)"   # Somio V4.5
    MODEL_VERSION_V4 = ".model-column li.model-item:nth-child(5)"     # Somio V4
    MODEL_VERSION_V3_5 = ".model-column li.model-item:nth-child(6)"   # Somio V3.5

    # Google 模型（右列 .model-column，选中 Google 后）
    MODEL_VERSION_LYRICS3 = ".model-column li.model-item:nth-child(1)"  # Lyria3 (Google)

    # MINIMAX 模型（右列 .model-column，选中 MINIMAX 后）
    MODEL_VERSION_MINIMAX_V2_6 = ".model-column li.model-item:nth-child(1)"   # Minimax V2.6
    MODEL_VERSION_MINIMAX_V2_5_PLUS = ".model-column li.model-item:nth-child(2)"  # Minimax V2.5+
    MODEL_VERSION_MINIMAX_V2_5 = ".model-column li.model-item:nth-child(3)"   # Minimax V2.5

    MODEL_VERSION_ACTIVE = ".model-column li.model-item.active"  # 当前选中的模型版本

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


    # =====================================================================
    # 音乐生成（AI MUSIC GENERATOR）
    # =====================================================================

    # 文本模式- 歌词生成窗口
    LYRICS_BACK_BTN = "//div[@class='back']" # 返回按钮
    LYRICS_CLOSE_BTN = "//div[@class='ai-dialog-content']//div[@class='close']" # 关闭按钮
    LYRICS_EDIT_BTN = "//div[contains(@class, 'ai-dialog-content')]//div[contains(@class, 'btn-edit')]" # 编辑按钮 (精准且独立于主页)
    LYRICS_CREATE_NOW_BTN = "//div[@class='btn-create']" # 创建按钮
    LYRICS_TITLE_INPUT = "//div[contains(@class, 'ai-dialog-content')]//input[@type='text']" # 标题输入框 (精准且独立于主页)
    LYRICS_CONTENT_TEXTAREA = ".custom-textarea-card .textarea-wrapper textarea:visible"  # 歌词内容输入框(切换到Lyrics Tab后可见)
    LYRICS_EDIT_UNDO_BTN = "//div[@class='undo disabled']" # 歌词编辑撤销按钮
    LYRICS_EDIT_REDO_BTN = "//div[@class='redo disabled']" # 歌词编辑重做按钮   
    LYRICS_EDIT_CANCEL_BTN = "//div[@class='cancel']" # 歌词编辑取消按钮
    LYRICS_EDIT_SAVE_BTN = "//div[contains(@class, 'ai-dialog-content')]//div[contains(@class, 'save') or @class='save']" # 歌词编辑保存按钮 (精准且独立于主页)
    LYRICS_CLEAR_BTN = "//div[@class='btn-clear']" # 清除按钮
    LYRICS_GENERATE_BTN = "//div[@class='btn-create']" # 生成按钮


    # 歌词模式
    LYRICS_AI_DIALOG_CONTENT = "//div[@class='ai-dialog-content lyrics_origin']"    #歌词模式AI分析弹窗
    LYRICS_TAB = ".content-type li:nth-child(2)" # 歌词分页标签(Lyrics)
    LYRICS_AI_ANALYSIS_FORMATTING_TAB = "//div[contains(@class, 'ai-dialog-content')]//div[contains(@class, 'tab-item')][1]"  # Lyrics Insight 弹窗内 Lyric Formatting 分页
    LYRICS_AI_ANALYSIS_REFINEMENT_TAB = "//div[contains(@class, 'ai-dialog-content')]//div[contains(@class, 'tab-item')][2]"  # Lyrics Insight 弹窗内 Lyric Refinement 分页
    LYRICS_AI_ANALYSIS_TABS = "//div[contains(@class, 'ai-dialog-content')]//div[contains(@class, 'tab-item')]"  # Lyrics Insight 弹窗内所有分页标签
    LYRICS_AI_CREATE_NOW_BTN = "//div[@class='btns']//div[@class='btn btn-advanced']" # AI分析页面 Create Now 按钮
    LYRICS_AI_ORIGINAL_VERSION_BTN = "//div[@class='btns']//div[@class='btn btn-original']//span" # AI分析页面 Original 版本按钮
    LYRICS_AI_ANALYSIS_LYRIC_REFINEMENT_TAB = "//div[contains(@class, 'ai-dialog-content')]//div[contains(@class, 'tab-item')][2]" # Lyrics Insight 弹窗 Lyric Refinement 标签
    GENNERATE_LYRICS_TIP_BTN = "//div[@class='generate-lyrics-tip']" # 生成歌词提示按钮

    # BGM 模式
    BGM_TAB = ".content-type li:nth-child(3)"  # BGM 分页标签
    BGM_CONTENT_TEXTAREA = ".textarea-wrapper textarea:visible"  # BGM 文本输入框 (与 Prompt 模式相同)


    # Reference 模式
    REFERENCE_TAB = ".content-type li:nth-child(4)"  # Reference 分页标签
    REFERENCE_LINK_INPUT = ".reference-link-input input"  # Reference 链接输入框
    REFERENCE_CONTENT_TEXTAREA = ".textarea-wrapper textarea:visible"  # Reference 文本输入框 (与 Prompt 模式相同)
    REFERENCE_AI_SHOW_MORE_BTN = "//span[@class='show-more']" # Reference Show More 按钮
    REFERENCE_AI_SHOW_MORE_BACK_BTN = "//div[@class='back']" # Reference 返回按钮
    REFERENCE_AI_SHOW_MORE_CLOSE_BTN = "//div[@class='ai-dialog-content reference']//div[@class='close']" # Reference Show More 关闭按钮
    REFERENCE_AI_VIEW_LYRICS_BTN = "//div[@class='btn-lyrics btn-lyrics-details']//span" # Reference View Lyrics 按钮
    REFERENCE_AI_CREATE_NOW_BTN = "//div[@class='btns']//div[@class='btn btn-advanced']" # Reference Create Now 按钮
    REFERENCE_AI_LOADING = "//div[@class='ai-dialog-content loading']" # Reference ai分析窗口



    # =====================================================================
    # 音效生成 (Sound Effect)
    # =====================================================================
    EFFECT_WORKBENCH_WRAPPER    = ".workbench-wrapper-content"                                # 音效生成左侧工作台容器
    EFFECT_MODEL_DROPDOWN       = "//div[@class='model-version model-version_effect']"             # 模型选择下拉框
    EFFECT_MODEL_OPTION_V5_5    = "//div[@class='model-version model-version_effect']//li[1]"                                 # 模型选项 - V5.5 PRO
    EFFECT_MODEL_OPTION_V5      = "//div[@class='model-version model-version_effect']//li[2]"      # 模型选项 - V5
    EFFECT_PROMPT_TEXTAREA      = ".workbench-wrapper-content textarea"                       # 音效描述文本输入框
    EFFECT_CLEAR_BTN            = "button.btn-clear"                                          # 清除输入框按钮
    EFFECT_ADVANCED_TOGGLE      = ".workbench-wrapper-content > div:nth-of-type(2)"           # 高级选项展开/折叠按钮 (第二部 `div` 容器)
    EFFECT_SONG_NAME_INPUT      = ".workbench-wrapper-content input >> nth=0"                 # 歌曲/音效名称输入框
    EFFECT_LOOP_SWITCH          = ".workbench-wrapper-content > div:nth-of-type(3) > div:first-child" # 无缝循环开关 (第三个 `div` 下的开关，100% 语言无关)
    EFFECT_TEMPO_INPUT          = ".workbench-wrapper-content input >> nth=1"                 # 速度(BPM)输入框
    EFFECT_KEY_DROPDOWN         = ".workbench-wrapper-content > div:nth-of-type(4)"           # 调性下拉框 (第四部 `div` 容器)
    EFFECT_KEY_OPTION           = "ul.key-list > li"                                          # 调性下拉选项
    EFFECT_CREATE_BTN           = "button.create-btn"                                         # 立即创作按钮



    # =====================================================================
    # 音乐扩展(Music Extension)
    # =====================================================================
    MUSIC_EXTENSION_UPLOAD_FILE = ".file-upload-dropzone .upload-placeholder"  # 音乐扩展上传文件点击/拖拽区
    MUSIC_EXTENSION_UPLOAD_LIBRARY = "ul.upload-type-wrapper li.library"  # 音乐扩展-从 Library 选择分页标签
    MUSIC_EXTENSION_INPUT_FILE = ".file-upload-dropzone input[type='file']"  # 隐藏的本地文件上传 input 元素
    MUSIC_EXTENSION_LIB_DIALOG = ".library-dialog-mask"  # 库选择弹窗容器
    MUSIC_EXTENSION_LIB_SELECT_BTN = ".music-list .music-item .select-btn"  # 库歌曲 Select 选择按钮
    MUSIC_EXTENSION_INSTRUMENT_SWITCH = "//div[@class='switch-wrapper']" # 音乐扩展-纯音乐开关
    MUSIC_EXTENSION_INSTRUMENT_SWITCH_ACTIVE = "//div[@class='switch-wrapper active']" # 音乐扩展-纯音乐开关-激活态
    
    #文件上传成功后，文件操作区
    MUSIC_EXTENSION_UPLOADED_STATUS_WRAPPER = "//div[@class='uploaded-status-wrapper']" # 文件上传成功后，文件操作区
    MUSIC_EXTENSION_PLAY_BTN = "//div[@class='play-btn']" # 文件上传成功后，播放按钮
    MUSIC_EXTENSION_DELETE_BTN = "//div[@class='delete-btn']" # 文件上传成功后，删除按钮
    MUSIC_EXTENSION_CUSTOM_REGION_DIVIDER_UNEXTENDED = "//div[@class='custom-region-divider_unextended']" # 文件上传成功后，自定义区域分割线
    MUSIC_EXTENSION_FROM_MINUTES = ".extend-from input >> nth=0"  # 开始扩展时间-分钟输入框
    MUSIC_EXTENSION_FROM_SECONDS = ".extend-from input >> nth=1"  # 开始扩展时间-秒钟输入框
    
    # 输入与配置
    MUSIC_EXTENSION_LYRICS_TEXTAREA = ".textarea_extend_lyrics textarea"  # 扩展歌词输入框
    MUSIC_EXTENSION_LYRICS_GENERATE_BTN = ".textarea_extend_lyrics .btn-paste"  # 扩展歌词-自动生成歌词按钮
    MUSIC_EXTENSION_STYLE_TEXTAREA = ".textarea_extend:not(.textarea_extend_lyrics) textarea"  # 扩展音乐风格/主题描述框
    MUSIC_EXTENSION_SONG_NAME_INPUT = ".song-input input"  # 歌曲名称输入框
    MUSIC_EXTENSION_CREATE_BTN = "button.create-btn"  # 立即创作按钮


    # =====================================================================
    # 音乐混音(Remix)
    # =====================================================================
    MUSIC_REMIX_MODEL_VERSION = "//div[@class='model-version']"  # 音乐混音模型版本
    MUSIC_REMIX_MODEL_VERSION_V5_5 = "//div[@class='model-version']//li[1]"  # 音乐混音模型版本V5.5 PRO
    MUSIC_REMIX_MODEL_VERSION_V5 = "//div[@class='model-version']//li[2]"  # 音乐混音模型版本V5
    MUSIC_REMIX_MODEL_VERSION_V4_5_PLUS = "//div[@class='model-version']//li[3]"  # 音乐混音模型版本V4.5+
    MUSIC_REMIX_MODEL_VERSION_V4_5 = "//div[@class='model-version']//li[4]"  # 音乐混音模型版本V4.5
    MUSIC_REMIX_UPLOAD_FILE = "div.upload-placeholder"  # 音乐混音本地上传文件
    MUSIC_REMIX_UPLOAD_LIBRARY = "li.library"  # 音乐混音从Library选择
    MUSIC_REMIX_LIBRARY_DIALOG = ".list-container"  # 音乐混音库选择弹窗容器
    MUSIC_REMIX_LIBRARY_SELECT_BTN = ".list-container button.select-btn"  # 音乐混音库选择按钮
    MUSIC_REMIX_STYLE_TEXTAREA = ".textarea_extend:not(.textarea_extend_lyrics) textarea"  # 音乐混音风格/主题描述框  
    MUSIC_REMIX_LYRIC_SWITCH = "(//div[@class='switch-wrapper'])[1]" # 音乐混音歌词开关
    MUSIC_REMIX_INSTRUMENTAL_SWITCH = "(//div[@class='switch-wrapper'])[2]"  # 音乐混音纯音乐开关
    MUSIC_REMIX_SONG_NAME_INPUT = "//input[@placeholder='Type your song name']" # 音乐混音歌曲名称输入框
    MUSIC_REMIX_MALE_VOICE = "//div[@class='advanced']//li[1]"  # 音乐混音男声
    MUSIC_REMIX_FEMALE_VOICE = "//div[@class='advanced']//li[2]"  # 音乐混音女声
    MUSIC_REMIX_RAMDON_VOICE = "//div[@class='advanced']//li[3]"  # 音乐混音随机声音
    MUSIC_REMIX_INPUT_FILE = ".file-upload-dropzone input[type='file']"  # 音乐混音本地隐藏文件 input

    MUSIC_REMIX_UPLOADED_STATUS_WRAPPER = "//div[@class='uploaded-status-wrapper']"  # 音乐混音文件上传成功操作区域
    MUSIC_REMIX_LYRICS_TEXTAREA = ".textarea_extend_lyrics textarea"  # 音乐混音歌词输入框
    MUSIC_REMIX_CREATE_BTN = "button.create-btn"  # 音乐混音创作按钮

    # =====================================================================
    # 音乐视频(Music Video)
    # =====================================================================
    MUSIC_VIDEO_UPLOAD_FILE             = "section:nth-of-type(1) .space-y-2 > div:nth-of-type(1)"  # 音乐视频本地上传文件触发区域
    MUSIC_VIDEO_UPLOAD_LIBRARY          = "section:nth-of-type(1) .space-y-2 > div:nth-of-type(2)"  # 音乐视频从Library选择触发区域
    MUSIC_VIDEO_INPUT_FILE              = "section:nth-of-type(1) input[type='file']"              # 音乐视频隐藏的音频 input 文件选择器
    
    MUSIC_VIDEO_UPLOAD_IMAGE            = "section:nth-of-type(2) .space-y-2 > div:nth-of-type(1)"  # 音乐视频上传参考图触发区域
    MUSIC_VIDEO_INPUT_IMAGE             = "section:nth-of-type(2) input[type='file']"              # 音乐视频隐藏的图片 input 选择器
    
    MUSIC_VIDEO_STYLE_TEXTAREA          = "section:nth-of-type(2) textarea"                        # 音乐视频风格/故事描述框
    
    MUSIC_VIDEO_ADVANCED_TOGGLE         = "section:nth-of-type(3) > button"                        # 音乐视频高级设置开关
    MUSIC_VIDEO_ASPECT_16_9             = "section:nth-of-type(3) div.glass:nth-of-type(1) button:nth-of-type(1)"  # 音乐视频 16:9 比例按钮
    MUSIC_VIDEO_ASPECT_9_16             = "section:nth-of-type(3) div.glass:nth-of-type(1) button:nth-of-type(2)"  # 音乐视频 9:16 比例按钮
    
    MUSIC_VIDEO_MODEL_DROPDOWN          = "section:nth-of-type(3) div.glass:nth-of-type(2) button" # 音乐视频模型版本下拉菜单触发器
    MUSIC_VIDEO_MODEL_OPTION_SEEDANCE_1_5 = "section:nth-of-type(3) div.glass:nth-of-type(2) div.absolute button:nth-of-type(1)" # 模型选项 - Seedance 1.5 Pro
    MUSIC_VIDEO_MODEL_OPTION_SEEDANCE_2_0 = "section:nth-of-type(3) div.glass:nth-of-type(2) div.absolute button:nth-of-type(2)" # 模型选项 - Seedance 2.0
    
    MUSIC_VIDEO_LIBRARY_DIALOG          = ".list-container"                                      # 音乐视频库选择弹窗容器
    MUSIC_VIDEO_LIBRARY_SELECT_BTN      = ".list-container button.select-btn"                    # 音乐视频库选择按钮
    MUSIC_VIDEO_UPLOADED_STATUS_WRAPPER = "//div[@class='uploaded-status-wrapper']"              # 音乐视频文件上传成功操作区域

    MUSIC_VIDEO_CREATE_BTN              = "div.flex.justify-center.pt-4 > button"                # 音乐视频创作/生成按钮
    

    
    MUSIC_VIDEO_CLIP_DIALOG             = "div.fixed.inset-0 > div.w-full.max-w-2xl"              # 剪辑时长弹窗容器
    MUSIC_VIDEO_CLIP_CLOSE_BTN          = "div.fixed.inset-0 > div.w-full.max-w-2xl div.p-6.border-b button"  # 剪辑时长弹窗关闭按钮
    
    # 快捷选择片段时长按钮 (Quick Select)
    MUSIC_VIDEO_CLIP_FULL_BTN           = "div.fixed.inset-0 > div.w-full.max-w-2xl div.flex.flex-wrap.gap-2 > button:nth-of-type(1)"  # 剪辑全长 (Full)
    MUSIC_VIDEO_CLIP_10S_BTN            = "div.fixed.inset-0 > div.w-full.max-w-2xl div.flex.flex-wrap.gap-2 > button:nth-of-type(2)"  # 剪辑 10s
    MUSIC_VIDEO_CLIP_30S_BTN            = "div.fixed.inset-0 > div.w-full.max-w-2xl div.flex.flex-wrap.gap-2 > button:nth-of-type(3)"  # 剪辑 30s
    MUSIC_VIDEO_CLIP_60S_BTN            = "div.fixed.inset-0 > div.w-full.max-w-2xl div.flex.flex-wrap.gap-2 > button:nth-of-type(4)"  # 剪辑 60s
    MUSIC_VIDEO_CLIP_90S_BTN            = "div.fixed.inset-0 > div.w-full.max-w-2xl div.flex.flex-wrap.gap-2 > button:nth-of-type(5)"  # 剪辑 90s
    MUSIC_VIDEO_CLIP_120S_BTN           = "div.fixed.inset-0 > div.w-full.max-w-2xl div.flex.flex-wrap.gap-2 > button:nth-of-type(6)"  # 剪辑 120s
    MUSIC_VIDEO_CLIP_180S_BTN           = "div.fixed.inset-0 > div.w-full.max-w-2xl div.flex.flex-wrap.gap-2 > button:nth-of-type(7)"  # 剪辑 180s
    
    MUSIC_VIDEO_CLIP_PLAY_BTN           = "div.fixed.inset-0 > div.w-full.max-w-2xl div.flex.items-center.gap-4.mb-4 > button" # 剪辑时长播放/暂停预览按钮
    MUSIC_VIDEO_CLIP_CANCEL_BTN         = "div.fixed.inset-0 > div.w-full.max-w-2xl div.border-t.flex.gap-3 > button:nth-of-type(1)" # 剪辑时长取消按钮
    MUSIC_VIDEO_CLIP_CONFIRM_BTN        = "div.fixed.inset-0 > div.w-full.max-w-2xl div.border-t.flex.gap-3 > button:nth-of-type(2)" # 剪辑时长确认按钮
    

    
    # =====================================================================
    # 音乐库 (Library) 
    # =====================================================================
    LIBRARY_NAV = ".link-item.library"  # 侧边栏 Library 导航

    # ---- 主分类 Tab (Songs / Videos) ----
    # 容器: .library-top-tabs ul.tab-list > li, 激活态 class="active"
    LIBRARY_TAB_SONGS   = "div.library-top-tabs ul.tab-list li:nth-child(1)"   # Songs 主 Tab
    LIBRARY_TAB_VIDEOS  = "div.library-top-tabs ul.tab-list li:nth-child(2)"   # Videos 主 Tab
    LIBRARY_TAB_ACTIVE  = "div.library-top-tabs ul.tab-list li.active"          # 当前选中的主 Tab

    # ---- 子分类 Sub Tab (Creations / Sound Effects / Extensions / Remixes ...) ----
    # 容器: .library-header ul.menu > li, 激活态 class="active"
    LIBRARY_SUB_TAB_ACTIVE     = "div.library-header ul.menu li.active"          # 当前选中的子 Tab
    LIBRARY_SUB_TAB_CREATIONS  = "div.library-header ul.menu li:nth-child(1)"    # Creations (创作)子 Tab
    LIBRARY_SUB_TAB_SOUNDS     = "div.library-header ul.menu li:nth-child(2)"    # Sound Effects (音效)子 Tab
    LIBRARY_SUB_TAB_EXTENSIONS = "div.library-header ul.menu li:nth-child(3)"    # Extensions (扩展)子 Tab
    LIBRARY_SUB_TAB_REMIXES    = "div.library-header ul.menu li:nth-child(4)"    # Remixes (混音)子 Tab

    # ---- 子过滤器 (All / Liked) ----
    # 容器: .filter-menu-select
    LIBRARY_FILTER_SELECT = ".filter-menu-select"                                # 过滤下拉框按钮
    LIBRARY_FILTER_ALL    = ".filter-menu-select ul.dropdown li.all"             # All (全部)过滤选项
    LIBRARY_FILTER_LIKED  = ".filter-menu-select ul.dropdown li.favorite"        # Liked (已赞)过滤选项
    LIBRARY_FILTER_ACTIVE = ".filter-menu-select span"                         # 当前选中子过滤展示文本

    # ---- 搜索框 ----
    LIBRARY_SEARCH_INPUT = ".search-input-wrapper input"  # 搜索框

    # ---- 歌曲列表容器 ----
    # 实际 DOM: .library-content > ul > li.item
    LIBRARY_SONG_ITEMS = ".library-content li.item"   # 每首歌的 li.item

    # ---- 单首歌曲 Item 内部相对定位 ----
    # 封面区 (.item_left > .cover)
    LIBRARY_ITEM_COVER    = ".cover"                  # 封面容器
    LIBRARY_ITEM_DURATION = ".cover .duration"        # 封面上的时长标签（生成成功标志）
    LIBRARY_ITEM_COVER_IMG = ".cover img"             # 封面图片

    # 信息区 (.info)
    LIBRARY_ITEM_TITLE    = ".info-title span.text"   # 歌曲标题
    LIBRARY_ITEM_MODEL    = ".info-title span.model"  # 模型标签 (lyria3 / V5 ...)
    LIBRARY_ITEM_TAGS     = ".info-tag li"             # 风格情绪标签
    LIBRARY_ITEM_TIME     = ".info-time"               # 生成时间
    LIBRARY_ITEM_TITLE_SPAN = ".info-title span.text" # 标题（用于按标题过滤）

    # ---- 行内操作按钮区（始终可见）----
    # 屏幕截图显示按钮为：👍 👎 ♥ 📤 …，在 item 右侧
    LIBRARY_ITEM_BTN_LIKE    = "li.like"  # 点赞
    LIBRARY_ITEM_BTN_DISLIKE = "li.dislike"                       # 踩
    LIBRARY_ITEM_BTN_COLLECT = "li.favorite"                      # 收藏
    LIBRARY_ITEM_BTN_SHARE   = "li.share"                         # 分享
    LIBRARY_ITEM_BTN_MORE    = "li.more"                          # 三点菜单

    # ---- More 菜单（点击三点后弹出）----
    # 菜单项用文本内容定位，兼容性最强
    LIBRARY_MORE_MENU            = "li.more > .more-wrapper"          # 菜单容器
    LIBRARY_MORE_EDIT_NAME       = "li.more > .more-wrapper > .more-item.edit"   # 修改歌名
    LIBRARY_MORE_DOWNLOAD        = "li.more > .more-wrapper > .more-item.download" # 下载
    LIBRARY_MORE_VOCAL           = "li.more > .more-wrapper > .more-item.vocal"    # Vocal Remover
    LIBRARY_MORE_STEM            = "li.more > .more-wrapper > .more-item.stem"     # Stem Splitter
    LIBRARY_MORE_EDIT_ORIGINAL   = "li.more > .more-wrapper > .more-item.edit-original" # 编辑原曲
    LIBRARY_MORE_FAVORITE        = "li.more > .more-wrapper > .more-item.favorite" # 收藏
    LIBRARY_MORE_SHARE           = "li.more > .more-wrapper > .more-item.external" # 外部分享
    LIBRARY_MORE_DELETE          = "li.more > .more-wrapper > .more-item.delete"   # 删除
    # 下载子菜单
    LIBRARY_MORE_DOWNLOAD_VIDEO  = ".submenu-item.mp4"   # 下载视频
    LIBRARY_MORE_DOWNLOAD_AUDIO  = ".submenu-item.mp3"   # 下载音频

    # ---- 修改歌名弹窗 ----
    LIBRARY_EDIT_NAME_DIALOG     = ".dialog-content:has(.edit-dialog)"  # 弹窗容器
    LIBRARY_EDIT_NAME_INPUT      = ".dialog-content:has(.edit-dialog) input"  # 输入框
    LIBRARY_EDIT_NAME_CANCEL_BTN = ".dialog-content:has(.edit-dialog) .cancel"   # 取消按钮
    LIBRARY_EDIT_NAME_SAVE_BTN   = ".dialog-content:has(.edit-dialog) .confirm"  # 保存按钮
    LIBRARY_EDIT_NAME_CLOSE_BTN  = ".dialog-content:has(.edit-dialog) .close"  # 关闭按钮

    # ---- 删除确认弹窗 ----
    LIBRARY_DELETE_DIALOG        = ".dialog-content:visible"  # 弹窗容器
    LIBRARY_DELETE_CANCEL_BTN    = ".dialog-content:visible .cancel"   # 取消按钮
    LIBRARY_DELETE_CONFIRM_BTN   = ".dialog-content:visible .confirm"  # 确认删除按钮
    LIBRARY_DELETE_CLOSE_BTN     = ".dialog-content:visible .close"  # 关闭按钮



    # -------------------------------------------------------------------------
    # 踩(Dislike) → 用户反馈弹窗 (User Feedback)
    # -------------------------------------------------------------------------
    DISLIKE_FEEDBACK_DIALOG    = ".feedback-dialog-card"  # 弹窗容器
    DISLIKE_FEEDBACK_CLOSE_BTN = ".feedback-dialog-card .close-icon"                # ✕ 关闭按钮
    DISLIKE_FEEDBACK_OPTION_ITEMS    = ".feedback-dialog-card .checkbox-item"   # 所有选项的集合
    DISLIKE_FEEDBACK_OPTION_1        = ".feedback-dialog-card .checkbox-item:nth-child(1)"  # 反馈选项 1
    DISLIKE_FEEDBACK_OPTION_2        = ".feedback-dialog-card .checkbox-item:nth-child(2)"  # 反馈选项 2
    DISLIKE_FEEDBACK_OPTION_3        = ".feedback-dialog-card .checkbox-item:nth-child(3)"  # 反馈选项 3
    DISLIKE_FEEDBACK_OPTION_4        = ".feedback-dialog-card .checkbox-item:nth-child(4)"  # 反馈选项 4
    DISLIKE_FEEDBACK_OPTION_5        = ".feedback-dialog-card .checkbox-item:nth-child(5)"  # 反馈选项 5
    DISLIKE_FEEDBACK_OPTION_6        = ".feedback-dialog-card .checkbox-item:nth-child(6)"  # 反馈选项 6
    DISLIKE_FEEDBACK_TEXTAREA  = ".feedback-dialog-card .feedback-textarea"                 # 反馈详细内容输入框
    DISLIKE_FEEDBACK_EMAIL     = ".feedback-dialog-card .feedback-input"                    # 反馈联系人邮箱输入框
    DISLIKE_FEEDBACK_SUBMIT    = ".feedback-dialog-card .submit-button"                     # 反馈提交按钮


    # =====================================================================
    # 感谢页 (Thank You Page) - /thanks-for-your-order/
    # =====================================================================

    THANK_YOU_PAGE         = ".thank-page"                                           # 感谢页主容器
    THANK_YOU_TITLE        = ".buy-title"                                            # 感谢标题 "Thank you for your purchase!"
    THANK_YOU_PLAN         = "p.buy-info:nth-of-type(1) .text2"                      # 已购套餐名称文本
    THANK_YOU_EMAIL        = ".buy-info:nth-of-type(2) .text2"                      # 账单邮箱文本
    THANK_YOU_PASSWORD_BOX = "#buyPsd"                                               # 密码框容器（新用户可见，旧用户隐藏）
    THANK_YOU_PASSWORD     = "#buyPsd .password"                                     # 初始密码文本（新用户专属）

    # =====================================================================
    # 公共格式选择弹窗 (Common Format Dialog)
    # =====================================================================
    COMMON_FORMAT_WINDOW = "div[class='popup downloadFormat'] div[class='wrapper']" #公共格式选择窗口

    # 选择mp3时的格式窗口定位
    COMMON_FORMAT_MP3_SELECT_MP3 = "div[class='item mp3 current'] p[class='title']" #格式选择窗口mp3选项
    COMMON_FORMAT_MP3_SELECT_WAV = "div[class='item wav'] p[class='title']" #格式选择窗口wav选项
    COMMON_FORMAT_SELECT_SAMPLE_RATE = ".select-header" #格式选择窗口-采样率选择下拉框入口
    COMMON_FORMAT_MP3_SAMPLE_RATE_44_1 = "div[class='popup downloadFormat'] li:nth-child(1)" #格式选择窗口-采样率选择44.1
    COMMON_FORMAT_MP3_SAMPLE_RATE_48 = "div[class='popup downloadFormat'] li:nth-child(2)" #格式选择窗口-采样率选择48
    COMMON_FORMAT_MP3_SAVE_BTN = ".btn.format-btn" #格式选择窗口保存按钮

    # 选择wav时的格式窗口定位
    COMMON_FORMAT_WAV_SELECT_MP3 = "div[class='item mp3'] p[class='title']" #格式选择窗口mp3选项
    COMMON_FORMAT_WAV_SELECT_WAV = "div[class='item wav current'] p[class='title']" #格式选择窗口wav选项
    COMMON_FORMAT_WAV_SAMPLE_RATE = ".selects .select-item:nth-child(1) .select-header" #格式选择窗口-采样率选择下拉框入口
    COMMON_FORMAT_WAV_SAMPLE_RATE_44_1 = "div[class='popup downloadFormat'] li:nth-child(1)" #格式选择窗口-采样率选择44.1
    COMMON_FORMAT_WAV_SAMPLE_RATE_48 = "div[class='popup downloadFormat'] li:nth-child(2)" #格式选择窗口-采样率选择48
    COMMON_FORMAT_WAV_BIT_DEPTH = ".selects .select-item:nth-child(2) .select-header" #格式选择窗口-位深度选择下拉框入口
    COMMON_FORMAT_WAV_BIT_DEPTH_16 = "div[class='popup downloadFormat'] li:nth-child(1)" #格式选择窗口-位深度选择16
    COMMON_FORMAT_WAV_BIT_DEPTH_24 = "div[class='popup downloadFormat'] li:nth-child(2)" #格式选择窗口-位深度选择24

    # =====================================================================
    # 公共音频上传组件 (Common Audio Upload Component)
    # =====================================================================
    COMMON_UPLOAD_TAB_SWITCH = ".upload-box-header-item" # "本地上传/从音乐库选择" tab切换按钮
    COMMON_UPLOAD_TAB_ACTIVE = ".upload-box-header-item.active" # 已激活的 tab切换按钮
    COMMON_UPLOAD_FILE_BTN = ".upload-btn" # 上传文件/唤起库选择按钮
    COMMON_UPLOAD_INPUT_FILE = ".upload-box-content input[type='file']" # 本地文件上传隐藏 input 元素
    COMMON_UPLOAD_FILE_INFO = ".file-info" # 上传文件信息
    COMMON_UPLOAD_REMOVE_BTN = "button[title='Remove']" # 移除已上传文件按钮
    COMMON_UPLOAD_BOX = ".upload-box-content" # 上传区域容器
    COMMON_UPLOAD_SEPARATE_BTN = ".separate-btn" # 分离/提交处理按钮
    COMMON_UPLOAD_LIBRARY_SELECT_BTN = "button.select-btn" # 音乐库列表中的选择按钮

    # =====================================================================
    # vocal remover
    # =====================================================================
    #人声分离处理结果页
    VOCAL_RESULT_BACK_BTN = "div[class='result-area'] div[class='icon']" #人声分离结果页返回按钮
    VOCAL_RESULT_FORMAT = ".format.vocal_select_format" #人声分离结果页格式按钮
    VOCAL_RESULT_DOWNLOAD_ALL_BTN = ".btn-mix.btn-download-all.vocal_download.vocal_download_all" #人声分离结果页下载全部按钮
    VOCAL_RESULT_DOWNLOAD_VOCAL_BTN = ".btn-download.vocal_download.vocal_download_voc" #人声分离结果页下载人声按钮
    VOCAL_RESULT_DOWNLOAD_INSTRUMENTAL_BTN = ".btn-download.vocal_download.vocal__download_ins" #人声分离结果页下载伴奏按钮
    VOCAL_RESULT_FORMAT_WAV_SAVE_BTN = ".btn.format-btn.vocal_select_wav" #人声分离格式选择窗口WAV保存按钮

    # =====================================================================
    # stem splitter
    # =====================================================================
    STEM_TAB_ALL = ".tab-item.active.all" #所有
    STEM_TAB_DRUMS = ".tab-item.drums" #鼓
    STEM_TAB_BASS = ".tab-item.bass" #贝斯
    STEM_TAB_PIANO = ".tab-item.piano" #钢琴
    STEM_TAB_GUITAR = ".tab-item.guitar" #吉他
    STEM_MY_MUSIC = ".my-music-wrapper" #我的音乐

    ##选择ALL进行处理
    STEM_FORMAT = ".format.stem_select_format" #格式选择
    STEM_FORMAT_WAV_SAVE_BTN = ".btn.format-btn.stem_select_wav" #分轨格式选择窗口WAV保存按钮
    
    STEM_MIX_DOWNLOAD_BTN = ".btn-mix.stem2_download" #下载按钮
    STEM_MIX_DOWNLOAD_WINDOW = ".audio-mixer" #音频调音台
    STEM_MIX_DOWNLOAD_TAP_ALL = ".mode-btn.stem2_download_tap_all" #MIX下载所有
    STEM_MIX_DOWNLOAD_STEMS = ".download-btn.stem2_download_stems" #MIX下载所有音轨

    STEM_MIX_DOWNLOAD_TAP_MIX = ".mode-btn.stem2_download_tap_mix" #MIX下载混音
    STEM_MIX_DOWNLOAD_MIX = ".download-btn.stem2_download_mix" #MIX下载混音

    STEM_ALL_VOCAL_DOWNLOAD_BTN = ".btn-download.stem_download.stem_download_voc" #下载人声
    STEM_ALL_DRUM_DOWNLOAD_BTN = ".btn-download.stem_download.stem_download_dru" #下载鼓音轨
    STEM_ALL_BASS_DOWNLOAD_BTN = ".btn-download.stem_download.stem_download_bas" #下载贝斯音轨
    STEM_ALL_PIANO_DOWNLOAD_BTN = ".btn-download.stem_download.stem_download_pia" #下载钢琴音轨
    STEM_ALL_GUITAR_DOWNLOAD_BTN = ".btn-download.stem_download.stem_download_gui" #下载吉他音轨
    STEM_ALL_OTHER_DOWNLOAD_BTN = ".btn-download.stem_download.stem_download_oth" #下载其他音轨

    # Mixer Checkboxes
    STEM_CHECKBOX_ALL = ".checkbox.stem2_download_all_select_all"
    STEM_CHECKBOX_VOCALS = ".checkbox.stem2_download_all_select_vocals"
    STEM_CHECKBOX_DRUMS = ".checkbox.stem2_download_all_select_drums"
    STEM_CHECKBOX_BASS = ".checkbox.stem2_download_all_select_bass"
    STEM_CHECKBOX_PIANO = ".checkbox.stem2_download_all_select_piano"
    STEM_CHECKBOX_GUITAR = ".checkbox.stem2_download_all_select_guitar"
    STEM_CHECKBOX_OTHER = ".checkbox.stem2_download_all_select_other"

    ##选择DRUMS进行处理
    DRUMS_DOWNLOAD_ALL = ".btn-mix.btn-download-all.stem_download.stem_download_all" #下载所有
    DRUMS_DOWNLOAD_DRUMS = ".btn-download.stem_download.stem_download_dru" #下载鼓音轨
    DRUMS_DOWNLOAD_DRUMS_NO = ".btn-download.stem_download.stem_download_dru_no" #下载非鼓音轨

    ##选择BASS进行处理
    BASS_DOWNLOAD_ALL = ".btn-mix.btn-download-all.stem_download.stem_download_all" #下载所有
    BASS_DOWNLOAD_BASS = ".btn-download.stem_download.stem_download_bas" #下载贝斯音轨
    BASS_DOWNLOAD_BASS_NO = ".btn-download.stem_download.stem_download_bas_no" #下载非贝斯音轨

    ##选择PIANO进行处理
    PIANO_DOWNLOAD_ALL = ".btn-mix.btn-download-all.stem_download.stem_download_all" #下载所有
    PIANO_DOWNLOAD_PIANO = ".btn-download.stem_download.stem_download_pia" #下载钢琴音轨
    PIANO_DOWNLOAD_PIANO_NO = ".btn-download.stem_download.stem_download_pia_no" #下载非钢琴音轨

    ##选择GUITAR进行处理
    GUITAR_DOWNLOAD_ALL = ".btn-mix.btn-download-all.stem_download.stem_download_all" #下载所有
    GUITAR_DOWNLOAD_GUITAR = ".btn-download.stem_download.stem_download_gui" #下载吉他音轨
    GUITAR_DOWNLOAD_GUITAR_NO = ".btn-download.stem_download.stem_download_gui_no" #下载非吉他音轨




    