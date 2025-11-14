"""
FastAPI应用主入口
配置CORS、路由、中间件等
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="汽车信息系统后端API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议配置具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", summary="根路径")
async def root():
    """根路径欢迎信息"""
    return {
        "message": "Welcome to Car System Backend API",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    print(f"🚀 {settings.PROJECT_NAME} is starting...")
    print(f"📚 API文档地址: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    print(f"🛑 {settings.PROJECT_NAME} is shutting down...")
