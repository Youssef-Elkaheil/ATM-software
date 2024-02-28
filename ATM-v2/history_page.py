from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from accounts import Account
from helper import send_email, ShowMessage
class History_page(QtWidgets.QWidget):
    def __init__(self, account:Account):
        super(History_page,self).__init__()
        uic.loadUi("history_page.ui",self)
        
        self.account = account
        self.table = self.findChild(QtWidgets.QTableWidget,"tableWidget")
        
        self.name_label = self.findChild(QtWidgets.QLabel,"name_label")
        self.balance_label = self.findChild(QtWidgets.QLabel,"balance_label")
        self.name_label.setText(f"Name: {self.account.Name}")
        self.balance_label.setText(f"Balance: EGP {self.account.Balance}")
        
        self.sendMail_button = self.findChild(QtWidgets.QPushButton, "send_email_button")
        self.sendMail_button.clicked.connect(self.sendMail)
        
        
        self.back_button = self.findChild(QtWidgets.QPushButton, "back_button")
        self.back_button.clicked.connect(self.close)
        
        self.back_button = self.findChild(QtWidgets.QPushButton, "ok_button")
        self.back_button.clicked.connect(self.close)
        
        self.load_transactions()

    
    def setTableItem(self, row, column, transactionitem):
        item = QTableWidgetItem(transactionitem) # create the item
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter) # change the alignment
        self.table.setItem(row,column, item)  
          
    def load_transactions(self):
        
        for transaction in self.account.transactions:
            self.table.insertRow(0)
            self.setTableItem(0, 0, transaction['date'])
            self.setTableItem(0, 1, transaction['type'])
            self.setTableItem(0, 2, f"{transaction['amount']}")
            
        self.table.resizeColumnsToContents()
    
    def sendMail(self):
        body = ""    