from django.conf.urls import url
from views import create,list,edit

urlpatterns = [
    #url(r'^$', index.as_view()),
    url(r'create/$', create),
    url(r'list/$', list),
    url(r'^edit/(.+)/$',edit),
]