import csv
from datetime import datetime

def save_status_report(results, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Email", "Status", "Timestamp"])

        for email, status in results:
            writer.writerow([email, status, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])


if __name__ == "__main__":
    # Sample results taken from Day 4 execution
    results = [
        ("nookanikki2k06@gmail.com", "Sent"),
        ("ananya@gmail.com", "Sent"),
        ("rohit@", "Failed: Invalid email")
    ]

    save_status_report(results, "day5/email_status_report.csv")
    print("Email status report generated successfully.")