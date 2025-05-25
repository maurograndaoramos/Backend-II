# Create your views here.
from rest_framework import generics
from myapp.models import BlogPost
from myapp.serializers import BlogPostSerializer

class BlogPostList(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer