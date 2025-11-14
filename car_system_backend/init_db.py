"""
初始化数据库脚本
清除旧的迁移记录，重新创建表结构
"""
import asyncio
from sqlalchemy import text
from app.core.database import sync_engine, Base
from app.models import Brand, Series, CarModel


def init_db():
    """初始化数据库"""
    print("开始初始化数据库...")
    
    # 删除所有表（包括 alembic_version）
    print("删除旧表...")
    with sync_engine.begin() as conn:
        # 禁用外键检查
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        conn.execute(text("DROP TABLE IF EXISTS car_models"))
        conn.execute(text("DROP TABLE IF EXISTS series"))
        conn.execute(text("DROP TABLE IF EXISTS car_series"))  # 旧表名
        conn.execute(text("DROP TABLE IF EXISTS brands"))
        conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
        # 启用外键检查
        conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
    
    # 创建所有表
    print("创建新表...")
    Base.metadata.create_all(bind=sync_engine)
    
    print("✅ 数据库初始化完成！")
    print("\n下一步:")
    print("1. 运行: alembic revision --autogenerate -m 'Initial migration'")
    print("2. 运行: alembic upgrade head")


if __name__ == "__main__":
    init_db()
