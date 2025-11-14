"""
直接创建用户表和测试账户（绕过Alembic）
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 直接使用MySQL连接
import pymysql
import bcrypt

# 密码加密函数
def hash_password(password: str) -> str:
    """BCrypt加密密码"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# 数据库配置（从.env读取或使用默认值）
DB_CONFIG = {
    'host': 'localhost',
    'port': 3307,  # 使用.env中的端口
    'user': 'root',
    'password': 'root',  # 使用.env中的密码
    'database': 'car_system',
    'charset': 'utf8mb4'
}

def create_users_table():
    """创建用户表"""
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 创建用户表
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
                username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
                email VARCHAR(100) UNIQUE COMMENT '邮箱',
                hashed_password VARCHAR(255) NOT NULL COMMENT '哈希密码',
                is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
                is_superuser BOOLEAN DEFAULT FALSE COMMENT '是否超级用户',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                INDEX idx_username (username),
                INDEX idx_email (email)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';
            """
            cursor.execute(create_table_sql)
            connection.commit()
            print("✅ 用户表创建成功！")
    finally:
        connection.close()


def create_admin_user():
    """创建管理员账户"""
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 检查是否已存在
            cursor.execute("SELECT id FROM users WHERE username = 'admin'")
            if cursor.fetchone():
                print("❌ 管理员账户已存在")
                return
            
            # 创建管理员
            hashed_password = hash_password("admin123")
            insert_sql = """
            INSERT INTO users (username, email, hashed_password, is_active, is_superuser)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_sql, ('admin', 'admin@example.com', hashed_password, True, True))
            connection.commit()
            print("✅ 管理员账户创建成功！")
            print("   用户名: admin")
            print("   密码: admin123")
    finally:
        connection.close()


def create_test_user():
    """创建普通测试用户"""
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor() as cursor:
            # 检查是否已存在
            cursor.execute("SELECT id FROM users WHERE username = 'testuser'")
            if cursor.fetchone():
                print("❌ 测试用户已存在")
                return
            
            # 创建测试用户
            hashed_password = hash_password("test123")
            insert_sql = """
            INSERT INTO users (username, email, hashed_password, is_active, is_superuser)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_sql, ('testuser', 'test@example.com', hashed_password, True, False))
            connection.commit()
            print("✅ 测试用户创建成功！")
            print("   用户名: testuser")
            print("   密码: test123")
    finally:
        connection.close()


def main():
    print("=" * 60)
    print("🔧 初始化用户系统")
    print("=" * 60)
    
    try:
        print("\n📦 创建用户表...")
        create_users_table()
        
        print("\n👤 创建测试账户...")
        create_admin_user()
        create_test_user()
        
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
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        print("\n请检查:")
        print("1. MySQL服务是否启动")
        print("2. 数据库car_system是否存在")
        print("3. DB_CONFIG中的密码是否正确")


if __name__ == "__main__":
    main()
