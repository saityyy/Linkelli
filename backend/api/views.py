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
from rest_framework.decorators import api_view
from rest_framework.decorators import action


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


class SetUserViewSet(viewsets.ModelViewSet):
    queryset = SocialAccount.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class SetUserInfoViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    # permission_classes = [permissions.IsAuthenticated]


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
        print(self.request.user.uid.all())
        q_param = self.request.query_params
        start, num = 0, 3
        if "start" in q_param:
            start = int(self.request.query_params.get("start"))
        if "num" in q_param:
            num = int(self.request.query_params.get("num"))
        sum_record = len(Post.objects.all())
        return Post.objects.all()[start:min(start + num, sum_record)]
