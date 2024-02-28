from PyQt5 import QtCore, QtGui, QtWidgets
from login_page import Login_page
from home_page import Home_page

class Ui_MainWindow(object):
    def setupUi(self, MainWindow:QtWidgets.QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pages = QtWidgets.QStackedWidget(self.centralwidget)
        self.pages.setObjectName("pages")
        self.login_page = Login_page()
        self.pages.addWidget(self.login_page)
        self.home_page = Home_page()
        self.pages.addWidget(self.home_page)
        self.gridLayout.addWidget(self.pages, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.pages.setCurrentWidget(self.login_page)
        
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
