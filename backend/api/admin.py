from django.contrib import admin
from .models import Post, Link, Keyword, UserInfo

admin.site.register(Post)
admin.site.register(Link)
admin.site.register(Keyword)
admin.site.register(UserInfo)
