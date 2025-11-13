from django.contrib import admin
from .models import Car, Sales, Complaint

# 注册汽车模型
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("brand", "series", "fuel_type", "official_price", "total_score", "create_time")  # 列表页显示的字段
    search_fields = ("brand", "series")  # 可搜索的字段
    list_filter = ("fuel_type", "car_type")  # 可筛选的字段

# 注册销量模型
@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ("car", "year_month", "sales_volume", "rank")
    search_fields = ("car__brand", "car__series")  # 按汽车品牌/车系搜索
    list_filter = ("year_month",)

# 注册投诉模型
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ("car", "complaint_type", "complaint_time", "tags")
    search_fields = ("car__brand", "car__series", "content")
    list_filter = ("complaint_type", "complaint_time")