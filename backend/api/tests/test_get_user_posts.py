import random
from django.urls import reverse, include, path
from rest_framework import status
from api.views import PostViewSet
from rest_framework.test import APITestCase
from api.models import Post, UserInfo, Link,Keyword
from django.contrib.auth.models import User
from faker import Faker
from rest_framework import status

random.seed(42)


class GetUserPostsTest(APITestCase):
    def setUp(self):
        for i in range(10):
            if i==0:
                name="anonymous_user"
                anonymousFlag=True
                user = User.objects.create_user(name)
            elif i==1:
                name="public_user"
                anonymousFlag=False
                user = User.objects.create_user(name)
                self.user=user
            else:
                name = "{}_{}".format("user",i)
                anonymousFlag=False
                user = User.objects.create_user("{}_{}".format("user",i-1))
            data = { 
                "display_name": name,
                "icon_url": "https://icon_url.png",
                "user": user,
                "anonymous_mode": anonymousFlag
            }
            user_info = UserInfo.objects.create(**data)
            for _ in range(random.randint(50, 100)): 
                comment = "test_comment"
                post=Post.objects.create(post_sender=user_info, comment=comment)
                for i in range(2):
                    Link.objects.create(post=post,link="https://test_{}".format(i),title="test")
                    Keyword.objects.create(post=post,keyword="test_{}".format(i))
        self.user_info=UserInfo.objects.get(display_name="public_user")
        self.url = reverse("api:post-get_user_post", kwargs={"pk":"public_user"})
        self.post_sum = len(Post.objects.all().filter(post_sender=self.user_info))
        self.client.force_authenticate(user=self.user)

    def test_success_get_post_a(self):
        res = self.client.get(
            self.url, {"start": 0, "num": 20}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 20)

    def test_success_get_post_b(self):
        res = self.client.get(
            self.url, {"start": 20, "num": 20}, format="json")
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


    def test_error_authentication_failed(self):
        self.client.logout()
        res = self.client.get(
            self.url, {"start": 0, "num": 20}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

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

    # case fetch not exist user's posts 
    def test_error_not_show_anonymous_user(self):
        url = reverse("api:post-get_user_post", kwargs={"pk":"not_exist_user"})
        res = self.client.get(
            url, {"start":0,"num":20},
            format="json")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.data["error_code"], "UserNotExist")

    # case fetch anonymous_user's posts 
    def test_error_not_show_anonymous_user(self):
        url = reverse("api:post-get_user_post", kwargs={"pk":"anonymous_user"})
        res = self.client.get(
            url, {"start":0,"num":20},
            format="json")
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.data["error_code"], "UserNotExist")