import asyncio
import nodriver as uc
import sys

async def main():
    print("Initializing configuration...")
    
    # Manually setting up the config to bypass root/sandbox issues
    config = uc.Config()
    config.no_sandbox = True
    config.headless = False # We use Xvfb to handle the 'head'
    
    # Critical flags for GitHub Actions/Docker
    args = [
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--disable-setuid-sandbox",
        "--no-first-run",
        "--no-zygote",
        "--remote-debugging-port=9222",
    ]
    for arg in args:
        config.add_argument(arg)

    print("Launching browser with manual config...")
    try:
        # Start using the explicit config object
        browser = await uc.start(config=config)
        
        page = await browser.get("https://www.google.com")
        print(f"Connection Successful! Title: {page.title}")
        
        await page.save_screenshot("nodriver_result.png")
        await browser.stop()
        
    except Exception as e:
        print(f"Browser launch failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
