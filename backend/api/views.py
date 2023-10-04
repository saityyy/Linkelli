import uuid
import os
from django.conf import settings
from django.http import JsonResponse
from allauth.socialaccount.models import SocialAccount
from .models import Post, UserInfo
from rest_framework import viewsets
from .serializers import PostSerializer, UserInfoSerializer
from django.middleware.csrf import get_token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import FileSystemStorage
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
    return response


@parser_classes([MultiPartParser, FormParser])
class UserViewSet(viewsets.ModelViewSet):
    queryset = SocialAccount.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    ttp_method_names = ['get', "post"]

    @action(methods=["get"], detail=False,
            permission_classes=[IsAuthenticated],
            url_path="get_my_info", url_name="get_my_info")
    def get_my_info(self, request, pk=None):
        user_id = uuid.uuid3(uuid.NAMESPACE_X500,
                             request.user.username).hex
        user = User.objects.get(username=request.user.username)
        no_settings = False
        try:
            user_info = UserInfo.objects.get(user=user)
        except ObjectDoesNotExist:
            user_info = UserInfo.objects.create(
                user=user,
                display_name=user_id[:10],
                icon_url="/app_static/images/user_icons/anonymous/icon.png",
                anonymous_mode=False
            )
        result = UserInfoSerializer(user_info).data
        if result["display_name"] == user_id[:10]:
            no_settings = True
        result["no_settings"] = no_settings
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=True,
            permission_classes=[IsAuthenticated],
            url_path="get_user_info", url_name="get_user_info")
    def get_user_info(self, request, pk=None):
        try:
            user_info = UserInfo.objects.get(display_name=pk)
        except ObjectDoesNotExist:
            return Response({"error_code": "UserNotExist"},
                            status=status.HTTP_404_NOT_FOUND)
        my_display_name = UserInfo.objects.get(user=request.user).display_name
        result = UserInfoSerializer(user_info).data
        if (result["anonymous_mode"] and
                result["display_name"] != my_display_name):
            return Response({"error_code": "UserNotExist"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(result, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False,
            permission_classes=[IsAuthenticated],
            url_path="set_user_info", url_name="set_user_info")
    def set_user_info(self, request, pk=None):
        setting_items = {}
        user_hash_id = uuid.uuid3(uuid.NAMESPACE_X500,
                                  request.user.username).hex
        user = User.objects.get(username=request.user.username)
        img = request.data["icon_image_file"]
        if img.size > 300_000:  # 300kb
            return Response({"error_code": "TooBigImageSize"},
                            status=status.HTTP_400_BAD_REQUEST)
        if not hasattr(img, "content_type"):
            return Response({"error_code": "InvalidFileType"},
                            status=status.HTTP_400_BAD_REQUEST)
        if not (img.content_type in ["image/png", "image/jpeg", "image/gif"]):
            return Response({"error_code": "InvalidFileType"},
                            status=status.HTTP_400_BAD_REQUEST)
        icon_path = os.path.join(settings.STATIC_ROOT, "images/user_icons/")
        if os.environ["DJANGO_MODE"] == "development":
            icon_path = "./api/static/images/user_icons/"
        user_icon_dir = os.path.join(icon_path, user_hash_id)
        filename = "icon.png"
        if not os.path.exists(user_icon_dir):
            os.mkdir(user_icon_dir)
            FileSystemStorage(
                location=user_icon_dir).save(filename, img)
        else:
            os.remove(os.path.join(user_icon_dir, filename))
            FileSystemStorage(
                location=user_icon_dir).save(filename, img)
        setting_items["display_name"] = request.data["display_name"]
        if request.data["anonymous_mode"] == 'true':
            setting_items["anonymous_mode"] = True
        else:
            setting_items["anonymous_mode"] = False
        setting_items["icon_url"] = os.path.join(
            "/app_static/images/user_icons/",
            user_hash_id,
            filename)
        is_same_name = False
        if UserInfo.objects.filter(user=user).exists():
            is_same_name = (setting_items["display_name"] ==
                            UserInfo.objects.get(user=user).display_name)
        serializer = UserInfoSerializer(data=setting_items)
        if not serializer.is_valid():
            errors = serializer.errors
            try:
                if errors["display_name"][0].code == "blank":
                    return Response({"error_code": "NotExistDisplayName"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except (KeyError, IndexError, TypeError):
                pass
            try:
                if (errors["display_name"][0].code ==
                        "unique" and not is_same_name):
                    return Response({"error_code": "DuplicateDisplayName"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except (KeyError, IndexError, TypeError):
                pass
            try:
                if errors["display_name"][0].code == "invalid":
                    return Response({"error_code": "InvalidDisplayName"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except (KeyError, IndexError, TypeError):
                pass
        res, _ = UserInfo.objects.update_or_create(
            user=user, defaults=setting_items)
        return Response(UserInfoSerializer(res).data,
                        status=status.HTTP_200_OK)


def is_error_get_post(q):
    if (q.get("start") is None) or (q.get("num") is None):
        return Response({"error_code": "BadQueryRequest"},
                        status=status.HTTP_400_BAD_REQUEST)
    if not q["start"].isdecimal() or not q["num"].isdecimal():
        return Response({"error_code": "BadQueryRequest"},
                        status=status.HTTP_400_BAD_REQUEST)
    start, num = (int(q["start"]), int(q["num"]))
    end = start + num
    if start < 0 or num < 0:
        return Response({"error_code": "BadQueryRequest"},
                        status=status.HTTP_400_BAD_REQUEST)
    if num >= 30:
        return Response({"error_code": "TooManyRequestPost"},
                        status=status.HTTP_400_BAD_REQUEST)
    return (start, end)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all()[0:1]

    @action(methods=["get"],
            detail=False,
            url_path="get_post", url_name="get_post")
    def get_post(self, request, pk=None):
        error_check_result = is_error_get_post(request.query_params)
        if not isinstance(error_check_result, tuple):
            return error_check_result
        start, end = error_check_result
        posts = []
        try:
            keyword = request.query_params["keyword"]
            sum_record = Post.objects.filter(
                keywords__keyword__exact=keyword).count()
            start = min(start, sum_record)
            end = min(end, sum_record)
            posts = Post.objects.filter(
                keywords__keyword__exact=keyword
            ).order_by("-created")[start:end]
        except KeyError:
            sum_record = Post.objects.all().count()
            start = min(start, sum_record)
            end = min(end, sum_record)
            posts = Post.objects.all().order_by("-created")[start:end]
        result = PostSerializer(posts, many=True).data
        my_display_name = UserInfo.objects.get(user=request.user).display_name
        for i, res in enumerate(result):
            sender = UserInfo.objects.get(user_info_id=res["post_sender"])
            result[i]["post_sender"] = {}
            if (sender.anonymous_mode and
                    sender.display_name != my_display_name):
                result[i]["post_sender"]["display_name"] = "anonymous_user"
                result[i]["post_sender"]["icon_url"] = os.path.join(
                    settings.ORIGIN_NAME,
                    "/app_static/images/user_icons/anonymous/icon.png"
                )
                result[i]["post_sender"]["anonymous_mode"] = True
            else:
                result[i]["post_sender"]["display_name"] = sender.display_name
                result[i]["post_sender"]["icon_url"] = sender.icon_url
                result[i]["post_sender"]["anonymous_mode"] = False

        res = Response(result, status=status.HTTP_200_OK)
        return res

    @action(methods=["get"],
            detail=True, url_path="get_user_post", url_name="get_user_post")
    def get_user_post(self, request, pk=None):
        error_check_result = is_error_get_post(request.query_params)
        if not isinstance(error_check_result, tuple):
            return error_check_result
        start, end = error_check_result
        if not UserInfo.objects.filter(display_name=pk).exists():
            return Response({"error_code": "UserNotExist"},
                            status=status.HTTP_404_NOT_FOUND)
        post_sender = UserInfo.objects.get(display_name=pk)
        my_display_name = UserInfo.objects.get(user=request.user).display_name
        if post_sender.anonymous_mode and pk != my_display_name:
            return Response({"error_code": "UserNotExist"},
                            status=status.HTTP_404_NOT_FOUND)
        posts = Post.objects.filter(post_sender=post_sender)
        sum_record = len(posts)
        start = min(start, sum_record)
        end = min(end, sum_record)
        show_posts = posts.order_by("-created")[start:end]
        result = PostSerializer(show_posts, many=True).data
        for i in range(len(result)):
            post_sender_dict = {
                "display_name": post_sender.display_name,
                "icon_url": post_sender.icon_url
            }
            result[i]["post_sender"] = post_sender_dict
        res = Response(result, status=status.HTTP_200_OK)
        return res

    @action(methods=["get"],
            detail=False,
            url_path="get_keyword_post",
            url_name="get_keyword_post")
    def get_keyword_post(self, request, pk=None):
        error_check_result = is_error_get_post(request.query_params)
        if not isinstance(error_check_result, tuple):
            return error_check_result
        start, end = error_check_result
        keyword = request.query_params["keyword"]
        posts = Post.objects.filter(keywords__keyword__exact=keyword)
        sum_record = len(posts)
        start = min(start, sum_record)
        end = min(end, sum_record)
        show_posts = posts.order_by("-created")[start:end]
        result = PostSerializer(show_posts, many=True).data
        my_display_name = UserInfo.objects.get(user=request.user).display_name
        for i, res in enumerate(result):
            sender = UserInfo.objects.get(user_info_id=res["post_sender"])
            if (sender.anonymous_mode and
                    sender.display_name != my_display_name):
                result[i]["post_sender"]["display_name"] = "anonymous_user"
                result[i]["post_sender"]["icon_url"] = os.path.join(
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
        user = User.objects.get(username=request.user.username)
        user_info = UserInfo.objects.get(user=user)
        post_data["post_sender"] = user_info.user_info_id
        serializer = PostSerializer(data=post_data)
        if not serializer.is_valid():
            errors = serializer.errors
            try:
                if errors["comment"][0].code == "max_length":
                    return Response({"error_code": "TooLongComment"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except (KeyError, IndexError):
                pass
            try:
                if errors["comment"][0].code == "blank":
                    return Response({"error_code": "NoComment"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except (KeyError, IndexError, TypeError):
                pass
            try:
                if errors["links"]["non_field_errors"][0].code == "min_length":
                    return Response({"error_code": "NoLink"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except (KeyError, IndexError, TypeError):
                pass
            try:
                if errors["links"][0]["link"][0].code == "invalid":
                    return Response({"error_code": "InvalidURL"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except (KeyError, IndexError, TypeError):
                pass
            try:
                if (errors["keywords"]["non_field_errors"][0].code
                        == "min_length"):
                    return Response({"error_code": "NoKeyword"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except (KeyError, IndexError, TypeError):
                pass
            try:
                if errors["keywords"][0]["keyword"][0].code == "max_length":
                    return Response({"error_code": "TooLongKeyword"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except (KeyError, IndexError, TypeError):
                pass
            try:
                if (errors["links"]["non_field_errors"][0].code
                        == "duplicate_value"):
                    return Response({"error_code": "DuplicateLink"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except (KeyError, IndexError, TypeError):
                pass
            try:
                if (errors["keywords"]["non_field_errors"][0].code
                        == "duplicate_value"):
                    return Response({"error_code": "DuplicateKeyword"},
                                    status=status.HTTP_400_BAD_REQUEST)
            except (KeyError, IndexError, TypeError):
                pass
            return Response({"error_code": "BadRequest"},
                            status=status.HTTP_400_BAD_REQUEST)

        res = serializer.save()
        return res
