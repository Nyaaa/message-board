from django.test import TestCase
from boardapp.models import Post, Comment, Category
from model_bakery import baker
from django.contrib.auth import get_user_model
from django.urls import reverse

baker.generators.add('tinymce.models.HTMLField', lambda: '')


class ViewTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        baker.make(Post)
        baker.make(Comment)
        cls.user = get_user_model().objects.create_user(username='user1', password='12345')
        cls.cat = Category.objects.get(pk=1)

    def setUp(self) -> None:
        self.client.login(username='user1', password='12345')

    def testPostCreate(self):
        response = self.client.post(reverse('post_create'), follow=True,
                                    data={'category': 1, 'title': 'title', 'text': 'text'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.get(author=self.user))

    def testCommentCreate(self):
        response = self.client.post(reverse('reply_create', args=[1]), follow=True, data={'text': 'text'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.get(text='text'))

    def testCommentAccept(self):
        post = baker.make(Post, author=self.user)
        comment = baker.make(Comment, post=post)
        response = self.client.post(reverse('reply_accept', args=[comment.pk]),
                                    follow=True, data={})
        self.assertEqual(response.status_code, 200)
        comment.refresh_from_db()
        self.assertTrue(comment.accepted)
