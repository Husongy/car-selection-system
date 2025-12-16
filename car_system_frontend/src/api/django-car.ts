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

/**
 * 差评榜单 - 根据时间范围和问题类型统计投诉数据
 * @param data {
 *   time_range: '1m'|'6m'|'1y'|具体月份(2024-01),
 *   category: 'quality'|'service'|'other'|'',
 *   page: number,
 *   pagesize: number
 * }
 */
export function getBadReviewRank(data: {
  time_range?: string
  category?: string
  page?: number
  pagesize?: number
}) {
  return instance.post('/api/cars/bad-review-rank/', data)
}

// 导出类型定义
export interface BadReviewRankItem {
  rank: number
  car_series_id: number
  car_series_name: string
  brand_name: string
  series_image: string
  issue_count: number
  total_reports: number
  quality_count: number
  service_count: number
  other_count: number
}

// 降价排行项
export interface PriceDiscountItem {
  series_name: string
  brand_name: string
  car_name: string
  price_min: number
  price_max: number
  discount: number
}

// 品牌车系数量项
export interface BrandCountItem {
  brand_id: number
  brand_name: string
  count: number
}

// 价格区间数量项
export interface PriceRangeItem {
  range: string
  count: number
  min: number
  max: number
}

/**
 * 获取车系降价排行榜
 * @param limit 返回数量限制
 */
export function getPriceDiscountRanking(limit: number = 15) {
  return instance.post<any, { code: number; message: string; data: PriceDiscountItem[] }>(
    '/api/cars/analysis/price-discount/',
    { limit }
  )
}

/**
 * 获取品牌车系数量分布
 * @param limit 返回数量限制
 */
export function getBrandCountDistribution(limit: number = 10) {
  return instance.post<any, { code: number; message: string; data: BrandCountItem[] }>(
    '/api/cars/analysis/brand-count/',
    { limit }
  )
}

/**
 * 获取价格区间分布
 */
export function getPriceRangeDistribution() {
  return instance.post<any, { code: number; message: string; data: PriceRangeItem[] }>(
    '/api/cars/analysis/price-range/',
    {}
  )
}
