from PyQt5.QtWidgets import QMessageBox
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
from tabulate import tabulate
import smtplib
import ssl


# show error message box
def ShowMessage(info, icon = QMessageBox.Critical):
    # for error message : use showErrorMessage method 
    msg = QMessageBox()
    msg.setIcon(icon)
    if icon == QMessageBox.Critical:
        msg.setWindowTitle("Error")
    else:
        msg.setWindowTitle("Info")
    msg.setText(info + "\t\n")
    msg.exec_()
    
    

# Define email sender and receiver
server = 'smtp.gmail.com:587'
email_sender = 'youssefhussein9880@gmail.com'
# email_password = os.environ.get('EMAIL_PASSWORD')
email_password = 'msivvuypvxzdexvf'
email_receiver = 'ymohamed9880@gmail.com'

def send_email( email_body):
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = 'Bank'
    em.set_content(email_body)
    
    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())



text = """
Hello, Friend.

Here is your data:

{table}

Regards,

Me"""

html = """
<html><body><p>Hello, Friend.</p>
<p>Here is your data:</p>
{table}
<p>Regards,</p>
<p>Me</p>
</body></html>
"""

text = text.format(table=tabulate(data, headers="firstrow", tablefmt="grid"))
html = html.format(table=tabulate(data, headers="firstrow", tablefmt="html"))

message = MIMEMultipart(
    "alternative", None, [MIMEText(text), MIMEText(html,'html')])

message['Subject'] = "Your data"
message['From'] = email_receiver
message['To'] = email_sender
server = smtplib.SMTP(server)
server.ehlo()
server.starttls()
server.login(email_sender, email_password)
server.sendmail(email_sender, email_receiver, message.as_string())
server.quit()

