import pytest
from myapp.models import BlogPost

@pytest.mark.django_db
def test_blog_post_creation():
    post = BlogPost.objects.create(title="Test Title", content="Test Content")
    assert post.title == "Test Title"
    assert post.content == "Test Content"
    assert post.published_date is not None