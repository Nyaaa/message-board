from django.urls import path
from .views import PostListView, PostCreate, PostUpdate, PostDelete, UserPostListView,\
    CommentCreate, CommentListView, CommentDelete, CommentAccept

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('my-posts/', UserPostListView.as_view(), name='user_posts'),
    path('post/', PostCreate.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('post/<int:post>/reply/', CommentCreate.as_view(), name='reply_create'),
    path('replies/', CommentListView.as_view(), name='replies'),
    path('reply/<int:pk>/delete/', CommentDelete.as_view(), name='reply_delete'),
    path('reply/<int:pk>/accept/', CommentAccept.as_view(), name='reply_accept'),
]
