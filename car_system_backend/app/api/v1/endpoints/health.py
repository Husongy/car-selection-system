from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    """健康检查响应"""
    status: str
    message: str


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    健康检查接口
    
    返回系统运行状态
    """
    return {
        "status": "ok",
        "message": "Backend is running!"
    }
