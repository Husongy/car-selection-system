/**
 * 用户认证 API
 */
import request from './request'

/**
 * 用户注册
 */
export function register(data: { username: string; password: string; email?: string }) {
  return request({
    url: '/api/users/register/',
    method: 'post',
    data
  })
}

/**
 * 用户登录
 */
export function login(data: { username: string; password: string }) {
  return request({
    url: '/api/users/login/',
    method: 'post',
    data
  })
}
