from django import forms
from .models import Post, Category, Comment
from django.utils.translation import gettext as _


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'text']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
