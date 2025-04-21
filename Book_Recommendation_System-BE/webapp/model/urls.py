from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Welcome'),
    path('genres/', views.genres, name='genres'),
    path('top-authors/', views.top_authors, name='top_authors'),
    path('top-book/', views.top_book, name='top_book'),
    path('top-publisher/', views.top_publisher, name='top_publisher'),
    path('secondpage.html/', views.second, name='secondpage'),
]