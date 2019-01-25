from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.blogs_list, name = 'blogs_list'),
    path('blog_detail/<int:blog_id>/', views.blog_detail, name= 'blog_detail'),
    path('blog_detail/<int:blog_id>/post_detail/<int:post_id>/', views.post_detail, name= 'post_detail'),
    path('registration/', views.registration, name= 'registration'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('create_new_blog/', views.create_new_blog, name= 'create_new_blog'),
    path('blog_detail/<int:blog_id>/create_new_post/', views.create_new_post, name= 'create_new_post'),
    path('blog_detail/<int:blog_id>/post_detail/<int:post_id>/create_new_comment/', views.create_new_comment, name= 'create_new_comment'),



]
