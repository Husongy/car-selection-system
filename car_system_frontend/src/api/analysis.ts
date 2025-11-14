/**
 * 可视化分析API
 */
import request from './request'

/**
 * 降价排行项
 */
export interface PriceDiscountItem {
  series_name: string
  discount: number
}

/**
 * 品牌车系数量项
 */
export interface BrandCountItem {
  brand_name: string
  count: number
}

/**
 * 价格区间数量项
 */
export interface PriceRangeItem {
  range: string
  count: number
}

/**
 * 获取车系降价排行榜
 * @param limit 返回数量限制
 */
export const getPriceDiscountRanking = (limit: number = 30) => {
  return request<PriceDiscountItem[]>({
    url: '/api/v1/analysis/price-discount',
    method: 'get',
    params: { limit }
  })
}

/**
 * 获取品牌车系数量分布
 * @param limit 返回数量限制
 */
export const getBrandCountDistribution = (limit: number = 30) => {
  return request<BrandCountItem[]>({
    url: '/api/v1/analysis/brand-count',
    method: 'get',
    params: { limit }
  })
}

/**
 * 获取价格区间分布
 */
export const getPriceRangeDistribution = () => {
  return request<PriceRangeItem[]>({
    url: '/api/v1/analysis/price-range',
    method: 'get'
  })
}
