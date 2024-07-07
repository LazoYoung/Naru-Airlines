from django.urls import path

from .views import (
    login, logout, register,
    send_register_email, verify_register_email,
    change_password, reset_password,
)

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('register/send-email', send_register_email, name='send_register_email'),
    path('register/verify-email/<str:uid>/<str:token>', verify_register_email, name='verify_register_email'),
    path('change-password', change_password, name='change_password'),
    path('reset-password', reset_password, name='reset_password'),
]
