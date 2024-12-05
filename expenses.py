import csv
import click

from decimal import Decimal
from collections import defaultdict
from pathlib import Path

class MonthEntry(object):
    def __init__(self):
        self.credits = Decimal(0)
        self.debits = Decimal(0)

field_names = ["date", "memo", "debit", "credit"]
IGNORE_LIST = ["MORTGAGE", "TFR-TO C/C", "PAYMENT - THANK YOU"]
global_months = defaultdict(MonthEntry)

@click.command()
@click.argument("directory")
def run(directory):
    p = Path(directory)
    for file in p.iterdir():
        process_file(file)
    print("TOTAL")
    for month,entry in global_months.items():
        print(f"{month}")
        print(f"Debits: {entry.debits}")
        print(f"Credits: {entry.credits}")
        print(f"Surplus: {entry.credits - entry.debits}")
        print("")

def process_file(file):
    print(file)
    with open(file, 'r', newline='') as f:
        reader = csv.DictReader(f, fieldnames=field_names)
        single_file_months = process_entries(reader, IGNORE_LIST)
        for month,entry in single_file_months.items():
            global_months[month].debits += entry.debits
            global_months[month].credits += entry.credits

def check_match(elem, ignore_list):
    for ignore_text in ignore_list:
        if ignore_text in elem["memo"]:
            return False
    return True

def process_entries(entries, ignore_list):
    filtered_entries = filter(lambda elem: check_match(elem, ignore_list), entries)
    months = defaultdict(MonthEntry)

    for entry in filtered_entries:
        debit = entry["debit"]
        credit = entry["credit"]
        month = entry["date"][0:2]+"-"+entry["date"][-4:]
        if debit:
            months[month].debits += Decimal(debit)
        elif credit:
            months[month].credits += Decimal(credit)
        else:
            print("Error processing entry, skipping: {entry}")

    return months

if __name__ == "__main__":
    run()
