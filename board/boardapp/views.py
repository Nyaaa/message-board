from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django_filters.views import FilterView
from .filters import PostFilter
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404


class PostListView(FilterView):
    template_name = 'post_list.html'
    filterset_class = PostFilter
    paginate_by = 5
    model = Post


class UserPostListView(LoginRequiredMixin, FilterView):
    template_name = 'post_list_user.html'
    filterset_class = PostFilter
    paginate_by = 5
    model = Post

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(author=self.request.user)
        return qs


class PostCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_message = _('Post "%(title)s" was created successfully.')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super(PostCreate, self).form_valid(form)


class PostUpdate(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_message = _('Post "%(title)s" was updated successfully.')


class PostDelete(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ('news.delete_post',)
    success_message = _('Post was deleted successfully.')


class CommentCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'post_edit.html'
    success_message = _('Reply sent.')
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        comment = form.save(commit=False)
        post_id = self.kwargs['post']
        comment.post = get_object_or_404(Post, pk=post_id)
        return super(CommentCreate, self).form_valid(form)
