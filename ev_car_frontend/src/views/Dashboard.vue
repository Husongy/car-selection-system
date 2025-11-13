<template>
  <div class="dashboard">
    <h1>欢迎，{{ user?.username }}！</h1>
    <p>这是您的仪表盘页面</p>
    <button @click="logout" class="logout-btn">退出登录</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const user = authStore.user

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.dashboard {
  padding: 2rem;
  text-align: center;
}

.logout-btn {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>