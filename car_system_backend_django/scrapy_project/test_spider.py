"""
爬虫测试脚本
用于快速测试爬虫功能和数据库连接
"""
import os
import sys
import django

# 添加Django项目路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_system.settings')
django.setup()

from apps.cars.models import Brand, CarSeries, CarSale, CarIssue
from car_spider.items import CarSaleItem, CarIssueItem
from car_spider.pipelines import DjangoPipeline


def test_database_connection():
    """测试数据库连接"""
    print("\n" + "="*60)
    print("测试数据库连接...")
    print("="*60)
    
    try:
        # 测试查询
        brand_count = Brand.objects.count()
        series_count = CarSeries.objects.count()
        sale_count = CarSale.objects.count()
        issue_count = CarIssue.objects.count()
        
        print(f"✓ 数据库连接成功！")
        print(f"  - 品牌数量: {brand_count}")
        print(f"  - 车系数量: {series_count}")
        print(f"  - 销量记录: {sale_count}")
        print(f"  - 质量问题: {issue_count}")
        return True
    except Exception as e:
        print(f"✗ 数据库连接失败: {e}")
        return False


def test_sale_item():
    """测试销量Item和Pipeline"""
    print("\n" + "="*60)
    print("测试销量数据处理...")
    print("="*60)
    
    try:
        # 创建测试Item
        item = CarSaleItem(
            brand_name='测试品牌',
            series_name='测试车系',
            month='2024-11',
            sales=12345
        )
        
        print(f"✓ 创建测试Item成功")
        print(f"  品牌: {item['brand_name']}")
        print(f"  车系: {item['series_name']}")
        print(f"  月份: {item['month']}")
        print(f"  销量: {item['sales']}")
        
        # 测试Pipeline
        pipeline = DjangoPipeline()
        pipeline.process_item(item, spider=None)
        
        print(f"✓ Pipeline处理成功")
        
        # 验证数据
        brand = Brand.objects.filter(name='测试品牌').first()
        if brand:
            print(f"✓ 品牌已保存: {brand.name}")
            series = CarSeries.objects.filter(brand=brand, name='测试车系').first()
            if series:
                print(f"✓ 车系已保存: {series.name}")
                sale = CarSale.objects.filter(car_series=series, month='2024-11').first()
                if sale:
                    print(f"✓ 销量已保存: {sale.sales}")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_issue_item():
    """测试质量问题Item和Pipeline"""
    print("\n" + "="*60)
    print("测试质量问题数据处理...")
    print("="*60)
    
    try:
        # 创建测试Item
        item = CarIssueItem(
            brand_name='测试品牌',
            series_name='测试车系',
            issue_type='测试问题',
            description='这是一个测试问题描述',
            severity='medium',
            report_count=1
        )
        
        print(f"✓ 创建测试Item成功")
        print(f"  品牌: {item['brand_name']}")
        print(f"  车系: {item['series_name']}")
        print(f"  问题: {item['issue_type']}")
        print(f"  严重程度: {item['severity']}")
        
        # 测试Pipeline
        pipeline = DjangoPipeline()
        pipeline.process_item(item, spider=None)
        
        print(f"✓ Pipeline处理成功")
        
        # 验证数据
        brand = Brand.objects.filter(name='测试品牌').first()
        if brand:
            series = CarSeries.objects.filter(brand=brand, name='测试车系').first()
            if series:
                issue = CarIssue.objects.filter(car_series=series, issue_type='测试问题').first()
                if issue:
                    print(f"✓ 质量问题已保存: {issue.issue_type} (投诉{issue.report_count}次)")
        
        return True
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def cleanup_test_data():
    """清理测试数据"""
    print("\n" + "="*60)
    print("清理测试数据...")
    print("="*60)
    
    try:
        # 删除测试品牌（级联删除相关数据）
        brand = Brand.objects.filter(name='测试品牌').first()
        if brand:
            brand.delete()
            print("✓ 测试数据已清理")
        else:
            print("- 没有需要清理的测试数据")
        return True
    except Exception as e:
        print(f"✗ 清理失败: {e}")
        return False


def show_recent_data():
    """显示最近的数据"""
    print("\n" + "="*60)
    print("最近的数据记录...")
    print("="*60)
    
    print("\n最近5个品牌：")
    for brand in Brand.objects.all()[:5]:
        print(f"  - {brand.name} ({brand.country})")
    
    print("\n最近5条销量记录：")
    for sale in CarSale.objects.select_related('car_series', 'car_series__brand').all()[:5]:
        print(f"  - {sale.car_series.brand.name} {sale.car_series.name}: {sale.sales}辆 ({sale.month})")
    
    print("\n最近5条质量问题：")
    for issue in CarIssue.objects.select_related('car_series', 'car_series__brand').all()[:5]:
        print(f"  - {issue.car_series.brand.name} {issue.car_series.name}: {issue.issue_type} [{issue.severity}] ({issue.report_count}次)")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("Scrapy 爬虫测试工具")
    print("="*60)
    
    # 测试数据库连接
    if not test_database_connection():
        print("\n✗ 数据库连接失败，请检查配置")
        return
    
    # 测试销量Item
    test_sale_item()
    
    # 测试质量问题Item
    test_issue_item()
    
    # 显示最近数据
    show_recent_data()
    
    # 询问是否清理测试数据
    print("\n" + "="*60)
    response = input("是否清理测试数据？(y/n): ").strip().lower()
    if response == 'y':
        cleanup_test_data()
    
    print("\n" + "="*60)
    print("测试完成！")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
