#!/usr/bin/env python
"""
初始化真实新能源汽车数据
数据来源：公开的新能源汽车基础信息
"""
import os
import sys
import django
import random
from datetime import datetime, timedelta

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_system.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.cars.models import Brand, CarSeries, CarSale, CarIssue, CarVersion, CarColor

# 真实新能源汽车数据（基于公开信息）
REAL_CAR_DATA = [
    # 比亚迪
    {
        'brand': '比亚迪', 'country': '中国',
        'cars': [
            {'name': '秦PLUS DM-i', 'fuel_type': 'PHEV', 'body_type': '轿车', 'price_min': 9.98, 'price_max': 14.58, 'endurance_min': 55, 'endurance_max': 120, 'seat_count': 5, 'acceleration': '7.3', 'max_speed': 185, 'wheelbase': 2718},
            {'name': '海豚', 'fuel_type': 'BEV', 'body_type': '两厢车', 'price_min': 9.68, 'price_max': 13.68, 'endurance_min': 301, 'endurance_max': 405, 'seat_count': 5, 'acceleration': '7.0', 'max_speed': 160, 'wheelbase': 2700},
            {'name': '汉EV', 'fuel_type': 'BEV', 'body_type': '轿车', 'price_min': 20.98, 'price_max': 32.98, 'endurance_min': 506, 'endurance_max': 715, 'seat_count': 5, 'acceleration': '3.9', 'max_speed': 200, 'wheelbase': 2920},
            {'name': '宋PLUS DM-i', 'fuel_type': 'PHEV', 'body_type': 'SUV', 'price_min': 14.98, 'price_max': 21.98, 'endurance_min': 51, 'endurance_max': 110, 'seat_count': 5, 'acceleration': '7.9', 'max_speed': 180, 'wheelbase': 2765},
            {'name': '海豹', 'fuel_type': 'BEV', 'body_type': '轿车', 'price_min': 17.98, 'price_max': 27.98, 'endurance_min': 550, 'endurance_max': 700, 'seat_count': 5, 'acceleration': '3.8', 'max_speed': 210, 'wheelbase': 2920},
            {'name': '元PLUS', 'fuel_type': 'BEV', 'body_type': 'SUV', 'price_min': 11.98, 'price_max': 15.98, 'endurance_min': 430, 'endurance_max': 510, 'seat_count': 5, 'acceleration': '7.3', 'max_speed': 160, 'wheelbase': 2720},
            {'name': '唐DM-i', 'fuel_type': 'PHEV', 'body_type': 'SUV', 'price_min': 20.98, 'price_max': 28.98, 'endurance_min': 52, 'endurance_max': 215, 'seat_count': 7, 'acceleration': '4.3', 'max_speed': 190, 'wheelbase': 2820},
        ]
    },
    # 特斯拉
    {
        'brand': '特斯拉', 'country': '美国',
        'cars': [
            {'name': 'Model Y', 'fuel_type': 'BEV', 'body_type': 'SUV', 'price_min': 26.39, 'price_max': 36.39, 'endurance_min': 545, 'endurance_max': 660, 'seat_count': 5, 'acceleration': '3.7', 'max_speed': 250, 'wheelbase': 2890},
            {'name': 'Model 3', 'fuel_type': 'BEV', 'body_type': '轿车', 'price_min': 23.19, 'price_max': 33.19, 'endurance_min': 556, 'endurance_max': 713, 'seat_count': 5, 'acceleration': '3.3', 'max_speed': 261, 'wheelbase': 2875},
        ]
    },
    # 理想
    {
        'brand': '理想', 'country': '中国',
        'cars': [
            {'name': '理想L9', 'fuel_type': 'PHEV', 'body_type': 'SUV', 'price_min': 42.98, 'price_max': 45.98, 'endurance_min': 180, 'endurance_max': 215, 'seat_count': 6, 'acceleration': '5.3', 'max_speed': 180, 'wheelbase': 3105},
            {'name': '理想L8', 'fuel_type': 'PHEV', 'body_type': 'SUV', 'price_min': 33.98, 'price_max': 39.98, 'endurance_min': 175, 'endurance_max': 210, 'seat_count': 6, 'acceleration': '5.5', 'max_speed': 180, 'wheelbase': 3005},
            {'name': '理想L7', 'fuel_type': 'PHEV', 'body_type': 'SUV', 'price_min': 31.98, 'price_max': 37.98, 'endurance_min': 175, 'endurance_max': 210, 'seat_count': 5, 'acceleration': '5.3', 'max_speed': 180, 'wheelbase': 2998},
            {'name': '理想MEGA', 'fuel_type': 'BEV', 'body_type': 'MPV', 'price_min': 55.98, 'price_max': 55.98, 'endurance_min': 710, 'endurance_max': 710, 'seat_count': 6, 'acceleration': '5.5', 'max_speed': 190, 'wheelbase': 3300},
        ]
    },
    # 蔚来
    {
        'brand': '蔚来', 'country': '中国',
        'cars': [
            {'name': 'ES6', 'fuel_type': 'BEV', 'body_type': 'SUV', 'price_min': 33.80, 'price_max': 42.60, 'endurance_min': 490, 'endurance_max': 625, 'seat_count': 5, 'acceleration': '4.5', 'max_speed': 200, 'wheelbase': 2915},
            {'name': 'ET5', 'fuel_type': 'BEV', 'body_type': '轿车', 'price_min': 29.80, 'price_max': 35.60, 'endurance_min': 560, 'endurance_max': 700, 'seat_count': 5, 'acceleration': '4.0', 'max_speed': 200, 'wheelbase': 2888},
            {'name': 'EC6', 'fuel_type': 'BEV', 'body_type': 'SUV', 'price_min': 35.80, 'price_max': 52.60, 'endurance_min': 475, 'endurance_max': 615, 'seat_count': 5, 'acceleration': '4.5', 'max_speed': 200, 'wheelbase': 2915},
            {'name': 'ES8', 'fuel_type': 'BEV', 'body_type': 'SUV', 'price_min': 46.80, 'price_max': 62.60, 'endurance_min': 465, 'endurance_max': 605, 'seat_count': 7, 'acceleration': '4.1', 'max_speed': 200, 'wheelbase': 3070},
        ]
    },
    # 小鹏
    {
        'brand': '小鹏', 'country': '中国',
        'cars': [
            {'name': 'P7', 'fuel_type': 'BEV', 'body_type': '轿车', 'price_min': 20.99, 'price_max': 33.99, 'endurance_min': 480, 'endurance_max': 706, 'seat_count': 5, 'acceleration': '4.1', 'max_speed': 200, 'wheelbase': 2998},
            {'name': 'G9', 'fuel_type': 'BEV', 'body_type': 'SUV', 'price_min': 26.39, 'price_max': 35.99, 'endurance_min': 520, 'endurance_max': 702, 'seat_count': 5, 'acceleration': '3.9', 'max_speed': 200, 'wheelbase': 2998},
            {'name': 'G6', 'fuel_type': 'BEV', 'body_type': 'SUV', 'price_min': 20.99, 'price_max': 27.69, 'endurance_min': 530, 'endurance_max': 755, 'seat_count': 5, 'acceleration': '3.9', 'max_speed': 200, 'wheelbase': 2890},
            {'name': 'P5', 'fuel_type': 'BEV', 'body_type': '轿车', 'price_min': 15.69, 'price_max': 22.39, 'endurance_min': 460, 'endurance_max': 600, 'seat_count': 5, 'acceleration': '7.5', 'max_speed': 170, 'wheelbase': 2768},
        ]
    },
    # 问界
    {
        'brand': '问界', 'country': '中国',
        'cars': [
            {'name': '问界M7', 'fuel_type': 'PHEV', 'body_type': 'SUV', 'price_min': 24.98, 'price_max': 32.98, 'endurance_min': 175, 'endurance_max': 240, 'seat_count': 6, 'acceleration': '4.8', 'max_speed': 190, 'wheelbase': 2880},
            {'name': '问界M5', 'fuel_type': 'PHEV', 'body_type': 'SUV', 'price_min': 25.98, 'price_max': 33.98, 'endurance_min': 150, 'endurance_max': 255, 'seat_count': 5, 'acceleration': '4.4', 'max_speed': 200, 'wheelbase': 2880},
            {'name': '问界M9', 'fuel_type': 'PHEV', 'body_type': 'SUV', 'price_min': 46.98, 'price_max': 56.98, 'endurance_min': 180, 'endurance_max': 275, 'seat_count': 6, 'acceleration': '4.3', 'max_speed': 200, 'wheelbase': 3110},
        ]
    },
    # 极氪
    {
        'brand': '极氪', 'country': '中国',
        'cars': [
            {'name': '极氪001', 'fuel_type': 'BEV', 'body_type': '猎装轿跑', 'price_min': 26.90, 'price_max': 36.80, 'endurance_min': 546, 'endurance_max': 741, 'seat_count': 5, 'acceleration': '3.8', 'max_speed': 200, 'wheelbase': 3005},
            {'name': '极氪009', 'fuel_type': 'BEV', 'body_type': 'MPV', 'price_min': 49.90, 'price_max': 58.80, 'endurance_min': 702, 'endurance_max': 822, 'seat_count': 6, 'acceleration': '4.5', 'max_speed': 190, 'wheelbase': 3205},
            {'name': '极氪X', 'fuel_type': 'BEV', 'body_type': 'SUV', 'price_min': 18.98, 'price_max': 20.98, 'endurance_min': 500, 'endurance_max': 560, 'seat_count': 5, 'acceleration': '5.8', 'max_speed': 180, 'wheelbase': 2750},
        ]
    },
    # 广汽埃安
    {
        'brand': '广汽埃安', 'country': '中国',
        'cars': [
            {'name': 'AION S', 'fuel_type': 'BEV', 'body_type': '轿车', 'price_min': 13.98, 'price_max': 20.58, 'endurance_min': 410, 'endurance_max': 602, 'seat_count': 5, 'acceleration': '7.0', 'max_speed': 156, 'wheelbase': 2750},
            {'name': 'AION Y', 'fuel_type': 'BEV', 'body_type': 'SUV', 'price_min': 11.98, 'price_max': 18.98, 'endurance_min': 410, 'endurance_max': 610, 'seat_count': 5, 'acceleration': '7.5', 'max_speed': 150, 'wheelbase': 2750},
            {'name': 'AION V', 'fuel_type': 'BEV', 'body_type': 'SUV', 'price_min': 17.26, 'price_max': 23.96, 'endurance_min': 500, 'endurance_max': 702, 'seat_count': 5, 'acceleration': '6.8', 'max_speed': 165, 'wheelbase': 2830},
        ]
    },
    # 哪吒
    {
        'brand': '哪吒', 'country': '中国',
        'cars': [
            {'name': '哪吒S', 'fuel_type': 'BEV', 'body_type': '轿车', 'price_min': 17.98, 'price_max': 26.98, 'endurance_min': 580, 'endurance_max': 715, 'seat_count': 5, 'acceleration': '3.9', 'max_speed': 200, 'wheelbase': 2980},
            {'name': '哪吒U', 'fuel_type': 'BEV', 'body_type': 'SUV', 'price_min': 11.98, 'price_max': 17.98, 'endurance_min': 400, 'endurance_max': 610, 'seat_count': 5, 'acceleration': '7.0', 'max_speed': 160, 'wheelbase': 2770},
            {'name': '哪吒X', 'fuel_type': 'BEV', 'body_type': 'SUV', 'price_min': 12.68, 'price_max': 14.68, 'endurance_min': 401, 'endurance_max': 501, 'seat_count': 5, 'acceleration': '9.5', 'max_speed': 150, 'wheelbase': 2770},
        ]
    },
    # 零跑
    {
        'brand': '零跑', 'country': '中国',
        'cars': [
            {'name': 'C11', 'fuel_type': 'BEV', 'body_type': 'SUV', 'price_min': 14.98, 'price_max': 20.98, 'endurance_min': 500, 'endurance_max': 650, 'seat_count': 5, 'acceleration': '7.0', 'max_speed': 170, 'wheelbase': 2930},
            {'name': 'C01', 'fuel_type': 'BEV', 'body_type': '轿车', 'price_min': 14.98, 'price_max': 23.18, 'endurance_min': 500, 'endurance_max': 717, 'seat_count': 5, 'acceleration': '3.7', 'max_speed': 200, 'wheelbase': 2930},
            {'name': 'T03', 'fuel_type': 'BEV', 'body_type': '微型车', 'price_min': 5.99, 'price_max': 8.99, 'endurance_min': 200, 'endurance_max': 403, 'seat_count': 4, 'acceleration': '12.0', 'max_speed': 100, 'wheelbase': 2400},
        ]
    },
]

