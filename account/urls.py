# Django Built-in modules
from django.urls import path
# Locals apps
from . import views

app_name = 'account'

urlpatterns = [
    # logout
    path('logout/', views.logout, name='logout'),
    # login
    path('login/', views.user_login, name='login'),
    # register
    path('users/register/', views.user_register, name='user_register'),
    path('users/register/verify/', views.user_register_verify, name='user_register_verify'),
    path('users/register/complete/', views.user_register_complete, name='user_register_complete'),
    # forgot password
    path('users/forgot_password/', views.user_forgot_password, name='user_forgot_password'),
    path('users/forgot_password/verify/', views.user_forgot_password_verify, name='user_forgot_password_verify'),
    path('users/forgot_password/complete/', views.user_forgot_password_complete, name='user_forgot_password_complete'),
    # resend code
    path('resend_code/', views.resend_verification_code, name='user_resend_verification_code'),
    # dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    # prodile
    path('profile/', views.profile, name='profile'),
    # change password
    path('change_password/', views.change_password, name='change_password'),
    # bookmark
    path('bookmark/', views.bookmark, name='bookmark'),
    path('bookmark/remove/<post_id>/', views.bookmark_remove, name='bookmark_remove'),
]
