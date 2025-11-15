<template>
  <div class="login-container">
    <!-- 左侧展示区 -->
    <div class="login-left">
      <div class="system-info">
        <!-- Logo 设计 -->
        <div class="logo-container">
          <div class="logo">
            <svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
              <!-- 外圈 -->
              <circle cx="100" cy="100" r="90" fill="none" stroke="#FFFFFF" stroke-width="3"/>
              
              <!-- 叶子装饰 -->
              <path d="M100,30 Q110,20 120,30 Q110,40 100,30" fill="#00E676"/>
              <path d="M80,30 Q90,20 100,30 Q90,40 80,30" fill="#00E676"/>
              
              <!-- 中间文字 -->
              <text x="100" y="105" font-family="Arial, sans-serif" font-size="32" font-weight="bold" fill="#FFFFFF" text-anchor="middle">HoH</text>
              <text x="100" y="135" font-family="Arial, sans-serif" font-size="14" fill="rgba(255,255,255,0.9)" text-anchor="middle">新能源选车系统</text>
              
              <!-- 电符号装饰 -->
              <path d="M100,150 L105,160 L110,150 L105,155 Z" fill="#FFD700"/>
              
              <!-- 装饰圆点 -->
              <circle cx="100" cy="100" r="95" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="1" stroke-dasharray="5,5">
                <animateTransform attributeName="transform" type="rotate" from="0 100 100" to="360 100 100" dur="20s" repeatCount="indefinite"/>
              </circle>
            </svg>
          </div>
        </div>
        
        <div class="system-header">
          <h1>新能源汽车智能选车系统</h1>
        </div>
        <p class="system-slogan">创新选车 · 智慧出行</p>
        
        <div class="features">
          <div class="feature-item">
            <div class="feature-icon">
              <n-icon size="24" :component="CarSportOutline" />
            </div>
            <div class="feature-content">
              <h3>多维度条件筛选</h3>
              <p>品牌、价格、续航、车型等多维度筛选</p>
            </div>
          </div>
          
          <div class="feature-item">
            <div class="feature-icon">
              <n-icon size="24" :component="BarChartOutline" />
            </div>
            <div class="feature-content">
              <h3>数据可视化分析</h3>
              <p>销量排行、价格分布、实时图表展示</p>
            </div>
          </div>
          
          <div class="feature-item">
            <div class="feature-icon">
              <n-icon size="24" :component="CheckmarkCircleOutline" />
            </div>
            <div class="feature-content">
              <h3>智能推荐引擎</h3>
              <p>基于大数据分析，精准匹配最优选择</p>
            </div>
          </div>
        </div>
        
        <div class="stats">
          <div class="stat-item">
            <div class="stat-value">500+</div>
            <div class="stat-label">车型数据</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">120</div>
            <div class="stat-label">品牌覆盖</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">200+</div>
            <div class="stat-label">活跃用户</div>
          </div>
        </div>
        
        <div class="copyright">
          ©2025 新能源汽车智能选车系统 版权所有
        </div>
      </div>
    </div>

    <!-- 右侧表单区 -->
    <div class="login-right">
      <div class="form-card">
        <h2 class="form-title">欢迎登录</h2>
        <p class="form-subtitle">请使用您的账号登录系统</p>
        
        <n-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          size="large"
        >
          <n-form-item path="username">
            <n-input
              v-model:value="loginForm.username"
              placeholder="请输入用户名"
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <n-icon :component="PersonOutline" />
              </template>
            </n-input>
          </n-form-item>
          
          <n-form-item path="password">
            <n-input
              v-model:value="loginForm.password"
              type="password"
              show-password-on="click"
              placeholder="请输入密码"
              @keyup.enter="handleLogin"
            >
              <template #prefix>
                <n-icon :component="LockClosedOutline" />
              </template>
            </n-input>
          </n-form-item>
          
          <n-form-item>
            <n-button
              type="primary"
              size="large"
              block
              :loading="loginLoading"
              @click="handleLogin"
              strong
              class="gradient-button"
            >
              登录
            </n-button>
          </n-form-item>
        </n-form>
        
        <div class="login-tips">
          <p>还没有账号？<a href="#">立即注册</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage, type FormInst, type FormRules } from 'naive-ui'
