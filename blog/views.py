from django.shortcuts import render, redirect, reverse
from django.views.generic import View

from .forms import TagForm, PostForm
from .models import Post, Tag
from .utils import ObjectDetailMixin, OblectCreateMixin, ObjectUpdateMixin


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class PostCreate(OblectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create.html'


class TagCreate(OblectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag_create.html'


class PostUpdate(ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'


class TagUpdate(ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'


class TagDelete(View):
    def get(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        return render(request, 'blog/tag_delete_form.html', context={
            'tag': tag
        })

    def post(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        tag.delete()
        return redirect(reverse('tags_list_url'))


def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', context={'posts': posts})


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})
