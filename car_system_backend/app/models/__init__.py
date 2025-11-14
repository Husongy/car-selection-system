"""
数据模型模块
导出所有数据库模型，便于Alembic自动检测
"""
from app.core.database import Base
from app.models.brand import Brand
from app.models.series import Series
from app.models.car_model import CarModel

__all__ = ["Base", "Brand", "Series", "CarModel"]
