from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from accounts import Account
from helper import ShowMessage, send_email
import datetime

class Withdraw_page(QtWidgets.QWidget):
    def __init__(self, account:Account):
        super(Withdraw_page,self).__init__()
        uic.loadUi("withdraw_page.ui",self)
        
        self.account = account
        
        self.lineEdit = self.findChild(QtWidgets.QLineEdit,"withdraw_lineedit")
        self.lineEdit.setInputMask("00000")
        
        # self.lineEdit.textEdited.connect(self.validate_number)
        withdraw_buttons = [100,200,500,1000,2000,3000,4000,5000]
        
        for withdraw_button in withdraw_buttons:
            name = "withdraw_{}".format(withdraw_button)
            button = self.findChild(QtWidgets.QPushButton,name)
            button.clicked.connect(lambda ch, i=withdraw_button:self.setAmount(i))
        
        button = self.findChild(QtWidgets.QPushButton,"withdraw_enter")
        button.clicked.connect(self.withdraw_credit)
        self.back_button = self.findChild(QtWidgets.QPushButton,"back_button")
        self.back_button.clicked.connect(self.close)
    
    def setAmount(self, amount):
        self.withdraw_amount = amount
        self.lineEdit.setText(f"{amount}")
        
    def withdraw_credit(self):
        if self.lineEdit.text() == "":
            ShowMessage("Please enter Amount to withdraw")
        else:
            self.withdraw_amount = int(self.lineEdit.text())
            self.lineEdit.clear()
            
            if self.withdraw_amount > 5000:
                ShowMessage("Maximum allowed value per transaction is 5000 L.E")
            elif self.withdraw_amount > self.account.Balance:
                ShowMessage("No sufficient balance")
            elif self.withdraw_amount %100 != 0:
                ShowMessage("Invalid Value")
            else:
                self.account.withdraw(self.withdraw_amount)
                ShowMessage("Thank you for banking with us",QMessageBox.Icon.Information)
                email_body = f"Your account {self.account.ID} "
                email_body += f"was debited with EGP {self.withdraw_amount} on "
                email_body += datetime.datetime.now().strftime("%d/%m %H:%M")
                email_body += f".\nYour current balance is EGP {self.account.Balance}."
                send_email(email_body)
         


