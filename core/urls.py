from django.urls import path
from . import views

urlpatterns = [
    path('yorumlar/', views.comments_view, name='comments'),
]
