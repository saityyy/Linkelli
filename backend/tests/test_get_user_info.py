import random
from django.urls import reverse, include, path
from rest_framework import status
from api.views import PostViewSet
from rest_framework.test import APITestCase
from api.models import Post, UserInfo, SocialAccount
from api import views
from django.contrib.auth.models import User
from faker import Faker
from rest_framework import status

random.seed(42)


class GetPostsTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user("test")
        # token = Token.objects.get(user__username="test")
        self.social_account = SocialAccount.objects.create(
            user=user,
            provider="google",
            uid=1
        )
        user_info_data = {
            "display_name": "test",
            "icon_url": "/static/images/user_icons/no_image.png",
            "user": self.social_account,
            "anonymous_mode": False
        }
        UserInfo.objects.create(**user_info_data)
        self.url = reverse("api:user-get_user_info")
        self.client.force_authenticate(user=user)

    def test_success_get_user_info_a(self):
        res = self.client.get(
            self.url, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
