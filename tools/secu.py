#coding:utf-8
import tools.webTools as tools
from django.http import Http404
import re
from dazhu.settings import DOMAIN_STR
from dazhu.settings import SECRET_KEY
import hashlib


def get_str_md5(input_str):
    md5obj = hashlib.md5()
    md5obj.update(input_str)
    return md5obj.hexdigest()


def decodeHtml(input):
    s = input
    s = s.replace("&gt;",">")
    s = s.replace("&lt;","<")
    #s = s.replace("&amp;","&")
    return s

def encodeHtml(input):
    s = input
    #s = s.replace("&", "&amp;")  # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    return s

def xssFilter(func):
    def returned_wrapper(request, *args, **kwargs):
        try:
            for key in request.POST:
                mutable = request.POST._mutable
                tools.debug("xssFilter",request,request.POST[key])
                request.POST._mutable = True
                request.POST[key] = encodeHtml(request.POST[key])               
                request.POST._mutable = mutable
            tools.debug("xssFilter over")
            return func(request, *args, **kwargs)
        except Exception as error:
            tools.debug("xssFilter failed",request,error)
            raise Http404
    return returned_wrapper

def xss_white_list(input):
    s = encodeHtml(input)
    #p相关
    pattern1 ="(&lt;p&gt;|" +\
    "&lt;/p&gt;|"+\
    '&lt;p style="([\s\S](?!&lt;))*"&gt;)'
    pattern2 ='(&lt;img src="http://' + DOMAIN_STR + '/.*"/&gt;' +\
    '|&lt;img src="http://img.baidu.com/(.(?!&lt;))*"/&gt;)'
    #a
    pattern3 = '(&lt;a href="http://' + DOMAIN_STR + '/(.(?!&lt;))*"&gt;(.(?!&lt;))*&lt;/a&gt;)'
    #br strong
    pattern4 = "(&lt;br/&gt;|"+\
               "&lt;strong&gt;|&lt;/strong&gt;)"
    #span
    pattern5 ='(&lt;span style="([\s\S](?!&lt;))*"&gt;' +\
    '|&lt;/span&gt;)'

    pat_list = [pattern1,pattern2,pattern3,pattern4,pattern5]

    for item in pat_list:
        pattern = re.compile(item)
        arry = pattern.findall(s)
        for safe_str in arry:
            if isinstance(safe_str,basestring):
                s = s.replace(safe_str, decodeHtml(safe_str));
            elif safe_str[0] !="":
                s = s.replace(safe_str[0],decodeHtml(safe_str[0]));

    return s


def get_secu_key(input_str):
    return get_str_md5(SECRET_KEY + input_str)


def check_secu_key(input_str, md5_str):
    return get_str_md5(SECRET_KEY + input_str) == md5_str