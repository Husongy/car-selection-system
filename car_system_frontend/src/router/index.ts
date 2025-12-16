import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useUserStore } from '@/stores/user'

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
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: {
      title: '用户注册'
    }
  },
  {
    path: '/select-car',
    name: 'SelectCar',
    component: () => import('@/views/SelectCar.vue'),
    meta: {
      title: '智能选车',
      requiresAuth: true  // 需要登录
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
  },
  // Django 后端页面
  {
    path: '/django/sales-rank',
    name: 'DjangoSalesRank',
    component: () => import('@/views/DjangoSalesRank.vue'),
    meta: {
      title: '销量排行榜 (Django)'
    }
  },
  {
    path: '/django/bad-review-rank',
    name: 'BadReviewRank',
    component: () => import('@/views/BadReviewRank.vue'),
    meta: {
      title: '差评榜单'
    }
  },
  {
    path: '/django/analysis',
    name: 'DjangoAnalysis',
    component: () => import('@/views/DjangoAnalysis.vue'),
    meta: {
      title: '价格分布分析 (Django)'
    }
  },
  {
    path: '/django/select-car',
    name: 'DjangoSelectCar',
    component: () => import('@/views/DjangoSelectCar.vue'),
    meta: {
      title: '条件选车 (Django)'
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
  
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    const userStore = useUserStore()
    
    if (!userStore.isLoggedIn) {
      // 未登录，跳转到登录页
      next({
        path: '/login',
        query: { redirect: to.fullPath }  // 保存目标路由
      })
      return
    }
  }
  
  next()
})

export default router
