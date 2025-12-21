<template>
  <div class="bad-review-rank-page">
    <n-space vertical :size="24">
      <!-- 页面标题 -->
      <n-page-header title="差评榜单" subtitle="根据投诉数据统计的车系质量问题排名">
        <template #extra>
          <n-tag type="error" :bordered="false">
            共 {{ totalRecords }} 款车型
          </n-tag>
        </template>
      </n-page-header>

      <!-- 筛选条件 -->
      <n-card title="筛选条件" :bordered="false" size="small">
        <n-space vertical :size="16">
          <!-- 时间范围选择 -->
          <n-space align="center">
            <span style="font-weight: 500">时间范围：</span>
            <n-radio-group v-model:value="timeRange" @update:value="handleTimeRangeChange">
              <n-radio-button value="1m">近1个月</n-radio-button>
              <n-radio-button value="6m">近半年</n-radio-button>
              <n-radio-button value="1y">近一年</n-radio-button>
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
              style="width: 150px"
            />
          </n-space>

          <!-- 问题类型筛选 -->
          <n-space align="center">
            <span style="font-weight: 500">问题类型：</span>
            <n-radio-group v-model:value="category" @update:value="handleCategoryChange">
              <n-radio-button value="">全部问题</n-radio-button>
              <n-radio-button value="quality">质量问题</n-radio-button>
              <n-radio-button value="service">服务问题</n-radio-button>
              <n-radio-button value="other">其他问题</n-radio-button>
            </n-radio-group>
          </n-space>
        </n-space>
      </n-card>

      <!-- 统计信息 -->
      <n-card :bordered="false" v-if="startDate && endDate">
        <n-descriptions :column="3" bordered size="small">
          <n-descriptions-item label="统计时间">
            {{ startDate }} ~ {{ endDate }}
          </n-descriptions-item>
          <n-descriptions-item label="上榜车型">
            {{ totalRecords }} 款
          </n-descriptions-item>
          <n-descriptions-item label="筛选条件">
            {{ categoryText }}
          </n-descriptions-item>
        </n-descriptions>
      </n-card>

      <!-- 排名表格 -->
      <n-card title="差评排行榜" :bordered="false">
        <template #header-extra>
          <n-button type="primary" @click="loadData" :loading="loading">
            刷新数据
          </n-button>
        </template>
        
        <n-data-table
          :columns="columns"
          :data="tableData"
          :loading="loading"
          :bordered="false"
          :single-line="false"
          striped
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
          <template #prefix>
            共 {{ totalRecords }} 条
          </template>
        </n-pagination>
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
  NPagination,
  NButton,
  NImage,
  NText,
  NTooltip,
  useMessage,
  type DataTableColumns
} from 'naive-ui'
import { getBadReviewRank, type BadReviewRankItem } from '@/api/django-car'

const message = useMessage()

// 生成SVG占位图的Data URL
const createPlaceholderSvg = (text: string, bgColor: string = '#f0f0f0', textColor: string = '#666') => {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="80" height="60" viewBox="0 0 80 60">
    <rect width="80" height="60" fill="${bgColor}"/>
    <text x="40" y="30" font-family="Arial" font-size="10" fill="${textColor}" text-anchor="middle" dominant-baseline="middle">${text}</text>
  </svg>`
  return `data:image/svg+xml,${encodeURIComponent(svg)}`
}

const defaultCarImage = createPlaceholderSvg('暂无图片', '#f5f5f5', '#999')

// 响应式数据
const loading = ref(false)
const timeRange = ref('1y')
const customMonth = ref<string | null>(null)
const category = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const totalRecords = ref(0)
const tableData = ref<BadReviewRankItem[]>([])
const startDate = ref('')
const endDate = ref('')

// 计算总页数
const totalPages = computed(() => Math.ceil(totalRecords.value / pageSize.value))

// 问题类型文本映射
const categoryTextMap: Record<string, string> = {
  '': '全部问题',
  'quality': '质量问题',
  'service': '服务问题',
  'other': '其他问题'
}

// 计算问题类型显示文本
const categoryText = computed(() => categoryTextMap[category.value] || '全部问题')

// 表格列定义
const columns: DataTableColumns<BadReviewRankItem> = [
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
            type: 'error',
            strong: true,
            style: { fontSize: '18px', color: colors[row.rank - 1] }
          },
          { default: () => `⚠️ ${row.rank}` }
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
          fallbackSrc: defaultCarImage,
          imgProps: { referrerpolicy: 'no-referrer' }
        })
      }
      return h(NText, { depth: 3 }, { default: () => '暂无图片' })
    }
  },
  {
    title: '车系名称',
    key: 'car_series_name',
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
    title: '总投诉次数',
    key: 'total_reports',
    width: 120,
    align: 'center',
    render(row) {
      return h(
        NText,
        { type: 'error', strong: true },
        { default: () => row.total_reports.toLocaleString() + ' 次' }
      )
    },
    sorter: (a, b) => a.total_reports - b.total_reports
  },
  {
    title: '问题种类数',
    key: 'issue_count',
    width: 120,
    align: 'center',
    render(row) {
      return h(
        NText,
        { type: 'warning' },
        { default: () => row.issue_count + ' 种' }
      )
    }
  },
  {
    title: '问题分类统计',
    key: 'category_stats',
    width: 220,
    render(row) {
      return h(
        NTooltip,
        {},
        {
          trigger: () => h(
            NSpace,
            { size: 8 },
            {
              default: () => [
                h(NTag, { type: 'error', size: 'small' }, { default: () => `质量: ${row.quality_count}` }),
                h(NTag, { type: 'warning', size: 'small' }, { default: () => `服务: ${row.service_count}` }),
                h(NTag, { type: 'info', size: 'small' }, { default: () => `其他: ${row.other_count}` })
              ]
            }
          ),
          default: () => '点击查看详细分类统计'
        }
      )
    }
  }
]

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const response: any = await getBadReviewRank({
      time_range: customMonth.value || timeRange.value,
      category: category.value,
      page: currentPage.value,
      pagesize: pageSize.value
    })
    
    tableData.value = response.records || []
    totalRecords.value = response.total || 0
    startDate.value = response.start_date || ''
    endDate.value = response.end_date || ''
  } catch (error) {
    console.error('加载差评榜单数据失败:', error)
    message.error('加载数据失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 时间范围变化处理
const handleTimeRangeChange = () => {
  customMonth.value = null
  currentPage.value = 1
  loadData()
}

// 自定义月份变化处理
const handleCustomMonthChange = (value: string | null) => {
  if (value) {
    timeRange.value = ''
    currentPage.value = 1
    loadData()
  } else {
    timeRange.value = '1y'
    loadData()
  }
}

// 问题类型变化处理
const handleCategoryChange = () => {
  currentPage.value = 1
  loadData()
}

// 页码变化处理
const handlePageChange = (page: number) => {
  currentPage.value = page
  loadData()
}

// 每页数量变化处理
const handlePageSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
  loadData()
}

// 页面加载时获取数据
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.bad-review-rank-page {
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
