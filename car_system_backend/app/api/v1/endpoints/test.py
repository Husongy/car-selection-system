from fastapi import APIRouter

router = APIRouter()


@router.get("/test")
async def test_route():
    """测试路由"""
    return {"message": "测试成功"}
