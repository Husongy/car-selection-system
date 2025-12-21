<template>
  <div class="select-car-page">
    <n-grid :cols="24" :x-gap="20">
      <!-- 左侧筛选区 -->
      <n-gi :span="5">
        <n-card title="筛选条件" :bordered="false" class="filter-card">
          <n-form label-placement="top" size="small">
            <!-- 品牌选择 -->
            <n-form-item label="品牌">
              <n-select
                v-model:value="filters.brand_id"
                :options="brandOptions"
                placeholder="全部品牌"
                clearable
                filterable
              />
            </n-form-item>

            <!-- 能源类型 -->
            <n-form-item label="能源类型">
              <n-radio-group v-model:value="filters.fuel_type" size="small">
                <n-space vertical>
                  <n-radio value="">&#x5168;&#x90e8;</n-radio>
                  <n-radio value="BEV">纯电动</n-radio>
                  <n-radio value="PHEV">插电混动</n-radio>
                  <n-radio value="HEV">混合动力</n-radio>
                </n-space>
              </n-radio-group>
            </n-form-item>

            <!-- 价格范围 -->
            <n-form-item label="价格范围">
              <n-space vertical style="width: 100%">
                <n-button-group size="small">
                  <n-button :type="priceRange === '0-15' ? 'primary' : 'default'" @click="setPriceRange(0, 15)">15万以下</n-button>
                  <n-button :type="priceRange === '15-25' ? 'primary' : 'default'" @click="setPriceRange(15, 25)">15-25万</n-button>
                </n-button-group>
                <n-button-group size="small">
                  <n-button :type="priceRange === '25-40' ? 'primary' : 'default'" @click="setPriceRange(25, 40)">25-40万</n-button>
                  <n-button :type="priceRange === '40-999' ? 'primary' : 'default'" @click="setPriceRange(40, 999)">40万以上</n-button>
                </n-button-group>
                <n-space>
                  <n-input-number
                    v-model:value="filters.min_price"
                    placeholder="最低"
                    :min="0"
                    size="small"
                    style="width: 80px"
                  />
                  <span>-</span>
                  <n-input-number
                    v-model:value="filters.max_price"
                    placeholder="最高"
                    :min="0"
                    size="small"
                    style="width: 80px"
                  />
                  <span>万</span>
                </n-space>
              </n-space>
            </n-form-item>

            <!-- 续航里程 -->
            <n-form-item label="最低续航">
              <n-slider
                v-model:value="filters.min_endurance"
                :min="0"
                :max="800"
                :step="50"
                :marks="{ 0: '0', 300: '300km', 500: '500km', 800: '800km' }"
              />
            </n-form-item>

            <!-- 车身类型 -->
            <n-form-item label="车身类型">
              <n-checkbox-group v-model:value="bodyTypeList">
                <n-space>
                  <n-checkbox value="SUV">SUV</n-checkbox>
                  <n-checkbox value="轿车">轿车</n-checkbox>
                  <n-checkbox value="MPV">MPV</n-checkbox>
                  <n-checkbox value="两厢车">两厢</n-checkbox>
                </n-space>
              </n-checkbox-group>
            </n-form-item>

            <!-- 操作按钮 -->
            <n-space vertical style="width: 100%">
              <n-button type="primary" block :loading="loading" @click="handleSearch">
                <template #icon><n-icon><SearchOutline /></n-icon></template>
                搜索车型
              </n-button>
              <n-button block @click="handleReset" quaternary>
                重置条件
              </n-button>
            </n-space>
          </n-form>
        </n-card>
      </n-gi>

      <!-- 右侧结果区 -->
      <n-gi :span="19">
        <!-- 结果统计栏 -->
        <n-space justify="space-between" align="center" style="margin-bottom: 16px">
          <n-space align="center">
            <n-tag type="success" size="large">
              共找到 <strong>{{ totalRecords }}</strong> 款车型
            </n-tag>
            <n-tag v-if="filters.fuel_type" type="info" closable @close="filters.fuel_type = ''; handleSearch()">
              {{ fuelTypeMap[filters.fuel_type] }}
            </n-tag>
            <n-tag v-if="filters.min_price || filters.max_price" type="info" closable @close="filters.min_price = null; filters.max_price = null; priceRange = ''; handleSearch()">
              {{ filters.min_price || 0 }}-{{ filters.max_price || '∞' }}万
            </n-tag>
          </n-space>
          <n-radio-group v-model:value="viewMode" size="small">
            <n-radio-button value="card">卡片视图</n-radio-button>
            <n-radio-button value="table">列表视图</n-radio-button>
          </n-radio-group>
        </n-space>

        <!-- 卡片视图 -->
        <div v-if="viewMode === 'card'" class="car-grid">
          <n-spin :show="loading">
            <div class="car-cards">
              <div v-for="car in tableData" :key="car.id" class="car-card" @click="goToDetail(car)">
                <div class="car-image">
                  <img :src="getCarImage(car)" :alt="car.name" referrerpolicy="no-referrer" @error="handleImageError" />
                  <n-tag :type="getFuelTypeColor(car.fuel_type)" size="small" class="fuel-tag">
                    {{ fuelTypeMap[car.fuel_type] || car.fuel_type }}
                  </n-tag>
                </div>
                <div class="car-info">
                  <div class="car-name">{{ car.brand_name }} {{ car.name }}</div>
                  <div class="car-price">
                    <span class="price-value">{{ car.price_min }}-{{ car.price_max }}</span>
                    <span class="price-unit">万</span>
                  </div>
                  <div class="car-specs">
                    <n-tag size="tiny" :bordered="false">{{ car.body_type || 'SUV' }}</n-tag>
                    <n-tag size="tiny" :bordered="false" v-if="car.endurance_max">续航{{ car.endurance_max }}km</n-tag>
                  </div>
                </div>
              </div>
            </div>
            <n-empty v-if="!loading && tableData.length === 0" description="暂无符合条件的车型" />
          </n-spin>
        </div>

        <!-- 列表视图 -->
        <n-card v-else :bordered="false">
          <n-data-table
            :columns="columns"
            :data="tableData"
            :loading="loading"
            :bordered="false"
            striped
          />
        </n-card>

        <!-- 分页器 -->
        <n-pagination
          v-model:page="currentPage"
          :page-count="totalPages"
          :page-size="pageSize"
          show-size-picker
          :page-sizes="[12, 24, 36, 48]"
          @update:page="handlePageChange"
          @update:page-size="handlePageSizeChange"
          style="margin-top: 20px; justify-content: center"
        />
      </n-gi>
    </n-grid>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, h } from 'vue'
