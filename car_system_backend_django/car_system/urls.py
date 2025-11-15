"""
URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from apps.cars import views as car_views

# 根路径重定向到前端
def redirect_to_frontend(request):
    """重定向到前端首页"""
    return HttpResponseRedirect('http://localhost:5173')

urlpatterns = [
    # 根路径重定向到前端
    path('', redirect_to_frontend, name='home'),
    
    path('admin/', admin.site.urls),
    
    # Django 项目的 API
    path('api/cars/', include('apps.cars.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/analysis/', include('apps.analysis.urls')),
    
    # 品牌接口 (GET)
    path('api/v1/brands', car_views.get_brands_list, name='api_brands'),
    
    # 统计接口 (GET)
    path('api/v1/statistics', car_views.get_statistics, name='api_statistics'),
]
