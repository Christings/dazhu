from django.conf.urls import url
from account.views import UserLogin

urlpatterns = [
    url(r'^userlogin$', UserLogin.as_view()),
]