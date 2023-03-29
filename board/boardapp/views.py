from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django_filters.views import FilterView
from .filters import PostFilter
from .models import Post


class PostListView(FilterView):
    template_name = 'post_list.html'
    filterset_class = PostFilter
    paginate_by = 3
    model = Post
