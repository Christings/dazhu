from django.conf.urls import url
from blog.views import index,test,get_category,list,catelist,details,download,recover,get_content


urlpatterns = [
    url(r'^$', index.as_view()),
    url(r'test/$', test),
    url(r'^get_category$', get_category),
    url(r'^list/(\d*)$', list.as_view()),
    url(r'^catelist/(.*)$', catelist.as_view()),
    url(r'^details/(.*)$', details.as_view()),
    url(r'download/$', download),
    url(r'recover/$', recover),
    url(r'get_content/$', get_content),
]