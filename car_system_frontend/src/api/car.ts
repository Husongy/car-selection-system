import { request } from './request'
import type { Car, CarListParams, CarListResponse } from '@/types/car'

// 获取车辆列表
export function getCarList(params: CarListParams): Promise<CarListResponse> {
  return request({
    url: '/cars',
    method: 'get',
    params
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
