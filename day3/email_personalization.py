from string import Template
import csv
import os

def load_template(template_path):
    # Read template with UTF-8 encoding to avoid character issues
    with open(template_path, 'r', encoding="utf-8") as file:
        return Template(file.read())

def generate_emails(csv_path, template):
    personalized_emails = []

    with open(csv_path, 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            # Skip rows with missing required fields
            if not row.get('Name') or not row.get('Email'):
                continue

            email_content = template.safe_substitute({
                "Name": row.get("Name"),
                "Domain": row.get("Domain"),
                "Role": row.get("Role")
            })

            personalized_emails.append({
                "email": row.get("Email"),
                "content": email_content
            })

    return personalized_emails


if __name__ == "__main__":
    # Paths resolved relative to project structure
    template_path = "email_template.txt"     # inside day3/
    csv_path = "../users.csv"                # project root

    template = load_template(template_path)
    emails = generate_emails(csv_path, template)

    for mail in emails:
        print("To:", mail["email"])
        print(mail["content"])
        print("-" * 40)