/**
 * 用户认证API
 */
import request from './request'

/**
 * 用户注册参数
 */
export interface RegisterParams {
  username: string
  password: string
  email?: string
}

/**
 * 用户登录参数
 */
export interface LoginParams {
  username: string
  password: string
}

/**
 * 用户信息
 */
export interface UserInfo {
  id: number
  username: string
  email?: string
  is_active: boolean
  is_superuser: boolean
}

/**
 * Token响应
 */
export interface TokenResponse {
  access_token: string
  token_type: string
}

/**
 * 用户注册
 */
export const register = (data: RegisterParams) => {
  return request<UserInfo>({
    url: '/api/v1/auth/register',
    method: 'post',
    data
  })
}

/**
 * 用户登录
 */
export const login = (data: LoginParams) => {
  return request<TokenResponse>({
    url: '/api/v1/auth/login',
    method: 'post',
    data
  })
}

/**
 * 获取当前用户信息
 */
export const getUserInfo = () => {
  return request<UserInfo>({
    url: '/api/v1/auth/me',
    method: 'get'
  })
}

/**
 * 退出登录
 */
export const logout = () => {
  return request({
    url: '/api/v1/auth/logout',
    method: 'post'
  })
}
