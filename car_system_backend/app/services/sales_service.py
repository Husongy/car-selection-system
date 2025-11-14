"""
销量数据服务层
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, desc
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import List, Tuple
from app.models.sales_data import SalesData
from app.models.series import Series
from app.models.brand import Brand
from app.schemas.sales import SalesRankingItem, SalesRankingResponse


class SalesService:
    """销量数据服务"""
    
    @staticmethod
    def _parse_period(period: str) -> Tuple[str, str]:
        """
        解析周期参数，返回开始和结束日期
        
        Args:
            period: 周期参数 (last_year, last_6months, last_3months, YYYY-MM)
            
        Returns:
            (start_date, end_date) 格式: YYYY-MM
        """
        now = datetime.now()
        
        if period == 'last_year':
            # 近一年
            start = now - relativedelta(years=1)
            end = now
        elif period == 'last_6months':
            # 近半年
            start = now - relativedelta(months=6)
            end = now
        elif period == 'last_3months':
            # 近三个月
            start = now - relativedelta(months=3)
            end = now
        elif period == 'last_month':
            # 上个月
            start = now - relativedelta(months=1)
            end = now - relativedelta(months=1)
        else:
            # 自定义月份 YYYY-MM
            try:
                date = datetime.strptime(period, '%Y-%m')
                start = date
                end = date
            except ValueError:
                # 默认返回近一年
                start = now - relativedelta(years=1)
                end = now
        
        start_str = start.strftime('%Y-%m')
        end_str = end.strftime('%Y-%m')
        
        return start_str, end_str
    
    @staticmethod
    async def get_sales_ranking(
        db: AsyncSession,
        period: str = 'last_year',
        limit: int = 50
    ) -> SalesRankingResponse:
        """
        获取销量排名
        
        Args:
            db: 数据库会话
            period: 查询周期
            limit: 返回数量限制
            
        Returns:
            销量排名响应
        """
        # 解析周期
        start_date, end_date = SalesService._parse_period(period)
        
        # 构建查询：按车系聚合销量
        query = (
            select(
                SalesData.series_id,
                func.sum(SalesData.sales_count).label('total_sales'),
                Series.name.label('series_name'),
                Series.image.label('series_image'),
                Series.price_min,
                Series.price_max,
                Series.energy_type,
                Brand.name.label('brand_name')
            )
            .join(Series, SalesData.series_id == Series.id)
            .join(Brand, Series.brand_id == Brand.id)
            .where(
                and_(
                    SalesData.period >= start_date,
                    SalesData.period <= end_date
                )
            )
            .group_by(
                SalesData.series_id,
                Series.name,
                Series.image,
                Series.price_min,
                Series.price_max,
                Series.energy_type,
                Brand.name
            )
            .order_by(desc('total_sales'))
            .limit(limit)
        )
        
        result = await db.execute(query)
        rows = result.all()
        
        # 构建排名列表
        ranking_items = []
        for rank, row in enumerate(rows, start=1):
            # 格式化价格区间
            price_range = None
            if row.price_min and row.price_max:
                price_range = f"{row.price_min:.2f}-{row.price_max:.2f}万"
            elif row.price_min:
                price_range = f"{row.price_min:.2f}万起"
            
            item = SalesRankingItem(
                rank=rank,
                series_id=row.series_id,
                series_name=row.series_name,
                brand_name=row.brand_name,
                total_sales=row.total_sales or 0,
                series_image=row.series_image,
                price_range=price_range,
                energy_type=row.energy_type
            )
            ranking_items.append(item)
        
        return SalesRankingResponse(
            period=period,
            start_date=start_date,
            end_date=end_date,
            total_count=len(ranking_items),
            data=ranking_items
        )
    
    @staticmethod
    async def create_sales_data(
        db: AsyncSession,
        series_id: int,
        sales_count: int,
        year: int,
        month: int
    ) -> SalesData:
        """
        创建销量数据
        
        Args:
            db: 数据库会话
            series_id: 车系ID
            sales_count: 销量
            year: 年份
            month: 月份
            
        Returns:
            销量数据对象
        """
        period = f"{year}-{month:02d}"
        
        # 检查是否已存在
        query = select(SalesData).where(
            and_(
                SalesData.series_id == series_id,
                SalesData.period == period
            )
        )
        result = await db.execute(query)
        existing = result.scalar_one_or_none()
        
        if existing:
            # 更新销量
            existing.sales_count = sales_count
            existing.updated_at = datetime.now()
            await db.commit()
            await db.refresh(existing)
            return existing
        else:
            # 创建新记录
            sales_data = SalesData(
                series_id=series_id,
                sales_count=sales_count,
                year=year,
                month=month,
                period=period
            )
            db.add(sales_data)
            await db.commit()
            await db.refresh(sales_data)
            return sales_data
