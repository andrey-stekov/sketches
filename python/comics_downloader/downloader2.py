#!/usr/bin/python
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import sqlite3 as lite
import urllib2
import getpass
import sys
import os

__author__ = 'Lemeshev Andrey'

### Configuration ###
SITE_URL = 'http://comicsia.ru'
DATABASE_FILE = '/home/andrey/work/data/comic.db'

PICTURE_NUMBER_LENGTH = 4

# Proxy settings #
USE_PROXY = False
PROXY_SCHEME = 'http'
PROXY_URL = 'HOST:PORT'
PROXY_USER = 'USERNAME'
# if None it will request from the shell #
PROXY_PASSWORD = None


def get_proxy_opener(proxyurl, proxyuser, proxypass, proxyscheme="http"):
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, proxyurl, proxyuser, proxypass)

    proxy_handler = urllib2.ProxyHandler({proxyscheme: proxyurl})
    proxy_auth_handler = urllib2.ProxyBasicAuthHandler(password_mgr)

    return urllib2.build_opener(proxy_handler, proxy_auth_handler)


def get_url_opener():
    global PROXY_PASSWORD
    if USE_PROXY:
        if PROXY_PASSWORD is None:
            PROXY_PASSWORD = getpass.getpass('Enter password for ' + PROXY_SCHEME +'-proxy: ')
        return get_proxy_opener(PROXY_URL, PROXY_USER, PROXY_PASSWORD, PROXY_SCHEME)
    else:
        return urllib2.build_opener()


class Downloader:
    __URL_SEPARATOR = '/'
    __EXT_SEPARATOR = '.'
    __CONTENT_LENGTH_KEY = 'Content-Length'

    def __init__(self, basedir):
        self.__basedir = basedir

    def __build_file_name(self, url, new_name):
        web_name = url[url.rfind(self.__URL_SEPARATOR) + 1:]

        if new_name is None:
            return self.__basedir + os.sep + web_name

        file_ext = web_name[web_name.rfind(self.__EXT_SEPARATOR):]
        return self.__basedir + os.sep + new_name + file_ext

    def download(self, url, new_name=None):
        remote_res = get_url_opener().open(url)
        file_name = self.__build_file_name(url, new_name)

        output = open(file_name, 'wb')
        file_len = int(remote_res.info()[self.__CONTENT_LENGTH_KEY])
        total_len = 0

        while total_len < file_len:
            tmp = remote_res.read()
            total_len += len(tmp)
            output.write(tmp)

        output.close()
        remote_res.close()


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__stack = []

    def __attrs_to_dict(self, attrs):
        dic = {}
        for item in attrs:
            dic.update({item[0].lower(): item[1]})
        return dic

    def handle__starttag(self, name, attrs, stack):
        pass

    def handle__startendtag(self, tag, attrs, stack):
        pass

    def handle__endtag(self, tag, stack):
        pass

    def handle__data(self, content, stack):
        pass

    class Elem:
        def __init__(self, name, attrs):
            self.name = name
            self.attrs = attrs

        def __repr__(self):
            return self.name + ' : ' + str(self.attrs)

    def handle_starttag(self, name, attrs):
        attributes = self.__attrs_to_dict(attrs)
        self.handle__starttag(name.lower(), attributes, self.__stack)
        self.__stack.append(self.Elem(name.lower(), attributes))

    def handle_startendtag(self, tag, attrs):
        attributes = self.__attrs_to_dict(attrs)
        self.handle__startendtag(tag.lower(), attributes, self.__stack)

    def handle_endtag(self, tag):
        self.handle__endtag(tag.lower(), self.__stack)

        if len(self.__stack) == 0:
            raise Exception('Illegal state')
        self.__stack.pop()

    def handle_data(self, content):
        self.handle__data(content, self.__stack)


class CollectionParser(MyHTMLParser):
    def __init__(self):
        MyHTMLParser.__init__(self)
        self.pages = {}
        self.__title = None

    def handle__starttag(self, name, attrs, stack):
        if len(stack) > 0:
            elem = stack[len(stack) - 1]
            if elem.name == 'div' and 'class' in elem.attrs:
                if elem.attrs['class'] == 'container' and name == 'a' \
                    and 'title' in attrs:
                    self.__title = attrs['title']
                elif elem.attrs['class'] == 'title' and name == 'a' \
                    and 'href' in attrs and self.__title is not None:
                    self.pages[self.__title] = attrs['href']
                    self.__title = None


class InfoPageParser(MyHTMLParser):
    def __init__(self):
        MyHTMLParser.__init__(self)
        self.pages = []

    def handle__starttag(self, name, attrs, stack):
        if len(stack) > 5:
            elem = stack[len(stack) - 4]
            if elem.name == 'div' and 'class' in elem.attrs and \
                elem.attrs['class'] == 'gray toc' and name == 'a' \
                    and 'href' in attrs:
                        self.pages.append(attrs['href'])


