/**
 * Django 后端 API 封装
 * 所有请求使用 POST 方法，参数通过 data 传递
 */
import axios from 'axios'

// 创建 axios 实例
const instance = axios.create({
  baseURL: 'http://localhost:8000',  // Django 后端地址
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 响应拦截器
instance.interceptors.response.use(
  response => response.data,
  error => {
    console.error('API 请求错误:', error)
    return Promise.reject(error)
  }
)

/**
 * 销量排行榜
 * @param data { month: '1m'|'3m'|'1y', page: number, pagesize: number }
 */
export function getSalesRank(data: {
  month?: string
  page?: number
  pagesize?: number
}) {
  return instance.post('/api/cars/sales-rank/', data)
}

/**
 * 质量问题排行榜
 * @param data { severity: 'low'|'medium'|'high'|'', page: number, pagesize: number }
 */
export function getIssueRank(data: {
  severity?: string
  page?: number
  pagesize?: number
}) {
  return instance.post('/api/cars/issue-rank/', data)
}

/**
 * 获取车系详情
 * @param data { car_series_id: number }
 */
export function getCarDetail(data: { car_series_id: number }) {
  return instance.post('/api/cars/detail/', data)
}

/**
 * 获取可视化分析图表配置
 */
export function getCarAnalysis() {
  return instance.post('/api/cars/analysis/', {})
}

/**
 * 条件选车
 * @param data 筛选条件
 */
export function filterCars(data: {
  brand_id?: number
  fuel_type?: string
  min_price?: number
  max_price?: number
  min_endurance?: number
  body_type?: string
  page?: number
  pagesize?: number
}) {
  return instance.post('/api/cars/filter/', data)
}

/**
 * 获取品牌列表
 */
export function getBrandList() {
  return instance.post('/api/cars/brands/', {})
}
