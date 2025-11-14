# 销量榜单功能设置指南

## 功能概述

销量榜单功能允许用户查看不同时间周期内汽车销量排名，支持以下查询周期：
- 近一年
- 近半年
- 近三个月
- 上个月
- 自定义月份（YYYY-MM格式）

## 后端设置步骤

### 1. 安装依赖

```bash
cd car_system_backend
pip install -r requirements.txt
```

### 2. 创建数据库表

使用 Alembic 创建迁移并应用：

```bash
# 生成迁移文件
alembic revision --autogenerate -m "add sales_data table"

# 应用迁移
alembic upgrade head
```

### 3. 生成模拟销量数据

```bash
python generate_sales_data.py
```

此脚本会：
- 为所有车系生成近12个月的模拟销量数据
- 显示销量TOP 10排行榜
- 数据包含季节性波动特征

### 4. 启动后端服务

```bash
python run.py
```

服务启动后，访问 http://localhost:8000/docs 查看API文档。

## API 端点

### 获取销量排名

**端点**: `GET /api/v1/sales-ranking`

**查询参数**:
- `period` (string): 查询周期
  - `last_year`: 近一年
  - `last_6months`: 近半年
  - `last_3months`: 近三个月
  - `last_month`: 上个月
  - `YYYY-MM`: 自定义月份，如 `2024-10`
- `limit` (integer): 返回数量限制，默认50，最大100

**请求示例**:
```bash
# 查询近一年销量排名
curl "http://localhost:8000/api/v1/sales-ranking?period=last_year&limit=50"

# 查询2024年10月销量排名
curl "http://localhost:8000/api/v1/sales-ranking?period=2024-10&limit=20"
```

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "period": "last_year",
    "start_date": "2023-11",
    "end_date": "2024-11",
    "total_count": 50,
    "data": [
      {
        "rank": 1,
        "series_id": 123,
        "series_name": "Model Y",
        "brand_name": "特斯拉",
        "total_sales": 125000,
        "series_image": "https://example.com/image.jpg",
        "price_range": "26.39-39.79万",
        "energy_type": "纯电动"
      }
    ]
  }
}
```

## 前端设置步骤

### 1. 访问销量榜单页面

前端路由已配置为 `/sales-ranking`

启动前端服务后，访问：
```
http://localhost:5173/sales-ranking
```

### 2. 功能特性

- **周期选择**: 使用单选按钮快速选择预设周期
- **自定义月份**: 使用日期选择器选择特定月份
- **排名展示**: 前3名显示奖牌图标和特殊颜色
- **数据表格**: 
  - 支持分页
  - 显示车系图片、名称、品牌、销量等信息
  - 销量列支持排序
  - 能源类型使用标签显示
- **统计信息**: 显示查询周期、日期范围、上榜车型数量

## 数据库表结构

### sales_data 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| series_id | INTEGER | 车系ID（外键） |
| sales_count | INTEGER | 销量数量 |
| year | INTEGER | 年份 |
| month | INTEGER | 月份 |
| period | VARCHAR(20) | 销售周期(YYYY-MM) |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

**索引**:
- `idx_series_period`: (series_id, period)
- `idx_year_month`: (year, month)

## 疑难解答

### 1. 数据库迁移失败

确保：
- `.env` 文件中数据库配置正确
- 数据库服务正在运行
- 已导入所有模型到 `app/models/__init__.py`

### 2. 没有销量数据

运行数据生成脚本：
```bash
python generate_sales_data.py
```

### 3. API返回空数据

检查：
- 数据库中是否有销量记录
- 查询的时间周期是否包含数据
- 数据库表是否正确创建

## 扩展功能建议

1. **真实数据集成**: 连接真实销量数据源
2. **图表展示**: 添加ECharts图表可视化
3. **趋势分析**: 显示同比、环比增长率
4. **导出功能**: 支持Excel/CSV导出
5. **筛选功能**: 按品牌、能源类型筛选
6. **详情页**: 点击车系查看详细销量趋势
