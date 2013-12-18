#!/usr/bin/python
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import sqlite3 as lite
import urllib2
import sys
import os

__author__ = 'Lemeshev Andrey'


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
        remote_res = urllib2.urlopen(url)
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
        if len(stack) > 6:
            elem = stack[len(stack) - 6]
            if elem.name == 'div' and 'class' in elem.attrs:
                if elem.attrs['class'] == 'gray toc' and name == 'a' \
                        and 'href' in attrs:
                        self.pages.append(attrs['href'])


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
        curr = self.__conn
        curr.execute('INSERT INTO COMICS(TITLE, PAGE_URL) VALUES ( ?, ? )', title, page_url)
        curr.close()

    def get_comics(self, title):
        curr = self.__conn
        curr.execute('SELECT * FROM COMICS WHERE TITLE = ?', title)
        comics = curr.fetchone()
        curr.close()
        return comics

    def add_strip(self, comics_id, title, file_url):
        curr = self.__conn
        curr.execute('INSERT INTO STRIPS(COMICS_ID, TITLE, FILE_URL) VALUES ( ?, ?, ? )',
                     comics_id, title, file_url)
        curr.close()

    def get_strips(self, comics_id):
        curr = self.__conn
        curr.execute('SELECT * FROM STRIPS WHERE COMICS_ID = ?', comics_id)
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
        res = urllib2.urlopen(url)
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
            print(str(ind) + ') ' + title)

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

    class CollectionIndex:
        def __init__(self, pages, titles):
            self.pages = pages
            self.titles = titles


def main():
    SITE_URL = 'http://comicsia.ru/'
    DATABASE_FILE = '/home/andrey/work/data/comic.db'

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