<template>
  <div class="register-page">
    <!-- 左侧品牌区 -->
    <div class="brand-side">
      <div class="brand-content">
        <div class="brand-icon">🎯</div>
        <h1>多模态AI求职助手</h1>
        <p class="brand-desc">注册账号，开启你的智能求职之旅</p>
        <div class="brand-features">
          <div class="feature"><span>🔍</span> 发现适合你的职业方向</div>
          <div class="feature"><span>🎤</span> AI面试官仿真模拟</div>
          <div class="feature"><span>📝</span> 智能生成专业简历</div>
          <div class="feature"><span>📊</span> 精准匹配对口企业</div>
        </div>
        <p class="brand-footer">第八组 · 2025</p>
      </div>
    </div>

    <!-- 右侧注册区 -->
    <div class="form-side">
      <div class="form-card">
        <div class="form-header">
          <h2>创建账号</h2>
          <p class="form-sub">填写信息，开始你的求职之旅</p>
        </div>
        <el-form :model="form" size="large" class="register-form">
          <el-form-item>
            <el-input v-model="form.username" placeholder="用户名（3-20位字母数字）" prefix-icon="User" />
          </el-form-item>
          <el-form-item>
            <el-input v-model="form.nickname" placeholder="昵称（给自己取个名字）" prefix-icon="EditPen" />
          </el-form-item>
          <el-form-item>
            <el-input v-model="form.password" type="password" placeholder="密码（至少6位）" show-password prefix-icon="Lock" />
          </el-form-item>
          <el-form-item>
            <el-input v-model="form.pwd2" type="password" placeholder="确认密码" show-password prefix-icon="Lock" @keyup.enter="doRegister" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="doRegister" :loading="loading" class="register-btn">注 册</el-button>
          </el-form-item>
        </el-form>
        <div class="form-footer">
          已有账号？<router-link to="/login">去登录 →</router-link>
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
const form = reactive({ username:'', nickname:'', password:'', pwd2:'' })

async function doRegister() {
  if (!form.username || !form.password) return ElMessage.warning('请填写完整')
  if (form.password !== form.pwd2) return ElMessage.warning('两次密码不一致')
  if (form.password.length < 6) return ElMessage.warning('密码至少6位')
  loading.value = true
  try {
    const qs = new URLSearchParams({ username:form.username, password:form.password, nickname:form.nickname||form.username })
    const res = await fetch('/api/user/register?' + qs, { method:'POST' })
    if (!res.ok) { const e = await res.json(); throw new Error(e.detail) }
    ElMessage.success('注册成功，请登录！')
    router.push('/login')
  } catch(e) {
    ElMessage.error(e.message || '注册失败')
  } finally { loading.value = false }
}
</script>

<style scoped>
.register-page {
  display: flex;
  min-height: 100vh;
  margin: -2rem -1rem;
}

/* ===== 左侧品牌区 ===== */
.brand-side {
  flex: 1;
  background: linear-gradient(135deg, #1a2744 0%, #2a3a5c 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  position: relative;
  overflow: hidden;
}

.brand-side::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at 30% 40%, rgba(255,255,255,0.04) 0%, transparent 60%);
  pointer-events: none;
}

.brand-content {
  color: white;
  text-align: center;
  max-width: 400px;
  position: relative;
  z-index: 1;
}

.brand-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  filter: drop-shadow(0 4px 12px rgba(0,0,0,0.2));
}

.brand-content h1 {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  letter-spacing: 0.02em;
}

.brand-desc {
  font-size: 0.95rem;
  opacity: 0.8;
  line-height: 1.6;
  margin-bottom: 2.5rem;
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 2.5rem;
}

.feature {
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(4px);
  padding: 0.7rem 1.2rem;
  border-radius: 10px;
  font-size: 0.9rem;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background 0.2s;
}

.feature:hover {
  background: rgba(255,255,255,0.18);
}

.feature span {
  font-size: 1.1rem;
}

.brand-footer {
  font-size: 0.75rem;
  opacity: 0.45;
  margin-top: 2rem;
}

/* ===== 右侧表单区 ===== */
.form-side {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  padding: 3rem;
}

.form-card {
  width: 100%;
  max-width: 400px;
  background: #ffffff;
  border-radius: 16px;
  padding: 2.5rem 2rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.06), 0 1px 4px rgba(0,0,0,0.04);
}

.form-header {
  margin-bottom: 1.5rem;
}

.form-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1a2744;
  margin-bottom: 0.25rem;
  text-align: center;
}

.form-sub {
  text-align: center;
  color: #8e99b0;
  font-size: 0.9rem;
}

.register-form {
  margin-top: 0.5rem;
}

.register-form :deep(.el-input__wrapper) {
  border-radius: 10px;
  box-shadow: 0 0 0 1px #e2e6ee inset;
  transition: box-shadow 0.2s;
}

.register-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #c0c8da inset;
}

.register-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px #2a3a5c inset;
}

.register-form :deep(.el-input__prefix) {
  color: #8e99b0;
}

.register-btn {
  width: 100%;
  height: 46px;
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  border-radius: 10px;
  background: linear-gradient(135deg, #1a2744 0%, #2a3a5c 100%);
  border: none;
  transition: opacity 0.2s, transform 0.1s;
}

.register-btn:hover {
  opacity: 0.92;
  transform: translateY(-1px);
}

.register-btn:active {
  transform: translateY(0);
}

.form-footer {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
  color: #8e99b0;
}

.form-footer a {
  color: #1a2744;
  font-weight: 600;
  text-decoration: none;
  transition: opacity 0.2s;
}

.form-footer a:hover {
  opacity: 0.75;
}

/* ===== 响应式 ===== */
@media (max-width: 768px) {
  .register-page {
    flex-direction: column;
  }

  .brand-side {
    padding: 2rem 1.5rem;
  }

  .brand-content h1 {
    font-size: 1.4rem;
  }

  .brand-features {
    max-width: 320px;
    margin-left: auto;
    margin-right: auto;
  }

  .form-side {
    padding: 2rem 1rem;
  }

  .form-card {
    padding: 2rem 1.5rem;
    border-radius: 12px;
  }
}
</style>