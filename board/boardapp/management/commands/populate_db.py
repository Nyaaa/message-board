from django.core.management.base import BaseCommand
from boardapp.models import Post, Comment, Category
from faker import Faker
import random
from django.contrib.auth import get_user_model

fake = Faker()


class Command(BaseCommand):
    help = 'Populates the database with random generated data.'

    def add_arguments(self, parser):
        parser.add_argument('--posts', type=int, help='The amount of posts to create.')

    def handle(self, *args, **options):
        posts = options['posts'] if options['posts'] else 50
        user = get_user_model()
        u1 = user.objects.create_user(username='user01', password='123')
        u2 = user.objects.create_user(username='user02', password='123')

        Post.objects.bulk_create([Post(
            title=fake.text(max_nb_chars=20),
            text=fake.paragraph(nb_sentences=5),
            category=random.choice(Category.objects.all()),
            author=random.choice([u1, u2])
        ) for _ in range(posts)], ignore_conflicts=True)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database.'))
