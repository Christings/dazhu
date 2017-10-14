"""
Django settings for dazhu project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import logging
import logging.handlers

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

fmt = '%(asctime)s %(levelname)s %(message)s'
datefmt='%Y-%m-%d %H:%M:%S'
logger = logging.getLogger()
# file_handler = logging.handlers.TimedRotatingFileHandler(
#             filename = BASE_DIR+'/logs/dazhu.log',
#             when = "midnight",
#             backupCount = 5)
# file_handler.setFormatter(logging.Formatter(fmt, datefmt))
# logger.addHandler(file_handler)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(fmt, datefmt))
logger.addHandler(handler)
logger.setLevel('DEBUG')

APPEND_SLASH = True
DOMAIN_STR = "www.superpig.win"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w&p^!3h-q2u37#6n@827329poo_z=0gddmqolomyu71hal_$l*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

LOGGING_CONFIG = None

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'django.contrib.staticfiles',
    'blog',
    'templateUtils',
   # "channels",
   # "chat",
    'ueditor',
    'album',
    'account',
    'diary',
    'cms',
    'dazhu',
    'search',
    'message',
    "ip_filter",
    "memo",
    'msg',
    'handler_statics'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
)

ROOT_URLCONF = 'dazhu.urls'

WSGI_APPLICATION = 'dazhu.wsgi.application'

# SESSION_COOKIE_AGE = 60*30
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
        },
        "ROUTING": "chat.routing.channel_routing",
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_USER_MODEL = 'account.Account'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = "/dazhu/dazhu/static/"

STATICFILES_FINDERS = (
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
'django.contrib.staticfiles.finders.FileSystemFinder',
)
