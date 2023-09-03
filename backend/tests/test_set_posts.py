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

    def test_error_too_many_links(self):
        data = {"comment": "test",
                "links": [
                    {"link": "https://github.com"},
                    {"link": "https://github.com"},
                    {"link": "https://github.com"},
                    {"link": "https://github.com"},
                    {"link": "https://github.com"},
                    {"link": "https://github.com"},
                ],
                "keywords": []
                }
        res = self.client.post(self.url,
                               data,
                               secure=True,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "TooManyLinksError")

    def test_error_too_many_keywords(self):
        data = {"comment": "test",
                "links": [],
                "keywords": [
                    {"keyword": "github"},
                    {"keyword": "github"},
                    {"keyword": "github"},
                    {"keyword": "github"},
                    {"keyword": "github"},
                    {"keyword": "github"},
                ]
                }
        res = self.client.post(self.url,
                               data,
                               secure=True,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "TooManyKeywordsError")

    def test_error_too_long_comment(self):
        # comment length <=120
        data = {"comment": ("123456789_123456789_123456789_123456789\
                            123456789_123456789_123456789_123456789\
                            123456789_123456789_123456789_123456789\
                            abcde"),
                "links": [],
                "keywords": []
                }
        res = self.client.post(self.url,
                               data,
                               secure=True,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_error_authentication_failed(self):
        self.client.logout()
        data = {"comment": "test",
                "links": [],
                "keywords": []
                }
        res = self.client.post(self.url,
                               data,
                               secure=True,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
