import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

/**
 * 条件选车筛选参数接口
 */
export interface SelectCarFilters {
  brandIds: number[]
  priceMin: number | null
  priceMax: number | null
  energyTypes: string[]
  seats: number[]
  levels: string[]
  sortBy: string
}

/**
 * 分页状态接口
 */
export interface PaginationState {
  page: number
  pageSize: number
  total: number
}

/**
 * 车型列表项接口
 */
export interface CarItem {
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

/**
 * 条件选车Store
 * 管理筛选条件、分页状态和车型列表数据
 */
export const useSelectCarStore = defineStore('selectCar', () => {
  // ========== 状态定义 ==========
  
  // 筛选条件
  const filters = ref<SelectCarFilters>({
    brandIds: [],
    priceMin: null,
    priceMax: null,
    energyTypes: [],
    seats: [],
    levels: [],
    sortBy: 'price_asc'
  })

  // 分页状态
  const pagination = ref<PaginationState>({
    page: 1,
    pageSize: 12,
    total: 0
  })

  // 车型列表
  const carList = ref<CarItem[]>([])

  // 加载状态
  const loading = ref(false)

  // ========== 计算属性 ==========
  
  // 总页数
  const totalPages = computed(() => {
    return Math.ceil(pagination.value.total / pagination.value.pageSize)
  })

  // 是否有筛选条件
  const hasFilters = computed(() => {
    return (
      filters.value.brandIds.length > 0 ||
      filters.value.priceMin !== null ||
      filters.value.priceMax !== null ||
      filters.value.energyTypes.length > 0 ||
      filters.value.seats.length > 0 ||
      filters.value.levels.length > 0
    )
  })

  // ========== 操作方法 ==========

  /**
   * 设置筛选条件
   */
  const setFilters = (newFilters: Partial<SelectCarFilters>) => {
    filters.value = { ...filters.value, ...newFilters }
    // 筛选条件改变时重置到第一页
    pagination.value.page = 1
  }

  /**
   * 重置筛选条件
   */
  const resetFilters = () => {
    filters.value = {
      brandIds: [],
      priceMin: null,
      priceMax: null,
      energyTypes: [],
      seats: [],
      levels: [],
      sortBy: 'price_asc'
    }
    pagination.value.page = 1
  }

  /**
   * 设置品牌ID列表
   */
  const setBrandIds = (brandIds: number[]) => {
    filters.value.brandIds = brandIds
    pagination.value.page = 1
  }

  /**
   * 设置价格区间
   */
  const setPriceRange = (min: number | null, max: number | null) => {
    filters.value.priceMin = min
    filters.value.priceMax = max
    pagination.value.page = 1
  }

  /**
   * 设置能源类型
   */
  const setEnergyTypes = (types: string[]) => {
    filters.value.energyTypes = types
    pagination.value.page = 1
  }

  /**
   * 设置座位数
   */
  const setSeats = (seats: number[]) => {
    filters.value.seats = seats
    pagination.value.page = 1
  }

  /**
   * 设置车型级别
   */
  const setLevels = (levels: string[]) => {
    filters.value.levels = levels
    pagination.value.page = 1
  }

  /**
   * 设置排序方式
   */
  const setSortBy = (sortBy: string) => {
    filters.value.sortBy = sortBy
    pagination.value.page = 1
  }

  /**
   * 设置当前页
   */
  const setPage = (page: number) => {
    pagination.value.page = page
  }

  /**
   * 设置每页数量
   */
  const setPageSize = (pageSize: number) => {
    pagination.value.pageSize = pageSize
    pagination.value.page = 1
  }

  /**
   * 更新车型列表
   */
  const updateCarList = (cars: CarItem[], total: number) => {
    carList.value = cars
    pagination.value.total = total
  }

  /**
   * 设置加载状态
   */
  const setLoading = (status: boolean) => {
    loading.value = status
  }

  /**
   * 清空车型列表
   */
  const clearCarList = () => {
    carList.value = []
    pagination.value.total = 0
  }

  return {
    // 状态
    filters,
    pagination,
    carList,
    loading,
    
    // 计算属性
    totalPages,
    hasFilters,
    
    // 方法
    setFilters,
    resetFilters,
    setBrandIds,
    setPriceRange,
    setEnergyTypes,
    setSeats,
    setLevels,
    setSortBy,
    setPage,
    setPageSize,
    updateCarList,
    setLoading,
    clearCarList
  }
})
