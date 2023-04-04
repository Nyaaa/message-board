from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from .filters import PostFilter, CommentFilter
from .models import Post, Comment
from .forms import PostForm, CommentForm, CommentAcceptForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from .mixins import ObjectPermissionRequiredMixin


class PostListView(FilterView):
    template_name = 'post_list.html'
    filterset_class = PostFilter
    paginate_by = 5
    model = Post
    ordering = ['date']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(archived=False)
        return qs


class UserPostListView(LoginRequiredMixin, FilterView):
    template_name = 'post_list.html'
    filterset_class = PostFilter
    paginate_by = 5
    model = Post
    ordering = ['date']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(author=self.request.user)
        return qs


class PostCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_message = _('Post "%(title)s" was created successfully.')
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        return super(PostCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('New post')
        return context


class PostUpdate(SuccessMessageMixin, ObjectPermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('boardapp.change_post',)
    success_message = _('Post "%(title)s" was updated successfully.')
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit post')
        return context


class PostDelete(SuccessMessageMixin, ObjectPermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    permission_required = ('boardapp.delete_post',)
    success_url = reverse_lazy('home')
    success_message = _('Post deleted.')


class CommentCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'post_edit.html'
    success_message = _('Reply sent.')
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        comment = form.save(commit=False)
        post_id = self.kwargs['post']
        comment.author = self.request.user
        comment.post = get_object_or_404(Post, pk=post_id)
        return super(CommentCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('New reply')
        return context


class CommentListView(FilterView):
    template_name = 'reply_list.html'
    filterset_class = CommentFilter
    paginate_by = 10
    model = Comment
    ordering = ['post', 'created']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(post__author=self.request.user)
        return qs


class CommentDelete(SuccessMessageMixin, ObjectPermissionRequiredMixin, DeleteView):
    model = Comment
    template_name = 'post_delete.html'
    permission_required = ('boardapp.delete_comment',)
    success_url = reverse_lazy('user_posts')
    success_message = _('Reply deleted.')


class CommentAccept(SuccessMessageMixin, ObjectPermissionRequiredMixin, UpdateView):
    model = Comment
    template_name = 'reply_accept.html'
    success_url = reverse_lazy('replies')
    permission_required = ('boardapp.accept_comment',)
    success_message = _('Reply accepted.')
    form_class = CommentAcceptForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        post = comment.post
        comment.accepted = True
        post.archived = True
        post.save()
        return super(CommentAccept, self).form_valid(form)
