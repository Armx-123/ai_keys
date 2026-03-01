import asyncio
import nodriver as uc
import sys

async def main():
    try:
        print("Starting browser...")

        browser = await uc.start(
            headless=True,
            no_sandbox=True,                 # Required for GitHub Actions (runs as root)
            disable_dev_shm_usage=True,      # Avoid /dev/shm crashes in CI
            browser_executable_path="/usr/bin/google-chrome",
            browser_args=[
                "--disable-gpu",
                "--disable-software-rasterizer",
                "--disable-dev-shm-usage",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-background-networking",
            ]
        )

        print("Opening Google...")
        page = await browser.get("https://www.google.com")

        print("Page title:", page.title)

        await page.save_screenshot("nodriver_final.png")

        print("Done successfully.")
        await browser.stop()

    except Exception as e:
        print("Automation failed:", e)
        sys.exit(1)


if __name__ == "__main__":
    uc.loop().run_until_complete(main())
