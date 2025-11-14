"""
销量排名API路由
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.services.sales_service import SalesService
from app.schemas.sales import SalesRankingResponse
from app.schemas.response import Response

router = APIRouter(prefix="/sales-ranking")


@router.get("", response_model=Response[SalesRankingResponse])
async def get_sales_ranking(
    period: str = Query(
        default='last_year',
        description="查询周期: last_year(近一年), last_6months(近半年), last_3months(近三个月), last_month(上月), 或 YYYY-MM(指定月份)"
    ),
    limit: int = Query(default=50, ge=1, le=100, description="返回数量限制"),
    db: AsyncSession = Depends(get_async_db)
):
    """
    获取销量排名榜单
    
    支持的period参数:
    - last_year: 近一年
    - last_6months: 近半年
    - last_3months: 近三个月
    - last_month: 上个月
    - YYYY-MM: 指定月份，例如 2024-10
    """
    ranking = await SalesService.get_sales_ranking(db, period, limit)
    
    return Response(
        code=200,
        message="查询成功",
        data=ranking
    )
