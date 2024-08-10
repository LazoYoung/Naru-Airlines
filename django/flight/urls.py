from django.urls import path

from . import views

urlpatterns = [
    path('dispatch/charter/', views.dispatch_charter, name='dispatch_charter'),
    path('schedules/', views.schedules, name='schedules'),
    path('schedule/<str:flight_number>/', views.ScheduleAPI.as_view(), name='schedule'),
    path('fleet/all/', views.fleet_all, name='fleet_all'),
    path('fleet/aircraft/', views.AircraftAPI.as_view(), name='fleet_aircraft'),
    path('fleet/aircraft/<str:icao_code>/', views.AircraftAPI.as_view(), name='fleet_aircraft'),
]
