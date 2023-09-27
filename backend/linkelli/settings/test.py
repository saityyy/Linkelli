from .base import *
from .development import *

DATABASES["default"]={
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": "test",
}