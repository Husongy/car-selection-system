from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import api_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="新能源汽车智能选车系统后端API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    print(f"🚀 {settings.APP_NAME} is starting...")
    print(f"📝 API文档地址: http://localhost:8000/api/docs")
    # 打印已注册的路由，便于调试路由是否正确挂载
    print("🛣️ Registered routes:")
    for r in app.routes:
        try:
            methods = getattr(r, 'methods', None)
            print(f"  - path: {r.path}, name: {r.name}, methods: {methods}")
        except Exception:
            print(f"  - route: {r}")
    # 尝试导入 cars 模块并打印其 router 的路由（便于确认模块是否正常导入）
    try:
        from app.api.v1.endpoints import cars as cars_module
        car_routes = getattr(cars_module.router, 'routes', None)
        if car_routes is None:
            print("🧭 cars.router has no 'routes' attribute")
        else:
            print(f"🧭 cars.router registered {len(car_routes)} routes:")
            for cr in car_routes:
                try:
                    print(f"    - {cr.path}")
                except Exception:
                    print(f"    - route object: {cr}")
    except Exception as e:
        print("❗ Failed to import app.api.v1.endpoints.cars:", e)


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    print(f"👋 {settings.APP_NAME} is shutting down...")
