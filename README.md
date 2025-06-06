# WebValueWatcher

A Python script that uses Selenium to scrape a numeric value from a JavaScript-driven webpage and send an email alert when the value exceeds a threshold.

## Overview

- **Script**: `scrape.py`
- **Purpose**:  
  1. Launch headless Chrome.  
  2. Visit a target URL (e.g., Ministry of Construction’s project list).  
  3. Wait for JavaScript/Angular to render the DOM.  
  4. Extract a numeric value using a CSS selector.  
  5. If the value ≥ 0 (configurable), send an email notification.  
  6. Repeat at a set interval.

## Prerequisites

- **Python 3.7+**  
- **Google Chrome** installed (or Chromium).  
- **pip** and these Python packages:
  ```
  selenium
  webdriver-manager
  ```

- **Gmail account** with a 16-character App Password (if using Gmail SMTP).

## Installation

1. Clone or download this repository.
2. In the project folder, optionally create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\Activate       # Windows PowerShell/CMD
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   If no `requirements.txt`, run:
   ```bash
   pip install selenium webdriver-manager
   ```

## Configuration

Edit `scrape.py` and adjust:

```python
URL_TO_CHECK      = "https://www.dira.moch.gov.il/ProjectsList"
CSS_SELECTOR      = "b.blue-label.col-md-1.count.ng-binding"
CHECK_INTERVAL_SEC = 3600   # Interval in seconds

# SMTP settings
SMTP_SERVER    = "smtp.gmail.com"
SMTP_PORT      = 587
SMTP_USER      = os.getenv("SMTP_USER")      # e.g., "youremail@gmail.com"
SMTP_PASS      = os.getenv("SMTP_PASS")      # 16-character App Password
SENDER_ADDR    = "youremail@gmail.com"
RECIPIENT_ADDR = "recipient@example.com"
```

- **`CSS_SELECTOR`**: CSS selector for the element containing the numeric value.  
- **`CHECK_INTERVAL_SEC`**: Time between checks.  
- **SMTP fields**: Set `SMTP_USER` and `SMTP_PASS` as environment variables.

## Environment Variables

Set sensitive values in your shell:

### macOS/Linux:
```bash
export SMTP_USER="youremail@gmail.com"
export SMTP_PASS="your_app_password"
```

### Windows PowerShell:
```powershell
$Env:SMTP_USER = "youremail@gmail.com"
$Env:SMTP_PASS = "your_app_password"
```

## Usage

Run the script:
```bash
python scrape.py
```
Output example:
```
[INFO] Checking https://www.dira.moch.gov.il/ProjectsList …
[INFO] Fetched value = 0.0
[INFO] Sleeping for 3600 seconds…
```
If the value ≥ 0, an email is sent.

## Deployment Options

- **Locally**: Keep a terminal open and run `python scrape.py`.
- **GitHub Actions**: Schedule a workflow to run the script on a cron schedule.
- **PythonAnywhere**: Use their “Tasks” to run the script daily or hourly.
- **VPS**: Use a cron job on a small VPS to run the script periodically.

## Troubleshooting

- **“Cannot find Chrome binary”**: Ensure Chrome is installed and set `chrome_opts.binary_location` to the correct path.
- **Floats parsing error**: Verify the CSS selector matches the numeric element; adjust extraction as needed.
- **SMTP authentication**: Use a 16-character Gmail App Password, not your regular password.

---

© 2025 WebValueWatcher. MIT License.