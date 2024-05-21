from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('home/', views.home, name="home"),
]  
    