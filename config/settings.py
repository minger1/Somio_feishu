# ==================== 全局配置 ====================
#会员账号
LOGIN_EMAIL = "testljkj20260428ymm@qq.com"
LOGIN_PASSWORD = "123456"

#非会员账号
FREE_EMAIL = "testljkj2026free@qq.com"
FREE_PASSWORD = "123456"

VERIFICATION_CODE = "999123" #通用验证码

# Stripe 全额优惠码（配合测试使用，免费完成支付）
PROMO_CODE = "freec"

SIGNUP_PASSWORD = "123456"

# 测试数据路径
TEST_AUDIO_PATH = "data/Dial Tone in My Head.mp3"
TEST_AUDIO_PATH_2 = "data/2s音频.mp3"
TEST_AUDIO_PATH_3 = "data/Baby.mp3"
TEST_AUDIO_PATH_4 = "data/40s_audio.mp3"
TEST_IMAGE_PATH = "data/女巫.jpg"
TEST_IMAGE_PROMPT = "A magical glowing forest at night, detailed, digital art"


# ==================== 环境配置 ====================
# key: 环境名（命令行 --env 传入）
# value: 域名前缀
ENVIRONMENTS = {
    "somio": "https://somio.ai",
    "doremi": "https://doremizone.org"
}

DEFAULT_ENV = "somio"

# ==================== 页面 URL 映射 ====================
def get_language_urls(base_domain: str, env: str = DEFAULT_ENV) -> dict:
    """
    根据域名和语言返回各个页面的 URL。
    这里仅保留一个基础模板，具体路径请根据 Somio 项目需求添加。
    """
    languages = [
        "en", "de", "it", "es", "pt", "fr", "nl", "ko", "ja", "zh-cn", "zh-tw", "ro", "pl"
    ]
    
    urls = {}
    for lang in languages:
        # 英文直接使用 base_domain，其他语言拼接 /{lang}
        prefix = base_domain if lang == "en" else f"{base_domain}/{lang}"
        urls[lang] = {
            "generate_url":   f"{prefix}",
        }
        
    return urls

# 默认语言（不传 --language 时使用）
DEFAULT_LANGUAGE = "en"

# 已知核心接口捕获白名单（API 契约匹配规则）已转移至顶级目录的 data/api_patterns.txt 中独立维护管理。

# ==================== 自动化报告与契约审计开关 ====================
# 是否生成标准 Pytest HTML 测试报告，默认开启 (True)
GENERATE_HTML_REPORT = False

# 是否在执行测试用例时拦截捕获接口数据、生成 JSON 并自动执行契约对比审计，默认开启 (True)
GENERATE_API_COMPARE = False

# ==================== 价格配置 ====================
# 各套餐在 Stripe 结算页应显示的 USD 金额（用于价格正确性断言）
PRICING_CONFIG = {
    "USD": {
        # 订阅套餐 (月付)
        "SUBSCRIBE_BASIC_MONTHLY":    "9.99",
        "SUBSCRIBE_STANDARD_MONTHLY": "24.99",
        "SUBSCRIBE_PRO_MONTHLY":      "49.99",
        # 订阅套餐 (年付，Stripe 显示年总价)
        "SUBSCRIBE_BASIC_YEARLY":     "71.88",
        "SUBSCRIBE_STANDARD_YEARLY":  "239.88",
        "SUBSCRIBE_PRO_YEARLY":       "479.88",
        # 一次性套餐
        "ONETIME_LITE":     "8.99",
        "ONETIME_BASIC":    "16.99",
        "ONETIME_STANDARD": "34.99",
        "ONETIME_PRO":      "69.99",
    }
}
