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
from django.core.files.storage.filesystem import FileSystemStorage
from django.core.files.uploadedfile import SimpleUploadedFile

random.seed(42)


class GetPostsTest(APITestCase):
    def setUp(self):
        user = User.objects.create_user("test")
        self.social_account = SocialAccount.objects.create(
            user=user,
            provider="google",
            uid=1
        )
        self.url = reverse("api:user-set_user_info")
        self.client.force_authenticate(user=user)

    def test_success_get_user_info_a(self):
        icon_path = "./api/static/images/user_icons/no_image.png"
        with open(icon_path, "rb")as f:
            a = SimpleUploadedFile(
                name="test.png",
                content=f.read(),
                content_type="image/png")
        user_info_data = {
            "display_name": "test",
            "icon_image_file": a,
            "anonymous_mode": False
        }
        res = self.client.post(
            self.url, data=user_info_data, secure=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
