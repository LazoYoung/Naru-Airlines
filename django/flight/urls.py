from django.urls import path

from . import views

urlpatterns = [
    path('dispatch/charter/', views.dispatch_charter, name='dispatch_charter'),
    path('dispatch/standard/', views.dispatch_standard, name='dispatch_standard'),
    path('schedule/', views.ScheduleAPI.as_view(), name='schedule'),
    path('route/', views.RouteAPI.as_view(), name='route'),
    path('fleet/', views.FleetAPI.as_view(), name='fleet'),
]
