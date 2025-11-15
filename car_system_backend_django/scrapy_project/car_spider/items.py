"""
Scrapy Items 定义
用于存储爬取的汽车销量和质量问题数据
"""
import scrapy


class CarSaleItem(scrapy.Item):
    """车系销量数据 Item"""
    brand_name = scrapy.Field()      # 品牌名称
    series_name = scrapy.Field()     # 车系名称
    month = scrapy.Field()           # 月份 (格式: 2024-01)
    sales = scrapy.Field()           # 销量
    

class CarIssueItem(scrapy.Item):
    """车系质量问题 Item"""
    brand_name = scrapy.Field()      # 品牌名称
    series_name = scrapy.Field()     # 车系名称
    issue_type = scrapy.Field()      # 问题类型
    description = scrapy.Field()     # 问题描述
    severity = scrapy.Field()        # 严重程度 (low/medium/high)
    report_count = scrapy.Field()    # 投诉次数
