#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import os
from HTMLParser import HTMLParser
import sys

__author__ = 'Lemeshev Andrey'

CLASS_ATTRIBUTE = 'class'
TITLE_ATTRIBUTE = 'title'
HREF_ATTRIBUTE = 'href'
SRC_ATTRIBUTE = 'src'

ANCHOR_TAG = 'a'
DIV_TAG = 'div'
H1_TAG = 'h1'
IMAGE_TAG = 'img'


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


class StateMachine:
    def __init__(self, states, state):
        self.__states = states
        self.__state = state
        self.__rules = {}
        self.__handlers = {}

    class Edge:
        def __init__(self, to, condition):
            self.to = to
            self.condition = condition

    def add_rule(self, from_state, to_state, condition):
        if from_state not in self.__states or to_state not in self.__states:
            raise Exception("Illegal state")

        self.__rules[from_state] = StateMachine.Edge(to_state, condition)
        return self

    def add_handler(self, state, handler):
        if state not in self.__states:
            raise Exception("Illegal state")

        self.__handlers[state] = handler
        return self

    def iterate(self, tag, attrs):
        attributes = attrs_to_dict(attrs)
        edge = self.__rules[self.__state]

        if edge.condition(tag, attributes):
            self.__state = edge.to

        if self.__state in self.__handlers:
            handler = self.__handlers[self.__state]
            handler(tag, attributes)

def attrs_to_dict(attrs):
    dic = {}
    for item in attrs:
        dic.update({item[0]: item[1]})
    return dic


class InfoPageHandler(HTMLParser):
    __TITLE_TAG = 'title'
    __AUTHOR_TAG = 'authors'
    __GREY_TOK_TAG = 'gray toc'

    def __init__(self):
        HTMLParser.__init__(self)
        self.__element = None

        self.title = None
        self.author = None
        self.pages = []

    def handle_starttag(self, name, attrs):
        attributes = attrs_to_dict(attrs)
        if name.lower() == H1_TAG and CLASS_ATTRIBUTE in attributes \
            and attributes[CLASS_ATTRIBUTE] == self.__TITLE_TAG:
            self.__element = self.__TITLE_TAG
        elif name.lower() == DIV_TAG and CLASS_ATTRIBUTE in attributes \
            and attributes[CLASS_ATTRIBUTE] == self.__AUTHOR_TAG:
            self.__element = self.__AUTHOR_TAG
        elif name.lower() == DIV_TAG and CLASS_ATTRIBUTE in attributes \
            and attributes[CLASS_ATTRIBUTE] == self.__GREY_TOK_TAG:
            self.__element = self.__GREY_TOK_TAG
        elif self.__element == self.__GREY_TOK_TAG and name.lower() == ANCHOR_TAG:
            self.pages.append(attributes[HREF_ATTRIBUTE])

    def handle_endtag(self, tag):
        if self.__element == self.__GREY_TOK_TAG and tag.lower() == DIV_TAG:
            self.__element = None

    def handle_data(self, content):
        if self.__element is None:
            return

        if self.__element == self.__TITLE_TAG:
            self.title = content
            self.__element = None
        if self.__element == self.__AUTHOR_TAG:
            self.author = content
            self.__element = None


class CollectionPageHandler(HTMLParser):
    __TITLE_TAG = 'title'
    __CONTAINER_TAG = 'container'

    def __init__(self):
        HTMLParser.__init__(self)

        self.__element = None
        self.pages = []

    def handle_starttag(self, name, attrs):
        attributes = attrs_to_dict(attrs)
        if name.lower() == DIV_TAG and CLASS_ATTRIBUTE in attributes \
            and attributes[CLASS_ATTRIBUTE] == self.__TITLE_TAG:
            self.__element = self.__TITLE_TAG
        elif name.lower() == DIV_TAG and CLASS_ATTRIBUTE in attributes \
            and attributes[CLASS_ATTRIBUTE] == self.__CONTAINER_TAG \
            and self.__element == self.__TITLE_TAG:
            self.__element = self.__CONTAINER_TAG
        elif self.__element == self.__CONTAINER_TAG and CLASS_ATTRIBUTE in attributes \
            and attributes[CLASS_ATTRIBUTE] == self.__TITLE_TAG:
            self.__element = self.__TITLE_TAG
        elif self.__element == self.__TITLE_TAG:
            if name.lower() == ANCHOR_TAG:
                self.pages.append({'title': attributes[TITLE_ATTRIBUTE], 'url': attributes[HREF_ATTRIBUTE]})
                self.__element = None
            else:
                self.__element = None


