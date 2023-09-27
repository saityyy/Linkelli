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


class GetMyUserInfoTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user("test")
        self.user2 = User.objects.create_user("test2")
        user_info_data = {
            "display_name": "test",
            "icon_url": "/static/images/user_icons/anonymous/icon.png",
            "user": user,
            "anonymous_mode": False
        }
        UserInfo.objects.create(**user_info_data)
        self.url = reverse("api:user-get_my_info")
        self.client.force_authenticate(user=user)

    def test_success_get_my_info_a(self):
        res = self.client.get(
            self.url, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_error_authentication_failed(self):
        self.client.logout()
        res = self.client.get(
            self.url, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_error_not_exist_my_info(self):
        self.client.logout()
        self.client.force_authenticate(user=self.user2)
        res = self.client.get(
            self.url, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["exist_user_info"], False)
