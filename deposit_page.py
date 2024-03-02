from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from accounts import Account

class Deposit_page(QtWidgets.QWidget):
    def __init__(self, account:Account):
        super(Deposit_page,self).__init__()
        uic.loadUi("deposit_page.ui",self)
        
        self.account = account
        
        self.lineEdit = self.findChild(QtWidgets.QLineEdit,"lineedit")
        self.lineEdit.setInputMask("0000")
        
        button = self.findChild(QtWidgets.QPushButton,"enter_button")
        button.clicked.connect(self.deposit_credit)
        self.back_button = self.findChild(QtWidgets.QPushButton,"back_button")
        self.back_button.clicked.connect(self.close)
        
    def deposit_credit(self):
        if self.lineEdit.text() == "":
            self.account.showMessage("Please enter Amount to deposit")
        else:
            self.deposit_amount = int(self.lineEdit.text())
            self.lineEdit.clear()
            
            if self.deposit_amount > 5000:
                self.account.showMessage("Maximum allowed value per transaction is 5000 L.E")
            elif self.deposit_amount %100 != 0:
                self.account.showMessage("Invalid Value")
            else:
                self.account.deposit(self.deposit_amount)
                self.account.showMessage("Thank you for banking with us",QMessageBox.Icon.Information)
         


