from tools.secu import get_secu_key
import datetime
import logging


def get_token(short_file_name):
    source_key = u"{}{}".format(short_file_name, datetime.datetime.now().day)
    token = get_secu_key(source_key)
    logging.debug("get_token token {} {}".format(type(token), token))
    return token


def check_token(short_file_name, token):
    token_target = get_token(short_file_name)
    logging.debug(u"token_target {} token {}".format(token_target, token))
    return token == token_target