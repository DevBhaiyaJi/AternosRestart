import os
import time
from playwright.sync_api import sync_playwright

EMAIL = os.getenv("ATERNOS_EMAIL")
PASSWORD = os.getenv("ATERNOS_PASSWORD")
SERVER_URL = os.getenv("SERVER_URL")
RESTART_HOURS = float(os.getenv("RESTART_HOURS", "5"))
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"

def restart_server(page):
    page.reload()
    time.sleep(3)
    if page.locator("button:has-text('Stop')").count() > 0:
        print("Stopping server...")
        page.locator("button:has-text('Stop')").first.click()
        time.sleep(15)
    if page.locator("button:has-text('Start')").count() > 0:
        print("Starting server...")
        page.locator("button:has-text('Start')").first.click()
        time.sleep(10)
    else:
        print("Start button not found!")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, args=["--no-sandbox"])
        context = browser.new_context()
        page = context.new_page()

        print("Logging in...")
        page.goto("https://aternos.org/go/")
        page.fill("input[type='email']", EMAIL)
        page.fill("input[type='password']", PASSWORD)
        page.keyboard.press("Enter")
        time.sleep(5)

        page.goto(SERVER_URL)
        interval = int(RESTART_HOURS * 3600)
        print(f"Bot started, restarting every {RESTART_HOURS} hours.")

        while True:
            print(f"\nRestarting at {time.ctime()}")
            try:
                restart_server(page)
            except Exception as e:
                print("Error:", e)
            time.sleep(interval)

if __name__ == "__main__":
    main()
