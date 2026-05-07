# -*- coding: utf-8 -*-
"""
验证最终修复后的 locators.py
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
        
        # Navigate and login
        page.goto("http://192.168.2.31:5174/")
        page.wait_for_load_state("networkidle", timeout=30000)
        btn = page.locator(Locators.START_CREATING_BTN)
        btn.scroll_into_view_if_needed(timeout=10000)
        btn.click(timeout=10000)
        page.wait_for_load_state("networkidle", timeout=30000)
        page.wait_for_timeout(1000)
        
        page.locator(Locators.LOGIN_BTN).click()
        page.fill(Locators.EMAIL_INPUT, LOGIN_EMAIL)
        page.fill(Locators.PASSWORD_INPUT, LOGIN_PASSWORD)
        page.locator(Locators.SUBMIT_BTN).click()
        page.wait_for_selector(Locators.USER_AVATAR, timeout=15000)
        page.wait_for_timeout(2000)
        print("Logged in. Testing locators...")
        
        # Test MODEL_VERSION_DROPDOWN trigger
        el = page.locator(Locators.MODEL_VERSION_DROPDOWN)
        count = el.count()
        print(f"MODEL_VERSION_DROPDOWN found: {count}")
        if count > 0:
            el.first.click()
            page.wait_for_timeout(800)
            print("Trigger clicked OK. Testing version li options...")
            
            versions = [
                ("V5.5", Locators.MODEL_VERSION_V5_5),
                ("V5", Locators.MODEL_VERSION_V5),
                ("V4.5+", Locators.MODEL_VERSION_V4_5_PLUS),
                ("V4.5", Locators.MODEL_VERSION_V4_5),
                ("V3.5", Locators.MODEL_VERSION_V3_5),
                ("lyria3", Locators.MODEL_VERSION_LYRIA3),
            ]
            all_ok = True
            for name, locator in versions:
                el2 = page.locator(locator)
                cnt = el2.count()
                if cnt > 0:
                    txt = el2.first.text_content()[:40].strip()
                    print(f"  OK  {name}: count={cnt}, text='{txt}'")
                else:
                    print(f"  NG  {name}: NOT FOUND! Locator: {locator}")
                    all_ok = False
            
            if all_ok:
                print("\nALL LOCATORS OK!")
            else:
                print("\nSome locators failed. Check above.")
        else:
            print("NG: Trigger NOT FOUND!")
        
        input("\nPress Enter to close...")
        browser.close()

if __name__ == "__main__":
    main()
