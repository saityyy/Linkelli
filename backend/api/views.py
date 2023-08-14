from pprint import pprint
from allauth.account.forms import LoginForm
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from allauth.socialaccount.models import SocialAccount
from .models import Post, Link, UserInfo
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, PostSerializer, UserInfoSerializer
from django.utils import timezone
from django.middleware.csrf import get_token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist


def csrf(request):
    token = get_token(request)
    response = JsonResponse({"x-csrftoken": token})
    response.set_cookie(
        key='csrftoken',
        value=token,
        secure=True,
        samesite="None"
    )
    # response.body = {"x-csrftoken": token}
    return response


def get_user_profile(request):
    if request.user.is_authenticated:
        print(request.user)
        social_account = SocialAccount.objects.get(user=request.user)
        serializer = UserSerializer(social_account)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse(UserSerializer().data, safe=False)


# @api_view(['GET'])
# def get_post(request):
    # print(request.GET)
    # posts = Post.objects.all()
    # print(posts)
    # serializer = PostSerializer(posts)
    # return HttpResponse(serializer.data)

class SetUserInfoViewSet(viewsets.ModelViewSet):
    queryset = SocialAccount.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = SocialAccount.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', "post"]

    @action(methods=["get"], detail=True)
    def get_user_profile(self, request, pk=None):
        if request.user.is_authenticated:
            social_account = SocialAccount.objects.get(user=request.user)
            user_info = UserInfo.objects.get(user=social_account)
            result = UserInfoSerializer(user_info).data
            _ = result.pop("user")
            _ = result.pop("user_info_id")
            print(result)
            return JsonResponse(result, safe=False)
        else:
            guest_account = {
                "display_name": "Guest",
                "icon_url": None
            }
            return JsonResponse(guest_account, safe=False)

    @action(methods=["post"], detail=True,
            permission_classes=[IsAuthenticated])
    def set_user_info(self, request, pk=None):
        setting_items = {
            "display_name": "test",
            "icon_url": "https://cdn-icons-png.flaticon.com/512/61/61205.png"
        }
        user_settings = request.data
        if "display_name"not in user_settings or "icon_url"not in user_settings:
            user_settings = setting_items
        user = SocialAccount.objects.get(user=request.user)
        UserInfo.objects.update_or_create(
            user=user, defaults=user_settings)
        return Response({"status": "userinfo set"})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all()[0:1]

    @action(methods=["get"], detail=False)
    def get_post(self, request, pk=None):
        print(request.query_params)
        q = request.query_params
        start, end = int(q["start"]), int(q["start"]) + int(q["num"])
        sum_record = len(Post.objects.all())
        start = min(start, sum_record)
        end = min(end, sum_record)
        posts = Post.objects.all()[start:end]
        result = self.get_serializer(posts, many=True).data
        for i in range(len(result)):
            _ = result[i]["post_sender"].pop("user_info_id")
            _ = result[i]["post_sender"].pop("user")
        return Response(result)

    @action(methods=["post"], detail=True,
            permission_classes=[IsAuthenticated])
    def set_post(self, request, pk=None):
        post_data = request.data
        user = SocialAccount.objects.get(user=request.user)
        user_info = UserInfoSerializer(
            UserInfo.objects.get(user=user)).data
        post_data["post_sender"] = user_info
        serializer = PostSerializer(data=post_data)
        print(serializer.is_valid())
        print(serializer.errors)
        print(serializer.validated_data)
        serializer.save()
        return Response({"status": "set post data"})


class GetPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        q_param = self.request.query_params
        start, num = 0, 3
        if "start" in q_param:
            start = int(self.request.query_params.get("start"))
        if "num" in q_param:
            num = int(self.request.query_params.get("num"))
        sum_record = len(Post.objects.all())
        return Post.objects.all()[start:min(start + num, sum_record)]
