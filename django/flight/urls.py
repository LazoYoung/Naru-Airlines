from django.urls import path

from . import views

urlpatterns = [
    path('dispatch/charter/', views.dispatch_charter, name='dispatch_charter'),
    path('dispatch/routine/', views.dispatch_routine, name='dispatch_routine'),
    path('schedule/', views.SchedulesAPI.as_view(), name='schedules'),
    path('schedule/<str:flight_number>/', views.ScheduleAPI.as_view(), name='schedule'),
    path('route/', views.RoutesAPI.as_view(), name='routes'),
    path('route/<str:flight_number>/', views.RouteAPI.as_view(), name='route'),
    path('fleet/', views.FleetAPI.as_view(), name='fleet'),
    path('fleet/<str:icao_code>/', views.AircraftAPI.as_view(), name='aircraft'),
]
