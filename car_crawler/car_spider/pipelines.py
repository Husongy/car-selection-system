from itemadapter import ItemAdapter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import sys
import os

# 添加后端项目路径到系统路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../car_system_backend'))

from app.models.car import Brand, CarSeries, CarSeriesScore, FuelType, CarModel


class CarSpiderPipeline:
    """车辆数据管道 - 将爬取的数据存入MySQL数据库"""
    
    def __init__(self, database_url):
        self.database_url = database_url
        self.engine = None
        self.Session = None
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            database_url=crawler.settings.get('DATABASE_URL')
        )
    
    def open_spider(self, spider):
        """爬虫开启时创建数据库连接"""
        spider.logger.info(f"连接数据库: {self.database_url}")
        self.engine = create_engine(
            self.database_url,
            pool_pre_ping=True,
            pool_recycle=3600,
            echo=False
        )
        self.Session = sessionmaker(bind=self.engine)
        spider.logger.info("数据库连接成功")
    
    def close_spider(self, spider):
        """爬虫关闭时关闭数据库连接"""
        if self.engine:
            self.engine.dispose()
            spider.logger.info("数据库连接已关闭")
    
    def process_item(self, item, spider):
        """处理每个 Item"""
        adapter = ItemAdapter(item)
        session = self.Session()
        
        try:
            # 1. 处理品牌数据
            brand = self._get_or_create_brand(
                session,
                adapter.get('brand_name'),
                adapter.get('brand_logo_url')
            )
            
            # 2. 处理车系数据
            car_series = self._get_or_create_car_series(
                session,
                brand,
                adapter
            )
            
            # 3. 处理评分数据
            self._save_car_series_score(
                session,
                car_series,
                adapter
            )
            
            session.commit()
            spider.logger.info(f"成功保存车系: {adapter.get('brand_name')} - {adapter.get('series_name')}")
            
        except Exception as e:
            session.rollback()
            spider.logger.error(f"保存数据失败: {e}")
            spider.logger.exception(e)
        finally:
            session.close()
        
        return item
    
    def _get_or_create_brand(self, session, brand_name, logo_url):
        """获取或创建品牌"""
        if not brand_name:
            return None
        
        # 查询品牌是否存在
        brand = session.query(Brand).filter_by(name=brand_name).first()
        
        if not brand:
            # 创建新品牌
            brand = Brand(
                name=brand_name,
                logo_url=logo_url or ''
            )
            session.add(brand)
            session.flush()  # 获取 brand.id
        
        return brand
    
    def _get_or_create_car_series(self, session, brand, adapter):
        """获取或创建车系"""
        series_name = adapter.get('series_name')
        
        if not series_name or not brand:
            return None
        
        # 查询车系是否存在
        car_series = session.query(CarSeries).filter_by(
            name=series_name,
            brand_id=brand.id
        ).first()
        
        if not car_series:
            # 映射燃料类型
            fuel_type = self._map_fuel_type(adapter.get('fuel_type'))
            # 映射车型类别
            car_model = self._map_car_model(adapter.get('car_model'))
            
            # 创建新车系
            car_series = CarSeries(
                name=series_name,
                brand_id=brand.id,
                price_min=adapter.get('price_min'),
                price_max=adapter.get('price_max'),
                fuel_type=fuel_type,
                seat_count=adapter.get('seat_count'),
                car_model=car_model,
                image_url=adapter.get('series_image_url') or ''
            )
            session.add(car_series)
            session.flush()
        else:
            # 更新车系信息
            car_series.price_min = adapter.get('price_min')
            car_series.price_max = adapter.get('price_max')
            car_series.seat_count = adapter.get('seat_count')
            if adapter.get('series_image_url'):
                car_series.image_url = adapter.get('series_image_url')
        
        return car_series
    
    def _save_car_series_score(self, session, car_series, adapter):
        """保存或更新车系评分"""
        if not car_series:
            return
        
        # 查询评分是否存在
        score = session.query(CarSeriesScore).filter_by(
            car_series_id=car_series.id
        ).first()
        
        if not score:
            # 创建新评分
            score = CarSeriesScore(
                car_series_id=car_series.id,
                comfort_score=adapter.get('comfort_score', 0.0),
                appearance_score=adapter.get('appearance_score', 0.0),
                config_score=adapter.get('config_score', 0.0),
                control_score=adapter.get('control_score', 0.0),
                power_score=adapter.get('power_score', 0.0),
                space_score=adapter.get('space_score', 0.0),
                interior_score=adapter.get('interior_score', 0.0),
                total_score=adapter.get('total_score', 0.0)
            )
            session.add(score)
        else:
            # 更新评分
            score.comfort_score = adapter.get('comfort_score', score.comfort_score)
            score.appearance_score = adapter.get('appearance_score', score.appearance_score)
            score.config_score = adapter.get('config_score', score.config_score)
            score.control_score = adapter.get('control_score', score.control_score)
            score.power_score = adapter.get('power_score', score.power_score)
            score.space_score = adapter.get('space_score', score.space_score)
            score.interior_score = adapter.get('interior_score', score.interior_score)
            score.total_score = adapter.get('total_score', score.total_score)
    
    def _map_fuel_type(self, fuel_type_str):
        """映射燃料类型到枚举"""
        fuel_type_map = {
            '纯电动': FuelType.ELECTRIC,
            '插电混动': FuelType.HYBRID,
            '增程式': FuelType.PHEV,
            '油电混动': FuelType.MILD_HYBRID,
            '汽油': FuelType.GASOLINE,
            '柴油': FuelType.DIESEL,
        }
        return fuel_type_map.get(fuel_type_str, FuelType.ELECTRIC)
    
    def _map_car_model(self, car_model_str):
        """映射车型类别到枚举"""
        car_model_map = {
            '轿车': CarModel.SEDAN,
            'SUV': CarModel.SUV,
            'MPV': CarModel.MPV,
            '跑车': CarModel.COUPE,
            '两厢车': CarModel.HATCHBACK,
            '旅行车': CarModel.WAGON,
            '皮卡': CarModel.PICKUP,
        }
        return car_model_map.get(car_model_str, CarModel.SEDAN)
