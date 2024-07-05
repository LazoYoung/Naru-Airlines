from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework import routers

from . import views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
#
# urlpatterns = [
#     path(r'', include(router.urls)),
#     path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
# ]

