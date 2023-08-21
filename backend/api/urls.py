from django.urls import include, path
from rest_framework import routers
from . import views

app_name = "api"
router = routers.DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'post', views.PostViewSet)
router.register(r'get_post', views.GetPostViewSet)
router.register(r'get_user_post', views.GetPostViewSet)
router.register(r'set_post', views.PostViewSet)


urlpatterns = [
    path("v1/", include(router.urls)),
    path("csrf/", views.csrf, name="csrf"),
]
