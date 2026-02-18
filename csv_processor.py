import csv
import re

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def process_csv(file_path):
    valid_records = []
    invalid_records = []

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = row.get('Name', '').strip()
            email = row.get('Email', '').strip()
            role = row.get('Role', '').strip()
            domain = row.get('Domain', '').strip()

            if not name or not email or not role or not domain:
                invalid_records.append(row)
                continue

            if not is_valid_email(email):
                invalid_records.append(row)
                continue

            valid_records.append({
                "Name": name,
                "Email": email,
                "Role": role,
                "Domain": domain
            })

    return valid_records, invalid_records


if __name__ == "__main__":
    valid, invalid = process_csv("users.csv")

    print("VALID RECORDS:")
    for v in valid:
        print(v)

    print("\nINVALID RECORDS:")
    for i in invalid:
        print(i)
