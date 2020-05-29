from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import formset_factory
from django.forms.models import modelformset_factory

from .forms import TagForm, PostForm, ImageForm
from .models import Post, Tag, Images
from .mixins import *


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, OblectCreateMixin, View):
    ImageFormSet = formset_factory(ImageForm, extra=5)
    raise_exception = True

    def get(self, request):
        form = PostForm()
        image_formset = self.ImageFormSet()
        return render(request, 'blog/post_create.html', context={
            'form': form,
            'formset': image_formset
        })

    def post(self, request):
        post_form = PostForm(request.POST, request.FILES)
        image_formset = self.ImageFormSet(request.POST, request.FILES)

        if post_form.is_valid() and image_formset.is_valid():
            new_post = post_form.save()

            for form in image_formset.cleaned_data:
                if form.get('image'):
                    name = form['name']
                    image = form['image']
                    Images.objects.create(name=name, post=new_post, image=image)

            new_post.replace_number_on_url()

            return redirect(new_post)

        return render(request, 'blog/post_create.html', context={
            'form': post_form,
            'formset': image_formset
        })


class PostUpdate(LoginRequiredMixin, View):
    raise_exception = True
    ImageModelFormSet = modelformset_factory(Images, form=ImageForm,
                                             fields={'name', 'image'}, extra=3)

    def get(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        post.replace_url_on_number()
        bound_form = PostForm(instance=post)
        post_images = self.ImageModelFormSet(queryset=post.images_set.all())

        return render(request, 'blog/post_update_form.html', context={
            'form': bound_form,
            'post': post,
            'modelformset': post_images
        })

    def post(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        bound_form = PostForm(request.POST, request.FILES, instance=post)
        post_images = self.ImageModelFormSet(request.POST, request.FILES,
                                             queryset=post.images_set.all())

        if post_images.is_valid():
            for form in post_images.cleaned_data:
                obj = form.get('id')
                if obj:
                    obj.image = form.get('image')
                    obj.save()

                elif not obj and form.get('image'):
                    name = form['name']
                    image = form['image']
                    Images.objects.create(name=name, post=post, image=image)

            post.replace_number_on_url()

            if bound_form.is_valid():
                post.replace_number_on_url()
                new_obj = bound_form.save()
                return redirect(new_obj)

        return render(request, 'blog/post_update_form.html', context={
            'form': bound_form,
            'post': post,
            'modelformset': post_images
        })


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True


class ImageDelete(View):
    def get(self, request, id):
        image = Images.objects.get(id=id)
        return render(request, 'blog/image_delete.html', context={'image': image})

    def post(self, request, id):
        image = Images.objects.get(id=id)
        post = image.post
        image.delete()
        return redirect(reverse('post_update_url', kwargs={'slug': post.slug}))


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
