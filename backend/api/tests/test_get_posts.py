import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Post,Link,Keyword,UserInfo
from django.contrib.auth.models import User
from faker import Faker
from rest_framework import status

random.seed(42)


class GetPostsTest(APITestCase):
    def setUp(self):
        fake = Faker(['en_US'])
        for i in range(10):
            name = "{}_{}".format(i + 1, fake.first_name())
            user = User.objects.create_user(name)
            data = { 
                "display_name": name,
                "icon_url": "https://icon_url.png",
                "user": user,
                "anonymous_mode": [True,False][i%2]
            }
            user_info = UserInfo.objects.create(**data)
            for post_num in range(10): 
                comment = "test_comment"
                post=Post.objects.create(post_sender=user_info, comment=comment)
                for i in range(2):
                    Link.objects.create(post=post,link="https://test_{}".format(i),title="test")
                    Keyword.objects.create(post=post,keyword="test_{}".format(i))
        self.post_sum = len(Post.objects.all())
        self.url = reverse("api:post-get_post")
        self.client.force_authenticate(user=user)

    def test_success_get_post_a(self):
        res = self.client.get(
            self.url, {"start": 0, "num": 20}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 20)

    def test_success_get_post_b(self):
        res = self.client.get(
            self.url, {"start": 50, "num": 20}, format="json")
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

    def test_success_get_post_with_keyword(self):
        res = self.client.get(
            self.url, {"start": 0,
                       "num": 20,
                       "keyword":"test_0"},
            format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data),20)
    
    # check all posts. the num of anonymous and public user must be the same.
    def test_success_check_public_or_anonymous(self):
        public_count,anonymous_count=(0,0)
        for i in range(0,self.post_sum,20):
            res = self.client.get(
                self.url, {"start": i,
                        "num": 20},
                format="json")
            for r in res.data:
                if r["post_sender"]["display_name"]=="anonymous_user":
                    anonymous_count+=1
                else:
                    public_count+=1

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 20)
        self.assertEqual(public_count,anonymous_count)

    def test_success_check_post_sender_field(self):
        res = self.client.get(
            self.url, {"start": 0,
                       "num": 20},
            format="json")
        for r in res.data:
            self.assertIs(type(r["post_sender"]["anonymous_mode"]),bool)
            if r["post_sender"]["anonymous_mode"]:
                self.assertEqual(r["post_sender"]["display_name"], "anonymous_user")


        self.assertEqual(res.status_code, status.HTTP_200_OK)


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
        self.assertEqual(res.data["error_code"], "TooManyRequestPost")

    # case input string query or invalid number format
    def test_error_bad_query_a(self):
        res = self.client.get(
            self.url, {"start": "hello",
                       "num": "world"},
            format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "BadQueryRequest")

    # case input minus number
    def test_error_bad_query_b(self):
        res = self.client.get(
            self.url, {"start": -1,
                       "num": 20},
            format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "BadQueryRequest")

    # case no input query parameter
    def test_error_bad_query_c(self):
        res = self.client.get(
            self.url, {},
            format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "BadQueryRequest")
