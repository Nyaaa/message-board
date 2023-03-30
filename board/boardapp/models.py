from django.conf import settings
from django.db import models
from tinymce import models as tinymce_models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Name'))

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('categories')


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Name'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    text = tinymce_models.HTMLField(verbose_name=_('Text'))
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, verbose_name=_('Category'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date'))
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=_('Post'))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('Author'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date'))
    text = models.TextField(verbose_name=_('Text'))
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
