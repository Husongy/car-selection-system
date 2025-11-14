"""
重置用户表 - 删除旧用户并创建新的测试账户
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import select, delete
from app.core.database import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash


async def reset_users():
    """重置用户数据"""
    async with AsyncSessionLocal() as db:
        # 删除所有用户
        print("🗑️  删除旧用户数据...")
        await db.execute(delete(User))
        await db.commit()
        print("✅ 旧用户数据已删除")
        
        # 创建管理员
        print("\n👤 创建管理员账户...")
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_superuser=True
        )
        db.add(admin_user)
        
        # 创建测试用户
        print("👤 创建测试用户...")
        test_user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("test123"),
            is_active=True,
            is_superuser=False
        )
        db.add(test_user)
        
        await db.commit()
        
        print("\n" + "="*60)
        print("✅ 用户重置成功！")
        print("="*60)
        print("\n管理员账户:")
        print("  用户名: admin")
        print("  密码: admin123")
        print("\n普通用户:")
        print("  用户名: testuser")
        print("  密码: test123")
        print("\n" + "="*60)


if __name__ == "__main__":
    print("="*60)
    print("🔄 重置用户表")
    print("="*60)
    
    # 使用新的事件循环方式，避免 Windows 上的 Event loop is closed 错误
    import platform
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(reset_users())
