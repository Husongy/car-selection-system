/**
 * 用户认证状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { 
  login as loginApi, 
  getUserInfo as getUserInfoApi, 
  logout as logoutApi, 
  type UserInfo 
} from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref<string>('')
  const userInfo = ref<UserInfo | null>(null)
  const loading = ref<boolean>(false)

  // 计算属性
  const isLoggedIn = computed(() => !!token.value && !!userInfo.value)
  const isAdmin = computed(() => userInfo.value?.is_superuser ?? false)

  /**
   * 设置Token
   */
  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  /**
   * 设置用户信息
   */
  const setUserInfo = (info: UserInfo) => {
    userInfo.value = info
    localStorage.setItem('userInfo', JSON.stringify(info))
  }

  /**
   * 清除用户信息
   */
  const clearUserInfo = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  /**
   * 初始化 - 从localStorage恢复状态
   */
  const init = () => {
    const savedToken = localStorage.getItem('token')
    const savedUserInfo = localStorage.getItem('userInfo')
    
    if (savedToken) {
      token.value = savedToken
    }
    
    if (savedUserInfo) {
      try {
        userInfo.value = JSON.parse(savedUserInfo)
      } catch (error) {
        console.error('解析用户信息失败:', error)
        clearUserInfo()
      }
    }
  }

  /**
   * 用户登录
   */
  const login = async (username: string, password: string) => {
    try {
      loading.value = true
      
      const response = await loginApi({ username, password }) as any
      
      // response 已经是 TokenResponse 类型（由响应拦截器处理）
      if (response && response.access_token) {
        // 保存token
        setToken(response.access_token)
        
        // 获取用户信息
        await fetchUserInfo()
        
        return { success: true, message: '登录成功' }
      } else {
        throw new Error('登录失败')
      }
    } catch (error: any) {
      clearUserInfo()
      
      // 提取错误信息
      let errorMessage = '登录失败'
      
      if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      } else if (error.response?.data?.message) {
        errorMessage = error.response.data.message
      } else if (error.message) {
        errorMessage = error.message
      }
      
      console.error('登录错误:', error)
      return { success: false, message: errorMessage }
    } finally {
      loading.value = false
    }
  }

  /**
   * 获取用户信息
   */
  const fetchUserInfo = async () => {
    try {
      const response = await getUserInfoApi() as any
      
      // response 已经是 UserInfo 类型（由响应拦截器处理）
      if (response) {
        setUserInfo(response as UserInfo)
        return { success: true, data: response }
      } else {
        throw new Error('获取用户信息失败')
      }
    } catch (error: any) {
      console.error('获取用户信息失败:', error)
      clearUserInfo()
      return { success: false, message: error.message || '获取用户信息失败' }
    }
  }

  /**
   * 退出登录
   */
  const logout = async () => {
    try {
      await logoutApi()
    } catch (error) {
      console.error('退出登录API调用失败:', error)
    } finally {
      clearUserInfo()
    }
  }

  return {
    // 状态
    token,
    userInfo,
    loading,
    
    // 计算属性
    isLoggedIn,
    isAdmin,
    
    // 方法
    setToken,
    setUserInfo,
    clearUserInfo,
    init,
    login,
    fetchUserInfo,
    logout
  }
})
