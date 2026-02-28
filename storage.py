"""
storage.py — Data Persistence Layer
Banking Project by Devankit Shukla

CONCEPT: Data Persistence
─────────────────────────
When your Python program stops running, ALL variables disappear from memory.
Without persistence, creating "Dhruv" with $1000 is gone the second you close the terminal.

Solution: Save data to a FILE (JSON format) on disk.
Next time you run the program, load it back from the file.

JSON (JavaScript Object Notation) is just a text format that looks like Python dicts:
  {"name": "Dhruv", "balance": 1500.00, "transactions": [...]}

Think of it like: RAM (memory) is a whiteboard. JSON file is a notebook.
Whiteboard gets erased. Notebook survives.
"""

import json
import os
from datetime import datetime

# The file where all account data lives
DATA_FILE = "bank_data.json"


def save_accounts(accounts: dict):
    """
    Converts account objects → plain Python dicts → JSON text → writes to file.
    
    Why can't we save the object directly?
    Objects live in memory. Files store text/bytes.
    We must SERIALIZE (convert object → saveable format) first.
    This is called serialization.
    """
    data = {}

    for name, account in accounts.items():
        # Extract all the info we need from the object
        account_data = {
            "class_type": type(account).__name__,   # "BankAccount", "SavingAccount", etc.
            "name": account.name,
            "balance": account.balance,
            "location": account.location,
            "account_number": account.account_number,
            "date_of_opening": account.date_of_opening.strftime("%Y-%m-%d %H:%M:%S"),
            "transactions": account.transactions,    # Already a list of dicts — easy to save

            # Extra fields for special account types
            "fee": getattr(account, "fee", None),
            "interest_rate": getattr(account, "interest_rate", None),
            "owners": getattr(account, "owners", None),
            "principal": getattr(account, "principal", None),
            "duration_months": getattr(account, "duration_months", None),
        }
        data[name] = account_data

    # json.dumps() → converts dict to JSON string
    # indent=2 → makes it human-readable (pretty printed)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"\n💾 Data saved to '{DATA_FILE}'")


def load_accounts() -> dict:
    """
    Reads JSON file → converts back to account objects.
    This is DESERIALIZATION (opposite of serialization).
    
    Returns empty dict if no save file exists yet.
    """
    # Import here to avoid circular imports
    from oop import BankAccount, SavingAccount, InterestRewardAccount, JointAccount, FixedDepositAccount

    if not os.path.exists(DATA_FILE):
        print("📂 No save file found. Starting fresh.")
        return {}

    with open(DATA_FILE, "r") as f:
        data = json.load(f)    # json.load() → converts JSON text back to Python dict

    accounts = {}

    # Map class name strings back to actual classes
    # This is called a "dispatch table" — a dict of string → class
    class_map = {
        "BankAccount": BankAccount,
        "SavingAccount": SavingAccount,
        "InterestRewardAccount": InterestRewardAccount,
        "JointAccount": JointAccount,
        "FixedDepositAccount": FixedDepositAccount,
    }

    for name, d in data.items():
        class_name = d["class_type"]
        AccountClass = class_map.get(class_name, BankAccount)

        # Reconstruct the object — suppress the "Account created" print during load
        import io, sys
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()   # Redirect output to nowhere

        if class_name == "JointAccount":
            obj = JointAccount(d["balance"], d["name"], d["owners"] or [], d["location"])
        elif class_name == "FixedDepositAccount":
            obj = FixedDepositAccount(d["balance"], d["name"], d["location"])
        else:
            obj = AccountClass(d["balance"], d["name"], d["location"])

        sys.stdout = old_stdout    # Restore normal output

        # Restore saved state
        obj.balance = d["balance"]
        obj.account_number = d["account_number"]
        obj.date_of_opening = datetime.strptime(d["date_of_opening"], "%Y-%m-%d %H:%M:%S")
        obj.transactions = d["transactions"]

        if d.get("fee") is not None:
            obj.fee = d["fee"]
        if d.get("interest_rate") is not None:
            obj.interest_rate = d["interest_rate"]

        accounts[name] = obj

    print(f"✅ Loaded {len(accounts)} account(s) from '{DATA_FILE}'")
    return accounts
