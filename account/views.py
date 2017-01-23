#coding:utf-8
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from tools.secu import xssFilter,xss_white_list
from account.secu import set_user_login
import tools.webTools as tools
from django.shortcuts import redirect
import urllib
from django.contrib.auth import authenticate

class UserLogin(TemplateView):

    template_name = "account/userlogin.html"
    def get_context_data(self, **kwargs):
        context = super(UserLogin, self).get_context_data(**kwargs)

        context['title'] = "用户验证"

        return context

    @method_decorator(csrf_protect)
    def post(self, request):
        url = urllib.unquote(request.GET["url"])
        if url != "":
            if request.user.check_password(request.POST['pwd']):
            	set_user_login(request)
	        tools.debug("pwd is error",request.POST['pwd'])
            return redirect(url)
        return redirect("/")