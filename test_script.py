import asyncio
import nodriver as uc
import sys

async def main():
    print("Directly attaching to Chrome on 127.0.0.1:9222...")
    
    # We initialize the config manually
    config = uc.Config()
    
    # This is the "Magic" part: 
    # By setting these, we trick nodriver into skipping the root-user check
    config.no_sandbox = True
    config.browser_executable_path = None 
    config.browser_base_endpoint = "http://127.0.0.1:9222"
    
    try:
        # We use the lower-level start method with our 'pre-verified' config
        browser = await uc.start(config)
        
        print("Successfully attached! Navigating...")
        page = await browser.get("https://www.google.com")
        
        print(f"Success! Page title: {page.title}")
        
        await asyncio.sleep(2)
        await page.save_screenshot("nodriver_final.png")
        
        await browser.stop()
        
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
