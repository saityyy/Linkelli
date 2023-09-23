import os
from pathlib import Path
import environ

env=environ.Env()
env.read_env(".env")
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

SECRET_KEY = 'django-insecure-3o%$$qsrf&g-v_5b94acw_in8jqwx!7r2d3%i&(nk7fk6=9eus'
ORIGIN_NAME="http://127.0.0.1"
ALLOWED_HOSTS = ["*"]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': env("google_client_id"),
            'secret': env("google_secret"),
            'key': ''
        }
    },
    'github': {
        'APP': {
            'client_id': env("github_dev_client_id"),
            'secret': env("github_dev_secret"),
            'key': ''
        }
    },
}
# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "linkelli",
        "USER": "linkelli",
        "PASSWORD": "linkelli",
        "HOST": "db",
        "PORT": "3306",
    }
}

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
ACCESS_CONTROL_ALLOW_ORIGIN = ["*"]
ACCESS_CONTROL_ALLOW_METHOD = ["*"]
CORS_ALLOW_HEADERS = [
    "Content-type",
    "x-csrftoken"
]
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = []
CSRF_TRUSTED_ORIGINS = [
    ORIGIN_NAME
]


