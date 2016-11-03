from django.conf.urls import url
from views import index,download_file,del_file


urlpatterns = [
    url(r'^$', index.as_view()),
    url(r'post$', download_file),
    url(r'delete/$', del_file),
]