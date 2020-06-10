from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import TagForm, PostForm
from .models import Post, Tag
from .mixins import *


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


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

    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)
    is_paginated = page.has_other_pages()

    return render(request, 'blog/index.html', context={
        'page_object': page,
        'is_paginated': is_paginated
    })


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


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
