import asyncio
import nodriver as uc

async def main():
    browser = await uc.start(
        headless=True,
        no_sandbox=True,
        disable_dev_shm_usage=True,
        browser_executable_path="/usr/bin/google-chrome"
    )

    page = await browser.get("https://www.google.com")
    print("Title:", page.title)

    await page.save_screenshot("nodriver_final.png")
    await browser.stop()

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
