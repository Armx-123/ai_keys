import asyncio
import nodriver as uc

async def main():
    # Start the browser
    # Note: --no-sandbox is required for Linux/GitHub Actions environments
    browser = await uc.start(
        browser_args=["--no-sandbox", "--disable-setuid-sandbox"]
    )
    
    page = await browser.get("https://www.google.com")
    
    print(f"Connected to: {page.title}")
    
    # Wait and take a screenshot to verify
    await page.sleep(2)
    await page.save_screenshot("nodriver_result.png")
    
    await browser.stop()

if __name__ == "__main__":
    # nodriver uses its own loop helper for convenience
    uc.loop().run_until_complete(main())
