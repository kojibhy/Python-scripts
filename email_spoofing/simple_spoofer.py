#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Python 3.4
# made by  Xtr3am3r.0k@gmail.com

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import Message
from email.header import make_header as mkh
from email.utils import make_msgid as msgid
from email.utils import formatdate


def sender():
    # smtp config loading
    login = ''
    password = ''
    host = ''
    port = '' #port mast be int

    #request config loading
    request_from = '' #From email
    request_to = '' #To email
    request_view = ''#
    request_subject = '' #
    request_text ='' #
    
    msg = Message()
    msg = MIMEMultipart('alternative')
    msg['Message-ID'] = msgid()
    msg['Date'] = formatdate(localtime=True)
    msg['From'] = mkh([('{}'.format(request_view), 'UTF-8'), ('<' + request_from + '>', 'us-ascii')])
    msg['To'] = request_to
    msg['Subject'] = request_subject
    msg['User-Agent'] = 'Horde Application Framework 5' # UA Exemple
    msg['Content-Disposition'] = "inline"
    msg['Content-Transfer-Encoding'] = "8bit"
    msg.attach(MIMEText(request_text, _subtype='html', _charset='utf-8'))
    msg.preamble = "This is a multi-part message in MIME format."
    msg.epilogue = "End of message"

    server = smtplib.SMTP_SSL(host, port)
    server.login(login, password)
    server.ehlo()
    server.sendmail(request_from, request_to, msg.as_string())
    server.quit()