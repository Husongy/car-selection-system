import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: {
      title: '首页'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: {
      title: '用户登录'
    }
  },
  {
    path: '/select-car',
    name: 'SelectCar',
    component: () => import('@/views/SelectCar.vue'),
    meta: {
      title: '智能选车'
    }
  },
  {
    path: '/sales-ranking',
    name: 'SalesRanking',
    component: () => import('@/views/SalesRanking.vue'),
    meta: {
      title: '销量榜单'
    }
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: () => import('@/views/Analysis.vue'),
    meta: {
      title: '可视化分析'
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 新能源汽车智能选车系统`
  }
  next()
})

export default router
