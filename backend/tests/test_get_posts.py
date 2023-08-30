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
        fake = Faker(['en_US', 'ja_JP'])
        for i in range(100):
            name = "{}_{}".format(i + 1, fake.name())
            user = User.objects.create_user(name)
            social_account = SocialAccount.objects.create(
                user=user,
                provider="google",
                uid=i
            )
            data = {
                "display_name": name,
                "icon_url": "test",
                "user": social_account,
                "anonymous_mode": False
            }
            user_info = UserInfo.objects.create(**data)
            for post_num in range(random.randint(5, 20)):
                comment = "test"
                Post.objects.create(post_sender=user_info, comment=comment)
        self.post_sum = len(Post.objects.all())
        self.url = reverse("api:post-get_post")

    def test_success_get_post_a(self):
        res = self.client.get(
            self.url, {"start": 0, "num": 20}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 20)

    def test_success_get_post_b(self):
        res = self.client.get(
            self.url, {"start": 100, "num": 20}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 20)

    def test_success_get_post_c(self):
        res = self.client.get(
            self.url, {"start": self.post_sum - 10,
                       "num": 20},
            format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 10)

    def test_success_get_post_d(self):
        res = self.client.get(
            self.url, {"start": self.post_sum + 10,
                       "num": 20},
            format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, [])

    # case too many fetch posts(no exceed 30 posts)
    def test_error_too_fetch(self):
        res = self.client.get(
            self.url, {"start": self.post_sum + 10,
                       "num": 30},
            format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "TooManyRequestPostError")

    # case input string query or invalid number format
    def test_error_bad_query_a(self):
        res = self.client.get(
            self.url, {"start": "hello",
                       "num": "world"},
            format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "BadQueryRequestError")

    # case input minus number
    def test_error_bad_query_b(self):
        res = self.client.get(
            self.url, {"start": -1,
                       "num": 20},
            format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "BadQueryRequestError")

    # case no input query parameter
    def test_error_bad_query_c(self):
        res = self.client.get(
            self.url, {},
            format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "BadQueryRequestError")
