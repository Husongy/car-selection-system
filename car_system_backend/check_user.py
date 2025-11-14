"""
检查用户数据和密码哈希格式
"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.user import User

async def check_users():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User))
        users = result.scalars().all()
        
        if not users:
            print("❌ 数据库中没有用户")
            return
        
        print(f"找到 {len(users)} 个用户：\n")
        for user in users:
            print(f"用户名: {user.username}")
            print(f"邮箱: {user.email}")
            pwd_hash = str(user.hashed_password)
            print(f"密码哈希: {pwd_hash[:60]}")
            
            # 判断哈希类型
            if pwd_hash.startswith('$2b$'):
                print("⚠️  类型: bcrypt (旧格式，需要重置)")
            elif pwd_hash.startswith('$argon2'):
                print("✅ 类型: argon2 (新格式，正确)")
            else:
                print("❓ 类型: 未知")
            print("-" * 60)

if __name__ == "__main__":
    asyncio.run(check_users())
