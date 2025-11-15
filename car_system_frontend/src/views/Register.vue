<template>
  <div class="register-container">
    <n-card class="register-card" title="用户注册" size="large">
      <n-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-placement="left"
        label-width="auto"
      >
        <n-form-item label="用户名" path="username">
          <n-input
            v-model:value="formData.username"
            placeholder="请输入用户名"
            @keydown.enter="handleRegister"
          />
        </n-form-item>
        
        <n-form-item label="邮箱" path="email">
          <n-input
            v-model:value="formData.email"
            placeholder="请输入邮箱（可选）"
            @keydown.enter="handleRegister"
          />
        </n-form-item>
        
        <n-form-item label="密码" path="password">
          <n-input
            v-model:value="formData.password"
            type="password"
            show-password-on="click"
            placeholder="请输入密码"
            @keydown.enter="handleRegister"
          />
        </n-form-item>
        
        <n-form-item label="确认密码" path="confirmPassword">
          <n-input
            v-model:value="formData.confirmPassword"
            type="password"
            show-password-on="click"
            placeholder="请再次输入密码"
            @keydown.enter="handleRegister"
          />
        </n-form-item>
        
        <n-form-item>
          <n-button
            type="primary"
            block
            :loading="loading"
            @click="handleRegister"
          >
            注册
          </n-button>
        </n-form-item>
        
        <n-form-item>
          <n-button
            text
            @click="goToLogin"
          >
            已有账号？立即登录
          </n-button>
        </n-form-item>
      </n-form>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage, FormInst } from 'naive-ui'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const message = useMessage()
const userStore = useUserStore()

const formRef = ref<FormInst | null>(null)
const loading = ref(false)

const formData = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度为 3-20 个字符', trigger: 'blur' }
  ],
  email: [
    { 
      pattern: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/, 
      message: '请输入有效的邮箱地址', 
      trigger: 'blur' 
    }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度为 6-20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      validator: (rule: any, value: string) => {
        return value === formData.password
      },
      message: '两次输入的密码不一致',
      trigger: 'blur'
    }
  ]
}

// 处理注册
const handleRegister = async () => {
  try {
    await formRef.value?.validate()
    
    loading.value = true
    const result = await userStore.registerDjango(
      formData.username,
      formData.password,
      formData.email || undefined
    )
    
    if (result.success) {
      message.success(result.message)
      setTimeout(() => {
        router.push('/login')
      }, 1000)
    } else {
      message.error(result.message)
    }
  } catch (error) {
    console.error('表单验证失败:', error)
  } finally {
    loading.value = false
  }
}

// 跳转到登录页
const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-card {
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}
</style>
