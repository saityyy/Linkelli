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
from django.contrib.auth.models import User
from .models import Post, Link, Keyword, UserInfo
from rest_framework import serializers
from django.contrib import auth
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    # user_info = UserInfoSerializer()

    class Meta:
        model = User
        fields = [
            "username"
        ]

    def create(self, validated_data):
        ret = super().create(validated_data)
        return ret


class UserInfoSerializer(serializers.ModelSerializer):
    #user_info_id = serializers.IntegerField()
    #user = UserSerializer(many=False, read_only=True)
    display_name = serializers.CharField(
        min_length=1,
        max_length=20,
        required=True,
        allow_blank=False
    )
    icon_url = serializers.CharField(required=True, allow_blank=False)
    anonymous_mode=serializers.BooleanField(required=True)

    class Meta:
        model = UserInfo
        fields =(
            "display_name",
            "icon_url",
            "anonymous_mode"
        )
    


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

    def get_post_sender(self,value):
        print("get_pose_sender")
        print(value)
        return value

    def create(self, validated_data):
        links_data = validated_data.pop("links")
        keywords_data = validated_data.pop("keywords")
        display_name = validated_data["post_sender"]["display_name"]
        validated_data["post_sender"] = UserInfo.objects.get(
            display_name=display_name)

        post_object = Post.objects.create(**validated_data)
        for link_data in links_data:
            link_data["post"] = post_object
            req_result=fetch_website_info(link_data["link"])
            print(req_result)
            if req_result=="InvalidURL":
                return Response({"error_code": "InvalidURL"},
                                status=status.HTTP_400_BAD_REQUEST)
            title,img_url=req_result
            link_data["img_url"]=img_url
            link_data["title"] =title
            print(link_data)
            Link.objects.create(**link_data)
        for keyword_data in keywords_data:
            keyword_data["post"] = post_object
            Keyword.objects.create(**keyword_data)
        return Response({"error_code":""},status=status.HTTP_200_OK)


def fetch_website_info(url):
    try:
        html = requests.get(url).content
    except:
        return "InvalidURL"
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find("title").get_text()
    up = urlparse(url)
    img_url = ("http://www.google.com/s2/favicons?domain={}://{}".format(
        up.scheme, up.hostname))
    return (title,img_url)
