import re
import uuid
import glob
from allauth.account.forms import LoginForm
import os
import uuid
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from allauth.socialaccount.models import SocialAccount
from .models import Post, Keyword, UserInfo
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, PostSerializer, UserInfoSerializer
from django.utils import timezone
from django.shortcuts import redirect
from django.middleware.csrf import get_token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import FileSystemStorage
from django.db import DatabaseError
from django.contrib.auth.models import User

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

def get_user_info(request):
    if request.user.is_authenticated:
        print(request.user)
        social_account = SocialAccount.objects.get(user=request.user)
        serializer = UserSerializer(social_account)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse(UserSerializer().data, safe=False)


class SetUserInfoViewSet(viewsets.ModelViewSet):
    queryset = SocialAccount.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]


@parser_classes([MultiPartParser, FormParser])
class UserViewSet(viewsets.ModelViewSet):
    queryset = SocialAccount.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    ttp_method_names = ['get', "post"]

    @action(methods=["get"], detail=False,
            url_path="get_user_info", url_name="get_user_info")
    def get_user_info(self, request, pk=None):
        if request.user.is_authenticated:
            user_id=uuid.uuid3(uuid.NAMESPACE_X500,
                               request.user.username).hex
            user = User.objects.get(username=request.user.username)
            try:
                user_info = UserInfo.objects.get(user=user)
            except ObjectDoesNotExist:
                return JsonResponse(
                    {"exist_user_info": False,
                     "display_name": user_id[:10],
                     "icon_url": os.path.join(
                         settings.ORIGIN_NAME,
                        "/app_static/images/user_icons/anonymous/icon.png"
                     )
                     }, status=status.HTTP_200_OK)
            result = UserInfoSerializer(user_info).data
            result["exist_user_info"] = True
            return JsonResponse(result, safe=False, status=status.HTTP_200_OK)
        else:
            guest_account = {
                "display_name": "Guest",
                "icon_url": None
            }
            return JsonResponse(guest_account, safe=False)

    @action(methods=["post"], detail=False,
            permission_classes=[IsAuthenticated],
            url_path="set_user_info", url_name="set_user_info")
    def set_user_info(self, request, pk=None):
        setting_items = {}
        user_hash_id=uuid.uuid3(uuid.NAMESPACE_X500,
                            request.user.username).hex
        user = User.objects.get(username=request.user.username)
        if "display_name" not in request.data:
            return Response({"error_code": "FieldNotExist"},
                            status=status.HTTP_400_BAD_REQUEST)
        if "icon_image_file" not in request.data:
            return Response({"error_code": "FieldNotExist"},
                            status=status.HTTP_400_BAD_REQUEST)
        img = request.data["icon_image_file"]
        if not hasattr(img, "content_type"):
            return Response({"error_code": "InvalidFileData"},
                            status=status.HTTP_400_BAD_REQUEST)
        if not (img.content_type in ["image/png", "image/jpeg", "image/gif"]):
            return Response({"error_code": "InvalidImageType"},
                            status=status.HTTP_400_BAD_REQUEST)
        if re.search("^[a-zA-Z0-9_]{1,20}$",
                     request.data["display_name"]) is None:
            return Response({"error_code": "InvalidDisplayName"},
                            status=status.HTTP_400_BAD_REQUEST)

        icon_path=os.path.join(settings.STATIC_ROOT, "./images/user_icons/")
        if os.environ["DJANGO_DEVELOPMENT"]:
            icon_path = "./api/static/images/user_icons/"
        ext = img.name.split(".")[-1].lower()
        user_icon_dir=os.path.join(icon_path,user_hash_id)
        filename = "{}.{}".format("icon",ext)
        if not os.path.exists(user_icon_dir):
            os.mkdir(user_icon_dir)
            FileSystemStorage(
                location=user_icon_dir).save(filename, img)
        else:
            os.remove(os.path.join(user_icon_dir,os.listdir(user_icon_dir)[0]))
            FileSystemStorage(
                location=user_icon_dir).save(filename, img)
        setting_items["display_name"] = request.data["display_name"]
        if request.data["anonymous_mode"] == 'true':
            setting_items["anonymous_mode"] = True
        else:
            setting_items["anonymous_mode"] = False
        setting_items["icon_url"] = os.path.join(
            settings.ORIGIN_NAME,
            "/app_static/images/user_icons/",
            user_hash_id,
              filename)
        try:
            UserInfo.objects.update_or_create(
                user=user, defaults=setting_items)
        except DatabaseError as e:
            err_code,_=e.args
            if err_code==1062:
                return Response({"error_code": "DuplicateDisplayName"},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "userinfo set"})

