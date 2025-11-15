"""
汽车相关视图 - 使用 FBV (函数式视图)
所有接口均接收 POST 请求,使用 JsonResponse 返回数据
"""
import json
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Sum, Count
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts
from .models import Brand, CarSeries, CarSale, CarIssue


# ==================== 辅助函数 ====================

def to_dict(obj, fields=None):
    """
    将模型实例或 QuerySet 转换为字典
    :param obj: 模型实例或 QuerySet
    :param fields: 需要转换的字段列表,为None时转换所有字段
    :return: 字典或字典列表
    """
    # 如果是 QuerySet,递归转换每个对象
    if hasattr(obj, 'model'):
        return [to_dict(item, fields) for item in obj]
    
    # 转换单个对象
    result = {}
    if fields is None:
        # 获取所有字段
        fields = [f.name for f in obj._meta.fields]
    
    for field in fields:
        value = getattr(obj, field, None)
        # 处理外键字段
        if hasattr(value, 'id'):
            result[field] = value.id
            result[f"{field}_name"] = str(value)
        # 处理日期时间
        elif isinstance(value, datetime):
            result[field] = value.strftime('%Y-%m-%d %H:%M:%S')
        # 处理 Decimal
        elif hasattr(value, '__str__') and 'Decimal' in str(type(value)):
            result[field] = float(value)
        else:
            result[field] = value
    
    return result


# ==================== API 视图 ====================

@csrf_exempt
@require_http_methods(["POST"])
def car_sales_rank(request):
    """
    销量排行榜
    POST 请求参数:
        - month: 月份 ('1m' 最近1个月, '3m' 最近3个月, '1y' 最近1年)
        - page: 页码 (默认 1)
        - pagesize: 每页数量 (默认 20)
    返回格式: {"total": 总数, "records": [数据列表]}
    """
    try:
        data = json.loads(request.body)
    except:
        data = {}
    
    month_range = data.get('month', '1m')
    page = int(data.get('page', 1))
    pagesize = int(data.get('pagesize', 20))
    
    # 计算时间范围
    now = datetime.now()
    if month_range == '1m':
        start_month = (now - timedelta(days=30)).strftime('%Y-%m')
    elif month_range == '3m':
        start_month = (now - timedelta(days=90)).strftime('%Y-%m')
    else:  # '1y'
        start_month = (now - timedelta(days=365)).strftime('%Y-%m')
    
    # 聚合查询:按车系统计销量
    sales_data = CarSale.objects.filter(
        month__gte=start_month
    ).values(
        'car_series__id',
        'car_series__name',
        'car_series__brand__name'
    ).annotate(
        total_sales=Sum('sales')
    ).order_by('-total_sales')
    
    # 分页
    total = sales_data.count()
    start = (page - 1) * pagesize
    end = start + pagesize
    records = list(sales_data[start:end])
    
    # 格式化返回数据
    formatted_records = []
    for idx, item in enumerate(records, start=start + 1):
        formatted_records.append({
            'rank': idx,
            'car_series_id': item['car_series__id'],
            'car_series_name': item['car_series__name'],
            'brand_name': item['car_series__brand__name'],
            'total_sales': item['total_sales'],
        })
    
    return JsonResponse({
        'total': total,
        'records': formatted_records
    })


@csrf_exempt
@require_http_methods(["POST"])
def car_issue_rank(request):
    """
    质量问题排行榜
    POST 请求参数:
        - severity: 严重程度筛选 ('low', 'medium', 'high', 或为空表示全部)
        - page: 页码
        - pagesize: 每页数量
    返回格式: {"total": 总数, "records": [数据列表]}
    """
    try:
        data = json.loads(request.body)
    except:
        data = {}
    
    severity = data.get('severity', '')
    page = int(data.get('page', 1))
    pagesize = int(data.get('pagesize', 20))
    
    # 查询
    queryset = CarIssue.objects.select_related('car_series', 'car_series__brand')
    
    if severity:
        queryset = queryset.filter(severity=severity)
    
    # 按车系聚合统计问题数
    issue_data = queryset.values(
        'car_series__id',
        'car_series__name',
        'car_series__brand__name'
    ).annotate(
        issue_count=Count('id'),
        total_reports=Sum('report_count')
    ).order_by('-total_reports')
    
    # 分页
    total = issue_data.count()
    start = (page - 1) * pagesize
    end = start + pagesize
    records = list(issue_data[start:end])
    
    # 格式化
    formatted_records = []
    for idx, item in enumerate(records, start=start + 1):
        formatted_records.append({
            'rank': idx,
            'car_series_id': item['car_series__id'],
            'car_series_name': item['car_series__name'],
            'brand_name': item['car_series__brand__name'],
            'issue_count': item['issue_count'],
            'total_reports': item['total_reports'],
        })
    
    return JsonResponse({
        'total': total,
        'records': formatted_records
    })


