from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from boardapp.utils import upload_file
from django.urls import reverse
import os
from django.conf import settings
from django.core import mail
from model_bakery import baker
from boardapp.models import Post, Comment
from django.contrib.auth import get_user_model

baker.generators.add('tinymce.models.HTMLField', lambda: '')


class UtilTests(TestCase):
    def tearDown(self) -> None:
        files = os.listdir(settings.MEDIA_ROOT)
        for f in files:
            os.remove(os.path.join(settings.MEDIA_ROOT, f))

    def testFileUpload(self):
        video = SimpleUploadedFile("file.mp4", b"file_content", content_type="video/mp4")
        request = RequestFactory().post(reverse('post_create'), data={'file': video})
        response = upload_file(request)
        self.assertEqual(response.status_code, 200)
        files = os.listdir(settings.MEDIA_ROOT)
        self.assertEqual(len(files), 1)


class TestMail(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_user(
            username='user1', password='12345', email='user1@localhost')
        cls.user2 = get_user_model().objects.create_user(
            username='user2', password='12345', email='user2@localhost')
        cls.post = baker.make(Post, author=cls.user)

    def setUp(self) -> None:
        self.client.login(username='user1', password='12345')

    def testReplyNotification(self):
        baker.make(Comment, post=self.post)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['user1@localhost'])

    def testReplyAcceptedNotification(self):
        baker.make(Comment, author=self.user2, post=self.post)
        mail.outbox.clear()
        self.client.post(reverse('reply_accept', args=[1]),
                         follow=True, data={})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['user2@localhost'])

    def testReplySilent(self):
        comment = baker.make(Comment, post=self.post, accepted=False)
        mail.outbox.clear()
        comment.text = '123'
        comment.save()
        self.assertEqual(len(mail.outbox), 0)
