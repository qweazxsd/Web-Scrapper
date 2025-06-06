from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from email.message import EmailMessage
import smtplib
import os

# ─────────────────────────────────────────────────────────────────────────────
# 1. CONFIGURATION (edit these!)
# ─────────────────────────────────────────────────────────────────────────────

URL_TO_CHECK      = "https://www.dira.moch.gov.il/ProjectsList"
CSS_SELECTOR      = "b.blue-label.col-md-1.count.ng-binding"

# Email (SMTP)
SMTP_SERVER    = "smtp.gmail.com"
SMTP_PORT      = 587
SMTP_USER      = "alonnergaon0@gmail.com"
SMTP_PASS      = os.getenv("SMTP_PASS")
SENDER_ADDR    = "alonnergaon0@gmail.com"
RECIPIENT_ADDR = "alonnergaon0@gmail.com"
# ─────────────────────────────────────────────────────────────────────────────
# 2. SCRAPE + PARSE FUNCTION
# ─────────────────────────────────────────────────────────────────────────────
def fetch_value_with_selenium(url: str) -> float | None:
    """
    Launches a headless Chrome, navigates to `url`, waits for JS to render,
    then finds the element by `css_selector` and returns its numeric text.
    """
    chrome_opts = Options()
    chrome_opts.add_argument("--headless")
    chrome_opts.add_argument("--no-sandbox")
    chrome_opts.add_argument("--disable-gpu")
    chrome_opts.add_argument("--disable-dev-shm-usage")

    # Automatically download & use the right ChromeDriver
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=chrome_opts
    )

    try:
        driver.get(url)
        # Wait a moment for JS to finish rendering. You might need to adjust or add
        # explicit waits if the page is slow. For many Angular pages, 2–3 seconds is enough:
        time.sleep(3)

        # Now that the JS has run, the <b> should exist in the DOM:
        elem = driver.find_element("css selector", CSS_SELECTOR)
        if not elem:
            print(f"[WARN] Selenium did not find element with selector '{CSS_SELECTOR}'")
            return None

        text = elem.text.strip()
        try:
            return float(text.replace(",", "").replace(" ", ""))
        except ValueError:
            print(f"[ERROR] Could not convert '{text}' to float.")
            return None

    except Exception as e:
        print(f"[ERROR] Selenium error: {e}")
        return None

    finally:
        driver.quit()

# ─────────────────────────────────────────────────────────────────────────────
# 3. EMAIL NOTIFICATION FUNCTION
# ─────────────────────────────────────────────────────────────────────────────

def send_email_notification(
    smtp_server: str,
    smtp_port: int,
    smtp_user: str,
    smtp_pass: str,
    sender_addr: str,
    recipient_addr: str,
    subject: str,
    body: str,
) -> bool:
    msg = EmailMessage()
    msg["From"] = sender_addr
    msg["To"] = recipient_addr
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")
        return False

# ─────────────────────────────────────────────────────────────────────────────
# 5. MAIN “AGENT” LOOP
# ─────────────────────────────────────────────────────────────────────────────

def main_loop():
    alerted_once = False
    print(f"\n[INFO] Checking {URL_TO_CHECK} …")
    val = fetch_value_with_selenium(URL_TO_CHECK)
    if val is None:
        print("[INFO] Could not get a valid numeric value. Retrying in a bit.")
    else:
        print(f"[INFO] Fetched value = {val}")

        # Check if value > 0
        if val >= 0 and not alerted_once:
            subject = f"🔔 Alert: value = {val} > 0"
            body    = f"The element '{CSS_SELECTOR}' at {URL_TO_CHECK} is now {val}, which is > 0."

            # Send email
            email_sent = send_email_notification(
                SMTP_SERVER,
                SMTP_PORT,
                SMTP_USER,
                SMTP_PASS,
                SENDER_ADDR,
                RECIPIENT_ADDR,
                subject,
                body
            )
            if email_sent:
                print("[INFO] Email notification sent.")
            else:
                print("[WARN] Email notification failed.")

            alerted_once = True  # so we don't spam multiple times in a row

        elif val <= 0:
            # Reset so that if it goes back above 0 later, we alert again
            if alerted_once:
                print("[INFO] Value ≤ 0 again. Resetting alert flag.")
            alerted_once = False

if __name__ == "__main__":
    main_loop()

