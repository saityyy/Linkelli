import os
import requests
import uuid
import hashlib
from PIL import Image
import io
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from django.http import HttpResponse
from allauth.socialaccount.models import SocialAccount
from .models import Post, Link, Keyword, UserInfo
from rest_framework import serializers
from django.contrib import auth
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    # user_info = UserInfoSerializer()

    class Meta:
        model = SocialAccount
        fields = [
            "user",
            "uid",
            "provider",
            "last_login",
            "date_joined",
            "extra_data"
        ]

    def create(self, validated_data):
        ret = super().create(validated_data)
        return ret


class UserInfoSerializer(serializers.ModelSerializer):
    user_info_id = serializers.IntegerField()
    user = UserSerializer(many=False, read_only=True)
    display_name = serializers.CharField(
        min_length=1,
        max_length=20,
        required=True,
        allow_blank=False
    )
    icon_url = serializers.CharField(required=True, allow_blank=False)

    class Meta:
        model = UserInfo
        fields = "__all__"


class LinkSerializer(serializers.ModelSerializer):
    link = serializers.CharField(required=False, allow_blank=False)
    title = serializers.CharField(required=False, allow_blank=False)
    img_url = serializers.CharField(required=False, allow_blank=False)

    class Meta:
        model = Link
        fields = (
            "link",
            "title",
            "img_url"
        )


class KeywordSerializer(serializers.ModelSerializer):
    keyword = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Keyword
        fields = [
            "keyword"
        ]


class PostSerializer(serializers.ModelSerializer):
    post_sender = UserInfoSerializer(many=False)
    links = LinkSerializer(many=True)
    keywords = KeywordSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            "post_id",
            "created",
            "post_sender",
            "links",
            "keywords",
            "comment"
        ]

    def create(self, validated_data):
        links_data = validated_data.pop("links")
        keywords_data = validated_data.pop("keywords")
        user_info_id = validated_data["post_sender"]["user_info_id"]
        validated_data["post_sender"] = UserInfo.objects.get(
            user_info_id=user_info_id)

        post_object = Post.objects.create(**validated_data)
        for link_data in links_data:
            link_data["post"] = post_object
            title, img_url = fetch_site_icon(link_data["link"])
            link_data["img_url"] = img_url
            link_data["title"] = title
            Link.objects.create(**link_data)
        for keyword_data in keywords_data:
            keyword_data["post"] = post_object
            Keyword.objects.create(**keyword_data)
        return Response({"status": "set post"})


def fetch_site_icon(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find("title").get_text()
    up = urlparse(url)
    img_url = ("http://www.google.com/s2/favicons?domain={}://{}".format(
        up.scheme, up.hostname))
    img_file_name = up.hostname + ".png"
    # img_file_name = hashlib.md5(img_file_name.encode()).hexdigest()
    if img_file_name not in os.listdir("./api/static/images/"):
        img = requests.get(img_url)
        image = Image.open(io.BytesIO(img.content))
        image.save("./api/static/images/{}".format(img_file_name))

    return title, img_url
