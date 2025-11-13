import redis.asyncio as aioredis
from typing import Optional
from app.core.config import settings


class RedisClient:
    """Redis客户端"""
    
    def __init__(self):
        self.redis: Optional[aioredis.Redis] = None
    
    async def connect(self):
        """连接Redis"""
        self.redis = await aioredis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
            password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
            encoding="utf-8",
            decode_responses=True
        )
    
    async def close(self):
        """关闭Redis连接"""
        if self.redis:
            await self.redis.close()
    
    async def get(self, key: str) -> Optional[str]:
        """获取缓存"""
        if self.redis:
            return await self.redis.get(key)
        return None
    
    async def set(self, key: str, value: str, expire: int = 3600):
        """设置缓存"""
        if self.redis:
            await self.redis.set(key, value, ex=expire)
    
    async def delete(self, key: str):
        """删除缓存"""
        if self.redis:
            await self.redis.delete(key)


redis_client = RedisClient()
