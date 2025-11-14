<template>
  <div class="login-container">
    <n-card class="login-card" title="用户登录" size="large">
      <n-tabs v-model:value="activeTab" type="segment" animated>
        <!-- 登录选项卡 -->
        <n-tab-pane name="login" tab="登录">
          <n-form
            ref="loginFormRef"
            :model="loginForm"
            :rules="loginRules"
            size="large"
            label-placement="left"
          >
            <n-form-item path="username" label="用户名">
              <n-input
                v-model:value="loginForm.username"
                placeholder="请输入用户名"
                @keyup.enter="handleLogin"
              />
            </n-form-item>
            
            <n-form-item path="password" label="密码">
              <n-input
                v-model:value="loginForm.password"
                type="password"
                show-password-on="click"
                placeholder="请输入密码"
                @keyup.enter="handleLogin"
              />
            </n-form-item>
            
            <n-form-item>
              <n-button
                type="primary"
                size="large"
                block
                :loading="loginLoading"
                @click="handleLogin"
              >
                登录
              </n-button>
            </n-form-item>
          </n-form>
        </n-tab-pane>

        <!-- 注册选项卡 -->
        <n-tab-pane name="register" tab="注册">
          <n-form
            ref="registerFormRef"
            :model="registerForm"
            :rules="registerRules"
            size="large"
            label-placement="left"
          >
            <n-form-item path="username" label="用户名">
              <n-input
                v-model:value="registerForm.username"
                placeholder="3-50个字符"
              />
            </n-form-item>
            
            <n-form-item path="email" label="邮箱">
              <n-input
                v-model:value="registerForm.email"
                placeholder="选填"
              />
            </n-form-item>
            
            <n-form-item path="password" label="密码">
              <n-input
                v-model:value="registerForm.password"
                type="password"
                show-password-on="click"
                placeholder="至少6个字符"
              />
            </n-form-item>
            
            <n-form-item path="confirmPassword" label="确认密码">
              <n-input
                v-model:value="registerForm.confirmPassword"
                type="password"
                show-password-on="click"
                placeholder="再次输入密码"
              />
            </n-form-item>
            
            <n-form-item>
              <n-button
                type="primary"
                size="large"
                block
                :loading="registerLoading"
                @click="handleRegister"
              >
                注册
              </n-button>
            </n-form-item>
          </n-form>
        </n-tab-pane>
      </n-tabs>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage, type FormInst, type FormRules } from 'naive-ui'
import { useUserStore } from '@/stores/user'
import { register as registerApi } from '@/api/auth'

const router = useRouter()
const message = useMessage()
const userStore = useUserStore()

// 当前选项卡
const activeTab = ref('login')

// 登录表单
const loginFormRef = ref<FormInst | null>(null)
const loginForm = ref({
  username: '',
  password: ''
})
const loginLoading = ref(false)

const loginRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

// 注册表单
const registerFormRef = ref<FormInst | null>(null)
const registerForm = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})
const registerLoading = ref(false)

const registerRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度为3-50个字符', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      validator: (rule, value) => {
        return value === registerForm.value.password
      },
      message: '两次输入的密码不一致',
      trigger: 'blur'
    }
  ]
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    loginLoading.value = true
    
    await userStore.login(loginForm.value.username, loginForm.value.password)
    
    message.success('登录成功')
    router.push('/')
  } catch (error: any) {
    console.error('登录失败:', error)
    message.error(error.message || '登录失败')
  } finally {
    loginLoading.value = false
  }
}

// 处理注册
const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  try {
    await registerFormRef.value.validate()
    registerLoading.value = true
    
    await registerApi({
      username: registerForm.value.username,
      password: registerForm.value.password,
      email: registerForm.value.email || undefined
    })
    
    message.success('注册成功，请登录')
    
    // 切换到登录选项卡
    activeTab.value = 'login'
    loginForm.value.username = registerForm.value.username
    
    // 清空注册表单
    registerForm.value = {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    }
  } catch (error: any) {
    console.error('注册失败:', error)
    message.error(error.message || '注册失败')
  } finally {
    registerLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 100%;
  max-width: 450px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}
</style>
