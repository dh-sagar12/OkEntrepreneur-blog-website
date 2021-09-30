
from django.urls import  path 
from blog import views
  
urlpatterns = [
    #API's for handle comment in blogs
    path('postComment/', views.postComment, name= 'postComment'),

    path('', views.blogHome, name='blogHome'),
    path('search/', views.search, name='search'),
    path('<str:slug>', views.blogPost, name='blogpost'),
    path('viewall/<str:str>', views.trendingPopular, name = 'trendingPopular')
]
 