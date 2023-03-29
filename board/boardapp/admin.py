from django.contrib import admin
from .models import Category, Post
from modeltranslation.admin import TranslationAdmin


class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(admin.ModelAdmin):
    model = Post


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
