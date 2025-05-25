import pytest
from rest_framework import status
from rest_framework.test import APIClient
from myapp.models import BlogPost

@pytest.mark.django_db
def test_blog_post_list():
    client = APIClient()
    # Create two BlogPost instances
    BlogPost.objects.create(title="Test Title 1", content="Test Content 1")
    BlogPost.objects.create(title="Test Title 2", content="Test Content 2")

    # Make a GET request to the API endpoint
    response = client.get('/api/blogposts/')
    
    # Assert the response status code and data
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert response.data[0]['title'] == "Test Title 1"
    assert response.data[1]['title'] == "Test Title 2"