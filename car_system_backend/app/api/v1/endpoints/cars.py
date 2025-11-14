"""
车型查询接口 - 支持条件筛选、排序、分页
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import joinedload
from typing import List, Optional
from app.core.database import get_async_db
from app.models.car_model import CarModel
from app.models.series import Series
from app.models.brand import Brand
from app.schemas.response import PageResponse
from pydantic import BaseModel, Field

router = APIRouter()


class CarQueryParams(BaseModel):
    """车型查询参数"""
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页数量")
    brand_ids: Optional[List[int]] = Field(None, description="品牌ID列表")
    price_min: Optional[float] = Field(None, description="最低价格(万元)")
    price_max: Optional[float] = Field(None, description="最高价格(万元)")
    energy_types: Optional[List[str]] = Field(None, description="能源类型列表")
    seats: Optional[List[int]] = Field(None, description="座位数列表")
    levels: Optional[List[str]] = Field(None, description="车型级别列表")
    sort_by: Optional[str] = Field("price_asc", description="排序方式: price_asc, price_desc, name_asc, name_desc")


class CarItemResponse(BaseModel):
    """车型列表项响应"""
    id: int
    name: str
    series_id: int
    series_name: str
    brand_id: int
    brand_name: str
    price: Optional[float] = None
    image: Optional[str] = None
    energy_type: Optional[str] = None
    seats: Optional[int] = None
    level: Optional[str] = None
    description: Optional[str] = None
    acceleration: Optional[float] = None
    fuel_consumption: Optional[float] = None
    
    class Config:
        from_attributes = True


@router.get("/cars", response_model=PageResponse[CarItemResponse], summary="条件查询车型列表")
async def query_cars(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    brand_ids: Optional[str] = Query(None, description="品牌ID列表，逗号分隔"),
    price_min: Optional[float] = Query(None, description="最低价格(万元)"),
    price_max: Optional[float] = Query(None, description="最高价格(万元)"),
    energy_types: Optional[str] = Query(None, description="能源类型列表，逗号分隔"),
    seats: Optional[str] = Query(None, description="座位数列表，逗号分隔"),
    levels: Optional[str] = Query(None, description="车型级别列表，逗号分隔"),
    sort_by: str = Query("price_asc", description="排序方式: price_asc, price_desc, name_asc, name_desc"),
    db: AsyncSession = Depends(get_async_db)
):
    """
    条件查询车型列表
    
    支持的筛选条件：
    - 品牌筛选（多选）
    - 价格区间
    - 能源类型（多选）
    - 座位数（多选）
    - 车型级别（多选）
    
    支持的排序方式：
    - price_asc: 价格升序
    - price_desc: 价格降序
    - name_asc: 名称升序
    - name_desc: 名称降序
    """
    # 构建基础查询，使用joinedload避免N+1查询问题
    query = select(CarModel).options(
        joinedload(CarModel.series).joinedload(Series.brand)
    )
    
    # 构建筛选条件
    conditions = []
    
    # 品牌筛选
    if brand_ids:
        brand_id_list = [int(x.strip()) for x in brand_ids.split(',') if x.strip()]
        if brand_id_list:
            query = query.join(CarModel.series).join(Series.brand)
            conditions.append(Brand.id.in_(brand_id_list))
    
    # 价格区间筛选
    if price_min is not None:
        conditions.append(CarModel.price >= price_min)
    if price_max is not None:
        conditions.append(CarModel.price <= price_max)
    
    # 能源类型筛选
    if energy_types:
        energy_type_list = [x.strip() for x in energy_types.split(',') if x.strip()]
        if energy_type_list:
            conditions.append(CarModel.energy_type.in_(energy_type_list))
    
    # 座位数筛选
    if seats:
        seat_list = [int(x.strip()) for x in seats.split(',') if x.strip()]
        if seat_list:
            conditions.append(CarModel.seats.in_(seat_list))
    
    # 车型级别筛选（通过关联的Series）
    if levels:
        level_list = [x.strip() for x in levels.split(',') if x.strip()]
        if level_list:
            if not (brand_ids):  # 如果还没有join series，需要join
                query = query.join(CarModel.series)
            conditions.append(Series.level.in_(level_list))
    
    # 应用所有筛选条件
    if conditions:
        query = query.where(and_(*conditions))
    
    # 获取总数（在排序和分页之前）
    count_query = select(func.count()).select_from(CarModel)
    if conditions:
        # 重新构建count查询的条件
        if brand_ids or levels:
            count_query = count_query.join(CarModel.series)
            if brand_ids:
                count_query = count_query.join(Series.brand)
        if conditions:
            count_query = count_query.where(and_(*conditions))
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # 排序（MySQL不支持NULLS LAST，使用CASE WHEN替代）
    if sort_by == "price_desc":
        query = query.order_by(CarModel.price.desc())
    elif sort_by == "price_asc":
        query = query.order_by(CarModel.price.asc())
    elif sort_by == "name_desc":
        query = query.order_by(CarModel.name.desc())
    else:  # name_asc
        query = query.order_by(CarModel.name.asc())
    
    # 分页
    query = query.offset((page - 1) * page_size).limit(page_size)
    
    # 执行查询
    result = await db.execute(query)
    car_models = result.unique().scalars().all()
    
    # 构建响应数据
    car_items = []
    for car in car_models:
        car_item = CarItemResponse(
            id=car.id,  # type: ignore
            name=car.name,  # type: ignore
            series_id=car.series_id,  # type: ignore
            series_name=car.series.name if car.series else "",
            brand_id=car.series.brand_id if car.series else 0,
            brand_name=car.series.brand.name if car.series and car.series.brand else "",
            price=car.price,  # type: ignore
            image=car.image,  # type: ignore
            energy_type=car.energy_type,  # type: ignore
            seats=car.seats,  # type: ignore
            level=car.series.level if car.series else None,
            description=car.description,  # type: ignore
            acceleration=car.acceleration,  # type: ignore
            fuel_consumption=car.fuel_consumption  # type: ignore
        )
        car_items.append(car_item)
    
    return PageResponse(
        code=200,
        message="success",
        data=car_items,
        total=total or 0,
        page=page,
        page_size=page_size
    )


@router.get("/cars/filters", summary="获取筛选条件选项")
async def get_filter_options(db: AsyncSession = Depends(get_async_db)):
    """
    获取所有可用的筛选条件选项
    用于前端动态生成筛选表单
    """
    # 获取所有能源类型
    energy_query = select(CarModel.energy_type).distinct().where(CarModel.energy_type.isnot(None))
    energy_result = await db.execute(energy_query)
    energy_types = [row[0] for row in energy_result.all() if row[0]]
    
    # 获取所有座位数
    seats_query = select(CarModel.seats).distinct().where(CarModel.seats.isnot(None)).order_by(CarModel.seats)
    seats_result = await db.execute(seats_query)
    seats_options = [row[0] for row in seats_result.all() if row[0]]
    
    # 获取所有车型级别
    levels_query = select(Series.level).distinct().where(Series.level.isnot(None))
    levels_result = await db.execute(levels_query)
    levels = [row[0] for row in levels_result.all() if row[0]]
    
    return {
        "energy_types": energy_types,
        "seats": seats_options,
        "levels": levels
    }
