from django.urls import path
from .views import home, post_detail, search

urlpatterns = {
    path('', home, name='home'),
    path('post/<int:post_id>/', post_detail, name='post_detail'),
    path('search/', search, name='search'),
}