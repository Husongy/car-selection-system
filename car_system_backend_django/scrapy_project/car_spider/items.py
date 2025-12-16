"""
Scrapy Items definition
Optimized version with data validation and processing
"""
import scrapy
try:
    from itemloaders.processors import TakeFirst, MapCompose, Join
except ImportError:
    from scrapy.loader.processors import TakeFirst, MapCompose, Join
import re


def clean_text(text):
    """Clean text data"""
    if not text:
        return ''
    text = re.sub(r'\s+', ' ', str(text))
    return text.strip()


def clean_number(text):
    """Clean number data"""
    if isinstance(text, (int, float)):
        return text
    if not text:
        return 0
    text = re.sub(r'[^0-9.]', '', str(text))
    try:
        return int(float(text))
    except ValueError:
        return 0


class CarSaleItem(scrapy.Item):
    """Car sale data item"""
    brand_name = scrapy.Field()
    series_name = scrapy.Field()
    month = scrapy.Field()
    sales = scrapy.Field()
    
    def is_valid(self):
        """Validate data"""
        if not self.get('brand_name') or not self.get('series_name'):
            return False
        if not self.get('month'):
            return False
        sales = self.get('sales', 0)
        if not isinstance(sales, (int, float)) or sales < 0:
            return False
        return True


class CarIssueItem(scrapy.Item):
    """Car issue data item"""
    brand_name = scrapy.Field()
    series_name = scrapy.Field()
    issue_type = scrapy.Field()
    description = scrapy.Field()
    severity = scrapy.Field()
    report_count = scrapy.Field()
    
    def is_valid(self):
        """Validate data"""
        if not self.get('brand_name') or not self.get('series_name'):
            return False
        if not self.get('issue_type'):
            return False
        severity = self.get('severity', 'medium')
        if severity not in ['low', 'medium', 'high']:
            return False
        return True