# 质量问题类型（基于常见投诉）
ISSUE_TYPES = [
    {'name': '转向系统卡滞', 'category': 'quality', 'severity': 'high'},
    {'name': '电池衰减', 'category': 'quality', 'severity': 'medium'},
    {'name': '车机系统卡顿', 'category': 'quality', 'severity': 'low'},
    {'name': '空调制冷效果差', 'category': 'quality', 'severity': 'low'},
    {'name': '异响', 'category': 'quality', 'severity': 'low'},
    {'name': '充电速度慢', 'category': 'quality', 'severity': 'medium'},
    {'name': '续航虚标', 'category': 'quality', 'severity': 'medium'},
    {'name': '刹车异响', 'category': 'quality', 'severity': 'medium'},
    {'name': '售后服务态度差', 'category': 'service', 'severity': 'low'},
    {'name': '维修等待时间长', 'category': 'service', 'severity': 'low'},
    {'name': '配件价格过高', 'category': 'service', 'severity': 'medium'},
    {'name': '承诺功能未兑现', 'category': 'service', 'severity': 'medium'},
    {'name': '车辆自动加速', 'category': 'quality', 'severity': 'high'},
    {'name': '辅助驾驶失灵', 'category': 'quality', 'severity': 'high'},
    {'name': '门窗异响', 'category': 'quality', 'severity': 'low'},
]

