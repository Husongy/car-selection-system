"""
API V1 版本路由聚合
"""
from fastapi import APIRouter
from app.api.v1.endpoints import health, brands, cars, sales_ranking

# 创建V1版本的API路由
api_router = APIRouter()

# 注册各个端点路由
api_router.include_router(health.router, tags=["健康检查"])
api_router.include_router(brands.router, tags=["品牌管理"])
api_router.include_router(cars.router, tags=["车型查询"])
api_router.include_router(sales_ranking.router, tags=["销量榜单"])

__all__ = ["api_router"]
