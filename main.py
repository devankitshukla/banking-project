"""
main.py — Banking System Entry Point
Banking Project by Devankit Shukla

This file demonstrates:
- Creating different account types
- Performing realistic transactions
- Using the AI Advisor
- Interactive menu (optional — uncomment at bottom)
"""

# Load .env file so ANTHROPIC_API_KEY is available to ai_advisor.py
from dotenv import load_dotenv
load_dotenv()

from oop import (
    BankAccount,
    InterestRewardAccount,
    SavingAccount,
    JointAccount,
    FixedDepositAccount
)
from ai_advisor import display_ai_advice, demo_advice, demo_all, custom_advice


def divider(title=""):
    print(f"\n{'─'*50}")
    if title:
        print(f"  {title}")
        print(f"{'─'*50}")


def run_demo():
    """
    Demonstrates all account types and features.
    Think of this as a 'test script' that shows interviewers your system works.
    """

    divider("🏦 DEMO: Standard Bank Accounts")

    # BUG FIX in original: JointAccount owners should be a LIST
    Dhruv     = BankAccount(1000, "Dhruv", "Punjab")
    Jyotshna  = BankAccount(1500, "Jyotshna", "Delhi")

    Dhruv.deposit(500)
    Jyotshna.withdraw(150)
    Dhruv.transfer(200, Jyotshna)     # Affordable transfer
    Dhruv.transfer(2000, Jyotshna)    # Should FAIL — shows error handling

    divider("💎 DEMO: Interest Reward Account")
    Shyam = InterestRewardAccount(2000, "Shyam", "Mumbai")
    Shyam.deposit(500)                # Gets 5% bonus on deposit
    Shyam.getBalance()

    divider("💰 DEMO: Savings Account")
    Tirth = SavingAccount(3000, "Tirth", "Ahmedabad")
    Tirth.deposit(300)
    Tirth.withdraw(100)               # Includes $5 fee
    Tirth.applyInterest()             # 3% monthly interest

    divider("👥 DEMO: Joint Account")
    # BUG FIX: owners is now a list, not a bare string
    Shruti = JointAccount(1500, "Shruti & Devankit Joint", ["Shruti", "Devankit"], "Ahmedabad")
    Shruti.getOwners()
    Shruti.deposit(200)

    divider("📊 DEMO: Fixed Deposit")
    # New customer FD (no existing account)
    Tirth_FD = FixedDepositAccount(5000, "Tirth FD", "Ahmedabad", duration_months=12)
    Tirth_FD.showDetails()

    # Loyal customer FD (linked to existing account → better rate)
    Tirth_FD_loyal = FixedDepositAccount(
        10000, "Tirth Loyal FD", "Ahmedabad",
        existing_account=Tirth,   # Checks age of Tirth's account
        duration_months=24
    )
    Tirth_FD_loyal.showDetails()

    divider("📜 DEMO: Transaction Statements")
    Tirth.getStatement()
    Shyam.getStatement()

    divider("🏦 DEMO: Account Info")
    Dhruv.getInfo()
    Shyam.getInfo()
    Tirth.getInfo()
    Shruti.getInfo()

    divider("🤖 DEMO: AI Investment Advisor")
    # Simulate some transactions so advisor has data to analyze
    demo_accounts = {
        "dhruv":    Dhruv,
        "jyotshna": Jyotshna,
        "shyam":    Shyam,
        "tirth":    Tirth,
        "shruti":   Shruti,
    }
    print("  Available accounts: " + ", ".join(demo_accounts.keys()))
    choice = input("  Enter account name for AI report: ").strip().lower()

    if choice in demo_accounts:
        display_ai_advice(demo_accounts[choice])
    else:
        print(f"  ⚠️  Account '{choice}' not found. Running report for Tirth by default.")
        Tirth.deposit(2000)
        Tirth.withdraw(300)
        Tirth.withdraw(150)
        display_ai_advice(Tirth)

