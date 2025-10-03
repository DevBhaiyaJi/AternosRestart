import os
import time
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

EMAIL = os.getenv("ATERNOS_EMAIL")
PASSWORD = os.getenv("ATERNOS_PASSWORD")
SERVER_URL = os.getenv("SERVER_URL")
SERVER_ID = os.getenv("SERVER_ID")
RESTART_HOURS = float(os.getenv("RESTART_HOURS", "5"))
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
COOKIES_PATH = Path("aternos_cookies.json")

if SERVER_ID and not SERVER_URL:
    SERVER_URL = f"https://aternos.org/server/{SERVER_ID}/"

if not EMAIL or not PASSWORD:
    raise SystemExit("⚠️ Please set ATERNOS_EMAIL and ATERNOS_PASSWORD env vars.")

def save_cookies(context):
    with open(COOKIES_PATH, "w") as f:
        json.dump(context.cookies(), f)

def load_cookies(context):
    if COOKIES_PATH.exists():
        with open(COOKIES_PATH, "r") as f:
            context.add_cookies(json.load(f))
        return True
    return False

def restart_server(page):
    page.reload()
    time.sleep(3)

    # Stop if running
    if page.locator("button:has-text('Stop')").count() > 0:
        print("Stopping server...")
        page.locator("button:has-text('Stop')").first.click()
        time.sleep(15)

    # Start again
    if page.locator("button:has-text('Start')").count() > 0:
        print("Starting server...")
        page.locator("button:has-text('Start')").first.click()
        time.sleep(10)
    else:
        print("Could not find Start button!")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, args=["--no-sandbox"])
        context = browser.new_context()
        page = context.new_page()

        if not load_cookies(context):
            print("Logging in with email/password...")
            page.goto("https://aternos.org/go/")
            page.fill("input[type='email']", EMAIL)
            page.fill("input[type='password']", PASSWORD)
            page.keyboard.press("Enter")
            time.sleep(5)
            save_cookies(context)
        else:
            print("Using saved cookies...")

        page.goto(SERVER_URL, wait_until="domcontentloaded")

        interval = int(RESTART_HOURS * 3600)
        print(f"⏳ Bot started, will restart server every {RESTART_HOURS} hours.")

        while True:
            print(f"\n🔄 Restarting at {time.ctime()}")
            try:
                restart_server(page)
            except Exception as e:
                print("Error:", e)
            time.sleep(interval)

if __name__ == "__main__":
    main()
