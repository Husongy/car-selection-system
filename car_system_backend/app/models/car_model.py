"""
车型模型
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class CarModel(Base):
    """汽车车型表"""
    __tablename__ = "car_models"
    
    id = Column(Integer, primary_key=True, index=True, comment="车型ID")
    name = Column(String(200), nullable=False, index=True, comment="车型名称")
    series_id = Column(Integer, ForeignKey("series.id"), nullable=False, comment="车系ID")
    price = Column(Float, comment="指导价(万元)")
    year = Column(String(20), comment="年款")
    image = Column(String(500), comment="车型图片")
    
    # 基本参数
    energy_type = Column(String(50), comment="能源类型")
    transmission = Column(String(100), comment="变速箱")
    engine = Column(String(100), comment="发动机")
    max_power = Column(String(50), comment="最大功率(kW)")
    max_torque = Column(String(50), comment="最大扭矩(N·m)")
    
    # 车身参数
    length = Column(Integer, comment="车身长度(mm)")
    width = Column(Integer, comment="车身宽度(mm)")
    height = Column(Integer, comment="车身高度(mm)")
    wheelbase = Column(Integer, comment="轴距(mm)")
    seats = Column(Integer, comment="座位数")
    
    # 性能参数
    max_speed = Column(Integer, comment="最高车速(km/h)")
    acceleration = Column(Float, comment="百公里加速(s)")
    fuel_consumption = Column(Float, comment="综合油耗(L/100km)")
    
    description = Column(Text, comment="车型描述")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关联车系
    series = relationship("Series", back_populates="models")
    
    def __repr__(self):
        return f"<CarModel(id={self.id}, name={self.name})>"
