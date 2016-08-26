from django.conf.urls import url
from views import chat_room


urlpatterns = [
    url(r'^$', chat_room),
]