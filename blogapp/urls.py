# from django.contrib import admin
from django.urls import path
from blogapp import views

urlpatterns = [
    path('register_user/', views.register_user, name="register"),
    path('create_blog/',views.create_blog, name="create_blog"),
    path('list_blog/', views.list_blog, name="list_blog"),
    path('blog_update/<int:pk>',views.blog_update , name= "blog_update"),
    path('blog_delete/<int:pk>/', views.blog_delete, name="blog_delete"),
    path('update_user/',views.update_user_profile, name= "update_profile"),
    path('get_username/', views.get_username, name="get_username"),
    path('blogs/<slug:slug>/',views.get_blog, name="get_blog"),
    path("get_userinfo/<str:username>/", views.get_user_info),
]