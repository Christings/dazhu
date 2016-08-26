# coding: utf-8
'''
Created on Mar 21, 2016

@author: yzh
'''

import tools 
from django import template 
register = template.Library() 
import urllib
@register.filter 
def removeHtml(value):
    return tools.webTools.RemoveHttpStr(value)

@register.filter 
def quote(value):
    try:            
        return urllib.quote(value.encode('utf-8'))
    except:
        tools.webTools.debug("quote fail",value)
        return ""

@register.filter 
def cutSafe(value, length):
    return tools.webTools.CutStringSafe(value, int(length))

@register.filter 
def getPic(value):
    picList = tools.webTools.getHtmlPics(value)
    if len(picList) == 0:
        return "/static/images/img1.jpg"
    else:
        if "/fileTypeImages/" in picList[0]:
            return "/static/images/img1.jpg"
        return picList[0]
    
    
class GetUserNode(template.Node):  
    def __init__(self):  
        pass  
  
    def render(self, context):  
        try:            
            user = context['user']               
            tools.webTools.debug("user is ",user.get_full_name())  
            return user.get_full_name()
        except Exception as error:   
            tools.webTools.debug("error is ")
            tools.webTools.debug(error)
            return u""
  
def GetUser(parser, token):  
    return GetUserNode()  
  
register.tag('get_user', GetUser)  

class GetTitleNode(template.Node):  
    def __init__(self):  
        pass  
  
    def render(self, context):  
        try:     
            title = context['title']             
            return title
        except Exception as error:   
            tools.webTools.debug("error is ",error)
            return u""
  
def GetTitle(parser, token):  
    return GetTitleNode()  
  
register.tag('get_title', GetTitle)

import datetime
def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

register.simple_tag(get_time)