class StripsParser(MyHTMLParser):
    def __init__(self):
        MyHTMLParser.__init__(self)
        self.strips = []
        self.__title = None

    class Strip:
        def __init__(self, title, url):
            self.title = title
            self.url = url

    def handle__data(self, content, stack):
        if len(stack) > 4:
            current = stack[len(stack) - 1]
            second = stack[len(stack) - 2]
            third = stack[len(stack) - 3]

            if current.name == 'a' and second.name == 'div' and \
                'class' in second.attrs and second.attrs['class'] == 'title' \
                and third.name == 'div' and 'class' in third.attrs \
                and third.attrs['class'] == 'strips':
                    self.__title = content

    def handle__startendtag(self, tag, attrs, stack):
        if len(stack) > 3:
            elem = stack[len(stack) - 2]

            if self.__title is not None and tag == 'img' and \
                elem.name == 'div' and 'class' in elem.attrs and \
                elem.attrs['class'] == 'strip' and 'src' in attrs:
                    self.strips.append(self.Strip(self.__title, attrs['src']))
                    self.__title = None


class ComicDAO:
    def __init__(self, dbfile):
        self.__conn = lite.connect(dbfile)

        try:
            curr = self.__conn.cursor()
            curr.execute('SELECT COUNT() FROM COMICS')
            curr.close()
        except lite.Error, e:
            ### Trying to create service tables ###
            curr = self.__conn.cursor()
            curr.execute('CREATE TABLE COMICS(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                         + 'TITLE VARCHAR(1024) NOT NULL, PAGE_URL VARCHAR(2048) NOT NULL)')
            curr.execute('CREATE TABLE STRIPS(ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                         + 'COMICS_ID INTEGER NOT NULL, TITLE VARCHAR(1024) NOT NULL,'
                         + 'FILE_URL VARCHAR(2048) NOT NULL)')
            curr.close()

    def add_comics(self, title, page_url):
        curr = self.__conn.cursor()
        curr.execute('INSERT INTO COMICS(TITLE, PAGE_URL) VALUES ( ?, ? )', (title, page_url))
        curr.close()

    def get_comics(self, title):
        curr = self.__conn.cursor()
        curr.execute('SELECT * FROM COMICS WHERE TITLE = ?', [title])
        comics = curr.fetchone()
        self.__conn.commit()
        curr.close()
        return comics

    def add_strip(self, comics_id, title, file_url):
        curr = self.__conn.cursor()
        curr.execute('INSERT INTO STRIPS(COMICS_ID, TITLE, FILE_URL) VALUES ( ?, ?, ? )',
                     (comics_id, title, file_url))
        self.__conn.commit()
        curr.close()

    def get_strips(self, comics_id):
        curr = self.__conn.cursor()
        curr.execute('SELECT * FROM STRIPS WHERE COMICS_ID = ?', [comics_id])
        rows = curr.fetchall()
        curr.close()

        strips = {}

        for row in rows:
            strips[row[3]] = row

        return strips

    def finish(self):
        self.__conn.close()


class Spider:
    def __init__(self, base_url, metadata_file):
        self.__base_url = base_url
        self.__metadata_file = metadata_file

    def __parse_page(self, url, parser):
        res = get_url_opener().open(url)
        html = res.read()
        res.close()
        parser.feed(html.decode('utf-8'))
        return parser

    def __parse_collection(self):
        url = self.__base_url + '/collections/'
        parser = self.__parse_page(url, CollectionParser())
        titles = parser.pages.keys()
        titles.sort()

        return self.CollectionIndex(parser.pages, titles)

    def process_collection(self):
        index = self.__parse_collection()
        ind = 0
        for title in index.titles:
            ind += 1
            print str(ind) + ') ' + title

    def __build_name_index(self, index, length):
        tmp = str(index)
        diff = length - len(tmp)
        if diff > 0:
            for i in xrange(0, diff):
                tmp = '0' + tmp
        return tmp

    def __build_file_name(self, num, title):
        return self.__build_name_index(num, PICTURE_NUMBER_LENGTH) + ' - ' + title

    def process_comic(self, ind, folder):
        dao = ComicDAO(self.__metadata_file)
        index = self.__parse_collection()
        title = index.titles[ind - 1]
        info_page_url = index.pages[title]
        url = self.__base_url + info_page_url
        parser = self.__parse_page(url, InfoPageParser())
        dest_folder = os.path.normpath(folder + os.path.sep + title)

        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)

        print title
        print 'Pages count: ' + str(len(parser.pages))
        print 'Folder: ' + dest_folder
        print 'URL: ' + url
        print '==============================='

        comics = dao.get_comics(title)

        if comics is None:
            dao.add_comics(title, info_page_url)
            comics = dao.get_comics(title)

        cache = dao.get_strips(comics[0])

        downloader = Downloader(dest_folder)

        page_num = 0
        strip_num = 0
        
        for page in parser.pages:
            page_num += 1
            print 'Processing page ' + str(page_num) 
            parser = self.__parse_page(self.__base_url + page, StripsParser())
            
            for strip in parser.strips:
                strip_num += 1
                if strip.url not in cache:
                    downloader.download(strip.url, self.__build_file_name(strip_num, strip.title))
                    dao.add_strip(comics[0], strip.title, strip.url)

    class CollectionIndex:
        def __init__(self, pages, titles):
            self.pages = pages
            self.titles = titles


def main():
    spider = Spider(SITE_URL, DATABASE_FILE)
    argc = len(sys.argv)
    if argc == 1:
        spider.process_collection()
    elif argc == 2:
        spider.process_comic(int(sys.argv[1]), os.path.dirname(os.path.realpath(__file__)))
    elif argc == 3:
        spider.process_comic(int(sys.argv[1]), os.path.normpath(sys.argv[2]))

if __name__ == '__main__':
    main()