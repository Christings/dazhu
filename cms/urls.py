from django.conf.urls import url
from views import controller

urlpatterns = [
    url(r'^$', controller),
   
]