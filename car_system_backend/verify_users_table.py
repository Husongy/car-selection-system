"""
验证用户表和账户
"""
import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'port': 3307,
    'user': 'root',
    'password': 'root',
    'database': 'car_system',
    'charset': 'utf8mb4'
}

def verify_users():
    connection = pymysql.connect(**DB_CONFIG)
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 查询所有用户
            cursor.execute("SELECT id, username, email, is_active, is_superuser, created_at FROM users")
            users = cursor.fetchall()
            
            print("=" * 80)
            print("📋 数据库用户列表")
            print("=" * 80)
            
            for user in users:
                print(f"\n用户ID: {user['id']}")
                print(f"  用户名: {user['username']}")
                print(f"  邮箱: {user['email']}")
                print(f"  是否激活: {'是' if user['is_active'] else '否'}")
                print(f"  是否管理员: {'是' if user['is_superuser'] else '否'}")
                print(f"  创建时间: {user['created_at']}")
            
            print("\n" + "=" * 80)
            print(f"✅ 共找到 {len(users)} 个用户")
            print("=" * 80)
            
    finally:
        connection.close()

if __name__ == "__main__":
    verify_users()
