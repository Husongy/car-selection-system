"""
创建用户表并生成测试管理员账户
"""
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import select
from app.core.database import AsyncSessionLocal, sync_engine
from app.models.user import User
from app.core.security import get_password_hash


async def create_admin_user():
    """创建管理员用户"""
    async with AsyncSessionLocal() as db:
        # 检查是否已存在管理员
        result = await db.execute(
            select(User).where(User.username == "admin")
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print("❌ 管理员用户已存在")
            return
        
        # 创建管理员
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_superuser=True
        )
        
        db.add(admin_user)
        await db.commit()
        await db.refresh(admin_user)
        
        print("✅ 管理员账户创建成功！")
        print(f"   用户名: admin")
        print(f"   密码: admin123")
        print(f"   邮箱: admin@example.com")


async def create_test_user():
    """创建普通测试用户"""
    async with AsyncSessionLocal() as db:
        # 检查是否已存在测试用户
        result = await db.execute(
            select(User).where(User.username == "testuser")
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print("❌ 测试用户已存在")
            return
        
        # 创建测试用户
        test_user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("test123"),
            is_active=True,
            is_superuser=False
        )
        
        db.add(test_user)
        await db.commit()
        await db.refresh(test_user)
        
        print("✅ 测试用户创建成功！")
        print(f"   用户名: testuser")
        print(f"   密码: test123")
        print(f"   邮箱: test@example.com")


def main():
    print("=" * 60)
    print("🔧 创建用户表和测试账户")
    print("=" * 60)
    
    # 创建用户表
    print("\n📦 创建数据库表...")
    from app.models import Base
    Base.metadata.create_all(bind=sync_engine)
    print("✅ 数据库表创建完成")
    
    # 创建测试账户
    print("\n👤 创建测试账户...")
    asyncio.run(create_admin_user())
    asyncio.run(create_test_user())
    
    print("\n" + "=" * 60)
    print("✨ 完成！现在你可以使用以下账户登录：")
    print("=" * 60)
    print("\n管理员账户:")
    print("  用户名: admin")
    print("  密码: admin123")
    print("\n普通用户账户:")
    print("  用户名: testuser")
    print("  密码: test123")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
