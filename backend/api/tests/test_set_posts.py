import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Post, UserInfo, Link, Keyword
from django.contrib.auth.models import User
from faker import Faker
from rest_framework import status

random.seed(42)


class SetPostsTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user("test")
        data = {
            "display_name": "test",
            "icon_url": "https://icon_url.png",
            "user":user,
            "anonymous_mode": False
        }
        _ = UserInfo.objects.create(**data)
        self.url = reverse("api:post-set_post")
        self.client.force_authenticate(user=user)

    def test_success_set_posts_a(self):
        data = {"comment": "test",
                "links": [
                    {
                        "link": "https://github.com",
                        "link": "https://qiita.com",  
                        "link": "https://zenn.dev",  
                        "link": "https://stackoverflow.com"
                    }
                ],
                "keywords": [
                    {
                        "keyword": "github"}
                ]}
        res = self.client.post(self.url,
                               data,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_error_not_exist_link(self):
        data = {"comment": "test",
                "links": [],
                "keywords": ["test"]
                }
        res = self.client.post(self.url,
                               data,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "NoLinkError")

    def test_error_not_exist_keyword(self):
        data = {"comment": "test",
                "links": ["https://github.com"],
                "keywords": []
                }
        res = self.client.post(self.url,
                               data,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "NoKeywordError")

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
                "keywords": [
                    {"keyword":"github"}
                ]
                }
        res = self.client.post(self.url,
                               data,
                               secure=True,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "BadRequestError")

    def test_error_too_many_keywords(self):
        data = {"comment": "test",
                "links": [
                    {"link":"https://github.com"}
                ],
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
        self.assertEqual(res.data["error_code"], "BadRequestError")

    def test_error_not_https_link(self):
        data = {"comment": "test",
                "links": [
                    {"link":"http://github.com"}
                ],
                "keywords": [
                    {"keyword": "github"},
                ]
                }
        res = self.client.post(self.url,
                               data,
                               secure=True,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "InvalidURL")

    def test_error_same_link_value(self):
        data = {"comment": "test",
                "links": [
                    {"link":"https://github.com"},
                    {"link":"https://github.com"}
                ],
                "keywords": [
                    {"keyword": "github"},
                ]
                }
        res = self.client.post(self.url,
                               data,
                               secure=True,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "DuplicateLinkError")

    def test_error_same_keyword_value(self):
        data = {"comment": "test",
                "links": [
                    {"link":"https://github.com"}
                ],
                "keywords": [
                    {"keyword": "github"},
                    {"keyword": "github"}
                ]
                }
        res = self.client.post(self.url,
                               data,
                               secure=True,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "DuplicateKeywordError")

    def test_error_too_long_keyword(self):
        # comment length exceeded 30
        data = {"comment":"test comment", 
                "links": [
                    {"link":"https://github.com"}
                ],
                "keywords": [
                    {"keyword": "_123456789_123456789_123456789..."}
                ]
                }
        res = self.client.post(self.url,
                               data,
                               secure=True,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"],"TooLongKeywordError")

    def test_error_too_long_comment(self):
        # comment length exceeded 120
        data = {"comment": ("123456789_123456789_123456789_123456789\
                            123456789_123456789_123456789_123456789\
                            123456789_123456789_123456789_123456789\
                            continue..."),
                "links": [
                    {"link":"https://github.com"}
                ],
                "keywords": [
                    {"keyword": "github"}
                ]
                }
        res = self.client.post(self.url,
                               data,
                               secure=True,
                               format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"],"TooLongCommentError")

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
