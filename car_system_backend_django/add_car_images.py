"""
为车系添加图片URL
"""
import os
import django
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_system.settings')
django.setup()

from apps.cars.models import CarSeries

# 车系图片数据（示例URL，可以替换为真实图片）
CAR_IMAGES = {
    '海豹': 'https://img2.autohome.com.cn/car/202306/202306081040494343.jpg',
    '汉EV': 'https://img2.autohome.com.cn/car/202208/202208091045534967.jpg',
    'Model 3': 'https://img2.autohome.com.cn/car/202309/202309071049594863.jpg',
    'ET5': 'https://img2.autohome.com.cn/car/202306/202306281051273687.jpg',
}

def add_images():
    """为车系添加图片"""
    updated_count = 0
    
    for name, image_url in CAR_IMAGES.items():
        try:
            car_series = CarSeries.objects.get(name=name)
            car_series.image = image_url
            car_series.save()
            print(f"✅ {name}: 图片已更新")
            updated_count += 1
        except CarSeries.DoesNotExist:
            print(f"⚠️  {name}: 车系不存在")
    
    print(f"\n🎉 完成！共更新了 {updated_count} 个车系的图片")

if __name__ == '__main__':
    print("=" * 50)
    print("🖼️  开始添加车系图片...")
    print("=" * 50)
    add_images()
    print("=" * 50)
