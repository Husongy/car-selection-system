<template>
  <div class="select-car-container">
    <n-space vertical :size="24">
      <!-- 筛选条件卡片 -->
      <n-card title="条件筛选">
        <n-space vertical :size="16">
          <n-grid :cols="24" :x-gap="16">
            <!-- 品牌多选 -->
            <n-grid-item :span="8">
              <n-form-item label="品牌">
                <n-select
                  v-model:value="selectedBrandIds"
                  multiple
                  :options="brandOptions"
                  placeholder="请选择品牌"
                  clearable
                  @update:value="handleBrandChange"
                />
              </n-form-item>
            </n-grid-item>

            <!-- 价格区间滑块 -->
            <n-grid-item :span="8">
              <n-form-item label="价格区间（万元）">
                <n-slider
                  v-model:value="priceRange"
                  range
                  :min="0"
                  :max="200"
                  :step="5"
                  :marks="priceMarks"
                  @update:value="handlePriceChange"
                />
              </n-form-item>
            </n-grid-item>

            <!-- 排序方式 -->
            <n-grid-item :span="8">
              <n-form-item label="排序方式">
                <n-select
                  v-model:value="sortBy"
                  :options="sortOptions"
                  @update:value="handleSortChange"
                />
              </n-form-item>
            </n-grid-item>

            <!-- 能源类型 -->
            <n-grid-item :span="8">
              <n-form-item label="能源类型">
                <n-checkbox-group
                  v-model:value="selectedEnergyTypes"
                  @update:value="handleEnergyTypeChange"
                >
                  <n-space>
                    <n-checkbox
                      v-for="type in energyTypeOptions"
                      :key="type.value"
                      :value="type.value"
                      :label="type.label"
                    />
                  </n-space>
                </n-checkbox-group>
              </n-form-item>
            </n-grid-item>

            <!-- 座位数 -->
            <n-grid-item :span="8">
              <n-form-item label="座位数">
                <n-checkbox-group
                  v-model:value="selectedSeats"
                  @update:value="handleSeatsChange"
                >
                  <n-space>
                    <n-checkbox
                      v-for="seat in seatOptions"
                      :key="seat.value"
                      :value="seat.value"
                      :label="seat.label"
                    />
                  </n-space>
                </n-checkbox-group>
              </n-form-item>
            </n-grid-item>

            <!-- 车型级别 -->
            <n-grid-item :span="8">
              <n-form-item label="车型级别">
                <n-checkbox-group
                  v-model:value="selectedLevels"
                  @update:value="handleLevelChange"
                >
                  <n-space>
                    <n-checkbox
                      v-for="level in levelOptions"
                      :key="level.value"
                      :value="level.value"
                      :label="level.label"
                    />
                  </n-space>
                </n-checkbox-group>
              </n-form-item>
            </n-grid-item>
          </n-grid>

          <!-- 操作按钮 -->
          <n-space>
            <n-button type="primary" @click="handleSearch">
              <template #icon>
                <n-icon><SearchOutline /></n-icon>
              </template>
              搜索
            </n-button>
            <n-button @click="handleReset">
              <template #icon>
                <n-icon><RefreshOutline /></n-icon>
              </template>
              重置
            </n-button>
          </n-space>
        </n-space>
      </n-card>

      <!-- 结果展示区域 -->
      <n-card>
        <template #header>
          <n-space align="center" justify="space-between">
            <span>车型列表</span>
            <n-text depth="3">共 {{ selectCarStore.pagination.total }} 条结果</n-text>
          </n-space>
        </template>

        <n-spin :show="selectCarStore.loading">
          <!-- 车型卡片网格 -->
          <n-grid v-if="selectCarStore.carList.length > 0" :cols="3" :x-gap="16" :y-gap="16">
            <n-grid-item v-for="car in selectCarStore.carList" :key="car.id">
              <n-card hoverable class="car-card" @click="handleViewDetail(car)">
                <template #cover>
                  <div class="car-image-wrapper">
                    <img
                      :src="car.image || 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaHQ9IjMwMCIgZmlsbD0iI2YwZjBmMCIvPjx0ZXh0IHg9IjUwJSIgeT0iNTAlIiBmb250LXNpemU9IjE4IiBmaWxsPSIjOTk5IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkeT0iLjNlbSI+5pqC5peg5Zu+54mHPC90ZXh0Pjwvc3ZnPg=='"
                      :alt="car.name"
                      class="car-image"
                    />
                  </div>
                </template>
                
                <template #header>
                  <n-ellipsis :line-clamp="1" :tooltip="{ width: 300 }">
                    {{ car.name }}
                  </n-ellipsis>
                </template>

                <template #header-extra>
                  <n-tag v-if="car.price" type="error" size="small">
                    {{ car.price.toFixed(2) }}万
                  </n-tag>
                </template>

                <n-space vertical :size="8">
                  <n-space>
                    <n-tag type="info" size="small">{{ car.brand_name }}</n-tag>
                    <n-tag v-if="car.level" type="success" size="small">{{ car.level }}</n-tag>
                  </n-space>

                  <n-text depth="3" style="font-size: 13px">
                    {{ car.series_name }}
                  </n-text>

                  <n-space v-if="car.energy_type || car.seats">
                    <n-text v-if="car.energy_type" depth="3" style="font-size: 12px">
                      <n-icon><FlashOutline /></n-icon> {{ car.energy_type }}
                    </n-text>
                    <n-text v-if="car.seats" depth="3" style="font-size: 12px">
                      <n-icon><PeopleOutline /></n-icon> {{ car.seats }}座
                    </n-text>
                  </n-space>

                  <n-space v-if="car.acceleration || car.fuel_consumption">
                    <n-text v-if="car.acceleration" depth="3" style="font-size: 12px">
                      <n-icon><SpeedometerOutline /></n-icon> {{ car.acceleration }}s
                    </n-text>
                    <n-text v-if="car.fuel_consumption" depth="3" style="font-size: 12px">
                      <n-icon><WaterOutline /></n-icon> {{ car.fuel_consumption }}L
                    </n-text>
                  </n-space>
                </n-space>
              </n-card>
            </n-grid-item>
          </n-grid>

          <!-- 空状态 -->
          <n-empty
            v-else
            description="暂无符合条件的车型"
            style="padding: 60px 0"
          >
            <template #icon>
              <n-icon size="80"><CarSportOutline /></n-icon>
            </template>
          </n-empty>

          <!-- 分页 -->
          <n-space v-if="selectCarStore.carList.length > 0" justify="center" style="margin-top: 24px">
            <n-pagination
              v-model:page="currentPage"
              v-model:page-size="pageSize"
              :item-count="selectCarStore.pagination.total"
              show-size-picker
              :page-sizes="[12, 24, 36, 48]"
              @update:page="handlePageChange"
              @update:page-size="handlePageSizeChange"
            >
              <template #prefix="{ itemCount }">
                共 {{ itemCount }} 条
              </template>
            </n-pagination>
          </n-space>
        </n-spin>
      </n-card>
    </n-space>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useMessage } from 'naive-ui'
