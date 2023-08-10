from allauth.account.forms import LoginForm
import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from allauth.socialaccount.models import SocialAccount
from .models import Post, Link
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, PostSerializer
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


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["get"])
    def get_post(self, request, pk=None):
        posts = self.get_object()
        print("GET")
        print(posts)
        return PostSerializer(request.data)

    @action(detail=True, methods=["post"])
    def set_post(self, request, pk=None):
        posts = self.get_object()
        print("POST")
        print(posts)
        return PostSerializer(request.data)
