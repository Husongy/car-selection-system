"""
汽车数据模型
支持销量排行、质量问题、条件选车等功能
"""
from django.db import models


class Brand(models.Model):
    """汽车品牌"""
    name = models.CharField(max_length=100, unique=True, verbose_name='品牌名称')
    logo = models.CharField(max_length=500, blank=True, null=True, verbose_name='品牌Logo')
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name='国家')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'brands'
        verbose_name = '品牌'
        verbose_name_plural = '品牌'
        ordering = ['name']

    def __str__(self):
        return self.name


class CarSeries(models.Model):
    """车系（核心模型）"""
    FUEL_TYPE_CHOICES = [
        ('BEV', '纯电动'),
        ('PHEV', '插电混动'),
        ('HEV', '混合动力'),
    ]
    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='series', verbose_name='品牌')
    name = models.CharField(max_length=100, verbose_name='车系名称')
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPE_CHOICES, default='BEV', verbose_name='能源类型')
    
    # 价格区间
    price_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='最低价格(万元)')
    price_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='最高价格(万元)')
    
    # 续航里程
    endurance_min = models.IntegerField(null=True, blank=True, verbose_name='最低续航(km)')
    endurance_max = models.IntegerField(null=True, blank=True, verbose_name='最高续航(km)')
    
    # 车身类型
    body_type = models.CharField(max_length=50, blank=True, null=True, verbose_name='车身类型')
    
    # 其他信息
    image = models.CharField(max_length=500, blank=True, null=True, verbose_name='车系图片')
    description = models.TextField(blank=True, null=True, verbose_name='车系描述')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'car_series'
        verbose_name = '车系'
        verbose_name_plural = '车系'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand.name} - {self.name}"


class CarSale(models.Model):
    """车系销量数据"""
    car_series = models.ForeignKey(CarSeries, on_delete=models.CASCADE, related_name='sales', verbose_name='车系')
    month = models.CharField(max_length=7, verbose_name='月份(格式: 2024-01)')
    sales = models.IntegerField(default=0, verbose_name='销量')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'car_sales'
        verbose_name = '销量数据'
        verbose_name_plural = '销量数据'
        ordering = ['-month', '-sales']
        unique_together = [['car_series', 'month']]

    def __str__(self):
        return f"{self.car_series.name} - {self.month}: {self.sales}"


class CarIssue(models.Model):
    """车系质量问题"""
    SEVERITY_CHOICES = [
        ('low', '轻微'),
        ('medium', '中等'),
        ('high', '严重'),
    ]
    
    car_series = models.ForeignKey(CarSeries, on_delete=models.CASCADE, related_name='issues', verbose_name='车系')
    issue_type = models.CharField(max_length=100, verbose_name='问题类型')
    description = models.TextField(blank=True, null=True, verbose_name='问题描述')
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='medium', verbose_name='严重程度')
    report_count = models.IntegerField(default=1, verbose_name='投诉次数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='上报时间')

    class Meta:
        db_table = 'car_issues'
        verbose_name = '质量问题'
        verbose_name_plural = '质量问题'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.car_series.name} - {self.issue_type}"