# ─────────────────────────────────────────────────────────
# INTERACTIVE CLI — Lets a real user control the system
# This is what makes it a real "application" vs just a script
# ─────────────────────────────────────────────────────────
def interactive_menu():
    """
    A menu-driven interface. Concept: while loop + match/case (Python 3.10+)
    This turns your script into an actual usable application.
    """
    accounts = {}  # Dict to store all accounts: {name: account_object}

    print("\n" + "═"*50)
    print("       🏦 Welcome to Devankit's Banking System")
    print("═"*50)

    while True:
        print("\nWhat would you like to do?")
        print("  1. Create Account")
        print("  2. Deposit")
        print("  3. Withdraw")
        print("  4. Transfer")
        print("  5. View Balance")
        print("  6. View Statement")
        print("  7. Get AI Investment Advice")
        print("  8. View Account Info")
        print("  9. AI Demo — preset profile")
        print("  10. AI Demo — run all profiles")
        print("  11. AI Advice — enter any person's details")
        print("  0. Exit")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            name = input("Account holder name: ").strip()
            try:
                amount = float(input("Initial deposit: $"))
            except ValueError:
                print("⚠️  Invalid amount.")
                continue
            location = input("Location: ").strip()
            print("Account type: 1=Standard  2=Savings  3=InterestReward  4=Joint")
            acc_type = input("Choose: ").strip()

            if acc_type == "1":
                accounts[name] = BankAccount(amount, name, location)
            elif acc_type == "2":
                accounts[name] = SavingAccount(amount, name, location)
            elif acc_type == "3":
                accounts[name] = InterestRewardAccount(amount, name, location)
            elif acc_type == "4":
                owners_input = input("Enter owner names separated by comma: ")
                owners = [o.strip() for o in owners_input.split(",")]
                accounts[name] = JointAccount(amount, name, owners, location)
            else:
                print("⚠️  Invalid type.")

        elif choice == "2":
            name = input("Account name: ").strip()
            if name not in accounts:
                print("⚠️  Account not found.")
                continue
            try:
                amount = float(input("Deposit amount: $"))
                accounts[name].deposit(amount)
            except ValueError:
                print("⚠️  Invalid amount.")

        elif choice == "3":
            name = input("Account name: ").strip()
            if name not in accounts:
                print("⚠️  Account not found.")
                continue
            try:
                amount = float(input("Withdrawal amount: $"))
                accounts[name].withdraw(amount)
            except ValueError:
                print("⚠️  Invalid amount.")

        elif choice == "4":
            from_name = input("Transfer FROM account: ").strip()
            to_name   = input("Transfer TO account: ").strip()
            if from_name not in accounts or to_name not in accounts:
                print("⚠️  One or both accounts not found.")
                continue
            try:
                amount = float(input("Transfer amount: $"))
                accounts[from_name].transfer(amount, accounts[to_name])
            except ValueError:
                print("⚠️  Invalid amount.")

        elif choice == "5":
            name = input("Account name: ").strip()
            if name in accounts:
                accounts[name].getBalance()
            else:
                print("⚠️  Account not found.")

        elif choice == "6":
            name = input("Account name: ").strip()
            if name in accounts:
                accounts[name].getStatement()
            else:
                print("⚠️  Account not found.")

        elif choice == "7":
            name = input("Account name: ").strip()
            if name in accounts:
                display_ai_advice(accounts[name])
            else:
                print("⚠️  Account not found.")

        elif choice == "8":
            name = input("Account name: ").strip()
            if name in accounts:
                accounts[name].getInfo()
            else:
                print("⚠️  Account not found.")

        elif choice == "0":
            print("\n👋 Thank you for using Devankit's Banking System. Goodbye!\n")
            break

        else:
            print("⚠️  Invalid choice. Please try again.")


# ─────────────────────────────────────────────────────────
# ENTRY POINT
# __name__ == "__main__" means: only run this if we're
# running this file directly (not importing it elsewhere)
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\nRun mode: 1 = Demo  |  2 = Interactive Menu")
    mode = input("Choose: ").strip()

    if mode == "1":
        run_demo()
    else:
        interactive_menu()