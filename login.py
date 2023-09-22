from PyQt5 import QtWidgets, uic

from UserWindow import MainWindow
from database import Database

import sys
import re

class ID_widget(QtWidgets.QWidget):
    def __init__(self):
        super(ID_widget, self).__init__()
        uic.loadUi('ID_widget.ui', self)
        # global variables
        
        self.df = Database()
        self.ID = None
        self.status = None
        self.password = None
        self.password_trials = 0

        
        # Find the lineEdit with the name "lineEdit"
        self.lineEdit =  self.findChild(QtWidgets.QLineEdit, 'lineEdit')
        # Find the button with the name "enter_button"
        self.enter_button = self.findChild(QtWidgets.QPushButton, 'enter_button')
        # Find the label with the name "feedback_label"
        self.feedback_label = self.findChild(QtWidgets.QLabel, 'feedback_label')
        # Find the label with the name "instruction_label"
        self.instruction_label = self.findChild(QtWidgets.QLabel, 'instruction_label')
        
        QtWidgets.QLabel.setStyleSheet(self.feedback_label,"color: red")
        QtWidgets.QLineEdit.setEchoMode(self.lineEdit,QtWidgets.QLineEdit.EchoMode.Normal)
        self.lineEdit.textEdited.connect(self.validate)
        
        self.feedback_label.hide()
        self.enter_button.clicked.connect(self.check_Input)
        self.show()
        
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
                
                self.main = MainWindow(self.ID)
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
                
            
            
app = QtWidgets.QApplication(sys.argv)
window = ID_widget()
app.exec_()
