"""
简单直接的用户创建脚本（使用同步方式）
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def create_users():
    """使用同步方式创建用户"""
    db = SessionLocal()
    
    try:
        # 删除现有用户
        print("🗑️  删除旧用户...")
        db.query(User).delete()
        db.commit()
        print("✅ 旧用户已删除")
        
        # 创建管理员
        print("\n👤 创建管理员账户...")
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
            is_superuser=True
        )
        db.add(admin)
        
        # 创建测试用户
        print("👤 创建测试用户...")
        testuser = User(
            username="testuser",
            email="test@example.com",
            hashed_password=get_password_hash("test123"),
            is_active=True,
            is_superuser=False
        )
        db.add(testuser)
        
        db.commit()
        
        print("\n" + "="*60)
        print("✅ 用户创建成功！")
        print("="*60)
        print("\n管理员账户:")
        print("  用户名: admin")
        print("  密码: admin123")
        print("\n普通用户:")
        print("  用户名: testuser")
        print("  密码: test123")
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("="*60)
    print("🔧 创建用户（同步方式）")
    print("="*60)
    create_users()
