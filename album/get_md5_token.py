from tools.secu import get_secu_key
import datetime
import logging


def get_token(short_file_name):
    source_key = "{}{}".format(short_file_name, datetime.datetime.day)
    token = get_secu_key(source_key)
    return token


def check_token(short_file_name, token):
    token_target = get_token(short_file_name)
    logging.debug("token_target {} token {}".format(token_target, token))
    return token == token_target