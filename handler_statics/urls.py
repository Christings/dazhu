from django.conf.urls import url
from views import handler_statics

urlpatterns = [
    url(r'^(.*)$', handler_statics),
    
]