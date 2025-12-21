<template>
  <div class="car-detail-page">
    <n-spin :show="loading" size="large">
      <!-- 返回按钮 -->
      <div class="back-bar">
        <n-button text @click="goBack">
          <template #icon><n-icon><ArrowBack /></n-icon></template>
          返回选车
        </n-button>
      </div>

      <template v-if="carData">
        <n-grid :cols="24" :x-gap="24">
          <!-- 左侧图片区 -->
          <n-gi :span="10">
            <n-card :bordered="false" class="image-card">
              <div class="main-image">
                <img 
                  :src="currentImage" 
                  :alt="carData.basic_info.name"
                  referrerpolicy="no-referrer"
                  @error="handleImageError"
                />
              </div>
              <!-- 颜色选择 -->
              <div class="color-selector" v-if="carData.colors && carData.colors.length > 0">
                <span class="color-label">车身颜色：</span>
                <div class="color-options">
                  <div
                    v-for="color in carData.colors"
                    :key="color.id"
                    class="color-item"
                    :class="{ active: selectedColorId === color.id }"
                    :style="{ backgroundColor: color.color_code }"
                    :title="color.name"
                    @click="selectedColorId = color.id"
                  />
                </div>
                <span class="color-name">{{ currentColorName }}</span>
              </div>
            </n-card>
          </n-gi>

          <!-- 右侧信息区 -->
          <n-gi :span="14">
            <n-card :bordered="false" class="info-card">
              <!-- 标题和价格 -->
              <div class="car-header">
                <div class="brand-info">
                  <n-tag :type="getFuelTypeColor(carData.basic_info.fuel_type)" size="small">
                    {{ carData.basic_info.fuel_type_display }}
                  </n-tag>
                  <span class="brand-name">{{ carData.basic_info.brand_name }}</span>
                </div>
                <h1 class="car-name">{{ carData.basic_info.name }}</h1>
                <div class="price-row">
                  <span class="price-value">{{ formatPrice }}</span>
                  <span class="price-unit">万元</span>
                </div>
              </div>

              <!-- 核心参数 -->
              <div class="core-params">
                <div class="param-item">
                  <div class="param-value">{{ carData.basic_info.endurance_max || '--' }}</div>
                  <div class="param-label">续航里程(km)</div>
                </div>
                <div class="param-item">
                  <div class="param-value">{{ carData.params.acceleration || '--' }}</div>
                  <div class="param-label">百公里加速(s)</div>
                </div>
                <div class="param-item">
                  <div class="param-value">{{ carData.params.max_speed || '--' }}</div>
                  <div class="param-label">最高时速(km/h)</div>
                </div>
                <div class="param-item">
                  <div class="param-value">{{ carData.params.seat_count || 5 }}</div>
                  <div class="param-label">座位数</div>
                </div>
              </div>

              <!-- 车型标签 -->
              <div class="car-tags">
                <n-tag v-if="carData.basic_info.body_type" size="medium" :bordered="false" type="info">
                  {{ carData.basic_info.body_type }}
                </n-tag>
                <n-tag v-if="carData.params.drive_type" size="medium" :bordered="false" type="success">
                  {{ carData.params.drive_type }}
                </n-tag>
                <n-tag size="medium" :bordered="false" type="warning">
                  轴距 {{ carData.params.wheelbase }}mm
                </n-tag>
              </div>

              <!-- 评分展示 -->
              <div class="scores-section">
                <h3>用户评分</h3>
                <div class="score-grid">
                  <div class="score-item" v-for="(value, key) in scoreLabels" :key="key">
                    <span class="score-label">{{ value }}</span>
                    <n-progress
                      type="line"
                      :percentage="(carData.scores[key] / 5) * 100"
                      :height="8"
                      :show-indicator="false"
                      status="success"
                    />
                    <span class="score-value">{{ carData.scores[key] }}</span>
                  </div>
                </div>
                <div class="total-score">
                  综合评分：<strong>{{ carData.scores.total }}</strong> 分
                </div>
              </div>
            </n-card>
          </n-gi>
        </n-grid>

        <!-- 车型版本 -->
        <n-card title="在售车型" :bordered="false" style="margin-top: 20px">
          <n-data-table
            :columns="versionColumns"
            :data="carData.versions"
            :bordered="false"
            striped
          />
        </n-card>

        <!-- 质量问题统计 -->
        <n-card title="用户反馈热点" :bordered="false" style="margin-top: 20px">
          <div class="issue-tags">
            <n-tag
              v-for="(tag, index) in carData.issue_tags.slice(0, 10)"
              :key="index"
              :type="getIssueTagType(tag.category)"
              size="large"
              round
            >
              {{ tag.name }} ({{ tag.count }})
            </n-tag>
          </div>
        </n-card>
      </template>

      <n-empty v-else-if="!loading" description="未找到该车型信息" />
    </n-spin>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, h } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  NCard, NGrid, NGi, NTag, NButton, NIcon, NProgress,
  NDataTable, NEmpty, NSpin, NSpace
} from 'naive-ui'
import { ArrowBack } from '@vicons/ionicons5'
import type { DataTableColumns } from 'naive-ui'
import { getCarDetailFull, type CarDetailData } from '@/api/django-car'

const route = useRoute()
const router = useRouter()

const loading = ref(true)
const carData = ref<CarDetailData | null>(null)
const selectedColorId = ref<number | null>(null)

