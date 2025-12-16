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
    
    # 评分字段（新增）
    score_comfort = models.DecimalField(max_digits=3, decimal_places=1, default=4.0, verbose_name='舒适性评分')
    score_appearance = models.DecimalField(max_digits=3, decimal_places=1, default=4.0, verbose_name='外观评分')
    score_power = models.DecimalField(max_digits=3, decimal_places=1, default=4.0, verbose_name='动力评分')
    score_interior = models.DecimalField(max_digits=3, decimal_places=1, default=4.0, verbose_name='内饰评分')
    score_config = models.DecimalField(max_digits=3, decimal_places=1, default=4.0, verbose_name='配置评分')
    score_space = models.DecimalField(max_digits=3, decimal_places=1, default=4.0, verbose_name='空间评分')
    
    # 车辆参数（新增）
    acceleration = models.CharField(max_length=20, blank=True, null=True, verbose_name='百公里加速(s)')
    max_speed = models.IntegerField(null=True, blank=True, verbose_name='最高车速(km/h)')
    curb_weight = models.CharField(max_length=50, blank=True, null=True, verbose_name='整备质量(kg)')
    drive_type = models.CharField(max_length=20, blank=True, null=True, verbose_name='驱动方式')
    seat_count = models.IntegerField(default=5, verbose_name='座位数')
    wheelbase = models.IntegerField(null=True, blank=True, verbose_name='轴距(mm)')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'car_series'
        verbose_name = '车系'
        verbose_name_plural = '车系'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand.name} - {self.name}"
    
    @property
    def total_score(self):
        """ 计算综合评分 """
        scores = [self.score_comfort, self.score_appearance, self.score_power,
                  self.score_interior, self.score_config, self.score_space]
        return round(sum(float(s) for s in scores) / len(scores), 2)


class CarVersion(models.Model):
    """车型版本"""
    car_series = models.ForeignKey(CarSeries, on_delete=models.CASCADE, related_name='versions', verbose_name='车系')
    name = models.CharField(max_length=100, verbose_name='版本名称')
    year = models.IntegerField(verbose_name='年份')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格(万元)')
    endurance = models.IntegerField(null=True, blank=True, verbose_name='续航(km)')
    is_default = models.BooleanField(default=False, verbose_name='默认版本')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'car_versions'
        verbose_name = '车型版本'
        verbose_name_plural = '车型版本'
        ordering = ['-year', 'price']

    def __str__(self):
        return f"{self.car_series.name} - {self.year}款 {self.name}"


class CarColor(models.Model):
    """车身颜色"""
    car_series = models.ForeignKey(CarSeries, on_delete=models.CASCADE, related_name='colors', verbose_name='车系')
    name = models.CharField(max_length=50, verbose_name='颜色名称')
    color_code = models.CharField(max_length=20, verbose_name='颜色代码')
    image = models.CharField(max_length=500, blank=True, null=True, verbose_name='该颜色车辆图片')
    is_default = models.BooleanField(default=False, verbose_name='默认颜色')

    class Meta:
        db_table = 'car_colors'
        verbose_name = '车身颜色'
        verbose_name_plural = '车身颜色'

    def __str__(self):
        return f"{self.car_series.name} - {self.name}"


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
    
    CATEGORY_CHOICES = [
        ('quality', '质量问题'),
        ('service', '服务问题'),
        ('other', '其他问题'),
    ]
    
    car_series = models.ForeignKey(CarSeries, on_delete=models.CASCADE, related_name='issues', verbose_name='车系')
    issue_type = models.CharField(max_length=100, verbose_name='问题类型')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='quality', verbose_name='问题分类')
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
