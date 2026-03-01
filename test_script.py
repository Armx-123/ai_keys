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
    
    # IMPORTANT: We set these via attributes, not add_argument
    config.no_sandbox = True
    config.headless = False  # Xvfb handles the "display," so nodriver stays "headful"
    
    # 3. Add allowed CI-specific arguments
    args = [
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
        # Increase timeout for GitHub Actions overhead
        browser = await uc.start(config=config, timeout=40)
        
        print("Successfully connected to browser!")
        page = await browser.get("https://www.google.com")
        
        print(f"Current page title: {page.title}")
        
        # Give it a moment to render before the screenshot
        await asyncio.sleep(2)
        await page.save_screenshot("nodriver_final.png")
        
        await browser.stop()
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
