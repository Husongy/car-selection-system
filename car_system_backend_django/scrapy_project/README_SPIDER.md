# Scrapy爬虫使用说明

## 📋 项目概述

本项目使用Scrapy框架实现了两个爬虫，用于抓取汽车相关数据：

1. **懂车帝爬虫** (`dongchedi`) - 抓取新能源汽车销量数据
2. **车质网爬虫** (`chezhi`) - 抓取汽车质量投诉数据

爬取的数据将自动存储到MySQL数据库中，供Django后端使用。

---

## 🚀 快速开始

### 1. 环境准备

确保已安装所需依赖：

```bash
cd car_system_backend_django
pip install -r requirements.txt
```

主要依赖：
- `scrapy` - 爬虫框架
- `django` - 与Django集成
- `mysqlclient` - MySQL数据库驱动

### 2. 数据库准备

确保Django数据库已迁移：

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 运行爬虫

#### 方式一：使用运行脚本（推荐）

```bash
cd scrapy_project

# 运行懂车帝爬虫
python run_spider.py dongchedi

# 运行车质网爬虫（爬取5页）
python run_spider.py chezhi

# 运行车质网爬虫（自定义页数）
python run_spider.py chezhi -p 10

# 运行所有爬虫
python run_spider.py all
```

#### 方式二：使用Scrapy命令

```bash
cd scrapy_project

# 运行懂车帝爬虫
scrapy crawl dongchedi

# 运行车质网爬虫
scrapy crawl chezhi -a max_pages=10
```

---

## 📊 爬虫详细说明

### 1. 懂车帝爬虫 (dongchedi)

**功能**：
- 抓取新能源汽车销量排行数据
- 自动识别品牌和车系
- 记录月度销量数据

**数据字段**：
- `brand_name` - 品牌名称（如：比亚迪、特斯拉）
- `series_name` - 车系名称（如：秦PLUS DM-i、Model Y）
- `month` - 月份（格式：2024-01）
- `sales` - 销量数量

**特点**：
- 支持API和HTML两种解析方式
- 自动生成当前月份
- 数据去重和验证
- 智能错误重试

**运行示例**：
```bash
python run_spider.py dongchedi
```

---

### 2. 车质网爬虫 (chezhi)

**功能**：
- 抓取汽车质量投诉数据
- 分析问题严重程度
- 统计投诉次数

**数据字段**：
- `brand_name` - 品牌名称
- `series_name` - 车系名称
- `issue_type` - 问题类型（如：电池故障、异响）
- `description` - 问题描述
- `severity` - 严重程度（low/medium/high）
- `report_count` - 投诉次数

**参数**：
- `max_pages` - 最大爬取页数（默认：5）

**特点**：
- 支持分页爬取
- 智能判断问题严重程度
- 相同问题自动合并投诉次数
- 文本清洗和验证

**运行示例**：
```bash
# 爬取5页
python run_spider.py chezhi

# 爬取10页
python run_spider.py chezhi -p 10
```

**严重程度判断规则**：
- **high** - 包含关键词：安全、失灵、断裂、自燃、爆炸、失控等
- **medium** - 包含关键词：故障、损坏、异响、抖动等
- **low** - 其他一般性问题

---

## ⚙️ 配置说明

### settings.py 配置项

```python
# 并发和限速
CONCURRENT_REQUESTS = 8              # 并发请求数
DOWNLOAD_DELAY = 2                   # 下载延迟（秒）
AUTOTHROTTLE_ENABLED = True          # 自动限速

# 重试配置
RETRY_TIMES = 3                      # 重试次数
RETRY_HTTP_CODES = [500, 502, ...]   # 重试的HTTP状态码

# 缓存配置
HTTPCACHE_ENABLED = True             # 启用缓存
HTTPCACHE_EXPIRATION_SECS = 3600     # 缓存1小时

# 日志配置
LOG_LEVEL = 'INFO'                   # 日志级别
LOG_FILE = 'logs/scrapy_spider.log'  # 日志文件
```

### 自定义配置

如需调整爬虫行为，可在各爬虫的 `custom_settings` 中覆盖：

```python
class DongchediSpider(scrapy.Spider):
    custom_settings = {
        'DOWNLOAD_DELAY': 3,    # 增加延迟
        'CONCURRENT_REQUESTS': 4,
    }
```

---

## 📁 项目结构