import { useRouter } from 'vue-router'
import {
  NGrid,
  NGi,
  NCard,
  NForm,
  NFormItem,
  NSelect,
  NInputNumber,
  NSpace,
  NButton,
  NButtonGroup,
  NDataTable,
  NPagination,
  NTag,
  NRadioGroup,
  NRadio,
  NRadioButton,
  NCheckboxGroup,
  NCheckbox,
  NSlider,
  NIcon,
  NSpin,
  NEmpty,
  NImage
} from 'naive-ui'
import { SearchOutline } from '@vicons/ionicons5'
import type { DataTableColumns, SelectOption } from 'naive-ui'
import { filterCars, getBrandList } from '@/api/django-car'

const router = useRouter()

// 生成SVG占位图
const createPlaceholderSvg = (text: string, bgColor: string = '#f0f0f0') => {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200" viewBox="0 0 300 200">
    <rect width="300" height="200" fill="${bgColor}"/>
    <text x="150" y="100" font-family="Arial" font-size="16" fill="#666" text-anchor="middle" dominant-baseline="middle">${text}</text>
  </svg>`
  return `data:image/svg+xml,${encodeURIComponent(svg)}`
}

// 品牌颜色映射
const brandColors: Record<string, string> = {
  '特斯拉': '#cc0000',
  '比亚迪': '#1a73e8',
  '蔚来': '#003366',
  '小鹏': '#ff6600',
  '理想': '#00b4ff',
  '问界': '#ff3366',
  '极氪': '#333333',
  '广汽埃安': '#00a0e9',
  '哪吒': '#ff5500',
  '零跑': '#4a90d9',
  '小米': '#ff6900',
  '五菱': '#e60012',
  '方程豹': '#c41e3a',
  '吉利': '#1e3a8a',
  '大众': '#001e50',
  '丰田': '#eb0a1e',
  '日产': '#c3002f',
  '奥迪': '#bb0a30',
}

// 获取车辆图片
const getCarImage = (car: any) => {
  // 检查图片是否有效（排除无效的外部API链接）
  if (car.image && 
      car.image.startsWith('http') && 
      !car.image.includes('api.nio.com') && 
      !car.image.includes('oip.byd.com') &&
      !car.image.includes('yccdn.cn')) {
    return car.image
  }
  // 使用品牌颜色生成占位图
  const bgColor = brandColors[car.brand_name] || '#667788'
  return createPlaceholderSvg(`${car.brand_name} ${car.name}`, bgColor)
}

// 点击车辆卡片，跳转到详情页
const goToDetail = (car: any) => {
  router.push(`/django/car-detail/${car.id}`)
}

// 图片加载失败处理
const handleImageError = (e: Event) => {
  const img = e.target as HTMLImageElement
  img.src = createPlaceholderSvg('暂无图片', '#f5f5f5')
}

// 视图模式
const viewMode = ref<'card' | 'table'>('card')

// 价格范围快捷选择
const priceRange = ref('')

const setPriceRange = (min: number, max: number) => {
  filters.value.min_price = min
  filters.value.max_price = max === 999 ? null : max
  priceRange.value = `${min}-${max}`
  handleSearch()
}

// 车身类型多选
const bodyTypeList = ref<string[]>([])

watch(bodyTypeList, (val) => {
  filters.value.body_type = val.join(',')
})

// 能源类型映射
const fuelTypeMap: Record<string, string> = {
  'BEV': '纯电动',
  'PHEV': '插电混动',
  'HEV': '混合动力'
}

// 获取能源类型颜色
const getFuelTypeColor = (type: string) => {
  const colors: Record<string, 'success' | 'info' | 'warning'> = {
    'BEV': 'success',
    'PHEV': 'info',
    'HEV': 'warning'
  }
  return colors[type] || 'default'
}

// 筛选条件
const filters = ref({
  brand_id: null as number | null,
  fuel_type: '' as string,
  min_price: null as number | null,
  max_price: null as number | null,
  min_endurance: 0 as number,
  body_type: ''
})

// 分页数据
const currentPage = ref(1)
const pageSize = ref(12)
const totalRecords = ref(0)
const tableData = ref<any[]>([])
const loading = ref(false)

// 品牌选项
const brandOptions = ref<SelectOption[]>([])

// 计算总页数
const totalPages = computed(() => Math.ceil(totalRecords.value / pageSize.value))

// 表格列定义
const columns: DataTableColumns = [
  {
    title: '图片',
    key: 'image',
    width: 120,
    render(row: any) {
      return h(NImage, {
        src: getCarImage(row),
        width: 100,
        height: 60,
        objectFit: 'cover',
        lazy: true,
        fallbackSrc: createPlaceholderSvg('暂无图片'),
        imgProps: { referrerpolicy: 'no-referrer' }
      })
    }
  },
  {
    title: '品牌',
    key: 'brand_name',
    width: 80
  },
  {
    title: '车系名称',
    key: 'name',
    ellipsis: { tooltip: true },
    render(row: any) {
      return h('a', {
        style: { color: '#1a73e8', cursor: 'pointer' },
        onClick: () => goToDetail(row)
      }, row.name)
    }
  },
  {
    title: '能源类型',
    key: 'fuel_type',
    width: 90,
    render(row: any) {
      return h(NTag, { type: getFuelTypeColor(row.fuel_type), size: 'small' }, 
        { default: () => fuelTypeMap[row.fuel_type] || row.fuel_type })
    }
  },
  {
    title: '价格(万)',
    key: 'price',
    width: 120,
    render(row: any) {
      return row.price_min && row.price_max ? `${row.price_min}-${row.price_max}` : '-'
    }
  },
  {
    title: '续航(km)',
    key: 'endurance',
    width: 100,
    render(row: any) {
      return row.endurance_max ? `${row.endurance_max}` : '-'
    }
  },
  {
    title: '车身类型',
    key: 'body_type',
    width: 80
  },
  {
    title: '操作',
    key: 'action',
    width: 80,
    render(row: any) {
      return h(NButton, {
        size: 'small',
        type: 'primary',
        text: true,
        onClick: () => goToDetail(row)
      }, { default: () => '查看' })
    }
  }
]

// 加载品牌列表
const loadBrands = async () => {
  try {
    const response: any = await getBrandList()
    brandOptions.value = (response.records || []).map((brand: any) => ({
      label: brand.name,
      value: brand.id
    }))
  } catch (error) {
    console.error('加载品牌列表失败:', error)
  }
}

// 加载车系数据
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      ...filters.value,
      page: currentPage.value,
      pagesize: pageSize.value
    }
    
    const response: any = await filterCars(params)
    
    tableData.value = response.records || []
    totalRecords.value = response.total || 0
  } catch (error) {
    console.error('加载车系数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 查询
const handleSearch = () => {
  currentPage.value = 1
  loadData()
}

// 重置
const handleReset = () => {
  filters.value = {
    brand_id: null,
    fuel_type: '',
    min_price: null,
    max_price: null,
    min_endurance: 0,
    body_type: ''
  }
  bodyTypeList.value = []
  priceRange.value = ''
  currentPage.value = 1
  loadData()
}

// 分页事件
const handlePageChange = (page: number) => {
  currentPage.value = page
  loadData()
}

const handlePageSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  loadData()
}

// 组件挂载时加载数据
onMounted(() => {
  loadBrands()
  loadData()
})
</script>

<style scoped>
.select-car-page {
  padding: 20px;
  background: #f5f5f5;
  min-height: 100vh;
}

.filter-card {
  position: sticky;
  top: 20px;
}

.car-grid {
  min-height: 400px;
}

.car-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}

.car-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.car-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.car-image {
  position: relative;
  height: 160px;
  background: #f0f0f0;
  overflow: hidden;
}

.car-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.fuel-tag {
  position: absolute;
  top: 8px;
  left: 8px;
}

.car-info {
  padding: 12px 16px;
}

.car-name {
  font-size: 15px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.car-price {
  margin-bottom: 8px;
}

.price-value {
  font-size: 18px;
  font-weight: 700;
  color: #e74c3c;
}

.price-unit {
  font-size: 12px;
  color: #999;
  margin-left: 2px;
}

.car-specs {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
</style>
