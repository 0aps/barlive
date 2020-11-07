import factory
from .models import Bar, BarSocialMedia, Post, Mention, SocialMedia


class BarFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bar


class SocialMediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SocialMedia


class BarSocialMediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BarSocialMedia

    bar = factory.SubFactory(BarFactory)
    social_media = factory.SubFactory(SocialMediaFactory)


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post


class MentionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Mention


class InstagramFactory(SocialMediaFactory):
    name = "Instagram"
    url = "https://www.instagram.com/"


class EmeFactory(BarFactory):
    name = "eme by marketcito"


class EmeInstagramFactory(BarSocialMediaFactory):
    social_media = factory.SubFactory(InstagramFactory)
    bar = factory.SubFactory(EmeFactory)
    username = "emebymarketcito"


class EmePost(PostFactory):
    bar_media = factory.SubFactory(EmeInstagramFactory)
    description = "Sunday plans : ir a ver a @dapatres en nuestra " \
                  "terraza 🎶 Gracias a @stoli_rd ‼️ #Emebymarketcito " \
                  " #emeHours #SundayFunday"
    url = "https://www.instagram.com/p/CHA4JbQgnLQ/" \
          "?utm_source=ig_web_copy_link"
