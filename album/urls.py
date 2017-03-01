from django.conf.urls import url
from album.views import index,upload,ajaxGetAlbum,show,ajaxGetFirst6Album,recover,rolate_pic

urlpatterns = [
    url(r'^$', index.as_view()),
    url(r'^index/(\d*)$', index.as_view()),
    url(r'^upload$', upload),
    url(r'^get_post/(\d*)$', ajaxGetAlbum),
    url(r'^show/(.*)$', show.as_view()),
    url(r'^rolate/(.*)$', rolate_pic),
    url(r'^get_first6/$', ajaxGetFirst6Album),
    url(r'recover/$', recover),
]