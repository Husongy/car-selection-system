import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'

// 创建axios实例
const service: AxiosInstance = axios.create({
  baseURL: '/',  // 修改为/，因为vite代理已经将/api转发到后端
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json;charset=utf-8'
  }
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    // 可以在这里添加token等
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    const res = response.data
    
    // 如果返回的状态码不是200，则判断为错误
    if (res.code && res.code !== 200) {
      console.error('接口错误:', res.message || 'Error')
      return Promise.reject(new Error(res.message || 'Error'))
    }
    
    // Django后端返回格式: {code: 200, message: 'xx', data: [...], total: xx}
    // 如果有code字段，说昏Django后端，返回完整的res对象
    if (res.code !== undefined) {
      return res
    }
    
    // 其他情况直接返回
    return res
  },
  (error) => {
    console.error('响应错误:', error.message)
    
    // 处理401未授权错误
    if (error.response && error.response.status === 401) {
      // 清除token
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
      
      // 跳转到登录页（如果不在登录页）
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    
    return Promise.reject(error)
  }
)

// 导出request方法
export function request<T = any>(config: AxiosRequestConfig): Promise<T> {
  return service.request(config)
}

export default service
