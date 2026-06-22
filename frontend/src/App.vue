<template>
  <!-- 独立页面（填资料、面试会话等）：不裹导航 -->
  <div v-if="token && isStandalone" class="layout-root standalone">
    <router-view />
  </div>

  <!-- 已登录 + 非独立：左导航 + 内容区 -->
  <div v-else-if="token" class="layout-root">
    <!-- ═══ 左导航栏 ═══ -->
    <aside class="app-sidebar">
      <router-link to="/dashboard" class="sidebar-brand">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 21V9l8-6 8 6v12"/>
          <path d="M9 21v-6h6v6"/>
        </svg>
        <span class="brand-name">启途</span>
        <span class="brand-sub">QITU</span>
      </router-link>

      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="sn-item" active-class="sn-active">
          <span class="sn-dot"></span>
          <span class="sn-label">首页</span>
        </router-link>
        <router-link to="/career" class="sn-item" active-class="sn-active">
          <span class="sn-dot"></span>
          <span class="sn-label">职业探索</span>
        </router-link>
        <router-link to="/interview" class="sn-item" active-class="sn-active">
          <span class="sn-dot"></span>
          <span class="sn-label">面试模拟</span>
        </router-link>
        <router-link to="/exam-practice" class="sn-item" active-class="sn-active">
          <span class="sn-dot"></span>
          <span class="sn-label">笔试</span>
        </router-link>
        <router-link to="/resume" class="sn-item" active-class="sn-active">
          <span class="sn-dot"></span>
          <span class="sn-label">简历</span>
        </router-link>
        <router-link to="/delivery-assistant" class="sn-item" active-class="sn-active">
          <span class="sn-dot"></span>
          <span class="sn-label">投递</span>
        </router-link>
        </nav>

      <div class="sidebar-footer">
        <router-link to="/settings" class="sf-item" title="设置">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="3"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
          </svg>
        </router-link>
        <div class="sf-user">
          <div class="user-avatar" :style="avatarStyle">{{ (userDisplay.nickname || userDisplay.username || '同')[0] }}</div>
          <span class="user-name">{{ userDisplay.nickname || userDisplay.username || '同学' }}</span>
        </div>
      </div>
    </aside>

    <!-- ═══ 主内容区 ═══ -->
    <div class="app-body">
      <header class="app-topbar" v-show="showTopbar">
        <div class="topbar-left">
        </div>
        <div class="topbar-right">
          <router-link to="/settings" class="topbar-icon-btn" title="设置">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#64748B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
          </router-link>
        </div>
      </header>

      <main class="app-main" :class="{ 'fav-page': isFavorites, 'dashboard-page': isDashboard, 'full-banner-page': isFullBannerPage }">
        <router-view />
      </main>
    </div>

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
const isStandalone = computed(() => route.meta?.standalone === true)
const isFavorites = computed(() => route.path === '/favorites')
const isDashboard = computed(() => route.path === '/dashboard')
const fullBannerPages = ['/career', '/interview', '/exam-practice', '/resume', '/delivery-assistant']
const isFullBannerPage = computed(() => fullBannerPages.some(path => route.path === path || route.path.startsWith(`${path}/`)))
const showTopbar = computed(() => !isFavorites.value && !isDashboard.value && !isFullBannerPage.value)

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

watch(() => route.path, () => {
  token.value = localStorage.getItem('token')
  const u = localStorage.getItem('user') || sessionStorage.getItem('user')
  if (u) { try { userDisplay.value = JSON.parse(u) } catch(e) { userDisplay.value = {} } }
}, { immediate: true })
</script>

<style>
/* ══════════════════════════════════════════════════════════════
   启途 — GLOBAL DESIGN SYSTEM
   清爽白蓝风 · 左导航圆点
   ══════════════════════════════════════════════════════════════ */

/* ── CSS Variables ── */
:root {
  --primary: #2563EB;
  --primary-light: #EFF6FF;
  --primary-dark: #1D4ED8;
  --accent: #0EA5E9;

  --bg-body: #FFFFFF;
  --bg-card: #FFFFFF;
  --bg-light: #EFF6FF;
  --bg-sidebar: #F8FAFC;

  --text-heading: #1E293B;
  --text-body: #475569;
  --text-muted: #94A3B8;
  --text-light: #64748B;

  --border: #E2E8F0;
  --border-light: #F1F5F9;
  --border-dashed: #93C5FD;

  --sidebar-width: 180px;
  --topbar-height: 56px;

  --shadow-sm: 0 1px 3px rgba(37,99,235,0.06);
  --shadow-md: 0 4px 12px rgba(37,99,235,0.08);
  --shadow-hover: 0 8px 24px rgba(37,99,235,0.1);

  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
}