# 车身颜色
COLORS = [
    ('冷光银', '#8B8B8B'),
    ('深海蓝', '#1E3A5F'),
    ('纯黑色', '#1C1C1C'),
    ('珠光白', '#F5F5F5'),
    ('中国红', '#C41E3A'),
    ('极光绿', '#00A86B'),
    ('星空灰', '#4A4A4A'),
]


def init_brands_and_cars():
    """初始化品牌和车系数据"""
    print("=" * 60)
    print("开始初始化真实新能源汽车数据...")
    print("=" * 60)
    
    total_brands = 0
    total_cars = 0
    
    for brand_data in REAL_CAR_DATA:
        # 创建或获取品牌
        brand, created = Brand.objects.get_or_create(
            name=brand_data['brand'],
            defaults={'country': brand_data['country']}
        )
        if created:
            total_brands += 1
            print(f"✓ 创建品牌: {brand.name}")
        
        # 创建车系
        for car_data in brand_data['cars']:
            car_series, created = CarSeries.objects.update_or_create(
                brand=brand,
                name=car_data['name'],
                defaults={
                    'fuel_type': car_data['fuel_type'],
                    'body_type': car_data['body_type'],
                    'price_min': car_data['price_min'],
                    'price_max': car_data['price_max'],
                    'endurance_min': car_data['endurance_min'],
                    'endurance_max': car_data['endurance_max'],
                    'seat_count': car_data.get('seat_count', 5),
                    'acceleration': car_data.get('acceleration', '7.0'),
                    'max_speed': car_data.get('max_speed', 180),
                    'wheelbase': car_data.get('wheelbase', 2800),
                    'drive_type': '后驱' if car_data['fuel_type'] == 'BEV' else '四驱',
                    # 评分数据（基于车型定位随机生成合理值）
                    'score_comfort': round(random.uniform(3.8, 4.7), 1),
                    'score_appearance': round(random.uniform(3.9, 4.8), 1),
                    'score_power': round(random.uniform(3.7, 4.9), 1),
                    'score_interior': round(random.uniform(3.6, 4.6), 1),
                    'score_config': round(random.uniform(3.5, 4.5), 1),
                    'score_space': round(random.uniform(3.7, 4.7), 1),
                }
            )
            if created:
                total_cars += 1
            print(f"  {'✓ 创建' if created else '↻ 更新'}车系: {brand.name} {car_series.name}")
    
    print(f"\n品牌总计: {total_brands} 个新增")
    print(f"车系总计: {total_cars} 个新增")
    return total_cars


