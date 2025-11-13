#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据验证脚本 - 验证爬取数据的完整性和准确性
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../car_system_backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.car import Brand, CarSeries, CarSeriesScore

# 数据库配置
DATABASE_URL = "mysql+pymysql://root:root@localhost:3307/car_system"


def verify_data():
    """验证数据库中的数据"""
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    print("=" * 60)
    print("🔍 数据验证报告")
    print("=" * 60)
    
    # 1. 统计数据量
    brand_count = session.query(Brand).count()
    series_count = session.query(CarSeries).count()
    score_count = session.query(CarSeriesScore).count()
    
    print(f"\n📊 数据统计:")
    print(f"  品牌数量: {brand_count}")
    print(f"  车系数量: {series_count}")
    print(f"  评分记录: {score_count}")
    
    # 2. 检查数据完整性
    print(f"\n✅ 数据完整性检查:")
    
    # 检查是否有车系没有品牌
    orphan_series = session.query(CarSeries).filter(
        CarSeries.brand_id.is_(None)
    ).count()
    if orphan_series == 0:
        print(f"  ✓ 所有车系都有关联品牌")
    else:
        print(f"  ✗ 有 {orphan_series} 个车系缺少品牌关联")
    
    # 检查是否有车系没有评分
    series_without_score = series_count - score_count
    if series_without_score == 0:
        print(f"  ✓ 所有车系都有评分数据")
    else:
        print(f"  ⚠ 有 {series_without_score} 个车系缺少评分")
    
    # 3. 数据样本展示
    print(f"\n📋 数据样本（前5条）:")
    print("-" * 60)
    
    series_list = session.query(CarSeries).limit(5).all()
    for series in series_list:
        print(f"\n  品牌: {series.brand.name}")
        print(f"  车系: {series.name}")
        print(f"  价格: {series.price_min}-{series.price_max} 万元")
        print(f"  类型: {series.fuel_type.value} / {series.car_model.value if series.car_model else 'N/A'}")
        if series.scores:
            print(f"  评分: {series.scores.total_score}")
    
    # 4. 数据异常检查
    print(f"\n⚠️  数据异常检查:")
    
    # 检查价格异常
    abnormal_price = session.query(CarSeries).filter(
        CarSeries.price_min > CarSeries.price_max
    ).count()
    if abnormal_price == 0:
        print(f"  ✓ 价格数据正常")
    else:
        print(f"  ✗ 有 {abnormal_price} 个车系价格异常（最低价>最高价）")
    
    # 检查评分异常
    abnormal_score = session.query(CarSeriesScore).filter(
        (CarSeriesScore.total_score < 0) | (CarSeriesScore.total_score > 5)
    ).count()
    if abnormal_score == 0:
        print(f"  ✓ 评分数据正常（0-5分范围内）")
    else:
        print(f"  ✗ 有 {abnormal_score} 个评分超出范围")
    
    # 5. 品牌分布
    print(f"\n📈 品牌分布:")
    print("-" * 60)
    
    brands = session.query(Brand).all()
    for brand in brands:
        count = session.query(CarSeries).filter(CarSeries.brand_id == brand.id).count()
        print(f"  {brand.name}: {count} 个车系")
    
    print("\n" + "=" * 60)
    print("验证完成！")
    print("=" * 60)
    
    session.close()


if __name__ == '__main__':
    try:
        verify_data()
    except Exception as e:
        print(f"\n❌ 验证失败: {e}")
        import traceback
        traceback.print_exc()
