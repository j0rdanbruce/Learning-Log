"""URL patterns for the users application"""

from . import views
from django.urls import path, include

app_name = 'users'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]

















