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
from rest_framework import status
from django.conf import settings
from django.core.validators import URLValidator, RegexValidator,MinLengthValidator,MaxLengthValidator
from rest_framework.validators import UniqueValidator


class CustomListSerializer(serializers.ListSerializer):
    def validate(self,data):
        set_data=set()
        for od in data:
            if self.field_name=="links":
                set_data.add(od["link"])
            elif self.field_name=="keywords":
                set_data.add(od["keyword"])
        if len(data) != len(set_data):
            raise serializers.ValidationError(code="duplicate_value")
        return data


class UserInfoSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(
        min_length=1,
        max_length=20,
        validators=[
            UniqueValidator(queryset=UserInfo.objects.all()),
            RegexValidator(regex="^[a-zA-Z0-9_]{1,20}$")
        ],
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
    link = serializers.CharField(required=True, allow_blank=False,
                                 max_length=200,validators=[URLValidator(schemes=["https"])])
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
    keyword = serializers.CharField(max_length=30,required=True, allow_blank=False)

    class Meta:
        model = Keyword
        fields = [
            "keyword"
        ]


class PostSerializer(serializers.ModelSerializer):
    links=CustomListSerializer(
        child=LinkSerializer(),
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(5)
        ])
    keywords=CustomListSerializer(
        child=KeywordSerializer(),
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(5)
        ])

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
        post_object = Post.objects.create(**validated_data)
        for link_data in links_data:
            link_data["post"] = post_object
            title,img_url=fetch_website_info(link_data["link"])
            link_data["img_url"]=img_url
            link_data["title"] =title
            Link.objects.create(**link_data)
        for keyword_data in keywords_data:
            keyword_data["post"] = post_object
            Keyword.objects.create(**keyword_data)
        return Response({},status=status.HTTP_200_OK)


def fetch_website_info(url):
    try:
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find("title").get_text()
    except:
        title="Not Found"
    up = urlparse(url)
    img_url = ("https://www.google.com/s2/favicons?domain={}://{}".format(
        up.scheme, up.hostname))
    res=requests.get(img_url)
    if res.status_code==404:
        img_url="/app_static/images/alt_site_image.png"
    return (title,img_url)
