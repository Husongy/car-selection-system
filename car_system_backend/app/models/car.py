from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base


class Brand(Base):
    """品牌模型"""
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True, comment="品牌ID")
    name = Column(String(100), unique=True, nullable=False, index=True, comment="品牌名称")
    logo_url = Column(String(500), comment="品牌Logo URL")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系：一个品牌有多个车系
    car_series = relationship("CarSeries", back_populates="brand", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Brand(id={self.id}, name={self.name})>"


class FuelType(str, enum.Enum):
    """燃料类型枚举"""
    ELECTRIC = "纯电动"
    HYBRID = "插电混动"
    PHEV = "增程式"
    MILD_HYBRID = "油电混动"
    GASOLINE = "汽油"
    DIESEL = "柴油"


class CarModel(str, enum.Enum):
    """车型类别枚举"""
    SEDAN = "轿车"
    SUV = "SUV"
    MPV = "MPV"
    COUPE = "跑车"
    HATCHBACK = "两厢车"
    WAGON = "旅行车"
    PICKUP = "皮卡"


class CarSeries(Base):
    """车系模型"""
    __tablename__ = "car_series"

    id = Column(Integer, primary_key=True, index=True, comment="车系ID")
    name = Column(String(200), nullable=False, index=True, comment="车系名称")
    brand_id = Column(Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False, comment="品牌ID")
    price_min = Column(Float, comment="最低价格(万元)")
    price_max = Column(Float, comment="最高价格(万元)")
    fuel_type = Column(SQLEnum(FuelType), nullable=False, comment="燃料类型")
    seat_count = Column(Integer, comment="座位数")
    car_model = Column(SQLEnum(CarModel), comment="车型类别")
    image_url = Column(String(500), comment="车系图片URL")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系
    brand = relationship("Brand", back_populates="car_series")
    scores = relationship("CarSeriesScore", back_populates="car_series", cascade="all, delete-orphan", uselist=False)
    sales_data = relationship("SalesData", back_populates="car_series", cascade="all, delete-orphan")
    complaints = relationship("ComplaintData", back_populates="car_series", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<CarSeries(id={self.id}, name={self.name}, brand_id={self.brand_id})>"


class CarSeriesScore(Base):
    """车系评分模型"""
    __tablename__ = "car_series_scores"

    id = Column(Integer, primary_key=True, index=True, comment="评分ID")
    car_series_id = Column(Integer, ForeignKey("car_series.id", ondelete="CASCADE"), nullable=False, unique=True, comment="车系ID")
    comfort_score = Column(Float, default=0.0, comment="舒适性评分")
    appearance_score = Column(Float, default=0.0, comment="外观评分")
    config_score = Column(Float, default=0.0, comment="配置评分")
    control_score = Column(Float, default=0.0, comment="操控评分")
    power_score = Column(Float, default=0.0, comment="动力评分")
    space_score = Column(Float, default=0.0, comment="空间评分")
    interior_score = Column(Float, default=0.0, comment="内饰评分")
    total_score = Column(Float, default=0.0, comment="总分")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系：一对一关联车系
    car_series = relationship("CarSeries", back_populates="scores")

    def __repr__(self):
        return f"<CarSeriesScore(car_series_id={self.car_series_id}, total_score={self.total_score})>"


class SalesData(Base):
    """销量数据模型"""
    __tablename__ = "sales_data"

    id = Column(Integer, primary_key=True, index=True, comment="销量数据ID")
    car_series_id = Column(Integer, ForeignKey("car_series.id", ondelete="CASCADE"), nullable=False, index=True, comment="车系ID")
    date = Column(String(7), nullable=False, index=True, comment="年月(格式: YYYY-MM)")
    sales_volume = Column(Integer, default=0, comment="销量")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系
    car_series = relationship("CarSeries", back_populates="sales_data")

    # 联合唯一索引：确保同一车系同一月份只有一条记录
    __table_args__ = (
        {'comment': '销量数据表'},
    )

    def __repr__(self):
        return f"<SalesData(car_series_id={self.car_series_id}, date={self.date}, sales={self.sales_volume})>"


class ProblemType(str, enum.Enum):
    """问题类型枚举"""
    QUALITY = "质量"
    SERVICE = "服务"
    OTHER = "其他"


class ComplaintData(Base):
    """投诉数据模型"""
    __tablename__ = "complaint_data"

    id = Column(Integer, primary_key=True, index=True, comment="投诉数据ID")
    car_series_id = Column(Integer, ForeignKey("car_series.id", ondelete="CASCADE"), nullable=False, index=True, comment="车系ID")
    date = Column(String(7), nullable=False, index=True, comment="年月(格式: YYYY-MM)")
    problem_type = Column(SQLEnum(ProblemType), nullable=False, comment="问题类型")
    problem_description = Column(Text, comment="问题描述")
    complaint_count = Column(Integer, default=0, comment="投诉量")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")

    # 关系
    car_series = relationship("CarSeries", back_populates="complaints")

    __table_args__ = (
        {'comment': '投诉数据表'},
    )

    def __repr__(self):
        return f"<ComplaintData(car_series_id={self.car_series_id}, date={self.date}, type={self.problem_type})>"
