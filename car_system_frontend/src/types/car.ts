// 车辆信息类型
export interface Car {
  id: number
  name: string
  brand: string
  type: string
  price: number
  range: number
  image: string
  description: string
}

// 车辆列表请求参数
export interface CarListParams {
  page?: number
  pageSize?: number
  priceRange?: string | null
  range?: string | null
  carType?: string | null
}

// 车辆列表响应
export interface CarListResponse {
  data: Car[]
  total: number
  totalPages: number
  currentPage: number
}
