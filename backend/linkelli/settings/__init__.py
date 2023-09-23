import os 

from .base import *
if os.environ["DJANGO_MODE"]=="development":
    print("development")
    from .development import *
else:
    print("production")
    from .production import *