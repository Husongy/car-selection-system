export * from './car'

// API通用响应类型
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}
