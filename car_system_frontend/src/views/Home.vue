<template>
  <div class="car-detail-page">
    <!-- 顶部车系选择 -->
    <div class="car-selector">
      <n-select
        v-model:value="selectedCarId"
        :options="carOptions"
        placeholder="选择车系"
        filterable
        style="width: 300px"
        @update:value="loadCarDetail"
      />
    </div>

    <n-spin :show="loading">
      <div v-if="carData" class="detail-content">
        <!-- 第一行：基本信息 + 雷达图 + 车辆图片和参数 -->
        <div class="top-section">
          <!-- 左侧：价格和评分 -->
          <div class="left-panel">
            <!-- 车系标题 -->
            <div class="car-title">
              <span class="brand-logo" v-if="carData.basic_info.brand_logo">
                <img :src="carData.basic_info.brand_logo" alt="logo" />
              </span>
              <span class="brand-icon" v-else>T</span>
              <h1>{{ carData.basic_info.name }}</h1>
              <span class="sub-info">{{ carData.basic_info.brand_name }}/{{ carData.basic_info.body_type || '中型SUV' }}</span>
            </div>

            <!-- 价格信息 -->
            <div class="price-info">
              <div class="price-row">
                <span class="label">经销商报价</span>
                <span class="price">{{ formatPrice(carData.basic_info.price_min) }}-{{ formatPrice(carData.basic_info.price_max) }}万</span>
              </div>
              <div class="price-row">
                <span class="label">厂商指导价</span>
                <span class="guide-price">{{ formatPrice(carData.basic_info.price_min) }}-{{ formatPrice(carData.basic_info.price_max) }}万</span>
              </div>
              <div class="rank-row">
                <span class="label">近一年销量排名</span>
                <span class="rank">{{ carData.rankings.sales_rank_year }}</span>
              </div>
              <div class="rank-row">
                <span class="label">近一年投诉排名</span>
                <span class="rank">{{ carData.rankings.issue_rank_year }}</span>
              </div>
            </div>

            <!-- 雷达图 -->
            <div class="radar-chart">
              <div id="radar-chart" style="width: 100%; height: 280px;"></div>
            </div>
          </div>

          <!-- 中间：车辆图片 -->
          <div class="center-panel">
            <div class="car-image">
              <img :src="currentCarImage" alt="车辆图片" referrerpolicy="no-referrer" @error="handleImageError" />
            </div>

            <!-- 版本选择 -->
            <div class="version-selector">
              <n-radio-group v-model:value="selectedVersionId" name="version">
                <n-space>
                  <n-radio
                    v-for="version in carData.versions"
                    :key="version.id"
                    :value="version.id"
                  >
                    {{ version.year }}款 {{ version.name }}
                  </n-radio>
                </n-space>
              </n-radio-group>
            </div>

            <!-- 颜色选择 -->
            <div class="color-selector">
              <div
                v-for="color in carData.colors"
                :key="color.id"
                class="color-circle"
                :class="{ active: selectedColorId === color.id }"
                :style="{ backgroundColor: color.color_code }"
                @click="selectedColorId = color.id"
                :title="color.name"
              ></div>
              <span class="color-name">{{ currentColorName }}</span>
            </div>
          </div>

          <!-- 右侧：车辆参数 -->
          <div class="right-panel">
            <div class="params-list">
              <div class="param-item">
                <span class="param-label">百公里加速时间:</span>
                <span class="param-value">{{ carData.params.acceleration }}s</span>
              </div>
              <div class="param-item">
                <span class="param-label">空调控制方式:</span>
                <span class="param-value">--</span>
              </div>
              <div class="param-item">
                <span class="param-label">行李箱容积:</span>
                <span class="param-value">--</span>
              </div>
              <div class="param-item">
                <span class="param-label">车身结构:</span>
                <span class="param-value">{{ carData.basic_info.body_type || 'SUV' }}</span>
              </div>
              <div class="param-item">
                <span class="param-label">整备质量:</span>
                <span class="param-value">{{ carData.params.curb_weight }}Kg</span>
              </div>
              <div class="param-item">
                <span class="param-label">驱动形式:</span>
                <span class="param-value">{{ carData.params.drive_type }}</span>
              </div>
              <div class="param-item">
                <span class="param-label">发动机描述:</span>
                <span class="param-value">{{ carData.basic_info.fuel_type_display }}</span>
              </div>
              <div class="param-item">
                <span class="param-label">续航里程:</span>
                <span class="param-value">{{ carData.basic_info.endurance_min }}-{{ carData.basic_info.endurance_max }}km</span>
              </div>
              <div class="param-item">
                <span class="param-label">燃料形式:</span>
                <span class="param-value">{{ carData.basic_info.fuel_type_display }}</span>
              </div>
              <div class="param-item">
                <span class="param-label">最高车速:</span>
                <span class="param-value">{{ carData.params.max_speed }}Km/h</span>
              </div>
              <div class="param-item">
                <span class="param-label">座位数:</span>
                <span class="param-value">{{ carData.params.seat_count }}座</span>
              </div>
              <div class="param-item">
                <span class="param-label">轴距:</span>
                <span class="param-value">{{ carData.params.wheelbase }}mm</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 投诉问题标签 -->
        <div class="issue-tags-section">
          <div class="tags-container">
            <n-tag
              v-for="(tag, index) in carData.issue_tags"
              :key="index"
              :type="getTagType(tag.category)"
              size="medium"
              class="issue-tag"
            >
              {{ tag.name }} {{ tag.count }}
            </n-tag>
          </div>
        </div>

        <!-- 词云图和趋势图 -->
        <div class="charts-section">
          <!-- 词云图 -->
          <n-card title="质量问题词云图" :bordered="false" class="chart-card">
            <div id="wordcloud-chart" style="width: 100%; height: 300px;"></div>
          </n-card>
        </div>

        <!-- 时间轴 -->
        <div class="timeline-section">
          <div id="timeline-chart" style="width: 100%; height: 80px;"></div>
        </div>

        <!-- 趋势图 -->
        <div class="trend-section">
          <n-card title="投诉趋势分析" :bordered="false">
            <div id="trend-chart" style="width: 100%; height: 350px;"></div>
          </n-card>
        </div>
      </div>

      <div v-else class="no-data">
        <n-empty description="暂无车系数据" />
      </div>
    </n-spin>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
