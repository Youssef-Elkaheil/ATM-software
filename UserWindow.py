from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from database import Database
import sys
import re


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self,ID = "215321701332"):
        super(MainWindow, self).__init__()
        uic.loadUi('MainWindow.ui', self)
        
        self.df = Database()
        self.ID = ID
        self.Name = self.df.getName(ID)
        self.Balance = int(self.df.getBalance(ID))
        self.Password = self.df.getPassword(ID)
        
        # Find the pages with the name "lineEdit"
        self.pages =  self.findChild(QtWidgets.QStackedWidget, 'pages')
        
        # home page widgets and button actions
        self.home_page = self.findChild(QtWidgets.QWidget, 'home_page')
        self.cash_withdraw_button = self.findChild(QtWidgets.QPushButton, 'withdraw_page_button')
        self.cash_withdraw_button.clicked.connect(self.switchWithdrawPage)
        self.balance_inquiry_button = self.findChild(QtWidgets.QPushButton, 'inquiry_page_button')
        self.balance_inquiry_button.clicked.connect(self.switchInquiryPage)
        self.password_change_button = self.findChild(QtWidgets.QPushButton, 'password_page_button')
        self.password_change_button.clicked.connect(self.switchPasswordPage)
        self.fawry_service_button = self.findChild(QtWidgets.QPushButton, 'fawry_page_button')
        self.fawry_service_button.clicked.connect(self.switchFawryPage)
        self.exit_button = self.findChild(QtWidgets.QPushButton, 'exit_button')
        self.exit_button.clicked.connect(self.close)
        
        # withdraw page and its button action 
        self.withdraw_page = self.findChild(QtWidgets.QWidget, 'withdraw_page')
        withdraw_buttons = [100,200,500,1000,2000,3000,4000,5000]
        
        for withdraw_button in withdraw_buttons:
            name = "withdraw_{}".format(withdraw_button)
            button = self.findChild(QtWidgets.QPushButton,name)
            button.clicked.connect(lambda ch, i=withdraw_button:self.withdraw_credit(i))
        
        button = self.findChild(QtWidgets.QPushButton,"withdraw_enter")
        button.clicked.connect(lambda ch, t=0:self.withdraw_credit(t))
        
        # inquiry page and its buttons actions
        self.Inquiry_page = self.findChild(QtWidgets.QWidget, 'Inquiry_page')
        
        # password page and its buttons actions 
        self.password_page = self.findChild(QtWidgets.QWidget, 'password_page')
        self.password_ok_button = QtWidgets.QPushButton()
        self.password_ok_button = self.findChild(QtWidgets.QPushButton,"password_ok")
        self.password_ok_button.clicked.connect(self.checkPassword)
        
        # fawry widget and button action
        self.fawry_page = self.findChild(QtWidgets.QWidget, 'fawry_page')
        self.etisalat_button = self.findChild(QtWidgets.QPushButton,"etisalat_button")
        company = self.etisalat_button.text()
        self.etisalat_button.clicked.connect(lambda c,i = company:self.switchSendPage(i))
        self.vodafone_button = self.findChild(QtWidgets.QPushButton,"vodafone_button")
        company = self.vodafone_button.text()
        self.vodafone_button.clicked.connect(lambda c,i = company:self.switchSendPage(i))
        self.orange_button = self.findChild(QtWidgets.QPushButton,"orange_button")
        company = self.orange_button.text()
        self.orange_button.clicked.connect(lambda c,i = company:self.switchSendPage(i))
        self.we_button = self.findChild(QtWidgets.QPushButton,"we_button")
        company = self.we_button.text()
        self.we_button.clicked.connect(lambda c,i = company:self.switchSendPage(i))        
        
        # send page and its button actions
        self.send_page = self.findChild(QtWidgets.QWidget, 'send_page')
        self.send_button = self.findChild(QtWidgets.QPushButton,"send_button")
        self.send_button.clicked.connect(self.sendCash)
        # back buttons action handling
        self.buttons = self.findChildren(QtWidgets.QPushButton)
        for button in self.buttons:
            if button.text() == "Back" or button.objectName() == "inquiry_ok":
                button.clicked.connect(self.handleBackButtons)
        
        # lineedit input validating
        self.lineedits = self.findChildren(QtWidgets.QLineEdit)
        for lineedit in self.lineedits:
            lineedit.textEdited.connect(lambda ch, i = lineedit:self.validate(i))
            
        # for error message : use showErrorMessage method 
        self.msg = QMessageBox()
        
        self.switchHomePage()
        self.show()

    # show error message
    def ShowMessage(self, info, icon = QMessageBox.Critical):
        self.msg.setIcon(icon)
        if icon == QMessageBox.Critical:
            self.msg.setWindowTitle("Error")
        else:
            self.msg.setWindowTitle("Info")
        self.msg.setText(info + "\t\n")
        self.msg.exec_()
    
    # accept only numerical values
    def validate(self,lineedit:QtWidgets.QLineEdit):
        text = lineedit.text()
        text = re.sub("[^0-9]","",text)
        lineedit.setText(text)
    
    # clear all lineedits
    def clear_lineedits(self):
        for lineedit in self.lineedits:
            lineedit.clear()

    # check if amount available and minus it from balance
    def handleBackButtons(self):
        if self.pages.currentIndex() != 5:
            self.switchHomePage()
        else:
            self.switchFawryPage()
        self.clear_lineedits()
            
    #  compine home page tools together
    def switchHomePage(self):
        QtWidgets.QStackedWidget.setCurrentWidget(self.pages,self.home_page)
        
    #  compine withdraw page tools together
    def switchWithdrawPage(self):
        QtWidgets.QStackedWidget.setCurrentWidget(self.pages,self.withdraw_page)

    # withdraw credit method
    def withdraw_credit(self,amount):
        print("Amount: ",amount,", Balance: ",self.Balance)
        if amount == 0:
            
            lineEdit = QtWidgets.QLineEdit()
            lineEdit = self.findChild(QtWidgets.QLineEdit,"withdraw_lineedit")
            amount = int(lineEdit.text())
        else:
            pass

        if amount > 5000:
            self.ShowMessage("Maximum allowed value per transaction is 5000 L.E")
        elif amount > self.Balance:
            self.ShowMessage("No sufficient balance")
        elif amount %100 != 0:
            self.ShowMessage("Invalid Value")
        else:
            self.ShowMessage("Thank you for banking with us",QMessageBox.Icon.Information)
            self.Balance -= amount
            self.df.setBalance(self.ID,self.Balance)
            self.switchHomePage()           
            
    
    #  compine balance inquiry page tools together
    def switchInquiryPage(self):
        
        QtWidgets.QStackedWidget.setCurrentWidget(self.pages,self.Inquiry_page)
        name_label = self.findChild(QtWidgets.QLabel,"Name_label")
        balance_label = self.findChild(QtWidgets.QLabel,"Balance_label")
        name_label.setText("Name:\t {}".format(self.Name))
        balance_label.setText("Balance:\t {}".format(self.Balance))
        
    #  compine Password page tools together
    def switchPasswordPage(self):
        QtWidgets.QStackedWidget.setCurrentWidget(self.pages,self.password_page)
      
    def checkPassword(self):
        password_line1 = self.findChild(QtWidgets.QLineEdit,"new_password_line")
        password_line2 = self.findChild(QtWidgets.QLineEdit,"re_new_password_line")
        if password_line1.text() == password_line2.text():
            self.Password = password_line1.text()
            self.df.setPassword(self.ID,self.Password)
            self.ShowMessage("Password Changed Successfully",QMessageBox.Icon.Information)
            self.switchHomePage()
        else:
            self.ShowMessage("Password don't match")
        password_line1.clear()
        password_line2.clear()
        
    #  compine withdraw page tools together
    def switchFawryPage(self):
        QtWidgets.QStackedWidget.setCurrentWidget(self.pages,self.fawry_page)

    #  compine send page tools together
    def switchSendPage(self,company):
        QtWidgets.QStackedWidget.setCurrentWidget(self.pages,self.send_page)
        company_label = self.findChild(QtWidgets.QLabel,"company_label")
        company_label.setText(company)

    def sendCash(self):
        mobile_lineedit = self.findChild(QtWidgets.QLineEdit,"mobile_lineedit") 
        amount_lineedit = self.findChild(QtWidgets.QLineEdit,"amount_lineedit") 
        mobile_number = mobile_lineedit.text()
        amount = int(amount_lineedit.text())
        if mobile_number[0] != '0' or mobile_number[1] != '1' or len(mobile_number) < 11:
            self.ShowMessage("invalid Mobile Number")
        elif amount > 5000:
            self.ShowMessage("Maximum allowed value per transaction is 5000 L.E")
        elif amount > self.Balance:
            self.ShowMessage("No sufficient balance")
        elif amount %100 != 0:
            self.ShowMessage("Invalid Value")
        else:
            self.ShowMessage("{}L.E. are sent to {} successfully".format(amount,mobile_number),QMessageBox.Icon.Information)
            self.Balance -= amount
            self.df.setBalance(self.ID,self.Balance)
            self.switchHomePage()     
        mobile_lineedit.clear()
        amount_lineedit.clear()
    
# app = QtWidgets.QApplication(sys.argv)
# window = MainWindow()
# app.exec_()






