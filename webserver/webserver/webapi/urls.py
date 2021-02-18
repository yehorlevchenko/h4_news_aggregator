from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news, name='news'),
    path('start/', views.start, name='start'),
]
