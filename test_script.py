import asyncio
import nodriver as uc
import sys

async def main():
    browser = None
    try:
        print("Starting browser...")

        config = uc.Config()
        config.headless = True
        config.no_sandbox = True
        config.disable_dev_shm_usage = True
        config.browser_executable_path = "/usr/bin/google-chrome"

        # 🔴 Increase timeout (this is the key fix)
        config.connection_timeout = 60   # default is lower

        browser = await uc.Browser.create(config)

        print("Opening YouTube...")
        page = await browser.get("https://armx-123.github.io/ai_keys/main.html")

        await asyncio.sleep(5)  # let heavy page settle

        print("Page title:", page.title)

        await page.save_screenshot("nodriver_final.png")

        print("Done successfully.")

    except Exception as e:
        print("Automation failed:", e)
        sys.exit(1)

    finally:
        if browser:
            try:
                browser.stop()
            except:
                pass


if __name__ == "__main__":
    uc.loop().run_until_complete(main())
