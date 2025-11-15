<template>
  <div class="sales-rank-page">
    <n-card title="销量排行榜" :bordered="false">
      <!-- 筛选条件 -->
      <n-space :size="16" style="margin-bottom: 20px">
        <n-radio-group v-model:value="monthRange" @update:value="handleMonthChange">
          <n-radio-button value="1m">最近1个月</n-radio-button>
          <n-radio-button value="3m">最近3个月</n-radio-button>
          <n-radio-button value="1y">最近1年</n-radio-button>
        </n-radio-group>
      </n-space>

      <!-- 数据表格 -->
      <n-data-table
        :columns="columns"
        :data="tableData"
        :loading="loading"
        :bordered="false"
        :single-line="false"
      />

      <!-- 分页器 -->
      <n-pagination
        v-model:page="currentPage"
        :page-count="totalPages"
        :page-size="pageSize"
        show-size-picker
        :page-sizes="[10, 20, 30, 50]"
        @update:page="handlePageChange"
        @update:page-size="handlePageSizeChange"
        style="margin-top: 20px; justify-content: flex-end"
      >
        <template #prefix="{ itemCount }">
          共 {{ itemCount }} 条
        </template>
      </n-pagination>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, h } from 'vue'
import { NCard, NSpace, NRadioGroup, NRadioButton, NDataTable, NPagination, NTag } from 'naive-ui'
import { getSalesRank } from '@/api/django-car'
import type { DataTableColumns } from 'naive-ui'

// 响应式数据
const monthRange = ref('1y')
const currentPage = ref(1)
const pageSize = ref(20)
const totalRecords = ref(0)
const tableData = ref<any[]>([])
const loading = ref(false)

// 计算总页数
const totalPages = computed(() => Math.ceil(totalRecords.value / pageSize.value))

// 表格列定义
const columns: DataTableColumns = [
  {
    title: '排名',
    key: 'rank',
    width: 80,
    align: 'center',
    render(row: any) {
      const rank = row.rank
      if (rank <= 3) {
        const colors = ['#FFD700', '#C0C0C0', '#CD7F32']
        return h(NTag, { type: 'warning', round: true, style: { backgroundColor: colors[rank - 1] } }, 
          { default: () => `第${rank}名` })
      }
      return rank
    }
  },
  {
    title: '品牌',
    key: 'brand_name',
    width: 120
  },
  {
    title: '车系名称',
    key: 'car_series_name',
    ellipsis: {
      tooltip: true
    }
  },
  {
    title: '总销量',
    key: 'total_sales',
    width: 120,
    align: 'right',
    render(row: any) {
      return h('span', { style: { color: '#18A058', fontWeight: 'bold' } }, 
        row.total_sales?.toLocaleString() || 0)
    }
  }
]

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const response: any = await getSalesRank({
      month: monthRange.value,
      page: currentPage.value,
      pagesize: pageSize.value
    })
    
    tableData.value = response.records || []
    totalRecords.value = response.total || 0
  } catch (error) {
    console.error('加载销量数据失败:', error)
    console.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 事件处理
const handleMonthChange = () => {
  currentPage.value = 1
  loadData()
}

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
  loadData()
})
</script>

<style scoped>
.sales-rank-page {
  padding: 20px;
}
</style>
