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
from django.contrib.auth.models import User
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
def bad_review_rank(request):
    """
    差评榜单 - 根据时间范围和问题类型统计投诉数据
    POST 请求参数:
        - time_range: 时间范围 ('1m' 近1个月, '6m' 近半年, '1y' 近一年, 或具体月份 '2024-01')
        - category: 问题分类 ('quality' 质量问题, 'service' 服务问题, 'other' 其他问题, 空表示全部)
        - page: 页码 (默认 1)
        - pagesize: 每页数量 (默认 20)
    返回格式: {"total": 总数, "records": [数据列表], "start_date": 开始日期, "end_date": 结束日期}
    """
    try:
        try:
            data = json.loads(request.body)
        except:
            data = {}
        
        time_range = data.get('time_range', '1y')
        category = data.get('category', '')  # 'quality', 'service', 'other' 或空
        page = int(data.get('page', 1))
        pagesize = int(data.get('pagesize', 20))
        
        # 计算时间范围
        now = datetime.now()
        end_date = now
        
        if time_range == '1m':  # 近1个月
            start_date = now - timedelta(days=30)
        elif time_range == '6m':  # 近半年
            start_date = now - timedelta(days=180)
        elif time_range == '1y':  # 近一年
            start_date = now - timedelta(days=365)
        else:  # 具体月份，如 '2024-01'
            try:
                # 解析月份格式
                start_date = datetime.strptime(time_range + '-01', '%Y-%m-%d')
                # 计算月末
                if start_date.month == 12:
                    end_date = start_date.replace(year=start_date.year + 1, month=1, day=1) - timedelta(days=1)
                else:
                    end_date = start_date.replace(month=start_date.month + 1, day=1) - timedelta(days=1)
                end_date = end_date.replace(hour=23, minute=59, second=59)
            except:
                # 默认近一年
                start_date = now - timedelta(days=365)
                end_date = now
        
        # 查询投诉数据
        queryset = CarIssue.objects.select_related(
            'car_series', 
            'car_series__brand'
        ).filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        )
        
        # 按问题分类筛选 - 检查category字段是否存在
        if category:
            # 先检查模型是否有category字段
            if hasattr(CarIssue, 'category'):
                queryset = queryset.filter(category=category)
        
        # 按车系聚合统计
        issue_stats = queryset.values(
            'car_series__id',
            'car_series__name',
            'car_series__brand__name',
            'car_series__image'
        ).annotate(
            issue_count=Count('id'),  # 问题种类数
            total_reports=Sum('report_count')  # 总投诉次数
        )
        
        # 如果caregory字段存在，添加分类统计
        if hasattr(CarIssue, 'category'):
            issue_stats = issue_stats.annotate(
                quality_count=Count('id', filter=Q(category='quality')),  # 质量问题数
                service_count=Count('id', filter=Q(category='service')),  # 服务问题数
                other_count=Count('id', filter=Q(category='other'))  # 其他问题数
            )
        
        issue_stats = issue_stats.order_by('-total_reports')  # 按总投诉次数排序
        
        # 分页
        total = issue_stats.count()
        start = (page - 1) * pagesize
        end = start + pagesize
        records = list(issue_stats[start:end])
        
        # 格式化返回数据
        formatted_records = []
        for idx, item in enumerate(records, start=start + 1):
            record = {
                'rank': idx,
                'car_series_id': item['car_series__id'],
                'car_series_name': item['car_series__name'],
                'brand_name': item['car_series__brand__name'],
                'series_image': item['car_series__image'] or '',
                'issue_count': item['issue_count'],
                'total_reports': item['total_reports'] or 0,
            }
            
            # 如果category字段存在，添加分类统计
            if hasattr(CarIssue, 'category'):
                record['quality_count'] = item.get('quality_count', 0)
                record['service_count'] = item.get('service_count', 0)
                record['other_count'] = item.get('other_count', 0)
            else:
                # 如果没有category字段，返回0
                record['quality_count'] = 0
                record['service_count'] = 0
                record['other_count'] = 0
            
            formatted_records.append(record)
        
        return JsonResponse({
            'total': total,
            'records': formatted_records,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
        })
    
    except Exception as e:
        # 返回错误信息
        import traceback
        error_msg = str(e)
        traceback_msg = traceback.format_exc()
        print(f"Error in bad_review_rank: {error_msg}")
        print(traceback_msg)
        
        return JsonResponse({
            'error': '服务器错误',
            'message': error_msg,
            'total': 0,
            'records': [],
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': datetime.now().strftime('%Y-%m-%d'),
        }, status=500)


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
@require_http_methods(["GET", "POST"])
def price_discount_ranking(request):
    """
    车系降价排行榜 - 返回JSON数据供前端渲染横向条形图
    按 (price_max - price_min) 计算降价幅度，返回TOP数据
    """
    try:
        # 获取limit参数
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
            except:
                data = {}
            limit = int(data.get('limit', 15))
        else:
            limit = int(request.GET.get('limit', 15))
        
        # 查询所有有价格区间的车系，计算降价幅度
        car_series = CarSeries.objects.select_related('brand').filter(
            price_min__isnull=False,
            price_max__isnull=False
        ).exclude(
            price_min=0,
            price_max=0
        )
        
        # 计算降价幅度并排序
        discount_list = []
        for car in car_series:
            discount = float(car.price_max) - float(car.price_min)
            if discount > 0:
                discount_list.append({
                    'series_name': f"{car.brand.name} {car.name}",
                    'brand_name': car.brand.name,
                    'car_name': car.name,
                    'price_min': float(car.price_min),
                    'price_max': float(car.price_max),
                    'discount': round(discount, 2)
                })
        
        # 按降价幅度排序，取TOP
        discount_list.sort(key=lambda x: x['discount'], reverse=True)
        result = discount_list[:limit]
        
        return JsonResponse({
            'code': 200,
            'message': '成功',
            'data': result
        })
        
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'服务器错误: {str(e)}',
            'data': []
        }, status=500)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def brand_count_distribution(request):
    """
    汽车品牌车系数量TOP分布 - 返回JSON数据供前端渲染环形图
    统计每个品牌下的车系数量
    """
    try:
        # 获取limit参数
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
            except:
                data = {}
            limit = int(data.get('limit', 10))
        else:
            limit = int(request.GET.get('limit', 10))
        
        # 按品牌统计车系数量
        brand_stats = CarSeries.objects.values(
            'brand__id',
            'brand__name'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:limit]
        
        result = []
        for item in brand_stats:
            result.append({
                'brand_id': item['brand__id'],
                'brand_name': item['brand__name'],
                'count': item['count']
            })
        
        return JsonResponse({
            'code': 200,
            'message': '成功',
            'data': result
        })
        
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'服务器错误: {str(e)}',
            'data': []
        }, status=500)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def price_range_distribution(request):
    """
    价格范围数量分布 - 返回JSON数据供前端渲染柱状图
    按价格区间统计车系数量
    """
    try:
        # 定义价格区间
        price_ranges = [
            {'name': '10万以下', 'min': 0, 'max': 10},
            {'name': '10-15万', 'min': 10, 'max': 15},
            {'name': '15-20万', 'min': 15, 'max': 20},
            {'name': '20-25万', 'min': 20, 'max': 25},
            {'name': '25-30万', 'min': 25, 'max': 30},
            {'name': '30-40万', 'min': 30, 'max': 40},
            {'name': '40-50万', 'min': 40, 'max': 50},
            {'name': '50万以上', 'min': 50, 'max': 9999},
        ]
        
        result = []
        for range_item in price_ranges:
            if range_item['max'] == 9999:
                # 50万以上
                count = CarSeries.objects.filter(
                    price_min__gte=range_item['min']
                ).count()
            else:
                # 其他区间
                count = CarSeries.objects.filter(
                    price_min__gte=range_item['min'],
                    price_min__lt=range_item['max']
                ).count()
            
            result.append({
                'range': range_item['name'],
                'count': count,
                'min': range_item['min'],
                'max': range_item['max']
            })
        
        return JsonResponse({
            'code': 200,
            'message': '成功',
            'data': result
        })
        
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'服务器错误: {str(e)}',
            'data': []
        }, status=500)


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


