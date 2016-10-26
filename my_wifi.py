import os
import sys
from subprocess import Popen, PIPE
import argparse
import time

BASE_DIR = os.getcwd()
args = 0
def parse_args():
    # Create the arguments
    parser = argparse.ArgumentParser(description='WIFI AP')
    parser.add_argument(
        "-i",
        "--interface",
        help=("Select wlan* interface. " +
              "default 'wlan0'"
              )
    )
    parser.add_argument(
        "-s",
        "--ssid",
        help=("Enter the ESSID of the rogue Access Point. " +
              "Example: --ssid 'Free WiFi'." +
              "default name 'Free-WIFI'"
              )
    )
    parser.add_argument(
        "-pK",
        "--presharedkey",
        help=("Add WPA/WPA2 protection on the rogue Access Point. " +
              "Example: -pK s3cr3tp4ssw0rd"))
    parser.add_argument(
        "-c",
        "--channel",
        help=("select channel. " +
              "default  '6'"))


    return parser.parse_args()

def make_config(wlan=None,name=None,chanel=None, password=None):
    print('[+] Building config AP interface....\n[+] interface= {wifi_wlan}\n[+] ssid= {wifi_name}\n[+] channel= {wifi_chanel}\n[+] wpa_passphrase= {pwd}'.format(
        wifi_wlan=wlan, wifi_name=name, wifi_chanel=chanel, pwd=password))
    hostapd = (
        'interface={wifi_wlan}\n'
        'driver=nl80211\n'
        'ssid={wifi_name}\n'
        'hw_mode=g\n'
        'channel={wifi_chanel}\n'
        'macaddr_acl=0\n'
        'ignore_broadcast_ssid=0\n'.format(wifi_wlan=wlan, wifi_name=name, wifi_chanel=chanel))
    if password != None:
       hostapd += ('wpa=2\n'
                   'wpa_passphrase={pwd}\n').format(pwd=password)
    dnsmasq= ('interface={wifi_wlan}\n'
              'dhcp-range=10.0.0.10,10.0.0.250,12h\n'
              'dhcp-option=3,10.0.0.1\n'
              'dhcp-option=6,10.0.0.1\n'
              'server=8.8.8.8\n').format(wifi_wlan=wlan)
    with open('hostapd.conf', 'w') as config_hostapd:
        config_hostapd.write(hostapd)
        config_hostapd.close()
    with open('dnsmasq.conf', 'w') as config_dnsmasq:
        config_dnsmasq.write(dnsmasq)
        config_dnsmasq.close()
def check_args(args):
    """Checks the given arguments for logic errors."""
    if args.presharedkey and (len(args.presharedkey) < 8  or len(args.presharedkey) > 64):
        sys.exit('[-] Pre-shared key must be between 8 and 63 printable characters.')

    if args.interface == None:
        args.interface = 'wlan0'
    if args.ssid == None:
        args.ssid = 'Free-WIFI'
    if args.channel == None:
        args.channel = '6'
def start_extentions(wlan=None):
    def execute(obj):
        with Popen(obj, stdout=PIPE) as proc:
            print(proc.stdout.read().decode())

    execute(['killall', 'hostapd'])
    execute(['killall', 'dnsmasq'])

    time.sleep(3)

    hostapd_conf_dir = BASE_DIR + '/' + 'hostapd.conf'
    dnsmasq_conf_dir = BASE_DIR + '/' + 'dnsmasq.conf'

    execute(['service', 'network-manager','stop'])
    execute(['ifconfig', wlan, '10.0.0.1'])
    execute(['ifconfig', wlan, 'up'])

    os.system("gnome-terminal -e 'bash -c \"hostapd -t {} ; exec bash\"'".format(hostapd_conf_dir))
    os.system("gnome-terminal -e 'bash -c \"dnsmasq -C {}  -d; exec bash\"'".format(dnsmasq_conf_dir))

def start_app():
    args = parse_args()
    check_args(args)
    make_config(wlan=args.interface, name=args.ssid, chanel=args.channel,password=args.presharedkey)
    start_extentions(wlan=args.interface)


if __name__ == "__main__":
    start_app()


