from django.conf.urls import url
from ueditor.views import controller


urlpatterns = [
    url(r'^controller$', controller),
]