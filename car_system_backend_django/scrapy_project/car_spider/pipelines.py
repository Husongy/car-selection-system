"""
Django Pipeline - 将爬取的数据保存到数据库
使用 Django ORM 操作数据库，避免重复数据
"""
from apps.cars.models import Brand, CarSeries, CarSale, CarIssue
from .items import CarSaleItem, CarIssueItem


class DjangoPipeline:
    """Django 数据库存储 Pipeline"""
    
    def process_item(self, item, spider):
        """处理每个 Item，保存到数据库"""
        
        if isinstance(item, CarSaleItem):
            self._save_car_sale(item)
        elif isinstance(item, CarIssueItem):
            self._save_car_issue(item)
        
        return item
    
    def _save_car_sale(self, item):
        """保存销量数据"""
        try:
            # 获取或创建品牌
            brand, _ = Brand.objects.get_or_create(
                name=item['brand_name'],
                defaults={'country': '中国'}
            )
            
            # 获取或创建车系
            car_series, _ = CarSeries.objects.get_or_create(
                brand=brand,
                name=item['series_name'],
                defaults={'fuel_type': 'BEV'}
            )
            
            # 更新或创建销量数据
            CarSale.objects.update_or_create(
                car_series=car_series,
                month=item['month'],
                defaults={'sales': int(item['sales'])}
            )
            
            print(f"✓ 保存销量: {brand.name} {car_series.name} - {item['month']}: {item['sales']}")
            
        except Exception as e:
            print(f"✗ 保存销量失败: {e}")
    
    def _save_car_issue(self, item):
        """保存质量问题数据"""
        try:
            # 获取或创建品牌
            brand, _ = Brand.objects.get_or_create(
                name=item['brand_name'],
                defaults={'country': '中国'}
            )
            
            # 获取或创建车系
            car_series, _ = CarSeries.objects.get_or_create(
                brand=brand,
                name=item['series_name'],
                defaults={'fuel_type': 'BEV'}
            )
            
            # 检查是否已存在相同问题，如果存在则增加投诉次数
            existing_issue = CarIssue.objects.filter(
                car_series=car_series,
                issue_type=item['issue_type']
            ).first()
            
            if existing_issue:
                existing_issue.report_count += int(item.get('report_count', 1))
                existing_issue.save()
                print(f"✓ 更新问题投诉次数: {car_series.name} - {item['issue_type']}")
            else:
                CarIssue.objects.create(
                    car_series=car_series,
                    issue_type=item['issue_type'],
                    description=item.get('description', ''),
                    severity=item.get('severity', 'medium'),
                    report_count=int(item.get('report_count', 1))
                )
                print(f"✓ 保存新问题: {car_series.name} - {item['issue_type']}")
            
        except Exception as e:
            print(f"✗ 保存质量问题失败: {e}")
