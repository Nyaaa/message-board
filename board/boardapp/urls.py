from django.urls import path
from .views import PostListView, PostCreate, PostUpdate, PostDelete, UserPostListView, CommentCreate

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('my-posts/', UserPostListView.as_view(), name='user_posts'),
    path('post/', PostCreate.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('post/<int:post>/reply/', CommentCreate.as_view(), name='reply_create'),
]
