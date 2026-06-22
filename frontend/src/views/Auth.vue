<template>
  <div class="auth-page">
    <div class="sign-wrapper">
      <!-- ═══ 品牌 ═══ -->
      <div class="brand-logo-area">
        <div class="brand-title">启途</div>
        <div class="brand-slogan">你的 AI 求职助手</div>
      </div>

      <!-- ═══ 磨砂玻璃卡片 ═══ -->
      <div class="login-card">
        <!-- 小猫 -->
        <img src="/auth-cat.png" class="auth-cat" alt="" />

        <!-- Tab -->
        <div class="auth-tabs">
          <button
            :class="['auth-tab', { active: mode === 'login' }]"
            @click="switchTab('login')"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
            登录
          </button>
          <button
            :class="['auth-tab', { active: mode === 'register' }]"
            @click="switchTab('register')"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>
            注册
          </button>
        </div>

        <!-- ═══ 登录表单 ═══ -->
        <form v-if="mode === 'login'" @submit.prevent="doLogin">
          <div class="form-group">
            <label>用户名</label>
            <input v-model="loginForm.username" type="text" placeholder="请输入用户名" @focus="loginErrors.username = ''" />
          </div>
          <p v-if="loginErrors.username" class="error-msg">{{ loginErrors.username }}</p>

          <div class="form-group">
            <label>密码</label>
            <input v-model="loginForm.password" :type="showPwd ? 'text' : 'password'" placeholder="请输入密码" @focus="loginErrors.password = ''" />
            <span class="password-toggle" @click="showPwd = !showPwd">
              <svg v-if="showPwd" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            </span>
          </div>
          <p v-if="loginErrors.password" class="error-msg">{{ loginErrors.password }}</p>

          <div class="form-options">
            <label class="remember-me">
              <input type="checkbox" v-model="remember" /> 记住我
            </label>
            <span class="forgot-link" @click="ElMessage.info('请联系管理员重置密码')">忘记密码？</span>
          </div>

          <button class="submit-btn" :class="{ loading }" type="submit" :disabled="loading">
            <svg v-if="loading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin" width="16" height="16"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
            <template v-else>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
              立即登录
            </template>
          </button>

          <div class="switch-area">
            还没有账号？<a @click="switchTab('register')">立即注册</a>
          </div>
        </form>

        <!-- ═══ 注册表单 ═══ -->
        <form v-else @submit.prevent="doRegister">
          <div class="form-group">
            <label>用户名</label>
            <input v-model="regForm.username" type="text" placeholder="3位以上字母数字" @focus="regErrors.username = ''" />
          </div>
          <p v-if="regErrors.username" class="error-msg">{{ regErrors.username }}</p>

          <div class="form-group">
            <label>昵称</label>
            <input v-model="regForm.nickname" type="text" placeholder="选填" />
          </div>

          <div class="form-group">
            <label>密码</label>
            <input v-model="regForm.password" :type="showRegPwd ? 'text' : 'password'" placeholder="至少6位" @focus="regErrors.password = ''" />
            <span class="password-toggle" @click="showRegPwd = !showRegPwd">
              <svg v-if="showRegPwd" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            </span>
          </div>
          <p v-if="regErrors.password" class="error-msg">{{ regErrors.password }}</p>

          <div class="form-group">
            <label>确认密码</label>
            <input v-model="regForm.pwd2" :type="showRegPwd ? 'text' : 'password'" placeholder="再次输入密码" @focus="regErrors.pwd2 = ''" />
          </div>
          <p v-if="regErrors.pwd2" class="error-msg">{{ regErrors.pwd2 }}</p>

          <button class="submit-btn" :class="{ loading }" type="submit" :disabled="loading">
            <svg v-if="loading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin" width="16" height="16"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
            <template v-else>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>
              创建账号
            </template>
          </button>

          <div class="switch-area">
            已有账号？<a @click="switchTab('login')">去登录</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const mode = ref('login')
const loading = ref(false)
const showPwd = ref(false)
const showRegPwd = ref(false)
const remember = ref(false)

const loginForm = reactive({ username: '', password: '' })
const loginErrors = reactive({ username: '', password: '' })

const regForm = reactive({ username: '', nickname: '', password: '', pwd2: '' })
const regErrors = reactive({ username: '', password: '', pwd2: '' })

function switchTab(t) {
  mode.value = t
  Object.keys(loginErrors).forEach(k => (loginErrors[k] = ''))
  Object.keys(regErrors).forEach(k => (regErrors[k] = ''))
}

async function doLogin() {
  loginErrors.username = loginErrors.password = ''
  if (!loginForm.username) { loginErrors.username = '请输入用户名'; return }
  if (!loginForm.password) { loginErrors.password = '请输入密码'; return }
  loading.value = true
  try {
    const qs = new URLSearchParams({ username: loginForm.username, password: loginForm.password })
    const res = await fetch('/api/user/login?' + qs, { method: 'POST' })
    if (!res.ok) { const e = await res.json(); throw new Error(e.detail) }
    const data = await res.json()
    localStorage.setItem('token', data.token)
    if (remember.value) localStorage.setItem('user', JSON.stringify(data.user))
    else sessionStorage.setItem('user', JSON.stringify(data.user))
    ElMessage.success(`欢迎回来，${data.user.nickname || data.user.username}！`)
    router.push('/career')
  } catch (e) {
    loginErrors.password = '用户名或密码错误'
  } finally { loading.value = false }
}