/* ── Reset & Base ── */
*, *::before, *::after { margin:0; padding:0; box-sizing:border-box; }
html { font-size: 15px; }
body {
  font-family: 'ZCOOL KuaiLe', -apple-system, BlinkMacSystemFont, "PingFang SC", sans-serif;
  background: var(--bg-body);
  color: var(--text-body);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
a { text-decoration:none; color:inherit; }
ul { list-style:none; }

/* ── Element Plus 主题覆盖 ── */
.el-button--primary { --el-button-bg-color: var(--primary); --el-button-border-color: var(--primary); --el-button-hover-bg-color: var(--primary-dark); --el-button-hover-border-color: var(--primary-dark); --el-button-active-bg-color: var(--primary-dark); }
.el-button--primary.is-plain { --el-button-bg-color: var(--bg-light); --el-button-border-color: #BFDBFE; --el-button-text-color: var(--primary); }
.el-card { border-radius: var(--radius-md) !important; border: 1.5px dashed var(--border-dashed) !important; }
.el-tag--primary { --el-tag-bg-color: var(--bg-light); --el-tag-border-color: #BFDBFE; --el-tag-text-color: var(--primary); }
.el-tag--success { --el-tag-bg-color: #ECFDF5; --el-tag-border-color: #A7F3D0; --el-tag-text-color: #059669; }
.el-tag--warning { --el-tag-bg-color: #FFFBEB; --el-tag-border-color: #FDE68A; --el-tag-text-color: #D97706; }
.el-tag--danger { --el-tag-bg-color: #FEF2F2; --el-tag-border-color: #FECACA; --el-tag-text-color: #DC2626; }
.el-tag--info { --el-tag-bg-color: var(--bg-light); --el-tag-border-color: #E2E8F0; --el-tag-text-color: var(--text-muted); }
.el-select { --el-select-input-focus-border-color: var(--primary); }
.el-input__wrapper.is-focus { box-shadow: 0 0 0 2px rgba(37,99,235,0.15) !important; }
.el-radio-button__inner { border-color: var(--border) !important; color: var(--text-body) !important; }
.el-radio-button.is-active .el-radio-button__inner { background: var(--primary) !important; border-color: var(--primary) !important; color: #fff !important; }
.el-progress-bar__inner { background: var(--primary) !important; }
.el-divider--vertical { border-color: var(--border) !important; }
.el-message { border-radius: var(--radius-md) !important; }
.el-dialog { border-radius: var(--radius-lg) !important; }

/* ── Layout Root ── */
.layout-root { min-height:100vh; display:flex; }
.layout-root.standalone, .layout-root.guest { min-height:100vh; display:flex; background:var(--bg-body); }

/* ═══════ 左导航栏 ═══════ */
.app-sidebar {
  width: var(--sidebar-width);
  min-height: 100vh;
  background: var(--bg-sidebar);
  border-right: 1.5px dashed var(--border-dashed);
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
  padding: 0;
}

/* 品牌区 */
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 20px 18px 16px;
  border-bottom: 1px dashed var(--border-dashed);
}
.sidebar-brand svg { flex-shrink:0; }
.brand-name { font-size: 24px; font-weight: 700; color: var(--primary); letter-spacing: 2px; }
.brand-sub { font-size: 9px; color: var(--text-muted); letter-spacing: 2.5px; margin-top: 2px; text-transform: uppercase; }

/* 圆点导航 */
.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 12px 0;
  gap: 2px;
}
.sn-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 18px;
  font-size: 16px;
  color: var(--text-light);
  transition: all 0.2s;
  position: relative;
}
.sn-item:hover {
  background: var(--bg-light);
  color: var(--primary);
}
.sn-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  border: 2px solid var(--text-muted);
  flex-shrink: 0;
  transition: all 0.2s;
}
.sn-item:hover .sn-dot {
  border-color: var(--primary);
}
.sn-active {
  color: var(--primary);
  font-weight: 500;
}
.sn-active .sn-dot {
  background: var(--primary);
  border-color: var(--primary);
}
.sn-label { line-height: 1; }

/* 侧栏底部用户 */
.sidebar-footer {
  padding: 12px 18px 16px;
  border-top: 1px dashed var(--border-dashed);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.sf-user {
  display: flex;
  align-items: center;
  gap: 8px;
}
.user-avatar {
  width: 30px; height: 30px; border-radius: 50%;
  background: var(--primary);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 12px; font-weight: 600;
}
.user-name { font-size: 12px; color: var(--text-light); }

/* ═══════ 顶部白条 ═══════ */
.app-body {
  margin-left: var(--sidebar-width);
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.app-topbar {
  height: var(--topbar-height);
  background: #fff;
  border-bottom: 1px dashed var(--border-dashed);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  position: sticky;
  top: 0;
  z-index: 90;
}
.topbar-left { display: flex; align-items: center; }
.topbar-right { display: flex; align-items: center; gap: 8px; }
.topbar-icon-btn {
  width: 32px; height: 32px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
  color: var(--text-light);
}
.topbar-icon-btn:hover {
  background: var(--bg-light);
  color: var(--primary);
}

/* ═══ 主内容 ═══ */
.app-main {
  flex: 1;
  --main-pad-x: 28px;
  padding: 24px var(--main-pad-x);
  animation: pageIn 0.3s ease;
}

@keyframes pageIn {
  from { opacity: 0; transform: translateY(6px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 收藏页：去掉顶部padding让欢迎横幅顶到头 */
.app-main.fav-page { padding-top: 0; }
.app-main.dashboard-page { overflow-x: hidden; }
/* 首页：同上 */
.app-main.dashboard-page { padding-top: 0; }
.app-main.full-banner-page { padding-top: 0; }
.layout-root:not(.standalone) .app-main.full-banner-page .page-banner.banner-fullwidth .banner-content {
  padding-left: calc(var(--sidebar-width) + 60px);
  padding-right: 32px;
}
/* 独立 standalone 页面：banner 不需要补偿侧边栏 */
.layout-root.standalone .page-banner.banner-fullwidth {
  width: 100%;
  margin-left: 0;
  border-radius: 0;
}

/* ── Common Components ── */

/* Cards */
.card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  border: 1.5px dashed var(--border-dashed);
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
  background: var(--primary);
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

/* Stats card */
.stat-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  border: 1.5px dashed var(--border-dashed);
  padding: 20px 22px;
  text-align: center;
  transition: all 0.25s;
}
.stat-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.stat-card .stat-icon { font-size: 24px; margin-bottom: 8px; color: var(--primary); }
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
.filter-tag.active { background: var(--primary); color: #fff; border-color: transparent; box-shadow: 0 2px 6px rgba(37,99,235,0.2); }

/* Grids */
.grid-2 { display:grid; grid-template-columns:repeat(2,1fr); gap:16px; }
.grid-3 { display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }
.grid-4 { display:grid; grid-template-columns:repeat(4,1fr); gap:16px; }

/* Tag pills */
.tag-pill { display:inline-flex; align-items:center; gap:4px; padding:3px 10px; border-radius:6px; font-size:11px; font-weight:600; }
.tag-pill.primary { background:var(--bg-light); color:var(--primary); }
.tag-pill.secondary { background:#F1F5F9; color:#64748B; }
.tag-pill.accent { background:#F0F9FF; color:#0EA5E9; }
.tag-pill.green { background:#ecfdf5; color:#059669; }
.tag-pill.red { background:#fef2f2; color:#dc2626; }

/* Buttons */
.btn-primary {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 24px; border-radius: var(--radius-sm);
  background: var(--primary); color: #fff;
  font-size: 14px; font-weight: 600; border: none;
  cursor: pointer; transition: all 0.25s;
  box-shadow: 0 2px 8px rgba(37,99,235,0.2);
}
.btn-primary:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(37,99,235,0.3); }
.btn-outline {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 24px; border-radius: var(--radius-sm);
  border: 1.5px solid var(--border); color: var(--text-body);
  font-size: 14px; font-weight: 500; background: transparent;
  cursor: pointer; transition: all 0.25s;
}
.btn-outline:hover { border-color: var(--primary); color: var(--primary); background: var(--bg-light); }

/* States */
.loading-state { text-align:center; padding:60px 20px; color:var(--text-muted); font-size:14px; }
.empty-state { text-align:center; padding:60px 20px; color:var(--text-muted); }
.empty-state .empty-icon { font-size:48px; margin-bottom:12px; display:block; }
.empty-state p { font-size:14px; margin-bottom:4px; }
.empty-hint { font-size:13px; color:var(--text-muted); }

/* Bookmark band */
.bookmark-band {
  background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
  border: 1.5px dashed var(--border-dashed);
  border-radius: var(--radius-md);
  padding: 14px 18px;
  margin-bottom: 20px;
}
.bm-band-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; }
.bm-band-title { font-size:14px; font-weight:600; color: var(--primary); }
.bm-band-scroll { display:flex; gap:10px; overflow-x:auto; padding-bottom:4px; }
.bm-band-card { flex-shrink:0; background:#fff; border-radius:8px; padding:10px 14px; border:1.5px dashed var(--border-dashed); cursor:pointer; transition:all 0.2s; min-width:140px; }
.bm-band-card:hover { border-color: var(--primary); box-shadow:0 2px 8px rgba(37,99,235,0.1); }
.bm-band-name { font-size:13px; font-weight:600; color: var(--primary); }
.bm-band-badge { font-size:16px; }
.bm-band-meta { font-size:11px; color: var(--text-muted); margin-top:2px; }

/* Responsive */
@media (max-width:900px) {
  .app-main { --main-pad-x: 20px; padding:20px var(--main-pad-x); }
  .user-name { display:none; }
}
@media (max-width:768px) {
  .brand-sub { display:none; }
}
@media (max-width:640px) {
  .grid-4, .grid-3, .grid-2 { grid-template-columns:1fr; }
  .app-main { --main-pad-x: 14px; padding:14px var(--main-pad-x); }
}
.icon-blue { color: var(--primary); }
.icon-blue svg { stroke: var(--primary); }

/* ═══ 品牌 Footer（全局） ═══ */
.brand-footer {
  text-align: center;
  padding: 36px 0 28px;
  color: #94A3B8;
  font-size: 13px;
  letter-spacing: 1px;
}
.brand-footer .qitu-up { color: #2563EB; font-weight: 800; }
.brand-footer .qitu-sl {
  margin-top: 4px;
  font-size: 11px;
  color: #BFDBFE;
}
</style>