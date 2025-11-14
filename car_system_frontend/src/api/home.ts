import { request } from './request'

/**
 * 品牌查询参数
 */
export interface BrandQueryParams {
  page?: number
  pageSize?: number
  keyword?: string
  initial?: string
}

/**
 * 品牌响应数据
 */
export interface BrandResponse {
  id: number
  name: string
  initial: string
  logo?: string
  description?: string
  series_count?: number
}

/**
 * 分页响应
 */
export interface PageResponse<T> {
  data: T[]
  total: number
  page: number
  page_size: number
}

// 获取统计数据
export function getStatistics() {
  return request({
    url: '/api/v1/statistics',
    method: 'get'
  })
}

// 获取健康检查
export function getHealth() {
  return request({
    url: '/api/v1/health',
    method: 'get'
  })
}

/**
 * 获取品牌列表
 */
export function getBrands(params: BrandQueryParams): Promise<PageResponse<BrandResponse>> {
  return request({
    url: '/api/v1/brands',
    method: 'get',
    params
  })
}
