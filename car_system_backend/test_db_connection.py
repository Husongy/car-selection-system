"""
测试数据库连接
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import sync_engine
from sqlalchemy import text

def test_connection():
    """测试数据库连接"""
    try:
        print("🔍 测试数据库连接...")
        print(f"连接信息: mysql://root:****@localhost:3307/car_system")
        
        with sync_engine.connect() as conn:
            # 测试查询
            result = conn.execute(text("SELECT 1"))
            print("✅ 数据库连接成功！")
            
            # 查询当前数据库
            result = conn.execute(text("SELECT DATABASE()"))
            db_name = result.scalar()
            print(f"✅ 当前数据库: {db_name}")
            
            # 查询users表是否存在
            result = conn.execute(text(
                "SELECT COUNT(*) FROM information_schema.tables "
                "WHERE table_schema = 'car_system' AND table_name = 'users'"
            ))
            table_exists = result.scalar()
            
            if table_exists:
                print("✅ users表存在")
                
                # 查询用户数量
                result = conn.execute(text("SELECT COUNT(*) FROM users"))
                user_count = result.scalar()
                print(f"✅ 用户数量: {user_count}")
            else:
                print("❌ users表不存在，需要运行数据库迁移")
                
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_connection()
