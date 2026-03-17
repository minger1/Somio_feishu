# ==================== 全局配置 ====================
#会员账号
LOGIN_EMAIL = "ljkjtest20260317@qq.com"
LOGIN_PASSWORD = "123456"

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
    return {
        "en": {
            "base_url": f"{base_domain}/generate/",
            "upgrade_url": f"{base_domain}/pricing/music-generator/",
            
        },
        "zh-cn": {
            "base_url": f"{base_domain}/zh-cn/generate/",
            "upgrade_url": f"{base_domain}/zh-cn/pricing/music-generator/",
        }
    }

# 默认语言（不传 --language 时使用）
DEFAULT_LANGUAGE = "en"

# 初始化映射
# LANGUAGE_URLS = get_language_urls(ENVIRONMENTS[DEFAULT_ENV], DEFAULT_ENV)
