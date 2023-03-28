from django.contrib.auth.models import AbstractUser
from django.db import models
import random


class User(AbstractUser):
    activated = models.BooleanField(default=False)


def generate_token():
    return random.randint(1000, 9999)


class Token(models.Model):
    value = models.IntegerField(default=generate_token)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def delete_old(self):
        raise NotImplementedError
