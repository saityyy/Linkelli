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
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '986388952862-pd9tvknj96mgsilndv962s7g7d1mkpkr.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    },
    'github': {
        'APP': {
            'client_id': 'c4ac5406b63682a2e4f4',
            'secret': '07ba56e80b61fd2d4614e4e5847dc7b9c2cb1e13',
            'key': ''
        }
    },
}
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


