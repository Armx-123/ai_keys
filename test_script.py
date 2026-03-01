import asyncio
import nodriver as uc
import sys

async def main():
    print("Forcefully attaching to Chrome on 127.0.0.1:9222...")
    
    # We manually build the config object to bypass all 'discovery' logic
    config = uc.Config()
    config.browser_base_endpoint = "http://127.0.0.1:9222"
    
    # This is the fix: we give it a dummy path so it doesn't return None
    # and we set no_sandbox just to be safe
    config.browser_executable_path = "/usr/bin/google-chrome"
    config.no_sandbox = True

    try:
        # Use the low-level create method
        browser = await uc.Browser.create(config)
        
        print("Connected! Opening Google...")
        page = await browser.get("https://www.google.com")
        
        # Accessing title as a property (no await!)
        print(f"Success! Page title: {page.title}")
        
        await asyncio.sleep(5)
        await page.save_screenshot("nodriver_final.png")
        
        # Close connection
        browser.stop()
        print("Done!")
        
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
