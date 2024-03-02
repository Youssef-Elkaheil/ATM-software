from PyQt5 import QtWidgets, uic
from accounts import Account
from withdraw_page import Withdraw_page
from deposit_page import Deposit_page
from history_page import History_page
from password_page import Password_page
from fawry_page import Fawry_page


class Home_page(QtWidgets.QStackedWidget):
    def __init__(self, ID):
        super(Home_page,self).__init__()
        uic.loadUi("home_page.ui",self)
        self.ID = ID
        self.account = Account(ID)
        self.signout = False
        
        self.cash_withdraw_button = self.findChild(QtWidgets.QPushButton, 'withdraw_page_button')
        self.cash_withdraw_button.clicked.connect(lambda ch,i=0:self.switchToSelectedPage(i))
        self.cash_deposit_button = self.findChild(QtWidgets.QPushButton, 'deposit_page_button')
        self.cash_deposit_button.clicked.connect(lambda ch,i=1:self.switchToSelectedPage(i))
        self.balance_inquiry_button = self.findChild(QtWidgets.QPushButton, 'inquiry_page_button')
        self.balance_inquiry_button.clicked.connect(lambda ch,i=2:self.switchToSelectedPage(i))
        self.password_change_button = self.findChild(QtWidgets.QPushButton, 'password_page_button')
        self.password_change_button.clicked.connect(lambda ch,i=3:self.switchToSelectedPage(i))
        self.fawry_service_button = self.findChild(QtWidgets.QPushButton, 'fawry_page_button')
        self.fawry_service_button.clicked.connect(lambda ch,i=4:self.switchToSelectedPage(i))
        self.exit_button = self.findChild(QtWidgets.QPushButton, 'exit_button')
        self.exit_button.clicked.connect(self.switchLoginPage)


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
    
    def switchToSelectedPage(self, selectedPage:int):
        if selectedPage == 0:
            self.selected_option =  Withdraw_page(self.account)
        elif selectedPage == 1:
            self.selected_option =  Deposit_page(self.account)
        elif selectedPage == 2:
            self.selected_option =  History_page(self.account)
        elif selectedPage == 3:
            self.selected_option =  Password_page(self.account)
        elif selectedPage == 4:
            self.selected_option =  Fawry_page(self.account)

        self.configureSelectedOption()     
        
    def switchFawryPage(self):
        pass
    
    def switchLoginPage(self):
        # set flag to kill current class
        self.signout = True
        