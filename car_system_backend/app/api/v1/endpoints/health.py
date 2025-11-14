"""
健康检查接口
用于验证后端服务是否正常运行
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="健康检查")
async def health_check():
    """
    健康检查接口
    返回服务运行状态
    """
    return {
        "status": "ok",
        "message": "Backend is running!"
    }
