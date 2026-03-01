import asyncio
import nodriver as uc

async def main():
    # Start the browser with the specific no_sandbox flag for root environments
    browser = await uc.start(
        no_sandbox=True,
        browser_args=["--disable-setuid-sandbox", "--disable-dev-shm-usage"]
    )
    
    # Rest of your script...
    page = await browser.get("https://www.google.com")
    print(f"Connected to: {page.title}")
    
    await page.save_screenshot("nodriver_result.png")
    await browser.stop()

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
