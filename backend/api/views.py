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
            serializer = UserInfoSerializer(user_info)
            print(serializer.data)
            return JsonResponse(serializer.data, safe=False)
        else:
            guest_account = UserSerializer().data
            guest_account["extra_data"] = '{}'
            print(guest_account)
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
        UserInfo.objects.update_or_create(user=user, defaults=user_settings)
        return Response({"status": "userinfo set"})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all()[0:1]


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
