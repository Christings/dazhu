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
def removeHtml(value,length):
    value = value.replace("<br/>","#br/#")\
    .replace("\r\n","\n")\
    .replace("\n","#br/#")\
    .replace("</p>","#br/#")\
    .replace("&nbsp;",'#nbsp;')
    value = tools.webTools.RemoveHttpStr(value)
    value = tools.webTools.CutStringSafe(value,int(length))
    value = value.replace("#br/#","<br/>").replace("#nbsp;","&nbsp;")
    while True:
        if '<br/><br/>' in value:
            value = value.replace('<br/><br/>','<br/>')
        else:
            break
    return value

@register.filter 
def quote(value):
    try:            
        return urllib.quote(value.encode('utf-8'))
    except:
        tools.webTools.debug("quote fail",value)
        return ""

@register.filter 
def cutSafe(value, length):
    data = tools.webTools.CutStringSafe(value, int(length))
    # tools.webTools.debug("cutSafe", data)
    return data

@register.filter 
def removeTags(value, tags):
    tags = tags.split(",")
    data = tools.webTools.RemoveSpecHtmlTag(value, tags)
    # tools.webTools.debug("cutSafe", data)
    return data

@register.filter 
def getPic(value):
    picList = tools.webTools.getHtmlPics(value)
    if len(picList) == 0:
        return "/static/images/img1.jpg"
    else:
        for item in picList:
            if "/fileTypeImages/" not in item:
                return item            
        return "/static/images/img1.jpg"
    
    
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
