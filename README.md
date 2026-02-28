# 🏦 Banking System with AI Advisor
**By Devankit Shukla**

A Python banking system with OOP architecture, Flask web dashboard, JSON persistence, and an AI investment advisor powered by Anthropic Claude.

---

## ✨ Features

- **5 Account Types** — Standard, Savings, Interest Reward, Joint, Fixed Deposit
- **Full Transactions** — Deposit, Withdraw, Transfer with validation
- **Transaction History** — Timestamped logs for every action
- **JSON Persistence** — Data saved to `bank_data.json`, survives restarts
- **AI Investment Advisor** — Personalised advice powered by Claude AI
- **Web Dashboard** — Beautiful Flask-powered UI at `localhost:5000`
- **Interactive CLI** — Menu-driven terminal interface

---

## 🗂️ Project Structure

```
banking-project/
├── app.py            # Flask web server (run this for the dashboard)
├── main.py           # CLI entry point
├── oop.py            # All account classes (OOP core)
├── ai_advisor.py     # Claude AI integration
├── storage.py        # JSON save/load
├── requirements.txt  # Python dependencies
├── templates/
│   └── index.html    # Web dashboard UI
├── .env              # Your API key (never commit this!)
├── .gitignore        # Keeps .env off GitHub
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/devankitshukla/banking-project.git
cd banking-project
```

### 2. Create virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
Create a `.env` file in the project root:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```
Get your free key at: https://console.anthropic.com

### 5. Run the web dashboard
```bash
python app.py
```
Open **http://localhost:5000** in your browser.

### 6. Or run the CLI
```bash
python main.py
```

---

## 🧠 OOP Concepts Demonstrated

```
BankAccount                     ← Base class
├── InterestRewardAccount       ← Overrides deposit() (+5% bonus)
│   └── SavingAccount           ← Adds withdrawal fee + monthly interest
├── JointAccount                ← Multi-owner support
└── FixedDepositAccount         ← Locks funds, loyalty-based rates
```

**Concepts:** Encapsulation, Inheritance, Polymorphism, Custom Exceptions, Class vs Instance Variables, JSON Serialization, REST API, Flask routing

---

## 🤖 AI Advisor

Analyzes each account's spending and gives:
- Financial health assessment
- 3 personalized investment recommendations  
- Actionable savings tip

Works for real accounts OR any custom person (enter name + numbers manually).

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/accounts` | List all accounts |
| POST | `/api/accounts` | Create new account |
| POST | `/api/accounts/<name>/deposit` | Deposit money |
| POST | `/api/accounts/<name>/withdraw` | Withdraw money |
| POST | `/api/accounts/<name>/transfer` | Transfer to another account |
| POST | `/api/accounts/<name>/interest` | Apply monthly interest |
| GET | `/api/accounts/<name>/ai-advice` | Get AI advice for account |
| POST | `/api/ai-advice/custom` | Get AI advice for custom person |
