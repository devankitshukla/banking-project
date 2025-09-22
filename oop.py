from datetime import datetime, timedelta

class BalanceException(Exception):
    pass
class BankAccount:
    account_counter = 1000
   
    def __init__(self,initialAmount,accountName, location):
        self.balance = initialAmount
        self.name = accountName
        self.transactions = []   # list to track all transactions
        self.date_of_opening = datetime.now()
        self.account_number = BankAccount.account_counter
        self.location = location
        BankAccount.account_counter += 1  # auto increment account number
        
        print(f"\nAccount {self.name} is created.\nBalane = ${self.balance:.2f}")
        self.log_transaction("Account Created", initialAmount)
    def log_transaction(self, type_, amount):
        """Logs transaction details into history"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append((type_, amount, self.balance))

    def getStatement(self):
        """Print all transactions of this account"""
        print(f"\n📜 Transaction History for {self.name}:")
        for t in self.transactions:
            print(f"{t[0]}: ${t[1]:.2f}, Balance after: ${t[2]:.2f}")
            
    def getBalance(self):
        print(f"\nAccount {self.name} balance = ${self.balance:.2f}\n")
    def deposit (self,amount):
        self.balance = self.balance + amount
        self.log_transaction("Deposited amount", +(amount))
        print ("\nDeposited Succefully.")
        self.getBalance()
    def viableTrasaction(self,amount):
        if self.balance >= amount:
            return
        else:
            raise BalanceException(f"\nSorry, account '{self.name}' only has a balance of ${self.balance:.2f}")
    def withdraw(self,amount):
        try:
            self.viableTrasaction(amount)
            self.balance = self.balance - amount
            self.log_transaction("Withdrawal", -(amount))
            print("\nWithdrawl Completed !!")
            self.getBalance()
        except BalanceException as error:
            print(f"\nWithdrawal Interrupted : {error}")
    def transfer(self,amount,account):
        try:
            print("\n**********\nBegining Transfer")
            self.viableTrasaction(amount)
            self.withdraw(amount)
            account.deposit(amount)
            self.log_transaction("Transfer Succeful", -(amount))
            print("\n**********\nTransfer Completed !!!")
        except BalanceException as error:
             print("\n**********\nTransfer Interrupted!!!")
    def getInfo(self):
        """Show account summary"""
        print("\n**********\n Account Information\n**********")
        print(f"Account Holder: {self.name}")
        print(f"Account Number: {self.account_number}")
        print(f"Balance: ${self.balance:.2f}")
        print(f"Date of Opening: {self.date_of_opening.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Location: {self.location}")
class InterestRewardAccount(BankAccount):
    def deposit(self, amount):
        self.balance = self.balance + (amount*1.05)
        self.log_transaction("Withdrawal with Fee", -(amount*1.05))
        print("\nDeposit Completed !!!!")
        self.getBalance
class SavingAccount(InterestRewardAccount):
    def __init__(self, initialAmount, accountName, location ):
        super().__init__(initialAmount, accountName ,location)
        self.fee = 5
        self.interest_rate = 0.03
    def withdraw(self, amount):
        try:
            self.viableTrasaction(amount+self.fee)
            self.balance = self.balance - (amount + self.fee)
            self.log_transaction("Withdrawal with Fee", -(amount + self.fee))
            print("\n Transaction Completed Succefully !!!")
            self.getBalance()
        except BalanceException as error:
            print("\n Transfer Interrupted :{error}")
    def applyInterest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        self.log_transaction("Interest Added", interest) 
        print(f"\nInterest of ${interest:.2f} added.")
        self.getBalance()
class JointAccount(BankAccount):
    def __init__(self, initialAmount, accountName, owners, location):
        super().__init__(initialAmount, accountName, location)
        self.owners = owners  # list of names

    def getOwners(self):
        print(f"Owners of {self.name}: {''.join(self.owners)}")
class FixedDepositAccount(BankAccount):
    def __init__(self, principal, accountName, location,existing_account=None, duration_months=12):
        super().__init__(principal, accountName, location)
        self.principal = principal
        self.duration_months = duration_months
        
        # Default interest rate for new customer
        self.interest_rate = 0.025  

        # If existing account is 6+ months old → 7.5%
        if existing_account:
            age = datetime.now() - existing_account.date_of_opening
            if age >= timedelta(days=180):  # 6 months approx
                self.interest_rate = 0.05

        self.maturity_amount = self.calculate_maturity()
        self.log_transaction("Fixed Deposit Opened", principal)

    def calculate_maturity(self):
        # Simple interest for demonstration
        return self.principal * (1 + self.interest_rate * (self.duration_months / 12))

    def showDetails(self):
        print(f"\nFixed Deposit Account Details for {self.name} (#{self.account_number}):")
        print(f"Principal: ${self.principal:.2f}")
        print(f"Duration: {self.duration_months} months")
        print(f"Interest Rate: {self.interest_rate*100:.2f}%")
        print(f"Maturity Amount: ${self.maturity_amount:.2f}")
        print(f"Date of Opening: {self.date_of_opening.strftime('%Y-%m-%d')}")