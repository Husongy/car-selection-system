import scrapy
import re
import json
from car_spider.items import CarItem


class AutohomeSpider(scrapy.Spider):
    """汽车之家爬虫 - 爬取新能源车系信息"""
    name = "autohome"
    allowed_domains = ["autohome.com.cn"]
    
    # 新能源车品牌列表页
    start_urls = [
        "https://www.autohome.com.cn/nev/",  # 新能源车首页
    ]
    
    custom_settings = {
        'DOWNLOAD_DELAY': 3,  # 增加延迟避免被封
        'CONCURRENT_REQUESTS': 4,
    }
    
    def parse(self, response):
        """解析品牌列表页"""
        self.logger.info(f"正在解析品牌列表页: {response.url}")
        
        # 提取品牌信息
        # 这里使用模拟数据，实际需要根据网站结构调整选择器
        brands = [
            {'name': '比亚迪', 'url': 'https://car.autohome.com.cn/price/brand-45.html'},
            {'name': '特斯拉', 'url': 'https://car.autohome.com.cn/price/brand-263.html'},
            {'name': '蔚来', 'url': 'https://car.autohome.com.cn/price/brand-458.html'},
            {'name': '小鹏', 'url': 'https://car.autohome.com.cn/price/brand-487.html'},
            {'name': '理想', 'url': 'https://car.autohome.com.cn/price/brand-491.html'},
        ]
        
        for brand in brands:
            yield scrapy.Request(
                url=brand['url'],
                callback=self.parse_brand_page,
                meta={'brand_name': brand['name']},
                dont_filter=True
            )
    
    def parse_brand_page(self, response):
        """解析品牌车系列表页"""
        brand_name = response.meta['brand_name']
        self.logger.info(f"正在解析品牌: {brand_name}")
        
        # 模拟车系数据（实际应从页面提取）
        car_series_list = self.get_mock_data(brand_name)
        
        for car_data in car_series_list:
            item = CarItem()
            
            # 品牌信息
            item['brand_name'] = car_data['brand_name']
            item['brand_logo_url'] = car_data.get('brand_logo_url', '')
            
            # 车系信息
            item['series_name'] = car_data['series_name']
            item['price_min'] = car_data['price_min']
            item['price_max'] = car_data['price_max']
            item['fuel_type'] = car_data['fuel_type']
            item['seat_count'] = car_data.get('seat_count', 5)
            item['car_model'] = car_data['car_model']
            item['series_image_url'] = car_data.get('series_image_url', '')
            
            # 评分信息（模拟数据）
            item['comfort_score'] = car_data.get('comfort_score', 4.5)
            item['appearance_score'] = car_data.get('appearance_score', 4.6)
            item['config_score'] = car_data.get('config_score', 4.4)
            item['control_score'] = car_data.get('control_score', 4.3)
            item['power_score'] = car_data.get('power_score', 4.5)
            item['space_score'] = car_data.get('space_score', 4.4)
            item['interior_score'] = car_data.get('interior_score', 4.3)
            item['total_score'] = car_data.get('total_score', 4.4)
            
            yield item
    
    def get_mock_data(self, brand_name):
        """获取模拟数据（实际项目中应该从页面抓取）"""
        mock_data = {
            '比亚迪': [
                {
                    'brand_name': '比亚迪',
                    'brand_logo_url': 'https://x.autoimg.cn/www/common/images/car/logo/byd.png',
                    'series_name': '海豹',
                    'price_min': 18.98,
                    'price_max': 28.68,
                    'fuel_type': '纯电动',
                    'seat_count': 5,
                    'car_model': '轿车',
                    'series_image_url': 'https://car3.autoimg.cn/cardfs/product/g30/M01/32/B5/400x300_autohomecar__ChxkPWN5Q4aAbD0oAAVGxfMZiY8866.jpg',
                    'comfort_score': 4.6,
                    'appearance_score': 4.8,
                    'config_score': 4.5,
                    'control_score': 4.4,
                    'power_score': 4.7,
                    'space_score': 4.3,
                    'interior_score': 4.5,
                    'total_score': 4.5,
                },
                {
                    'brand_name': '比亚迪',
                    'series_name': '汉EV',
                    'price_min': 20.98,
                    'price_max': 32.98,
                    'fuel_type': '纯电动',
                    'seat_count': 5,
                    'car_model': '轿车',
                    'series_image_url': '',
                    'total_score': 4.6,
                },
                {
                    'brand_name': '比亚迪',
                    'series_name': '宋PLUS新能源',
                    'price_min': 13.58,
                    'price_max': 20.78,
                    'fuel_type': '插电混动',
                    'seat_count': 5,
                    'car_model': 'SUV',
                    'series_image_url': '',
                    'total_score': 4.5,
                },
            ],
            '特斯拉': [
                {
                    'brand_name': '特斯拉',
                    'series_name': 'Model 3',
                    'price_min': 26.14,
                    'price_max': 34.99,
                    'fuel_type': '纯电动',
                    'seat_count': 5,
                    'car_model': '轿车',
                    'series_image_url': '',
                    'total_score': 4.7,
                },
                {
                    'brand_name': '特斯拉',
                    'series_name': 'Model Y',
                    'price_min': 26.39,
                    'price_max': 35.99,
                    'fuel_type': '纯电动',
                    'seat_count': 5,
                    'car_model': 'SUV',
                    'series_image_url': '',
                    'total_score': 4.6,
                },
            ],
            '蔚来': [
                {
                    'brand_name': '蔚来',
                    'series_name': 'ET5',
                    'price_min': 29.80,
                    'price_max': 35.60,
                    'fuel_type': '纯电动',
                    'seat_count': 5,
                    'car_model': '轿车',
                    'series_image_url': '',
                    'total_score': 4.5,
                },
                {
                    'brand_name': '蔚来',
                    'series_name': 'ES6',
                    'price_min': 33.80,
                    'price_max': 39.60,
                    'fuel_type': '纯电动',
                    'seat_count': 5,
                    'car_model': 'SUV',
                    'series_image_url': '',
                    'total_score': 4.6,
                },
            ],
            '小鹏': [
                {
                    'brand_name': '小鹏',
                    'series_name': 'P7',
                    'price_min': 22.39,
                    'price_max': 33.99,
                    'fuel_type': '纯电动',
                    'seat_count': 5,
                    'car_model': '轿车',
                    'series_image_url': '',
                    'total_score': 4.4,
                },
                {
                    'brand_name': '小鹏',
                    'series_name': 'G9',
                    'price_min': 26.39,
                    'price_max': 35.99,
                    'fuel_type': '纯电动',
                    'seat_count': 5,
                    'car_model': 'SUV',
                    'series_image_url': '',
                    'total_score': 4.5,
                },
            ],
            '理想': [
                {
                    'brand_name': '理想',
                    'series_name': '理想L7',
                    'price_min': 31.98,
                    'price_max': 37.98,
                    'fuel_type': '增程式',
                    'seat_count': 5,
                    'car_model': 'SUV',
                    'series_image_url': '',
                    'total_score': 4.7,
                },
                {
                    'brand_name': '理想',
                    'series_name': '理想L9',
                    'price_min': 42.98,
                    'price_max': 45.98,
                    'fuel_type': '增程式',
                    'seat_count': 6,
                    'car_model': 'SUV',
                    'series_image_url': '',
                    'total_score': 4.8,
                },
            ],
        }
        
        return mock_data.get(brand_name, [])
