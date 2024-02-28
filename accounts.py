import json

class Account:
    def __init__(self, account_number):
        self.account_number = account_number
        self.filename = f"accounts/account_{account_number}.json"
        self.load_transactions()

    def load_transactions(self):
        try:
            with open(self.filename, "r") as f:
                self.transactions = json.load(f)
        except FileNotFoundError:
            self.transactions = []

    def save_transactions(self):
        with open(self.filename, "w") as f:
            json.dump(self.transactions, f)

    def deposit(self, amount):
        self.transactions.append(f"Deposited ${amount}")
        self.save_transactions()

    def withdraw(self, amount):
        self.transactions.append(f"Withdrew ${amount}")
        self.save_transactions()

    def get_balance(self):
        balance = 0
        for transaction in self.transactions:
            if transaction.startswith("Deposited"):
                amount = float(transaction.split()[1])
                balance += amount
            else:
                amount = float(transaction.split()[1])
                balance -= amount
        return balance

    def get_transaction_history(self):
        return self.transactions
