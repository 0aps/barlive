from django.test import TestCase
from barlive.apps.bars.factories import EmePost
from .models import BotManager, ObjectDoesNotExist, InstagramBot
from unittest import skip


class BotManagerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = EmePost()

    def test_should_not_resolve_invalid(self):
        """should fail for unknown service"""
        self.assertRaises(ObjectDoesNotExist, BotManager, ["NextBigThing"])

    def test_should_resolve_instagram(self):
        """should resolve for instagram bot"""
        bot_manager = BotManager(["Instagram"])

        self.assertEqual(1, len(bot_manager.bots))

        instagram_bot = bot_manager.get_bot("instagram")
        self.assertIsInstance(instagram_bot, InstagramBot)

    @skip
    def test_should_find_posts(self):
        """should find an existing post"""
        bot_manager = BotManager(["Instagram"])

        posts = bot_manager.find_posts()
        self.assertTrue(posts)
