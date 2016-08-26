from django.conf.urls import url
from views import result

urlpatterns = [
    url(r'', result.as_view()),
]