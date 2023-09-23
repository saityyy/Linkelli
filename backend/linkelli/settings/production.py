import os
from pathlib import Path
import environ

env=environ.Env()
env.read_env(".env")
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False

ORIGIN_NAME="https://linkelli.net"
ALLOWED_HOSTS = ["linkelli.net","django"]

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
            'client_id': env("github_prod_client_id"),
            'secret': env("github_prod_secret"),
            'key': ''
        }
    },
}
ACCOUNT_LOGOUT_REDIRECT_URL = ORIGIN_NAME
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE=True
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


