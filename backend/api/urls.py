from django.urls import include, path
from rest_framework import routers
from . import views

app_name = "api"
router = routers.DefaultRouter()
router.register(r'set_user', views.SetUserViewSet)
router.register(r'get_post', views.PostViewSet)


urlpatterns = [
    path("v1/", include(router.urls)),
    path(
        "auth/get_user_profile/",
        views.get_user_profile,
        name="get_user_profile"),
    # path("get_post/", views.get_post, name="get_post"),
    path("csrf/", views.csrf, name="csrf"),
]
