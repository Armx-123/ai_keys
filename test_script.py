from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate and interact
        print("Navigating to example.com...")
        page.goto("https://example.com")
        
        # Take a screenshot for the CI artifact
        page.screenshot(path="example.png")
        print(f"Page title is: {page.title()}")
        
        browser.close()

if __name__ == "__main__":
    run()
