from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from sqlalchemy.orm import joinedload
from typing import List, Tuple, Optional
import math

from app.models.car import Brand, CarSeries, CarSeriesScore
from app.schemas.car import CarQueryParams, CarSeriesSimpleResponse, PaginationResponse


class CarService:
    """车系服务类 - 处理车系相关业务逻辑"""
    
    @staticmethod
    async def get_car_series_list(
        db: AsyncSession,
        params: CarQueryParams
    ) -> Tuple[List[dict], PaginationResponse]:
        """
        获取车系列表（支持筛选、排序、分页）
        
        Args:
            db: 数据库会话
            params: 查询参数
            
        Returns:
            车系列表和分页信息的元组
        """
        # 构建基础查询
        query = select(CarSeries).join(Brand).outerjoin(CarSeriesScore)
        
        # 应用筛选条件
        query = CarService._apply_filters(query, params)
        
        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        result = await db.execute(count_query)
        total = result.scalar() or 0
        
        # 应用排序
        query = CarService._apply_sorting(query, params)
        
        # 应用分页
        offset = (params.page - 1) * params.page_size
        query = query.offset(offset).limit(params.page_size)
        
        # 预加载关联数据
        query = query.options(
            joinedload(CarSeries.brand),
            joinedload(CarSeries.scores)
        )
        
        # 执行查询
        result = await db.execute(query)
        car_series_list = result.unique().scalars().all()
        
        # 转换为响应格式
        items = [
            {
                "id": car.id,
                "name": car.name,
                "brand_name": car.brand.name,
                "brand_logo_url": car.brand.logo_url,
                "price_min": car.price_min,
                "price_max": car.price_max,
                "fuel_type": car.fuel_type.value,
                "car_model": car.car_model.value if car.car_model else None,
                "image_url": car.image_url,
                "total_score": car.scores.total_score if car.scores else 0.0
            }
            for car in car_series_list
        ]
        
        # 计算分页信息
        total_pages = math.ceil(total / params.page_size) if total > 0 else 0
        pagination = PaginationResponse(
            total=total,
            page=params.page,
            page_size=params.page_size,
            total_pages=total_pages,
            has_next=params.page < total_pages,
            has_prev=params.page > 1
        )
        
        return items, pagination
    
    @staticmethod
    def _apply_filters(query, params: CarQueryParams):
        """应用筛选条件"""
        # 品牌名称筛选
        if params.brand_name:
            query = query.where(Brand.name.like(f"%{params.brand_name}%"))
        
        # 价格范围筛选
        if params.min_price is not None:
            query = query.where(
                or_(
                    CarSeries.price_max >= params.min_price,
                    CarSeries.price_min >= params.min_price
                )
            )
        
        if params.max_price is not None:
            query = query.where(
                or_(
                    CarSeries.price_min <= params.max_price,
                    CarSeries.price_max <= params.max_price
                )
            )
        
        # 燃料类型筛选
        if params.fuel_type:
            query = query.where(CarSeries.fuel_type == params.fuel_type.value)
        
        # 车型类别筛选
        if params.car_model:
            query = query.where(CarSeries.car_model == params.car_model.value)
        
        # 最低评分筛选
        if params.min_score is not None:
            query = query.where(CarSeriesScore.total_score >= params.min_score)
        
        return query
    
    @staticmethod
    def _apply_sorting(query, params: CarQueryParams):
        """应用排序"""
        # 验证排序字段
        allowed_fields = {
            "total_score": CarSeriesScore.total_score,
            "price_min": CarSeries.price_min,
            "price_max": CarSeries.price_max,
            "created_at": CarSeries.created_at
        }
        
        order_field = allowed_fields.get(params.order_by, CarSeriesScore.total_score)
        
        # 应用排序方向
        if params.order_direction == "asc":
            query = query.order_by(order_field.asc())
        else:
            query = query.order_by(order_field.desc())
        
        return query
    
    @staticmethod
    async def get_car_series_by_id(db: AsyncSession, car_id: int) -> Optional[CarSeries]:
        """
        根据ID获取车系详情
        
        Args:
            db: 数据库会话
            car_id: 车系ID
            
        Returns:
            车系对象或None
        """
        query = select(CarSeries).where(CarSeries.id == car_id).options(
            joinedload(CarSeries.brand),
            joinedload(CarSeries.scores)
        )
        
        result = await db.execute(query)
        return result.unique().scalar_one_or_none()
    
    @staticmethod
    async def get_brands_list(db: AsyncSession) -> List[Brand]:
        """
        获取所有品牌列表
        
        Args:
            db: 数据库会话
            
        Returns:
            品牌列表
        """
        query = select(Brand).order_by(Brand.name)
        result = await db.execute(query)
        return result.scalars().all()
