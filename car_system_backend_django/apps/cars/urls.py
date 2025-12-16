"""
汽车模块 URL 配置
"""
from django.urls import path
from . import views

urlpatterns = [
    # POST API (原有的Django项目 API)
    path('sales-rank/', views.car_sales_rank, name='car_sales_rank'),
    path('issue-rank/', views.car_issue_rank, name='car_issue_rank'),
    path('bad-review-rank/', views.bad_review_rank, name='bad_review_rank'),  # 差评榜单
    path('detail/', views.get_detail, name='get_detail'),
    path('analysis/', views.car_series_analysis, name='car_series_analysis'),
    path('filter/', views.filter_cars, name='filter_cars'),
    path('brands/', views.brand_list, name='brand_list'),
    
    # 可视化分析API
    path('analysis/price-discount/', views.price_discount_ranking, name='price_discount_ranking'),
    path('analysis/brand-count/', views.brand_count_distribution, name='brand_count_distribution'),
    path('analysis/price-range/', views.price_range_distribution, name='price_range_distribution'),
    
    # GET API (RESTful API)
    path('v1/cars', views.get_cars_list, name='get_cars_list'),
    path('v1/cars/filters', views.get_filter_options, name='get_filter_options'),
    
    # 车系详情API
    path('detail-full/', views.car_detail_full, name='car_detail_full'),
    path('list-simple/', views.car_list_simple, name='car_list_simple'),
]
