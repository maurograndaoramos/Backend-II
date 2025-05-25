from django.urls import path
from .views import secure_input_view

urlpatterns = [
    path('secure-input/', secure_input_view, name='secure_input'),
]