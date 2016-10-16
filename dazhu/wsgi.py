"""
WSGI config for dazhu project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
from os.path import join,dirname,abspath


PROJECT_DIR = dirname(dirname(abspath(__file__)))#3
import sys # 4
sys.path.insert(0,PROJECT_DIR) # 5

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dazhu.settings")

# from channels.asgi import get_channel_layer
# channel_layer = get_channel_layer()
# from asgiref.wsgi import WsgiToAsgiAdapter
# application = WsgiToAsgiAdapter(channel_layer)


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
