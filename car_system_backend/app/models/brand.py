"""
品牌模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Brand(Base):
    """汽车品牌表"""
    __tablename__ = "brands"
    
    id = Column(Integer, primary_key=True, index=True, comment="品牌ID")
    name = Column(String(100), nullable=False, unique=True, index=True, comment="品牌名称")
    logo = Column(String(500), comment="品牌Logo URL")
    initial = Column(String(1), index=True, comment="首字母")
    description = Column(Text, comment="品牌描述")
    country = Column(String(50), comment="所属国家")
    website = Column(String(200), comment="官方网站")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关联车系
    series = relationship("Series", back_populates="brand", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Brand(id={self.id}, name={self.name})>"
