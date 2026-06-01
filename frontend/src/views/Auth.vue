<template>
  <div class="auth-page">
    <!-- ═══ 背景云朵装饰 ═══ -->
    <div class="auth-sky">
      <div class="sky-cloud ac-1"></div>
      <div class="sky-cloud ac-2"></div>
      <div class="sky-cloud ac-3"></div>
      <div class="sky-cloud ac-4"></div>
      <div class="sky-cloud ac-5"></div>
      <div class="sky-cloud ac-6"></div>
    </div>

    <!-- ═══ 左侧品牌区（不动） ═══ -->
    <div class="brand-panel">
      <div class="brand-content">
        <div class="brand-logo">
          <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="22" height="22">
            <circle cx="12" cy="12" r="10"/>
            <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>
          </svg>
        </div>
        <h1 class="brand-title">启途</h1>
        <p class="brand-sub">QITU · AI 求职助手</p>
        <p class="brand-tagline">探索职业方向 · 模拟面试实战<br>优化简历排版 · 精准投递追踪</p>
        <div class="brand-features">
          <div class="brand-feature-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14">
              <circle cx="12" cy="12" r="10"/>
              <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>
            </svg>
            <span>职业探索</span>
          </div>
          <div class="brand-feature-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14">
              <rect x="9" y="2" width="6" height="11" rx="3"/>
              <path d="M5 10a7 7 0 0 0 14 0"/>
              <line x1="12" y1="19" x2="12" y2="23"/>
              <line x1="8" y1="23" x2="16" y2="23"/>
            </svg>
            <span>面试模拟</span>
          </div>
          <div class="brand-feature-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
              <line x1="8" y1="13" x2="16" y2="13"/>
              <line x1="8" y1="17" x2="12" y2="17"/>
            </svg>
            <span>简历优化</span>
          </div>
          <div class="brand-feature-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14">
              <line x1="22" y1="2" x2="11" y2="13"/>
              <polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
            <span>投递助手</span>
          </div>
        </div>
        <div class="brand-quote">「每一步，都有启途帮你」</div>
      </div>
    </div>

    <!-- ═══ 右侧淡灰底 + 白卡片表单 ═══ -->
    <div class="form-panel">
      <div class="auth-welcome">
        <h2>欢迎回来</h2>
        <p>登录你的账户，继续求职之旅</p>
      </div>

      <div class="form-card">
        <img src="/src/assets/auth-cat.png" class="auth-cat" alt="" />
        <div class="auth-tabs">
          <button :class="['auth-tab', { active: mode === 'login' }]" @click="switchTab('login')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
            登录
          </button>
          <button :class="['auth-tab', { active: mode === 'register' }]" @click="switchTab('register')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>
            注册
          </button>
        </div>

        <div v-if="mode === 'login'" class="form-fields">
          <div class="form-field" :class="{ error: loginErrors.username }">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inp-icon"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <input v-model="loginForm.username" placeholder="用户名" @focus="loginErrors.username = ''" @keyup.enter="doLogin" />
          </div>
          <p v-if="loginErrors.username" class="error-msg"><svg viewBox="0 0 24 24" fill="none" stroke="#f56c6c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg> {{ loginErrors.username }}</p>

          <div class="form-field" :class="{ error: loginErrors.password }">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inp-icon"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            <input v-model="loginForm.password" :type="showPwd ? 'text' : 'password'" placeholder="密码" @focus="loginErrors.password = ''" @keyup.enter="doLogin" />
            <span class="password-toggle" @click="showPwd = !showPwd">
              <svg v-if="showPwd" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            </span>
          </div>
          <p v-if="loginErrors.password" class="error-msg"><svg viewBox="0 0 24 24" fill="none" stroke="#f56c6c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg> {{ loginErrors.password }}</p>

          <div class="form-options">
            <label class="remember-me">
              <input type="checkbox" v-model="remember" />
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="17" height="17" :class="['cb-icon', { checked: remember }]"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
              记住我
            </label>
            <span class="forgot-link" @click="ElMessage.info('请联系管理员重置密码')">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>
              忘记密码？
            </span>
          </div>

          <button class="submit-btn" :class="{ loading }" @click="doLogin" :disabled="loading">
            <svg v-if="loading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin" width="16" height="16"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
            <template v-else>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
              立即登录
            </template>
          </button>

          <p class="switch-prompt">还没有账号？<span @click="switchTab('register')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>
            立即注册</span>
          </p>
        </div>

        <div v-else class="form-fields">
          <div class="form-field" :class="{ error: regErrors.username }">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inp-icon"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <input v-model="regForm.username" placeholder="用户名" @focus="regErrors.username = ''" />
          </div>
          <p v-if="regErrors.username" class="error-msg"><svg viewBox="0 0 24 24" fill="none" stroke="#f56c6c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg> {{ regErrors.username }}</p>

          <div class="form-field">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inp-icon"><rect x="2" y="4" width="20" height="16" rx="2"/><line x1="8" y1="9" x2="14" y2="9"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="12" y2="17"/></svg>
            <input v-model="regForm.nickname" placeholder="昵称（选填）" />
          </div>

          <div class="form-field" :class="{ error: regErrors.password }">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inp-icon"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
            <input v-model="regForm.password" :type="showRegPwd ? 'text' : 'password'" placeholder="密码（至少6位）" @focus="regErrors.password = ''" />
            <span class="password-toggle" @click="showRegPwd = !showRegPwd">
              <svg v-if="showRegPwd" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/><path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
              <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            </span>
          </div>
          <p v-if="regErrors.password" class="error-msg"><svg viewBox="0 0 24 24" fill="none" stroke="#f56c6c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg> {{ regErrors.password }}</p>

          <div class="form-field" :class="{ error: regErrors.pwd2 }">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inp-icon"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>
            <input v-model="regForm.pwd2" :type="showRegPwd ? 'text' : 'password'" placeholder="确认密码" @focus="regErrors.pwd2 = ''" @keyup.enter="doRegister" />
          </div>
          <p v-if="regErrors.pwd2" class="error-msg"><svg viewBox="0 0 24 24" fill="none" stroke="#f56c6c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg> {{ regErrors.pwd2 }}</p>

          <button class="submit-btn" :class="{ loading }" @click="doRegister" :disabled="loading">
            <svg v-if="loading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin" width="16" height="16"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
            <template v-else>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>
              创建账号
            </template>
          </button>

          <p class="switch-prompt">已有账号？<span @click="switchTab('login')">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
            去登录</span>
          </p>
        </div>
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
    if (data.needs_profile) {
      localStorage.setItem('needs_profile', 'true')
      ElMessage.info('首次登录，请先完善基础信息～')
      router.push('/profile-setup')
    } else {
      localStorage.removeItem('needs_profile')
      ElMessage.success(`欢迎回来，${data.user.nickname || data.user.username}！`)
      router.push('/career')
    }
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
/* ═══ 页面布局 ═══ */
.auth-page {
  display: flex;
  min-height: 100vh;
  width: 100%;
  position: relative;
  background: linear-gradient(180deg,#6FA3C8 0%,#8DB8D8 25%,#B0D0E4 50%,#D0E4F0 75%,#E8F0F5 100%);
  overflow: hidden;
}

/* ═══ 背景云朵 ═══ */
.auth-sky {
  position: absolute; inset:0;
  pointer-events:none; overflow:hidden;
}
.auth-sky .sky-cloud {
  position:absolute; border-radius:50%;
  background:rgba(255,255,255,.45); filter:blur(40px);
  will-change:transform;
}
.ac-1 { width:500px; height:120px; top:5%; left:-8%; animation:cloudA 120s linear infinite; }
.ac-2 { width:400px; height:100px; top:15%; left:40%; animation:cloudB 140s linear infinite; }
.ac-3 { width:350px; height:85px; top:55%; left:65%; animation:cloudA 100s linear infinite; }
.ac-4 { width:300px; height:70px; top:70%; left:20%; animation:cloudB 90s linear infinite; }
.ac-5 { width:180px; height:45px; top:40%; left:80%; animation:cloudA 70s linear infinite; }
.ac-6 { width:250px; height:60px; top:80%; left:-5%; animation:cloudB 85s linear infinite; }
@keyframes cloudA { 0%{transform:translateX(0)} 100%{transform:translateX(1200px)} }
@keyframes cloudB { 0%{transform:translateX(0)} 100%{transform:translateX(1000px)} }

/* ═══ 左侧品牌区 ═══ */
.brand-panel {
  width: 35%;
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(155deg, rgba(61,90,128,.88) 0%, rgba(74,107,148,.72) 60%, rgba(142,160,184,.55) 100%);
  backdrop-filter: blur(4px);
}
.brand-content {
  position:relative; z-index:1; text-align:center;
  color:#fff; padding:2rem; display:flex;
  flex-direction:column; align-items:center;
}
.brand-logo {
  width:56px; height:56px; border-radius:16px;
  background:rgba(255,255,255,.15); backdrop-filter:blur(8px);
  display:flex; align-items:center; justify-content:center;
  margin-bottom:8px;
}
.brand-title { font-size:2.2rem; font-weight:800; letter-spacing:6px; margin-bottom:2px; text-shadow:0 2px 12px rgba(0,0,0,.08); }
.brand-sub { font-size:.78rem; color:rgba(255,255,255,.55); letter-spacing:4px; margin-bottom:14px; }
.brand-tagline { font-size:.85rem; color:rgba(255,255,255,.75); line-height:1.7; max-width:240px; margin:0 auto 24px; }
.brand-features { display:flex; flex-wrap:wrap; justify-content:center; gap:8px 14px; margin-bottom:20px; }
.brand-feature-item { display:flex; align-items:center; gap:6px; font-size:.8rem; color:rgba(255,255,255,.7); background:rgba(255,255,255,.1); padding:5px 12px; border-radius:20px; backdrop-filter:blur(4px); border:1px solid rgba(255,255,255,.06); }
.brand-feature-item svg { color:#8EA0B8; flex-shrink:0; }
.brand-quote { font-size:.82rem; color:rgba(255,255,255,.4); font-style:italic; letter-spacing:1px; margin-top:6px; }

/* ═══ 表单上方趴边猫 ═══ */
.auth-cat {
  position: absolute;
  top: -70px;
  right: 20px;
  width: 90px;
  z-index: 5;
  pointer-events: none;
}

.auth-box {
  width: 100%;
  max-width: 480px;
}

/* ═══ 白色卡片 ═══ */
.form-card {
  width: 100%;
  max-width: 480px;
  background: #ffffff;
  border-radius: 18px;
  padding: 2.4rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, .08);
  position: relative;
  animation: fadeIn .3s ease;
}

/* ═══ 右侧 — 淡灰底 ═══ */
.form-panel {
  flex: 1;
  position: relative;
  z-index: 1;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* ═══ 白色区域左上角的欢迎文字 ═══ */
.auth-welcome {
  position: absolute;
  top: 4.5rem;
  left: 3.5rem;
  text-align: left;
  z-index: 2;
}
.auth-welcome h2 {
  font-size: 2.6rem;
  font-weight: 800;
  color: #1a2744;
  margin: 0 0 6px 0;
}
.auth-welcome p {
  font-size: 1.1rem;
  color: #8EA0B8;
  margin: 0;
}

@keyframes fadeIn { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }

/* ═══ Tab ═══ */
.auth-tabs {
  display:flex; margin-bottom:1.8rem; gap:2px;
  background:rgba(240,242,246,.8); border-radius:12px;
  padding:4px; border:1px solid rgba(0,0,0,.03);
}
.auth-tab {
  flex:1; display:flex; align-items:center; justify-content:center;
  gap:.4rem; background:transparent; border:none;
  font-size:1rem; color:#8EA0B8;
  cursor:pointer; padding:.75rem 0;
  font-weight:500; border-radius:9px;
  transition:all .25s ease;
}
.auth-tab svg { flex-shrink:0; }
.auth-tab.active { background:#fff; color:#3D5A80; font-weight:600; box-shadow:0 1px 4px rgba(61,90,128,.08); }
.auth-tab:hover:not(.active) { color:#3D5A80; }

/* ═══ 表单字段 ═══ */
.form-fields { width: 100%; }

.form-field {
  display:flex; align-items:center;
  background:#fff; border:1.5px solid #D8DCE6; border-radius:12px;
  padding:0 1.1rem; margin-bottom:.6rem;
  transition:border-color .2s, box-shadow .2s;
}
.form-field:focus-within { border-color:#3D5A80; box-shadow:0 0 0 3px rgba(61,90,128,.08); }
.form-field.error { border-color:#f56c6c; }

.inp-icon {
  width:18px; height:18px; color:#8EA0B8; flex-shrink:0; margin-right:.75rem;
  transition:color .2s;
}
.form-field:focus-within .inp-icon { color:#3D5A80; }

.form-field input {
  flex:1; border:none; outline:none; font-size:1rem;
  padding:.95rem 0; background:transparent; color:#4A5568;
}
.form-field input::placeholder { color:#9AAEC2; }
.password-toggle { cursor:pointer; color:#8EA0B8; flex-shrink:0; transition:color .2s; padding:.3rem; display:flex; align-items:center; }
.password-toggle:hover { color:#3D5A80; }
.error-msg { color:#f56c6c; font-size:.8rem; margin:-.2rem 0 .6rem .3rem; display:flex; align-items:center; gap:.3rem; }

.form-options { display:flex; justify-content:space-between; align-items:center; margin:.8rem 0 1.4rem; font-size:.85rem; color:#8EA0B8; }
.remember-me { display:flex; align-items:center; gap:.4rem; cursor:pointer; user-select:none; }
.remember-me input { display:none; }
.cb-icon { color:#BFA895; transition:color .2s; flex-shrink:0; }
.cb-icon.checked { color:#3D5A80; }
.forgot-link { cursor:pointer; color:#8EA0B8; display:flex; align-items:center; gap:.3rem; transition:opacity .2s; }
.forgot-link:hover { color:#3D5A80; }

.submit-btn {
  width:100%; padding:.95rem; border:none; border-radius:12px;
  background:linear-gradient(135deg,#3D5A80,#2C4460);
  color:#fff; font-size:1rem; font-weight:600;
  cursor:pointer; transition:transform .15s, box-shadow .2s, opacity .2s;
  display:flex; align-items:center; justify-content:center; gap:.4rem;
}
.submit-btn:hover:not(:disabled) { transform:translateY(-1px); box-shadow:0 6px 20px rgba(61,90,128,.25); }
.submit-btn:disabled { opacity:.7; cursor:not-allowed; }
.submit-btn.loading { pointer-events:none; }
.submit-btn svg { flex-shrink:0; }

.switch-prompt { text-align:center; margin-top:1.5rem; font-size:.85rem; color:#8EA0B8; }
.switch-prompt span { color:#3D5A80; cursor:pointer; font-weight:500; display:inline-flex; align-items:center; gap:.3rem; transition:opacity .2s; }
.switch-prompt span:hover { opacity:.8; text-decoration:underline; }

.spin { animation: spin 1s linear infinite; }
@keyframes spin { to{transform:rotate(360deg)} }

/* ═══ 响应式 ═══ */
@media (max-width:1100px) {
  .brand-panel { width: 32%; }
}
@media (max-width:900px) {
  .auth-page { flex-direction: column; }
  .brand-panel { width:100%; min-height:170px; }
  .brand-title { font-size:1.6rem; }
  .form-panel { padding:2rem 1rem; }
  .auth-welcome { position: static; text-align: center; margin-bottom: 1rem; }
  .form-card { max-width:480px; }
}
@media (max-width:480px) {
  .brand-panel { min-height:140px; }
  .form-card { padding:1.6rem 1.2rem; }
  .auth-tab { font-size:.9rem; padding:.6rem 0; }
  .form-field input { font-size:.95rem; padding:.8rem 0; }
  .submit-btn { padding:.8rem; font-size:.95rem; }
}
</style>