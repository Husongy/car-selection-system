# app/api/v1/endpoints/brands.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/brands",  # 注意这里的前缀
    tags=["车系管理"]   # 这个标签会在Swagger中显示
)

@router.get("/")
async def get_brands():
    return {"message": "获取所有车系", "data": []}

@router.get("/{brand_id}")
async def get_brand(brand_id: int):
    return {"message": f"获取车系{brand_id}", "data": {}}

@router.post("/")
async def create_brand():
    return {"message": "创建车系成功"}
