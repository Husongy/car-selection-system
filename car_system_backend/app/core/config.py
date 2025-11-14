"""
项目配置模块
使用pydantic-settings管理环境变量
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置类"""
    
    # 项目基本信息
    PROJECT_NAME: str = "Car System Backend"
    API_V1_PREFIX: str = "/api/v1"
    
    # 数据库配置
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "car_system"
    
    # 异步数据库连接URL（用于FastAPI异步操作）
    DATABASE_URL: str = ""
    
    # 同步数据库连接URL（用于Alembic迁移）
    SYNC_DATABASE_URL: str = ""
    
    # Redis配置（可选）
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()
