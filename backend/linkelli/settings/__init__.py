import os ,sys

from .base import *
if os.environ["DJANGO_MODE"]=="development":
    print("development")
    from .development import *
else:
    print("production")
    from .production import *

if sys.argv[1]=="test":
    print("test")
    from .test import *