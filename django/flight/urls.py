from django.urls import path

from . import views

urlpatterns = [
    path('dispatch/', views.dispatch, name='dispatch'),
    path('schedules/', views.schedules, name='schedules'),
    path('schedule/<str:flt_number>/', views.ScheduleAPI.as_view(), name='schedule'),
]
