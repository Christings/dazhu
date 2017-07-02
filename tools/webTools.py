'''
Created on Mar 12, 2016

@author: yzh
'''
# coding: utf-8
import logging
import os
import base64
import re
import HTMLParser
import dazhu.settings as settings
import random
import time
import datetime

def GetRndStr():
    rndByte = os.urandom(6)
    b64Str = base64.urlsafe_b64encode(rndByte)
    return b64Str

def GetMap(input):
    return chr(input + 97)

def GetTimeCode(input=0):
    '''
    0 - a
    1 - b
    25 - z
    26 - aa
    '''
    if input == 0:
        input = int(time.time())*100 + random.randint(1, 99)

    result = ""
    while True:
        quotient = input // 26
        remainder = input - quotient * 26
        input = quotient
        result = GetMap(remainder) + result
        if quotient < 26:
            if quotient == 0:
                break
            result = GetMap(quotient-1) + result
            break
    return result

def get_utc_timestamp():
    d = datetime.datetime.utcnow()
    epoch = datetime.datetime(1970,1,1)
    t = (d - epoch).total_seconds()
    return t


def RemoveHttpStr(val):
    # '<[^>]*>|&[^;]*;'
    return re.sub('<[^>]*>', '', val)

def RemoveHtmlTag(htmlstr,allowTags):
    class parseLinks(HTMLParser.HTMLParser):
        def __init__(self):
            HTMLParser.HTMLParser.__init__(self)
            self.result = ""

        def handle_starttag(self, tag, attrs):
            if tag in allowTags:
                self.result += self.get_starttag_text()

        def handle_endtag(self, tag):
            if tag in allowTags:
                self.result += "</"+tag+">"

        def handle_data(self, data):
                self.result+= data

    lParser = parseLinks()
    lParser.feed(htmlstr)

    return lParser.result

def RemoveSpecHtmlTag(htmlstr,removedTag):
    class TagDropper(HTMLParser.HTMLParser):
        def __init__(self, tags_to_drop):
            HTMLParser.HTMLParser.__init__(self)
            self._text = []
            self._tags_to_drop = set(tags_to_drop)
        def clear_text(self):
            self._text = []
        def get_text(self):
            return ''.join(self._text)
        def handle_starttag(self, tag, attrs):
            if tag not in self._tags_to_drop:
                self._text.append(self.get_starttag_text())
        def handle_endtag(self, tag):
            if tag not in self._tags_to_drop:
                self._text.append('</{0}>'.format(tag))
        def handle_data(self, data):
            self._text.append(data)

    lParser = TagDropper(removedTag)
    lParser.feed(htmlstr)
    return lParser.get_text()

def CutStringSafe(strIn, length):
    if length > len(strIn):
        return strIn
    else:
        result = strIn[0:length]

        for i in range(len(result) - 1, -1, -1):
            if i < len(result) - 8:
                break
            char = result[i]
            if char == '>':
                break
            if char == '<':
                result = result[0:i]
        return result

def getHtmlPics(strHtml):
    class parseLinks(HTMLParser.HTMLParser):
        def __init__(self):
            HTMLParser.HTMLParser.__init__(self)
            self.links = []

        def handle_starttag(self, tag, attrs):
            if tag == 'img':
                for name, value in attrs:
                    if name == 'src':
                        self.links.append(value)
    lParser = parseLinks()
    lParser.feed(strHtml)
    return lParser.links

def trim_string(in_str, trim_list):
    in_str = in_str.strip()
    while True:
        match = 0
        for trim_key in trim_list:
            if in_str.startswith(trim_key):
                in_str = in_str[len(trim_key):]
                match += 1
        if match == 0:
            break
    while True:
        match = 0
        for trim_key in trim_list:
            if in_str.endswith(trim_key):
                in_str = in_str[:len(in_str) - len(trim_key)]
                match += 1
        if match == 0:
            break
    return in_str

def readFile(filePath):
    data = None
    try:
        with open(filePath, 'r') as f:
            return f.read()
    except Exception as error:
        #print(error)
        pass
    return data

def ExtractData(regex, content):
    r = None
    p = re.compile(regex)
    m = p.findall(content)
    if m:
        r = m
    return r

isdebug = settings.DEBUG
def debug(*obj):
    if isdebug:
        try:
            if len(obj) == 1:
                logging.debug("{}".format(obj))
            pattern = ""
            for i in range(0, len(obj)):
                pattern += u"{} "
            logging.debug(pattern.format(*obj))
        except:
            print("debug func error, data print", obj)
