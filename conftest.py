import pytest
import os
import subprocess
import time
from playwright.sync_api import sync_playwright, expect
from playwright_stealth import Stealth
from config.settings import ENVIRONMENTS, DEFAULT_ENV, DEFAULT_LANGUAGE, LOGIN_EMAIL, LOGIN_PASSWORD, get_language_urls
from utils import logger
from config.locators import Locators
from pages.login_page import LoginPage

# 支持的浏览器引擎
SUPPORTED_BROWSERS = ["chromium", "firefox", "webkit", "msedge"]
DEFAULT_BROWSER = "chromium"

# ==================== 命令行参数注册 ====================

def pytest_addoption(parser):
    """注册自定义命令行参数 --env, --language 和 --browser"""
    parser.addoption(
        "--env",
        action="store",
        default=DEFAULT_ENV,
        help=f"测试环境，可选值: {list(ENVIRONMENTS.keys())}（默认：{DEFAULT_ENV}）"
    )
    parser.addoption(
        "--language",
        action="store",
        default=DEFAULT_LANGUAGE,
        help="要测试的语言，多个用逗号分隔，如 en 或 zh-cn（默认：en）"
    )
    parser.addoption(
        "--browser",
        action="store",
        default=DEFAULT_BROWSER,
        help="要测试的浏览器，多个用逗号分隔，如 chromium 或 chromium,firefox（默认：chromium）"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="以无头模式运行浏览器（默认：False）"
    )

def pytest_generate_tests(metafunc):
    """动态参数化"""
    if "lang_urls" in metafunc.fixturenames:
        env = metafunc.config.getoption("--env", default=DEFAULT_ENV)
        logger.info(f"使用环境: {env}")
        if env not in ENVIRONMENTS:
            logger.error(f"不支持的环境: {env}")
            raise pytest.UsageError(f"不支持的环境: {env}，可用值: {list(ENVIRONMENTS.keys())}")
        
        language_urls = get_language_urls(ENVIRONMENTS[env], env)
        raw = metafunc.config.getoption("--language", default=DEFAULT_LANGUAGE)
        
        if raw.strip() == "all":
            languages = list(language_urls.keys())
        else:
            languages = [lang.strip() for lang in raw.split(",") if lang.strip()]
        
        invalid = [l for l in languages if l not in language_urls]
        if invalid:
            raise pytest.UsageError(f"不支持的语言代码: {invalid}，可用值: {list(language_urls.keys())} 或 'all'")
        
        params = [
            pytest.param(
                {
                    "lang": lang,
                    "env": env,
                    "generate_url": language_urls[lang]["generate_url"],
                },
                id=f"{env}-{lang}"
            )
            for lang in languages
        ]
        metafunc.parametrize("lang_urls", params, scope="session")

    if "browser_engine" in metafunc.fixturenames:
        raw = metafunc.config.getoption("--browser", default=DEFAULT_BROWSER)
        if raw.strip() == "all":
            browsers = list(SUPPORTED_BROWSERS)
        else:
            browsers = [b.strip() for b in raw.split(",") if b.strip()]
        invalid = [b for b in browsers if b not in SUPPORTED_BROWSERS]
        if invalid:
            raise pytest.UsageError(f"不支持的浏览器: {invalid}，可用值: {SUPPORTED_BROWSERS} 或 'all'")
        metafunc.parametrize("browser_engine", browsers, scope="session")

# ==================== 浏览器 Fixtures ====================

@pytest.fixture(scope="session")
def browser_engine(request):
    return request.param

@pytest.fixture(scope="session")
def browser(browser_engine, request):
    """启动浏览器（session级别）"""
    logger.info(f"正在启动 {browser_engine} 浏览器")
    headless = bool(request.config.getoption("--headless"))
    with sync_playwright() as playwright:
        if browser_engine == "chromium":
            # 示例：启动外部浏览器或直接 launch
            b = playwright.chromium.launch(headless=headless, args=["--start-maximized"])
            yield b
            b.close()
        elif browser_engine == "msedge":
            b = playwright.chromium.launch(channel="msedge", headless=headless, args=["--start-maximized"])
            yield b
            b.close()
        elif browser_engine == "firefox":
            b = playwright.firefox.launch(headless=headless)
            yield b
            b.close()
        else:
            engine = getattr(playwright, browser_engine)
            b = engine.launch(headless=headless)
            yield b
            b.close()

# ==================== 页面 Fixtures ====================

@pytest.fixture(scope="function")
def page(browser, lang_urls, browser_engine):
    """普通页面，带 Stealth"""
    context = browser.new_context(no_viewport=True, permissions=['clipboard-read', 'clipboard-write'])
    if browser_engine in ["chromium", "firefox", "msedge", "webkit"]:
        context.on("page", Stealth().apply_stealth_sync)
    p = context.new_page()
    p.set_default_timeout(30000)

    p.goto(lang_urls["generate_url"], timeout=60000)
    p.locator(Locators.START_CREATING_BTN).click()
    p.wait_for_load_state("networkidle", timeout=30000)
    
    yield p
    context.close()

@pytest.fixture(scope="session")
def authenticated_context(browser, lang_urls, browser_engine):
    """已登录的浏览器上下文（需根据 Somio 项目实现登录流程）"""
    context = browser.new_context(no_viewport=True, permissions=['clipboard-read', 'clipboard-write'])
    if browser_engine in ["chromium", "firefox", "msedge", "webkit"]:
        context.on("page", Stealth().apply_stealth_sync)
    p = context.new_page()


    
    # 登录流程
    logger.info(f"正在导航至首页: {lang_urls['generate_url']}")
    p.goto(lang_urls["generate_url"])
    
    logger.info("点击 'start creating' 进入功能页")
    p.locator(Locators.START_CREATING_BTN).click()
    p.wait_for_load_state("domcontentloaded")
    
    login_page = LoginPage(p)
    login_page.login(LOGIN_EMAIL, LOGIN_PASSWORD)
    
    yield context
    context.close()

@pytest.fixture(scope="function")
def logged_in_page(authenticated_context, lang_urls):
    """生成已登录页面"""
    p = authenticated_context.new_page()
    p.set_default_timeout(10000)
    
    logger.info(f"正在导航至首页: {lang_urls['generate_url']}")
    p.goto(lang_urls["generate_url"])
    
    logger.info("点击 'start creating' 进入功能页")
    p.locator(Locators.START_CREATING_BTN).click()
    p.wait_for_load_state("domcontentloaded")
    
    yield p
    p.close()


# ==================== 错误处理与截图 ====================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    当测试失败时自动截图，并在支持 pytest-html 时附加到报告。
    需要测试用例中使用 page fixture。
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page")
        if page:
            report_dir = "report/screenshots"
            if not os.path.exists(report_dir):
                os.makedirs(report_dir)
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            file_name = f"{item.name}_{timestamp}.png"
            file_path = os.path.join(report_dir, file_name)
            
            try:
                page.screenshot(path=file_path, full_page=True)
                logger.error(f"测试失败，截图已保存至: {file_path}")
            except Exception as e:
                logger.error(f"截图失败: {e}")
                return
            
            try:
                from pytest_html import extras
                if not hasattr(rep, "extra") or rep.extra is None:
                    rep.extra = []
                rep.extra.append(extras.image(file_path))
            except Exception:
                pass
