import asyncio
import nodriver as uc
import sys

async def main():
    print("Directly attaching to Chrome on 127.0.0.1:9222...")
    
    # We manually build the config to be as empty as possible
    # This stops the library from trying to "verify" a local browser
    config = uc.Config()
    config.browser_base_endpoint = "http://127.0.0.1:9222"
    config.no_sandbox = True
    config.browser_executable_path = None

    try:
        # We use .create() instead of .start() to avoid the 'root' check logic
        browser = await uc.Browser.create(config)
        
        print("Successfully attached! Loading page...")
        # Get the first open tab/page
        page = await browser.get("https://www.google.com")
        
        # page.title is a property, not a method
        print(f"Success! Page title: {page.title}")
        
        await page.sleep(3)
        await page.save_screenshot("nodriver_final.png")
        
        # Just disconnect, don't try to kill the process (YAML handles pkill)
        browser.stop()
        print("Done!")
        
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
