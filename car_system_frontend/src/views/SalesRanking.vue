<template>
  <div class="sales-ranking-container">
    <n-space vertical :size="24">
      <!-- 页面标题 -->
      <n-page-header title="销量榜单" subtitle="汽车销量数据排名">
        <template #extra>
          <n-space>
            <n-tag type="success" :bordered="false">
              {{ rankingData?.total_count || 0 }} 款车型
            </n-tag>
          </n-space>
        </template>
      </n-page-header>

      <!-- 筛选条件 -->
      <n-card title="筛选条件" :bordered="false" size="small">
        <n-space align="center">
          <span>查询周期：</span>
          <n-radio-group v-model:value="selectedPeriod" @update:value="handlePeriodChange">
            <n-radio-button value="last_year">近一年</n-radio-button>
            <n-radio-button value="last_6months">近半年</n-radio-button>
            <n-radio-button value="last_3months">近三个月</n-radio-button>
            <n-radio-button value="last_month">上个月</n-radio-button>
          </n-radio-group>
          
          <n-divider vertical />
          
          <span>自定义月份：</span>
          <n-date-picker
            v-model:formatted-value="customMonth"
            type="month"
            format="yyyy-MM"
            placeholder="选择月份"
            clearable
            @update:formatted-value="handleCustomMonthChange"
          />
        </n-space>
      </n-card>

      <!-- 统计信息 -->
      <n-card :bordered="false" v-if="rankingData">
        <n-descriptions :column="4" bordered size="small">
          <n-descriptions-item label="查询周期">
            {{ periodText }}
          </n-descriptions-item>
          <n-descriptions-item label="开始日期">
            {{ rankingData.start_date }}
          </n-descriptions-item>
          <n-descriptions-item label="结束日期">
            {{ rankingData.end_date }}
          </n-descriptions-item>
          <n-descriptions-item label="上榜车型">
            {{ rankingData.total_count }} 款
          </n-descriptions-item>
        </n-descriptions>
      </n-card>

      <!-- 排名表格 -->
      <n-card title="销量排行榜" :bordered="false">
        <n-data-table
          :columns="columns"
          :data="tableData"
          :loading="loading"
          :pagination="pagination"
          :row-key="(row: SalesRankingItem) => row.series_id"
          striped
        />
      </n-card>
    </n-space>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, h } from 'vue'
import {
  NSpace,
  NPageHeader,
  NCard,
  NTag,
  NRadioGroup,
  NRadioButton,
  NDivider,
  NDatePicker,
  NDescriptions,
  NDescriptionsItem,
  NDataTable,
  NImage,
  NText,
  useMessage,
  type DataTableColumns
} from 'naive-ui'
import { getSalesRanking, type SalesRankingItem } from '@/api/sales'

const message = useMessage()

// 响应式数据
const loading = ref(false)
const selectedPeriod = ref('last_year')
const customMonth = ref<string | null>(null)
const rankingData = ref<any>(null)
const tableData = ref<SalesRankingItem[]>([])

// 分页配置
const pagination = ref({
  pageSize: 20,
  showSizePicker: true,
  pageSizes: [10, 20, 50, 100],
  showQuickJumper: true
})

// 周期文本映射
const periodTextMap: Record<string, string> = {
  last_year: '近一年',
  last_6months: '近半年',
  last_3months: '近三个月',
  last_month: '上个月'
}

// 计算周期显示文本
const periodText = computed(() => {
  if (customMonth.value) {
    return customMonth.value
  }
  return periodTextMap[selectedPeriod.value] || selectedPeriod.value
})

// 表格列定义
const columns: DataTableColumns<SalesRankingItem> = [
  {
    title: '排名',
    key: 'rank',
    width: 80,
    align: 'center',
    render(row) {
      const colors = ['#FFD700', '#C0C0C0', '#CD7F32'] // 金银铜
      if (row.rank <= 3) {
        return h(
          NText,
          {
            type: 'success',
            strong: true,
            style: { fontSize: '18px', color: colors[row.rank - 1] }
          },
          { default: () => `🏆 ${row.rank}` }
        )
      }
      return row.rank
    }
  },
  {
    title: '车系图片',
    key: 'series_image',
    width: 120,
    render(row) {
      if (row.series_image) {
        return h(NImage, {
          width: 80,
          height: 60,
          src: row.series_image,
          objectFit: 'cover',
          lazy: true,
          fallbackSrc: 'https://via.placeholder.com/80x60?text=No+Image'
        })
      }
      return h(NText, { depth: 3 }, { default: () => '暂无图片' })
    }
  },
  {
    title: '车系名称',
    key: 'series_name',
    width: 180,
    ellipsis: {
      tooltip: true
    }
  },
  {
    title: '品牌',
    key: 'brand_name',
    width: 120,
    ellipsis: {
      tooltip: true
    }
  },
  {
    title: '总销量',
    key: 'total_sales',
    width: 120,
    align: 'right',
    render(row) {
      return h(
        NText,
        { type: 'success', strong: true },
        { default: () => row.total_sales.toLocaleString() + ' 辆' }
      )
    },
    sorter: (a, b) => a.total_sales - b.total_sales
  },
  {
    title: '价格区间',
    key: 'price_range',
    width: 150,
    render(row) {
      return row.price_range || '-'
    }
  },
  {
    title: '能源类型',
    key: 'energy_type',
    width: 120,
    render(row) {
      if (!row.energy_type) return '-'
      const typeMap: Record<string, { text: string; type: any }> = {
        '纯电动': { text: '纯电动', type: 'success' },
        '插电式混合动力': { text: '插混', type: 'info' },
        '油电混合': { text: '油混', type: 'warning' },
        '燃油': { text: '燃油', type: 'default' }
      }
      const config = typeMap[row.energy_type] || { text: row.energy_type, type: 'default' }
      return h(NTag, { type: config.type, size: 'small' }, { default: () => config.text })
    }
  }
]

// 加载数据
const loadData = async () => {
  try {
    loading.value = true
    const period = customMonth.value || selectedPeriod.value
    const res = await getSalesRanking(period, 100)
    
    if (res.code === 200 && res.data) {
      rankingData.value = res.data
      tableData.value = res.data.data || []
    } else {
      message.error(res.message || '加载失败')
    }
  } catch (error: any) {
    console.error('加载销量榜单失败:', error)
    message.error(error.message || '加载失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 周期变化处理
const handlePeriodChange = () => {
  customMonth.value = null
  loadData()
}

// 自定义月份变化处理
const handleCustomMonthChange = (value: string | null) => {
  if (value) {
    selectedPeriod.value = ''
    loadData()
  }
}

// 页面加载时获取数据
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.sales-ranking-container {
  padding: 24px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

:deep(.n-data-table) {
  font-size: 14px;
}

:deep(.n-data-table-th) {
  font-weight: 600;
  background-color: #fafafa;
}

:deep(.n-data-table-td) {
  padding: 12px 16px;
}
</style>
