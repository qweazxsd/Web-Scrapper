import argparse
import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from twilio.rest import Client


def fetch_value(url: str, selector: str) -> float:
    """Fetch the numeric value from the given page using the CSS selector."""
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    element = soup.select_one(selector)
    if element is None:
        raise ValueError(f"Element '{selector}' not found")
    text = element.get_text(strip=True)
    try:
        return float(text)
    except ValueError as exc:
        raise ValueError(
            f"Element '{selector}' does not contain a numeric value: '{text}'"
        ) from exc


def send_email(to_addr: str, subject: str, body: str) -> None:
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    username = os.getenv("SMTP_USERNAME")
    password = os.getenv("SMTP_PASSWORD")
    if not host or not username or not password:
        raise RuntimeError("SMTP credentials are not fully configured")

    msg = EmailMessage()
    msg["From"] = username
    msg["To"] = to_addr
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)


def send_whatsapp(to_number: str, message: str) -> None:
    sid = os.getenv("TWILIO_SID")
    token = os.getenv("TWILIO_TOKEN")
    from_number = os.getenv("TWILIO_FROM")
    if not sid or not token or not from_number:
        raise RuntimeError("Twilio credentials are not fully configured")

    client = Client(sid, token)
    client.messages.create(
        body=message,
        from_=f"whatsapp:{from_number}",
        to=f"whatsapp:{to_number}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Monitor a web page element and send notifications if its value is > 0"
        )
    )
    parser.add_argument("--url", required=True, help="Page URL to check")
    parser.add_argument(
        "--selector", required=True, help="CSS selector for the numeric element"
    )
    parser.add_argument("--email", help="Email address to notify")
    parser.add_argument("--whatsapp", help="WhatsApp phone number to notify")
    args = parser.parse_args()

    value = fetch_value(args.url, args.selector)
    print(f"Value found: {value}")
    if value > 0:
        message = (
            f"Value at {args.url} for selector '{args.selector}' is {value} (> 0)"
        )
        if args.email:
            send_email(args.email, "Web page alert", message)
        if args.whatsapp:
            send_whatsapp(args.whatsapp, message)
        if not args.email and not args.whatsapp:
            print("No notification method provided")
    else:
        print("Value <= 0; no notification sent")


if __name__ == "__main__":
    main()
