from django.db import models
from django.utils import timezone  # 用于处理时间

# 1. 汽车信息模型（存储汽车基本信息）
class Car(models.Model):
    brand = models.CharField(max_length=50, verbose_name="品牌")  # 如“特斯拉”
    series = models.CharField(max_length=100, verbose_name="车系")  # 如“Model 3”
    fuel_type = models.CharField(max_length=20, verbose_name="燃料类型")  # 如“纯电动”
    seats = models.IntegerField(verbose_name="座位数")  # 如5
    car_type = models.CharField(max_length=50, verbose_name="车型")  # 如“紧凑型车”
    official_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="厂商报价(万)")  # 如23.19
    dealer_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="经销商报价(万)")  # 如22.59
    # 六个维度评分（0-10分）
    comfort_score = models.FloatField(verbose_name="舒适性评分")
    appearance_score = models.FloatField(verbose_name="外观评分")
    config_score = models.FloatField(verbose_name="配置评分")
    control_score = models.FloatField(verbose_name="操控评分")
    power_score = models.FloatField(verbose_name="动力评分")
    space_score = models.FloatField(verbose_name="空间评分")
    interior_score = models.FloatField(verbose_name="内饰评分")
    total_score = models.FloatField(verbose_name="总分")  # 六个维度的平均分
    image_urls = models.TextField(verbose_name="外观图片链接")  # 多个链接用逗号分隔
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return f"{self.brand} {self.series}"  # 显示“品牌 车系”

    class Meta:
        verbose_name = "汽车信息"
        verbose_name_plural = "汽车信息"


# 2. 销量模型（关联汽车，记录每月销量）
class Sales(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="sales", verbose_name="关联汽车")  # 外键关联Car
    year_month = models.CharField(max_length=7, verbose_name="年月")  # 格式：2025-10
    sales_volume = models.IntegerField(verbose_name="销量(辆)")  # 当月销量
    rank = models.IntegerField(verbose_name="当月排名")  # 当月销量排名
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")

    def __str__(self):
        return f"{self.car.brand} {self.car.series} {self.year_month}销量"

    class Meta:
        verbose_name = "销量数据"
        verbose_name_plural = "销量数据"
        unique_together = ("car", "year_month")  # 同一汽车同一月份只能有一条数据


# 3. 投诉模型（关联汽车，记录投诉信息）
class Complaint(models.Model):
    COMPLAINT_TYPES = (
        ("质量问题", "质量问题"),
        ("服务问题", "服务问题"),
        ("其他问题", "其他问题"),
    )  # 投诉类型选项
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="complaints", verbose_name="关联汽车")  # 外键关联Car
    complaint_type = models.CharField(max_length=20, choices=COMPLAINT_TYPES, verbose_name="问题类型")
    content = models.TextField(verbose_name="投诉内容")
    complaint_time = models.DateField(verbose_name="投诉时间")  # 格式：2025-10-01
    tags = models.CharField(max_length=200, verbose_name="投诉标签")  # 多个标签用逗号分隔，如“续航缩水,车机卡顿”
    create_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")

    def __str__(self):
        return f"{self.car.brand} {self.car.series} {self.complaint_type}"

    class Meta:
        verbose_name = "投诉数据"
        verbose_name_plural = "投诉数据"