<template>
  <div class="analysis-container">
    <!-- 页面标题 -->
    <n-page-header title="数据可视化分析" subtitle="基于ECharts的多维度数据展示">
      <template #extra>
        <n-space>
          <n-button type="primary" @click="loadAllData" :loading="loading">
            刷新数据
          </n-button>
        </n-space>
      </template>
    </n-page-header>

    <n-space vertical :size="16" style="margin-top: 16px">
      <!-- 降价排行榜 -->
      <n-card title="车系降价排行榜" :bordered="false">
        <template #header-extra>
          <n-text depth="3" style="font-size: 13px">
            展示官方价与经销商价差额最大的前30款车系
          </n-text>
        </template>
        <n-spin :show="loading">
          <price-discount-chart 
            v-if="priceDiscountData.length > 0"
            :data="priceDiscountData" 
            height="500px"
          />
          <n-empty v-else description="暂无数据" />
        </n-spin>
      </n-card>

      <!-- 品牌和价格分布并排显示 -->
      <n-grid :cols="2" :x-gap="16">
        <!-- 品牌数量分布 -->
        <n-grid-item>
          <n-card title="汽车品牌数量TOP分布" :bordered="false">
            <template #header-extra>
              <n-text depth="3" style="font-size: 13px">
                展示车系数量最多的前30个品牌
              </n-text>
            </template>
            <n-spin :show="loading">
              <brand-count-chart 
                v-if="brandCountData.length > 0"
                :data="brandCountData" 
                height="500px"
              />
              <n-empty v-else description="暂无数据" />
            </n-spin>
          </n-card>
        </n-grid-item>

        <!-- 价格区间分布 -->
        <n-grid-item>
          <n-card title="价格范围数量分布" :bordered="false">
            <template #header-extra>
              <n-text depth="3" style="font-size: 13px">
                展示不同价格区间的车系数量分布
              </n-text>
            </template>
            <n-spin :show="loading">
              <price-range-chart 
                v-if="priceRangeData.length > 0"
                :data="priceRangeData" 
                height="500px"
              />
              <n-empty v-else description="暂无数据" />
            </n-spin>
          </n-card>
        </n-grid-item>
      </n-grid>
    </n-space>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useMessage } from 'naive-ui'
import PriceDiscountChart from '@/components/PriceDiscountChart.vue'
import BrandCountChart from '@/components/BrandCountChart.vue'
import PriceRangeChart from '@/components/PriceRangeChart.vue'
import {
  getPriceDiscountRanking,
  getBrandCountDistribution,
  getPriceRangeDistribution,
  type PriceDiscountItem,
  type BrandCountItem,
  type PriceRangeItem
} from '@/api/analysis'

const message = useMessage()

// 数据状态
const priceDiscountData = ref<PriceDiscountItem[]>([])
const brandCountData = ref<BrandCountItem[]>([])
const priceRangeData = ref<PriceRangeItem[]>([])

// 加载状态
const loading = ref(false)

/**
 * 加载降价排行数据
 */
const loadPriceDiscountData = async () => {
  try {
    const response = await getPriceDiscountRanking(30)
    if (response.data) {
      priceDiscountData.value = response.data
    }
  } catch (error: any) {
    console.error('加载降价排行数据失败:', error)
    message.error(error.message || '加载降价排行数据失败')
  }
}

/**
 * 加载品牌数量分布数据
 */
const loadBrandCountData = async () => {
  try {
    const response = await getBrandCountDistribution(30)
    if (response.data) {
      brandCountData.value = response.data
    }
  } catch (error: any) {
    console.error('加载品牌数量数据失败:', error)
    message.error(error.message || '加载品牌数量数据失败')
  }
}

/**
 * 加载价格区间分布数据
 */
const loadPriceRangeData = async () => {
  try {
    const response = await getPriceRangeDistribution()
    if (response.data) {
      priceRangeData.value = response.data
    }
  } catch (error: any) {
    console.error('加载价格区间数据失败:', error)
    message.error(error.message || '加载价格区间数据失败')
  }
}

/**
 * 加载所有数据
 */
const loadAllData = async () => {
  loading.value = true
  try {
    await Promise.all([
      loadPriceDiscountData(),
      loadBrandCountData(),
      loadPriceRangeData()
    ])
    message.success('数据加载成功')
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadAllData()
})
</script>

<style scoped>
.analysis-container {
  padding: 16px;
  max-width: 1400px;
  margin: 0 auto;
}
</style>
