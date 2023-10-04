import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

random.seed(42)


class SetUserInfoTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("test")
        self.user2 = User.objects.create_user("test2")
        self.url = reverse("api:user-set_user_info")
        self.client.force_authenticate(user=self.user)

    def test_success_create_user_info(self):
        icon_path = "./api/tests/icon_images/linkelli_logo.png"
        with open(icon_path, "rb")as f:
            icon_image_file = SimpleUploadedFile(
                name="test.png",
                content=f.read(),
                content_type="image/png")
        user_info_data = {
            "display_name": "test",
            "icon_image_file": icon_image_file,
            "anonymous_mode": 'false'
        }
        res = self.client.post(
            self.url, data=user_info_data, secure=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["display_name"], "test")
        self.assertEqual(res.data["anonymous_mode"], False)

    def test_success_update_user_info(self):
        icon_path = "./api/tests/icon_images/linkelli_logo.png"
        with open(icon_path, "rb")as f:
            icon_image_file = SimpleUploadedFile(
                name="test.png",
                content=f.read(),
                content_type="image/png")
        user_info_data = {
            "display_name": "test",
            "icon_image_file": icon_image_file,
            "anonymous_mode": 'false'
        }
        _ = self.client.post(
            self.url, data=user_info_data)
        update_user_info_data = {
            "display_name": "updated",
            "icon_image_file": icon_image_file,
            "anonymous_mode": 'true'
        }
        res = self.client.post(
            self.url, data=update_user_info_data)
        self.assertEqual(res.data["display_name"], "updated")
        self.assertEqual(res.data["anonymous_mode"], True)

    def test_error_authentication_failed(self):
        self.client.logout()
        icon_path = "./api/tests/icon_images/linkelli_logo.png"
        with open(icon_path, "rb")as f:
            icon_image_file = SimpleUploadedFile(
                name="test.png",
                content=f.read(),
                content_type="image/png")
        user_info_data = {
            "display_name": "test",
            "icon_image_file": icon_image_file,
            "anonymous_mode": 'false'
        }
        res = self.client.post(
            self.url, data=user_info_data, secure=True)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_error_not_exist_display_name(self):
        icon_path = "./api/tests/icon_images/linkelli_logo.png"
        with open(icon_path, "rb")as f:
            icon_image_file = SimpleUploadedFile(
                name="test.png",
                content=f.read(),
                content_type="image/png")
        user_info_data = {
            "display_name": "",
            "icon_image_file": icon_image_file,
            "anonymous_mode": 'false'
        }
        res = self.client.post(
            self.url, data=user_info_data, secure=True)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "NotExistDisplayName")

    def test_error_invalid_display_name(self):
        icon_path = "./api/tests/icon_images/linkelli_logo.png"
        with open(icon_path, "rb")as f:
            icon_image_file = SimpleUploadedFile(
                name="test.png",
                content=f.read(),
                content_type="image/png")
        user_info_data = {
            "display_name": "あえいうえおあお",
            "icon_image_file": icon_image_file,
            "anonymous_mode": 'false'
        }
        res = self.client.post(
            self.url, data=user_info_data, secure=True)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "InvalidDisplayName")

    def test_error_duplicate_display_name(self):
        icon_path = "./api/tests/icon_images/linkelli_logo.png"
        with open(icon_path, "rb")as f:
            icon_image_file = SimpleUploadedFile(
                name="test.png",
                content=f.read(),
                content_type="image/png")
        user_info_data = {
            "display_name": "test",
            "icon_image_file": icon_image_file,
            "anonymous_mode": 'false'
        }
        self.client.force_authenticate(user=self.user2)
        _ = self.client.post(
            self.url, data=user_info_data)
        self.client.logout()
        self.client.force_authenticate(user=self.user)
        res = self.client.post(
            self.url, data=user_info_data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "DuplicateDisplayName")

    def test_error_invalid_image_content_type(self):
        icon_path = "./api/tests/icon_images/linkelli_logo.png"
        with open(icon_path, "rb")as f:
            icon_image_file = SimpleUploadedFile(
                name="test.png",
                content=f.read(),
                content_type="application/json")
        user_info_data = {
            "display_name": "test",
            "icon_image_file": icon_image_file,
            "anonymous_mode": 'false'
        }
        res = self.client.post(
            self.url, data=user_info_data, secure=True)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "InvalidFileType")

    def test_error_too_big_image_size(self):
        icon_path = "./api/tests/icon_images/linkelli_logo_1536.png"
        with open(icon_path, "rb")as f:
            icon_image_file = SimpleUploadedFile(
                name="test.png",
                content=f.read(),
                content_type="image/png")
        user_info_data = {
            "display_name": "test",
            "icon_image_file": icon_image_file,
            "anonymous_mode": 'false'
        }
        res = self.client.post(
            self.url, data=user_info_data, secure=True)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data["error_code"], "TooBigImageSize")
