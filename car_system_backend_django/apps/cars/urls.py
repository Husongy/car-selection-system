"""
汽车模块 URL 配置
"""
from django.urls import path
from . import views

urlpatterns = [
    path('sales-rank/', views.car_sales_rank, name='car_sales_rank'),
    path('issue-rank/', views.car_issue_rank, name='car_issue_rank'),
    path('detail/', views.get_detail, name='get_detail'),
    path('analysis/', views.car_series_analysis, name='car_series_analysis'),
    path('filter/', views.filter_cars, name='filter_cars'),
    path('brands/', views.brand_list, name='brand_list'),
]
