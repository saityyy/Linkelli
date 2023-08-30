from django.urls import include, path
from rest_framework import routers
from . import views

app_name = "api"
router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet, basename="user")
router.register(r'post', views.PostViewSet, basename="post")


urlpatterns = [
    path("", include(router.urls)),
    path("csrf/", views.csrf, name="csrf"),
]