def init_versions_and_colors():
    """初始化车型版本和颜色"""
    print("\n" + "=" * 60)
    print("初始化车型版本和颜色...")
    print("=" * 60)
    
    for car_series in CarSeries.objects.all():
        # 添加车型版本
        if not car_series.versions.exists():
            for year in [2022, 2023, 2024]:
                CarVersion.objects.create(
                    car_series=car_series,
                    name=random.choice(['标准版', '长续航版', '高性能版', '旗舰版']),
                    year=year,
                    price=float(car_series.price_min or 20) + random.uniform(0, 8),
                    endurance=random.randint(
                        car_series.endurance_min or 400,
                        car_series.endurance_max or 600
                    ),
                    is_default=(year == 2024)
                )
        
        # 添加车身颜色
        if not car_series.colors.exists():
            selected_colors = random.sample(COLORS, min(5, len(COLORS)))
            for i, (name, code) in enumerate(selected_colors):
                CarColor.objects.create(
                    car_series=car_series,
                    name=name,
                    color_code=code,
                    is_default=(i == 0)
                )
    
    print(f"✓ 已为 {CarSeries.objects.count()} 个车系添加版本和颜色")


def init_sales_data():
    """初始化销量数据（模拟真实趋势）"""
    print("\n" + "=" * 60)
    print("初始化销量数据...")
    print("=" * 60)
    
    # 生成过去12个月的数据
    months = []
    current = datetime.now()
    for i in range(12):
        month = (current - timedelta(days=30 * i)).strftime('%Y-%m')
        months.append(month)
    months.reverse()
    
    # 品牌销量基数（基于市场份额）
    brand_base_sales = {
        '比亚迪': 25000,
        '特斯拉': 18000,
        '理想': 12000,
        '问界': 10000,
        '蔚来': 8000,
        '小鹏': 7000,
        '极氪': 6000,
        '广汽埃安': 15000,
        '哪吒': 5000,
        '零跑': 6000,
    }
    
    count = 0
    for car_series in CarSeries.objects.select_related('brand').all():
        brand_name = car_series.brand.name
        base_sales = brand_base_sales.get(brand_name, 5000)
        
        for month in months:
            # 添加随机波动
            sales = int(base_sales * random.uniform(0.7, 1.3))
            
            CarSale.objects.update_or_create(
                car_series=car_series,
                month=month,
                defaults={'sales': sales}
            )
            count += 1
    
    print(f"✓ 创建/更新 {count} 条销量记录")


