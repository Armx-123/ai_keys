import asyncio
import nodriver as uc
import sys

async def main():
    print("Directly attaching to Chrome on 127.0.0.1:9222...")
    
    # We bypass the start() wrapper to avoid the root-user check
    config = uc.Config()
    config.browser_base_endpoint = "http://127.0.0.1:9222"
    
    try:
        # Create the browser instance directly from the config
        browser = await uc.Browser.create(config)
        
        print("Successfully attached! Loading page...")
        # Note: In nodriver, browsers start with a default tab
        page = await browser.get("https://www.google.com")
        
        print(f"Success! Page title is: {page.title}")
        
        await asyncio.sleep(3)
        await page.save_screenshot("nodriver_final.png")
        
        print("Screenshot saved. Disconnecting...")
        # We stop the connection, not the browser process (YAML handles the process)
        await browser.stop()
        
    except Exception as e:
        print(f"Connection failed: {e}")
        # Print more info to debug if it still fails
        sys.exit(1)

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
