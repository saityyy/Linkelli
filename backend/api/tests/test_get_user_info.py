import random
from django.urls import reverse, include, path
from rest_framework import status
from api.views import PostViewSet
from rest_framework.test import APITestCase
from api.models import Post, UserInfo
from api import views
from django.contrib.auth.models import User
from faker import Faker
from rest_framework import status

random.seed(42)


class GetUserInfoTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user("test")
        anonymous_user = User.objects.create_user("anonymous_user")
        user_info_data = {
            "display_name": "test",
            "icon_url": "/static/images/user_icons/no_image.png",
            "user": user,
            "anonymous_mode": False
        }
        anonymous_user_info_data = {
            "display_name": "anonymous_user",
            "icon_url": "/static/images/user_icons/no_image.png",
            "user": anonymous_user,
            "anonymous_mode": True
        }
        UserInfo.objects.create(**user_info_data)
        UserInfo.objects.create(**anonymous_user_info_data)
        self.client.force_authenticate(user=user)

    def test_success_get_user_info_a(self):
        url = reverse("api:user-get_user_info",kwargs={"pk":"test"})
        res = self.client.get(
            url, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_error_authentication_failed(self):
        self.client.logout()
        url = reverse("api:user-get_user_info",kwargs={"pk":"test"})
        res = self.client.get(
            url, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_error_not_exist_user(self):
        url = reverse("api:user-get_user_info",kwargs={"pk":"not_exist_user"})
        res = self.client.get(
            url, format="json")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.data["error_code"], "UserNotExist")

    def test_error_not_show_anonymous_user(self):
        url = reverse("api:user-get_user_info",kwargs={"pk":"anonymous_user"})
        res = self.client.get(
            url, format="json")
        self.assertEqual(res.data["error_code"], "UserNotExist")