def init_issue_data():
    """初始化质量问题数据"""
    print("\n" + "=" * 60)
    print("初始化质量问题数据...")
    print("=" * 60)
    
    count = 0
    for car_series in CarSeries.objects.all():
        # 每个车系随机分配3-8个问题类型
        selected_issues = random.sample(ISSUE_TYPES, random.randint(3, 8))
        
        for issue in selected_issues:
            CarIssue.objects.update_or_create(
                car_series=car_series,
                issue_type=issue['name'],
                defaults={
                    'category': issue['category'],
                    'severity': issue['severity'],
                    'description': f"{car_series.name}用户反馈{issue['name']}问题",
                    'report_count': random.randint(1, 50)
                }
            )
            count += 1
    
    print(f"✓ 创建/更新 {count} 条质量问题记录")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("  新能源汽车真实数据初始化脚本")
    print("=" * 60)
    
    # 初始化数据
    init_brands_and_cars()
    init_versions_and_colors()
    init_sales_data()
    init_issue_data()
    
    # 统计
    print("\n" + "=" * 60)
    print("数据初始化完成！统计信息：")
    print("=" * 60)
    print(f"品牌数量: {Brand.objects.count()}")
    print(f"车系数量: {CarSeries.objects.count()}")
    print(f"销量记录: {CarSale.objects.count()}")
    print(f"质量问题: {CarIssue.objects.count()}")
    print(f"车型版本: {CarVersion.objects.count()}")
    print(f"车身颜色: {CarColor.objects.count()}")
    print("=" * 60)


if __name__ == '__main__':
    main()
