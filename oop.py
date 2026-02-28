"""
oop.py — Core Banking Classes
Banking Project by Devankit Shukla

Concepts used:
- OOP: Classes, Inheritance, Encapsulation
- Custom Exceptions
- Class variables vs instance variables
- Method overriding (polymorphism)
"""

from datetime import datetime, timedelta


# ─────────────────────────────────────────────
# CUSTOM EXCEPTION
# Why: Instead of crashing with a generic error, we define our OWN
#      error type so we can catch it specifically.
# ─────────────────────────────────────────────
class BalanceException(Exception):
    pass


# ─────────────────────────────────────────────
# BASE CLASS: BankAccount
# ─────────────────────────────────────────────
class BankAccount:
    """
    The foundation class. All account types inherit from this.
    
    Key OOP concept: 
    - account_counter is a CLASS variable (shared across ALL instances)
    - self.balance is an INSTANCE variable (unique to each object)
    """
    account_counter = 1000  # Class variable — auto-increments for each new account

    def __init__(self, initialAmount, accountName, location):
        self.balance = initialAmount
        self.name = accountName
        self.location = location
        self.transactions = []          # Each account keeps its own transaction list
        self.date_of_opening = datetime.now()
        self.account_number = BankAccount.account_counter
        BankAccount.account_counter += 1  # Increment BEFORE next account is created

        print(f"\n✅ Account '{self.name}' created successfully.")
        print(f"   Account #: {self.account_number} | Balance: ${self.balance:.2f}")
        self.log_transaction("Account Opened", initialAmount)

    # ── PRIVATE HELPER ─────────────────────────────
    def log_transaction(self, type_, amount):
        """
        Stores a record of every action taken on this account.
        We store: (timestamp, type, amount, balance AFTER the action)
        The timestamp is NOW stored and NOW shown — fixing the original bug.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append({
            "timestamp": timestamp,
            "type": type_,
            "amount": amount,
            "balance_after": self.balance
        })

    def viableTransaction(self, amount):
        """
        Guard method — raises our custom exception if funds are insufficient.
        Called BEFORE any withdrawal/transfer to stop bad transactions early.
        """
        if self.balance < amount:
            raise BalanceException(
                f"Insufficient funds. '{self.name}' has ${self.balance:.2f}, needs ${amount:.2f}."
            )

    # ── PUBLIC METHODS ─────────────────────────────
    def getBalance(self):
        print(f"   💰 {self.name}'s Balance: ${self.balance:.2f}")

    def deposit(self, amount):
        if amount <= 0:
            print("   ⚠️  Deposit amount must be positive.")
            return
        self.balance += amount
        self.log_transaction("Deposit", amount)
        print(f"\n✅ Deposited ${amount:.2f} into '{self.name}'.")
        self.getBalance()

    def withdraw(self, amount):
        try:
            self.viableTransaction(amount)
            self.balance -= amount
            self.log_transaction("Withdrawal", -amount)
            print(f"\n✅ Withdrew ${amount:.2f} from '{self.name}'.")
            self.getBalance()
        except BalanceException as error:
            print(f"\n❌ Withdrawal Failed: {error}")

    def transfer(self, amount, target_account):
        """
        Transfers money from THIS account to target_account.
        Uses withdraw() + deposit() internally — DRY principle (Don't Repeat Yourself).
        """
        try:
            print(f"\n🔄 Transferring ${amount:.2f} from '{self.name}' → '{target_account.name}'...")
            self.viableTransaction(amount)
            self.balance -= amount
            self.log_transaction(f"Transfer Out → {target_account.name}", -amount)
            target_account.balance += amount
            target_account.log_transaction(f"Transfer In ← {self.name}", amount)
            print(f"✅ Transfer Complete.")
            self.getBalance()
            target_account.getBalance()
        except BalanceException as error:
            print(f"\n❌ Transfer Failed: {error}")

    def getStatement(self):
        """Print a clean transaction history — now shows timestamps."""
        print(f"\n{'═'*55}")
        print(f"  📜 Statement for {self.name} (#{self.account_number})")
        print(f"{'═'*55}")
        print(f"  {'Date & Time':<22} {'Type':<25} {'Amount':>8}")
        print(f"  {'─'*22} {'─'*25} {'─'*8}")
        for t in self.transactions:
            sign = "+" if t["amount"] >= 0 else ""
            print(f"  {t['timestamp']:<22} {t['type']:<25} {sign}${t['amount']:.2f}")
        print(f"{'═'*55}")
        print(f"  Final Balance: ${self.balance:.2f}")
        print(f"{'═'*55}\n")

    def getInfo(self):
        """Full account summary."""
        print(f"\n{'═'*40}")
        print(f"  🏦 Account Information")
        print(f"{'═'*40}")
        print(f"  Holder:   {self.name}")
        print(f"  Number:   #{self.account_number}")
        print(f"  Type:     {type(self).__name__}")   # Shows actual class name dynamically!
        print(f"  Balance:  ${self.balance:.2f}")
        print(f"  Location: {self.location}")
        print(f"  Opened:   {self.date_of_opening.strftime('%Y-%m-%d')}")
        print(f"{'═'*40}\n")

    def get_monthly_spending(self):
        """
        Calculates total money spent (withdrawals + transfers out) this month.
        Used by the AI Advisor to analyze spending patterns.
        Returns a dict: { 'total_spent': float, 'total_deposited': float }
        """
        now = datetime.now()
        spent = 0
        deposited = 0
        for t in self.transactions:
            # Parse the timestamp string back to datetime
            t_date = datetime.strptime(t["timestamp"], "%Y-%m-%d %H:%M:%S")
            if t_date.month == now.month and t_date.year == now.year:
                if t["amount"] < 0:
                    spent += abs(t["amount"])
                elif t["type"] not in ("Account Opened",):
                    deposited += t["amount"]
        return {"total_spent": spent, "total_deposited": deposited}


# ─────────────────────────────────────────────
# CHILD CLASS: InterestRewardAccount
# Deposits earn 5% bonus interest
# ─────────────────────────────────────────────
class InterestRewardAccount(BankAccount):
    """
    Overrides deposit() to add 5% bonus.
    Key concept: METHOD OVERRIDING — child replaces parent's method.
    """
    INTEREST_BONUS = 0.05  # Class-level constant — easy to update

    def deposit(self, amount):
        if amount <= 0:
            print("   ⚠️  Deposit amount must be positive.")
            return
        bonus = amount * self.INTEREST_BONUS
        total = amount + bonus
        self.balance += total
        self.log_transaction(f"Deposit + {self.INTEREST_BONUS*100:.0f}% Bonus", total)
        print(f"\n✅ Deposited ${amount:.2f} + ${bonus:.2f} bonus = ${total:.2f} into '{self.name}'.")
        self.getBalance()


# ─────────────────────────────────────────────
# CHILD CLASS: SavingAccount
# Inherits from InterestRewardAccount (gets deposit bonus)
# + monthly fee on withdrawals + monthly interest
# ─────────────────────────────────────────────
class SavingAccount(InterestRewardAccount):
    """
    Multi-level inheritance: SavingAccount → InterestRewardAccount → BankAccount
    Adds: withdrawal fee, monthly interest rate.
    """
    def __init__(self, initialAmount, accountName, location):
        super().__init__(initialAmount, accountName, location)
        self.fee = 5.00             # Fixed fee per withdrawal
        self.interest_rate = 0.03   # 3% monthly interest

    def withdraw(self, amount):
        total_deducted = amount + self.fee
        try:
            self.viableTransaction(total_deducted)
            self.balance -= total_deducted
            self.log_transaction(f"Withdrawal (incl. ${self.fee} fee)", -total_deducted)
            print(f"\n✅ Withdrew ${amount:.2f} + ${self.fee:.2f} fee from '{self.name}'.")
            self.getBalance()
        except BalanceException as error:
            # BUG FIX: was missing f-string prefix, so {error} printed literally
            print(f"\n❌ Withdrawal Failed: {error}")

    def applyInterest(self):
        """Call this once a month to credit interest."""
        interest = self.balance * self.interest_rate
        self.balance += interest
        self.log_transaction("Monthly Interest Applied", interest)
        print(f"\n💹 Interest of ${interest:.2f} applied to '{self.name}'.")
        self.getBalance()


# ─────────────────────────────────────────────
# CHILD CLASS: JointAccount
# BUG FIX: owners is now properly a list
# ─────────────────────────────────────────────
class JointAccount(BankAccount):
    """
    An account shared between multiple people.
    BUG FIX: owners should be a list ['Alice', 'Bob'], not a single string.
    Original join() was joining characters of a single string!
    """
    def __init__(self, initialAmount, accountName, owners: list, location):
        super().__init__(initialAmount, accountName, location)
        self.owners = owners  # ['Name1', 'Name2', ...]

    def getOwners(self):
        owner_str = ", ".join(self.owners)  # Now properly joins LIST items
        print(f"   👥 Owners of '{self.name}': {owner_str}")

    def getInfo(self):
        super().getInfo()
        self.getOwners()


# ─────────────────────────────────────────────
# CHILD CLASS: FixedDepositAccount
# Higher interest rate for loyal customers
# ─────────────────────────────────────────────
class FixedDepositAccount(BankAccount):
    """
    Money locked in for a fixed duration.
    Loyal customers (existing account 6+ months old) get better rates.
    Uses simple interest: Maturity = Principal × (1 + r × t)
    """
    def __init__(self, principal, accountName, location, existing_account=None, duration_months=12):
        super().__init__(principal, accountName, location)
        self.principal = principal
        self.duration_months = duration_months

        # Business logic: reward loyalty with better rates
        if existing_account:
            age = datetime.now() - existing_account.date_of_opening
            if age >= timedelta(days=180):
                self.interest_rate = 0.075  # 7.5% for loyal customers (6+ months)
            else:
                self.interest_rate = 0.05   # 5% for newer customers
        else:
            self.interest_rate = 0.025      # 2.5% default rate

        self.maturity_amount = self._calculate_maturity()
        self.log_transaction("Fixed Deposit Opened", principal)

    def _calculate_maturity(self):
        """Simple Interest: A = P(1 + r*t) where t = duration in years"""
        return self.principal * (1 + self.interest_rate * (self.duration_months / 12))

    def withdraw(self, amount):
        """FDs cannot be withdrawn early — penalty message."""
        print("   🔒 Fixed Deposit accounts cannot be withdrawn before maturity.")

    def showDetails(self):
        print(f"\n{'═'*45}")
        print(f"  📊 Fixed Deposit Details — {self.name}")
        print(f"{'═'*45}")
        print(f"  Principal:       ${self.principal:.2f}")
        print(f"  Duration:        {self.duration_months} months")
        print(f"  Interest Rate:   {self.interest_rate*100:.2f}%")
        print(f"  Maturity Amount: ${self.maturity_amount:.2f}")
        print(f"  Profit:          ${self.maturity_amount - self.principal:.2f}")
        print(f"  Opened:          {self.date_of_opening.strftime('%Y-%m-%d')}")
        print(f"{'═'*45}\n")
