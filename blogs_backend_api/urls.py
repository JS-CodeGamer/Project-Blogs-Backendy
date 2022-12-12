from django.urls import path
from . import views

urlpatterns = [
    path('root/', views.allBlogs),
    path('create/', views.newBlog),
    path('blog/<int:pk>', views.blog),
    path('blogs/', views.blogsList),
    path('blogs/u/', views.blogsList),
    path('blogs/u/<str:pk>', views.blogsListUser),
]
