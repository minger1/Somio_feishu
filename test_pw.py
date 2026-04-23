from playwright.sync_api import sync_playwright

def test():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True, permissions=['clipboard-read', 'clipboard-write'])
        from playwright_stealth import Stealth
        context.on("page", Stealth().apply_stealth_sync)
        page = context.new_page()
        try:
            page.goto("https://somio.ai/")
            print("Title:", page.title())
        except Exception as e:
            print("Error:", e)
        finally:
            browser.close()

if __name__ == "__main__":
    test()
