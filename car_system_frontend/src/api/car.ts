import { request } from './request'
import type { Car, CarListParams, CarListResponse } from '@/types/car'

/**
 * 条件查询车型列表
 */
export interface QueryCarsParams {
  page?: number
  page_size?: number
  brand_ids?: string  // 逗号分隔的品牌ID
  price_min?: number
  price_max?: number
  energy_types?: string  // 逗号分隔的能源类型
  seats?: string  // 逗号分隔的座位数
  levels?: string  // 逗号分隔的车型级别
  sort_by?: string
}

export interface CarItemResponse {
  id: number
  name: string
  series_id: number
  series_name: string
  brand_id: number
  brand_name: string
  price?: number
  image?: string
  energy_type?: string
  seats?: number
  level?: string
  description?: string
  acceleration?: number
  fuel_consumption?: number
}

export interface PageResponse<T> {
  data: T[]
  total: number
  page: number
  page_size: number
}

/**
 * 筛选条件选项
 */
export interface FilterOptions {
  energy_types: string[]
  seats: number[]
  levels: string[]
}

// 获取车辆列表
export function getCarList(params: CarListParams): Promise<CarListResponse> {
  return request({
    url: '/cars',
    method: 'get',
    params
  })
}

/**
 * 条件查询车型列表 - Django后端
 */
export function queryCars(params: QueryCarsParams): Promise<any> {
  return request({
    url: '/api/cars/v1/cars',
    method: 'get',
    params
  })
}

/**
 * 获取筛选条件选项 - Django后端
 */
export function getFilterOptions(): Promise<any> {
  return request({
    url: '/api/cars/v1/cars/filters',
    method: 'get'
  })
}

// 获取车辆详情
export function getCarDetail(id: number): Promise<Car> {
  return request({
    url: `/cars/${id}`,
    method: 'get'
  })
}

// 搜索车辆
export function searchCars(keyword: string) {
  return request({
    url: '/cars/search',
    method: 'get',
    params: { keyword }
  })
}
