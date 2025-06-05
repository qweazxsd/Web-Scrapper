# WebValueWatcher

A lightweight Python “agent” that periodically scrapes a numerical value from a JavaScript-rendered webpage and sends an email alert when the value crosses a threshold (≥ 0). This script uses Selenium to allow Angular/JS content to render, then checks a specific CSS selector for a numeric value and notifies you via SMTP (e.g., Gmail).

---

## 🔍 Overview

- **Script name**: `scrape.py`
- **Primary function**:  
  1. Launch a headless browser (Chrome + ChromeDriver).  
  2. Visit a target URL (e.g., Ministry of Construction’s project list).  
  3. Wait for Angular/JS to finish rendering.  
  4. Extract a numeric value from a specified CSS selector.  
  5. If the value ≥ 0 (or > 0, depending on configuration), send an email notification.  
  6. Sleep, then repeat on a configurable interval.

---

## ✨ Features

- **Headless scraping** of JavaScript/Angular-powered pages via Selenium.
- **Configurable CSS selector** to target any element whose text you want checked.
- **Email notification** through a standard SMTP server (e.g., Gmail with App Password).
- **Configurable polling interval** (default: once every hour).
- **Alert flagging** so you won’t receive duplicate alerts until the value goes below threshold and back above again.
- **Easy to customize**—just edit a few constants or environment variables.

---

## 📋 Prerequisites

1. **Python 3.7+** installed on your system.  
2. **Google Chrome** (or Chromium) installed and on your PATH (or you must specify its full path in `chrome_opts.binary_location`).  
3. **pip** (Python package installer).  
4. A **Gmail account** (or any SMTP server) with an App Password (for Gmail, see below).
5. (Optional) A **Google App Password** if using Gmail.  
   - Visit your Google Account → Security → App passwords → “Mail” × "Other" → Generate → Copy the 16-character password.

---

## 📥 Installation

1. **Clone or download** this repository to your local machine.
2. Open a terminal and navigate into the project folder:
   ```bash
   cd /path/to/WebValueWatcher
   ```
3. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS/Linux
   # or
   venv\Scripts\Activate         # Windows PowerShell/CMD
   ```
4. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   If there is no `requirements.txt`, install manually:
   ```bash
   pip install selenium webdriver-manager
   ```

---

## ⚙️ Configuration

Open `scrape.py` in your favorite editor. At the top you will find a **Configuration** block. Adjust the following constants:

```python
# ─────────────────────────────────────────────────────────────────────────────
# 1. CONFIGURATION (edit these!)
# ─────────────────────────────────────────────────────────────────────────────

URL_TO_CHECK      = "https://www.dira.moch.gov.il/ProjectsList"
CSS_SELECTOR      = "b.blue-label.col-md-1.count.ng-binding"

CHECK_INTERVAL_SEC = 60 * 60   # check every 1 hour (default)

