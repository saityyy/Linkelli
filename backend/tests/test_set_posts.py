import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Post, UserInfo, SocialAccount, Link, Keyword
from django.contrib.auth.models import User
from faker import Faker
from rest_framework import status

random.seed(42)


class SetPostsTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user("test")
        # token = Token.objects.get(user__username="test")
        print(self.client.credentials())
        self.social_account = SocialAccount.objects.create(
            user=user,
            provider="google",
            uid=1
        )
        data = {
            "display_name": "test",
            "icon_url": "test",
            "user": self.social_account,
            "anonymous_mode": False
        }
        user_info = UserInfo.objects.create(**data)
        self.url = reverse("api:post-set_post")
        self.client.force_authenticate(user=user)

    def test_success_set_posts_a(self):
        data = {"comment": "test",
                "links": [
                    {"link": "https://github.com"}
                ],
                "keywords": [
                    {"keyword": "github"}
                ]}
        res = self.client.post(self.url,
                               data,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_success_set_posts_b(self):
        data = {"comment": "test",
                "links": [],
                "keywords": []
                }
        res = self.client.post(self.url,
                               data,
                               secure=True,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
