from database import Database
import datetime
from helper import Server
import json


# Your ATM project likely has these structures already
class Transaction:
    def __init__(self, type, amount):
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.type = type
        self.amount = amount


class Account:
    def __init__(self, ID):
        
        self.df = Database()
        self.ID = ID
        self.Name = self.df.getName(ID)
        self.Balance = self.df.getBalance(ID)
        self.Password = self.df.getPassword(ID)
        self.email = 'ymohamed9880@gmail.com'
        self.__filename = f"accounts/account_{ID}.json"
        self.__server = Server('ymohamed9880@gmail.com',self.Name.split()[0])
        self.load_transactions()

    def load_transactions(self):
        try:
            with open(self.__filename, 'r') as f:
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

        with open(self.__filename, "w") as f:
            json.dump(data, f, indent=4)  # Indent for readability

    def deposit(self, amount:int):
        self.transactions.append(Transaction("Deposit",amount))
        self.save_transactions()
        self.Balance += amount
        self.df.setBalance(self.ID,self.Balance)
        self.send_deposit_email(amount)

    def withdraw(self, amount:int):
        
        self.transactions.append(Transaction("Withdrawal",amount))
        self.save_transactions()
        self.Balance -= amount
        self.df.setBalance(self.ID,self.Balance)
        self.send_withdraw_email(amount)

    def get_transaction_history(self):
        transactions = []
        for transaction in self.transactions:
            try:
                transactions.insert(0, {'date':transaction['date'],'type':transaction['type'],'amount':transaction['amount']})
            except:
                transactions.insert(0,{'date':transaction.date,'type':transaction.type,'amount':transaction.amount})
        return transactions
    
    def send_withdraw_email(self, amount):
        email_body = f"Your account {self.ID} "
        email_body += f"was debited with EGP {amount} on "
        email_body += datetime.datetime.now().strftime("%d/%m %H:%M")
        email_body += f".\nYour current balance is EGP {self.Balance}."
        self.__server.send_email(email_body)
        
    def send_deposit_email(self, amount):
        email_body = f"Your account {self.ID} "
        email_body += f"was credited with EGP {amount} on "
        email_body += datetime.datetime.now().strftime("%d/%m %H:%M")
        email_body += f".\nYour current balance is EGP {self.Balance}."
        self.__server.send_email(email_body)
        
    def send_history_email(self):
        self.__server.send_history(self.Balance,self.get_transaction_history())