# Email (SMTP)
SMTP_SERVER    = "smtp.gmail.com"
SMTP_PORT      = 587
SMTP_USER      = os.getenv("SMTP_USER")      # e.g., "youremail@gmail.com"
SMTP_PASS      = os.getenv("SMTP_PASS")      # your App Password
SENDER_ADDR    = "youremail@gmail.com"
RECIPIENT_ADDR = "recipient@example.com"
```

- **`URL_TO_CHECK`**:  
  The exact webpage URL you want to monitor.  
- **`CSS_SELECTOR`**:  
  A CSS selector string that matches the element containing the numeric value.  
  – For Angular/JS pages, Selenium must render the DOM first.  
  — Example:  
  ```css
  div.ng-binding.ng-scope[ng-if="project.LotteryApparmentsNum != -1"]
  ```  
  or  
  ```css
  b.blue-label.col-md-1.count.ng-binding
  ```  
- **`CHECK_INTERVAL_SEC`**:  
  Delay between checks, in seconds. Default = 3600 (1 hour).  
- **SMTP / Email fields**:  
  – `SMTP_SERVER`: your SMTP host (e.g., `smtp.gmail.com`).  
  – `SMTP_PORT`: usually 587 (TLS) for Gmail.  
  – `SMTP_USER`: environment variable → your Gmail address.  
  – `SMTP_PASS`: environment variable → your Gmail App Password (16 chars).  
  – `SENDER_ADDR`: the “From” address (match your Gmail).  
  – `RECIPIENT_ADDR`: the “To” address (where you receive alerts).

> **Important**: For Gmail, you must enable 2-Step Verification and create an **App Password**; do not use your regular Gmail password.

---

## 🔒 Environment Variables

It’s best practice to store sensitive credentials outside the script. In your terminal/PowerShell (before running `scrape.py`), set:

### On macOS/Linux (bash/zsh)

```bash
export SMTP_USER="yourusername@gmail.com"
export SMTP_PASS="your_16_character_app_password"
```

### On Windows (PowerShell)

```powershell
$Env:SMTP_USER = "yourusername@gmail.com"
$Env:SMTP_PASS = "your_16_character_app_password"
```

After setting those, verify:

```bash
echo $SMTP_USER   # should print yourusername@gmail.com
echo $SMTP_PASS   # should print the 16-char password
```

*(In Windows CMD, use `set SMTP_USER=...` instead of `export`.)*

---

## 🚀 Usage

1. Ensure environment variables are set (see above).  
2. (Optional) Activate your virtual environment.  
3. Run the script:
   ```bash
   python scrape.py
   ```

   You should see output like:

   ```
   [INFO] Checking https://www.dira.moch.gov.il/ProjectsList …
   [INFO] Fetched value = 0.0
   [INFO] Sleeping for 3600 seconds…
   ```

4. If the scraped value is **≥ 0** (configurable), you will see:
   ```
   🔔 Alert: value = 0.0 > 0
   [INFO] Email notification sent.
   ```
   (And an email will be delivered to the `RECIPIENT_ADDR`.)

5. The script loops forever—checking every `CHECK_INTERVAL_SEC` seconds—until you terminate it (Ctrl+C).

---

## 🛠️ How It Works

1. **`main_loop()`**:  
   - Initializes `alerted_once = False`.  
   - In a `while True` loop, calls `fetch_value_with_selenium(URL_TO_CHECK)`.  
   - Prints `[INFO] Fetched value = X`.  
   - If `X >= 0 and not alerted_once`, it:  
     - Constructs an email “Subject”/“Body” and calls `send_email_notification(...)`.  
     - Sets `alerted_once = True`.  
   - If `X <= 0`, resets `alerted_once` so a new alert can run later.  
   - Sleeps for `CHECK_INTERVAL_SEC` seconds, then repeats.

2. **`fetch_value_with_selenium(url)`**:  
   - Uses Selenium’s headless Chrome to navigate to `url`.  
   - Sleeps ~3 seconds for JavaScript/Angular to populate the DOM.  
   - Locates the first element matching `CSS_SELECTOR`.  
   - Reads `.text`, strips commas/spaces, and returns `float(text)`.  
   - If anything fails (no element, conversion error, Selenium error), returns `None`.

3. **`send_email_notification(...)`**:  
   - Creates a plain‐text `EmailMessage` with `From`, `To`, `Subject`, `Body`.  
   - Connects to `smtp.gmail.com:587` with `starttls()`.  
   - Calls `server.login(SMTP_USER, SMTP_PASS)`.  
   - Sends the email. Returns `True` on success or `False` if an exception is raised.

---

## 📝 Sample Output

```
[INFO] Checking https://www.dira.moch.gov.il/ProjectsList …
[INFO] Fetched value = 0.0
[INFO] Sleeping for 3600 seconds…

# …60 minutes pass…

[INFO] Checking https://www.dira.moch.gov.il/ProjectsList …
🔔 Alert: value = 2.0 > 0
[INFO] Email notification sent.
[INFO] Sleeping for 3600 seconds…

