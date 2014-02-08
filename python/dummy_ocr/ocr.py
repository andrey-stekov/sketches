#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, sys, re
from PIL import Image

__author__ = 'Lemeshev Andrey'

### Configuration ###
PATTERNS = {
    '0': '0.png',
    '1': '1.png',
    '2': '2.png',
    '3': '3.png',
    '4': '4.png',
    '5': '5.png',
    '6': '6.png',
    '7': '7.png',
    '8': '8.png',
    '9': '9.png',
    '.': 'dot.png',
    ':': 'colon.png'
}

PATTERNS_PATH = 'patterns'

PATTERN_WIDTH = 6
PATTERN_HEIGHT = 6

REGION_X_COORD = 122
REGION_Y_COORD = 432
REGION_WIDTH = 400
REGION_HEIGHT = 288

def module_path(rel_path):
    return os.getcwd() + \
            os.sep + rel_path + os.sep

def load_bw_image(path):
    col = Image.open(path)
    gray = col.convert('L')
    bw = gray.point(lambda x: 0 if x < 128 else 255, '1')
    return bw


def load_patterns():
    patterns = {}

    for pattern in PATTERNS:
        patterns[pattern] = load_bw_image(module_path(PATTERNS_PATH) + PATTERNS[pattern])

    return patterns


def compare_with_pattern(image, x, y, pattern):
    for i in xrange(0, PATTERN_WIDTH):
        for j in xrange(0, PATTERN_HEIGHT):
            ip = image.getpixel((x + i, y + j))
            pp = pattern.getpixel((i, j))
            if ip != pp:
                return False
    return True


def classify_region(image, x, y, patterns):
    char = None

    for pattern in PATTERNS:
        if compare_with_pattern(image, x, y, patterns[pattern]):
            char = pattern

    return char


def process_image(path):
    patterns = load_patterns()
    image = load_bw_image(path)

    i = REGION_Y_COORD
    wasFounded = False
    while i < REGION_Y_COORD + REGION_HEIGHT:
        text = ''
        j = REGION_X_COORD
        while j < REGION_X_COORD + REGION_WIDTH:
            char = classify_region(image, j, i, patterns)
            j += 1 if char is None else PATTERN_WIDTH
            text += char if char is not None else ' '
        text = text.strip()

        if len(text) is 0:
            if wasFounded:
                i -= 1
                wasFounded = False
            else:
                i += 1
        else:
            wasFounded = True
            i += 2 * PATTERN_HEIGHT
            print re.sub('\s+', '\t', text)


def main():
    argc = len(sys.argv)
    if argc == 1:
        print 'Need file-name'
    elif argc == 2:
        process_image(sys.argv[1])

if __name__ == '__main__':
    main()
