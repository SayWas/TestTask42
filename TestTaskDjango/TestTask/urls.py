from django.urls import path

from .views import (
    fetch_users
)

urlpatterns = [
    path('fetch_users/', fetch_users, name='fetch_users'),
]
