import django_filters
from .models import Post, Category


class PostFilter(django_filters.FilterSet):

    class Meta:
        model = Post
        fields = ['category']
