from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('rules/', views.rules, name='rules'),
    path('search/', views.search, name='search'),
    path('orm-demo/', views.orm_demo, name='orm_demo'),

    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:post_id>/comment/', views.comment_create, name='comment_create'),

    path('category/create/', views.category_create, name='category_create'),
]