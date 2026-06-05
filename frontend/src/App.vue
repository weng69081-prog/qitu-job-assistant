<template>
  <!-- 独立页面（填资料、面试会话等）：不裹导航 -->
  <div v-if="token && isStandalone" class="layout-root standalone">
    <router-view />
  </div>

  <!-- 已登录 + 非独立：标准布局 (对比3排版) -->
  <div v-else-if="token" class="layout-root">
    <!-- ═══ 顶部导航栏 (对比3：深色渐变 + 水平导航) ═══ -->
    <header class="app-topbar">
      <div class="topbar-left">
        <router-link to="/landing" class="brand-link">
          <div class="brand-logo">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </div>
          <div class="brand-text">
            <span class="brand-name">启途</span>
            <span class="brand-sub">QITU</span>
          </div>
        </router-link>
        <!-- 水平导航（对比3：在topbar内水平排列） -->
        <nav class="topbar-nav">
          <router-link to="/dashboard" class="tn-item" active-class="tn-active"><LayoutDashboard :size="16" class="icon-blue" /> 首页</router-link>
          <router-link to="/career" class="tn-item" active-class="tn-active"><Compass :size="16" class="icon-blue" /> 职业探索</router-link>
          <router-link to="/interview" class="tn-item" active-class="tn-active"><Mic :size="16" class="icon-blue" /> 面试模拟</router-link>
          <router-link to="/exam-practice" class="tn-item" active-class="tn-active"><Pen :size="16" class="icon-blue" /> 笔试</router-link>
          <router-link to="/resume" class="tn-item" active-class="tn-active"><FileText :size="16" class="icon-blue" /> 简历</router-link>
          <router-link to="/delivery-assistant" class="tn-item" active-class="tn-active"><Send :size="16" class="icon-blue" /> 投递</router-link>
        </nav>
      </div>
      <div class="topbar-right">
        <div class="search-box">
          <Search :size="16" class="icon-blue" />
          <input
            type="text"
            v-model="searchQuery"
            placeholder="搜索职业、岗位、面试题..."
            @keyup.enter="doSearch"
          />
        </div>
        <router-link to="/settings" class="settings-btn" title="设置"><Settings :size="16" class="icon-blue" /></router-link>
        <div class="user-avatar" :style="avatarStyle">{{ (userDisplay.nickname || userDisplay.username || '同')[0] }}</div>
        <span class="user-name">{{ userDisplay.nickname || userDisplay.username || '同学' }}</span>
      </div>
    </header>

    <!-- ═══ 主内容区域（无sidebar，全宽） ═══ -->
    <main class="app-main">
      <router-view />
    </main>
    <AiAssistant />
  </div>

  <!-- 未登录：全屏 -->
  <div v-else class="layout-root guest">
    <router-view />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AiAssistant from './components/AiAssistant.vue'

const route = useRoute()
const token = ref(null)
const userDisplay = ref({})
const searchQuery = ref('')
const isStandalone = computed(() => route.meta?.standalone === true)

