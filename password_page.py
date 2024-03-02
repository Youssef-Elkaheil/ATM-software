from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from accounts import Account
from PyQt5.QtGui import QIntValidator

class Password_page(QtWidgets.QWidget):
    def __init__(self, account:Account):
        super(Password_page,self).__init__()
        uic.loadUi("password_page.ui",self)
        self.account = account
        
        self.password_line1 = self.findChild(QtWidgets.QLineEdit,"new_password")
        
        self.password_line1.setValidator(QIntValidator())
        self.password_line2 = self.findChild(QtWidgets.QLineEdit,"re_password")
        self.password_line2.setValidator(QIntValidator())
        
        self.back_button = self.findChild(QtWidgets.QPushButton,"back_button")
        self.back_button.clicked.connect(self.close)
        self.ok_button = self.findChild(QtWidgets.QPushButton,"enter_button")
        self.ok_button.clicked.connect(self.checkPassword)

        
    # check it the two paswords entered match  
    def checkPassword(self):
        if len(self.password_line1.text()) == 4:
            if self.password_line1.text() == self.password_line2.text():
                self.newPassword = self.password_line1.text()
                if self.newPassword != self.account.Password:
                    self.account.changePassword(self.newPassword)
                    self.account.showMessage("Password Changed Successfully",QMessageBox.Icon.Information)
                    self.back_button.click()
                else: 
                    # self.newPassword != self.password_line1.text()
                    self.account.showMessage("New password cannot be the same as your old password.", QMessageBox.Icon.Information)
            else:
                # self.password_line1.text() != self.password_line2.text():
                self.account.showMessage("Password and re-entered password don't match")
        else:
            # len(self.password_line1.text()) != 4:
            self.account.showMessage("Password must contain 4 digits")
            
        self.password_line1.clear()
        self.password_line2.clear()
        