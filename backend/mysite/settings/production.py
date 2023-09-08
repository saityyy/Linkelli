import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False

ORIGIN_NAME="https://linkelli.net"
ALLOWED_HOSTS = ["linkelli.net","127.0.0.1","django"]

LOGIN_REDIRECT_URL = os.path.join(
    ORIGIN_NAME,
    '/user/settings?redirect=',
    ORIGIN_NAME
)
ACCOUNT_LOGOUT_REDIRECT_URL = ORIGIN_NAME
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


