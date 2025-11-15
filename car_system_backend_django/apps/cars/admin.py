from django.contrib import admin
from .models import Brand, CarSeries, CarSale, CarIssue


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'created_at')
    search_fields = ('name',)


@admin.register(CarSeries)
class CarSeriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'fuel_type', 'price_min', 'price_max', 'created_at')
    list_filter = ('brand', 'fuel_type', 'body_type')
    search_fields = ('name',)


@admin.register(CarSale)
class CarSaleAdmin(admin.ModelAdmin):
    list_display = ('car_series', 'month', 'sales')
    list_filter = ('month',)
    search_fields = ('car_series__name',)


@admin.register(CarIssue)
class CarIssueAdmin(admin.ModelAdmin):
    list_display = ('car_series', 'issue_type', 'severity', 'report_count', 'created_at')
    list_filter = ('issue_type', 'severity')
    search_fields = ('car_series__name', 'issue_type')
