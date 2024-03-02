from PyQt5.QtWidgets import QMessageBox
from database import Database
import datetime
from helper import Response, Transaction
import json


class Account:
    def __init__(self, ID):
        
        self.df = Database()
        self.ID = ID
        self.Name = self.df.getName(ID)
        self.Balance = self.df.getBalance(ID)
        self.Password = self.df.getPassword(ID)
        self.mobile_number = self.df.getMobileNum(ID)
        self.email = self.df.getEmail(ID)
        
        self.__filename = f"accounts/account_{ID}.json"
        self.__response = Response(self.email, self.Name.split()[0])
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

    def withdraw(self, amount:int, number=None):
        
        self.transactions.append(Transaction("Withdrawal",amount))
        self.save_transactions()
        self.Balance -= amount
        self.df.setBalance(self.ID,self.Balance)
        self.send_withdraw_email(amount, number)

    def get_transaction_history(self):
        self.load_transactions()
        transactions = []
        for transaction in self.transactions:
            try:
                transactions.insert(0, {'date':transaction['date'],'type':transaction['type'],'amount':transaction['amount']})
            except:
                transactions.insert(0,{'date':transaction.date,'type':transaction.type,'amount':transaction.amount})
        return transactions
    
    def send_withdraw_email(self, amount, number=None):
        if number == None:
            email_body = f"Your account {self.ID} "
            email_body += f"was debited with EGP {amount} on "
            email_body += datetime.datetime.now().strftime("%d/%m %H:%M")
            email_body += f".\nYour current balance is EGP {self.Balance}."
        else:
            email_body = f"EGP {amount} was sent from your account "
            email_body += f"{self.ID} to {number} on "
            email_body += datetime.datetime.now().strftime("%d/%m %H:%M")
            email_body += f".\nYour current balance is EGP {self.Balance}."
            
        self.__response.send_email(email_body)
        
    def send_deposit_email(self, amount):
        email_body = f"Your account {self.ID} "
        email_body += f"was credited with EGP {amount} on "
        email_body += datetime.datetime.now().strftime("%d/%m %H:%M")
        email_body += f".\nYour current balance is EGP {self.Balance}."
        self.__response.send_email(email_body)
        
    def send_history_email(self):
        self.__response.send_history(self.Balance,self.get_transaction_history())
    
    def send_password_change_email(self):
        email_body =  f"Your account {self.ID} password "
        email_body += f"has been changed in "
        email_body += datetime.datetime.now().strftime("%d/%m %H:%M")
        email_body += f".\nIf it's not you please contact the bank as soon as possible."
        self.__response.send_email(email_body)
    
    def showMessage(self, info, icon = QMessageBox.Critical):
        self.__response.ShowMessage(info, icon)
    
    def changePassword(self,new_password):
    
        self.df.setPassword(self.ID, new_password)
        self.Password = new_password
        self.send_password_change_email()
            
            