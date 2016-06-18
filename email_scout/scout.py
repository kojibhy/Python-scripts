#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Python 3.4
# made by  Xtr3am3r.0k@gmail.com
# version 0.0.1
# pip install bs4
import re, os
import argparse
import urllib.request, urllib.error, urllib.parse
from bs4 import BeautifulSoup


class Spider:
    def __init__(self):
        self.tasklist = []
        self.perfected = []
        self.fond_mails = {}

    def add_task(self, request):
        main_link = urllib.parse.urlparse(request)
        if request in self.perfected:
            pass
        elif request in self.tasklist:
            pass
        else:
            self.tasklist.append(request)

    def srch_page(self, request):
        html = urllib.request.urlopen(request).read().decode()
        mailsrch = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
        found = mailsrch.findall(html)
        for item in found:
            self.fond_mails[item] = 1
    def spider_searcher(self, request):
        found_links = []
        search = re.compile(r'^/\w+')
        html = urllib.request.urlopen(request).read().decode()
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
            self.add_task(pars_link[0] + '://' + pars_link[1] + request_link[2])


    def spider(self):
        while len(self.tasklist) != 0:
            for item in self.tasklist:
                self.printall(item)
                try:
                    self.spider_searcher(item)
                except (KeyboardInterrupt, EOFError) as err:
                    raise
                except:
                    pass
                try:
                    self.srch_page(item)
                except (KeyboardInterrupt, EOFError) as err:
                    raise
                except:
                    pass
                self.perfected.append(str(item))
                del self.tasklist[self.tasklist.index(item)]
    def __str__(self):
        found= ''
        for items in list(self.fond_mails):
            found += '{}\n'.format(items)
        return found

    def printall(self, request):
        print('+' * 64, '\n [+] current link in process = {}'.format(request),
                '\n [*] request links left= {}\n'.format(len(self.tasklist)),
                '[*] response links status= {}\n'.format(len(self.perfected)),
                '[*] Emails found not sorted = {}\n'.format(len(self.fond_mails)),
                'Press Ctrl+C to exit\n')
    def filewriter(self):
        found = ''
        for items in list(self.fond_mails):
            try:
                found += '{}\n'.format(str(items))
            except:
                pass
        return found



def main():
    site_parse = Spider()
    site_parse.add_task(args['url'])
    print('Start Program...')
    try:
        site_parse.spider()
    except KeyboardInterrupt:
        print('\n\n[-] KeyboardInterrupt = Exit')
    print('Program Ends...')
    print(site_parse,'\n [+] all results write in found_emails.txt')
    with open('found_emails.txt', 'w') as file:
        file.write(site_parse.filewriter())
        file.close()



parser = argparse.ArgumentParser(description='Site Email spider')
parser.add_argument('-u', '--url', help='set url in format http://exemple.com', required=True)

args = vars(parser.parse_args())



if __name__ == "__main__":
    main()


