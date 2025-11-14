"""测试数据库连接"""
from app.core.database import sync_engine
from sqlalchemy import text

try:
    with sync_engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('✓ 数据库连接成功')
        
        # 测试car_system数据库
        result = conn.execute(text('SELECT DATABASE()'))
        db_name = result.scalar()
        print(f'✓ 当前数据库: {db_name}')
        
        # 列出所有表
        result = conn.execute(text('SHOW TABLES'))
        tables = [row[0] for row in result]
        print(f'✓ 数据表数量: {len(tables)}')
        print(f'✓ 数据表列表: {", ".join(tables)}')
        
except Exception as e:
    print(f'✗ 数据库连接失败: {e}')
    import traceback
    traceback.print_exc()
