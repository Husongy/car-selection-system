import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useUserStore } from './stores/user'

// Naive UI
import naive from 'naive-ui'

// 全局样式
import './assets/styles/main.css'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(naive)

// 初始化用户store
const userStore = useUserStore()
userStore.init()

app.mount('#app')