@csrf_exempt
@require_http_methods(["POST"])
def get_detail(request):
    """
    获取车系详情
    POST 请求参数:
        - car_series_id: 车系 ID
    """
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({'error': '请求参数错误'}, status=400)
    
    car_series_id = data.get('car_series_id')
    
    if not car_series_id:
        return JsonResponse({'error': '缺少 car_series_id 参数'}, status=400)
    
    try:
        car_series = CarSeries.objects.select_related('brand').get(id=car_series_id)
    except CarSeries.DoesNotExist:
        return JsonResponse({'error': '车系不存在'}, status=404)
    
    # 转换为字典
    detail = to_dict(car_series)
    
    # 添加品牌信息
    detail['brand'] = to_dict(car_series.brand)
    
    # 添加最近3个月销量数据
    recent_sales = car_series.sales.all()[:3]
    detail['recent_sales'] = to_dict(recent_sales, fields=['month', 'sales'])
    
    # 添加质量问题数据
    issues = car_series.issues.all()[:5]
    detail['recent_issues'] = to_dict(issues, fields=['issue_type', 'severity', 'report_count'])
    
    return JsonResponse(detail)


@csrf_exempt
@require_http_methods(["POST"])
def car_series_analysis(request):
    """
    车系价格分布分析 - 使用 pyecharts 生成图表配置
    返回 ECharts 图表 JSON 配置
    """
    # 按价格区间统计车系数量
    price_ranges = [
        ('0-15万', 0, 15),
        ('15-25万', 15, 25),
        ('25-35万', 25, 35),
        ('35-50万', 35, 50),
        ('50万+', 50, 999),
    ]
    
    range_names = []
    range_counts = []
    
    for name, min_price, max_price in price_ranges:
        if max_price == 999:
            count = CarSeries.objects.filter(price_min__gte=min_price).count()
        else:
            count = CarSeries.objects.filter(
                price_min__gte=min_price,
                price_max__lt=max_price
            ).count()
        range_names.append(name)
        range_counts.append(count)
    
    # 使用 pyecharts 生成柱状图
    bar = (
        Bar()
        .add_xaxis(range_names)
        .add_yaxis("车系数量", range_counts)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="新能源汽车价格分布"),
            xaxis_opts=opts.AxisOpts(name="价格区间"),
            yaxis_opts=opts.AxisOpts(name="车系数量"),
        )
    )
    
    # 返回图表配置 JSON
    return HttpResponse(bar.dump_options(), content_type="application/json")


@csrf_exempt
@require_http_methods(["POST"])
def filter_cars(request):
    """
    条件选车 - 根据品牌、能源类型、价格等筛选车系
    POST 请求参数:
        - brand_id: 品牌 ID (可选)
        - fuel_type: 能源类型 ('BEV', 'PHEV', 'HEV', 可选)
        - min_price: 最低价格 (可选)
        - max_price: 最高价格 (可选)
        - min_endurance: 最低续航 (可选)
        - body_type: 车身类型 (可选)
        - page: 页码 (默认 1)
        - pagesize: 每页数量 (默认 20)
    返回格式: {"total": 总数, "records": [数据列表]}
    """
    try:
        data = json.loads(request.body)
    except:
        data = {}
    
    # 获取筛选条件
    brand_id = data.get('brand_id')
    fuel_type = data.get('fuel_type')
    min_price = data.get('min_price')
    max_price = data.get('max_price')
    min_endurance = data.get('min_endurance')
    body_type = data.get('body_type')
    page = int(data.get('page', 1))
    pagesize = int(data.get('pagesize', 20))
    
    # 构建查询
    queryset = CarSeries.objects.select_related('brand').all()
    
    # 使用 Q 对象进行条件筛选
    if brand_id:
        queryset = queryset.filter(brand_id=brand_id)
    
    if fuel_type:
        queryset = queryset.filter(fuel_type=fuel_type)
    
    if min_price is not None:
        queryset = queryset.filter(Q(price_min__gte=min_price) | Q(price_max__gte=min_price))
    
    if max_price is not None:
        queryset = queryset.filter(Q(price_min__lte=max_price) | Q(price_max__lte=max_price))
    
    if min_endurance is not None:
        queryset = queryset.filter(Q(endurance_min__gte=min_endurance) | Q(endurance_max__gte=min_endurance))
    
    if body_type:
        queryset = queryset.filter(body_type__icontains=body_type)
    
    # 按创建时间排序
    queryset = queryset.order_by('-created_at')
    
    # 分页
    total = queryset.count()
    start = (page - 1) * pagesize
    end = start + pagesize
    records = queryset[start:end]
    
    # 转换为字典
    formatted_records = []
    for car in records:
        item = to_dict(car)
        item['brand_name'] = car.brand.name
        formatted_records.append(item)
    
    return JsonResponse({
        'total': total,
        'records': formatted_records
    })


@csrf_exempt
@require_http_methods(["POST"])
def brand_list(request):
    """
    获取所有品牌列表 (用于下拉框)
    """
    brands = Brand.objects.all().order_by('name')
    brand_list = to_dict(brands, fields=['id', 'name', 'logo'])
    
    return JsonResponse({
        'total': len(brand_list),
        'records': brand_list
    })
