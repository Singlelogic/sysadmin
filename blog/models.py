from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time
from PIL import Image


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    body = models.TextField(blank=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    date_pub = models.DateTimeField(auto_now_add=True)
    image_preview = models.ImageField(upload_to='images/')

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def replace_number_on_url(self):
        for image in self.images_set.all():
            self.body = self.body.replace(
                f'/*{image.name}*/',
                f'<img src="{image.image.url}">'
            )

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

        if self.image_preview:
            filepath = self.image_preview.path
            width = self.image_preview.width
            height = self.image_preview.height
            max_size = max(width, height)

            if max_size > 200:
                image = Image.open(filepath)
                image = image.resize(
                    (round(width / max_size * 200),
                     round(height / max_size * 200)),
                    Image.ANTIALIAS
                )
                image.save(filepath)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_pub']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)


class Images(models.Model):
    name = models.CharField(blank=True, max_length=20)
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image')

    def __str__(self):
        return "%s - %s" % (self.post.title, self.name)