async function doRegister() {
  regErrors.username = regErrors.password = regErrors.pwd2 = ''
  if (!regForm.username) { regErrors.username = '请输入用户名'; return }
  if (regForm.username.length < 3) { regErrors.username = '用户名至少3位'; return }
  if (!regForm.password) { regErrors.password = '请输入密码'; return }
  if (regForm.password.length < 6) { regErrors.password = '密码至少6位'; return }
  if (regForm.password !== regForm.pwd2) { regErrors.pwd2 = '两次密码不一致'; return }
  loading.value = true
  try {
    const qs = new URLSearchParams({ username: regForm.username, password: regForm.password, nickname: regForm.nickname || regForm.username })
    const res = await fetch('/api/user/register?' + qs, { method: 'POST' })
    if (!res.ok) { const e = await res.json(); throw new Error(e.detail) }
    ElMessage.success('注册成功，请登录')
    loginForm.username = regForm.username
    switchTab('login')
  } catch (e) { regErrors.username = e.message || '注册失败' }
  finally { loading.value = false }
}
</script>

<style scoped>
/* ═══ 页面 — 全屏背景图 ═══ */
.auth-page {
  min-height: 100vh;
  width: 100%;
  background: url('/auth-bg-watercolor-clean.png') center/cover no-repeat fixed;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

/* ═══ 微遮罩（几乎不压暗） ═══ */
.auth-page::before {
  content: '';
  position: fixed; inset:0;
  background: rgba(0,0,0,0.05);
  z-index: 0;
}

/* ═══ 外层容器 ═══ */
.sign-wrapper {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 20px;
}

/* ═══ 品牌 ═══ */
.brand-logo-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 26px;
}
.brand-title {
  font-size: 52px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 10px;
  line-height: 1;
  text-shadow: 0 2px 8px rgba(0,0,0,0.12);
}
.brand-slogan {
  font-size: 16px;
  color: rgba(255,255,255,0.75);
  margin-top: 10px;
  text-shadow: 0 1px 4px rgba(0,0,0,0.08);
}

/* ═══ 磨砂玻璃卡片 ═══ */
.login-card {
  width: 460px;
  max-width: 100%;
  background: rgba(255,255,255,0.05);
  border-radius: 14px;
  padding: 28px 30px 0;
  box-shadow: 0 8px 32px rgba(0,0,0,0.45);
  position: relative;
  border: 1px solid rgba(255,255,255,0.35);
}

/* ═══ 小猫 ═══ */
.auth-cat {
  position: absolute;
  top: -66px;
  right: 10px;
  width: 86px;
  z-index: 5;
  pointer-events: none;
}

/* ═══ Tab 切换 ═══ */
.auth-tabs {
  display: flex;
  gap: 0;
  margin-bottom: 22px;
  background: rgba(255,255,255,0.3);
  border-radius: 10px;
  padding: 4px;
}
.auth-tab {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 15px;
  font-weight: 500;
  height: 40px;
  border: none;
  background: transparent;
  border-radius: 8px;
  color: rgba(25,27,31,0.55);
  cursor: pointer;
  font-family: inherit;
  transition: all .2s;
}
.auth-tab.active {
  background: #fff;
  color: #191b1f;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.auth-tab:hover:not(.active) { color: #191b1f; }

/* ═══ 表单字段 ═══ */
.form-group {
  margin-bottom: 18px;
  position: relative;
}
.form-group label {
  display: block;
  font-size: 14px;
  color: #191b1f;
  margin-bottom: 6px;
  font-weight: 500;
}
.form-group input {
  width: 100%;
  padding: 10px 0;
  border: none;
  border-bottom: 1px solid rgba(235,236,237,0.7);
  font-size: 15px;
  color: #373a40;
  outline: none;
  background: transparent;
  font-family: inherit;
  border-radius: 0;
  transition: border-color .2s;
}
.form-group input:focus {
  border-bottom-color: #1772f6;
}
.form-group input::placeholder { color: #adb0b7; }

.password-toggle {
  position: absolute;
  right: 0;
  bottom: 10px;
  cursor: pointer;
  color: #8590a6;
  display: flex;
  align-items: center;
  padding: 2px;
  transition: color .2s;
}
.password-toggle:hover { color: #1772f6; }

.error-msg {
  color: #e54d4d;
  font-size: 13px;
  margin: -12px 0 8px 0;
  line-height: 1.4;
}

/* ═══ 选项 ═══ */
.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 2px 0 20px;
  font-size: 14px;
}
.remember-me {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #8590a6;
  cursor: pointer;
}
.remember-me input { accent-color: #1772f6; }
.forgot-link { color: #8590a6; cursor: pointer; font-size: 14px; }
.forgot-link:hover { color: #1772f6; }

/* ═══ 按钮 ═══ */
.submit-btn {
  width: 100%;
  height: 42px;
  border: none;
  border-radius: 8px;
  background: #1772f6;
  color: #fff;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  font-family: inherit;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  transition: background .2s;
}
.submit-btn:hover:not(:disabled) { background: #1560d4; }
.submit-btn:disabled { opacity: 0.7; cursor: not-allowed; }
.submit-btn svg { flex-shrink: 0; }

/* ═══ 底部切换 ═══ */
.switch-area {
  text-align: center;
  padding: 16px 0;
  margin: 20px -30px 0;
  border-top: 1px solid rgba(235,236,237,0.4);
  font-size: 14px;
  color: #8590a6;
}
.switch-area a {
  color: #09408e;
  cursor: pointer;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}
.switch-area a:hover { text-decoration: underline; }

.spin { animation: spin 1s linear infinite; }
@keyframes spin { to{transform:rotate(360deg)} }

/* ═══ 响应式 ═══ */
@media (max-width: 600px) {
  .login-card {
    padding: 24px 20px 0;
  }
  .brand-title {
    font-size: 38px;
    letter-spacing: 6px;
  }
  .switch-area {
    margin: 18px -20px 0;
  }
  .auth-cat {
    width: 70px;
    top: -56px;
    right: 6px;
  }
}
</style>