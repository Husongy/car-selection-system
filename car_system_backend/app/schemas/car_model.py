"""
车型相关Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CarModelBase(BaseModel):
    """车型基础模型"""
    name: str = Field(..., description="车型名称", max_length=200)
    series_id: int = Field(..., description="车系ID")
    price: Optional[float] = Field(None, description="指导价(万元)")
    year: Optional[str] = Field(None, description="年款", max_length=20)
    image: Optional[str] = Field(None, description="车型图片", max_length=500)
    energy_type: Optional[str] = Field(None, description="能源类型", max_length=50)
    transmission: Optional[str] = Field(None, description="变速箱", max_length=100)
    engine: Optional[str] = Field(None, description="发动机", max_length=100)
    max_power: Optional[str] = Field(None, description="最大功率(kW)", max_length=50)
    max_torque: Optional[str] = Field(None, description="最大扭矩(N·m)", max_length=50)
    length: Optional[int] = Field(None, description="车身长度(mm)")
    width: Optional[int] = Field(None, description="车身宽度(mm)")
    height: Optional[int] = Field(None, description="车身高度(mm)")
    wheelbase: Optional[int] = Field(None, description="轴距(mm)")
    seats: Optional[int] = Field(None, description="座位数")
    max_speed: Optional[int] = Field(None, description="最高车速(km/h)")
    acceleration: Optional[float] = Field(None, description="百公里加速(s)")
    fuel_consumption: Optional[float] = Field(None, description="综合油耗(L/100km)")
    description: Optional[str] = Field(None, description="车型描述")


class CarModelCreate(CarModelBase):
    """创建车型模型"""
    pass


class CarModelUpdate(BaseModel):
    """更新车型模型"""
    name: Optional[str] = Field(None, description="车型名称", max_length=200)
    series_id: Optional[int] = Field(None, description="车系ID")
    price: Optional[float] = Field(None, description="指导价(万元)")
    year: Optional[str] = Field(None, description="年款", max_length=20)
    image: Optional[str] = Field(None, description="车型图片", max_length=500)
    energy_type: Optional[str] = Field(None, description="能源类型", max_length=50)
    transmission: Optional[str] = Field(None, description="变速箱", max_length=100)
    engine: Optional[str] = Field(None, description="发动机", max_length=100)
    max_power: Optional[str] = Field(None, description="最大功率(kW)", max_length=50)
    max_torque: Optional[str] = Field(None, description="最大扭矩(N·m)", max_length=50)
    length: Optional[int] = Field(None, description="车身长度(mm)")
    width: Optional[int] = Field(None, description="车身宽度(mm)")
    height: Optional[int] = Field(None, description="车身高度(mm)")
    wheelbase: Optional[int] = Field(None, description="轴距(mm)")
    seats: Optional[int] = Field(None, description="座位数")
    max_speed: Optional[int] = Field(None, description="最高车速(km/h)")
    acceleration: Optional[float] = Field(None, description="百公里加速(s)")
    fuel_consumption: Optional[float] = Field(None, description="综合油耗(L/100km)")
    description: Optional[str] = Field(None, description="车型描述")


class CarModelInDB(CarModelBase):
    """数据库车型模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CarModelResponse(CarModelInDB):
    """车型响应模型"""
    series_name: Optional[str] = Field(None, description="车系名称")
    brand_name: Optional[str] = Field(None, description="品牌名称")
