from PyQt5 import QtWidgets, uic,QtGui
from PyQt5.QtGui import QIntValidator,QCloseEvent
from database import Database

import images_rc
import re
import os

if os.getenv("RASPBERRY_PI") is not None:
    from RFID import RFIDThread

class Login_page(QtWidgets.QWidget):
    def __init__(self):
        super(Login_page, self).__init__()
        uic.loadUi("login_page.ui",self)
        
        self.df = Database()
        self.ID = None
        self.status = None
        self.password = None
        self.password_trials = 0
        self.login_succeded = False
        self.is_raspberry_pi = os.getenv("RASPBERRY_PI") is not None
        
        if self.is_raspberry_pi:
             # Initialize the RFID thread
            try:
                self.rfid_thread = RFIDThread()
                # Connect the thread's signal to a slot in your main window
                self.rfid_thread.tag_read.connect(self.on_tag_read)
            except ImportError:
                self.is_raspberry_pi = False
                print("RFIDThread not found. Assuming PC environment.")
        
        # Find the lineEdit with the name "login_lineEdit"
        self.lineEdit =  self.findChild(QtWidgets.QLineEdit, 'login_lineEdit')
        # Find the button with the name "login_enter_button"
        self.enter_button = self.findChild(QtWidgets.QPushButton, 'login_button')
        self.cancel_button = self.findChild(QtWidgets.QPushButton, 'cancel_button')
        self.cancel_button.clicked.connect(self.EnterID)
        # Find the label with the name "feedback_label"
        self.feedback_label = self.findChild(QtWidgets.QLabel, 'feedback_label')
        # Find the label with the name "instruction_label"
        self.instruction_label = self.findChild(QtWidgets.QLabel, 'login_instruction_label')
        # Find the label with the name "resource_img_label"
        self.image = self.findChild(QtWidgets.QLabel, 'resource_img_label')
        
        QtWidgets.QLabel.setStyleSheet(self.feedback_label,"color: red")
        self.EnterID()
        self.lineEdit.textEdited.connect(self.validate)
        
        self.enter_button.clicked.connect(self.check_Input)
        
        
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        
        if self.is_raspberry_pi:
            try:
                import RPI.GPIO as GPIO
                self.rfid_thread.quit()
                self.rfid_thread.wait()
                GPIO.cleanup()
            except:
                print("can't import GPIO, Assuming PC environment.")
                    
        a0.accept()
        return super().closeEvent(a0)
          
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
        self.login_succeded = False
        self.feedback_label.hide()
        self.cancel_button.hide()
        self.lineEdit.clear()
        if self.is_raspberry_pi:
            self.rfid_thread.start()
        QtWidgets.QLabel.setPixmap(self.image
                                   , QtGui.QPixmap(":/images/rfid.png").scaled(500,500))
        QtWidgets.QLabel.setMargin(self.image,0)
        if self.is_raspberry_pi == False:
            QtWidgets.QLabel.setText(self.instruction_label,"Please enter account ID:")
        else:
            QtWidgets.QLabel.setText(self.instruction_label
                                     ,"Please put your card near card reader \nor enter your account ID manually:")
        QtWidgets.QLineEdit.setMaxLength(self.lineEdit,12)
        QtWidgets.QLineEdit.setEchoMode(self.lineEdit,QtWidgets.QLineEdit.EchoMode.Normal)

    # set widget to accept password
    def EnterPassword(self):
        
        self.lineEdit.clear()
        self.feedback_label.hide()
        self.cancel_button.show()
        if self.is_raspberry_pi:
            self.rfid_thread.quit()
        QtWidgets.QLabel.setMargin(self.image, 50)
        self.password_trials = 0
        QtWidgets.QLabel.setPixmap(self.image
                                   , QtGui.QPixmap(":/images/password.png").scaled(500,500))
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
                
                self.login_succeded = True
                
            # not found            
            elif self.password_trials < 2 :
                
                self.password_trials += 1
                self.showIncorrectPasswordSign()
            # more that 3 incorrect trials
            else:
                self.df.setStatus(self.ID,"Blocked")
                self.showBlockedSign()
                self.EnterID()
                
    def on_tag_read(self, account_ID, tag_ID):
        # Update your GUI elements with the received data
        print(f"Tag detected: ID: {tag_ID}, account: {account_ID}\n")
        self.lineEdit.setText(account_ID)
        self.enter_button.click()
        
        
                
            
        
