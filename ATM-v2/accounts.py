from database import Database
import datetime
import json


# Your ATM project likely has these structures already
class Transaction:
    def __init__(self, type, amount):
        self.type = type
        self.amount = amount
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

class Account:
    def __init__(self, ID):
        
        self.df = Database()
        self.ID = ID
        self.Name = self.df.getName(ID)
        self.Balance = self.df.getBalance(ID)
        self.Password = self.df.getPassword(ID)
        
        self.filename = f"accounts/account_{ID}.json"
        self.load_transactions()

    def load_transactions(self):
        try:
            with open(self.filename, 'r') as f:
                self.transactions = json.load(f)
        except FileNotFoundError:
            self.transactions = []

    def save_transactions(self):
        data = []  # Convert transactions to dicts
        for transaction in self.transactions:
            try:
                data.append(transaction.__dict__)
            except:
                data.append(transaction)

        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)  # Indent for readability

    def deposit(self, amount:int):
        self.transactions.append(Transaction("Deposit",amount))
        self.save_transactions()
        self.Balance += amount
        self.df.setBalance(self.ID,self.Balance)

    def withdraw(self, amount:int):
        
        self.transactions.append(Transaction("Withdrawal",amount))
        self.save_transactions()
        self.Balance -= amount
        self.df.setBalance(self.ID,self.Balance)

    def get_transaction_history(self):
        return self.transactions
