<template>
  <div class="analysis-page">
    <!-- 车系降价排行榜 - 横向条形图 -->
    <n-card title="📉 车系价格区间排行榜" :bordered="false" class="chart-card">
      <n-spin :show="discountLoading">
        <div id="discount-bar" class="chart-container"></div>
      </n-spin>
    </n-card>

    <div class="charts-row">
      <!-- 汽车品牌数量TOP分布图 - 环形图 -->
      <n-card title="🏆 汽车品牌车系TOP分布" :bordered="false" class="chart-card half-width">
        <n-spin :show="brandLoading">
          <div id="brand-pie" class="chart-container"></div>
        </n-spin>
      </n-card>

      <!-- 价格范围数量分布图 - 柱状图 -->
      <n-card title="💰 价格范围数量分布" :bordered="false" class="chart-card half-width">
        <n-spin :show="priceLoading">
          <div id="price-bar" class="chart-container"></div>
        </n-spin>
      </n-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { NCard, NSpin } from 'naive-ui'
import * as echarts from 'echarts'
import type { ECharts } from 'echarts'
import {
  getPriceDiscountRanking,
  getBrandCountDistribution,
  getPriceRangeDistribution,
  type PriceDiscountItem,
  type BrandCountItem,
  type PriceRangeItem
} from '@/api/django-car'

// 加载状态
const discountLoading = ref(false)
const brandLoading = ref(false)
const priceLoading = ref(false)

// 图表实例
let discountChart: ECharts | null = null
let brandChart: ECharts | null = null
let priceChart: ECharts | null = null

// 加载降价排行榜图表
const loadDiscountChart = async () => {
  discountLoading.value = true
  try {
    const res = await getPriceDiscountRanking(15)
    const data: PriceDiscountItem[] = res.data || []
    
    const chartDom = document.getElementById('discount-bar')
    if (chartDom) {
      discountChart = echarts.init(chartDom)
      
      // 反转数据顺序，让最大的在上面
      const reversedData = [...data].reverse()
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' },
          formatter: (params: any) => {
            const item = params[0]
            const dataIndex = reversedData.length - 1 - item.dataIndex
            const original = data[dataIndex]
            return `<strong>${item.name}</strong><br/>
                    价格区间: ${original?.price_min || 0} - ${original?.price_max || 0} 万<br/>
                    区间差价: <span style="color:#ee6666;font-weight:bold">${item.value} 万</span>`
          }
        },
        grid: {
          left: '3%',
          right: '8%',
          bottom: '3%',
          top: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: '价格区间(万元)',
          axisLabel: {
            formatter: '{value}'
          }
        },
        yAxis: {
          type: 'category',
          data: reversedData.map(item => item.series_name),
          axisLabel: {
            width: 120,
            overflow: 'truncate'
          }
        },
        series: [
          {
            name: '价格区间',
            type: 'bar',
            data: reversedData.map(item => item.discount),
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                { offset: 0, color: '#5470c6' },
                { offset: 1, color: '#91cc75' }
              ]),
              borderRadius: [0, 4, 4, 0]
            },
            label: {
              show: true,
              position: 'right',
              formatter: '{c} 万'
            }
          }
        ]
      }
      
      discountChart.setOption(option)
    }
  } catch (error) {
    console.error('加载降价排行榜失败:', error)
  } finally {
    discountLoading.value = false
  }
}

// 加载品牌数量分布图表
const loadBrandChart = async () => {
  brandLoading.value = true
  try {
    const res = await getBrandCountDistribution(10)
    const data: BrandCountItem[] = res.data || []
    
    const chartDom = document.getElementById('brand-pie')
    if (chartDom) {
      brandChart = echarts.init(chartDom)
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c} 个车系 ({d}%)'
        },
        legend: {
          type: 'scroll',
          orient: 'vertical',
          right: '5%',
          top: 'center',
          formatter: (name: string) => {
            const item = data.find(d => d.brand_name === name)
            return `${name}: ${item?.count || 0}`
          }
        },
        series: [
          {
            name: '品牌车系数量',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['35%', '50%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 20,
                fontWeight: 'bold',
                formatter: '{b}\n{c} 个'
              }
            },
            labelLine: {
              show: false
            },
            data: data.map(item => ({
              value: item.count,
              name: item.brand_name
            }))
          }
        ]
      }
      
      brandChart.setOption(option)
    }
  } catch (error) {
    console.error('加载品牌分布图失败:', error)
  } finally {
    brandLoading.value = false
  }
}

// 加载价格区间分布图表
const loadPriceChart = async () => {
  priceLoading.value = true
  try {
    const res = await getPriceRangeDistribution()
    const data: PriceRangeItem[] = res.data || []
    
    const chartDom = document.getElementById('price-bar')
    if (chartDom) {
      priceChart = echarts.init(chartDom)
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'shadow' },
          formatter: (params: any) => {
            const item = params[0]
            return `<strong>${item.name}</strong><br/>车系数量: <span style="color:#5470c6;font-weight:bold">${item.value}</span> 个`
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '10%',
          top: '10%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: data.map(item => item.range),
          axisLabel: {
            rotate: 30
          }
        },
        yAxis: {
          type: 'value',
          name: '车系数量'
        },
        series: [
          {
            name: '车系数量',
            type: 'bar',
            data: data.map(item => item.count),
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#5470c6' },
                { offset: 1, color: '#91cc75' }
              ]),
              borderRadius: [4, 4, 0, 0]
            },
            label: {
              show: true,
              position: 'top',
              formatter: '{c}'
            }
          }
        ]
      }
      
      priceChart.setOption(option)
    }
  } catch (error) {
    console.error('加载价格分布图失败:', error)
  } finally {
    priceLoading.value = false
  }
}

// 处理窗口大小改变
const handleResize = () => {
  discountChart?.resize()
  brandChart?.resize()
  priceChart?.resize()
}

// 组件挂载时加载所有图表
onMounted(() => {
  loadDiscountChart()
  loadBrandChart()
  loadPriceChart()
  window.addEventListener('resize', handleResize)
})

// 组件卸载时清理
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  discountChart?.dispose()
  brandChart?.dispose()
  priceChart?.dispose()
})
</script>

<style scoped>
.analysis-page {
  padding: 20px;
}

.chart-card {
  margin-bottom: 20px;
}

.chart-container {
  width: 100%;
  height: 450px;
}

.charts-row {
  display: flex;
  gap: 20px;
}

.half-width {
  flex: 1;
}

@media (max-width: 1200px) {
  .charts-row {
    flex-direction: column;
  }
  
  .half-width {
    width: 100%;
  }
}
</style>