import { 
  SearchOutline, 
  RefreshOutline, 
  CarSportOutline,
  FlashOutline,
  PeopleOutline,
  SpeedometerOutline,
  WaterOutline
} from '@vicons/ionicons5'
import { useSelectCarStore } from '@/stores/selectCar'
import type { CarItem } from '@/stores/selectCar'
import { queryCars, getFilterOptions, type QueryCarsParams } from '@/api/car'
import { getBrands } from '@/api/home'

const message = useMessage()
const selectCarStore = useSelectCarStore()

// ========== 筛选条件状态 ==========
const selectedBrandIds = ref<number[]>([])
const priceRange = ref<[number, number]>([0, 200])
const selectedEnergyTypes = ref<string[]>([])
const selectedSeats = ref<number[]>([])
const selectedLevels = ref<string[]>([])
const sortBy = ref('price_asc')

// ========== 分页状态 ==========
const currentPage = ref(1)
const pageSize = ref(24)  // 增加到24，显示更多车型

// ========== 筛选选项 ==========
const brandOptions = ref<Array<{ label: string; value: number }>>([])
const energyTypeOptions = ref<Array<{ label: string; value: string }>>([])
const seatOptions = ref<Array<{ label: string; value: number }>>([])
const levelOptions = ref<Array<{ label: string; value: string }>>([])

// 价格滑块标记
const priceMarks = {
  0: '0',
  50: '50',
  100: '100',
  150: '150',
  200: '200万+'
}

// 排序选项
const sortOptions = [
  { label: '价格从低到高', value: 'price_asc' },
  { label: '价格从高到低', value: 'price_desc' },
  { label: '名称升序', value: 'name_asc' },
  { label: '名称降序', value: 'name_desc' }
]

// ========== 数据加载方法 ==========

/**
 * 加载品牌列表
 */
const loadBrands = async () => {
  try {
    const response = await getBrands({ page: 1, pageSize: 100 }) as any
    console.log('品牌列表响应:', response)
    
    // Django后端返回: {code: 200, data: [...], total: xx}
    const brands = (response && response.data && Array.isArray(response.data)) ? response.data : []
    
    brandOptions.value = brands.map((brand: any) => ({
      label: brand.name,
      value: brand.id
    }))
    
    console.log('品牌选项:', brandOptions.value)
  } catch (error) {
    console.error('加载品牌列表失败:', error)
  }
}

/**
 * 加载筛选条件选项
 */
const loadFilterOptions = async () => {
  try {
    const response = await getFilterOptions() as any
    console.log('筛选选项响应:', response)
    
    // Django后端返回: {code: 200, data: {energy_types: [...], seats: [...], levels: [...]}}
    const options = response.data || {}
    
    // 能源类型选项
    if (options.energy_types && Array.isArray(options.energy_types)) {
      energyTypeOptions.value = options.energy_types.map((type: string) => ({
        label: type,
        value: type
      }))
    }
    
    // 座位数选项
    if (options.seats && Array.isArray(options.seats)) {
      seatOptions.value = options.seats.map((seat: number) => ({
        label: `${seat}座`,
        value: seat
      }))
    }
    
    // 车型级别选项
    if (options.levels && Array.isArray(options.levels)) {
      levelOptions.value = options.levels.map((level: string) => ({
        label: level,
        value: level
      }))
    }
  } catch (error: any) {
    console.error('加载筛选选项失败:', error)
    console.error('错误详情:', error.response?.data || error.message)
  }
}

