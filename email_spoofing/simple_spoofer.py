#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Python 3.4
# made by  Xtr3am3r.0k@gmail.com


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sender():
    smtp_host_user = ""
    smtp_host_password = ""
    smtp_host = ''
    smtp_port = 465
    
    fromaddress = smtp_host_user
    toaddress = ''

    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = ""
    msg['From'] =  ""
    msg['To'] = toaddress
    msg.attach(MIMEText('<h1> Sender hello word from all citizens</h1>', 'html'))
    server = smtplib.SMTP_SSL(smtp_host, smtp_port)
    server.ehlo()
    print(server.ehlo())
    server.login(smtp_host_user,smtp_host_password)
    print(server.login(smtp_host_user, smtp_host_password))
    server.sendmail(fromaddress, toaddress,msg.as_string())
    server.quit()

sender()