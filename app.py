"""
app.py — Flask Web Dashboard Backend
Banking Project by Devankit Shukla

Run with:  python app.py
Opens at:  http://localhost:5000
"""

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from dotenv import load_dotenv
from oop import BankAccount, SavingAccount, InterestRewardAccount, JointAccount, FixedDepositAccount
from storage import save_accounts, load_accounts
from ai_advisor import get_investment_advice

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load existing accounts from JSON file, or start fresh
accounts = load_accounts()

# ── Helper ──────────────────────────────────────────────────────────────────

def account_to_dict(acc):
    """Convert a BankAccount object to a plain dict for JSON response."""
    return {
        "name":         acc.name,
        "type":         type(acc).__name__,
        "balance":      round(acc.balance, 2),
        "location":     acc.location,
        "account_number": acc.account_number,
        "date_opened":  acc.date_of_opening.strftime("%Y-%m-%d"),
        "owners":       getattr(acc, "owners", []),
        "interest_rate": getattr(acc, "interest_rate", 0),
        "transactions": acc.transactions,
    }

# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/accounts", methods=["GET"])
def get_accounts():
    return jsonify([account_to_dict(a) for a in accounts.values()])

@app.route("/api/accounts", methods=["POST"])
def create_account():
    d = request.json
    name     = d.get("name", "").strip()
    amount   = float(d.get("amount", 0))
    location = d.get("location", "").strip()
    acc_type = d.get("type", "BankAccount")
    owners   = d.get("owners", [])

    if not name or amount < 0 or not location:
        return jsonify({"error": "Invalid input"}), 400
    if name in accounts:
        return jsonify({"error": f"Account '{name}' already exists"}), 400

    type_map = {
        "BankAccount":          BankAccount,
        "SavingAccount":        SavingAccount,
        "InterestRewardAccount": InterestRewardAccount,
        "JointAccount":         JointAccount,
        "FixedDepositAccount":  FixedDepositAccount,
    }
    AccountClass = type_map.get(acc_type, BankAccount)

    if acc_type == "JointAccount":
        acc = JointAccount(amount, name, owners, location)
    else:
        acc = AccountClass(amount, name, location)

    accounts[name] = acc
    save_accounts(accounts)
    return jsonify(account_to_dict(acc)), 201

@app.route("/api/accounts/<name>/deposit", methods=["POST"])
def deposit(name):
    if name not in accounts:
        return jsonify({"error": "Account not found"}), 404
    amount = float(request.json.get("amount", 0))
    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400
    accounts[name].deposit(amount)
    save_accounts(accounts)
    return jsonify(account_to_dict(accounts[name]))

@app.route("/api/accounts/<name>/withdraw", methods=["POST"])
def withdraw(name):
    if name not in accounts:
        return jsonify({"error": "Account not found"}), 404
    amount = float(request.json.get("amount", 0))
    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400
    acc = accounts[name]
    fee = getattr(acc, "fee", 0)
    total = amount + fee
    if acc.balance < total:
        return jsonify({"error": f"Insufficient funds. Balance: ${acc.balance:.2f}, Need: ${total:.2f}"}), 400
    acc.withdraw(amount)
    save_accounts(accounts)
    return jsonify(account_to_dict(acc))

@app.route("/api/accounts/<name>/transfer", methods=["POST"])
def transfer(name):
    if name not in accounts:
        return jsonify({"error": "Source account not found"}), 404
    d      = request.json
    amount = float(d.get("amount", 0))
    target = d.get("target", "")
    if target not in accounts:
        return jsonify({"error": "Target account not found"}), 404
    if accounts[name].balance < amount:
        return jsonify({"error": "Insufficient funds"}), 400
    accounts[name].transfer(amount, accounts[target])
    save_accounts(accounts)
    return jsonify({
        "from": account_to_dict(accounts[name]),
        "to":   account_to_dict(accounts[target]),
    })

@app.route("/api/accounts/<name>/interest", methods=["POST"])
def apply_interest(name):
    if name not in accounts:
        return jsonify({"error": "Account not found"}), 404
    acc = accounts[name]
    if not hasattr(acc, "applyInterest"):
        return jsonify({"error": "This account type does not support interest"}), 400
    acc.applyInterest()
    save_accounts(accounts)
    return jsonify(account_to_dict(acc))

@app.route("/api/accounts/<name>/ai-advice", methods=["GET"])
def ai_advice(name):
    if name not in accounts:
        return jsonify({"error": "Account not found"}), 404
    acc          = accounts[name]
    monthly_data = acc.get_monthly_spending()
    advice       = get_investment_advice(acc.name, acc.balance, monthly_data)
    return jsonify({"advice": advice, "account": account_to_dict(acc)})

@app.route("/api/ai-advice/custom", methods=["POST"])
def custom_ai_advice():
    d            = request.json
    name         = d.get("name", "User")
    balance      = float(d.get("balance", 0))
    deposited    = float(d.get("deposited", 0))
    spent        = float(d.get("spent", 0))
    monthly_data = {"total_deposited": deposited, "total_spent": spent}
    advice       = get_investment_advice(name, balance, monthly_data)
    return jsonify({"advice": advice})

if __name__ == "__main__":
    print("\n🏦  Banking Dashboard running at http://localhost:5000\n")
    app.run(debug=True, port=5000)