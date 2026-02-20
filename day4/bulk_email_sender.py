import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from string import Template
from email_config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD


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

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        return "Sent"
    except Exception as e:
        return f"Failed: {e}"


def bulk_send(csv_path, template):
    results = []

    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            email = row.get("Email")

            if not email or "@" not in email:
                results.append((email, "Failed: Invalid email"))
                continue

            content = template.safe_substitute(
                Name=row.get("Name"),
                Domain=row.get("Domain"),
                Role=row.get("Role")
            )

            subject, body = content.split("\n", 1)
            subject = subject.replace("Subject:", "").strip()

            status = send_email(email, subject, body)
            results.append((email, status))

    return results


if __name__ == "__main__":
    template = load_template("day3/email_template.txt")
    results = bulk_send("users.csv", template)

    for email, status in results:
        print(email, "→", status)