# coding:utf-8
'''
Created on Mar 21, 2016

@author: yzh
'''
from django.http import HttpResponse


def get_404(request):
    return HttpResponse(request.get_full_path() + u"神马也没找到")