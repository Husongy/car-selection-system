"""
销量数据验证模式
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SalesDataBase(BaseModel):
    """销量数据基础模型"""
    series_id: int = Field(..., description="车系ID")
    sales_count: int = Field(..., ge=0, description="销量数量")
    year: int = Field(..., ge=2000, le=2100, description="年份")
    month: int = Field(..., ge=1, le=12, description="月份")
    period: str = Field(..., description="销售周期(YYYY-MM)")


class SalesDataCreate(SalesDataBase):
    """创建销量数据"""
    pass


class SalesDataResponse(SalesDataBase):
    """销量数据响应"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SalesRankingItem(BaseModel):
    """销量排名项"""
    rank: int = Field(..., description="排名")
    series_id: int = Field(..., description="车系ID")
    series_name: str = Field(..., description="车系名称")
    brand_name: str = Field(..., description="品牌名称")
    total_sales: int = Field(..., description="总销量")
    series_image: Optional[str] = Field(None, description="车系图片")
    price_range: Optional[str] = Field(None, description="价格区间")
    energy_type: Optional[str] = Field(None, description="能源类型")


class SalesRankingResponse(BaseModel):
    """销量排名响应"""
    period: str = Field(..., description="查询周期")
    start_date: str = Field(..., description="开始日期")
    end_date: str = Field(..., description="结束日期")
    total_count: int = Field(..., description="总记录数")
    data: list[SalesRankingItem] = Field(..., description="排名列表")
