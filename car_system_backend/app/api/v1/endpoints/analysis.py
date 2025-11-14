"""
可视化分析API接口
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from app.core.database import get_async_db
from app.models.series import Series
from app.models.brand import Brand
from app.schemas.response import Response
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/analysis")


class PriceDiscountItem(BaseModel):
    """降价排行项"""
    series_name: str
    discount: float  # 降价金额


class BrandCountItem(BaseModel):
    """品牌车系数量项"""
    brand_name: str
    count: int


class PriceRangeItem(BaseModel):
    """价格区间数量项"""
    range: str
    count: int


@router.get("/price-discount", response_model=Response[List[PriceDiscountItem]])
async def get_price_discount_ranking(
    limit: int = 30,
    db: AsyncSession = Depends(get_async_db)
):
    """
    获取车系降价排行榜
    降价金额 = price_max - price_min（官方价 - 经销商价）
    """
    # 查询所有有价格的车系，计算降价金额并排序
    query = select(
        Series.name,
        (Series.price_max - Series.price_min).label('discount')
    ).where(
        Series.price_min.isnot(None),
        Series.price_max.isnot(None),
        Series.price_max > Series.price_min
    ).order_by(
        (Series.price_max - Series.price_min).desc()
    ).limit(limit)
    
    result = await db.execute(query)
    rows = result.all()
    
    data = [
        PriceDiscountItem(
            series_name=row.name,
            discount=round(float(row.discount), 2)
        )
        for row in rows
    ]
    
    return Response(
        code=200,
        message="查询成功",
        data=data
    )


@router.get("/brand-count", response_model=Response[List[BrandCountItem]])
async def get_brand_count_distribution(
    limit: int = 30,
    db: AsyncSession = Depends(get_async_db)
):
    """
    获取品牌车系数量分布（TOP N）
    """
    # 统计每个品牌的车系数量
    query = select(
        Brand.name,
        func.count(Series.id).label('count')
    ).join(
        Series, Brand.id == Series.brand_id
    ).group_by(
        Brand.id, Brand.name
    ).order_by(
        func.count(Series.id).desc()
    ).limit(limit)
    
    result = await db.execute(query)
    rows = result.all()
    
    data = []
    for row in rows:
        data.append(
            BrandCountItem(
                brand_name=row.name,  # type: ignore
                count=row.count  # type: ignore
            )
        )
    
    return Response(
        code=200,
        message="查询成功",
        data=data
    )


@router.get("/price-range", response_model=Response[List[PriceRangeItem]])
async def get_price_range_distribution(
    db: AsyncSession = Depends(get_async_db)
):
    """
    获取价格区间分布
    根据price_min字段统计不同价格区间的车系数量
    """
    # 定义价格区间
    price_ranges = [
        ('0-10万', 0, 10),
        ('10-15万', 10, 15),
        ('15-20万', 15, 20),
        ('20-30万', 20, 30),
        ('30-50万', 30, 50),
        ('50-100万', 50, 100),
        ('100万以上', 100, 9999)
    ]
    
    data = []
    
    for range_name, min_price, max_price in price_ranges:
        # 统计每个价格区间的车系数量
        query = select(func.count(Series.id)).where(
            Series.price_min.isnot(None),
            Series.price_min >= min_price,
            Series.price_min < max_price
        )
        
        result = await db.execute(query)
        count = result.scalar() or 0
        
        data.append(
            PriceRangeItem(
                range=range_name,
                count=count
            )
        )
    
    return Response(
        code=200,
        message="查询成功",
        data=data
    )
