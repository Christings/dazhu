from django.conf.urls import url
from views import index,ajaxDiary,edit,recover,download

urlpatterns = [
    url(r'^$', index.as_view()),
    url(r'^edit/(\d*)', edit.as_view()),
    url(r'^edit/(\d*)/', edit.as_view()),
    url(r'^get_post/(\d*)$', ajaxDiary),
    url(r'recover/$', recover),
    url(r'download/$', download),
]