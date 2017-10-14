# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
import logging
import os
from album.models import Photoes
from django.views.decorators.http import condition, last_modified
import time
import datetime


def get_real_path(request, path):
    real_file_path = u"{}/dazhu/static/{}".format(os.getcwd(), path)
    if real_file_path.endswith("/"):
        real_file_path = real_file_path[:-1]

    short_file_name = real_file_path.split("/")
    short_file_name = short_file_name[len(short_file_name)-1]

    # 对 album 要鉴权
    if "album/" in path:
        real_file_path = handler_album(request, short_file_name, real_file_path)
    return short_file_name, real_file_path


def get_file_create_time(request, path):
    try:
        _, real_file_path = get_real_path(request, path)
        mtime = time.ctime(os.path.getmtime(real_file_path))
        logging.info("last modified: {}".format(mtime))
        return datetime.datetime.strptime(mtime, "%a %b %d %H:%M:%S %Y")
    except:
        return datetime.datetime.now()


@last_modified(get_file_create_time)
def handler_statics(request, path):
    short_file_name, real_file_path = get_real_path(request, path)
    
    response = StreamingHttpResponse(readFile(real_file_path))
    response['Content-Type'] = get_right_content_type(short_file_name)
    response['Content-Disposition'] = get_right_content_disposition(short_file_name)

    logging.info(u"handler_statics type {} path {}".format(get_right_content_type(short_file_name)
                                                           , real_file_path))
    return response


# 相册要鉴权
def handler_album(request, short_name, file_path):
    pic = Photoes.objects.get(rndName = short_name)
    if pic.phototype == "private":
        if not request.user.is_authenticated():
            file_path = u"{}/dazhu/static/{}".format(os.getcwd(), u'/images/dazhu.jpg')
    return file_path


def get_right_content_disposition(filename):
    filename = filename.lower()
    img_types = ['jpg', 'png', 'jpeg', 'gif']
    content_disposition = ""
    for img_type in img_types:
        if img_type in filename:
            content_disposition = u'inline;filename="{}"'.format(filename)
            break
    if content_disposition == "":
        content_disposition = u'attachment;filename="{}"'.format(filename)
    return content_disposition


def get_right_content_type(filename):
    filename = filename.lower()
    if ".css" in filename:
        return "text/css"
    if ".png" in filename:
        return "image/png"
    if '.jpg' in filename or '.jpeg' in filename:
        return "image/jpeg"
    else:
        return "application/octet-stream"

def readFile(file_name, chunk_size=512):
    try:
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    except:
        yield b""
