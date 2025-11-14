"""
车系相关Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SeriesBase(BaseModel):
    """车系基础模型"""
    name: str = Field(..., description="车系名称", max_length=100)
    brand_id: int = Field(..., description="品牌ID")
    image: Optional[str] = Field(None, description="车系图片", max_length=500)
    price_min: Optional[float] = Field(None, description="最低价格(万元)")
    price_max: Optional[float] = Field(None, description="最高价格(万元)")
    level: Optional[str] = Field(None, description="车型级别", max_length=50)
    energy_type: Optional[str] = Field(None, description="能源类型", max_length=50)
    description: Optional[str] = Field(None, description="车系描述")


class SeriesCreate(SeriesBase):
    """创建车系模型"""
    pass


class SeriesUpdate(BaseModel):
    """更新车系模型"""
    name: Optional[str] = Field(None, description="车系名称", max_length=100)
    brand_id: Optional[int] = Field(None, description="品牌ID")
    image: Optional[str] = Field(None, description="车系图片", max_length=500)
    price_min: Optional[float] = Field(None, description="最低价格(万元)")
    price_max: Optional[float] = Field(None, description="最高价格(万元)")
    level: Optional[str] = Field(None, description="车型级别", max_length=50)
    energy_type: Optional[str] = Field(None, description="能源类型", max_length=50)
    description: Optional[str] = Field(None, description="车系描述")


class SeriesInDB(SeriesBase):
    """数据库车系模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SeriesResponse(SeriesInDB):
    """车系响应模型"""
    brand_name: Optional[str] = Field(None, description="品牌名称")
    model_count: Optional[int] = Field(0, description="车型数量")
