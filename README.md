# Daily Webpage Check

## Overview

This project provides an automated way to monitor a specific webpage for updates (in this case, the number of apartment raffles open for registration) and send an email notification when new raffles become available. It consists of:

- **`scrape.py`**: A Python script that uses Selenium to fetch a numeric value from a target webpage. If the value exceeds zero, it sends an email notification.
- **`.github/workflows/daily_check.yml`**: A GitHub Actions workflow that schedules a daily run of `scrape.py`, ensuring the check happens automatically on a remote server.

## Contents

- `scrape.py` – Main Python script for scraping and email alerts.
- `.github/workflows/daily_check.yml` – GitHub Actions configuration to run the script once per day.
- `README.md` – This file.

## Prerequisites

- **Python 3.12**  
  Ensure you have Python 3.12 installed on your system or use the GitHub Actions runner.

- **Dependencies**  
  The script relies on:
  - `selenium`
  - `webdriver-manager`

  You can install these via pip:

  ```bash
  pip install selenium webdriver-manager
  ```

- **Chrome Browser**  
  The script runs Google Chrome in headless mode. The `webdriver-manager` automatically handles downloading the compatible ChromeDriver.

- **Gmail SMTP Credentials**  
  The script expects the following environment variable:
  - `SMTP_PASS`: The SMTP password (app-specific password if using Gmail’s two-step verification).

  Additionally, the Gmail user is hardcoded as:
  ```
  alonnergaon0@gmail.com
  ```

## Configuration

1. **Environment Variable**  
   Before running `scrape.py`, set the `SMTP_PASS` environment variable. For example:

   ```bash
   export SMTP_PASS="your_gmail_app_password"
   ```

2. **Adjusting Target URL or CSS Selector**  
   - In `scrape.py`, you can modify:
     ```python
     URL_TO_CHECK = "https://www.dira.moch.gov.il/ProjectsList"
     CSS_SELECTOR  = "b.blue-label.col-md-1.count.ng-binding"
     ```
   - Replace with the target webpage and CSS selector you want to monitor.

## Usage

To run the scraping script locally:

```bash
python3 scrape.py
```

- The script will:
  1. Open a headless Chrome browser.
  2. Navigate to the URL specified.
  3. Wait for JavaScript-rendered content to load.
  4. Extract a numeric value from the specified element.
  5. If the value is greater than zero (and you haven’t already been alerted for this “opening”), send an email notification to `alonnergaon0@gmail.com`.

## GitHub Actions Integration

The `daily_check.yml` workflow (located under `.github/workflows/`) automates running `scrape.py` once per day at midnight UTC. It includes:

1. **Checkout**: Fetches the repository’s code.
2. **Python Setup**: Installs Python 3.12 on the runner.
3. **Dependency Installation**: Installs `selenium` and `webdriver-manager`.
4. **Execution**: Runs `scrape.py` with `SMTP_PASS` pulled from GitHub Secrets.

### Setting Up Secrets

1. Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**.
2. Click **New repository secret**.
3. Add `SMTP_PASS` with your Gmail app password as the value.

Once set, the workflow will automatically pick up the secret and use it when running the script.