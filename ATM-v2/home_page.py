from PyQt5 import QtWidgets, uic
from accounts import Account
from withdraw_page import Withdraw_page
from deposit_page import Deposit_page
from history_page import History_page

import sys

class Home_page(QtWidgets.QStackedWidget):
    def __init__(self, ID):
        super(Home_page,self).__init__()
        uic.loadUi("home_page.ui",self)
        
        self.ID = ID
        self.account = Account(ID)
        self.signout = False
        
        self.cash_withdraw_button = self.findChild(QtWidgets.QPushButton, 'withdraw_page_button')
        self.cash_withdraw_button.clicked.connect(lambda ch,i=Withdraw_page(self.account):self.switchToSelectedPage(i))
        self.cash_deposit_button = self.findChild(QtWidgets.QPushButton, 'deposit_page_button')
        self.cash_deposit_button.clicked.connect(lambda ch,i=Deposit_page(self.account):self.switchToSelectedPage(i))
        self.balance_inquiry_button = self.findChild(QtWidgets.QPushButton, 'inquiry_page_button')
        self.balance_inquiry_button.clicked.connect(lambda ch,i=History_page(self.account):self.switchToSelectedPage(i))
        self.password_change_button = self.findChild(QtWidgets.QPushButton, 'password_page_button')
        self.password_change_button.clicked.connect(self.switchPasswordPage)
        self.fawry_service_button = self.findChild(QtWidgets.QPushButton, 'fawry_page_button')
        self.fawry_service_button.clicked.connect(self.switchFawryPage)
        self.exit_button = self.findChild(QtWidgets.QPushButton, 'exit_button')
        self.exit_button.clicked.connect(self.switchLoginPage)
        self.show()

    def configureSelectedOption(self):
        if self.selected_option != None:
            self.addWidget(self.selected_option)
            self.setCurrentWidget(self.selected_option)
            self.selected_option.back_button.clicked.connect(self.ReturnToHomePage)
        
    def ReturnToHomePage(self):
        self.setCurrentIndex(0)
        self.removeWidget(self.selected_option)
        if self.selected_option != None:
            self.selected_option.destroy()
        self.selected_option = None
    
    def switchToSelectedPage(self, selectedPage):
        self.selected_option =  selectedPage
        self.configureSelectedOption()     
        
    def switchPasswordPage(self):
        pass
    def switchFawryPage(self):
        pass
    
    def switchLoginPage(self):
        # set flag to kill current class
        self.signout = True
        
    
app = QtWidgets.QApplication(sys.argv)
window = Home_page("215321701332")
app.exec_()