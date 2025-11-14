"""
健康检查接口
用于验证后端服务是否正常运行
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_async_db
from app.models.car_model import CarModel
from app.models.series import Series
from app.models.brand import Brand

router = APIRouter()


@router.get("/health", summary="健康检查")
async def health_check():
    """
    健康检查接口
    返回服务运行状态
    """
    return {
        "status": "ok",
        "message": "Backend is running!"
    }


@router.get("/statistics", summary="获取统计数据")
async def get_statistics(db: AsyncSession = Depends(get_async_db)):
    """
    获取系统统计数据
    包括车型总数、品牌总数、车系总数等
    """
    try:
        # 获取车型总数
        car_count_query = select(func.count(CarModel.id))
        car_result = await db.execute(car_count_query)
        car_count = car_result.scalar() or 0
        
        # 获取品牌总数
        brand_count_query = select(func.count(Brand.id))
        brand_result = await db.execute(brand_count_query)
        brand_count = brand_result.scalar() or 0
        
        # 获取车系总数
        series_count_query = select(func.count(Series.id))
        series_result = await db.execute(series_count_query)
        series_count = series_result.scalar() or 0
        
        return {
            "car_count": car_count,
            "brand_count": brand_count,
            "series_count": series_count,
            "visit_count": 0  # 暂时固定为0，后续可以接入真实访问统计
        }
    except Exception as e:
        return {
            "car_count": 0,
            "brand_count": 0,
            "series_count": 0,
            "visit_count": 0
        }
