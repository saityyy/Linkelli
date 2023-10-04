from .development import *  # noqa
from .development import DATABASES

DATABASES["default"] = {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": "test",
}