/**
 * 加载车型列表
 */
const loadCarList = async () => {
  selectCarStore.setLoading(true)
  
  try {
    // 构建查询参数
    const params: QueryCarsParams = {
      page: currentPage.value,
      page_size: pageSize.value,
      sort_by: sortBy.value
    }
    
    // 品牌筛选
    if (selectedBrandIds.value.length > 0) {
      params.brand_ids = selectedBrandIds.value.join(',')
    }
    
    // 价格区间
    if (priceRange.value[0] > 0) {
      params.price_min = priceRange.value[0]
    }
    if (priceRange.value[1] < 200) {
      params.price_max = priceRange.value[1]
    }
    
    // 能源类型
    if (selectedEnergyTypes.value.length > 0) {
      params.energy_types = selectedEnergyTypes.value.join(',')
    }
    
    // 座位数
    if (selectedSeats.value.length > 0) {
      params.seats = selectedSeats.value.map(String).join(',')
    }
    
    // 车型级别
    if (selectedLevels.value.length > 0) {
      params.levels = selectedLevels.value.join(',')
    }
    
    console.log('查询参数:', params)
    
    // 请求数据
    const response = await queryCars(params) as any
    
    console.log('API响应:', response)
    
    // Django后端返回格式: {code: 200, data: [...], total: xx, page: xx, page_size: xx}
    if (response && response.data && Array.isArray(response.data)) {
      // 更新store
      selectCarStore.updateCarList(response.data, response.total || 0)
      selectCarStore.setPage(response.page || currentPage.value)
    } else {
      console.warn('响应数据格式异常:', response)
      selectCarStore.clearCarList()
    }
    
  } catch (error: any) {
    console.error('加载车型列表失败:', error)
    console.error('错误详情:', error.response?.data || error.message)
    message.error(error.response?.data?.message || error.message || '加载车型列表失败，请稍后重试')
    selectCarStore.clearCarList()
  } finally {
    selectCarStore.setLoading(false)
  }
}

// ========== 事件处理方法 ==========

/**
 * 品牌选择改变
 */
const handleBrandChange = (value: number[]) => {
  selectedBrandIds.value = value
  selectCarStore.setBrandIds(value)
}

/**
 * 价格区间改变
 */
const handlePriceChange = (value: [number, number]) => {
  priceRange.value = value
  selectCarStore.setPriceRange(value[0] > 0 ? value[0] : null, value[1] < 200 ? value[1] : null)
}

/**
 * 能源类型改变
 */
const handleEnergyTypeChange = (value: string[]) => {
  selectedEnergyTypes.value = value
  selectCarStore.setEnergyTypes(value)
}

/**
 * 座位数改变
 */
const handleSeatsChange = (value: number[]) => {
  selectedSeats.value = value
  selectCarStore.setSeats(value)
}

/**
 * 车型级别改变
 */
const handleLevelChange = (value: string[]) => {
  selectedLevels.value = value
  selectCarStore.setLevels(value)
}

/**
 * 排序方式改变
 */
const handleSortChange = (value: string) => {
  sortBy.value = value
  selectCarStore.setSortBy(value)
  loadCarList()
}

/**
 * 搜索按钮点击
 */
const handleSearch = () => {
  currentPage.value = 1
  loadCarList()
}

/**
 * 重置按钮点击
 */
const handleReset = () => {
  selectedBrandIds.value = []
  priceRange.value = [0, 200]
  selectedEnergyTypes.value = []
  selectedSeats.value = []
  selectedLevels.value = []
  sortBy.value = 'price_asc'
  currentPage.value = 1
  
  selectCarStore.resetFilters()
  loadCarList()
}

/**
 * 页码改变
 */
const handlePageChange = (page: number) => {
  currentPage.value = page
  selectCarStore.setPage(page)
  loadCarList()
}

/**
 * 每页数量改变
 */
const handlePageSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  selectCarStore.setPageSize(size)
  loadCarList()
}

/**
 * 查看车型详情
 */
const handleViewDetail = (car: CarItem) => {
  message.info(`查看 ${car.name} 的详情`)
  // TODO: 跳转到详情页
}

// ========== 生命周期 ==========

onMounted(async () => {
  // 加载筛选选项
  await Promise.all([
    loadBrands(),
    loadFilterOptions()
  ])
  
  // 加载车型列表
  await loadCarList()
})
</script>

<style scoped>
.select-car-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.car-card {
  cursor: pointer;
  transition: all 0.3s ease;
  height: 100%;
}

.car-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.car-image-wrapper {
  width: 100%;
  height: 200px;
  overflow: hidden;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.car-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
