"""
Quick check spider data
Usage: python check_spider_data.py
"""
import os
import django
import sys

# Setup Django environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_system.settings')
django.setup()

from apps.cars.models import Brand, CarSeries, CarSale, CarIssue


def main():
    print("\n" + "=" * 70)
    print("🔍 Scrapy Spider Data Check")
    print("=" * 70)
    
    # Statistics
    brand_count = Brand.objects.count()
    series_count = CarSeries.objects.count()
    sale_count = CarSale.objects.count()
    issue_count = CarIssue.objects.count()
    
    print("\n📊 Database Statistics:")
    print(f"  ├─ Brands: {brand_count}")
    print(f"  ├─ Car Series: {series_count}")
    print(f"  ├─ Sales Records: {sale_count}")
    print(f"  └─ Quality Issues: {issue_count}")
    
    if brand_count == 0:
        print("\n❌ No data found! Please run spider first:")
        print("   cd scrapy_project")
        print("   python run_spider.py dongchedi")
        print("   python run_spider.py chezhi")
        return
    
    # Latest Brands
    print("\n🚗 Latest Brands (Top 5):")
    for i, brand in enumerate(Brand.objects.all()[:5], 1):
        series_num = brand.series.count()
        print(f"  {i}. {brand.name} ({brand.country}) - {series_num} series")
    
    # Latest Sales
    if sale_count > 0:
        print("\n📈 Latest Sales Data (Top 5):")
        for i, sale in enumerate(
            CarSale.objects.select_related('car_series', 'car_series__brand')
            .order_by('-sales')[:5], 1
        ):
            print(f"  {i}. {sale.car_series.brand.name} {sale.car_series.name}: "
                  f"{sale.sales:,} units ({sale.month})")
    
    # Latest Issues
    if issue_count > 0:
        print("\n⚠️ Latest Quality Issues (Top 5):")
        for i, issue in enumerate(
            CarIssue.objects.select_related('car_series', 'car_series__brand')
            .order_by('-report_count')[:5], 1
        ):
            severity_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(issue.severity, '⚪')
            print(f"  {i}. {severity_icon} {issue.car_series.brand.name} {issue.car_series.name}: "
                  f"{issue.issue_type} ({issue.report_count} reports)")
    
    # Monthly sales trend
    if sale_count > 0:
        print("\n📅 Sales by Month:")
        from django.db.models import Sum, Count
        monthly_stats = CarSale.objects.values('month').annotate(
            total_sales=Sum('sales'),
            car_count=Count('id')
        ).order_by('-month')[:3]
        
        for stat in monthly_stats:
            print(f"  {stat['month']}: {stat['total_sales']:,} units "
                  f"({stat['car_count']} records)")
    
    print("\n" + "=" * 70)
    print("✅ Data check completed!")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()
