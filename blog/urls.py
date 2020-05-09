from django.urls import path

from .views import *


urlpatterns = [
    path('', posts_list, name='posts_list_url'),
    path('post/<slug>/', PostDetail.as_view(), name='post_detail_url'),
    path('tags/', tags_list, name='tags_list_url'),
    path('tag/create/', TagCreate.as_view(), name='tag_create_url'),
    path('tag/<slug>/', TagDetail.as_view(), name='tag_detail_url'),
]