class StripsPageHandler(HTMLParser):
    __TITLE_TAG = 'title'
    __STRIP_TAG = 'strip'
    __ANCHOR_TITLE = 'anchor_title'

    def __init__(self):
        HTMLParser.__init__(self)

        self.__element = None
        self.__title = None
        self.strips = []

    def handle_starttag(self, name, attrs):
        attributes = attrs_to_dict(attrs)
        if name.lower() == DIV_TAG and CLASS_ATTRIBUTE in attributes \
            and attributes[CLASS_ATTRIBUTE] == self.__TITLE_TAG:
            self.__element = self.__TITLE_TAG
        elif name.lower() == DIV_TAG and CLASS_ATTRIBUTE in attributes \
            and attributes[CLASS_ATTRIBUTE] == self.__STRIP_TAG:
            self.__element = self.__STRIP_TAG
        elif self.__element == self.__TITLE_TAG and name.lower() == ANCHOR_TAG:
            self.__element = self.__ANCHOR_TITLE
        elif self.__element == self.__STRIP_TAG and name.lower() == IMAGE_TAG:
            self.strips.append({'url': attributes[SRC_ATTRIBUTE], 'new_name': self.__title})
            self.__title = None
            self.__element = None

    def handle_data(self, data):
        if self.__element == self.__ANCHOR_TITLE:
            self.__title = data
            self.__element = None


class Spider:
    def __init__(self, base_url):
        self.__base_url = base_url

    def __parse_page(self, url, handler):
        res = urllib2.urlopen(url)
        html = res.read()
        res.close()
        handler.feed(html.decode('utf-8'))
        return handler

    def parse_first_page(self, first_page_path):
        url = self.__base_url + first_page_path
        return self.__parse_page(url, InfoPageHandler())

    def parse_collection(self):
        url = self.__base_url + '/collections/'
        return self.__parse_page(url, CollectionPageHandler())

    def parse_page(self, page_path):
        url = self.__base_url + page_path
        return self.__parse_page(url, StripsPageHandler())


def build_name_index(index, length):
    tmp = str(index)
    diff = length - len(tmp)
    if diff > 0:
        for i in xrange(0, diff):
            tmp = '0' + tmp
    return tmp


def build_name(index, length, comic_name, name):
    return comic_name + ' - ' + build_name_index(index, length) + ' - ' + name


def main():
    SITE_URL = 'http://comicsia.ru/'
    DOWNLOAD_FOLDER = '/home/andrey/tmp'

    spider = Spider(SITE_URL)

    if len(sys.argv) == 1:
        bean = spider.parse_collection()

        ind = 0
        for comic in bean.pages:
            ind += 1
            print(str(ind) + ') ' + comic['title'])
    elif len(sys.argv) == 3 and (sys.argv[1] == '-i' or sys.argv[1] == '-l'):
        bean = spider.parse_collection()
        page = bean.pages[int(sys.argv[2]) - 1]
        info = spider.parse_first_page(page['url'])
        title = page['title']

        print title
        print 'Author: ' + info.author
        print 'Pages: ' + str(len(info.pages))

        if sys.argv[1] == '-l':
            print '================================'

            num = 0
            index = 0
            downloader = Downloader(DOWNLOAD_FOLDER)

            for page in info.pages:
                num += 1
                print 'Processing page ' + str(num) + ' from ' + str(len(info.pages))
                strips_info = spider.parse_page(page)
                for strip in strips_info.strips:
                    index += 1
                    downloader.download(strip['url'],
                                        build_name(index, 3, title, strip['new_name']))


if __name__ == '__main__':
    main()