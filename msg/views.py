from django.shortcuts import render
from msg.models import get_msg as db_get_msg
from msg.models import clear as db_clear
from django.http import HttpResponse
import json as simplejson
import logging
from django.shortcuts import redirect
# Create your views here.
# ajax get msg
def get_msg(request):
    is_login = request.user.is_authenticated()
    if is_login:
        result = db_get_msg()
        logging.debug("get msg result {}".format(result))
        json_result = []
        for msg in result:
            json_result.append(msg.__dict__)
        return HttpResponse(simplejson.dumps(json_result, ensure_ascii=False))
    else:
        return HttpResponse()

def index(request):
    is_login = request.user.is_authenticated()
    if is_login:
        result = db_get_msg()
        logging.debug("get msg result {}".format(result))
        return render(request, "msg/index.html", {'msgs':result})
    else:
        return HttpResponse()

def clear(request):
    is_login = request.user.is_authenticated()
    if is_login:
        db_clear()
        return redirect("/msg/")
    else:
        return HttpResponse()