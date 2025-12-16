<template>
  <n-config-provider :theme-overrides="themeOverrides">
    <n-message-provider>
      <n-notification-provider>
        <n-dialog-provider>
          <n-layout>
            <n-layout-header bordered style="height: 64px; padding: 0 24px; display: flex; align-items: center;">
              <div class="logo" style="display: flex; align-items: center;">
                <!-- SVG Logo -->
                <svg width="50" height="50" xmlns="http://www.w3.org/2000/svg" style="margin-right: 12px;">
                  <!-- 外圈 -->
                  <circle cx="25" cy="25" r="22" fill="none" stroke="#18A058" stroke-width="2"/>
                  
                  <!-- 叶子装饰 -->
                  <path d="M25,8 Q27.5,5 30,8 Q27.5,11 25,8" fill="#00E676"/>
                  <path d="M20,8 Q22.5,5 25,8 Q22.5,11 20,8" fill="#00E676"/>
                  
                  <!-- 中间文字 -->
                  <text x="25" y="29" font-family="Arial, sans-serif" font-size="10" font-weight="bold" fill="#18A058" text-anchor="middle">HoH</text>
                  
                  <!-- 电符号装饰 -->
                  <path d="M25,37 L26.5,40 L28,37 L26.5,38 Z" fill="#FFD700"/>
                </svg>
                <h2 style="margin: 0; font-size: 20px; color: #18a058;">新能源汽车智能选车系统</h2>
              </div>
              <n-menu
                :value="activeKey"
                mode="horizontal"
                :options="menuOptions"
                style="flex: 1; margin-left: 40px;"
              />
            </n-layout-header>
            <n-layout-content style="padding: 24px; min-height: calc(100vh - 64px);">
              <router-view />
            </n-layout-content>
          </n-layout>
        </n-dialog-provider>
      </n-notification-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup lang="ts">
import { h, computed, type Component } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { NIcon, type GlobalThemeOverrides } from 'naive-ui'
import type { MenuOption } from 'naive-ui'
import { HomeOutline, BarChartOutline, TrophyOutline, FilterOutline, WarningOutline } from '@vicons/ionicons5'

const route = useRoute()

// 自定义主题配置 - 主题色 #18A058
const themeOverrides: GlobalThemeOverrides = {
  common: {
    primaryColor: '#18A058',
    primaryColorHover: '#36ad6a',
    primaryColorPressed: '#0c7a43',
    primaryColorSuppl: '#36ad6a'
  },
  Button: {
    textColorPrimary: '#FFF'
  }
}

const activeKey = computed(() => route.path)

function renderIcon(icon: Component) {
  return () => h(NIcon, null, { default: () => h(icon) })
}

const menuOptions: MenuOption[] = [
  {
    label: () =>
      h(
        RouterLink,
        {
          to: '/'
        },
        { default: () => '首页' }
      ),
    key: '/',
    icon: renderIcon(HomeOutline)
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: '/django/select-car'
        },
        { default: () => '条件选车' }
      ),
    key: '/django/select-car',
    icon: renderIcon(FilterOutline)
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: '/django/sales-rank'
        },
        { default: () => '销量排行' }
      ),
    key: '/django/sales-rank',
    icon: renderIcon(TrophyOutline)
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: '/django/bad-review-rank'
        },
        { default: () => '差评榜单' }
      ),
    key: '/django/bad-review-rank',
    icon: renderIcon(WarningOutline)
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: '/django/analysis'
        },
        { default: () => '数据分析' }
      ),
    key: '/django/analysis',
    icon: renderIcon(BarChartOutline)
  }
]
</script>

<style scoped>
.logo {
  display: flex;
  align-items: center;
}

.logo svg {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
  animation: logoRotate 20s linear infinite;
}

@keyframes logoRotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.logo h2 {
  margin: 0;
  font-size: 20px;
  color: #18a058;
}
</style>
