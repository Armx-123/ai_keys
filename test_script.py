import asyncio
import json
import random
import string
import os
import warnings
import nodriver as uc
import sys

# Configuration
TARGET_URL = "https://armx-123.github.io/ai_keys/main.html"
GMAIL_FILE = "gmails.txt"
TOKENS_FILE = "tokens.json"

warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed transport")


# ------------------- CONFIG (IMPORTANT FIX) -------------------
def get_browser_config():
    config = uc.Config()
    config.headless = True
    config.no_sandbox = True
    config.disable_dev_shm_usage = True
    config.browser_executable_path = "/usr/bin/google-chrome"
    config.connection_timeout = 60  # important for CI
    return config
# -------------------------------------------------------------


async def human_type(element, text):
    for char in text:
        await element.send_keys(char)
        await asyncio.sleep(random.uniform(0.04, 0.15))


def get_next_gmail():
    if not os.path.exists(GMAIL_FILE):
        return None
    with open(GMAIL_FILE, "r") as f:
        lines = f.readlines()
    return lines[0].strip() if lines else None


def remove_first_gmail():
    if not os.path.exists(GMAIL_FILE):
        return
    with open(GMAIL_FILE, "r") as f:
        lines = f.readlines()
    with open(GMAIL_FILE, "w") as f:
        f.writelines(lines[1:])


def append_token_data(gmail, token):
    existing_data = []
    if os.path.exists(TOKENS_FILE):
        try:
            with open(TOKENS_FILE, "r") as f:
                existing_data = json.load(f)
        except:
            existing_data = []

    existing_data.append({
        "gmail": gmail,
        "puter_auth_token": token
    })

    with open(TOKENS_FILE, "w") as f:
        json.dump(existing_data, f, indent=2)


def generate_custom_string():
    letters = ''.join(random.choices(string.ascii_letters, k=random.randint(4, 6)))
    digits = ''.join(random.choices(string.digits, k=random.randint(3, 5)))
    special_char = random.choice(string.punctuation)
    return f"{letters}{digits}{special_char}"


async def process_single_registration():
    current_gmail = get_next_gmail()
    if not current_gmail:
        print("No Gmails found.")
        return

    print(f"--- Starting: {current_gmail} ---")

    browser = None
    try:
        # ✅ USE CONFIG INSTEAD OF uc.start()
        browser = await uc.Browser.create(get_browser_config())

        main_tab = await browser.get(TARGET_URL)
        await asyncio.sleep(3)

        # 1. Open Popup
        sign_in_btn = await main_tab.find("Sign in", best_match=True)
        if sign_in_btn:
            await asyncio.sleep(random.uniform(1, 1.5))
            await sign_in_btn.mouse_click()

        # 2. Detect Popup
        popup_tab = None
        for _ in range(20):
            if len(browser.tabs) > 1:
                popup_tab = browser.tabs[-1]
                break
            await asyncio.sleep(1)

        if not popup_tab:
            print("Popup failed.")
            return

        await popup_tab.activate()

        # 3. Wait for Form
        for _ in range(25):
            try:
                if await popup_tab.select(".username"):
                    break
            except:
                pass
            await asyncio.sleep(1)
        else:
            print("Form timeout.")
            return

        # 4. Fill Form
        print("Filling form...")
        username = f"User_{random.randint(100, 9999999)}"
        password = generate_custom_string()

        steps = [
            (".username", username),
            (".email", current_gmail),
            (".password", password),
            (".confirm-password", password)
        ]

        for selector, value in steps:
            field = await popup_tab.select(selector)
            rect = await field.get_position()
            await popup_tab.mouse_move(rect.x + rect.width/2, rect.y + rect.height/2)
            await field.click()
            await human_type(field, value)
            await asyncio.sleep(0.3)

        # 5. Captcha (best-effort only)
        print("Checking captcha...")
        for _ in range(10):
            iframes = await popup_tab.query_selector_all("iframe")
            for f in iframes:
                attrs = f.attributes
                src = attrs[attrs.index("src")+1] if "src" in attrs else ""
                if "challenge-platform" in src:
                    rect = await f.get_position()
                    await popup_tab.mouse_click(rect.x + 35, rect.y + 32)
                    await asyncio.sleep(8)
                    break
            await asyncio.sleep(1)

        # 6. Submit
        submit_btn = await popup_tab.select(".signup-btn")
        if submit_btn:
            await submit_btn.mouse_click()

        # 7. Detect Success
        token = None
        for _ in range(25):
            cookies = await browser.cookies.get_all()
            for c in cookies:
                c_dict = c.to_dict() if hasattr(c, 'to_dict') else c.__dict__
                if c_dict.get("name") == "puter_auth_token":
                    token = c_dict.get("value")
                    break
            if token:
                break
            await asyncio.sleep(1)

        if token:
            append_token_data(current_gmail, token)
            print(token)
            remove_first_gmail()
            print("SUCCESS:", token)
        else:
            print("FAILED to get token.")

    except Exception as e:
        print("Automation failed:", e)
        sys.exit(1)

    finally:
        if browser:
            try:
                browser.stop()
            except:
                pass


if __name__ == "__main__":
    asyncio.run(process_single_registration())
