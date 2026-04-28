# ==================== 全局配置 ====================
#会员账号
# LOGIN_EMAIL = "ljkjtest20260317@qq.com"
LOGIN_EMAIL = "testljkj20260428ymm@qq.com"
LOGIN_PASSWORD = "123456"

VERIFICATION_CODE = "999123" #通用验证码

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
