<template>
  <n-config-provider :theme-overrides="themeOverrides">
    <n-message-provider>
      <n-notification-provider>
        <n-dialog-provider>
          <n-layout>
            <n-layout-header bordered style="height: 64px; padding: 0 24px; display: flex; align-items: center;">
              <div class="logo" style="display: flex; align-items: center;">
                <!-- SVG Logo -->
                <svg width="40" height="40" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg" style="margin-right: 12px;">
                  <circle cx="100" cy="100" r="85" fill="none" stroke="rgba(24, 160, 88, 0.3)" stroke-width="2"/>
                  <circle cx="100" cy="100" r="75" fill="none" stroke="rgba(24, 160, 88, 0.5)" stroke-width="3"/>
                  <path d="M 100 40 L 85 100 L 105 100 L 90 160 L 130 90 L 110 90 L 125 40 Z" 
                        fill="#FFD700" stroke="#FFA500" stroke-width="2"/>
                  <ellipse cx="70" cy="140" rx="15" ry="15" fill="#18A058" opacity="0.9"/>
                  <ellipse cx="70" cy="140" rx="8" ry="8" fill="rgba(24, 160, 88, 0.8)"/>
                  <ellipse cx="130" cy="140" rx="15" ry="15" fill="#18A058" opacity="0.9"/>
                  <ellipse cx="130" cy="140" rx="8" ry="8" fill="rgba(24, 160, 88, 0.8)"/>
                  <path d="M 50 130 Q 60 110 80 105 L 120 105 Q 140 110 150 130" 
                        fill="none" stroke="#18A058" stroke-width="4" stroke-linecap="round"/>
                </svg>
                <h2 style="margin: 0; font-size: 20px; color: #18a058;">🚗 新能源汽车智能选车系统</h2>
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
import { ref, h, computed, type Component } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { NIcon, type GlobalThemeOverrides } from 'naive-ui'
import type { MenuOption } from 'naive-ui'
import { HomeOutline, CarSportOutline, BarChartOutline, TrophyOutline, FilterOutline } from '@vicons/ionicons5'

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
