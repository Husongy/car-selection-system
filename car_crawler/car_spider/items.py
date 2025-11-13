import scrapy


class CarItem(scrapy.Item):
    """车系信息 Item"""
    # 品牌信息
    brand_name = scrapy.Field()  # 品牌名
    brand_logo_url = scrapy.Field()  # 品牌Logo URL
    
    # 车系信息
    series_name = scrapy.Field()  # 车系名
    price_min = scrapy.Field()  # 最低价格(万元)
    price_max = scrapy.Field()  # 最高价格(万元)
    fuel_type = scrapy.Field()  # 燃料类型
    seat_count = scrapy.Field()  # 座位数
    car_model = scrapy.Field()  # 车型类别
    series_image_url = scrapy.Field()  # 车系图片URL
    
    # 评分信息（如果能抓到）
    comfort_score = scrapy.Field()  # 舒适性评分
    appearance_score = scrapy.Field()  # 外观评分
    config_score = scrapy.Field()  # 配置评分
    control_score = scrapy.Field()  # 操控评分
    power_score = scrapy.Field()  # 动力评分
    space_score = scrapy.Field()  # 空间评分
    interior_score = scrapy.Field()  # 内饰评分
    total_score = scrapy.Field()  # 总分
