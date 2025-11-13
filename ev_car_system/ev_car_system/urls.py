from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

# 首页视图函数，渲染 home.html 模板
def home(request):
    return render(request, 'home.html')

urlpatterns = [
    # 首页路由：访问根路径时渲染 home.html
  #  path('', home, name='home'),
    # Django 后台管理路由
    path('admin/', admin.site.urls),
    # API 接口路由：所有汽车相关的接口都在 cars.urls 中配置
    path('api/', include('cars.urls')),
]