// 评分标签
const scoreLabels: Record<string, string> = {
  comfort: '舒适性',
  appearance: '外观',
  power: '动力',
  interior: '内饰',
  config: '配置',
  space: '空间'
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

// 获取问题标签类型
const getIssueTagType = (category: string) => {
  const types: Record<string, 'error' | 'warning' | 'info'> = {
    'quality': 'error',
    'service': 'warning',
    'other': 'info'
  }
  return types[category] || 'default'
}

// 格式化价格
const formatPrice = computed(() => {
  if (!carData.value) return '--'
  const { price_min, price_max } = carData.value.basic_info
  if (price_min && price_max) {
    return price_min === price_max ? price_min.toFixed(2) : `${price_min.toFixed(2)}-${price_max.toFixed(2)}`
  }
  return price_min?.toFixed(2) || price_max?.toFixed(2) || '--'
})

// 当前颜色名称
const currentColorName = computed(() => {
  if (!carData.value?.colors) return ''
  const color = carData.value.colors.find(c => c.id === selectedColorId.value)
  return color?.name || ''
})

// 当前图片
const currentImage = computed(() => {
  if (!carData.value) return ''
  
  // 尝试使用颜色对应的图片
  const color = carData.value.colors?.find(c => c.id === selectedColorId.value)
  if (color?.image) return color.image
  
  // 使用车系图片
  return carData.value.basic_info.image || createPlaceholderSvg(
    `${carData.value.basic_info.brand_name} ${carData.value.basic_info.name}`
  )
})

// 生成占位图
const createPlaceholderSvg = (text: string) => {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
    <rect width="600" height="400" fill="#e8f4ff"/>
    <text x="300" y="200" font-family="Arial" font-size="24" fill="#1a73e8" text-anchor="middle" dominant-baseline="middle">${text}</text>
  </svg>`
  return `data:image/svg+xml,${encodeURIComponent(svg)}`
}

// 图片加载失败处理
const handleImageError = (e: Event) => {
  const img = e.target as HTMLImageElement
  if (carData.value) {
    img.src = createPlaceholderSvg(`${carData.value.basic_info.brand_name} ${carData.value.basic_info.name}`)
  }
}

// 版本表格列
const versionColumns: DataTableColumns = [
  { title: '车型名称', key: 'name', ellipsis: { tooltip: true } },
  { title: '年款', key: 'year', width: 80 },
  { 
    title: '指导价(万)', 
    key: 'price', 
    width: 120,
    render: (row: any) => row.price?.toFixed(2) || '--'
  },
  { 
    title: '续航(km)', 
    key: 'endurance', 
    width: 100,
    render: (row: any) => row.endurance || '--'
  },
  {
    title: '状态',
    key: 'is_default',
    width: 80,
    render: (row: any) => row.is_default ? h(NTag, { type: 'success', size: 'small' }, { default: () => '热销' }) : ''
  }
]

// 返回上一页
const goBack = () => {
  router.push('/django/select-car')
}

// 加载数据
const loadCarDetail = async () => {
  loading.value = true
  try {
    const carId = Number(route.params.id || route.query.id)
    const response = await getCarDetailFull(carId || undefined)
    
    if (response.code === 200 && response.data) {
      carData.value = response.data
      // 设置默认选中颜色
      const defaultColor = response.data.colors?.find(c => c.is_default) || response.data.colors?.[0]
      if (defaultColor) {
        selectedColorId.value = defaultColor.id
      }
    }
  } catch (error) {
    console.error('加载车型详情失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadCarDetail()
})
</script>

<style scoped>
.car-detail-page {
  padding: 20px;
  background: #f5f5f5;
  min-height: 100vh;
}

.back-bar {
  margin-bottom: 16px;
}

.image-card {
  position: sticky;
  top: 20px;
}

.main-image {
  width: 100%;
  height: 300px;
  background: #f8f8f8;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.color-selector {
  margin-top: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.color-label {
  font-size: 14px;
  color: #666;
}

.color-options {
  display: flex;
  gap: 8px;
}

.color-item {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s;
}

.color-item:hover {
  transform: scale(1.1);
}

.color-item.active {
  border-color: #1a73e8;
  box-shadow: 0 0 0 2px rgba(26, 115, 232, 0.3);
}

.color-name {
  font-size: 14px;
  color: #333;
}

.info-card {
  height: 100%;
}

.car-header {
  margin-bottom: 24px;
}

.brand-info {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.brand-name {
  font-size: 14px;
  color: #666;
}

.car-name {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin: 0 0 12px 0;
}

.price-row {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.price-value {
  font-size: 32px;
  font-weight: 700;
  color: #e74c3c;
}

.price-unit {
  font-size: 14px;
  color: #999;
}

.core-params {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 20px;
}

.param-item {
  text-align: center;
}

.param-value {
  font-size: 24px;
  font-weight: 700;
  color: #333;
}

.param-label {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.car-tags {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
}

.scores-section h3 {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 16px 0;
  color: #333;
}

.score-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.score-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.score-label {
  width: 50px;
  font-size: 13px;
  color: #666;
}

.score-item .n-progress {
  flex: 1;
}

.score-value {
  width: 30px;
  text-align: right;
  font-weight: 600;
  color: #333;
}

.total-score {
  margin-top: 16px;
  text-align: right;
  font-size: 14px;
  color: #666;
}

.total-score strong {
  font-size: 20px;
  color: #1a73e8;
}

.issue-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
</style>