# ==================== RESTful API (GET请求) ====================

@csrf_exempt
def get_cars_list(request):
    """
    获取车型列表 (GET请求)
    支持多条件筛选和分页
    
    查询参数:
        - page: 页码
        - page_size: 每页数量
        - brand_ids: 品牌ID列表(逗号分隔)
        - price_min: 最低价格
        - price_max: 最高价格
        - energy_types: 能源类型(逗号分隔)
        - seats: 座位数(逗号分隔)
        - levels: 车型级别(逗号分隔)
        - sort_by: 排序方式
    """
    try:
        # 获取查询参数
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 12))
        brand_ids = request.GET.get('brand_ids', '')
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        energy_types = request.GET.get('energy_types', '')
        seats = request.GET.get('seats', '')
        levels = request.GET.get('levels', '')
        sort_by = request.GET.get('sort_by', 'price_asc')
        
        # 构建查询
        queryset = CarSeries.objects.select_related('brand').all()
        
        # 品牌筛选
        if brand_ids:
            brand_id_list = [int(x) for x in brand_ids.split(',') if x]
            queryset = queryset.filter(brand_id__in=brand_id_list)
        
        # 价格筛选
        if price_min:
            queryset = queryset.filter(price_min__gte=float(price_min))
        if price_max:
            queryset = queryset.filter(price_max__lte=float(price_max))
        
        # 能源类型筛选
        if energy_types:
            energy_type_list = [x.strip() for x in energy_types.split(',') if x]
            queryset = queryset.filter(fuel_type__in=energy_type_list)
        
        # 车身类型筛选(暂时用body_type字段)
        if levels:
            level_list = [x.strip() for x in levels.split(',') if x]
            queryset = queryset.filter(body_type__in=level_list)
        
        # 排序
        if sort_by == 'price_asc':
            queryset = queryset.order_by('price_min')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price_max')
        elif sort_by == 'name_asc':
            queryset = queryset.order_by('name')
        elif sort_by == 'name_desc':
            queryset = queryset.order_by('-name')
        else:
            queryset = queryset.order_by('-created_at')
        
        # 总数
        total = queryset.count()
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        cars = queryset[start:end]
        
        # 格式化返回数据
        data = []
        for car in cars:
            data.append({
                'id': car.id,
                'name': car.name,
                'series_id': car.id,
                'series_name': car.name,
                'brand_id': car.brand.id,
                'brand_name': car.brand.name,
                'price': float(car.price_min) if car.price_min else None,
                'image': car.image,
                'energy_type': car.get_fuel_type_display(),
                'level': car.body_type,
                'description': car.description,
            })
        
        return JsonResponse({
            'code': 200,
            'message': '成功',
            'data': data,
            'total': total,
            'page': page,
            'page_size': page_size
        })
        
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }, status=500)


