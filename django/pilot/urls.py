from django.urls.conf import path

from . import views

urlpatterns = [
    path('pilot/stats/', views.stats, name='stats'),
]
