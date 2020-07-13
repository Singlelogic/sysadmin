from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .forms import TagForm, PostForm
from .models import Post, Tag
from .mixins import *
from .utils import paginator


class PostDetail(View):

    def get(self, request, slug):
        obj = get_object_or_404(Post, slug__iexact=slug)
        return render(request, 'blog/post_detail.html', context={
            'post': obj,
            'admin_object': obj,
            'detail': True
        })


class PostCreate(LoginRequiredMixin, OblectCreateMixin, View):
    raise_exception = True

    def get(self, request):
        form = PostForm()
        return render(request, 'blog/post_create.html', context={
            'form': form,
        })

    def post(self, request):
        post_form = PostForm(request.POST, request.FILES)

        if post_form.is_valid():
            new_post = post_form.save()
            return redirect(new_post)

        return render(request, 'blog/post_create.html', context={
            'form': post_form,
        })


class PostUpdate(LoginRequiredMixin, View):
    raise_exception = True

    def get(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        bound_form = PostForm(instance=post)

        return render(request, 'blog/post_update_form.html', context={
            'form': bound_form,
            'post': post,
        })

    def post(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        bound_form = PostForm(request.POST, request.FILES, instance=post)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)

        return render(request, 'blog/post_update_form.html', context={
            'form': bound_form,
            'post': post,
        })


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True


def posts_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) |
                                    Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    page, is_paginated = paginator(request, posts)
    return render(request, 'blog/index.html', context={
        'page_object': page,
        'is_paginated': is_paginated
    })


class TagDetail(View):
    def get(self, request, slug):
        obj = get_object_or_404(Tag, slug__iexact=slug)
        posts = obj.posts.all()
        page, is_paginated = paginator(request, posts)
        return render(request, 'blog/index.html', context={
            'detail': True,
            'page_object': page,
            'is_paginated': is_paginated,
            'title': obj.title,
        })


class TagCreate(LoginRequiredMixin, OblectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})
