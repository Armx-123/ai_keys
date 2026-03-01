import asyncio
import nodriver as uc
import sys

async def main():
    print("Directly attaching to Chrome on 127.0.0.1:9222...")
    
    config = uc.Config()
    config.browser_executable_path = "/usr/bin/google-chrome" 
    config.browser_base_endpoint = "http://127.0.0.1:9222"
    config.no_sandbox = True
    
    try:
        browser = await uc.start(config, timeout=30)
        print("Successfully attached!")

        # Getting the first tab
        page = await browser.get("https://www.google.com")
        
        # In nodriver, title is a property, NOT an awaited function
        print(f"Success! Page title: {page.title}")
        
        # Wait for the page to actually load before screenshot
        await page.sleep(3) 
        
        print("Taking screenshot...")
        await page.save_screenshot("nodriver_final.png")
        
        # Just close the connection, don't await a return value
        browser.stop()
        print("Done!")
        
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
