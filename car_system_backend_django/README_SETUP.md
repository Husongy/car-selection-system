# Django 后端系统扩展模块使用说明

## 📦 已完成的三大扩展模块

### 1️⃣ Scrapy 爬虫模块
### 2️⃣ Django SimpleUI 后台管理
### 3️⃣ 用户登录注册系统

---

## 🚀 快速开始

### 第一步：安装依赖

在 `car_system_backend_django` 目录下运行：

```bash
pip install -r requirements.txt
```

主要依赖包括：
- `Scrapy==2.11.0` - 爬虫框架
- `django-simpleui==2024.1.1` - 后台管理美化
- Django 及相关依赖

---

### 第二步：数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 第三步:创建超级管理员

```bash
python manage.py createsuperuser
```

按提示输入用户名、邮箱和密码。

---

## 📊 模块详细说明

### 1. Scrapy 爬虫模块

#### 📁 目录结构
```
scrapy_project/
├── car_spider/
│   ├── spiders/
│   │   ├── dongchedi_spider.py    # 东车帝爬虫
│   │   └── chezhi_spider.py       # 车质网爬虫
│   ├── items.py                    # Item定义
│   ├── pipelines.py                # Django Pipeline
│   └── settings.py                 # 爬虫配置
├── run_spider.py                   # 运行脚本
└── scrapy.cfg                      # Scrapy配置
```

#### 🔧 运行爬虫

**方式1：使用运行脚本**
```bash
cd scrapy_project
python run_spider.py dongchedi    # 运行东车帝爬虫
python run_spider.py chezhi       # 运行车质网爬虫
```

**方式2：使用 Scrapy 命令**
```bash
cd scrapy_project
scrapy crawl dongchedi
scrapy crawl chezhi
```

#### 📝 爬虫说明

当前提供的爬虫是**框架示例**，包含：
- ✅ 完整的项目结构
- ✅ Django ORM 集成
- ✅ Pipeline 数据存储
- ✅ 示例数据生成

**实际使用需要调整：**
1. 分析目标网站的真实数据接口
2. 修改选择器或 JSON 解析逻辑
3. 添加翻页和错误处理
4. 配置反爬策略

---

### 2. Django SimpleUI 后台管理

#### 🎨 访问后台

启动服务后访问：`http://localhost:8000/admin/`

使用之前创建的超级管理员账号登录。

#### ✨ 功能特性

**品牌管理 (Brand)**
- 品牌名称、国家、Logo
- 搜索和过滤

**车系管理 (CarSeries)**
- 基本信息、价格区间、续航里程
- **内联显示**销量数据和质量问题
- 多维度筛选

**销量数据 (CarSale)**
- 月度销量统计
- 按品牌、月份筛选

**质量问题 (CarIssue)**
- 问题类型、严重程度
- 投诉次数统计

#### 🎯 配置说明

已在 `settings.py` 中配置：
```python
INSTALLED_APPS = [
    'simpleui',  # 必须在 admin 之前
    'django.contrib.admin',
    ...
]

SIMPLEUI_CONFIG = {
    'system_keep': False,
    'dynamic': True,
    'menus': [...]  # 自定义菜单
}
```

---

### 3. 用户登录注册系统

#### 🔐 后端 API

**注册接口**
```http
POST /api/users/register/
Content-Type: application/json

{
  "username": "testuser",
  "password": "123456",
  "email": "test@example.com"  // 可选
}
```

**登录接口**
```http
POST /api/users/login/
Content-Type: application/json

{
  "username": "testuser",
  "password": "123456"
}
```

返回格式：
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "token": "user_1_testuser"
  }
}
```

#### 🎨 前端页面

**登录页面**：`/login`
- 使用 Django 后端认证
- 支持重定向到目标页面

**注册页面**：`/register`
- 用户名、邮箱、密码验证
- 注册成功后跳转登录

**路由守卫**
- 需要登录的页面添加 `meta: { requiresAuth: true }`
- 未登录自动跳转到登录页

#### 📦 Pinia Store

```typescript
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

// Django 登录
await userStore.loginDjango(username, password)

// Django 注册
await userStore.registerDjango(username, password, email)

// 退出登录
await userStore.logout()

// 状态
userStore.isLoggedIn  // 是否登录
userStore.userInfo    // 用户信息
```

---

## 🔄 启动完整系统

### 1. 启动 Django 后端
```bash
cd car_system_backend_django
python manage.py runserver
```

访问：
- 前端 API：`http://localhost:8000/api/`
- 后台管理：`http://localhost:8000/admin/`

### 2. 启动前端
```bash
cd car_system_frontend
npm run dev
```

访问：`http://localhost:5173/`

### 3. 测试流程

1. **注册新用户**：访问 `/register` 创建账号
2. **登录系统**：使用注册的账号登录
3. **访问选车页面**：需要登录才能访问
4. **后台管理**：使用超级管理员账号访问 `/admin/`
5. **运行爬虫**：采集测试数据

---

## 📝 重要提示

### 🔒 安全建议

当前实现使用了简化的 token 机制，**生产环境**建议：
1. 使用 JWT (djangorestframework-simplejwt)
2. 添加 CSRF 保护
3. 配置 HTTPS
4. 限制登录尝试次数

### 🌐 爬虫使用

提供的爬虫是**示例框架**：
- 包含完整的结构和 Pipeline
- 生成测试数据验证功能
- 实际使用需要根据网站调整

### 🎨 SimpleUI 定制

可在 `settings.py` 中自定义：
- Logo 和主题
- 菜单结构
- 首页信息
- 分析页面

---

## 🐛 常见问题

**Q: 爬虫运行报错？**
A: 确保在 `scrapy_project` 目录下运行，Django 环境已配置。

**Q: 后台登录失败？**
A: 先创建超级管理员：`python manage.py createsuperuser`

**Q: 前端登录后无响应？**
A: 检查后端服务是否启动，查看浏览器控制台错误信息。

**Q: 路由守卫不生效？**
A: 确保在 `main.ts` 中调用了 `userStore.init()` 初始化状态。

---

## 📚 技术栈

**后端：**
- Django 4.2.7
- Scrapy 2.11.0
- django-simpleui 2024.1.1
- MySQL 数据库

**前端：**
- Vue 3 + TypeScript
- Pinia 状态管理
- Naive UI 组件库
- Vue Router 路由

---

## ✅ 功能检查清单

- [x] Scrapy 爬虫框架搭建
- [x] Django Pipeline 数据存储
- [x] SimpleUI 后台管理界面
- [x] 四大模型 Admin 配置
- [x] 内联表格显示
- [x] 用户注册 API
- [x] 用户登录 API
- [x] 前端登录页面
- [x] 前端注册页面
- [x] Pinia 状态管理
- [x] 路由守卫保护
- [x] Token 持久化

---

## 🎉 总结

现在你已经拥有一个功能完整的汽车智能选车系统，包含：
- 🕷️ 数据采集（Scrapy）
- 🎨 后台管理（SimpleUI）
- 🔐 用户认证（登录注册）

所有代码遵循"简单至上"原则，清晰易懂，开箱即用！
