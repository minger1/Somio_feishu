# -*- coding: utf-8 -*-
"""
快速验证脚本：检查修复后的定位器是否正常工作
"""
import sys
sys.path.insert(0, r"c:\Users\73446\PycharmProjects\Somio_feishu")

from playwright.sync_api import sync_playwright
from config.locators import Locators
from config.settings import LOGIN_EMAIL, LOGIN_PASSWORD

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        page.set_default_timeout(15000)
        
        # Navigate to application
        print("Navigating to home...")
        page.goto("http://192.168.2.31:5174/")
        page.wait_for_load_state("networkidle", timeout=30000)
        
        # Click start creating (scroll into view first)
        print("Clicking 'start creating'...")
        btn = page.locator(Locators.START_CREATING_BTN)
        btn.scroll_into_view_if_needed(timeout=10000)
        btn.click(timeout=10000)
        page.wait_for_load_state("networkidle", timeout=30000)
        page.wait_for_timeout(1000)
        print("OK: START_CREATING_BTN success")
        
        # Login
        print("Clicking login button...")
        page.locator(Locators.LOGIN_BTN).click()
        page.fill(Locators.EMAIL_INPUT, LOGIN_EMAIL)
        page.fill(Locators.PASSWORD_INPUT, LOGIN_PASSWORD)
        page.locator(Locators.SUBMIT_BTN).click()
        print("Waiting for login...")
        page.wait_for_selector(Locators.USER_AVATAR, timeout=15000)
        print("OK: Login success")
        
        page.wait_for_timeout(2000)
        
        # Test MODEL_VERSION_DROPDOWN trigger
        print("\nTesting MODEL_VERSION_DROPDOWN trigger...")
        el = page.locator(Locators.MODEL_VERSION_DROPDOWN)
        count = el.count()
        print(f"  Found {count} element(s)")
        if count > 0:
            text = el.first.inner_text()
            print(f"  Current version text: '{text.strip()[:30]}'")
            el.first.click()
            page.wait_for_timeout(800)
            print("  OK: Trigger clicked, checking version options...")
            
            for name, locator in [
                ("V5.5", Locators.MODEL_VERSION_V5_5),
                ("V5", Locators.MODEL_VERSION_V5),
                ("V4.5+", Locators.MODEL_VERSION_V4_5_PLUS),
                ("V4.5", Locators.MODEL_VERSION_V4_5),
                ("V3.5", Locators.MODEL_VERSION_V3_5),
                ("lyria3", Locators.MODEL_VERSION_LYRIA3),
            ]:
                el2 = page.locator(locator)
                cnt = el2.count()
                if cnt > 0:
                    txt = el2.first.inner_text()[:40].strip()
                    print(f"  OK  {name}: found -> '{txt}'")
                else:
                    print(f"  NG  {name}: NOT FOUND! locator: {locator}")
        else:
            print("  NG: Trigger NOT FOUND! Debugging...")
            ww_count = page.locator(".workbench-wrapper-content").count()
            print(f"  .workbench-wrapper-content count: {ww_count}")
            if ww_count > 0:
                js_result = page.evaluate("""() => {
                    const ww = document.querySelector('.workbench-wrapper-content');
                    if (!ww) return 'NOT FOUND';
                    return {
                        class: ww.className,
                        directChildren: Array.from(ww.children).map(c => ({tag: c.tagName, class: c.className, text: c.textContent.trim().substring(0, 50)}))
                    };
                }""")
                print(f"  workbench structure: {js_result}")
        
        print("\nVerification done!")
        input("Press Enter to close browser...")
        browser.close()

if __name__ == "__main__":
    main()
