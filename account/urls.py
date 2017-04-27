from django.conf.urls import url
from account.views import UserLogin,get_user_info

urlpatterns = [
    url(r'^userlogin$', UserLogin.as_view()),
    url(r'^get_user_info$', get_user_info),
]