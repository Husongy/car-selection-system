"""
车系模型
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Series(Base):
    """汽车车系表"""
    __tablename__ = "series"
    
    id = Column(Integer, primary_key=True, index=True, comment="车系ID")
    name = Column(String(100), nullable=False, index=True, comment="车系名称")
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False, comment="品牌ID")
    image = Column(String(500), comment="车系图片")
    price_min = Column(Float, comment="最低价格(万元)")
    price_max = Column(Float, comment="最高价格(万元)")
    level = Column(String(50), comment="车型级别")
    energy_type = Column(String(50), comment="能源类型")
    description = Column(Text, comment="车系描述")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关联品牌
    brand = relationship("Brand", back_populates="series")
    
    # 关联车型
    models = relationship("CarModel", back_populates="series", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Series(id={self.id}, name={self.name})>"
