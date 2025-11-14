"""
品牌管理接口
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from app.core.database import get_async_db
from app.models.brand import Brand
from app.models.series import Series
from app.schemas.brand import BrandCreate, BrandUpdate, BrandResponse
from app.schemas.response import Response, PageResponse

router = APIRouter()


@router.get("/brands", response_model=PageResponse[BrandResponse], summary="获取品牌列表")
async def get_brands(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    keyword: str = Query(None, description="搜索关键词"),
    initial: str = Query(None, description="首字母筛选"),
    db: AsyncSession = Depends(get_async_db)
):
    """获取品牌列表（支持分页、搜索、首字母筛选）"""
    query = select(Brand)
    
    if keyword:
        query = query.where(Brand.name.like(f"%{keyword}%"))
    
    if initial:
        query = query.where(Brand.initial == initial.upper())
    
    # 获取总数
    total_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(total_query)
    total = total_result.scalar()
    
    # 分页查询
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    brands = result.scalars().all()
    
    # 获取每个品牌的车系数量
    brand_responses = []
    for brand in brands:
        series_count_query = select(func.count()).where(Series.brand_id == brand.id)
        series_count_result = await db.execute(series_count_query)
        series_count = series_count_result.scalar()
        
        brand_dict = {
            **brand.__dict__,
            "series_count": series_count
        }
        brand_responses.append(BrandResponse(**brand_dict))
    
    return PageResponse(
        data=brand_responses,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/brands/{brand_id}", response_model=Response[BrandResponse], summary="获取品牌详情")
async def get_brand(
    brand_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """根据ID获取品牌详情"""
    result = await db.execute(select(Brand).where(Brand.id == brand_id))
    brand = result.scalar_one_or_none()
    
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    
    # 获取车系数量
    series_count_query = select(func.count()).where(Series.brand_id == brand.id)
    series_count_result = await db.execute(series_count_query)
    series_count = series_count_result.scalar()
    
    brand_dict = {
        **brand.__dict__,
        "series_count": series_count
    }
    
    return Response(data=BrandResponse(**brand_dict))


@router.post("/brands", response_model=Response[BrandResponse], summary="创建品牌")
async def create_brand(
    brand_data: BrandCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """创建新品牌"""
    # 检查品牌名称是否已存在
    result = await db.execute(select(Brand).where(Brand.name == brand_data.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="品牌名称已存在")
    
    brand = Brand(**brand_data.model_dump())
    db.add(brand)
    await db.commit()
    await db.refresh(brand)
    
    brand_dict = {
        **brand.__dict__,
        "series_count": 0
    }
    
    return Response(data=BrandResponse(**brand_dict), message="创建成功")


@router.put("/brands/{brand_id}", response_model=Response[BrandResponse], summary="更新品牌")
async def update_brand(
    brand_id: int,
    brand_data: BrandUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    """更新品牌信息"""
    result = await db.execute(select(Brand).where(Brand.id == brand_id))
    brand = result.scalar_one_or_none()
    
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    
    # 更新字段
    update_data = brand_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(brand, field, value)
    
    await db.commit()
    await db.refresh(brand)
    
    # 获取车系数量
    series_count_query = select(func.count()).where(Series.brand_id == brand.id)
    series_count_result = await db.execute(series_count_query)
    series_count = series_count_result.scalar()
    
    brand_dict = {
        **brand.__dict__,
        "series_count": series_count
    }
    
    return Response(data=BrandResponse(**brand_dict), message="更新成功")


@router.delete("/brands/{brand_id}", response_model=Response, summary="删除品牌")
async def delete_brand(
    brand_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """删除品牌"""
    result = await db.execute(select(Brand).where(Brand.id == brand_id))
    brand = result.scalar_one_or_none()
    
    if not brand:
        raise HTTPException(status_code=404, detail="品牌不存在")
    
    await db.delete(brand)
    await db.commit()
    
    return Response(message="删除成功")
