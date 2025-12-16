# Scrapy爬虫快速入门

## 🚀 5分钟快速开始

### 步骤1: 安装依赖（1分钟）

```bash
cd car_system_backend_django
pip install scrapy mysqlclient
```

### 步骤2: 准备数据库（1分钟）

```bash
# 确保MySQL服务已启动
# 运行Django迁移
python manage.py migrate
```

### 步骤3: 测试爬虫（1分钟）

```bash
cd scrapy_project
python test_spider.py
```

### 步骤4: 运行爬虫（2分钟）

#### Windows用户（推荐）
```bash
start_spider.bat
# 然后选择要运行的爬虫
```

#### 命令行用户
```bash
# 懂车帝爬虫
python run_spider.py dongchedi

# 车质网爬虫（爬取5页）
python run_spider.py chezhi

# 运行所有爬虫
python run_spider.py all
```

---

## 📋 常用命令

### 运行爬虫
```bash
# 方式1: 使用运行脚本（推荐）
python run_spider.py dongchedi
python run_spider.py chezhi -p 10

# 方式2: 直接使用Scrapy命令
scrapy crawl dongchedi
scrapy crawl chezhi -a max_pages=10
```

### 查看数据
```bash
# 进入Django shell
python manage.py shell

# 查询数据
from apps.cars.models import Brand, CarSale, CarIssue
Brand.objects.all()
CarSale.objects.all()[:5]
CarIssue.objects.all()[:5]
```

### 查看日志
```bash
# Windows
type logs\scrapy_spider.log

# Linux/Mac
cat logs/scrapy_spider.log
tail -f logs/scrapy_spider.log  # 实时查看
```

---

## 🎯 核心功能

### 1. 懂车帝爬虫
- **功能**: 抓取汽车销量数据
- **命令**: `python run_spider.py dongchedi`
- **数据**: 品牌、车系、月份、销量

### 2. 车质网爬虫
- **功能**: 抓取质量投诉数据
- **命令**: `python run_spider.py chezhi -p 5`
- **数据**: 品牌、车系、问题类型、严重程度、投诉次数

---

## 🛠️ 常见问题

### Q1: 数据库连接失败？
**A**: 检查 `.env` 文件中的数据库配置：
```env
DB_NAME=your_database
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### Q2: 没有抓到数据？
**A**: 
1. 查看日志: `type logs\scrapy_spider.log`
2. 当前版本会生成测试数据用于演示
3. 真实数据需要分析网站API接口

### Q3: 如何自定义爬取页数？
**A**: 
```bash
python run_spider.py chezhi -p 10  # 爬取10页
```

### Q4: 如何清理测试数据？
**A**:
```bash
python test_spider.py  # 运行后选择清理
```

---

## 📊 验证结果

运行爬虫后，通过Django shell验证：

```python
python manage.py shell
```

```python
from apps.cars.models import *

# 查看统计
print(f"品牌数量: {Brand.objects.count()}")
print(f"车系数量: {CarSeries.objects.count()}")
print(f"销量记录: {CarSale.objects.count()}")
print(f"质量问题: {CarIssue.objects.count()}")

# 查看具体数据
for sale in CarSale.objects.select_related('car_series__brand')[:5]:
    print(f"{sale.car_series.brand.name} {sale.car_series.name}: {sale.sales}辆")
```

---

## 🎓 学习路径

1. **入门**: 阅读本文档，运行测试
2. **理解**: 查看 `README_SPIDER.md`
3. **深入**: 阅读爬虫源码
4. **优化**: 根据实际需求调整配置

---

## 📁 项目结构速览

```
scrapy_project/
├── car_spider/          # 爬虫代码
│   ├── spiders/        # 爬虫文件
│   ├── items.py        # 数据模型
│   ├── pipelines.py    # 数据处理
│   └── settings.py     # 配置文件
├── logs/               # 日志目录
├── run_spider.py       # 运行脚本
├── test_spider.py      # 测试脚本
├── start_spider.bat    # Windows启动脚本
└── README_SPIDER.md    # 详细文档
```

---

## ⚡ 性能参数

默认配置（平衡性能和稳定性）：
- 并发请求: 8个
- 下载延迟: 2秒
- 自动限速: 开启
- 重试次数: 3次

如需调整，编辑 `car_spider/settings.py`

---

## 📞 获取帮助

1. 查看完整文档: `README_SPIDER.md`
2. 查看优化说明: `OPTIMIZATION_SUMMARY.md`
3. 运行测试工具: `python test_spider.py`
4. 查看运行日志: `logs/scrapy_spider.log`

---

## ✅ 下一步

- [ ] 运行测试确保环境正常
- [ ] 尝试运行不同的爬虫
- [ ] 查看抓取的数据
- [ ] 阅读详细文档了解更多功能

---

**祝您使用愉快！** 🎉

如有问题，请参考详细文档或查看日志文件。
