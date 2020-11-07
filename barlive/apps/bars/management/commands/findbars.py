from django.core.management.base import BaseCommand, CommandError
from barlive.apps.bots.models import BotManager
import traceback


class Command(BaseCommand):
    help = "Find bars that are playing live music "

    def add_arguments(self, parser):
        parser.add_argument("social_medias", nargs='+', type=str)

    def handle(self, *args, **options):
        bot_manager = BotManager(options["social_medias"])
        try:
            posts = bot_manager.find_posts()
            self._handle_posts(posts)
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            raise CommandError(e)

    def _handle_posts(self, posts):
        self.stdout.write(
            self.style.SUCCESS(f"Successfully found {len(posts)}"))

        for post in posts:
            self.stdout.write(str(post))
