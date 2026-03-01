import asyncio
import nodriver as uc
import sys

async def main():
    print("Connecting to Chrome on port 9222...")
    
    # We create a config that points specifically to the running instance
    # We set browser_executable_path to None so it doesn't try to launch its own
    config = uc.Config(
        browser_base_endpoint="http://127.0.0.1:9222",
        browser_executable_path=None, 
    )
    
    try:
        # Start using the config that points to our manual Chrome instance
        browser = await uc.start(config)
        
        print("Successfully hooked into Chrome!")
        page = await browser.get("https://www.google.com")
        
        print(f"Current page title: {page.title}")
        
        await asyncio.sleep(2)
        await page.save_screenshot("nodriver_final.png")
        
        # In this mode, browser.stop() will just disconnect the CDP session
        await browser.stop()
        
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
