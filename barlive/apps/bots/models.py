from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist
from instagram_web_api import Client
from barlive.apps.bars.models import (
    BarSocialMedia, Post, SocialMedia, Word)
from urllib import request
from urllib.parse import urlparse

import logging
import hashlib
import string
import random
import re
import os


logger = logging.getLogger("findbars")


class Bot:
    """
        Abstract class to handle interactions with social media
    """
    def __init__(self, social_media, words):
        self.social_media = social_media
        self.words = words
        self.regex = f"({'|'.join(self.words)})"

    def get_bars(self):
        bars = BarSocialMedia.objects.filter(
            social_media__name=self.social_media.name)
        return bars

    def find_posts(self):
        raise NotImplementedError("")

    def get_post_image(self, url):
        result = request.urlretrieve(url)
        name = os.path.basename(urlparse(url).path)
        return File(open(result[0], "rb"), name)


class InstagramClient(Client):
    @staticmethod
    def _extract_rhx_gis(html):
        options = string.ascii_lowercase + string.digits
        text = ''.join([random.choice(options) for _ in range(8)])
        return hashlib.md5(text.encode()).hexdigest()


class InstagramBot(Bot):
    """
        Handle interactions with instagram
    """
    def __init__(self, social_media, words):
        super().__init__(social_media, words)
        self.client = InstagramClient(auto_patch=True,
                                      drop_incompat_keys=False)

    def find_posts(self):
        logger.info(f"Looking at {self.social_media.name} social media:")
        posts = []
        bars = self.get_bars()
        for bar in bars:
            logger.info(f"Checking @{bar.username} ...")
            if not bar.user_reference:
                self._find_and_store_user_id(bar)

            raw_posts = self.client.user_feed(bar.user_reference, count=10)
            live_music_posts = [post["node"] for post in raw_posts
                                if self._is_live_music_post(post["node"])]

            valid_posts = self._get_non_stored_posts(live_music_posts)
            for live_music_post in valid_posts:
                image = self.get_post_image(live_music_post["display_url"])
                description = live_music_post["caption"]["text"]
                link = live_music_post["link"]

                post = Post(bar_media=bar,
                            description=description,
                            url=link)

                post.image.save(image.name, image)
                post.save()
                posts.append(post)

        return posts

    def _find_and_store_user_id(self, bar):
        user_info = self.client.user_info2(bar.username)
        bar.user_reference = user_info["id"]
        bar.save()

    def _is_live_music_post(self, post):
        description = post["caption"]["text"].lower()
        result = re.search(self.regex, description)
        return result

    def _get_non_stored_posts(self, posts):
        links = [post["link"] for post in posts]
        saved_links = list(Post.objects.filter(url__in=links)
                           .values_list("url", flat=True))

        return [post for post in posts
                if post["link"] not in saved_links]


class BotManager:
    """
        Handle interactions between all supported social media managers
    """
    def __init__(self, names):
        self.bots = self._get_available_bots(names)

    def get_bot(self, name):
        return next((bot for bot in self.bots
                     if bot.social_media.name == name.capitalize()), None)

    def find_posts(self):
        posts = []
        for bot in self.bots:
            posts += bot.find_posts()

        return posts

    def _get_available_bots(self, names):
        bots = []
        module = globals()
        social_medias = SocialMedia.objects.filter(name__in=names)

        if len(names) != len(social_medias):
            raise ObjectDoesNotExist(
                "One ore more social media isn't supported.")

        words = list(Word.objects.all().values_list("name", flat=True))
        for social_media in social_medias:
            name = social_media.name.capitalize()
            bot_class = module[f"{name}Bot"]
            bots.append(bot_class(social_media, words))

        return bots
