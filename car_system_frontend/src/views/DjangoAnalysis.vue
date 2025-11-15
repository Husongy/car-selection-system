<template>
  <div class="analysis-page">
    <n-card title="价格分布分析" :bordered="false">
      <n-spin :show="loading">
        <!-- ECharts 图表容器 -->
        <div id="price-bar" style="width: 100%; height: 500px"></div>
      </n-spin>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { NCard, NSpin } from 'naive-ui'
import * as echarts from 'echarts'
import type { ECharts } from 'echarts'
import { getCarAnalysis } from '@/api/django-car'

const loading = ref(false)
let chartInstance: ECharts | null = null

// 加载图表数据
const loadChart = async () => {
  loading.value = true
  
  try {
    // 获取后端返回的 ECharts 配置
    const chartOptions: any = await getCarAnalysis()
    
    // 初始化 ECharts 实例
    const chartDom = document.getElementById('price-bar')
    if (chartDom) {
      chartInstance = echarts.init(chartDom)
      
      // 直接使用后端返回的配置
      chartInstance.setOption(chartOptions)
      
      // 窗口大小改变时自适应
      window.addEventListener('resize', handleResize)
    }
  } catch (error) {
    console.error('加载图表数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 处理窗口大小改变
const handleResize = () => {
  chartInstance?.resize()
}

// 组件挂载时加载图表
onMounted(() => {
  loadChart()
})

// 组件卸载时清理
onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
})
</script>

<style scoped>
.analysis-page {
  padding: 20px;
}
</style>
