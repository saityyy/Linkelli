import os
import sys

from .base import *  # noqa

if os.environ["DJANGO_MODE"] == "development":
    print("development")
    from .development import *  # noqa
else:
    print("production")
    from .production import *  # noqa
if sys.argv[1] == "test":
    print("test")
    from .test import *  # noqa
