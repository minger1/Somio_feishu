# -*- coding: utf-8 -*-
"""
调试脚本：分析模型版本下拉的实际 DOM 结构
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
        print("Logged in. Analyzing DOM structure...")
        
        # Analyze the workbench structure
        result = page.evaluate("""() => {
            const ww = document.querySelector('.workbench-wrapper-content');
            if (!ww) return {error: 'workbench-wrapper-content not found'};
            
            function getElementInfo(el, depth=0) {
                const indent = '  '.repeat(depth);
                const children = Array.from(el.children);
                return {
                    tag: el.tagName,
                    class: el.className || '(no class)',
                    id: el.id || '',
                    textPreview: el.childElementCount === 0 ? el.textContent.trim().substring(0, 50) : '',
                    children: depth < 4 ? children.map(c => getElementInfo(c, depth+1)) : []
                };
            }
            
            return getElementInfo(ww);
        }""")
        
        def print_tree(node, depth=0):
            indent = "  " * depth
            tag = node.get('tag', '?')
            cls = node.get('class', '')
            id_ = node.get('id', '')
            text = node.get('textPreview', '')
            id_str = f" id='{id_}'" if id_ else ""
            text_str = f" -> '{text}'" if text else ""
            print(f"{indent}<{tag} class='{cls}'{id_str}>{text_str}")
            for child in node.get('children', []):
                print_tree(child, depth+1)
        
        print_tree(result)
        
        # Also find the model button by looking for the "lyria3" or "V5" element
        print("\n\nSearching for model version button...")
        model_btn_info = page.evaluate("""() => {
            // Find all elements whose direct text contains V5, V5.5, lyria3 etc
            const allEls = document.querySelectorAll('div, span, button');
            const found = [];
            for (const el of allEls) {
                // Check if this element has no div children but has text matching a version name
                const ownText = Array.from(el.childNodes)
                    .filter(n => n.nodeType === 3)
                    .map(n => n.textContent.trim())
                    .join('').trim();
                if (['V5.5','V5','V4.5+','V4.5','V3.5','lyria3'].some(v => ownText.startsWith(v))) {
                    found.push({
                        tag: el.tagName,
                        class: el.className || '(no class)',
                        ownText: ownText.substring(0,30),
                        parentTag: el.parentElement?.tagName,
                        parentClass: el.parentElement?.className || '(no class)',
                        gpTag: el.parentElement?.parentElement?.tagName,
                        gpClass: el.parentElement?.parentElement?.className || '(no class)',
                        ggpClass: el.parentElement?.parentElement?.parentElement?.className || '(no class)'
                    });
                }
            }
            return found;
        }""")
        
        print("Model version related elements found:")
        for item in model_btn_info:
            print(f"  {item}")
        
        input("\nPress Enter to close browser...")
        browser.close()

if __name__ == "__main__":
    main()
