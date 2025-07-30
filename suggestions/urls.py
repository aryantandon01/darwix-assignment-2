from django.urls import path
from . import views

urlpatterns = [
    path('suggest-titles/', views.suggest_titles, name='suggest_titles'),
]
