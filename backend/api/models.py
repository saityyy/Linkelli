from django.db import models
from allauth.socialaccount.models import SocialAccount


class UserInfo(models.Model):
    user = models.OneToOneField(
        SocialAccount,
        on_delete=models.CASCADE,
        primary_key=True)
    display_name = models.CharField(max_length=30)
    icon_url = models.CharField(max_length=100)

    def __str__(self):
        return str(self.display_name)


class Post(models.Model):
    post_id = models.BigAutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    post_sender = models.ForeignKey(
        SocialAccount,
        related_name="post_sender",
        blank=True,
        null=True,
        on_delete=models.CASCADE)
    comment = models.CharField(max_length=100, default="")

    def __str__(self):
        return str(self.post_id)


class Link(models.Model):
    link_id = models.BigAutoField(primary_key=True)
    post = models.ForeignKey(
        Post,
        related_name="links",
        on_delete=models.CASCADE)
    link = models.CharField(max_length=300)
    title = models.CharField(max_length=300, default="")
    img_url = models.CharField(
        max_length=300,
        default="https://static.djangoproject.com/img/icon-touch.e4872c4da341.png")

    class Meta:
        unique_together = (("link", "post"))

    def __str__(self):
        return "{}\n{}\n{}".format(self.post.post_id, self.title, self.link)


class Keyword(models.Model):
    keyword_id = models.BigAutoField(primary_key=True)
    keyword = models.CharField(max_length=300)
    post = models.ForeignKey(
        Post,
        related_name="keywords",
        on_delete=models.CASCADE)

    class Meta:
        unique_together = (("keyword", "post"))

    def __str__(self):
        return str(self.post.post_id) + " , " + self.keyword
