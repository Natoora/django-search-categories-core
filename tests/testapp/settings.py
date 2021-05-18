# -*- coding: utf-8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = 'dummy'

INSTALLED_APPS = [
    'tests.testapp',
    'search_categories_core'
]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3"}}

MEDIA_ROOT = '/tmp/'

MEDIA_PATH = '/media/'

DEBUG = True

STATIC_URL = "/static/"

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
