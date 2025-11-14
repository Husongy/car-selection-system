<template>
  <div class="home-container">
    <n-space vertical :size="24">
      <!-- 用户信息栏 -->
      <n-card v-if="userStore.token">
        <n-space justify="space-between" align="center">
          <n-space align="center">
            <n-avatar round size="large">
              {{ userStore.userInfo?.username.charAt(0).toUpperCase() }}
            </n-avatar>
            <div>
              <div style="font-size: 16px; font-weight: bold;">
                欢迎，{{ userStore.userInfo?.username }}
              </div>
              <n-tag v-if="userStore.userInfo?.is_superuser" type="warning" size="small">
                管理员
              </n-tag>
              <n-tag v-else type="info" size="small">
                普通用户
              </n-tag>
            </div>
          </n-space>
          <n-button @click="handleLogout" secondary>
            退出登录
          </n-button>
        </n-space>
      </n-card>
      
      <n-card v-else>
        <n-space justify="space-between" align="center">
          <n-text>您尚未登录，请先登录</n-text>
          <n-button type="primary" @click="goToLogin">
            去登录
          </n-button>
        </n-space>
      </n-card>

      <!-- 欢迎横幅 -->
      <n-card>
        <n-space vertical align="center">
          <h1>欢迎来到新能源汽车智能选车系统</h1>
          <p style="font-size: 16px; color: #666;">
            基于大数据分析，为您推荐最适合的新能源汽车
          </p>
          <n-button type="primary" size="large" @click="goToSelectCar">
            开始选车
          </n-button>
        </n-space>
      </n-card>

      <!-- 数据统计 -->
      <n-grid :cols="4" :x-gap="12">
        <n-gi>
          <n-statistic label="车辆总数" :value="statisticsData.totalCars">
            <template #suffix>辆</template>
          </n-statistic>
        </n-gi>
        <n-gi>
          <n-statistic label="品牌数量" :value="statisticsData.totalBrands">
            <template #suffix>个</template>
          </n-statistic>
        </n-gi>
        <n-gi>
          <n-statistic label="用户数量" :value="statisticsData.totalUsers">
            <template #suffix>人</template>
          </n-statistic>
        </n-gi>
        <n-gi>
          <n-statistic label="今日访问" :value="statisticsData.todayVisits">
            <template #suffix>次</template>
          </n-statistic>
        </n-gi>
      </n-grid>

      <!-- ECharts 图表示例 -->
      <n-card title="热门品牌分布">
        <v-chart class="chart" :option="chartOption" autoresize />
      </n-card>
    </n-space>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { useUserStore } from '@/stores/user'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components'
import type { EChartsOption } from 'echarts'
import { getStatistics } from '@/api/home'

// 注册ECharts组件
use([
  CanvasRenderer,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
])

const router = useRouter()
const message = useMessage()
const userStore = useUserStore()

// 统计数据
const statisticsData = ref({
  totalCars: 0,
  totalBrands: 0,
  totalUsers: 0,
  todayVisits: 0
})

// ECharts 配置
const chartOption = ref<EChartsOption>({
  tooltip: {
    trigger: 'item',
    formatter: '{a} <br/>{b}: {c} ({d}%)'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: '品牌占比',
      type: 'pie',
      radius: '50%',
      data: [
        { value: 1048, name: '比亚迪' },
        { value: 735, name: '特斯拉' },
        { value: 580, name: '蔚来' },
        { value: 484, name: '小鹏' },
        { value: 300, name: '理想' }
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
})

// 跳转到选车页面
const goToSelectCar = () => {
  router.push('/select-car')
}

// 跳转到登录页面
const goToLogin = () => {
  router.push('/login')
}

// 退出登录
const handleLogout = async () => {
  try {
    await userStore.logout()
    message.success('退出登录成功')
  } catch (error) {
    console.error('退出登录失败:', error)
  }
}

// 加载统计数据
const loadStatistics = async () => {
  try {
    const data = await getStatistics()
    statisticsData.value = data
  } catch (error) {
    console.error('加载统计数据失败:', error)
    // 使用模拟数据
    statisticsData.value = {
      totalCars: 1280,
      totalBrands: 45,
      totalUsers: 8960,
      todayVisits: 342
    }
  }
}

onMounted(() => {
  loadStatistics()
})
</script>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  margin: 0;
  font-size: 32px;
  color: #18a058;
}

.chart {
  height: 400px;
}
</style>
