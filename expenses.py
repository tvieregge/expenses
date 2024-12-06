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

@click.command()
@click.argument("directory")
def run(directory):
    cumulative_records = defaultdict(MonthEntry)
    p = Path(directory)
    for file in p.iterdir():
        print(file)
        with open(file, 'r', newline='') as f:
            reader = csv.DictReader(f, fieldnames=field_names)
            cumulative_records = process_entries(reader, cumulative_records, IGNORE_LIST)

    print("TOTAL")
    for month,entry in cumulative_records.items():
        print(f"{month}")
        print(f"Debits: {entry.debits}")
        print(f"Credits: {entry.credits}")
        print(f"Surplus: {entry.credits - entry.debits}")
        print("")


def check_match(elem, ignore_list):
    for ignore_text in ignore_list:
        if ignore_text in elem["memo"]:
            return False
    return True

def process_entries(entries, records, ignore_list):
    filtered_entries = filter(lambda elem: check_match(elem, ignore_list), entries)

    for entry in filtered_entries:
        debit = entry["debit"]
        credit = entry["credit"]
        month = entry["date"][0:2]+"-"+entry["date"][-4:]
        if debit:
            records[month].debits += Decimal(debit)
        elif credit:
            records[month].credits += Decimal(credit)
        else:
            print("Error processing entry, skipping: {entry}")

    return records

if __name__ == "__main__":
    run()