import { NSelect, NSpin, NCard, NTag, NRadioGroup, NRadio, NSpace, NEmpty } from 'naive-ui'
import * as echarts from 'echarts'
import 'echarts-wordcloud'
import type { ECharts } from 'echarts'
import { getCarDetailFull, getCarListSimple, type CarDetailData } from '@/api/django-car'

const loading = ref(false)
const carData = ref<CarDetailData | null>(null)
const carOptions = ref<Array<{ label: string; value: number }>>([])
const selectedCarId = ref<number | null>(null)
const selectedVersionId = ref<number>(1)
const selectedColorId = ref<number>(1)

// 图表实例
let radarChart: ECharts | null = null
let wordcloudChart: ECharts | null = null
let timelineChart: ECharts | null = null
let trendChart: ECharts | null = null

// 生成SVG占位图的Data URL
const createPlaceholderSvg = (text: string, bgColor: string = '#f0f0f0', textColor: string = '#666') => {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
    <rect width="600" height="400" fill="${bgColor}"/>
    <text x="300" y="200" font-family="Arial, sans-serif" font-size="32" font-weight="bold" fill="${textColor}" text-anchor="middle" dominant-baseline="middle">${text}</text>
  </svg>`
  return `data:image/svg+xml,${encodeURIComponent(svg)}`
}

// 默认车辆图片
const defaultCarImage = createPlaceholderSvg('车辆图片', '#f5f5f5', '#999')

// 品牌图片映射 - 使用彩色SVG占位图
const brandColors: Record<string, { bg: string; text: string }> = {
  '特斯拉': { bg: '#cc0000', text: '#fff' },
  '蔚来': { bg: '#003366', text: '#fff' },
  '比亚迪': { bg: '#1a73e8', text: '#fff' },
  '小鹏': { bg: '#ff6600', text: '#fff' },
  '理想': { bg: '#00b4ff', text: '#fff' },
  '广汽埃安': { bg: '#0066cc', text: '#fff' },
  '零跑': { bg: '#ff3366', text: '#fff' },
  '哪吒': { bg: '#6633cc', text: '#fff' },
  '极氪': { bg: '#333333', text: '#fff' },
  '问界': { bg: '#009966', text: '#fff' },
}

// 当前选中的颜色名称
const currentColorName = computed(() => {
  if (!carData.value) return ''
  const color = carData.value.colors.find(c => c.id === selectedColorId.value)
  return color?.name || ''
})

// 当前车辆图片
const currentCarImage = computed(() => {
  if (!carData.value) return defaultCarImage
  // 优先使用颜色图片，其次使用车系图片
  const color = carData.value.colors.find(c => c.id === selectedColorId.value)
  if (color?.image) return color.image
  
  // 检查车系图片是否为有效URL（排除无法访问的外部API）
  const seriesImage = carData.value.basic_info.image
  if (seriesImage && !seriesImage.includes('api.nio.com') && !seriesImage.includes('api.xpeng.com')) {
    return seriesImage
  }
  
  // 使用品牌彩色占位图
  const brandName = carData.value.basic_info.brand_name
  const carName = carData.value.basic_info.name
  const colors = brandColors[brandName] || { bg: '#667788', text: '#fff' }
  return createPlaceholderSvg(`${brandName} ${carName}`, colors.bg, colors.text)
})

// 格式化价格
const formatPrice = (price: number | null) => {
  if (!price) return '--'
  return price.toFixed(2)
}

// 获取标签类型
const getTagType = (category: string) => {
  switch (category) {
    case 'quality': return 'error'
    case 'service': return 'warning'
    default: return 'info'
  }
}

// 图片加载错误处理
const handleImageError = (e: Event) => {
  const img = e.target as HTMLImageElement
  img.src = defaultCarImage
}

// 加载车系列表
const loadCarList = async () => {
  try {
    const res = await getCarListSimple()
    if (res.data) {
      carOptions.value = res.data.map(item => ({
        label: item.name,
        value: item.id
      }))
      if (carOptions.value.length > 0 && !selectedCarId.value) {
        selectedCarId.value = carOptions.value[0].value
      }
    }
  } catch (error) {
    console.error('加载车系列表失败:', error)
  }
}

// 加载车系详情
const loadCarDetail = async (id?: number) => {
  loading.value = true
  try {
    const res = await getCarDetailFull(id || selectedCarId.value || undefined)
    if (res.data) {
      carData.value = res.data
      // 设置默认选中
      const defaultVersion = res.data.versions.find(v => v.is_default)
      if (defaultVersion) selectedVersionId.value = defaultVersion.id
      const defaultColor = res.data.colors.find(c => c.is_default)
      if (defaultColor) selectedColorId.value = defaultColor.id

      // 渲染图表
      await nextTick()
      renderRadarChart()
      renderWordcloudChart()
      renderTimelineChart()
      renderTrendChart()
    }
  } catch (error) {
    console.error('加载车系详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 渲染雷达图
const renderRadarChart = () => {
  if (!carData.value) return
  const chartDom = document.getElementById('radar-chart')
  if (!chartDom) return

  if (radarChart) radarChart.dispose()
  radarChart = echarts.init(chartDom)

  const scores = carData.value.scores
  const option = {
    radar: {
      indicator: [
        { name: '舒适性', max: 5 },
        { name: '外观', max: 5 },
        { name: '动力', max: 5 },
        { name: '空间', max: 5 },
        { name: '内饰', max: 5 },
        { name: '配置', max: 5 }
      ],
      center: ['50%', '55%'],
      radius: '65%'
    },
    series: [{
      type: 'radar',
      data: [{
        value: [scores.comfort, scores.appearance, scores.power, scores.space, scores.interior, scores.config],
        name: '评分',
        areaStyle: { color: 'rgba(255, 215, 0, 0.6)' },
        lineStyle: { color: '#FFD700' },
        itemStyle: { color: '#333' }
      }]
    }],
    graphic: [{
      type: 'text',
      left: 'center',
      top: '45%',
      style: {
        text: scores.total.toFixed(2),
        fontSize: 28,
        fontWeight: 'bold',
        fill: '#333'
      }
    }]
  }
  radarChart.setOption(option)
}

// 渲染词云图
const renderWordcloudChart = () => {
  if (!carData.value) return
  const chartDom = document.getElementById('wordcloud-chart')
  if (!chartDom) return

  if (wordcloudChart) wordcloudChart.dispose()
  wordcloudChart = echarts.init(chartDom)

  const option = {
    series: [{
      type: 'wordCloud',
      gridSize: 8,
      sizeRange: [14, 50],
      rotationRange: [-45, 45],
      shape: 'circle',
      textStyle: {
        fontFamily: 'sans-serif',
        fontWeight: 'bold',
        color: function () {
          return 'rgb(' + [
            Math.round(Math.random() * 160),
            Math.round(Math.random() * 160),
            Math.round(Math.random() * 160)
          ].join(',') + ')'
        }
      },
      data: carData.value.word_cloud.map(item => ({
        name: item.name,
        value: item.value
      }))
    }]
  }
  wordcloudChart.setOption(option)
}

// 渲染时间轴
const renderTimelineChart = () => {
  if (!carData.value) return
  const chartDom = document.getElementById('timeline-chart')
  if (!chartDom) return

  if (timelineChart) timelineChart.dispose()
  timelineChart = echarts.init(chartDom)

  const months = carData.value.issue_trend.map(item => item.month)
  const option = {
    xAxis: {
      type: 'category',
      data: months,
      axisLine: { lineStyle: { color: '#ccc' } },
      axisTick: { show: false }
    },
    yAxis: { show: false },
    grid: { left: 50, right: 50, top: 20, bottom: 30 },
    series: [{
      type: 'scatter',
      symbolSize: 12,
      data: months.map(() => 0),
      itemStyle: { color: '#1890ff' }
    }]
  }
  timelineChart.setOption(option)
}

// 渲染趋势图
const renderTrendChart = () => {
  if (!carData.value) return
  const chartDom = document.getElementById('trend-chart')
  if (!chartDom) return

  if (trendChart) trendChart.dispose()
  trendChart = echarts.init(chartDom)

  const trend = carData.value.issue_trend
  const option = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['质量问题', '服务问题', '其他问题'], top: 10 },
    grid: { left: 60, right: 30, top: 60, bottom: 30 },
    xAxis: { type: 'category', data: trend.map(item => item.month) },
    yAxis: { type: 'value', name: '投诉量' },
    series: [
      {
        name: '质量问题',
        type: 'line',
        smooth: true,
        areaStyle: { opacity: 0.3 },
        data: trend.map(item => item.quality)
      },
      {
        name: '服务问题',
        type: 'line',
        smooth: true,
        areaStyle: { opacity: 0.3 },
        data: trend.map(item => item.service)
      },
      {
        name: '其他问题',
        type: 'line',
        smooth: true,
        areaStyle: { opacity: 0.3 },
        data: trend.map(item => item.other)
      }
    ]
  }
  trendChart.setOption(option)
}

// 窗口大小变化时重新渲染
const handleResize = () => {
  radarChart?.resize()
  wordcloudChart?.resize()
  timelineChart?.resize()
  trendChart?.resize()
}

onMounted(async () => {
  await loadCarList()
  await loadCarDetail()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  radarChart?.dispose()
  wordcloudChart?.dispose()
  timelineChart?.dispose()
  trendChart?.dispose()
})
</script>

<style scoped>
.car-detail-page {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.car-selector {
  margin-bottom: 20px;
}

.detail-content {
  background: #fff;
}

.top-section {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.left-panel {
  width: 320px;
  flex-shrink: 0;
}

.car-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.car-title h1 {
  font-size: 24px;
  margin: 0;
}

.car-title .sub-info {
  color: #666;
  font-size: 14px;
}

.brand-icon {
  width: 30px;
  height: 30px;
  background: #e74c3c;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  border-radius: 4px;
}

.brand-logo img {
  width: 30px;
  height: 30px;
}

.price-info {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.price-row, .rank-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.price-row .label, .rank-row .label {
  color: #666;
  font-size: 13px;
}

.price-row .price {
  color: #e74c3c;
  font-size: 18px;
  font-weight: bold;
}

.price-row .guide-price {
  font-size: 14px;
}

.rank-row .rank {
  font-weight: bold;
}

.center-panel {
  flex: 1;
  text-align: center;
}

.car-image {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
}

.car-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.version-selector {
  margin: 15px 0;
  text-align: left;
}

.color-selector {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-top: 10px;
}

.color-circle {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.2s;
}

.color-circle:hover {
  transform: scale(1.1);
}

.color-circle.active {
  border-color: #1890ff;
  box-shadow: 0 0 5px rgba(24, 144, 255, 0.5);
}

.color-name {
  color: #666;
  font-size: 13px;
}

.right-panel {
  width: 280px;
  flex-shrink: 0;
}

.params-list {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
}

.param-item {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px dashed #eee;
  font-size: 13px;
}

.param-item:last-child {
  border-bottom: none;
}

.param-label {
  color: #666;
}

.param-value {
  color: #333;
  font-weight: 500;
}

.issue-tags-section {
  margin: 20px 0;
  padding: 15px;
  background: #fff;
  border-radius: 8px;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.issue-tag {
  cursor: pointer;
}

.charts-section {
  margin: 20px 0;
}

.chart-card {
  margin-bottom: 20px;
}

.timeline-section {
  margin: 20px 0;
  padding: 10px;
  background: #f9f9f9;
  border-radius: 8px;
}

.trend-section {
  margin: 20px 0;
}

.no-data {
  padding: 100px 0;
  text-align: center;
}
</style>