@csrf_exempt
def get_filter_options(request):
    """
    获取筛选条件的可选项
    返回能源类型、座位数、车型级别等选项
    """
    try:
        # 能源类型(从CHOICES中获取)
        energy_types = [choice[1] for choice in CarSeries.FUEL_TYPE_CHOICES]
        
        # 车身类型(从现有数据中获取)
        body_types = CarSeries.objects.exclude(
            body_type__isnull=True
        ).exclude(
            body_type=''
        ).values_list('body_type', flat=True).distinct()
        
        return JsonResponse({
            'code': 200,
            'message': '成功',
            'data': {
                'energy_types': list(energy_types),
                'seats': [4, 5, 6, 7],  # 常见座位数
                'levels': list(body_types)  # 车型级别使用车身类型
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }, status=500)


@csrf_exempt
def get_brands_list(request):
    """
    获取品牌列表 (GET请求)
    支持分页
    """
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('pageSize', 100))
        
        # 查询所有品牌
        brands = Brand.objects.all().order_by('name')
        
        # 总数
        total = brands.count()
        
        # 分页
        start = (page - 1) * page_size
        end = start + page_size
        brands_page = brands[start:end]
        
        # 格式化数据
        data = []
        for brand in brands_page:
            data.append({
                'id': brand.id,
                'name': brand.name,
                'logo': brand.logo,
                'country': brand.country
            })
        
        return JsonResponse({
            'code': 200,
            'message': '成功',
            'data': data,
            'total': total
        })
        
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }, status=500)


@csrf_exempt
def get_statistics(request):
    """
    获取系统统计数据 (GET请求)
    """
    try:
        # 统计车辆总数（车系数量）
        total_cars = CarSeries.objects.count()
        
        # 统计品牌数量
        total_brands = Brand.objects.count()
        
        # 统计用户数量
        total_users = User.objects.count()
        
        # 今日访问（模拟数据，后续可以通过访问日志统计）
        today_visits = 342
        
        return JsonResponse({
            'code': 200,
            'message': '成功',
            'data': {
                'totalCars': total_cars,
                'totalBrands': total_brands,
                'totalUsers': total_users,
                'todayVisits': today_visits
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'code': 500,
            'message': f'服务器错误: {str(e)}'
        }, status=500)