// 头像：如果有 base64 就显示图片，否则只显示文字
const avatarDataUrl = ref(localStorage.getItem('user_avatar') || '')
const avatarStyle = computed(() => {
  if (avatarDataUrl.value) {
    return {
      backgroundImage: `url(${avatarDataUrl.value})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      color: 'transparent',
    }
  }
  return {}
})
// 定时检查头像更新（从设置页切回来时）
let avatarCheckTimer
onMounted(() => {
  avatarCheckTimer = window.setInterval(() => {
    const stored = localStorage.getItem('user_avatar')
    if (stored && stored !== avatarDataUrl.value) {
      avatarDataUrl.value = stored
    }
  }, 2000)
})

function doSearch() {
  const q = searchQuery.value.trim()
  if (!q) return
  // 导航到投递助手页并携带搜索词（该页面支持 keyword 搜索）
  window.location.href = `/delivery-assistant?search=${encodeURIComponent(q)}`
}

watch(() => route.path, () => {
  token.value = localStorage.getItem('token')
  const u = localStorage.getItem('user') || sessionStorage.getItem('user')
  if (u) { try { userDisplay.value = JSON.parse(u) } catch(e) { userDisplay.value = {} } }
}, { immediate: true })
</script>

<style>
/* ══════════════════════════════════════════════════════════════
   启途 — GLOBAL DESIGN SYSTEM
   学者灰蓝系 · 对比3排版
   ══════════════════════════════════════════════════════════════ */

/* ── CSS Variables ── */
:root {
  /* 学者灰蓝系 五色 */
  --clr-base: #f0f2f6;
  --clr-primary: #3D5A80;
  --clr-secondary: #BFA895;
  --clr-muted: #8EA0B8;
  --clr-accent: #C85A20;

  /* Primary 派生 */
  --primary: var(--clr-primary);
  --primary-light: #54759C;
  --primary-dark: #2C4460;
  --primary-bg: rgba(61, 90, 128, 0.08);
  --primary-gradient: linear-gradient(135deg, #3D5A80, #2C4460);

  /* Accent 派生 */
  --accent: var(--clr-accent);
  --accent-bg: rgba(200, 90, 32, 0.08);
  --accent-gradient: linear-gradient(135deg, #C85A20, #B54E1A);

  /* Backgrounds */
  --bg-body: #f0f2f6;
  --bg-card: #FFFFFF;
  --bg-alt: #E8ECF2;
  --bg-hover: #F4F6F9;

  /* Text */
  --text-heading: #2C3E50;
  --text-body: #4A5568;
  --text-muted: var(--clr-muted);
  --text-light: var(--clr-secondary);

  /* Borders */
  --border: #D8DCE6;
  --border-light: #E8ECF2;

  /* Shadows */
  --shadow-sm: 0 1px 3px rgba(61, 90, 128, 0.06);
  --shadow-md: 0 4px 12px rgba(61, 90, 128, 0.08);
  --shadow-lg: 0 8px 24px rgba(61, 90, 128, 0.1);
  --shadow-hover: 0 12px 32px rgba(61, 90, 128, 0.12);

  /* Radius */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-xl: 20px;

  /* Layout */
  --topbar-height: 68px;
}

/* ── Reset & Base ── */
*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
html { font-size: 15px; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif;
  background: var(--bg-body);
  color: var(--text-body);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
a { text-decoration:none; color:inherit; }
ul { list-style:none; }

/* ── Element Plus 主题覆盖 ── */
.el-button--primary { --el-button-bg-color: var(--primary); --el-button-border-color: var(--primary); --el-button-hover-bg-color: var(--primary-dark); --el-button-hover-border-color: var(--primary-dark); --el-button-active-bg-color: var(--primary-dark); }
.el-button--primary.is-plain { --el-button-bg-color: var(--primary-bg); --el-button-border-color: #C8D4E0; --el-button-text-color: var(--primary); }
.el-button--primary.is-plain:hover { --el-button-bg-color: #DCE4EE; --el-button-border-color: var(--primary); }
.el-button--warning { --el-button-bg-color: var(--accent); --el-button-border-color: var(--accent); --el-button-text-color: #fff; --el-button-hover-bg-color: #B54E1A; }
.el-card { border-radius: var(--radius-md) !important; border: 1px solid var(--border) !important; }
.el-tag--primary { --el-tag-bg-color: var(--primary-bg); --el-tag-border-color: #C8D4E0; --el-tag-text-color: var(--primary); }
.el-tag--success { --el-tag-bg-color: #ECFDF5; --el-tag-border-color: #A7F3D0; --el-tag-text-color: #059669; }
.el-tag--warning { --el-tag-bg-color: #FFFBEB; --el-tag-border-color: #FDE68A; --el-tag-text-color: #D97706; }
.el-tag--danger { --el-tag-bg-color: #FEF2F2; --el-tag-border-color: #FECACA; --el-tag-text-color: #DC2626; }
.el-tag--info { --el-tag-bg-color: var(--bg-alt); --el-tag-border-color: var(--border-light); --el-tag-text-color: var(--text-muted); }
.el-select { --el-select-input-focus-border-color: var(--primary); }
.el-input__wrapper.is-focus { box-shadow: 0 0 0 2px rgba(61, 90, 128, 0.15) !important; }
.el-radio-button__inner { border-color: var(--border) !important; color: var(--text-body) !important; }
.el-radio-button.is-active .el-radio-button__inner { background: var(--primary) !important; border-color: var(--primary) !important; color: #fff !important; }
.el-progress-bar__inner { background: var(--primary-gradient) !important; }
.el-divider--vertical { border-color: var(--border) !important; }
.el-message { border-radius: var(--radius-md) !important; }
.el-dialog { border-radius: var(--radius-lg) !important; }

/* ── Layout Root ── */
.layout-root { min-height:100vh; }
.layout-root.standalone, .layout-root.guest { min-height:100vh; display:flex; background:var(--bg-body); }

/* ═══════ Topbar (对比3：深色渐变 + 水平导航) ═══════ */
.app-topbar {
  height: var(--topbar-height);
  background: var(--primary-gradient);
  box-shadow: 0 2px 12px rgba(0,0,0,.25);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  position: sticky;
  top: 0;
  z-index: 100;
}

/* 左侧：品牌 + 水平导航 */
.topbar-left { display:flex; align-items:center; gap:8px; }
.brand-link { display:flex; align-items:center; gap:10px; margin-right:8px; }
.brand-logo {
  width: 36px; height: 36px;
  background: rgba(255,255,255,.12);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
  backdrop-filter: blur(4px);
}
.brand-text { display:flex; flex-direction:column; }
.brand-name { font-size:18px; font-weight:700; color: #fff; letter-spacing:2px; }
.brand-sub { font-size:9px; color: rgba(255,255,255,.4); letter-spacing:2.5px; margin-top:-2px; text-transform:uppercase; }

/* 水平导航（对比3核心特征） */
.topbar-nav { display:flex; align-items:center; gap:2px; margin-left:10px; }
.tn-item {
  display:flex; align-items:center; gap:6px;
  padding: 6px 12px;
  font-size: 13px;
  color: rgba(255,255,255,.6);
  border-radius: 6px;
  transition: all 0.2s;
  white-space: nowrap;
}
.tn-item i { font-size: 12px; }
.tn-item:hover {
  background: rgba(59,130,246,.15);
  color: #fff;
}
.tn-active, .tn-active:hover {
  background: rgba(59,130,246,.25);
  color: #fff;
  font-weight: 500;
}

/* 右侧：搜索 + 设置 + 通知 + 用户 */
.topbar-right { display:flex; align-items:center; gap:14px; }
.search-box {
  display:flex; align-items:center;
  background: rgba(255,255,255,.08);
  border: 1px solid rgba(255,255,255,.06);
  border-radius: 8px;
  padding: 0 4px 0 12px;
  height: 34px;
  width: 220px;
  transition: all 0.3s;
}
.search-box:focus-within {
  border-color: rgba(59,130,246,.4);
  width: 260px;
  background: rgba(255,255,255,.12);
}
.search-box i { font-size:13px; color: rgba(255,255,255,.3); margin-right:6px; }
.search-box input {
  background:none; border:none; outline:none;
  color: rgba(255,255,255,.8); font-size:13px; flex:1;
}
.search-box input::placeholder { color: rgba(255,255,255,.3); }
.settings-btn {
  color: rgba(255,255,255,.4); font-size:16px; cursor:pointer;
  transition: color 0.2s;
}
.settings-btn:hover { color: #fff; }
.user-avatar {
  width: 32px; height: 32px; border-radius: 50%;
  background: rgba(59,130,246,.5);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 13px; font-weight: 600;
  cursor: pointer;
  border: 1px solid rgba(255,255,255,.1);
}
.user-name { font-size:13px; color: rgba(255,255,255,.5); }

/* ═══ Main Content（无sidebar，全宽） ═══ */
.app-main {
  padding: 28px 32px;
  min-height: calc(100vh - var(--topbar-height));
  animation: pageIn 0.3s ease;
}

@keyframes pageIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

/* ── Common Components ── */

/* Cards */
.card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
  transition: all 0.25s;
}
.card:hover { box-shadow: var(--shadow-md); }

/* Section header */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.section-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-heading);
  display: flex;
  align-items: center;
  gap: 10px;
}
.section-title .badge {
  background: var(--accent-gradient);
  color: #fff;
  font-size: 10px;
  padding: 2px 10px;
  border-radius: 10px;
  font-weight: 500;
}
.section-more {
  font-size: 13px;
  color: var(--primary);
  font-weight: 500;
  transition: color 0.2s;
  cursor: pointer;
}
.section-more:hover { color: var(--primary-dark); }
.section-more i { font-size: 11px; margin-left: 4px; }

/* Stats card */
.stat-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
  padding: 20px 22px;
  text-align: center;
  transition: all 0.25s;
}
.stat-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.stat-card .stat-icon { font-size: 24px; margin-bottom: 8px; }
.stat-card .stat-num { font-size: 28px; font-weight: 700; color: var(--text-heading); }
.stat-card .stat-label { font-size: 13px; color: var(--text-muted); margin-top: 4px; }

/* Filter bar */
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}
.filter-group { display:flex; align-items:center; gap:8px; }
.filter-label { font-size:13px; color:var(--text-muted); white-space:nowrap; font-weight:500; }
.filter-tags { display:flex; gap:6px; flex-wrap:wrap; }
.filter-tag {
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 12px;
  cursor: pointer;
  border: 1px solid var(--border);
  color: var(--text-body);
  background: var(--bg-card);
  transition: all 0.2s;
  font-weight: 500;
}
.filter-tag:hover { border-color: var(--primary); color: var(--primary); }
.filter-tag.active { background: var(--primary-gradient); color: #fff; border-color: transparent; box-shadow: 0 2px 6px rgba(61,90,128,0.2); }

/* Grids */
.grid-2 { display:grid; grid-template-columns:repeat(2,1fr); gap:16px; }
.grid-3 { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
.grid-4 { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; }

/* Tag pills */
.tag-pill { display:inline-flex; align-items:center; gap:4px; padding:3px 10px; border-radius:6px; font-size:11px; font-weight:600; }
.tag-pill.primary { background:var(--primary-bg); color:var(--primary); }
.tag-pill.secondary { background:rgba(191,168,149,0.2); color:#8A7560; }
.tag-pill.accent { background:var(--accent-bg); color:var(--accent); }
.tag-pill.green { background:#ecfdf5; color:#059669; }
.tag-pill.red { background:#fef2f2; color:#dc2626; }

/* Buttons */
.btn-primary {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 24px; border-radius: var(--radius-sm);
  background: var(--primary-gradient); color: #fff;
  font-size: 14px; font-weight: 600; border: none;
  cursor: pointer; transition: all 0.25s;
  box-shadow: 0 2px 8px rgba(61,90,128,0.2);
}
.btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(61,90,128,0.3); }
.btn-accent {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 24px; border-radius: var(--radius-sm);
  background: var(--accent-gradient); color: #fff;
  font-size: 14px; font-weight: 600; border: none;
  cursor: pointer; transition: all 0.25s;
  box-shadow: 0 2px 8px rgba(200,90,32,0.25);
}
.btn-accent:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(200,90,32,0.35); }
.btn-outline {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 24px; border-radius: var(--radius-sm);
  border: 1.5px solid var(--border); color: var(--text-body);
  font-size: 14px; font-weight: 500; background: transparent;
  cursor: pointer; transition: all 0.25s;
}
.btn-outline:hover { border-color: var(--primary); color: var(--primary); background: var(--primary-bg); }

/* States */
.loading-state { text-align:center; padding:60px 20px; color:var(--text-muted); font-size:14px; }
.loading-state i { margin-right:8px; }
.empty-state { text-align:center; padding:60px 20px; color:var(--text-muted); }
.empty-state .empty-icon { font-size:48px; margin-bottom:12px; display:block; }
.empty-state p { font-size:14px; margin-bottom:4px; }
.empty-hint { font-size:13px; color:var(--text-muted); }

/* Bookmark band */
.bookmark-band {
  background: linear-gradient(135deg, #FFF8F0 0%, #F5EDE0 100%);
  border: 1px solid var(--clr-secondary);
  border-radius: var(--radius-md);
  padding: 14px 18px;
  margin-bottom: 20px;
}
.bm-band-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; }
.bm-band-title { font-size:14px; font-weight:600; color: var(--primary-dark); }
.bm-band-scroll { display:flex; gap:10px; overflow-x:auto; padding-bottom:4px; }
.bm-band-card { flex-shrink:0; background:#fff; border-radius:8px; padding:10px 14px; border:1px solid var(--clr-secondary); cursor:pointer; transition:all 0.2s; min-width:140px; }
.bm-band-card:hover { border-color: var(--primary); box-shadow:0 2px 8px rgba(61,90,128,0.1); }
.bm-band-name { font-size:13px; font-weight:600; color: var(--primary-dark); }
.bm-band-badge { font-size:16px; }
.bm-band-meta { font-size:11px; color: var(--clr-secondary); margin-top:2px; }

/* Responsive */
@media (max-width:1200px) {
  .tn-item span { display:none; }
  .tn-item i { font-size:15px; }
  .tn-item { padding:6px 10px; }
}
@media (max-width:900px) {
  .app-main { padding:20px; }
  .topbar-nav { gap:0; }
  .user-name { display:none; }
  .search-box { width:160px; }
}
@media (max-width:768px) {
  .search-box { width:120px; }
  .brand-sub { display:none; }
}
@media (max-width:640px) {
  .grid-4, .grid-3, .grid-2 { grid-template-columns:1fr; }
  .app-main { padding:14px; }
  .search-box { display:none; }
  .tn-item i { font-size:16px; }
}
.icon-blue { color: var(--pri); }
.icon-blue svg { stroke: var(--pri); }
</style>