from django.urls import path

from .views import (
    login, logout, register,
    send_register_email, verify_account,
    change_password, reset_password, profile, SendVerificationEmail, verify_change_email, verify_reset_password,
)

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('send-verify-email/', SendVerificationEmail.as_view(), name='send_verify_email'),
    path('verify-account/<str:uid>/<str:token>/', verify_account, name='verify_account'),
    path('reset-password/<str:uid>/<str:token>/', verify_reset_password, name='verify_reset_password'),
    path('change-email/<str:uid>/<str:token>/', verify_change_email, name='verify_change_email'),
    path('change-password/', change_password, name='change_password'),
    path('profile/', profile, name='profile'),

    # deprecated endpoints
    path('send-register-email/', send_register_email, name='send_register_email'),
    path('reset-password/', reset_password, name='reset_password'),
]
