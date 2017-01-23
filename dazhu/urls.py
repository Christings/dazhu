from django.conf.urls import  include, url
from django.contrib import admin
from views import get_404
admin.autodiscover()

handler404 = 'dazhu.views.get_404'

urlpatterns = [
    url(r'^$', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blog.urls')),
    url(r'^ueditor/', include('ueditor.urls')),
   # url(r'^chat/', include('chat.urls')),
    url(r'^album/', include('album.urls')),
    url(r'^diary/', include('diary.urls')),
    url(r'^search', include('search.urls')),
    url(r'^message/', include('message.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^memo/', include('memo.urls')),
    url(r'^pan/', include('pan.urls')),
    url(r'^(.*)/(.*)/', include('cms.urls')),

]
