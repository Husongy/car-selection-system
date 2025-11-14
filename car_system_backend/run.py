"""
项目运行启动脚本
使用uvicorn启动FastAPI应用
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=False,  # 关闭热重载，避免频繁重启
        log_level="info"
    )
