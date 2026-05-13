"""
core/urls.py

URL configuration for the core app.
"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('access-denied/', views.access_denied, name='access_denied'),
]
