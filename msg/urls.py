from django.conf.urls import url
from msg.views import get_msg, index, clear


urlpatterns = [
    url(r'^$', index),
    url(r'^admin/', get_msg),
    url(r'^clear/', clear),
]