import { PersonOutline, LockClosedOutline, CarSportOutline, BarChartOutline, CheckmarkCircleOutline } from '@vicons/ionicons5'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const message = useMessage()
const userStore = useUserStore()

// 登录表单
const loginFormRef = ref<FormInst | null>(null)
const loginForm = ref({
  username: '',
  password: ''
})
const loginLoading = ref(false)

const loginRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度为3-50个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6个字符', trigger: 'blur' }
  ]
}



/**
 * 处理登录
 */
const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    // 表单验证
    await loginFormRef.value.validate()
    
    loginLoading.value = true
    
    // 在控制台打印表单数据
    console.log('登录表单数据:', {
      username: loginForm.value.username,
      password: loginForm.value.password
    })
    
    // 模拟登录延迟
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // 模拟登录成功 - 直接设置用户信息到 store
    const mockToken = 'mock-token-' + Date.now()
    const mockUserInfo = {
      id: 1,
      username: loginForm.value.username,
      email: loginForm.value.username + '@example.com',
      is_superuser: loginForm.value.username === 'admin', // admin 用户为管理员
      is_active: true,
      created_at: new Date().toISOString()
    }
    
    // 保存到 store
    userStore.setToken(mockToken)
    userStore.setUserInfo(mockUserInfo)
    
    message.success('登录成功')
    
    // 跳转到首页
    await router.push('/')
  } catch (error: any) {
    console.error('表单验证失败:', error)
  } finally {
    loginLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  min-height: 100vh;
  background: #f0f2f5;
}

/* 左侧展示区 */
.login-left {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px;
  position: relative;
  overflow: hidden;
}

.login-left::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: float 20s linear infinite;
}

@keyframes float {
  0% {
    transform: translate(0, 0);
  }
  100% {
    transform: translate(50px, 50px);
  }
}

.system-info {
  max-width: 500px;
  color: white;
  position: relative;
  z-index: 1;
}

/* Logo 样式 */
.logo-container {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.logo {
  width: 150px;
  height: 150px;
  animation: logoFloat 3s ease-in-out infinite;
}

.logo svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.3));
}

@keyframes logoFloat {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.system-header {
  text-align: center;
  margin-bottom: 20px;
}

.system-header h1 {
  font-size: 32px;
  font-weight: 600;
  margin: 0;
  color: white;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.system-slogan {
  font-size: 18px;
  margin-bottom: 50px;
  opacity: 0.95;
}

.features {
  margin-bottom: 50px;
}

.feature-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 30px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  transition: all 0.3s;
}

.feature-item:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateX(10px);
}

.feature-icon {
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  flex-shrink: 0;
}

.feature-content h3 {
  font-size: 18px;
  margin: 0 0 8px 0;
  font-weight: 500;
}

.feature-content p {
  font-size: 14px;
  margin: 0;
  opacity: 0.9;
}

.stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 40px;
  padding: 30px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.copyright {
  text-align: center;
  font-size: 13px;
  opacity: 0.8;
}

/* 右侧表单区 */
.login-right {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: white;
  padding: 40px;
}

.form-card {
  width: 100%;
  max-width: 420px;
  background: white;
  border-radius: 16px;
  padding: 50px 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

.form-title {
  font-size: 32px;
  color: #333;
  margin: 0 0 12px 0;
  font-weight: 600;
  text-align: center;
}

.form-subtitle {
  font-size: 14px;
  color: #666;
  margin: 0 0 40px 0;
  text-align: center;
}

.login-tips {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}

.login-tips a {
  color: #18A058;
  text-decoration: none;
  font-weight: 500;
}

.login-tips a:hover {
  text-decoration: underline;
}

/* 渐变按钮样式 */
.gradient-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  border: none !important;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 1px;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.gradient-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
}

.gradient-button:active {
  transform: translateY(0);
}

/* 响应式设计 */
@media (max-width: 968px) {
  .login-container {
    flex-direction: column;
  }
  
  .login-left {
    min-height: 300px;
    padding: 40px 20px;
  }
  
  .system-header h1 {
    font-size: 24px;
  }
  
  .features {
    display: none;
  }
  
  .stats {
    margin-bottom: 20px;
  }
  
  .stat-value {
    font-size: 28px;
  }
  
  .form-card {
    padding: 30px 20px;
  }
}
</style>
