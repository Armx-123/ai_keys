import asyncio
import nodriver as uc
import sys
import os
import shutil

async def main():
    # 1. Find the actual Chrome path
    chrome_path = shutil.which("google-chrome") or shutil.which("google-chrome-stable")
    print(f"Detected Chrome path: {chrome_path}")
    
    # 2. Setup Config
    config = uc.Config()
    config.browser_executable_path = chrome_path
    config.no_sandbox = True  # Crucial for root/GitHub Actions
    
    # 3. Add CI-specific arguments
    # We use --headless=new alongside xvfb for maximum stability
    args = [
        "--headless=new",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--disable-setuid-sandbox",
        "--no-zygote",
        "--remote-debugging-port=9222"
    ]
    for arg in args:
        config.add_argument(arg)

    print("Attempting to launch browser...")
    try:
        # High timeout for slow CI environments
        browser = await uc.start(config=config, timeout=40)
        
        print("Successfully connected to browser!")
        page = await browser.get("https://www.google.com")
        
        print(f"Current page title: {page.title}")
        await page.save_screenshot("nodriver_final.png")
        
        await browser.stop()
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
