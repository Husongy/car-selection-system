import { request } from './request'

// 获取统计数据
export function getStatistics() {
  return request({
    url: '/statistics',
    method: 'get'
  })
}

// 获取健康检查
export function getHealth() {
  return request({
    url: '/health',
    method: 'get'
  })
}
