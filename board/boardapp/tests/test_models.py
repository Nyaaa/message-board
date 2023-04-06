from django.test import TestCase
from boardapp.models import Post, Comment, Category
from model_bakery import baker


baker.generators.add('tinymce.models.HTMLField', lambda: '')


class ModelTests(TestCase):
    def testCategoryStr(self):
        obj = baker.make(Category, name='123')
        self.assertEqual(str(obj), '123')

    def testPostStr(self):
        obj = baker.make(Post, title='123')
        self.assertEqual(str(obj), '123')

    def testCommentStr(self):
        obj = baker.make(Comment, text='123')
        self.assertEqual(str(obj), '123')
