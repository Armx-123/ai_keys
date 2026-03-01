import asyncio
import nodriver as uc
import sys

async def main():
    print("Connecting to existing Chrome instance on port 9222...")
    try:
        # We connect to the browser we started in the YAML
        browser = await uc.connect(host="127.0.0.1", port=9222)
        
        print("Connected! Navigating to Google...")
        page = await browser.get("https://www.google.com")
        
        print(f"Success! Page title: {page.title}")
        
        await asyncio.sleep(2)
        await page.save_screenshot("nodriver_final.png")
        
        # We don't call browser.stop() because we want the YAML to handle the process
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
