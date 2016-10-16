from django.conf.urls import url
from message.views import recover,list

urlpatterns = [
    url(r'^(\d*)$', list.as_view()),
    url(r'recover/$', recover),
    url(r'^index/(\d*)$', list.as_view()),
]