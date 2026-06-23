import pytest
import os
import subprocess
import time
import json
from playwright.sync_api import sync_playwright, expect
from playwright_stealth import Stealth
from config.settings import ENVIRONMENTS, DEFAULT_ENV, DEFAULT_LANGUAGE, LOGIN_EMAIL, LOGIN_PASSWORD, get_language_urls
from utils import logger
from config.locators import Locators
from pages.login_page import LoginPage
from pages.vocal_remover_page import VocalRemoverPage
from config.settings import TEST_AUDIO_PATH_4  

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
        "--test-browser",
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
        raw = metafunc.config.getoption("--test-browser", default=DEFAULT_BROWSER)
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
def page(browser, lang_urls, browser_engine, request):
    """普通页面，带 Stealth"""
    context = browser.new_context(no_viewport=True, permissions=['clipboard-read', 'clipboard-write'])
    if browser_engine in ["chromium", "firefox", "msedge", "webkit"]:
        context.on("page", Stealth().apply_stealth_sync)
    p = context.new_page()

    p.goto(lang_urls["generate_url"], timeout=0, wait_until="domcontentloaded")
    p.wait_for_load_state("networkidle", timeout=0)
    p.locator(Locators.START_CREATING_BTN).click()
    p.wait_for_load_state("networkidle", timeout=0)

    
    from utils.api_capturer import api_capture
    test_name = request.node.name
    with api_capture(p, test_name):
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
    p.goto(lang_urls["generate_url"], timeout=0, wait_until="domcontentloaded")
    p.wait_for_load_state("networkidle", timeout=0)
    
    logger.info("点击 'start creating' 进入功能页")
    p.locator(Locators.START_CREATING_BTN).click()
    p.wait_for_load_state("networkidle", timeout=0)
    
    login_page = LoginPage(p)
    login_page.login(LOGIN_EMAIL, LOGIN_PASSWORD)
    
    yield context
    context.close()

@pytest.fixture(scope="function")
def logged_in_page(authenticated_context, lang_urls, request):
    """生成已登录页面"""
    p = authenticated_context.new_page()
    
    logger.info(f"正在导航至首页: {lang_urls['generate_url']}")
    p.goto(lang_urls["generate_url"], timeout=0, wait_until="domcontentloaded")
    p.wait_for_load_state("networkidle", timeout=0)
    
    logger.info("点击 'start creating' 进入功能页")
    p.locator(Locators.START_CREATING_BTN).click()
    
    # 1. 等待默认侧边栏（音乐生成）被激活/加载稳定
    p.wait_for_selector("a.link-item.music.active", timeout=15000)
    
    # 2. 等待右侧历史生成列表加载完毕 (确保所有后台请求和列表渲染完成)
    logger.info("等待右侧生成历史列表加载完毕...")
    p.locator(Locators.LIBRARY_SONG_ITEMS).first.wait_for(state="visible", timeout=15000)
    
    from utils.api_capturer import api_capture
    test_name = request.node.name
    with api_capture(p, test_name):
        yield p
    p.close()


