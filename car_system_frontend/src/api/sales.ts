/**
 * 销量榜单API
 */
import request from './request'

export interface SalesRankingItem {
  rank: number
  series_id: number
  series_name: string
  brand_name: string
  total_sales: number
  series_image?: string
  price_range?: string
  energy_type?: string
}

export interface SalesRankingResponse {
  period: string
  start_date: string
  end_date: string
  total_count: number
  data: SalesRankingItem[]
}

/**
 * 获取销量排名
 * @param period 查询周期
 * @param limit 返回数量限制
 */
export const getSalesRanking = (period: string = 'last_year', limit: number = 50) => {
  return request<SalesRankingResponse>({
    url: '/api/v1/sales-ranking',
    method: 'get',
    params: {
      period,
      limit
    }
  })
}
