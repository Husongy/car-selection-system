#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
API 测试脚本 - 测试条件选车API功能
"""
import requests
import json


BASE_URL = "http://localhost:8000/api/v1"


def test_get_all_cars():
    """测试获取所有车系"""
    print("\n" + "=" * 60)
    print("测试1: 获取所有车系（默认参数）")python run.py
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/cars")
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"总数: {data['pagination']['total']}")
        print(f"当前页: {data['pagination']['page']}")
        print(f"每页数量: {data['pagination']['page_size']}")
        print(f"\n前3条数据:")
        for item in data['items'][:3]:
            print(f"  - {item['brand_name']} {item['name']}: {item['price_min']}-{item['price_max']}万 (评分: {item['total_score']})")
    else:
        print(f"错误: {response.text}")


def test_filter_by_brand():
    """测试按品牌筛选"""
    print("\n" + "=" * 60)
    print("测试2: 按品牌筛选（品牌=比亚迪）")
    print("=" * 60)
    
    params = {
        "brand_name": "比亚迪"
    }
    response = requests.get(f"{BASE_URL}/cars", params=params)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"找到 {data['pagination']['total']} 个车系")
        for item in data['items']:
            print(f"  - {item['name']}: {item['price_min']}-{item['price_max']}万")


def test_filter_by_price():
    """测试按价格筛选"""
    print("\n" + "=" * 60)
    print("测试3: 按价格筛选（15-30万）")
    print("=" * 60)
    
    params = {
        "min_price": 15,
        "max_price": 30
    }
    response = requests.get(f"{BASE_URL}/cars", params=params)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"找到 {data['pagination']['total']} 个车系")
        for item in data['items'][:5]:
            print(f"  - {item['brand_name']} {item['name']}: {item['price_min']}-{item['price_max']}万")


def test_filter_by_fuel_type():
    """测试按燃料类型筛选"""
    print("\n" + "=" * 60)
    print("测试4: 按燃料类型筛选（纯电动）")
    print("=" * 60)
    
    params = {
        "fuel_type": "纯电动"
    }
    response = requests.get(f"{BASE_URL}/cars", params=params)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"找到 {data['pagination']['total']} 个纯电动车系")
        for item in data['items'][:5]:
            print(f"  - {item['brand_name']} {item['name']}: {item['fuel_type']}")


def test_complex_filter():
    """测试复合筛选"""
    print("\n" + "=" * 60)
    print("测试5: 复合筛选（纯电动 + 20-40万 + 评分≥4.5）")
    print("=" * 60)
    
    params = {
        "fuel_type": "纯电动",
        "min_price": 20,
        "max_price": 40,
        "min_score": 4.5,
        "order_by": "total_score",
        "order_direction": "desc"
    }
    response = requests.get(f"{BASE_URL}/cars", params=params)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"找到 {data['pagination']['total']} 个符合条件的车系")
        for item in data['items']:
            print(f"  - {item['brand_name']} {item['name']}: {item['price_min']}-{item['price_max']}万 (评分: {item['total_score']})")


def test_pagination():
    """测试分页"""
    print("\n" + "=" * 60)
    print("测试6: 分页（第2页，每页3条）")
    print("=" * 60)
    
    params = {
        "page": 2,
        "page_size": 3
    }
    response = requests.get(f"{BASE_URL}/cars", params=params)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"总页数: {data['pagination']['total_pages']}")
        print(f"当前页: {data['pagination']['page']}")
        print(f"是否有下一页: {data['pagination']['has_next']}")
        print(f"是否有上一页: {data['pagination']['has_prev']}")
        print(f"\n当前页数据:")
        for item in data['items']:
            print(f"  - {item['brand_name']} {item['name']}")


def test_get_car_detail():
    """测试获取车系详情"""
    print("\n" + "=" * 60)
    print("测试7: 获取车系详情（ID=1）")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/cars/1")
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"车系名称: {data['name']}")
        print(f"品牌: {data['brand']['name']}")
        print(f"价格: {data['price_min']}-{data['price_max']}万")
        print(f"燃料类型: {data['fuel_type']}")
        if data.get('scores'):
            print(f"总评分: {data['scores']['total_score']}")
            print(f"  - 舒适性: {data['scores']['comfort_score']}")
            print(f"  - 外观: {data['scores']['appearance_score']}")
            print(f"  - 动力: {data['scores']['power_score']}")


def test_get_brands():
    """测试获取品牌列表"""
    print("\n" + "=" * 60)
    print("测试8: 获取所有品牌")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/brands")
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"品牌数量: {len(data)}")
        for brand in data:
            print(f"  - {brand['name']}")


if __name__ == '__main__':
    print("\n" + "🚀 开始测试 FastAPI 车系查询接口")
    print("请确保后端服务已启动: python run.py")
    
    try:
        # 先测试健康检查
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 后端服务运行正常\n")
        else:
            print("❌ 后端服务未启动，请先运行: python run.py")
            exit(1)
        
        # 执行所有测试
        test_get_all_cars()
        test_filter_by_brand()
        test_filter_by_price()
        test_filter_by_fuel_type()
        test_complex_filter()
        test_pagination()
        test_get_car_detail()
        test_get_brands()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试完成！")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到后端服务")
        print("请确保后端服务已启动: python run.py")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