# ==================== 错误处理与截图 ====================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    当测试失败时自动截图，并在支持 pytest-html 时附加到报告。
    同时，把执行状态和耗时等写入全局数组供飞书卡片用
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" or (rep.when == "setup" and rep.failed):
        result_data = {
            "name": item.name,
            "status": "PASS" if rep.passed else "FAIL" if rep.failed else "SKIPPED",
            "duration": round(rep.duration, 2),
            "screenshot": None,
            "error_msg": str(rep.longrepr) if rep.failed else ""
        }
        
        if rep.failed:
            page = item.funcargs.get("page") or item.funcargs.get("logged_in_page")
            if not page and hasattr(item, "instance") and item.instance and hasattr(item.instance, "page"):
                page = item.instance.page
                
            if page and hasattr(page, 'screenshot'):
                report_dir = "report/screenshots"
                if not os.path.exists(report_dir):
                    os.makedirs(report_dir)
                
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                file_name = f"{item.name}_{timestamp}.png"
                file_path = os.path.join(report_dir, file_name)
                
                try:
                    page.screenshot(path=file_path, full_page=True)
                    logger.error(f"测试失败，截图已保存至: {file_path}")
                    result_data["screenshot"] = os.path.abspath(file_path)
                except Exception as e:
                    logger.error(f"截图失败: {e}")
                
                try:
                    from pytest_html import extras
                    if not hasattr(rep, "extra") or rep.extra is None:
                        rep.extra = []
                    rep.extra.append(extras.image(file_path))
                except Exception:
                    pass
                
        # ===== 飞书专属：写入 test_results.jsonl =====
        out_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_results.jsonl")
        try:
            with open(out_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(result_data, ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"写入报告文件 test_results.jsonl 失败: {e}")


# ==============================================================================
# Vocal Remover Fixtures
# ==============================================================================

@pytest.fixture(scope="class")
def processed_vocal_page(authenticated_context, lang_urls):
    """类级别 fixture：只执行一次上传和处理，返回页面供类中所有测试使用"""
    logger.info("正在初始化 Vocal Remover 页面处理 fixture (processed_vocal_page)")
    p = authenticated_context.new_page()
    
    logger.info(f"正在导航至首页: {lang_urls['generate_url']}")
    p.goto(lang_urls["generate_url"], timeout=0, wait_until="domcontentloaded")
    p.wait_for_load_state("networkidle", timeout=0)
    
    logger.info("点击 'start creating' 进入功能页")
    p.locator(Locators.START_CREATING_BTN).click()
    
    # 等待默认侧边栏（音乐生成）被激活/加载稳定
    p.wait_for_selector("a.link-item.music.active", timeout=15000)
    
    # 等待右侧历史生成列表加载完毕
    logger.info("等待右侧生成历史列表加载完毕...")
    p.locator(Locators.LIBRARY_SONG_ITEMS).first.wait_for(state="visible", timeout=15000)
    
    # 切换至 Vocal Remover 页面
    vr_page = VocalRemoverPage(p)
    vr_page.switch_to_vocal_remover()
    
    # 上传文件并等待处理完成
    vr_page.upload_local_file(TEST_AUDIO_PATH_4)
    vr_page.click_separate()
    
    # 等待处理完成（下载全部按钮可见说明处理结束）
    logger.info("正在等待 Vocal Remover 文件处理完成 (最多 360 秒)")
    p.locator(Locators.VOCAL_RESULT_DOWNLOAD_ALL_BTN).wait_for(state="visible", timeout=360000)
    logger.success("Vocal Remover 文件处理完成，结果页已成功加载")
    
    # 等待各个音轨的音频加载完毕
    vr_page.wait_for_audio_loaded()
    
    # 断言下载按钮出现
    expect(p.locator(Locators.VOCAL_RESULT_DOWNLOAD_VOCAL_BTN)).to_be_visible(timeout=5000)
    expect(p.locator(Locators.VOCAL_RESULT_DOWNLOAD_INSTRUMENTAL_BTN)).to_be_visible(timeout=5000)
    
    yield p
    logger.info("正在关闭 processed_vocal_page fixture")
    p.close()


@pytest.fixture(scope="class")
def vr_page(processed_vocal_page):
    """类级别 fixture：将 processed_vocal_page 包装成 VocalRemoverPage 实例"""
    return VocalRemoverPage(processed_vocal_page)


# ==============================================================================
# Stem Splitter Fixtures
# ==============================================================================

def _init_single_instrument_page(authenticated_context, lang_urls, instrument: str):
    logger.info(f"正在初始化 Stem Splitter {instrument} 模式页面处理 fixture")
    p = authenticated_context.new_page()
    
    logger.info(f"正在导航至首页: {lang_urls['generate_url']}")
    p.goto(lang_urls["generate_url"], timeout=0, wait_until="domcontentloaded")
    p.wait_for_load_state("networkidle", timeout=0)
    
    logger.info("点击 'start creating' 进入功能页")
    p.locator(Locators.START_CREATING_BTN).click()
    
    # 等待加载稳定
    p.wait_for_selector("a.link-item.music.active", timeout=15000)
    p.locator(Locators.LIBRARY_SONG_ITEMS).first.wait_for(state="visible", timeout=15000)
    
    # 切换至 Stem Splitter 页面
    from pages.stem_splitter_page import StemSplitterPage
    sp_page = StemSplitterPage(p, instrument=instrument)
    sp_page.switch_to_stem_splitter()
    
    # 选择对应的单乐器 Tab
    mode_btn = sp_page.INSTRUMENT_MODES[instrument]["mode_btn"]
    sp_page.select_mode(mode_btn)
    
    # 上传文件并处理
    sp_page.upload_local_file(TEST_AUDIO_PATH_4)
    sp_page.click_separate()
    
    # 等待处理完成
    all_btn = sp_page.INSTRUMENT_MODES[instrument]["all_btn"]
    logger.info(f"正在等待 {instrument} 模式文件处理完成 (最多 360 秒)")
    p.locator(all_btn).wait_for(state="visible", timeout=360000)
    
    # 等待各个音轨的音频加载完毕
    sp_page.wait_for_audio_loaded()
    
    # 验证单轨和去乐器轨按钮可见
    solo_btn = sp_page.INSTRUMENT_MODES[instrument]["solo_btn"]
    no_inst_btn = sp_page.INSTRUMENT_MODES[instrument]["no_inst_btn"]
    expect(p.locator(solo_btn)).to_be_visible(timeout=5000)
    expect(p.locator(no_inst_btn)).to_be_visible(timeout=5000)
    
    logger.success(f"{instrument} 模式文件处理完成")
    return p


@pytest.fixture(scope="class")
def processed_stem_page(authenticated_context, lang_urls):
    """类级别 fixture：只执行一次上传和处理，返回页面供类中所有测试使用"""
    logger.info("正在初始化 Stem Splitter 页面处理 fixture (processed_stem_page)")
    p = authenticated_context.new_page()
    
    logger.info(f"正在导航至首页: {lang_urls['generate_url']}")
    p.goto(lang_urls["generate_url"], timeout=0, wait_until="domcontentloaded")
    p.wait_for_load_state("networkidle", timeout=0)
    
    logger.info("点击 'start creating' 进入功能页")
    p.locator(Locators.START_CREATING_BTN).click()
    
    # 等待默认侧边栏（音乐生成）被激活/加载稳定
    p.wait_for_selector("a.link-item.music.active", timeout=15000)
    
    # 等待右侧历史生成列表加载完毕
    logger.info("等待右侧生成历史列表加载完毕...")
    p.locator(Locators.LIBRARY_SONG_ITEMS).first.wait_for(state="visible", timeout=15000)
    
    # 切换至 Stem Splitter 页面
    from pages.stem_splitter_page import StemSplitterPage
    sp_page = StemSplitterPage(p)
    sp_page.switch_to_stem_splitter()
    
    # 上传文件并等待处理完成
    sp_page.upload_local_file(TEST_AUDIO_PATH_4)
    sp_page.click_separate()
    
    # 等待处理完成（下载全部按钮可见说明处理结束）
    logger.info("正在等待 Stem Splitter 文件处理完成 (最多 360 秒)")
    p.locator(Locators.STEM_MIX_DOWNLOAD_BTN).wait_for(state="visible", timeout=360000)
    logger.success("Stem Splitter 文件处理完成，结果页已成功加载")
    
    # 等待各个音轨的音频加载完毕
    sp_page.wait_for_audio_loaded()
    
    # 断言各个声道的波形图已成功加载并显示
    expect(p.locator("#vocal-waveform")).to_be_visible(timeout=5000)
    expect(p.locator("#drums-waveform")).to_be_visible(timeout=5000)
    expect(p.locator("#bass-waveform")).to_be_visible(timeout=5000)
    expect(p.locator("#piano-waveform")).to_be_visible(timeout=5000)
    expect(p.locator("#guitar-waveform")).to_be_visible(timeout=5000)
    expect(p.locator("#other-waveform")).to_be_visible(timeout=5000)
    
    yield p
    logger.info("正在关闭 processed_stem_page fixture")
    p.close()


@pytest.fixture(scope="class")
def stem_page(processed_stem_page):
    """类级别 fixture：将 processed_stem_page 包装成 StemSplitterPage 实例"""
    from pages.stem_splitter_page import StemSplitterPage
    return StemSplitterPage(processed_stem_page)


@pytest.fixture(scope="class")
def processed_stem_drums_page(authenticated_context, lang_urls):
    p = _init_single_instrument_page(authenticated_context, lang_urls, "drums")
    yield p
    p.close()


@pytest.fixture(scope="class")
def stem_drums_page(processed_stem_drums_page):
    from pages.stem_splitter_page import StemSplitterPage
    return StemSplitterPage(processed_stem_drums_page, instrument="drums")


@pytest.fixture(scope="class")
def processed_stem_bass_page(authenticated_context, lang_urls):
    p = _init_single_instrument_page(authenticated_context, lang_urls, "bass")
    yield p
    p.close()


@pytest.fixture(scope="class")
def stem_bass_page(processed_stem_bass_page):
    from pages.stem_splitter_page import StemSplitterPage
    return StemSplitterPage(processed_stem_bass_page, instrument="bass")


@pytest.fixture(scope="class")
def processed_stem_piano_page(authenticated_context, lang_urls):
    p = _init_single_instrument_page(authenticated_context, lang_urls, "piano")
    yield p
    p.close()


@pytest.fixture(scope="class")
def stem_piano_page(processed_stem_piano_page):
    from pages.stem_splitter_page import StemSplitterPage
    return StemSplitterPage(processed_stem_piano_page, instrument="piano")


@pytest.fixture(scope="class")
def processed_stem_guitar_page(authenticated_context, lang_urls):
    p = _init_single_instrument_page(authenticated_context, lang_urls, "guitar")
    yield p
    p.close()


@pytest.fixture(scope="class")
def stem_guitar_page(processed_stem_guitar_page):
    from pages.stem_splitter_page import StemSplitterPage
    return StemSplitterPage(processed_stem_guitar_page, instrument="guitar")
