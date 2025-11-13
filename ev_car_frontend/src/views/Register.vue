<template>
  <div class="login-container">
    <div class="login-form">
      <h2>用户注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <input
            v-model="registerForm.username"
            type="text"
            placeholder="用户名"
            required
          />
        </div>
        <div class="form-group">
          <input
            v-model="registerForm.email"
            type="email"
            placeholder="邮箱 (可选)"
          />
        </div>
        <div class="form-group">
          <input
            v-model="registerForm.password"
            type="password"
            placeholder="密码 (至少 6 位)"
            required
          />
        </div>
        <div class="form-group">
          <input
            v-model="registerForm.password_confirm"
            type="password"
            placeholder="确认密码"
            required
          />
        </div>
        <button type="submit" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>
      <p class="register-link">
        已有账号？<router-link to="/login">去登录</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const registerForm = ref({
  username: '',
  email: '',
  password: '',
  password_confirm: ''
})

const loading = ref(false)

const handleRegister = async () => {
  // 前端验证
  if (!registerForm.value.username || !registerForm.value.password || !registerForm.value.password_confirm) {
    alert('请填写必填项')
    return
  }

  if (registerForm.value.password.length < 6) {
    alert('密码长度至少 6 位')
    return
  }

  if (registerForm.value.password !== registerForm.value.password_confirm) {
    alert('两次输入的密码不一致')
    return
  }

  loading.value = true
  
  // 这里先模拟注册成功
  setTimeout(() => {
    authStore.setToken('mock-token-456')
    authStore.setUser({ username: registerForm.value.username })
    router.push('/dashboard')
    loading.value = false
  }, 1000)
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.login-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

button {
  width: 100%;
  padding: 0.75rem;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.register-link {
  margin-top: 1rem;
  text-align: center;
}

.register-link a {
  color: #42b883;
  text-decoration: none;
}
</style>