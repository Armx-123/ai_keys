import asyncio
import nodriver as uc
import os

async def main():
    # Force the path to the chrome binary installed via apt-get
    browser_path = "/usr/bin/google-chrome"
    
    print(f"Starting browser at {browser_path}...")
    
    browser = await uc.start(
        browser_executable_path=browser_path,
        no_sandbox=True,
        browser_args=[
            "--disable-dev-shm-usage",
            "--disable-setuid-sandbox",
            "--no-first-run",
            "--no-zygote"
        ]
    )
    
    page = await browser.get("https://www.google.com")
    print(f"Success! Connected to: {page.title}")
    
    await page.save_screenshot("nodriver_result.png")
    await browser.stop()

if __name__ == "__main__":
    try:
        uc.loop().run_until_complete(main())
    except Exception as e:
        print(f"Script failed with: {e}")
        exit(1)
