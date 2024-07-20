from django.urls import path

from .views import dispatch

urlpatterns = [
    path('dispatch/', dispatch, name='dispatch'),
]
