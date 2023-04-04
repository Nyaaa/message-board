from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from django.utils import timezone


class User(AbstractUser):
    activated = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True
        if perm in ('boardapp.change_post', 'boardapp.delete_post'):
            return True if obj.author == self else False
        elif perm in ('boardapp.accept_comment', 'boardapp.change_comment', 'boardapp.delete_comment'):
            return True if obj.post.author == self else False
        else:
            return super().has_perm(perm, obj)


def generate_token():
    return random.randint(1000, 9999)


class Token(models.Model):
    value = models.IntegerField(default=generate_token)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def delete_old():
        time = timezone.now() - timezone.timedelta(hours=3)
        old = Token.objects.filter(date__lte=time)
        old.delete()
