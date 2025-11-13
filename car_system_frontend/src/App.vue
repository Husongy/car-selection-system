<template>
  <n-config-provider :theme="theme">
    <n-message-provider>
      <n-notification-provider>
        <n-dialog-provider>
          <n-layout>
            <n-layout-header bordered style="height: 64px; padding: 0 24px; display: flex; align-items: center;">
              <div class="logo">
                <h2>🚗 新能源汽车智能选车系统</h2>
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
import { NIcon } from 'naive-ui'
import type { MenuOption } from 'naive-ui'
import { HomeOutline, CarSportOutline } from '@vicons/ionicons5'

const route = useRoute()
const theme = ref(null)
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
          to: '/select-car'
        },
        { default: () => '智能选车' }
      ),
    key: '/select-car',
    icon: renderIcon(CarSportOutline)
  }
]
</script>

<style scoped>
.logo h2 {
  margin: 0;
  font-size: 20px;
  color: #18a058;
}
</style>
