# data_handler.py

import csv
import os

CSV_FILE = "budget_data.csv"

def save_entry(entry):
    os.makedirs("data", exist_ok=True)
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["amount", "category", "type", "date"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(entry)

def load_entries():
    if not os.path.exists(CSV_FILE):
        return []

    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]
