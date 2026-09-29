from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('rules/', views.rules, name='rules'),
    path('search/', views.search, name='search'),

    path('posts/', views.post_list, name='post_list'),
    path('category/<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    path('categories/', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/<int:category_id>/edit/', views.category_update, name='category_update'),
    path('category/<int:category_id>/delete/', views.category_delete, name='category_delete'),

    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:post_id>/edit/', views.post_update, name='post_update'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),

    path('post/<int:post_id>/comment/', views.comment_create, name='comment_create'),
    path('comment/<int:comment_id>/edit/', views.comment_update, name='comment_update'),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),

    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('my-posts/', views.my_posts, name='my_posts'),

    path('confirm-email/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
    path('registration-pending/', views.registration_pending, name='registration_pending'),
    path('resend-confirmation/', views.resend_confirmation, name='resend_confirmation'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='blog/password_reset_form.html',
        email_template_name='blog/password_reset_email.html',
        success_url='/blog/password-reset/done/'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='blog/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='blog/password_reset_confirm.html',
        success_url='/blog/reset/done/'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='blog/password_reset_complete.html'
    ), name='password_reset_complete'),
]