# Next loop, if value remains >0, alerted_once=True → no new email until it drops below 0…
```

---

## 🔧 Customization & Tips

- **Change the CSS selector** to target any element on any Angular/JS page.  
  - Example (Lottery apartments):  
    ```css
    div.ng-binding.ng-scope[ng-if="project.LotteryApparmentsNum != -1"]
    ```  
  - If you want **all** matching rows, replace `find_element` with `find_elements` and return a list of ints.

- **Adjust `CHECK_INTERVAL_SEC`** to your desired polling frequency:  
  - e.g., `60 * 5` for every 5 minutes, or `60 * 60 * 24` for once per day.  
- **Set a longer `sleep()` in `fetch_value_with_selenium`** if the page takes more than 3 seconds to load. Alternatively, use `WebDriverWait` for a specific DOM element.  
- **Change `if val >= 0` to `if val > 0`** if you only want alerts when the number is strictly positive.  
- **Logging**: Feel free to swap `print(...)` calls for a proper `logging` module setup.

---

## 📥 Deployment Options

1. **Run locally** (leave a terminal open):  
   ```bash
   python scrape.py
   ```  
   – Keeps your laptop/server awake.

2. **GitHub Actions** (no server required):  
   - Store `scrape.py` in a GitHub repo.  
   - Add a workflow (`.github/workflows/daily_check.yml`) that runs on a cron schedule.  
   - Save `SMTP_USER` and `SMTP_PASS` as GitHub Secrets.  
   - GitHub will spin up an Ubuntu runner daily (or hourly) and execute your script.

3. **PythonAnywhere** (free tier):  
   - Upload `scrape.py`.  
   - Under “Tasks,” schedule it to run once a day or every hour.  
   - In their **Environment Variables** section, set `SMTP_USER`/`SMTP_PASS`.  
   - PythonAnywhere will run the script even if your PC is off.

4. **VPS / Small Cloud VM** (e.g., DigitalOcean $5/month):  
   - Install Python, Chrome + ChromeDriver.  
   - Cron-tab the execution:
     ```cron
     0 * * * * /usr/bin/python3 /home/you/scrape.py >> /home/you/scrape.log 2>&1
     ```
   - Script will run hourly (or daily), and logs append to `scrape.log`.

---

## 🛡️ Troubleshooting

- **“cannot find Chrome binary”**  
  – Make sure Chrome is installed.  
  – If Chrome is installed but not on your PATH, set:
  ```python
  chrome_opts.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
  ```
  (or the correct path for your OS).  
- **“ValueError: Could not convert … to float”**  
  – The element’s `.text` may not be purely numeric. Inspect in DevTools to confirm the raw text. Remove extra characters or adjust the CSS selector.  
- **“BadCredentials”** from Gmail SMTP  
  – You must use a 16-character App Password (not your normal Gmail password).  
  – Enable Two-Step Verification → create an App Password → store it in `SMTP_PASS`.  
- **`val` always `None` or no element found**  
  – Increase `time.sleep(3)` to 5–7 seconds.  
  – Use DevTools → “View Source” vs. “Inspect” to verify if the element is truly in the static HTML or only injected by JS. If it’s injected, Selenium is required; if it’s in raw HTML, you could also use `requests + BeautifulSoup`.

---

## 📚 Further Reading

- **Selenium Python docs**:  
  https://selenium-python.readthedocs.io/  
- **webdriver-manager**:  
  https://github.com/SergeyPirogov/webdriver_manager  
- **Gmail App Passwords**:  
  https://support.google.com/accounts/answer/185833  
- **Angular/JS scraping pitfalls**:  
  – Understanding Rendered vs. Static HTML  
  – Using `WebDriverWait` for robust element detection

---

## 📜 License

This project is released under the **MIT License**. See `LICENSE` for more details.

---

> Crafted with ❤️ for a robust, headless scraping + alert solution. Happy monitoring!