```
scrapy_project/
├── car_spider/
│   ├── spiders/
│   │   ├── dongchedi_spider.py    # 懂车帝爬虫
│   │   └── chezhi_spider.py       # 车质网爬虫
│   ├── items.py                    # 数据模型定义
│   ├── pipelines.py                # 数据处理管道
│   └── settings.py                 # 爬虫配置
├── logs/                           # 日志目录
├── httpcache/                      # 缓存目录
├── run_spider.py                   # 运行脚本
└── scrapy.cfg                      # Scrapy配置
```

---

## 🔍 数据流程

```
1. 爬虫启动
   ↓
2. 发送HTTP请求
   ↓
3. 解析响应数据
   ↓
4. 生成Item对象
   ↓
5. Pipeline处理
   ↓
6. 数据验证
   ↓
7. 保存到数据库（Django ORM）
   ↓
8. 日志记录
```

---

## 📝 日志查看

爬虫运行日志保存在 `logs/scrapy_spider.log`：

```bash
# 实时查看日志
tail -f logs/scrapy_spider.log

# Windows PowerShell
Get-Content logs/scrapy_spider.log -Wait -Tail 50
```

日志级别：
- **INFO** - 一般信息（默认）
- **WARNING** - 警告信息
- **ERROR** - 错误信息
- **DEBUG** - 调试信息

---

## 🛠️ 故障排查

### 问题1：无法连接数据库

**症状**：`OperationalError: (2003, "Can't connect to MySQL server")`

**解决**：
1. 检查MySQL服务是否启动
2. 确认 `.env` 文件中的数据库配置正确
3. 测试数据库连接：`python manage.py dbshell`

### 问题2：爬虫无数据

**症状**：爬虫运行完成但没有数据

**解决**：
1. 检查网站结构是否改变
2. 查看日志文件中的错误信息
3. 尝试使用测试数据验证Pipeline

### 问题3：被网站封禁

**症状**：大量403或429错误

**解决**：
1. 增加 `DOWNLOAD_DELAY` 到3-5秒
2. 减少 `CONCURRENT_REQUESTS` 到4-8
3. 启用 `AUTOTHROTTLE`
4. 考虑使用代理IP

### 问题4：重复数据

**症状**：相同数据多次保存

**解决**：
- 数据库已设置唯一约束，会自动处理
- Pipeline会自动更新已存在的数据

---

## 📊 数据验证

运行后可通过Django shell验证数据：

```bash
python manage.py shell
```

```python
from apps.cars.models import Brand, CarSeries, CarSale, CarIssue

# 查看品牌数量
Brand.objects.count()

# 查看销量数据
CarSale.objects.all()[:5]

# 查看质量问题
CarIssue.objects.all()[:5]

# 查看某品牌的所有车系
Brand.objects.get(name='比亚迪').series.all()
```

---

## 🎯 最佳实践

1. **定期运行**：建议每月运行一次抓取最新数据
2. **增量更新**：爬虫会自动去重，可安全重复运行
3. **监控日志**：定期检查日志文件，发现异常及时处理
4. **合理限速**：避免过快请求导致IP被封
5. **数据备份**：定期备份数据库数据

---

## ⚠️ 注意事项

1. **合法使用**：仅用于学习研究，遵守网站robots.txt和服务条款
2. **频率控制**：不要频繁爬取，避免给服务器造成压力
3. **数据准确性**：网站结构可能变化，需要及时更新选择器
4. **隐私保护**：不要爬取和传播敏感信息

---

## 🔧 高级功能

### 1. 使用代理IP

编辑 `settings.py`：

```python
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

# 设置代理
HTTPPROXY_ENABLED = True
```

### 2. 自定义User-Agent

已内置User-Agent池，随机选择浏览器标识。

### 3. 导出数据

```bash
# 导出为JSON
scrapy crawl dongchedi -o output.json

# 导出为CSV
scrapy crawl chezhi -o output.csv
```

---

## 📞 技术支持

如遇问题，请查看：
1. 项目日志文件：`logs/scrapy_spider.log`
2. Scrapy官方文档：https://docs.scrapy.org/
3. Django文档：https://docs.djangoproject.com/

---

## 📈 性能优化建议

1. **调整并发数**：根据服务器响应速度调整
2. **启用缓存**：避免重复请求相同URL
3. **数据库索引**：确保数据库有适当索引
4. **批量保存**：Pipeline已优化为批量操作

---

## 📅 更新日志

### v2.0 - 优化版本
- ✅ 增强错误处理和重试机制
- ✅ 添加数据验证和清洗
- ✅ 优化反爬虫策略
- ✅ 改进日志记录
- ✅ 支持命令行参数
- ✅ 批量运行功能

### v1.0 - 初始版本
- ✅ 基本爬虫框架
- ✅ Django ORM集成
- ✅ 简单数据存储

---

**祝您使用愉快！** 🎉
