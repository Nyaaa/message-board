from django.test import TestCase
from users.models import User, generate_token
from boardapp.models import Post, Comment
from model_bakery import baker

baker.generators.add('tinymce.models.HTMLField', lambda: '')


class ModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = baker.make(User)
        cls.post2 = baker.make(Post)
        cls.post = baker.make(Post, author=cls.user)

    def testToken(self):
        token = generate_token()
        self.assertEqual(len(str(token)), 4)

    def testPostPerms(self):
        self.assertTrue(self.user.has_perm('boardapp.delete_post', self.post))
        self.assertFalse(self.user.has_perm('boardapp.change_post', self.post2))

    def testCommentPerms(self):
        comment = baker.make(Comment, post=self.post)
        comment2 = baker.make(Comment)
        self.assertTrue(self.user.has_perm('boardapp.accept_comment', comment))
        self.assertFalse(self.user.has_perm('boardapp.accept_comment', comment2))

    def testOtherPerms(self):
        self.assertFalse(self.user.has_perm('boardapp.create_category'))

    def testAdminPerms(self):
        admin = baker.make(User, is_superuser=True)
        self.assertTrue(admin.has_perm('boardapp.delete_post', self.post2))
        self.assertTrue(admin.has_perm('boardapp.delete_category'))
