from fastapi import APIRouter
from app.schemas.response import HealthResponse

router = APIRouter()


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
