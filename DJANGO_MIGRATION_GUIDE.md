# 新能源汽车智能选车系统 - Django迁移指南

## 📋 项目概述

本项目从 FastAPI 迁移到 Django + DRF，使用以下技术栈：

### 后端技术栈
- Python 3.12
- Django 4.2.7
- Django REST Framework 3.14.0
- MySQL 数据库
- JWT 认证

### 前端技术栈
- Vue 3 (Composition API with `<script setup>`)
- Vite
- Element Plus (替换 Naive UI)
- Pinia
- Vue Router
- Axios
- ECharts
- vicons/ionicons5 (图标库)
- 主题色: #18A058

## 🚀 快速开始

### 第一步：安装 Django 环境

```powershell
# 进入 Django 后端目录
cd e:\graduation-project\car_system_backend_django

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt
```

### 第二步：配置数据库

1. 确保 MySQL 服务运行在端口 3307
2. 创建数据库：
```sql
CREATE DATABASE car_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. 检查 `.env` 文件配置是否正确

### 第三步：创建数据库表

```powershell
# 创建迁移文件
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

### 第四步：启动开发服务器

```powershell
# 启动 Django 服务器
python manage.py runserver 0.0.0.0:8000
```

访问：
- API: http://localhost:8000/api/v1/
- Admin: http://localhost:8000/admin/

## 📁 项目结构

```
car_system_backend_django/
├── car_system/                 # Django 项目配置
│   ├── __init__.py
│   ├── settings.py            # 项目配置
│   ├── urls.py                # 主路由
│   ├── wsgi.py                # WSGI配置
│   └── utils.py               # 工具函数
│
├── apps/                       # 应用目录
│   ├── users/                 # 用户模块
│   │   ├── models.py          # 用户模型
│   │   ├── serializers.py     # 序列化器
│   │   ├── views.py           # 视图
│   │   └── urls.py            # 路由
│   │
│   ├── cars/                  # 汽车模块
│   │   ├── models.py          # 汽车模型
│   │   ├── serializers.py     # 序列化器
│   │   ├── views.py           # 视图
│   │   ├── filters.py         # 过滤器
│   │   └── urls.py            # 路由
│   │
│   └── analysis/              # 数据分析模块
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
│
├── manage.py                   # Django 管理脚本
├── requirements.txt            # Python 依赖
└── .env                        # 环境变量
```

## 📝 下一步工作

### 1. 创建应用模块
```powershell
python manage.py startapp users
python manage.py startapp cars
python manage.py startapp analysis
```

### 2. 定义数据模型

在 `apps/cars/models.py` 中定义：
- Brand (品牌)
- Series (车系)
- CarModel (车型)
- SalesData (销量数据)

### 3. 创建 API 接口

使用 DRF 的 ViewSet 和 Serializer

### 4. 前端迁移

- 安装 Element Plus
- 替换所有 Naive UI 组件
- 更新图标库
- 调整主题色
- 适配新的 API

## 🔧 常用命令

```powershell
# 创建迁移
python manage.py makemigrations

# 执行迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 运行开发服务器
python manage.py runserver

# 进入 Django Shell
python manage.py shell

# 收集静态文件
python manage.py collectstatic
```

## 📌 注意事项

1. **数据库端口**：确认 MySQL 运行在 3307 端口
2. **虚拟环境**：始终在虚拟环境中工作
3. **代码风格**：保持简洁，添加清晰注释
4. **核心功能**：优先实现条件选车功能
5. **前后端分离**：确保 CORS 配置正确

## 🎯 核心功能清单

- [ ] 用户认证（注册、登录、JWT）
- [ ] 汽车数据管理（CRUD）
- [ ] 条件筛选（价格、续航、品牌等）
- [ ] 智能推荐
- [ ] 数据可视化（ECharts）
- [ ] 销量排行
- [ ] 车型对比

## 💡 技术要点

### Django ORM vs SQLAlchemy
- 使用 Django 的模型定义
- 关系通过 ForeignKey, ManyToManyField 定义
- 查询使用 QuerySet API

### DRF ViewSet
- 使用 ModelViewSet 快速创建 CRUD
- 使用 @action 装饰器添加自定义操作
- 使用 filter_backends 实现筛选

### JWT 认证
- 使用 simplejwt 库
- 配置 ACCESS_TOKEN_LIFETIME = 24小时
- 前端在 Authorization header 中携带 token

## 🔗 相关资源

- Django 官方文档: https://docs.djangoproject.com/
- DRF 官方文档: https://www.django-rest-framework.org/
- Element Plus: https://element-plus.org/
- Vue 3: https://vuejs.org/
