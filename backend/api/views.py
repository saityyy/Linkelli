import re
import uuid
from allauth.account.forms import LoginForm
import os
import uuid
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
            user = SocialAccount.objects.get(user=request.user)
            uid, provider = user.uid, user.provider
            try:
                user_info = UserInfo.objects.get(user=user)
            except ObjectDoesNotExist:
                temp_display_name = uuid.uuid3(
                    uuid.NAMESPACE_X500,
                    uid + provider).hex
                return JsonResponse(
                    {"exist_user_info": False,
                     "display_name": temp_display_name[:10],
                     "icon_url": "http://127.0.0.1:8000/static/images/user_icons/no_image.png"
                     }, status=status.HTTP_200_OK)
            result = UserInfoSerializer(user_info).data
            _ = result.pop("user")
            _ = result.pop("user_info_id")
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
        user = SocialAccount.objects.get(user=request.user)
        uid, provider = user.uid, user.provider
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
        ext = img.name.split(".")[-1]
        filename = "{}.{}".format(
            uuid.uuid3(
                uuid.NAMESPACE_X500,
                uid + provider).hex,
            ext)
        icon_path = "./api/static/images/user_icons/"
        if os.path.isfile(os.path.join(icon_path, filename)):
            os.remove(os.path.join(icon_path, filename))
        FileSystemStorage(
            location=icon_path).save(filename, img)
        setting_items["display_name"] = request.data["display_name"]
        if request.data["anonymous_mode"] == 'true':
            setting_items["anonymous_mode"] = True
        else:
            setting_items["anonymous_mode"] = False
        setting_items["icon_url"] = os.path.join(
            "http://127.0.0.1:8000/static/images/user_icons/", filename)
        UserInfo.objects.update_or_create(
            user=user, defaults=setting_items)
        return Response({"status": "userinfo set"})


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all()[0:1]

    @action(methods=["get"], detail=False,
            url_path="get_post", url_name="get_post")
    def get_post(self, request, pk=None):
        q = request.query_params
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
        sum_record = len(Post.objects.all())
        start = min(start, sum_record)
        end = min(end, sum_record)
        posts = Post.objects.all().order_by("-created")[start:end]
        result = self.get_serializer(posts, many=True).data
        for i in range(len(result)):
            _ = result[i]["post_sender"].pop("user_info_id")
            _ = result[i]["post_sender"].pop("user")
        res = Response(result, status=status.HTTP_200_OK)
        return res

    @action(methods=["get"], detail=True)
    def get_user_post(self, request, pk=None):
        q = request.query_params
        start, end = int(q["start"]), int(q["start"]) + int(q["num"])
        post_sender = UserInfo.objects.get(display_name=pk)
        posts = Post.objects.filter(post_sender=post_sender)
        sum_record = len(posts)
        start = min(start, sum_record)
        end = min(end, sum_record)
        show_posts = posts.order_by("-created")[start:end]
        result = self.get_serializer(show_posts, many=True).data
        for i in range(len(result)):
            _ = result[i]["post_sender"].pop("user_info_id")
            _ = result[i]["post_sender"].pop("user")
        res = Response(result, status=status.HTTP_200_OK)
        return res

    @action(methods=["get"], detail=False)
    def get_keyword_post(self, request, pk=None):
        q = request.query_params
        start, end = int(q["start"]), int(q["start"]) + int(q["num"])
        keyword = q["keyword"]
        # keywords_post = Keyword.objects.filter(keyword=keyword)
        posts = Post.objects.filter(keywords__keyword__exact=keyword)
        sum_record = len(posts)
        print(sum_record)
        start = min(start, sum_record)
        end = min(end, sum_record)
        show_posts = posts.order_by("-created")[start:end]
        result = self.get_serializer(show_posts, many=True).data
        for i in range(len(result)):
            _ = result[i]["post_sender"].pop("user_info_id")
            _ = result[i]["post_sender"].pop("user")
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
        user = SocialAccount.objects.get(user=request.user)
        user_info = UserInfoSerializer(
            UserInfo.objects.get(user=user)).data
        post_data["post_sender"] = user_info
        serializer = PostSerializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = Response({"result": "success set post"},
                       status=status.HTTP_200_OK)
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
