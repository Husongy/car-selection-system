"""
销量数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class SalesData(Base):
    """销量数据表"""
    __tablename__ = "sales_data"
    
    id = Column(Integer, primary_key=True, index=True, comment="销量记录ID")
    series_id = Column(Integer, ForeignKey("series.id"), nullable=False, comment="车系ID")
    sales_count = Column(Integer, nullable=False, default=0, comment="销量数量")
    year = Column(Integer, nullable=False, comment="年份")
    month = Column(Integer, nullable=False, comment="月份")
    period = Column(String(20), nullable=False, index=True, comment="销售周期(YYYY-MM)")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关联车系
    series = relationship("Series", backref="sales_records")
    
    # 创建复合索引，优化查询性能
    __table_args__ = (
        Index('idx_series_period', 'series_id', 'period'),
        Index('idx_year_month', 'year', 'month'),
    )
    
    def __repr__(self):
        return f"<SalesData(series_id={self.series_id}, period={self.period}, sales={self.sales_count})>"
