<template>
  <div class="select-car-page">
    <n-grid :cols="24" :x-gap="20">
      <!-- 左侧筛选区 -->
      <n-gi :span="6">
        <n-card title="筛选条件" :bordered="false">
          <n-form label-placement="top">
            <!-- 品牌选择 -->
            <n-form-item label="品牌">
              <n-select
                v-model:value="filters.brand_id"
                :options="brandOptions"
                placeholder="请选择品牌"
                clearable
              />
            </n-form-item>

            <!-- 能源类型 -->
            <n-form-item label="能源类型">
              <n-select
                v-model:value="filters.fuel_type"
                :options="fuelTypeOptions"
                placeholder="请选择能源类型"
                clearable
              />
            </n-form-item>

            <!-- 价格范围 -->
            <n-form-item label="价格范围（万元）">
              <n-space vertical style="width: 100%">
                <n-input-number
                  v-model:value="filters.min_price"
                  placeholder="最低价格"
                  :min="0"
                  style="width: 100%"
                />
                <n-input-number
                  v-model:value="filters.max_price"
                  placeholder="最高价格"
                  :min="0"
                  style="width: 100%"
                />
              </n-space>
            </n-form-item>

            <!-- 续航里程 -->
            <n-form-item label="最低续航（km）">
              <n-input-number
                v-model:value="filters.min_endurance"
                placeholder="请输入最低续航"
                :min="0"
                style="width: 100%"
              />
            </n-form-item>

            <!-- 车身类型 -->
            <n-form-item label="车身类型">
              <n-input
                v-model:value="filters.body_type"
                placeholder="如：SUV、轿车"
                clearable
              />
            </n-form-item>

            <!-- 操作按钮 -->
            <n-space vertical style="width: 100%">
              <n-button
                type="primary"
                block
                :loading="loading"
                @click="handleSearch"
              >
                查询
              </n-button>
              <n-button block @click="handleReset">
                重置
              </n-button>
            </n-space>
          </n-form>
        </n-card>
      </n-gi>

      <!-- 右侧结果区 -->
      <n-gi :span="18">
        <n-card title="车系列表" :bordered="false">
          <!-- 结果统计 -->
          <template #header-extra>
            <n-tag type="info">
              共找到 {{ totalRecords }} 个车系
            </n-tag>
          </template>

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
            <template #prefix>
              共 {{ totalRecords }} 条
            </template>
          </n-pagination>
        </n-card>
      </n-gi>
    </n-grid>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, h } from 'vue'
import {
  NGrid,
  NGi,
  NCard,
  NForm,
  NFormItem,
  NSelect,
  NInput,
  NInputNumber,
  NSpace,
  NButton,
  NDataTable,
  NPagination,
  NTag
} from 'naive-ui'
import type { DataTableColumns, SelectOption } from 'naive-ui'
import { filterCars, getBrandList } from '@/api/django-car'

// 筛选条件
const filters = ref({
  brand_id: null as number | null,
  fuel_type: null as string | null,
  min_price: null as number | null,
  max_price: null as number | null,
  min_endurance: null as number | null,
  body_type: ''
})

// 分页数据
const currentPage = ref(1)
const pageSize = ref(20)
const totalRecords = ref(0)
const tableData = ref<any[]>([])
const loading = ref(false)

// 品牌选项
const brandOptions = ref<SelectOption[]>([])

// 能源类型选项
const fuelTypeOptions: SelectOption[] = [
  { label: '纯电动', value: 'BEV' },
  { label: '插电混动', value: 'PHEV' },
  { label: '混合动力', value: 'HEV' }
]

// 计算总页数
const totalPages = computed(() => Math.ceil(totalRecords.value / pageSize.value))

// 表格列定义
const columns: DataTableColumns = [
  {
    title: '品牌',
    key: 'brand_name',
    width: 100
  },
  {
    title: '车系名称',
    key: 'name',
    ellipsis: {
      tooltip: true
    }
  },
  {
    title: '能源类型',
    key: 'fuel_type',
    width: 100,
    render(row: any) {
      const typeMap: any = {
        BEV: '纯电动',
        PHEV: '插电混动',
        HEV: '混合动力'
      }
      return typeMap[row.fuel_type] || row.fuel_type
    }
  },
  {
    title: '价格区间（万元）',
    key: 'price',
    width: 150,
    render(row: any) {
      if (row.price_min && row.price_max) {
        return `${row.price_min} - ${row.price_max}`
      }
      return '-'
    }
  },
  {
    title: '续航（km）',
    key: 'endurance',
    width: 120,
    render(row: any) {
      if (row.endurance_min && row.endurance_max) {
        return `${row.endurance_min} - ${row.endurance_max}`
      }
      return '-'
    }
  },
  {
    title: '车身类型',
    key: 'body_type',
    width: 100
  }
]

// 加载品牌列表
const loadBrands = async () => {
  try {
    const response: any = await getBrandList()
    brandOptions.value = (response.records || []).map((brand: any) => ({
      label: brand.name,
      value: brand.id
    }))
  } catch (error) {
    console.error('加载品牌列表失败:', error)
  }
}

// 加载车系数据
const loadData = async () => {
  loading.value = true
  try {
    const params = {
      ...filters.value,
      page: currentPage.value,
      pagesize: pageSize.value
    }
    
    const response: any = await filterCars(params)
    
    tableData.value = response.records || []
    totalRecords.value = response.total || 0
  } catch (error) {
    console.error('加载车系数据失败:', error)
  } finally {
    loading.value = false
  }
}

// 查询
const handleSearch = () => {
  currentPage.value = 1
  loadData()
}

// 重置
const handleReset = () => {
  filters.value = {
    brand_id: null,
    fuel_type: null,
    min_price: null,
    max_price: null,
    min_endurance: null,
    body_type: ''
  }
  currentPage.value = 1
  loadData()
}

// 分页事件
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
  loadBrands()
  loadData()
})
</script>

<style scoped>
.select-car-page {
  padding: 20px;
}
</style>
