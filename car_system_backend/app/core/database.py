"""
数据库连接配置模块
提供异步和同步的数据库引擎及会话管理
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings

# 创建异步引擎（用于FastAPI异步操作）
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # 开发环境打印SQL，生产环境建议设为False
    pool_pre_ping=True,
    pool_recycle=3600,
)

# 创建同步引擎（用于Alembic迁移）
sync_engine = create_engine(
    settings.SYNC_DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# 异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 同步会话工厂（用于Alembic）
SessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
)

# 声明基类
Base = declarative_base()


async def get_async_db():
    """
    异步数据库会话依赖
    用于FastAPI路由中的依赖注入
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_db():
    """
    同步数据库会话依赖
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
