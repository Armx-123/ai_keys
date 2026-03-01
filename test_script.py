import asyncio
import nodriver as uc
import sys

async def main():
    print("Directly attaching to Chrome on 127.0.0.1:9222...")
    
    # We provide a real path so the library doesn't throw a 'NoneType' error,
    # but we force the endpoint so it connects to our running instance.
    config = uc.Config()
    config.browser_executable_path = "/usr/bin/google-chrome" 
    config.browser_base_endpoint = "http://127.0.0.1:9222"
    config.no_sandbox = True
    
    try:
        # We use a high timeout to ensure the websocket handshake completes
        browser = await uc.start(config, timeout=30)
        
        print("Successfully attached! Loading page...")
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
