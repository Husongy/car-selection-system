"""
项目运行启动脚本
使用uvicorn启动FastAPI应用
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 开发环境开启热重载
        log_level="info"
    )
