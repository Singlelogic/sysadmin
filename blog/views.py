from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import TagForm, PostForm
from .models import Post, Tag
from .utils import ObjectDetailMixin, OblectCreateMixin


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


class TagUpdate(View):
    def get(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        bound_form = TagForm(instance=tag)

        return render(request, 'blog/tag_update_form.html', context={
            'form': bound_form,
            'tag': tag
        })

    def post(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        bound_form = TagForm(request.POST, instance=tag)

        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)
        return render(request, 'blog/tag_update_form.html', context={
            'form': bound_form,
            'tag': tag
        })


def posts_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', context={'posts': posts})


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})
