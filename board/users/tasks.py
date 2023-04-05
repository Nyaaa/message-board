from users.models import Token
from boardapp.models import Post
from django.utils import timezone
from django.db.models import Count


def delete_old():
    Token.delete_old()


def newsletter():
    time = timezone.now() - timezone.timedelta(days=7)
    posts = Post.objects.filter(date__gte=time)

