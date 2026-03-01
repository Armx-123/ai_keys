import asyncio
import nodriver as uc
import sys
import os

async def main():
    print("Initializing configuration...")
    
    # Create a local directory for Chrome to store its data (avoids root /tmp issues)
    user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
    os.makedirs(user_data_dir, exist_ok=True)
    
    config = uc.Config()
    config.no_sandbox = True
    config.user_data_dir = user_data_dir
    
    # Standard CI flags
    args = [
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--disable-setuid-sandbox",
        "--no-first-run",
        "--no-zygote",
        "--single-process",
    ]
    for arg in args:
        config.add_argument(arg)

    print(f"Launching browser. Using data dir: {user_data_dir}")
    try:
        # We increase the timeout significantly to allow Xvfb to catch up
        browser = await uc.start(config=config, timeout=30)
        
        page = await browser.get("https://www.google.com")
        print(f"Connection Successful! Title: {page.title}")
        
        await page.save_screenshot("nodriver_result.png")
        await browser.stop()
        
    except Exception as e:
        print(f"Browser launch failed: {e}")
        # List files to see if a crash dump or log was created
        sys.exit(1)

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