def is_error_get_post(q):
    if (q.get("start") is None) or (q.get("num") is None):
        return Response({"error_code": "BadQueryRequestError"},
                        status=status.HTTP_400_BAD_REQUEST)
    if not q["start"].isdecimal() or not q["num"].isdecimal():
        return Response({"error_code": "BadQueryRequestError"},
                        status=status.HTTP_400_BAD_REQUEST)
    start, num = (int(q["start"]), int(q["num"]))
    end = start + num
    if start < 0 or num < 0:
        return Response({"error_code": "BadQueryRequestError"},
                        status=status.HTTP_400_BAD_REQUEST)
    if num >= 30:
        return Response({"error_code": "TooManyRequestPostError"},
                        status=status.HTTP_400_BAD_REQUEST)
    return (start,end)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all()[0:1]

    @action(methods=["get"],
            permission_classes=[IsAuthenticated],
             detail=False,
            url_path="get_post", url_name="get_post")
    def get_post(self, request, pk=None):
        error_check_result=is_error_get_post(request.query_params)
        if not isinstance(error_check_result,tuple):
            return error_check_result
        start,end=error_check_result
        sum_record = Post.objects.all().count()
        start = min(start, sum_record)
        end = min(end, sum_record)
        posts = Post.objects.all().order_by("-created")[start:end]
        result = PostSerializer(posts, many=True).data
        my_display_name=UserInfo.objects.get(user=request.user).display_name
        for i,res in enumerate(result):
            sender=res["post_sender"]
            if sender["anonymous_mode"] and sender["display_name"]!=my_display_name:
                result[i]["post_sender"]["display_name"]="anonymous_user"
                result[i]["post_sender"]["icon_url"]=os.path.join(
                         settings.ORIGIN_NAME,
                        "/app_static/images/user_icons/anonymous/icon.png"
                     )
        res = Response(result, status=status.HTTP_200_OK)
        return res

    @action(methods=["get"],
            permission_classes=[IsAuthenticated],
             detail=True)
    def get_user_post(self, request, pk=None):
        error_check_result=is_error_get_post(request.query_params)
        if not isinstance(error_check_result,tuple):
            return error_check_result
        start,end=error_check_result
        post_sender = UserInfo.objects.get(display_name=pk)
        my_display_name=UserInfo.objects.get(user=request.user).display_name
        if post_sender.anonymous_mode and pk!=my_display_name:
            return Response({"error_code": "UserNotExist"},
                            status=status.HTTP_400_BAD_REQUEST)
        posts = Post.objects.filter(post_sender=post_sender)
        sum_record = len(posts)
        start = min(start, sum_record)
        end = min(end, sum_record)
        show_posts = posts.order_by("-created")[start:end]
        result = PostSerializer(show_posts, many=True).data
        res = Response(result, status=status.HTTP_200_OK)
        return res

    @action(methods=["get"], 
            permission_classes=[IsAuthenticated],
            detail=False)
    def get_keyword_post(self, request, pk=None):
        error_check_result=is_error_get_post(request.query_params)
        if not isinstance(error_check_result,tuple):
            return error_check_result
        start,end=error_check_result
        keyword = request.query_params["keyword"]
        posts = Post.objects.filter(keywords__keyword__exact=keyword)
        sum_record = len(posts)
        print(sum_record)
        start = min(start, sum_record)
        end = min(end, sum_record)
        show_posts = posts.order_by("-created")[start:end]
        result = PostSerializer(show_posts, many=True).data
        my_display_name=UserInfo.objects.get(user=request.user).display_name
        for i,res in enumerate(result):
            sender=res["post_sender"]
            if sender["anonymous_mode"] and sender["display_name"]!=my_display_name:
                result[i]["post_sender"]["display_name"]="anonymous_user"
                result[i]["post_sender"]["icon_url"]=os.path.join(
                         settings.ORIGIN_NAME,
                        "/app_static/images/user_icons/anonymous/icon.png"
                     )
        res = Response(result, status=status.HTTP_200_OK)
        return res

    @action(methods=["post"], detail=False,
            permission_classes=[IsAuthenticated],
            url_path="set_post", url_name="set_post")
    def set_post(self, request, pk=None):
        post_data = request.data
        if len(post_data["links"]) > 5:
            return Response({"error_code": "TooManyLinksError"},
                            status=status.HTTP_400_BAD_REQUEST)
        if len(post_data["keywords"]) > 5:
            return Response({"error_code": "TooManyKeywordsError"},
                            status=status.HTTP_400_BAD_REQUEST)
        if len(post_data["links"]) == 0:
            return Response({"error_code": "NoLinkError"},
                            status=status.HTTP_400_BAD_REQUEST)
        if len(post_data["keywords"]) ==0:
            return Response({"error_code": "NoKeywordError"},
                            status=status.HTTP_400_BAD_REQUEST)
        if len(post_data["comment"])==0:
            return Response({"error_code": "NoCommentError"},
                            status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(username=request.user.username)
        user_info = UserInfoSerializer(
            UserInfo.objects.get(user=user)).data
        post_data["post_sender"] = user_info
        serializer = PostSerializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        res=serializer.save()
        print(type(res))
        return res


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
