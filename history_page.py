from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from accounts import Account

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
        
        self.ok_button = self.findChild(QtWidgets.QPushButton, "ok_button")
        self.ok_button.clicked.connect(self.backToHomePage)
        
        self.load_transactions()

    
    def setTableItem(self, row, column, transactionitem):
        item = QTableWidgetItem(transactionitem) # create the item
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter) # change the alignment
        self.table.setItem(row,column, item)  
          
    def load_transactions(self):
        self.table.clearContents()
        for transaction in self.account.get_transaction_history():
            self.table.insertRow(self.table.rowCount())
            self.setTableItem(self.table.rowCount()-1, 0, transaction['date'])
            self.setTableItem(self.table.rowCount()-1, 1, transaction['type'])
            self.setTableItem(self.table.rowCount()-1, 2, f"{transaction['amount']}")
            
        self.table.resizeColumnsToContents()
    
    def sendMail(self):
        self.account.send_history_email() 
        
    def backToHomePage(self):
        self.back_button.click()