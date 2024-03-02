from PyQt5.QtWidgets import QMessageBox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from prettytable import PrettyTable
import smtplib
import datetime
import os


# Your ATM project likely has these structures already
class Transaction:
    def __init__(self, type, amount):
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        self.type = type
        self.amount = amount

class Response:
    def __init__(self, client_email, client_firstname) -> None:

        self.__server = smtplib.SMTP('smtp.gmail.com:587')
        
        # Define server , company email
        self.__server.ehlo()
        self.__server.starttls()
        self.__client_email = client_email
        self.__client_name = client_firstname
        
        self.__company_email = os.environ.get('EMAIL_ADDRESS')
        self.__company_email_password = os.environ.get('EMAIL_PASSWORD')

        self.__server.login(self.__company_email, self.__company_email_password)
        
        self.table = PrettyTable()
        self.table.field_names = ["date", "type", "amount"]       
        
        self.text = "\nHello, {name}.\n"
        self.text += "Your current balance : EGP {balance}.\n\n"
        self.text += "Here is your Transaction History:\n\n"
        self.text += "{table}\n\nBest Regards,\nBank"
        self.html = "\n<html><body><p>Hello, {name}.<br></p>\n"
        self.html += "<p>Your current balance : EGP {balance}.<br><br></p>\n\n"
        self.html += "<p>Here is your Transaction History:</p>\n\n"
        self.html += "<p>{table}</p>\n\n<br><br><p>Regards,</p><p>Bank</p></body></html>"
            
    def send_email(self, email_body):
        em = EmailMessage()
        em['From'] = self.__company_email
        em['To'] = self.__client_email 
        em['Subject'] = 'Bank Transaction'
        em.set_content(email_body)

        # send the email
        self.__server.sendmail(self.__company_email, self.__client_email , em.as_string())
    
    def send_history(self, balance, data):

        for trasaction in data:
            self.table.add_row([trasaction['date'],trasaction['type'],trasaction['amount']])
        
        self.text = self.text.format(name=f"{self.__client_name}",
                                    balance=f"{balance}",
                                    table=self.table
                                    )
        self.html = self.html.format(name=f"{self.__client_name}",
                                     balance=f"{balance}",
                                     table=self.table.get_html_string(format = True)
                                    )
 
        message = MIMEMultipart("alternative", None, [MIMEText(self.text), MIMEText(self.html,'html')])
        message['Subject'] = "Bank Transaction History"
        message['From'] = self.__company_email
        message['To'] = self.__client_email 
        self.__server.sendmail(self.__company_email, self.__client_email , message.as_string())

    # show error message box
    @staticmethod
    def ShowMessage( info, icon = QMessageBox.Critical):
        # for error message : use showErrorMessage method 
        msg = QMessageBox()
        msg.setIcon(icon)
        if icon == QMessageBox.Critical:
            msg.setWindowTitle("Error")
        else:
            msg.setWindowTitle("Info")
        msg.setText(info + "\t\n")
        msg.exec_()
