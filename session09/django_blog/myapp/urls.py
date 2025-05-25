from django.urls import path
from myapp.views import BlogPostList

urlpatterns = [
    path('api/blogposts/', BlogPostList.as_view(), name='blogpost-list'),
]