from __future__ import unicode_literals
from django.db import models
import tools.webTools as tools 
# Create your models here.

msg_box = []

class Msg(object):
    def __init__(self):
        self.guid = ""
        self.receive_id = 0
        self.send_id = 0
        self.content = ""
        self.title = ""
        self.time_stamp = None

def send_msg(rid,sid=0,title="",content=""):
    msg = Msg()
    msg.guid = tools.GetTimeCode()
    msg.receive_id = rid
    msg.send_id = sid
    msg.title = title
    msg.content = content
    msg.time_stamp = tools.get_utc_timestamp()

    global msg_box
    msg_box.append(msg)

def get_msg(rid=0):
    result = []
    if rid == 0:
        result = [x for x in msg_box]
        return result
    result = [x for x in msg_box if x.receive_id == rid]
    return result

def rm_msg(guid):
    global msg_box
    msg_box = [x for x in msg_box if x.guid != guid]

def clear():
    global msg_box
    msg_box[:] = []