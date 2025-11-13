from fastapi import APIRouter
from app.api.v1.endpoints import health, cars

api_router = APIRouter()

# 注册健康检查路由
api_router.include_router(health.router, tags=["健康检查"])

# 注册车系管理路由（不使用prefix）
api_router.include_router(cars.router, tags=["车系管理"])
