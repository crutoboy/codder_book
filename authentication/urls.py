from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('signin/', views.signin, name='login'),
    path('signup/', views.signup, name='register'),
    path('logout/', views.logout_, name='logout'),
]
