# coding:utf-8
from album.models import Photoes
import os
from album.get_md5_token import check_token
import logging


# 相册要鉴权
def handler_album(request, short_name, file_path):
    pic = Photoes.objects.get(rndName = short_name)
    token = ""
    is_checked = False

    if 'token' in request.GET:
        token = request.GET['token']
    
    if token:
        is_checked = check_token(short_name, token)

    logging.debug("token {}".format(token))

    if pic.phototype == "private":
        if not request.user.is_authenticated():
            if is_checked == False:
                file_path = u"{}/dazhu/static/{}".format(os.getcwd(), u'/images/dazhu.jpg')
    return file_path
