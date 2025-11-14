"""
品牌相关Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BrandBase(BaseModel):
    """品牌基础模型"""
    name: str = Field(..., description="品牌名称", max_length=100)
    logo: Optional[str] = Field(None, description="品牌Logo URL", max_length=500)
    initial: Optional[str] = Field(None, description="首字母", max_length=1)
    description: Optional[str] = Field(None, description="品牌描述")
    country: Optional[str] = Field(None, description="所属国家", max_length=50)
    website: Optional[str] = Field(None, description="官方网站", max_length=200)


class BrandCreate(BrandBase):
    """创建品牌模型"""
    pass


class BrandUpdate(BaseModel):
    """更新品牌模型"""
    name: Optional[str] = Field(None, description="品牌名称", max_length=100)
    logo: Optional[str] = Field(None, description="品牌Logo URL", max_length=500)
    initial: Optional[str] = Field(None, description="首字母", max_length=1)
    description: Optional[str] = Field(None, description="品牌描述")
    country: Optional[str] = Field(None, description="所属国家", max_length=50)
    website: Optional[str] = Field(None, description="官方网站", max_length=200)


class BrandInDB(BrandBase):
    """数据库品牌模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BrandResponse(BrandInDB):
    """品牌响应模型"""
    series_count: Optional[int] = Field(0, description="车系数量")
