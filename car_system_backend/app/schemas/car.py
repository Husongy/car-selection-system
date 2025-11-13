from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# 枚举类型定义
class FuelTypeEnum(str, Enum):
    """燃料类型枚举"""
    ELECTRIC = "纯电动"
    HYBRID = "插电混动"
    PHEV = "增程式"
    MILD_HYBRID = "油电混动"
    GASOLINE = "汽油"
    DIESEL = "柴油"


class CarModelEnum(str, Enum):
    """车型类别枚举"""
    SEDAN = "轿车"
    SUV = "SUV"
    MPV = "MPV"
    COUPE = "跑车"
    HATCHBACK = "两厢车"
    WAGON = "旅行车"
    PICKUP = "皮卡"


# 品牌相关 Schema
class BrandBase(BaseModel):
    """品牌基础模型"""
    name: str
    logo_url: Optional[str] = None


class BrandResponse(BrandBase):
    """品牌响应模型"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# 车系评分 Schema
class CarSeriesScoreResponse(BaseModel):
    """车系评分响应模型"""
    comfort_score: float = 0.0
    appearance_score: float = 0.0
    config_score: float = 0.0
    control_score: float = 0.0
    power_score: float = 0.0
    space_score: float = 0.0
    interior_score: float = 0.0
    total_score: float = 0.0
    
    class Config:
        from_attributes = True


# 车系相关 Schema
class CarSeriesBase(BaseModel):
    """车系基础模型"""
    name: str
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    fuel_type: FuelTypeEnum
    seat_count: Optional[int] = None
    car_model: Optional[CarModelEnum] = None
    image_url: Optional[str] = None


class CarSeriesResponse(CarSeriesBase):
    """车系响应模型（详细信息）"""
    id: int
    brand_id: int
    brand: BrandResponse
    scores: Optional[CarSeriesScoreResponse] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CarSeriesSimpleResponse(BaseModel):
    """车系简单响应模型（列表使用）"""
    id: int
    name: str
    brand_name: str
    brand_logo_url: Optional[str] = None
    price_min: Optional[float] = None
    price_max: Optional[float] = None
    fuel_type: str
    car_model: Optional[str] = None
    image_url: Optional[str] = None
    total_score: Optional[float] = 0.0
    
    class Config:
        from_attributes = True


# 查询参数 Schema
class CarQueryParams(BaseModel):
    """车系查询参数模型"""
    # 筛选条件
    brand_name: Optional[str] = Field(None, description="品牌名称")
    min_price: Optional[float] = Field(None, ge=0, description="最低价格（万元）")
    max_price: Optional[float] = Field(None, ge=0, description="最高价格（万元）")
    fuel_type: Optional[FuelTypeEnum] = Field(None, description="燃料类型")
    car_model: Optional[CarModelEnum] = Field(None, description="车型类别")
    min_score: Optional[float] = Field(None, ge=0, le=5, description="最低评分")
    
    # 排序
    order_by: Optional[str] = Field("total_score", description="排序字段: total_score, price_min, price_max")
    order_direction: Optional[str] = Field("desc", description="排序方向: asc, desc")
    
    # 分页
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页数量")
    
    class Config:
        json_schema_extra = {
            "example": {
                "brand_name": "比亚迪",
                "min_price": 10.0,
                "max_price": 30.0,
                "fuel_type": "纯电动",
                "order_by": "total_score",
                "order_direction": "desc",
                "page": 1,
                "page_size": 10
            }
        }


# 分页响应 Schema
class PaginationResponse(BaseModel):
    """分页响应模型"""
    total: int = Field(..., description="总记录数")
    page: int = Field(..., description="当前页码")
    page_size: int = Field(..., description="每页数量")
    total_pages: int = Field(..., description="总页数")
    has_next: bool = Field(..., description="是否有下一页")
    has_prev: bool = Field(..., description="是否有上一页")


class CarSeriesListResponse(BaseModel):
    """车系列表响应模型"""
    items: List[CarSeriesSimpleResponse]
    pagination: PaginationResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "name": "海豹",
                        "brand_name": "比亚迪",
                        "price_min": 18.98,
                        "price_max": 28.68,
                        "fuel_type": "纯电动",
                        "car_model": "轿车",
                        "total_score": 4.5
                    }
                ],
                "pagination": {
                    "total": 100,
                    "page": 1,
                    "page_size": 10,
                    "total_pages": 10,
                    "has_next": True,
                    "has_prev": False
                }
            }
        }
