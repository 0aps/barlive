from django.db import models
from barlive.models import BaseModel


class SocialMedia(models.Model):
    name = models.CharField(max_length=30)
    url = models.URLField(max_length=100)

    def __str__(self):
        return self.name


class Bar(BaseModel):
    social_medias = models.ManyToManyField(SocialMedia,
                                           through='BarSocialMedia')
    name = models.CharField(max_length=30)
    logo = models.ImageField(
        null=True,
        blank=True,
    )
    last_check = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class BarSocialMedia(models.Model):
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE)
    url = models.URLField(max_length=100, null=True, blank=True, unique=True)
    username = models.CharField(max_length=30)
    user_reference = models.CharField(max_length=30, null=True, blank=True)

    @property
    def bar_url(self):
        if not self.url:
            return f'{self.social_media.url}/{self.username}'

        return self.url

    def __str__(self):
        return self.bar_url


class Post(BaseModel):
    bar_media = models.ForeignKey(BarSocialMedia, on_delete=models.CASCADE)
    image = models.ImageField(
        null=True,
        blank=True,
    )
    description = models.TextField(max_length=1000)
    url = models.URLField(max_length=200)

    def __str__(self):
        return (
            f'Bar: {self.bar_media.bar.name}\n'
            f'URL: {self.url}'
        )


class Mention(BaseModel):
    name = models.CharField(max_length=30)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Word(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
