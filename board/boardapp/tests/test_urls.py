from django.test import TestCase
from boardapp.models import Post, Comment
from model_bakery import baker
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

baker.generators.add('tinymce.models.HTMLField', lambda: '')


def get_url(page):
    try:
        return reverse(page)
    except NoReverseMatch:
        return reverse(page, args=[1])


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        baker.make(Post)
        baker.make(Comment)
        cls.public = ['home', 'post_detail', 'activate', 'signup', 'login']
        cls.private = ['user_posts', 'post_create', 'post_edit', 'post_delete',
                       'reply_create', 'profile', 'password_change', 'profile_edit',
                       'replies', 'reply_create', 'reply_delete']

    def testPublicAccess(self):
        for page in self.public:
            url = get_url(page)
            self.assertEqual(self.client.get(url).status_code, 200)

    def testPrivateNoAccess(self):
        for page in self.private:
            url = get_url(page)
            expected_url = '/user/login/?next=' + url
            self.assertRedirects(self.client.get(url), expected_url, status_code=302, target_status_code=200,
                                 fetch_redirect_response=True)

    def testPrivateAccess(self):
        user = get_user_model()
        user.objects.create_user(username='testuser', password='12345', is_superuser=True)
        self.assertTrue(self.client.login(username='testuser', password='12345'))

        for page in self.private:
            url = get_url(page)
            self.assertEqual(self.client.get(url).status_code, 200)
