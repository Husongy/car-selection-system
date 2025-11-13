<template>
  <div class="select-car-container">
    <n-space vertical :size="24">
      <n-card title="智能选车">
        <n-space vertical :size="16">
          <!-- 筛选条件 -->
          <n-form
            ref="formRef"
            :model="formValue"
            label-placement="left"
            label-width="auto"
          >
            <n-grid :cols="3" :x-gap="24">
              <n-form-item-gi label="价格区间">
                <n-select
                  v-model:value="formValue.priceRange"
                  :options="priceRangeOptions"
                  placeholder="请选择价格区间"
                />
              </n-form-item-gi>
              <n-form-item-gi label="续航里程">
                <n-select
                  v-model:value="formValue.range"
                  :options="rangeOptions"
                  placeholder="请选择续航里程"
                />
              </n-form-item-gi>
              <n-form-item-gi label="车型类别">
                <n-select
                  v-model:value="formValue.carType"
                  :options="carTypeOptions"
                  placeholder="请选择车型类别"
                />
              </n-form-item-gi>
            </n-grid>
            <n-space>
              <n-button type="primary" @click="handleSearch">
                搜索
              </n-button>
              <n-button @click="handleReset">
                重置
              </n-button>
            </n-space>
          </n-form>
        </n-space>
      </n-card>

      <!-- 车辆列表 -->
      <n-card title="推荐车辆">
        <n-spin :show="loading">
          <n-list hoverable clickable>
            <n-list-item v-for="car in carList" :key="car.id">
              <template #prefix>
                <n-avatar
                  :size="80"
                  :src="car.image"
                  fallback-src="https://via.placeholder.com/80"
                />
              </template>
              <n-thing :title="car.name" :description="car.brand">
                <template #description>
                  <n-space>
                    <n-tag type="success">{{ car.brand }}</n-tag>
                    <n-tag type="info">{{ car.type }}</n-tag>
                  </n-space>
                </template>
                <n-space vertical size="small">
                  <n-text>价格: {{ car.price }} 万元</n-text>
                  <n-text>续航: {{ car.range }} km</n-text>
                  <n-text>{{ car.description }}</n-text>
                </n-space>
              </n-thing>
              <template #suffix>
                <n-button type="primary" @click="handleViewDetail(car)">
                  查看详情
                </n-button>
              </template>
            </n-list-item>
          </n-list>

          <!-- 分页 -->
          <n-pagination
            v-model:page="currentPage"
            :page-count="totalPages"
            style="margin-top: 16px; justify-content: center;"
            @update:page="handlePageChange"
          />
        </n-spin>
      </n-card>
    </n-space>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMessage } from 'naive-ui'
import { getCarList } from '@/api/car'
import type { Car } from '@/types/car'

const message = useMessage()
const loading = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)

// 表单数据
const formValue = ref({
  priceRange: null,
  range: null,
  carType: null
})

// 车辆列表
const carList = ref<Car[]>([])

// 筛选选项
const priceRangeOptions = [
  { label: '10万以下', value: '0-10' },
  { label: '10-20万', value: '10-20' },
  { label: '20-30万', value: '20-30' },
  { label: '30-50万', value: '30-50' },
  { label: '50万以上', value: '50-999' }
]

const rangeOptions = [
  { label: '300km以下', value: '0-300' },
  { label: '300-500km', value: '300-500' },
  { label: '500-700km', value: '500-700' },
  { label: '700km以上', value: '700-9999' }
]

const carTypeOptions = [
  { label: '轿车', value: 'sedan' },
  { label: 'SUV', value: 'suv' },
  { label: 'MPV', value: 'mpv' },
  { label: '跑车', value: 'sports' }
]

// 搜索
const handleSearch = async () => {
  currentPage.value = 1
  await loadCarList()
}

// 重置
const handleReset = () => {
  formValue.value = {
    priceRange: null,
    range: null,
    carType: null
  }
  handleSearch()
}

// 加载车辆列表
const loadCarList = async () => {
  loading.value = true
  try {
    const response = await getCarList({
      page: currentPage.value,
      pageSize: 10,
      ...formValue.value
    })
    carList.value = response.data
    totalPages.value = response.totalPages
  } catch (error) {
    console.error('加载车辆列表失败:', error)
    message.error('加载车辆列表失败')
    // 使用模拟数据
    carList.value = [
      {
        id: 1,
        name: '比亚迪海豹',
        brand: '比亚迪',
        type: '轿车',
        price: 21.28,
        range: 700,
        image: '',
        description: '性能强劲的纯电轿车，搭载CTB电池车身一体化技术'
      },
      {
        id: 2,
        name: '特斯拉 Model 3',
        brand: '特斯拉',
        type: '轿车',
        price: 26.14,
        range: 606,
        image: '',
        description: '全球热销的纯电轿车，智能驾驶辅助系统领先'
      }
    ]
    totalPages.value = 1
  } finally {
    loading.value = false
  }
}

// 翻页
const handlePageChange = (page: number) => {
  currentPage.value = page
  loadCarList()
}

// 查看详情
const handleViewDetail = (car: Car) => {
  message.info(`查看 ${car.name} 的详情`)
  // TODO: 跳转到详情页
}

onMounted(() => {
  loadCarList()
})
</script>

<style scoped>
.select-car-container {
  max-width: 1200px;
  margin: 0 auto;
}
</style>
