#coding:utf-8
from django.shortcuts import render
# Create your views here.

from django.core.cache import cache
import tools.webTools as tools
from django.http import Http404,HttpResponseForbidden
import models

def ip_filter(func):
    def returned_wrapper(request, *args, **kwargs):
        try:
            if is_black_ip(get_ip(request)) == False:
                return func(request, *args, **kwargs)
            resp =  HttpResponseForbidden()
            resp.write("你的IP被封禁")
            return resp
        except Exception as error:
            tools.debug("ip filter failed",request,error)
            raise Http404
    return returned_wrapper

def is_black_ip(input_ip):
    tools.debug("is_black_ip input ip:",input_ip)
    black_list = cache.get('black_ip_list')
    if black_list == None:
        db_ip_list = models.IP.objects.all()
        cache.set('black_ip_list', db_ip_list, 60)
        black_list = db_ip_list
    for item in black_list:
        if input_ip.startswith(item.body):
            return True
    return False

def get_ip(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip

