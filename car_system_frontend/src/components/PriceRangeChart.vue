<template>
  <div ref="chartRef" :style="{ width: '100%', height: height }"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import type { PriceRangeItem } from '@/api/analysis'

interface Props {
  data: PriceRangeItem[]
  height?: string
  title?: string
}

const props = withDefaults(defineProps<Props>(), {
  height: '400px',
  title: '价格范围数量分布'
})

const chartRef = ref<HTMLElement>()
let chartInstance: echarts.ECharts | null = null

// 初始化图表
const initChart = () => {
  if (!chartRef.value) return
  
  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

// 更新图表数据
const updateChart = () => {
  if (!chartInstance) return
  
  const ranges = props.data.map(item => item.range)
  const counts = props.data.map(item => item.count)
  
  const option: echarts.EChartsOption = {
    title: {
      text: props.title,
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: (params: any) => {
        const item = params[0]
        return `${item.name}<br/>车系数量: ${item.value}款`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ranges,
      axisLabel: {
        interval: 0,
        rotate: 30,
        fontSize: 12
      }
    },
    yAxis: {
      type: 'value',
      name: '车系数量(款)',
      axisLabel: {
        formatter: '{value}'
      }
    },
    series: [
      {
        name: '车系数量',
        type: 'bar',
        data: counts,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#fccb05' },
            { offset: 0.5, color: '#f5804d' },
            { offset: 1, color: '#f54a45' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#f54a45' },
              { offset: 0.7, color: '#f5804d' },
              { offset: 1, color: '#fccb05' }
            ])
          }
        },
        label: {
          show: true,
          position: 'top',
          formatter: '{c}款',
          fontSize: 11
        },
        barWidth: '50%'
      }
    ]
  }
  
  chartInstance.setOption(option)
}

// 监听数据变化
watch(() => props.data, () => {
  updateChart()
}, { deep: true })

// 窗口大小改变时重新调整图表大小
const handleResize = () => {
  chartInstance?.resize()
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>
