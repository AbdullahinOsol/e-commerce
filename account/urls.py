from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register', views.register, name='register'),
    path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email-verification'),
    path('email-verification-sent', views.email_verification_sent, name='email-verification-sent'),
    path('email-verification-success', views.email_verification_success, name='email-verification-success'),
    path('email-verification-failed', views.email_verification_failed, name='email-verification-failed'),
    path('my-login', views.my_login, name='my-login'),
    path('my-logout', views.my_logout, name='my-logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile-management', views.profile_management, name='profile-management'),
    path('delete-account', views.delete_account, name='delete-account'),
    path(
        'reset-password',
        auth_views.PasswordResetView.as_view(
            template_name='account/password/reset-password.html',
            extra_context={'page': 'reset-password'}
        ),
        name='reset_password'
    ),
    path('reset-password-sent', auth_views.PasswordResetDoneView.as_view(template_name='account/password/reset-password-sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password/reset-password-confirm.html'), name='password_reset_confirm'),
    path('reset-password-complete', auth_views.PasswordResetCompleteView.as_view(template_name='account/password/reset-password-complete.html'), name='password_reset_complete'),
    path('manage-shipping', views.manage_shipping, name='manage-shipping'),
    path('track-orders', views.track_orders, name='track-orders'),
    path('change-password', views.change_password, name='change-password'),
]
