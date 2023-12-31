import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import UserInfo
from django.contrib.auth.models import User

random.seed(42)


class GetMyUserInfoTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user("test")  # userinfo作成済み
        self.user2 = User.objects.create_user("test2")  # userinfo未作成
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
        self.assertEqual(res.data["no_settings"], False)

    def test_success_new_create_my_info(self):
        self.client.logout()
        self.client.force_authenticate(user=self.user2)
        res = self.client.get(
            self.url, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["no_settings"], True)

    def test_error_authentication_failed(self):
        self.client.logout()
        res = self.client.get(
            self.url, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
