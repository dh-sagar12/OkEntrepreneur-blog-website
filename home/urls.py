from django.contrib import admin
from django.urls import include, path 
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('signup/', views.userHandling, name='userHandling'),
    path('login/', views.loginHandeling, name='userHandling'),
    path('logout/', views.logoutHandeling, name='userHandling'),
    
]
