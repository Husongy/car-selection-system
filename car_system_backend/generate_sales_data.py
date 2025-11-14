"""
生成模拟销量数据
用于演示销量榜单功能
"""
import asyncio
import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.series import Series
from app.models.sales_data import SalesData


async def generate_sales_data():
    """生成模拟销量数据"""
    async with AsyncSessionLocal() as db:
        # 获取所有车系
        result = await db.execute(select(Series))
        all_series = result.scalars().all()
        
        if not all_series:
            print("错误: 数据库中没有车系数据，请先运行爬虫抓取数据")
            return
        
        print(f"找到 {len(all_series)} 个车系")
        
        # 生成近12个月的销量数据
        now = datetime.now()
        months_to_generate = 12
        
        created_count = 0
        
        for i in range(months_to_generate):
            # 计算目标月份
            target_date = now - relativedelta(months=i)
            year = target_date.year
            month = target_date.month
            period = f"{year}-{month:02d}"
            
            print(f"\n生成 {period} 的销量数据...")
            
            # 为每个车系生成销量数据
            for series in all_series:
                # 随机生成销量（模拟真实情况，有些车系销量高，有些低）
                # 基础销量范围: 100-50000
                base_sales = random.randint(100, 50000)
                
                # 添加季节性波动（例如：年底销量较高）
                if month in [11, 12, 1, 2]:  # 年底和春节期间
                    base_sales = int(base_sales * random.uniform(1.2, 1.5))
                
                # 检查是否已存在
                existing = await db.execute(
                    select(SalesData).where(
                        SalesData.series_id == series.id,
                        SalesData.period == period
                    )
                )
                existing_data = existing.scalar_one_or_none()
                
                if existing_data:
                    # 更新现有数据
                    existing_data.sales_count = base_sales
                    existing_data.updated_at = datetime.now()
                else:
                    # 创建新数据
                    sales_data = SalesData(
                        series_id=series.id,
                        sales_count=base_sales,
                        year=year,
                        month=month,
                        period=period
                    )
                    db.add(sales_data)
                    created_count += 1
            
            # 提交当月数据
            await db.commit()
            print(f"✓ {period} 数据生成完成")
        
        print(f"\n成功生成 {created_count} 条销量记录")
        print(f"覆盖时间范围: {months_to_generate} 个月")


async def show_top_sales():
    """显示销量前10的车系"""
    async with AsyncSessionLocal() as db:
        from sqlalchemy import func, desc
        from app.models.brand import Brand
        
        # 查询近一年销量前10
        now = datetime.now()
        start_date = (now - relativedelta(years=1)).strftime('%Y-%m')
        end_date = now.strftime('%Y-%m')
        
        query = (
            select(
                Series.name,
                Brand.name.label('brand_name'),
                func.sum(SalesData.sales_count).label('total_sales')
            )
            .join(Series, SalesData.series_id == Series.id)
            .join(Brand, Series.brand_id == Brand.id)
            .where(
                SalesData.period >= start_date,
                SalesData.period <= end_date
            )
            .group_by(Series.name, Brand.name)
            .order_by(desc('total_sales'))
            .limit(10)
        )
        
        result = await db.execute(query)
        rows = result.all()
        
        print("\n" + "="*60)
        print("近一年销量排行榜 TOP 10")
        print("="*60)
        print(f"{'排名':<6} {'品牌':<15} {'车系':<20} {'总销量':<15}")
        print("-"*60)
        
        for rank, row in enumerate(rows, start=1):
            print(f"{rank:<6} {row.brand_name:<15} {row.name:<20} {row.total_sales:>12,} 辆")
        
        print("="*60)


if __name__ == "__main__":
    print("开始生成模拟销量数据...\n")
    asyncio.run(generate_sales_data())
    print("\n数据生成完成！\n")
    
    print("查询销量排行榜...\n")
    asyncio.run(show_top_sales())
