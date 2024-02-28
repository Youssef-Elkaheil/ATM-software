import smtplib
import ssl
from email.message import EmailMessage
import os
import datetime
import time

# Define email sender and receiver
email_sender = 'youssefhussein9880@gmail.com'
email_password = os.environ.get('EMAIL_PASSWORD')
#email_password = 'msivvuypvxzdexvf'
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
        
