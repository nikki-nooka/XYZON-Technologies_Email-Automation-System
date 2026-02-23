import smtplib
import csv
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from string import Template
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "day4"))

from email_config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD
# -------- DAY 6 OPTIMIZATION SETTINGS --------
RATE_LIMIT_SECONDS = 2       # Spam prevention
MAX_EMAILS_PER_RUN = 10      # Batch control
# --------------------------------------------


def load_template(path):
    with open(path, "r", encoding="utf-8") as file:
        return Template(file.read())


def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        return "Sent"
    except Exception as e:
        return f"Failed: {e}"


def optimized_bulk_send(csv_path, template):
    results = []
    sent_count = 0

    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if sent_count >= MAX_EMAILS_PER_RUN:
                break

            email = row.get("Email")

            # Email validation (spam prevention)
            if not email or "@" not in email:
                results.append((email, "Failed: Invalid email"))
                continue

            # Email body personalization (Day 3 logic reused)
            content = template.safe_substitute(
                Name=row.get("Name"),
                Domain=row.get("Domain"),
                Role=row.get("Role")
            )

            # -------- DAY 6 SUBJECT PERSONALIZATION --------
            subject = f"{row.get('Name')}, Opportunity in {row.get('Domain')} Domain"
            body = content.split("\n", 1)[1]
            # ----------------------------------------------

            status = send_email(email, subject, body)
            results.append((email, status))

            sent_count += 1

            # -------- DAY 6 RATE LIMITING --------
            time.sleep(RATE_LIMIT_SECONDS)
            # ------------------------------------

    return results


if __name__ == "__main__":
    template_path = os.path.join(BASE_DIR, "day3", "email_template.txt")
    csv_path = os.path.join(BASE_DIR, "users.csv")
    template = load_template(template_path)
    results = optimized_bulk_send(csv_path, template)

    for email, status in results:
        print(email, "→", status)