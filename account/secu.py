import tools.webTools as tools
from django.http import Http404,HttpResponseForbidden
from django.http import HttpResponseRedirect
import urllib
import time

def login_filter(func):
    def returned_wrapper(request, *args, **kwargs):
        try:
            if request.user.is_authenticated():
                tools.debug("user is ",request.user.id)
                return func(request, *args, **kwargs)
            return HttpResponseForbidden()
        except Exception as error:
            tools.debug("login failed",request,error)
            raise Http404
    return returned_wrapper

def user_login(func):
    def returned_wrapper(request, *args, **kwargs):
        try:
            if is_user_login_timeout(request) == False:
                return func(request, *args, **kwargs)
            return HttpResponseRedirect('/account/userlogin?url=' + urllib.quote(request.get_full_path()) )
        except Exception as error:
            tools.debug("user_login check failed",request,error)
            raise Http404
    return returned_wrapper

def set_user_login(request):
    request.session['user_login'] = int(time.time())


def is_user_login_timeout(request):
    if "user_login" in request.session:
        saved_time = int(request.session['user_login'])
        now = time.time()
        delta = now - saved_time
        mins = delta / 60.0
        if mins > 20 :
            return True
        else:
            return False
    return True