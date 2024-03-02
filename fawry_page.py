from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui
from accounts import Account
import sys
import images_rc

class Fawry_page(QtWidgets.QStackedWidget):
    def __init__(self, account:Account):
        super(Fawry_page,self).__init__()
        uic.loadUi("fawry_page.ui",self)
        
        self.account = account
        lineEdits = self.findChildren(QtWidgets.QLineEdit)
        for lineEdit in lineEdits:
            lineEdit.setValidator(QtGui.QIntValidator())
        
        # company menu 
        self.setCurrentIndex(0)
        
        self.vodafone_button = self.findChild(QtWidgets.QPushButton,'vodafone_button')
        self.vodafone_button.clicked.connect(self.switchToVodafonePage)
        self.orange_button = self.findChild(QtWidgets.QPushButton,'orange_button')
        self.orange_button.clicked.connect(self.switchToOrangePage)
        self.etisalat_button = self.findChild(QtWidgets.QPushButton,'etisalat_button')
        self.etisalat_button.clicked.connect(self.switchToEtisalatPage)
        self.we_button = self.findChild(QtWidgets.QPushButton,'we_button')
        self.we_button.clicked.connect(self.switchToWePage)
        
        self.__company_logo = self.findChild(QtWidgets.QLabel,'company_logo')
        self.selected_company = None
        self.company_unique_digit = {'Vodafone':"010"
                                     ,'Orange':"012"
                                     ,'Etisalat':"011"
                                     ,'We':"015"}
        self.back_button = self.findChild(QtWidgets.QPushButton,'back_button_1')
        self.back_button.clicked.connect(self.close)
        self.back_button_2 = self.findChild(QtWidgets.QPushButton,'back_button_2')
        self.back_button_2.clicked.connect(lambda:self.setCurrentIndex(0))
        self.ok_button = self.findChild(QtWidgets.QPushButton,'ok_button')
        self.ok_button.clicked.connect(self.validate)
        
    
    def switchToVodafonePage(self):
        self.__company_logo.setPixmap(QtGui.QPixmap(":/logo/vodafone_Logo.png"))
        self.selected_company = 'Vodafone'
        self.setCurrentIndex(1)
        
        
    def switchToOrangePage(self):
        self.__company_logo.setPixmap(QtGui.QPixmap(":/logo/Orange_Logo.png"))
        self.__company_logo.setMargin(-40)
        self.selected_company = 'Orange'
        self.setCurrentIndex(1)
        
        
    def switchToEtisalatPage(self):
        self.__company_logo.setPixmap(QtGui.QPixmap(":/logo/ET_Logo.png"))
        self.selected_company = 'Etisalat'
        self.setCurrentIndex(1)
        
        
    def switchToWePage(self):
        self.__company_logo.setPixmap(QtGui.QPixmap(":/logo/We_Logo.png"))
        self.selected_company = 'We'
        self.setCurrentIndex(1)
        
    
    def validate_number(self, mobile_number) -> bool:
        if len(mobile_number) == 11:
            if self.company_unique_digit[self.selected_company] == mobile_number[:3]:
                    return True 
            else:
                self.account.showMessage(f"This number doesn't belong to {self.selected_company}.")
        else:
            self.account.showMessage("Invalid mobile number.")
        return False
    
    def validate_amount(self,amount:int) -> bool:
        if amount > 5000:
            self.account.showMessage("Maximum allowed value per transaction is 5000 L.E")
            return False
        elif amount > self.account.Balance:
            self.account.showMessage("No sufficient balance")
            return False
        elif amount < 5:
            self.account.showMessage("Minimum allowed value per transaction is 5 L.E")
            return False
        else:
            return True
        
    def validate(self):
        mobile_lineEdit = self.findChild(QtWidgets.QLineEdit,'mobile_lineEdit')
        amount_lineEdit = self.findChild(QtWidgets.QLineEdit,'amount_lineEdit')
        
        if self.validate_number(mobile_lineEdit.text()) == True \
            and self.validate_amount(int(amount_lineEdit.text())) == True:
                
            self.account.withdraw(int(amount_lineEdit.text()), mobile_lineEdit.text())
            self.account.showMessage("Thank you for banking with us"
                                     ,QtWidgets.QMessageBox.Icon.Information)    
            self.back_button.click()
        else:
            mobile_lineEdit.clear()
            amount_lineEdit.clear()
        
