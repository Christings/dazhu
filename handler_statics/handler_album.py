# coding:utf-8
from album.models import Photoes
import os
from album.get_md5_token import check_token
import logging
from dazhu.settings import ERROR_PIC


# 相册要鉴权
def handler_album(request, short_name, file_path):
    logging.debug("handler_album run")
    error_file_path = u"{}/dazhu/static/{}".format(os.getcwd(), ERROR_PIC)
    try:
        pic = Photoes.objects.get(rndName = short_name)
    except Exception as err:
        logging.error(u"handler_album {}".format(err))
        return "dazhu.jpg", error_file_path

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
                file_path = error_file_path
    return short_name, file_path
