from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.core.database import get_db
from app.services.car_service import CarService
from app.schemas.car import (
    CarSeriesListResponse,
    CarSeriesResponse,
    CarQueryParams,
    BrandResponse,
    FuelTypeEnum,
    CarModelEnum
)

router = APIRouter()


@router.get("/v1/cars", summary="获取车系列表")
async def get_cars(
    brand_name: Optional[str] = Query(None, description="品牌名称"),
    min_price: Optional[float] = Query(None, ge=0, description="最低价格（万元）"),
    max_price: Optional[float] = Query(None, ge=0, description="最高价格（万元）"),
    fuel_type: Optional[FuelTypeEnum] = Query(None, description="燃料类型"),
    car_model: Optional[CarModelEnum] = Query(None, description="车型类别"),
    min_score: Optional[float] = Query(None, ge=0, le=5, description="最低评分"),
    order_by: str = Query("total_score", description="排序字段: total_score, price_min, price_max"),
    order_direction: str = Query("desc", description="排序方向: asc, desc"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db)
):
    """
    获取车系列表（支持多条件筛选、排序、分页）
    
    ## 筛选条件
    - **brand_name**: 品牌名称（支持模糊搜索）
    - **min_price**: 最低价格
    - **max_price**: 最高价格
    - **fuel_type**: 燃料类型（纯电动、插电混动、增程式等）
    - **car_model**: 车型类别（轿车、SUV、MPV等）
    - **min_score**: 最低评分（0-5分）
    
    ## 排序
    - **order_by**: 排序字段（total_score, price_min, price_max）
    - **order_direction**: 排序方向（asc升序, desc降序）
    
    ## 分页
    - **page**: 页码（从1开始）
    - **page_size**: 每页数量（1-100）
    
    ## 示例
    ```
    GET /api/v1/cars?brand_name=比亚迪&min_price=15&max_price=30&fuel_type=纯电动&order_by=total_score&page=1&page_size=10
    ```
    """
    try:
        # 构建查询参数
        params = CarQueryParams(
            brand_name=brand_name,
            min_price=min_price,
            max_price=max_price,
            fuel_type=fuel_type,
            car_model=car_model,
            min_score=min_score,
            order_by=order_by,
            order_direction=order_direction,
            page=page,
            page_size=page_size
        )
        
        # 调用服务层获取数据
        items, pagination = await CarService.get_car_series_list(db, params)
        
        return CarSeriesListResponse(
            items=items,
            pagination=pagination
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.get("/v1/cars/{car_id}", summary="获取车系详情")
async def get_car_detail(
    car_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    根据ID获取车系详细信息
    
    ## 参数
    - **car_id**: 车系ID
    
    ## 返回
    包含品牌信息、车系信息、评分信息的完整数据
    
    ## 示例
    ```
    GET /api/v1/cars/1
    ```
    """
    try:
        car_series = await CarService.get_car_series_by_id(db, car_id)
        
        if not car_series:
            raise HTTPException(status_code=404, detail=f"车系ID {car_id} 不存在")
        
        return car_series
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.get("/v1/brands", summary="获取品牌列表")
async def get_brands(
    db: AsyncSession = Depends(get_db)
):
    """
    获取所有品牌列表
    
    ## 返回
    所有品牌的列表（按名称排序）
    
    ## 示例
    ```
    GET /api/v1/brands
    ```
    """
    try:
        brands = await CarService.get_brands_list(db)
        return brands
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")
