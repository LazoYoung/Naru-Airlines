from django.urls import path

from . import views

urlpatterns = [
    path('dispatch/charter/', views.dispatch_charter, name='dispatch_charter'),
    path('dispatch/standard/', views.dispatch_standard, name='dispatch_standard'),
    path('schedules/', views.schedules, name='schedules'),
    path('schedule/<str:flight_number>/', views.ScheduleAPI.as_view(), name='schedule'),
    path('routes/', views.routes, name='routes'),
    path('route/', views.RouteAPI.as_view(), name='route'),
    path('route/<str:flight_number>/', views.RouteAPI.as_view(), name='route'),
    path('fleet/profiles/', views.fleet_profiles, name='fleet_profiles'),
    path('fleet/aircraft/', views.AircraftAPI.as_view(), name='fleet_aircraft'),
    path('fleet/aircraft/<str:icao_code>/', views.AircraftAPI.as_view(), name='fleet_aircraft'),
]
