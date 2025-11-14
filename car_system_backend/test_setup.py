"""
测试脚本 - 验证项目配置
在安装依赖后运行此脚本，验证环境配置是否正确
"""
import sys
import os

def test_imports():
    """测试依赖包导入"""
    print("=" * 50)
    print("测试依赖包导入...")
    print("=" * 50)
    
    try:
        import fastapi
        print(f"✓ FastAPI: {fastapi.__version__}")
    except ImportError as e:
        print(f"✗ FastAPI 导入失败: {e}")
        return False
    
    try:
        import sqlalchemy
        print(f"✓ SQLAlchemy: {sqlalchemy.__version__}")
    except ImportError as e:
        print(f"✗ SQLAlchemy 导入失败: {e}")
        return False
    
    try:
        import pydantic
        print(f"✓ Pydantic: {pydantic.__version__}")
    except ImportError as e:
        print(f"✗ Pydantic 导入失败: {e}")
        return False
    
    try:
        import uvicorn
        print(f"✓ Uvicorn: {uvicorn.__version__}")
    except ImportError as e:
        print(f"✗ Uvicorn 导入失败: {e}")
        return False
    
    try:
        import alembic
        print(f"✓ Alembic: {alembic.__version__}")
    except ImportError as e:
        print(f"✗ Alembic 导入失败: {e}")
        return False
    
    return True


def test_config():
    """测试项目配置"""
    print("\n" + "=" * 50)
    print("测试项目配置...")
    print("=" * 50)
    
    try:
        from app.core.config import settings
        print(f"✓ 配置加载成功")
        print(f"  - 项目名称: {settings.PROJECT_NAME}")
        print(f"  - API前缀: {settings.API_V1_PREFIX}")
        print(f"  - 数据库主机: {settings.DB_HOST}")
        print(f"  - 数据库名称: {settings.DB_NAME}")
        
        # 检查数据库URL是否配置
        if settings.DATABASE_URL and settings.DATABASE_URL != "":
            print(f"✓ 异步数据库URL已配置")
        else:
            print(f"⚠ 异步数据库URL未配置，请检查.env文件")
            
        if settings.SYNC_DATABASE_URL and settings.SYNC_DATABASE_URL != "":
            print(f"✓ 同步数据库URL已配置")
        else:
            print(f"⚠ 同步数据库URL未配置，请检查.env文件")
            
        return True
    except Exception as e:
        print(f"✗ 配置加载失败: {e}")
        return False


def test_app():
    """测试应用创建"""
    print("\n" + "=" * 50)
    print("测试应用创建...")
    print("=" * 50)
    
    try:
        from app.main import app
        print(f"✓ FastAPI应用创建成功")
        print(f"  - 标题: {app.title}")
        print(f"  - 版本: {app.version}")
        print(f"  - 文档路径: {app.docs_url}")
        return True
    except Exception as e:
        print(f"✗ 应用创建失败: {e}")
        return False


def test_routes():
    """测试路由注册"""
    print("\n" + "=" * 50)
    print("测试路由注册...")
    print("=" * 50)
    
    try:
        from app.main import app
        routes = [route.path for route in app.routes]
        print(f"✓ 已注册路由:")
        for route in routes:
            print(f"  - {route}")
        return True
    except Exception as e:
        print(f"✗ 路由测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("\n" + "=" * 50)
    print("   FastAPI 项目环境检测工具")
    print("=" * 50 + "\n")
    
    results = []
    
    # 测试依赖导入
    results.append(("依赖包导入", test_imports()))
    
    # 测试配置
    results.append(("项目配置", test_config()))
    
    # 测试应用创建
    results.append(("应用创建", test_app()))
    
    # 测试路由
    results.append(("路由注册", test_routes()))
    
    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ 所有测试通过！项目环境配置正确。")
        print("\n下一步:")
        print("1. 确保MySQL已启动并创建了数据库")
        print("2. 修改.env文件中的数据库密码")
        print("3. 运行: python run.py")
        print("4. 访问: http://localhost:8000/docs")
    else:
        print("✗ 部分测试失败，请检查以上错误信息。")
        print("\n建议:")
        print("1. 确保虚拟环境已激活")
        print("2. 重新安装依赖: pip install -r requirements.txt")
        print("3. 检查.env文件配置")
    print("=" * 50 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
