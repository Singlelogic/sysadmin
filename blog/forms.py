from django import forms
from django.core.exceptions import ValidationError
from django_summernote.widgets import SummernoteWidget

from .models import Tag, Post, Images


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('We have "{}" slug already'.format(new_slug))
        return new_slug


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'image_preview', 'tags', 'body']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': SummernoteWidget(),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        if Post.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('We have "{}" slug already'.format(new_slug))
        return new_slug


class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['name', 'image']

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control'})
    }