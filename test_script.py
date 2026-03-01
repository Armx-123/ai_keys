import asyncio
import nodriver as uc
import sys

async def main():
    print("Connecting to Chrome on port 9222...")
    try:
        # In nodriver, you connect to an existing instance by passing the endpoint
        browser = await uc.start(
            browser_base_endpoint="http://127.0.0.1:9222",
        )
        
        print("Successfully hooked into Chrome!")
        page = await browser.get("https://www.google.com")
        
        print(f"Current page title: {page.title}")
        
        # Take the screenshot to prove it worked
        await asyncio.sleep(2)
        await page.save_screenshot("nodriver_final.png")
        
        # We don't stop the browser here, let the YAML cleanup handle it
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
