from pathlib import Path
import environ

env = environ.Env()
env.read_env(".env")
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False


SECRET_KEY = env("DJANGO_SECRET_KEY")
ORIGIN_NAME = "https://linkelli.net"
ALLOWED_HOSTS = ["linkelli.net", "django"]

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

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "linkelli",
        "USER": "linkelli",
        "PASSWORD": env("db_password"),
        "HOST": "db",
        "PORT": "3306",
    }
}
ACCOUNT_LOGOUT_REDIRECT_URL = ORIGIN_NAME
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
ACCESS_CONTROL_ALLOW_ORIGIN = [ORIGIN_NAME]
ACCESS_CONTROL_ALLOW_METHOD = ["*"]
CSRF_TRUSTED_ORIGINS = [
    ORIGIN_NAME
]
