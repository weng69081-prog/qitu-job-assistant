<template>
  <div class="login-page">
    <!-- 左侧品牌区：深蓝渐变 -->
    <div class="brand-side">
      <div class="brand-content">
        <div class="brand-icon">
          <i class="fas fa-graduation-cap"></i>
        </div>
        <h1>多模态AI求职助手</h1>
        <p class="brand-desc">基于大模型的智能择业分析 · 模拟面试 · 简历优化 · 投递匹配</p>
        <div class="brand-features">
          <div class="feature"><i class="fas fa-search"></i> 职业探索</div>
          <div class="feature"><i class="fas fa-microphone"></i> AI面试</div>
          <div class="feature"><i class="fas fa-file-lines"></i> 简历优化</div>
          <div class="feature"><i class="fas fa-chart-bar"></i> 投递分析</div>
        </div>
        <p class="brand-footer">第八组 · 2025</p>
      </div>
    </div>

    <!-- 右侧登录区：浅灰背景 + 白色卡片 -->
    <div class="form-side">
      <div class="form-wrapper card">
        <h2>欢迎回来</h2>
        <p class="form-sub">登录你的账号，继续求职之旅</p>
        <el-form :model="form" size="large" class="login-form">
          <el-form-item>
            <el-input v-model="form.username" placeholder="用户名" prefix-icon="User" />
          </el-form-item>
          <el-form-item>
            <el-input v-model="form.password" type="password" placeholder="密码" show-password prefix-icon="Lock" @keyup.enter="doLogin" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="doLogin" :loading="loading" class="login-btn">登 录</el-button>
          </el-form-item>
        </el-form>
        <div class="form-footer">
          还没有账号？<router-link to="/register">立即注册 <i class="fas fa-arrow-right"></i></router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const form = reactive({ username: '', password: '' })

async function doLogin() {
  if (!form.username || !form.password) return ElMessage.warning('请填写用户名和密码')
  loading.value = true
  try {
    const qs = new URLSearchParams({ username: form.username, password: form.password })
    const res = await fetch('/api/user/login?' + qs, { method: 'POST' })
    if (!res.ok) { const e = await res.json(); throw new Error(e.detail) }
    const data = await res.json()
    localStorage.setItem('token', data.token)
    localStorage.setItem('user', JSON.stringify(data.user))
    ElMessage.success(`欢迎回来，${data.user.nickname || data.user.username}！`)
    router.push('/career')
  } catch(e) {
    ElMessage.error(e.message || '用户名或密码错误')
  } finally { loading.value = false }
}
</script>

<style scoped>
.login-page {
  display: flex;
  min-height: 100vh;
  margin: -2rem -1rem;
}
/* 左侧品牌区：深蓝渐变 */
.brand-side {
  flex: 1;
  background: linear-gradient(135deg, #1a2744 0%, #2a3a5c 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem;
}
.brand-content {
  color: white;
  text-align: center;
  max-width: 400px;
}
.brand-icon {
  width: 72px;
  height: 72px;
  margin: 0 auto 1.2rem;
  background: rgba(255,255,255,0.12);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.2rem;
  backdrop-filter: blur(4px);
}
.brand-content h1 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  letter-spacing: 0.5px;
}
.brand-desc {
  font-size: 0.9rem;
  opacity: 0.75;
  line-height: 1.6;
  margin-bottom: 2.2rem;
}
.brand-features {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.8rem;
  margin-bottom: 2rem;
}
.feature {
  background: rgba(255,255,255,0.10);
  padding: 0.7rem 1rem;
  border-radius: 10px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  backdrop-filter: blur(2px);
}
.feature i {
  width: 18px;
  text-align: center;
  font-size: 0.85rem;
  opacity: 0.85;
}
.brand-footer {
  font-size: 0.75rem;
  opacity: 0.4;
  margin-top: 2rem;
}

/* 右侧表单区 */
.form-side {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  padding: 3rem;
}
.form-wrapper {
  width: 100%;
  max-width: 400px;
  padding: 2.5rem 2rem;
}
.form-wrapper h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-heading, #1e293b);
  margin-bottom: 0.3rem;
  text-align: center;
}
.form-sub {
  text-align: center;
  color: var(--text-muted, #94a3b8);
  font-size: 0.9rem;
  margin-bottom: 1.8rem;
}
.login-form {
  margin-top: 0.5rem;
}
.login-btn {
  width: 100%;
  height: 44px;
  font-size: 1rem;
  font-weight: 600;
}
.form-footer {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: var(--text-muted, #94a3b8);
}
.form-footer a {
  color: var(--primary, #3D5A80);
  font-weight: 600;
  transition: color 0.2s;
}
.form-footer a:hover {
  color: var(--primary-dark, #2563eb);
}
.form-footer a i {
  font-size: 0.8rem;
  margin-left: 3px;
}

@media (max-width: 768px) {
  .login-page { flex-direction: column; }
  .brand-side { padding: 2.5rem 1.5rem; }
  .brand-content h1 { font-size: 1.4rem; }
  .form-side { padding: 2rem 1rem; }
  .form-wrapper { padding: 1.8rem 1.2rem; }
}
</style>