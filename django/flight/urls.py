from django.urls import path

from . import views

urlpatterns = [
    path('dispatch/', views.dispatch, name='dispatch'),
    path('flight_list/', views.flight_list, name='flight_list'),
    path('flight/<str:flt_number>/', views.FlightDetail.as_view(), name='flight'),
]
