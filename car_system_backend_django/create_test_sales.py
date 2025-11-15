"""
创建测试销量数据
运行方式: python create_test_sales.py
"""
import os
import django
import sys
from datetime import datetime, timedelta

# 设置Django环境
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_system.settings')
django.setup()

from apps.cars.models import Brand, CarSeries, CarSale

def create_test_sales():
    """创建测试销量数据"""
    
    # 获取所有车系
    car_series_list = CarSeries.objects.all()
    
    if not car_series_list:
        print("❌ 数据库中没有车系数据，请先添加品牌和车系！")
        return
    
    print(f"✅ 找到 {car_series_list.count()} 个车系")
    
    # 为每个车系生成最近3个月的销量数据
    now = datetime.now()
    months = []
    for i in range(3):
        month = (now - timedelta(days=30 * i)).strftime('%Y-%m')
        months.append(month)
    
    print(f"📅 生成月份: {', '.join(months)}")
    
    created_count = 0
    for car_series in car_series_list:
        for idx, month in enumerate(months):
            # 生成随机销量（越近的月份销量越高）
            base_sales = 5000 + (2 - idx) * 2000
            sales = base_sales + (hash(car_series.name) % 5000)
            
            # 使用 update_or_create 避免重复
            obj, created = CarSale.objects.update_or_create(
                car_series=car_series,
                month=month,
                defaults={'sales': sales}
            )
            
            if created:
                created_count += 1
                print(f"  ✅ {car_series.name} - {month}: {sales}辆")
            else:
                print(f"  ⚠️  {car_series.name} - {month}: {sales}辆 (已存在，已更新)")
    
    print(f"\n🎉 完成！共创建/更新了 {created_count} 条销量数据")
    print(f"📊 总销量记录数: {CarSale.objects.count()}")

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 开始创建测试销量数据...")
    print("=" * 50)
    create_test_sales()
    print("=" * 50)
