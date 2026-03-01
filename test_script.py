import asyncio
import nodriver as uc
import sys

async def main():
    browser = None
    try:
        print("Starting browser...")

        browser = await uc.start(
            headless=True,
            no_sandbox=True,
            disable_dev_shm_usage=True,
            browser_executable_path="/usr/bin/google-chrome",
            browser_args=[
                "--disable-gpu",
                "--no-first-run",
                "--disable-dev-shm-usage",
            ],
        )

        print("Opening Google...")
        page = await browser.get("https://www.google.com")

        print("Page title:", page.title)

        await page.save_screenshot("nodriver_final.png")

        print("Done successfully.")

    except Exception as e:
        print("Automation failed:", e)
        sys.exit(1)

    finally:
        # Stop browser safely
        if browser:
            try:
                browser.stop()   # 🚀 NO await
            except:
                pass


if __name__ == "__main__":
    uc.loop().run_until_complete(main())
