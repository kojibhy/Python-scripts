#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Python 3.4
# made by  Xtr3am3r.0k@gmail.com
# pip install bs4
import re
import argparse
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Site Email spider')
parser.add_argument('-u','--url', help='set url in format http://exemple.com', required=True)
args = vars(parser.parse_args())

tasklist = []
perfected = []
fond_mails = {}

def site_url(request):
    main_link = urllib.parse.urlparse(request)
    if request in perfected:
        pass
    elif request in tasklist:
        pass
    else:
        tasklist.append(request)

def page_srch(request):
    try:
        html = urllib.request.urlopen(request).read().decode('utf-8', errors='ignore')
    except:
        html = urllib.request.urlopen(perfected[0]).read().decode('utf-8', errors='ignore')
    mailsrch = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-\.]+[a-zA-Z]{1,4}')
    found = mailsrch.findall(html)
    for item in found:
        fond_mails[item] = 1

def spider_searcher(request):
    found_links = []
    search = re.compile(r'^/\w+')
    try:
        html = urllib.request.urlopen(request).read().decode('utf-8', errors='ignore')
    except:
        html = urllib.request.urlopen(perfected[0]).read().decode('utf-8', errors='ignore')
    pars_link = urllib.parse.urlparse(request)
    soup = (BeautifulSoup(html, "html.parser")).findAll('a')
    for link in soup:
        newlink = str(link).split(' ')[1].split('"')[1]
        if 'http' in newlink:
            found_links.append(newlink)
        elif search.findall(newlink):
            found_links.append(newlink)
        else:
            pass
    for url in found_links:
        request_link = urllib.parse.urlparse(url)
        site_url(pars_link[0] + '://' + pars_link[1] + request_link[2])


def spider():
    try:
        while len(tasklist) != 0:
            for item in tasklist:
                print('++++'*64)
                print('[*] request links left=', len(tasklist))
                print('[*] response links status=', len(perfected))
                print('[*] Emails found =', len(fond_mails))
                print('Press Ctrl+C to exit')
                spider_searcher(item)
                page_srch(item)
                perfected.append(str(item))
                del tasklist[tasklist.index(item)]
            print('----' * 64)
            print('[+] STATUS..............')
            print('[*] request links left=', len(tasklist))
            print('[*] response links status=', len(perfected))
            print('[*] Emails found =', len(fond_mails))
            for items in fond_mails:
                print(items)

    except KeyboardInterrupt:
        print('----' * 64)
        print('[+] STATUS..............')
        print('[*] request links left=', len(tasklist))
        print('[*] response links status=', len(perfected))
        print('[*] Emails found =', len(fond_mails))
        for items in fond_mails:
            print(items)
if __name__ == "__main__":
    site_url(args['url'])
    spider()