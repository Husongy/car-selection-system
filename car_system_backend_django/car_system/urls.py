"""
URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cars/', include('apps.cars.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/analysis/', include('apps.analysis.urls')),
]