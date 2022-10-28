import random

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, call_command
from django.core.management.commands import loaddata, makemigrations, migrate
from faker import Faker
from posts.models import Comment, Post

User = get_user_model()


class Command(BaseCommand):

    def create_posts_and_comments(self, objects_quantity):
        fake = Faker()
        for _ in range(objects_quantity):
            Post.objects.create(
                author_id=random.randint(1, 4),
                group_id=random.randint(1, 3),
                text=fake.text(max_nb_chars=random.randint(200, 800))
            )
            print(f'Created post {_ + 1}')
        for _ in range(objects_quantity * 3):
            Comment.objects.create(
                author_id=random.randint(1, 4),
                post_id=random.randint(1, 50),
                text=fake.sentence()
            )
            print(f'Created comment {_ + 1}')

    def handle(self, *args, **options):
        call_command('collectstatic', verbosity=0, interactive=False)
        call_command(makemigrations.Command())
        call_command(migrate.Command())
        call_command(loaddata.Command(), 'db_dump')
        self.create_posts_and_comments(objects_quantity=50)
