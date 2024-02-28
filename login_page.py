from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from database import Database
from email_response import send_email
import sys
import re

class Login_page(QtWidgets.QWidget):
    def __init__(self, lineEdit, enter_button, feedback_label, instruction_label, image):
        self.lineEdit =  lineEdit
        self.enter_button =  enter_button
        self.feedback_label =  feedback_label
        self.instruction_label =  instruction_label
        self.image = image
        QtWidgets.QLabel.setStyleSheet(self.feedback_label,"color: red")
        QtWidgets.QLineEdit.setEchoMode(self.lineEdit,QtWidgets.QLineEdit.EchoMode.Normal)
        self.lineEdit.textEdited.connect(self.validate)
        
        self.feedback_label.hide()
        self.enter_button.clicked.connect(self.check_Input)
          
    # accept only numerical values
    def validate(self):
        text = self.lineEdit.text()
        text = re.sub("[^0-9]","",text)
        self.lineEdit.setText(text)
        
    # set widget to accept ID
    def EnterID(self):

        self.ID = None
        self.password = None
        self.password_trials = 0
        
        self.lineEdit.clear()

        QtWidgets.QLabel.setText(self.instruction_label,"Please enter account number:")
        QtWidgets.QLineEdit.setMaxLength(self.lineEdit,12)
        QtWidgets.QLineEdit.setEchoMode(self.lineEdit,QtWidgets.QLineEdit.EchoMode.Normal)

    # set widget to accept password
    def EnterPassword(self):
        
        self.lineEdit.clear()
        self.password_trials = 0
        
        QtWidgets.QLabel.setText(self.instruction_label,"Enter Password:")
        QtWidgets.QLineEdit.setMaxLength(self.lineEdit,4)
        QtWidgets.QLineEdit.setEchoMode(self.lineEdit,QtWidgets.QLineEdit.EchoMode.Password)
         
    # show error message that account is blocked
    def showBlockedSign(self):
        self.lineEdit.clear()
        QtWidgets.QLabel.setText(self.feedback_label,"Account Blocked, please visit branch")
        self.feedback_label.show()
        
    # show error message that account is not found
    def showAccountNotFoundSign(self):
        self.lineEdit.clear()
        QtWidgets.QLabel.setText(self.feedback_label,"Account number is not identified")
        self.feedback_label.show()
    
    # show error message incorrect password
    def showIncorrectPasswordSign(self):
        self.lineEdit.clear()
        QtWidgets.QLabel.setText(self.feedback_label,"Incorrect Password:{}".format(self.password_trials))
        self.feedback_label.show()
            
    # method to check ID then check password
    def check_Input(self):
        # if ID is not set by user keep checking for ID 
        if self.ID == None :
            # search for ID
            self.ID = self.lineEdit.text()
            self.ID_index = self.df.searchForID(self.ID)
            if self.ID_index != None:
                self.status = self.df.getStatus(self.ID)
                
                if self.status == "Running":
                    self.password = self.df.getPassword(self.ID)
                    self.feedback_label.hide()
                    self.EnterPassword()
                elif self.status == "Blocked":
                    self.ID = None
                    self.showBlockedSign()
            else:
                self.ID = None
                self.showAccountNotFoundSign()
                
        
        # check password             
        else:
            # found
            if self.password == self.lineEdit.text():
                
                # TODO open user account
                self.EnterID()

            # not found            
            elif self.password_trials < 2 :
                
                self.password_trials += 1
                self.showIncorrectPasswordSign()
            # more that 3 incorrect trials
            else:
                self.df.setStatus(self.ID,"Blocked")
                self.showBlockedSign()
                self.EnterID()
                
            
        