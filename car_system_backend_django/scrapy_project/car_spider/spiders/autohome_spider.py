"""
汽车之家爬虫 - 获取新能源车系完整信息
包括：品牌、车系、价格、续航、图片等
"""
import scrapy
import json
import re
from datetime import datetime
from urllib.parse import urljoin


class CarSeriesItem(scrapy.Item):
    """车系完整信息Item"""
    brand_name = scrapy.Field()      # 品牌名称
    series_name = scrapy.Field()     # 车系名称
    fuel_type = scrapy.Field()       # 能源类型：BEV/PHEV/HEV
    body_type = scrapy.Field()       # 车身类型：SUV/轿车/MPV
    price_min = scrapy.Field()       # 最低价格（万）
    price_max = scrapy.Field()       # 最高价格（万）
    endurance_min = scrapy.Field()   # 最低续航（km）
    endurance_max = scrapy.Field()   # 最高续航（km）
    image_url = scrapy.Field()       # 车系图片URL
    # 可选字段
    seat_count = scrapy.Field()      # 座位数
    acceleration = scrapy.Field()    # 百公里加速
    max_speed = scrapy.Field()       # 最高时速


class AutohomeSpider(scrapy.Spider):
    """
    汽车之家新能源车爬虫
    数据来源：汽车之家新能源频道
    """
    name = 'autohome'
    allowed_domains = ['autohome.com.cn', 'cars.app.autohome.com.cn']
    
    custom_settings = {
        'DOWNLOAD_DELAY': 1.5,
        'CONCURRENT_REQUESTS': 4,
        'RETRY_TIMES': 3,
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/html, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
    }
    
    # 新能源品牌列表（可配置）
    TARGET_BRANDS = [
        '比亚迪', '特斯拉', '理想', '蔚来', '小鹏', '问界', '极氪', 
        '零跑', '哪吒', '广汽埃安', '智己', '阿维塔', '岚图', 
        '极狐', '飞凡', '深蓝', '欧拉', '几何', '领克', '大众'
    ]
    
    def __init__(self, brands=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 支持命令行参数指定品牌
        if brands:
            self.TARGET_BRANDS = [b.strip() for b in brands.split(',')]
        self.success_count = 0
        self.error_count = 0
    
    def start_requests(self):
        """开始爬取"""
        self.logger.info(f"开始爬取 {len(self.TARGET_BRANDS)} 个品牌的新能源车数据...")
        
        # 汽车之家新能源车列表API
        # 纯电动(BEV): fueltype=1
        # 插电混动(PHEV): fueltype=3
        # 增程式(EREV): fueltype=4
        fuel_types = [
            ('1', 'BEV'),   # 纯电动
            ('3', 'PHEV'),  # 插电混动
            ('4', 'PHEV'),  # 增程式（归类为插混）
        ]
        
        for fuel_code, fuel_type in fuel_types:
            # 分页获取
            for page in range(1, 20):  # 最多20页
                url = f'https://cars.app.autohome.com.cn/cars/series-api/api/series/list?fueltype={fuel_code}&page={page}&pagesize=50'
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_series_list,
                    meta={'fuel_type': fuel_type, 'page': page},
                    errback=self.handle_error
                )
    
    def parse_series_list(self, response):
        """解析车系列表"""
        fuel_type = response.meta['fuel_type']
        page = response.meta['page']
        
        try:
            data = json.loads(response.text)
            
            if data.get('returncode') != 0:
                self.logger.warning(f"API返回错误: {data.get('message')}")
                return
            
            series_list = data.get('result', {}).get('serieslist', [])
            
            if not series_list:
                self.logger.info(f"第{page}页无数据，停止分页")
                return
            
            self.logger.info(f"解析到 {len(series_list)} 个车系 (页{page}, {fuel_type})")
            
            for series in series_list:
                item = self._parse_series_item(series, fuel_type)
                if item and self._is_target_brand(item.get('brand_name', '')):
                    self.success_count += 1
                    yield item
                    
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON解析失败: {e}")
            # 尝试备用方法
            yield from self.parse_html_fallback(response)
        except Exception as e:
            self.logger.error(f"解析异常: {e}")
            self.error_count += 1
    
    def _parse_series_item(self, series_data, fuel_type):
        """解析单个车系数据"""
        try:
            # 提取基本信息
            brand_name = series_data.get('brandname', '')
            series_name = series_data.get('seriesname', '') or series_data.get('name', '')
            
            if not brand_name or not series_name:
                return None
            
            # 提取价格
            price_str = series_data.get('price', '') or series_data.get('pricerange', '')
            price_min, price_max = self._parse_price(price_str)
            
            # 提取续航
            endurance = series_data.get('endurance', 0) or series_data.get('nedc', 0)
            endurance_min = endurance
            endurance_max = endurance
            
            # 提取图片
            image_url = series_data.get('seriesimage', '') or series_data.get('image', '')
            if image_url and not image_url.startswith('http'):
                image_url = 'https:' + image_url
            
            # 提取车身类型
            body_type = series_data.get('levelname', '') or series_data.get('type', 'SUV')
            
            return CarSeriesItem(
                brand_name=brand_name.strip(),
                series_name=series_name.strip(),
                fuel_type=fuel_type,
                body_type=self._normalize_body_type(body_type),
                price_min=price_min,
                price_max=price_max,
                endurance_min=endurance_min,
                endurance_max=endurance_max,
                image_url=image_url,
                seat_count=series_data.get('seatnum', 5),
            )
        except Exception as e:
            self.logger.warning(f"解析车系失败: {e}")
            return None
    
    def _parse_price(self, price_str):
        """解析价格字符串，返回(最低价, 最高价)"""
        if not price_str:
            return None, None
        
        # 移除"万"等文字
        price_str = re.sub(r'[万元]', '', str(price_str))
        
        # 尝试匹配价格范围，如 "25.99-35.99"
        match = re.search(r'(\d+\.?\d*)\s*[-~至]\s*(\d+\.?\d*)', price_str)
        if match:
            return float(match.group(1)), float(match.group(2))
        
        # 单一价格
        match = re.search(r'(\d+\.?\d*)', price_str)
        if match:
            price = float(match.group(1))
            return price, price
        
        return None, None
    
    def _normalize_body_type(self, body_type):
        """标准化车身类型"""
        body_type = str(body_type).upper()
        if 'SUV' in body_type:
            return 'SUV'
        elif 'MPV' in body_type:
            return 'MPV'
        elif '轿' in body_type or 'SEDAN' in body_type:
            return '轿车'
        elif '跑' in body_type:
            return '跑车'
        elif '两厢' in body_type:
            return '两厢车'
        else:
            return body_type or 'SUV'
    
    def _is_target_brand(self, brand_name):
        """检查是否为目标品牌"""
        return any(target in brand_name or brand_name in target 
                   for target in self.TARGET_BRANDS)
    
    def parse_html_fallback(self, response):
        """备用HTML解析方法"""
        self.logger.info("使用备用HTML解析...")
        # 这里可以添加HTML解析逻辑作为备用
        return []
    
    def handle_error(self, failure):
        """错误处理"""
        self.logger.error(f"请求失败: {failure.request.url}")
        self.error_count += 1
    
    def closed(self, reason):
        """爬虫结束统计"""
        self.logger.info('='*60)
        self.logger.info(f'汽车之家爬虫完成: {reason}')
        self.logger.info(f'成功获取: {self.success_count} 个车系')
        self.logger.info(f'错误次数: {self.error_count} 次')
        self.logger.info('='*60)
