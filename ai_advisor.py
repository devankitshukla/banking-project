"""
ai_advisor.py — AI-Powered Investment Advisor
Banking Project by Devankit Shukla

Uses Anthropic Claude API.
────
"""

import json
import os
import urllib.request
import urllib.error


def get_investment_advice(account_name: str, balance: float, monthly_data: dict) -> str:
    """
    Sends financial data to Claude AI and returns investment advice.

    Parameters:
        account_name  : Person's name
        balance       : Current account balance
        monthly_data  : Dict with 'total_spent' and 'total_deposited' this month

    Returns:
        String containing AI-generated investment advice
    """

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return (
            "⚠️  No Anthropic API key found.\n"
            "1. Get your key at: https://console.anthropic.com\n"
            "2. Add to your .env file:  ANTHROPIC_API_KEY=sk-ant-your-key-here"
        )

    total_spent     = monthly_data.get("total_spent", 0)
    total_deposited = monthly_data.get("total_deposited", 0)
    monthly_savings = total_deposited - total_spent

    prompt = f"""You are a friendly and knowledgeable personal finance advisor helping regular people.

Here is the financial profile of your client:
- Name: {account_name}
- Current Account Balance: ${balance:.2f}
- This Month's Deposits (income): ${total_deposited:.2f}
- This Month's Spending: ${total_spent:.2f}
- This Month's Net Savings: ${monthly_savings:.2f}

Please provide:
1. A brief assessment of their financial health (2-3 sentences)
2. Three specific investment recommendations suitable for their savings level
3. One actionable tip to improve their savings rate

Keep your advice practical, friendly, and under 200 words."""

    payload = {
        "model": "claude-haiku-4-5-20251001",
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}]
    }

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=data,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["content"][0]["text"]

    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            error_json = json.loads(body)
            message = error_json.get("error", {}).get("message", body)
        except Exception:
            message = body
        return f"⚠️  Anthropic API Error {e.code}: {message}"

    except Exception as e:
        return f"⚠️  Could not reach AI Advisor: {e}"


def display_ai_advice(account):
    """
    Takes a BankAccount object, extracts spending data,
    and prints AI-generated investment advice.
    """
    print(f"\n{'═'*55}")
    print(f"  🤖 AI Investment Advisor — Report for {account.name}")
    print(f"{'═'*55}")

    monthly_data = account.get_monthly_spending()
    advice = get_investment_advice(account.name, account.balance, monthly_data)

    print(f"\n{advice}\n")
    print(f"{'═'*55}\n")


# ─────────────────────────────────────────────
# DEMO PROFILES — Test the AI with fake people
# ─────────────────────────────────────────────

DEMO_PROFILES = {
    "student": {
        "name": "Rahul (Student)",
        "balance": 8000.00,
        "monthly_data": {"total_deposited": 5000.00, "total_spent": 4200.00},
    },
    "freelancer": {
        "name": "Priya (Freelancer)",
        "balance": 45000.00,
        "monthly_data": {"total_deposited": 25000.00, "total_spent": 18000.00},
    },
    "salaried": {
        "name": "Amit (Salaried Employee)",
        "balance": 120000.00,
        "monthly_data": {"total_deposited": 60000.00, "total_spent": 38000.00},
    },
    "broke": {
        "name": "Vikram (Struggling)",
        "balance": 500.00,
        "monthly_data": {"total_deposited": 15000.00, "total_spent": 16200.00},
    },
    "rich": {
        "name": "Sneha (High Earner)",
        "balance": 900000.00,
        "monthly_data": {"total_deposited": 200000.00, "total_spent": 80000.00},
    },
}


def demo_advice(profile: str = "student"):
    """
    Test the AI advisor with a preset demo profile.
    No real account needed.

    Usage:
        demo_advice("student")
        demo_advice("freelancer")
        demo_advice("salaried")
        demo_advice("broke")
        demo_advice("rich")
    """
    profile = profile.lower()

    if profile not in DEMO_PROFILES:
        print(f"⚠️  Unknown profile '{profile}'.")
        print(f"   Available: {', '.join(DEMO_PROFILES.keys())}")
        return

    p = DEMO_PROFILES[profile]
    total_deposited = p["monthly_data"]["total_deposited"]
    total_spent     = p["monthly_data"]["total_spent"]
    savings         = total_deposited - total_spent

    print(f"\n{'═'*55}")
    print(f"  🤖 AI Advisor — Demo Profile: {p['name']}")
    print(f"{'═'*55}")
    print(f"  Balance   : ₹{p['balance']:,.2f}")
    print(f"  Income    : ₹{total_deposited:,.2f}/month")
    print(f"  Spending  : ₹{total_spent:,.2f}/month")
    print(f"  Savings   : ₹{savings:,.2f}/month")
    print(f"{'─'*55}")

    advice = get_investment_advice(p["name"], p["balance"], p["monthly_data"])
    print(f"\n{advice}\n")
    print(f"{'═'*55}\n")


def demo_all():
    """Run AI advice for ALL demo profiles at once."""
    for profile in DEMO_PROFILES:
        demo_advice(profile)


def custom_advice():
    """
    Ask the user to enter any person's name and financial details,
    then get personalised AI investment advice for that person.
    """
    print(f"\n{'─'*55}")
    print("  🤖 AI Advisor — Custom Person")
    print(f"{'─'*55}")

    name = input("  Enter person's name          : ").strip()
    if not name:
        print("  ⚠️  Name cannot be empty.")
        return

    try:
        balance   = float(input("  Current account balance (₹)  : "))
        deposited = float(input("  Monthly income/deposits (₹)  : "))
        spent     = float(input("  Monthly spending (₹)          : "))
    except ValueError:
        print("  ⚠️  Please enter valid numbers.")
        return

    savings = deposited - spent

    print(f"\n  Summary for {name}:")
    print(f"  Balance  : ₹{balance:,.2f}")
    print(f"  Income   : ₹{deposited:,.2f}/month")
    print(f"  Spending : ₹{spent:,.2f}/month")
    print(f"  Savings  : ₹{savings:,.2f}/month")
    print(f"{'─'*55}")
    print("  Fetching AI advice...\n")

    monthly_data = {"total_deposited": deposited, "total_spent": spent}
    advice = get_investment_advice(name, balance, monthly_data)

    print(advice)
    print(f"{'═'*55}\n")