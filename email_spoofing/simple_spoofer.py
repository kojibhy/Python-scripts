#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Python 3.4
# made by  Xtr3am3r.0k@gmail.com

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import make_header
from email.utils import make_msgid
from email.utils import formatdate


class EmailSender():
    def __init__(self, **kwargs):
        self.login = kwargs['login']
        self.password = kwargs['password']
        self.host = kwargs['host']
        self.port = int(kwargs['port'])
        self.from_email = kwargs['from_email']
        self.from_text = kwargs['from_text']
        self.to = kwargs['to']
        self.subject = kwargs['subject']
        self.message_text = kwargs['message_text']

    def masseges(self):
        msg = MIMEMultipart()
        msg['Message-ID'] = make_msgid()
        msg['Date'] = formatdate(localtime=True)
        msg['From'] = make_header([('{}'.format(self.from_text), 'UTF-8'), ('<' + self.from_email + '>', 'us-ascii')])
        msg['To'] = self.to
        msg['Subject'] = self.subject
        msg['User-Agent'] = 'Horde Application Framework 5'
        msg['Content-Disposition'] = "inline"
        msg['Content-Transfer-Encoding'] = "8bit"
        msg.attach(MIMEText(self.message_text, _subtype='html', _charset='utf-8'))
        return(msg)

    def chainsend(self):
        server = smtplib.SMTP_SSL(self.host, self.port)
        authentication = server.login(self.login, self.password)
        echo = server.ehlo()
        awere = server.sendmail(self.from_email, self.to, self.masseges().as_string())
        server.quit()


if __name__ == '__main__':
    print('Debug mode')
    d = EmailSender(**{'login': '',
                       'password': '',
                       'host': 'smtp.mail.ru',
                       'port': 465,
                       'from_email': '',
                       'from_text': '',
                       'to': '',
                       'subject': '',
                       'message_text': '<img src="" width="500" height="900" align="center" />'
                       })
    d.chainsend()
