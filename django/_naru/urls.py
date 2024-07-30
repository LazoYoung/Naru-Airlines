from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('member.urls')),
    path('api/', include('flight.urls')),
    path('api/', include('passenger.urls')),
]
