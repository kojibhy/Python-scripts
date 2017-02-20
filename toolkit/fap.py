#! /usr/bin/env python3
import os, sys
import subprocess
import argparse


class FakeAccessPoint(object):
    def __init__(self, iface, gateway,channel,name,password=None,debug=False):
        """iface, gateway,channel,name,password=None,debug=False"""
        self.iface=iface
        self.gateway=gateway
        self.channel=channel
        self.name =name
        self.password=password


        #BASE CONFIG
        self.debug=debug
        self.temp= os.path.join(os.getcwd(), 'temp')
        self.config_hostapd_name= 'hostapd.conf'
        self.config_dnsmasq_name='dnsmasq.conf'

    def main(self):
        # Work with interface and other things
        self.stop()

        self.call_subprocess(['ifconfig', self.iface, '10.16.1.1', 'netmask', '255.255.255.0'])

        status, msg = self.call_subprocess(['hostapd','-B','-t', os.path.join(self.temp,self.config_hostapd_name)])

        if 'AP-DISABLED' in msg:
            print('ERROR:\n {msg}'.format(msg=msg))
            sys.exit()
        else:
            self.call_subprocess(['dnsmasq', '-C', os.path.join(self.temp,self.config_dnsmasq_name)])
            self.call_subprocess(['sysctl', '-w', 'net.ipv4.ip_forward=1'])

        # Clean UP IPTABLES + add new Rules

            self.call_subprocess(
                ['iptables', '-A', 'FORWARD', '-i', self.gateway, '-o', self.iface, '-m', 'state', '--state',
                 'ESTABLISHED,RELATED', '-j', 'ACCEPT'])

            # iptables -A FORWARD -i wlan1   -o wlan0 -j ACCEPT
            self.call_subprocess(['iptables', '-A', 'FORWARD', '-i', self.iface, '-o', self.gateway, '-j', 'ACCEPT'])


            # iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
            self.call_subprocess(
                ['iptables', '-A', 'FORWARD', '-m', 'conntrack', '--ctstate', 'ESTABLISHED,RELATED', '-j', 'ACCEPT'])

            # iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
            self.call_subprocess(['iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', self.gateway, '-j', 'MASQUERADE'])

            print('[+] AP-ENABLED')

    def call_subprocess(self,command):
        if self.debug:
            print(' '.join(command))

        call = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        msg_ok = call.stdout.read()
        msg_error= call.stderr.read()

        if msg_error.__len__() !=0:
            if self.debug:
                print(msg_error.decode())
            return False, msg_error.decode()

        else:
            if self.debug:
                print(msg_ok.decode())
            return True, msg_ok.decode()

    def start(self):
        self.check_file_exists(self.temp, self.config_hostapd_name)
        self.check_file_exists(self.temp, self.config_dnsmasq_name)

        # create hostapd config
        self.hostapd()
        self.dnsmasq()

        self.main()

    def stop(self):
        commands_pool = [
            ['killall', 'hostapd'],
            ['killall', 'dnsmasq'],
            ['service', 'hostapd', 'stop'],
            ['service', 'dnsmasq', 'stop'],
            ['ifconfig', self.iface, '0.0.0.0'],

        ]
        for key in commands_pool:
            self.call_subprocess(key)

        return True

    def hostapd(self):
        # base config template for hostapd
        config = []
        config.append('interface={iface}'.format(iface=self.iface))
        config.append('driver=nl80211')
        config.append('ssid={name}'.format(name=self.name))
        config.append('hw_mode=g')
        config.append('channel={channel}'.format(channel=self.channel))
        config.append('macaddr_acl=0')
        config.append('ignore_broadcast_ssid=0')
        if self.password is not None:
            config.append('wpa=2')
            config.append('wpa_passphrase={password}'.format(password=self.password))

        config_template = '\n'.join(config)

        self.save_config(os.path.join(self.temp,self.config_hostapd_name), config_template)

    def dnsmasq(self):
        config = []
        config.append('no-resolv')
        config.append('server=8.8.8.8')
        config.append('server=8.8.8.4')
        config.append('interface={iface}'.format(iface=self.iface))
        config.append('listen-address=10.16.1.1') # you can add as Parametr if you want
        config.append('bind-interfaces')
        config.append('dhcp-range=10.16.1.1,10.16.1.250,255.255.255.0,12h')
        config.append('dhcp-option=3,10.16.1.1')
        config.append('dhcp-option=6,10.16.1.1')

        config_template= '\n'.join(config)

        self.save_config(os.path.join(self.temp, self.config_dnsmasq_name), config_template)

    def save_config(self, path,config):
        with open(path, 'w') as file:
            file.write(config)

    def check_file_exists(self, path,filename):
        if os.path.exists(path):
            if os.path.exists(os.path.join(path,filename)):
                os.remove(os.path.join(path,filename))
                if self.debug:
                    print('[*] Remove Temp Files {}'.format(filename))
            else:
                if self.debug:
                    print('[*] no config {}'.format(filename))
                else:
                    pass
        else:
            os.mkdir(path)
            if self.debug:
                print('[+] making new path:  {}'.format(path))


if __name__=="__main__":
    def parse_args():
        parser = argparse.ArgumentParser(description='Create WIFI Accesspoint')

        parser.add_argument(
            '-i',
            '--iface',
            help=(
                "Select iface"
            ),
            required=True
        )
        parser.add_argument(
            '-g',
            '--gateway',
            help=(
                "Select iface for gateway"
            ),
            required=True

        )
        parser.add_argument(
            '-s',
            '--ssid',
            help=(
                "Select Name for FAP"
            ),
            default=' '

        )
        parser.add_argument(
            '-p',
            '--password',
            help=(
                "Select Password"
            )
        )
        parser.add_argument(
            '-c',
            '--channel',
            help=(
                "Select Channel"
            ),
            default=6
        )
        parser.add_argument(
            '-d',
            '--debug',

            help=(
                "Select iface"
            ),
            action='store_true'
        )
        parser.add_argument(
            '--stop',

            help=(
                "Select iface"
            ),
            action='store_true'
        )

        return parser.parse_args()
    args=parse_args()

    if args.password and (len(args.password) < 8 or len(args.password) > 64):
        sys.exit('[-] Password must be beetween 8 and 63 printable characters')
    if args.password == '':
        password=None
    else:
        password = args.password

    if args.stop:
        commands_pool = [
            ['killall', 'hostapd'],
            ['killall', 'dnsmasq'],
            ['service', 'hostapd', 'stop'],
            ['service', 'dnsmasq', 'stop']
        ]
        for key in commands_pool:
            subprocess.Popen(key, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    fap=FakeAccessPoint(iface=args.iface, gateway=args.gateway,channel=args.channel,name=args.ssid,debug=args.debug, password=password)

    fap.start()