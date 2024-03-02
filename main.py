from PyQt5 import QtWidgets, uic
from login_page import Login_page
from home_page import Home_page
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("main.ui", self)
        self.ID = None
        self.Name = None
        self.Balance = None
        self.Password = None
        self.account = None
        
        # Find the pages widget with the name "pages"
        self.pages =  self.findChild(QtWidgets.QStackedWidget, "pages")
        
        self.login_page = Login_page()
        self.pages.addWidget(self.login_page)

        self.pages.setCurrentWidget(self.login_page)
        self.login_page.enter_button.clicked.connect(self.check_login)
        self.showFullScreen()
        
    def check_login(self):
        if self.login_page.login_succeded:
            self.home_page = Home_page(self.login_page.ID)
            self.home_page.exit_button.clicked.connect(self.check_logout)
            self.pages.addWidget(self.home_page)
            self.pages.setCurrentIndex(1)
            self.login_page.EnterID()
    
    def check_logout(self):        
        if self.home_page.signout:
            self.pages.setCurrentIndex(0)
            self.pages.removeWidget(self.home_page)
            self.home_page.destroy()
            
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
app.exec_()
