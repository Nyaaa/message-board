from django.test import TestCase
from django.contrib.auth import get_user_model
from users.tasks import delete_old, newsletter
from boardapp.models import Post
from users.models import Token
from model_bakery import baker
from django.core import mail
from django.utils import timezone
from unittest import mock

baker.generators.add('tinymce.models.HTMLField', lambda: '')


class TaskTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_user(
            username='user1', password='12345', email='user1@localhost', subscriber=True)

    def testNewsletter(self):
        baker.make(Post)
        newsletter()
        self.assertEqual(len(mail.outbox), 1)

    def testDeleteTokens(self):
        mocked = timezone.datetime(2020, 1, 1, 1, 1, 1, tzinfo=timezone.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            token = baker.make(Token)
            self.assertEqual(token.date, mocked)
            self.assertTrue(Token.objects.all().exists())
        delete_old()
        self.assertFalse(Token.objects.all().exists())
