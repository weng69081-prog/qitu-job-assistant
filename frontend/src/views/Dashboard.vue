<template>
  <div class="dashboard">
    <!-- ═══ 全宽欢迎横幅（对比3风格：深色渐变，铺满整个宽度） ═══ -->
    <div class="welcome-banner-wrap">
      <div class="welcome-banner">
        <div class="wb-inner">
          <div class="wb-left">
            <div class="wb-avatar">{{ initial }}</div>
            <div>
              <h2 class="wb-greeting">{{ greeting }}，{{ displayName }}</h2>
              <p class="wb-subtitle">{{ subtitle }}</p>
            </div>
          </div>
          <div class="wb-right">
            <router-link to="/career" class="wb-btn"><i class="fas fa-compass"></i> 探索职业</router-link>
            <router-link to="/interview" class="wb-btn wb-btn-accent"><i class="fas fa-microphone"></i> 模拟面试</router-link>
          </div>
        </div>
        <!-- 趴边小橘猫 -->
        <img src="/src/assets/xiaoju-on-banner.png" class="banner-cat" alt="小橘">
      </div>
    </div>

    <!-- ═══ 内容容器 ═══ -->
    <div class="dash-container">
      <!-- 统计卡片 -->
      <div class="stats-grid">
        <div class="stat-card" v-for="s in stats" :key="s.label">
          <div class="stat-icon-bg" :style="{ background: s.bg }"><i class="fas" :class="s.icon"></i></div>
          <div class="stat-info">
            <span class="stat-num">{{ s.num }}</span>
            <span class="stat-plus" v-if="s.suffix">+</span>
            <span class="stat-label">{{ s.label }}</span>
          </div>
        </div>
      </div>

      <!-- ═══ 收藏内容汇总 ═══ -->
      <div class="fav-section">
        <div class="fav-header">
          <span class="fav-title"><i class="fas fa-star" style="color:var(--accent);"></i> 收藏内容</span>
          <router-link to="/favorites" class="fav-more">管理收藏 <i class="fas fa-chevron-right"></i></router-link>
        </div>
        <template v-if="careerBookmarks.length || videoBookmarks.length || interviewItems.length || examItems.length">
          <div class="fav-scroll">
            <!-- 收藏职业 -->
            <router-link
              v-for="b in careerBookmarks"
              :key="b.career"
              :to="`/career/${encodeURIComponent(b.career)}`"
              class="fav-card career"
            >
              <div class="fav-card-top"></div>
              <div class="fav-card-body">
                <div class="fav-badge-row">
                  <span class="fav-badge-wrap"><i class="fas fa-star"></i></span>
                  <span class="fav-arrow"><i class="fas fa-chevron-right"></i></span>
                </div>
                <span class="fav-name">{{ b.career }}</span>
                <div class="fav-meta-row">
                  <span class="fav-meta-dot"></span>
                  <span class="fav-meta">{{ b.difficulty || '中等' }} · {{ b.salary || '' }}</span>
                </div>
              </div>
            </router-link>
            <!-- 收藏视频 -->
            <router-link
              v-for="v in videoBookmarks"
              :key="v.bvid"
              :to="v.url || '/career'"
              class="fav-card video"
            >
              <div class="fav-card-top"></div>
              <div class="fav-card-body">
                <div class="fav-badge-row">
                  <span class="fav-badge-wrap"><i class="fas fa-film"></i></span>
                  <span class="fav-arrow"><i class="fas fa-chevron-right"></i></span>
                </div>
                <span class="fav-name">{{ (v.title || '').slice(0, 22) }}{{ (v.title || '').length > 22 ? '…' : '' }}</span>
                <div class="fav-meta-row">
                  <span class="fav-meta-dot"></span>
                  <span class="fav-meta">{{ v.author || 'B站' }}</span>
                </div>
              </div>
            </router-link>
            <!-- 面试题收藏 -->
            <router-link
              v-for="q in interviewItems"
              :key="`iq-${q.id}`"
              to="/favorites"
              class="fav-card interview"
            >
              <div class="fav-card-top"></div>
              <div class="fav-card-body">
                <div class="fav-badge-row">
                  <span class="fav-badge-wrap"><i class="fas fa-microphone"></i></span>
                  <span class="fav-arrow"><i class="fas fa-chevron-right"></i></span>
                </div>
                <span class="fav-name">{{ (q.question || '').slice(0, 24) }}{{ (q.question || '').length > 24 ? '…' : '' }}</span>
                <div class="fav-meta-row">
                  <span class="fav-meta-dot"></span>
                  <span class="fav-meta">{{ q.difficulty || '中等' }}</span>
                </div>
              </div>
            </router-link>
            <!-- 笔试收藏 -->
            <router-link
              v-for="q in examItems"
              :key="`eq-${q.id}`"
              to="/favorites"
              class="fav-card exam"
            >
              <div class="fav-card-top"></div>
              <div class="fav-card-body">
                <div class="fav-badge-row">
                  <span class="fav-badge-wrap"><i class="fas fa-pen"></i></span>
                  <span class="fav-arrow"><i class="fas fa-chevron-right"></i></span>
                </div>
                <span class="fav-name">{{ (q.question || q.title || '试题').slice(0, 22) }}{{ (q.question || '').length > 22 ? '…' : '' }}</span>
                <div class="fav-meta-row">
                  <span class="fav-meta-dot"></span>
                  <span class="fav-meta">{{ q.category || '笔试' }}</span>
                </div>
              </div>
            </router-link>
          </div>
        </template>
        <div v-else class="fav-empty">
          <i class="fas fa-star" style="color:#8EA0B8;font-size:20px;margin-right:6px;"></i>
          去职业探索或面试页收藏内容，就会出现在这里
        </div>
      </div>

      <!-- 主体：两栏布局 -->
      <div class="dash-main">
        <!-- 左栏：最近活动 -->
        <div class="dash-card activity-card">
          <div class="dash-card-header">
            <h3><i class="fas fa-clock" style="color:#3D5A80;"></i> 最近活动</h3>
          </div>
          <div class="activity-list" v-if="activities.length">
            <div class="activity-item" v-for="(a, i) in activities" :key="i">
              <div class="act-dot" :style="{ background: a.color }"></div>
              <div class="act-content">
                <span class="act-text">{{ a.text }}</span>
                <span class="act-time">{{ a.time }}</span>
              </div>
            </div>
          </div>
          <div class="empty-state" v-else>
            <span class="empty-icon"><i class="fas fa-inbox"></i></span>
            <p>还没有活动记录</p>
            <p class="empty-hint">先去探索一个职业方向吧</p>
          </div>
        </div>

        <!-- 右栏：待办 + 快捷入口 -->
        <div class="dash-right">
          <div class="dash-card todo-card">
            <div class="dash-card-header">
              <h3><i class="fas fa-clipboard-list" style="color:#C85A20;"></i> 今日待办</h3>
            </div>
            <div class="todo-list" v-if="todos.length">
              <label class="todo-item" v-for="(t, i) in todos" :key="i">
                <input type="checkbox" v-model="t.done" />
                <i class="fas fa-check-circle" :class="{ checked: t.done }"></i>
                <span :class="{ done: t.done }">{{ t.text }}</span>
              </label>
            </div>
          </div>

          <div class="dash-card quick-card">
            <div class="dash-card-header">
              <h3><i class="fas fa-bolt" style="color:#BFA895;"></i> 快捷入口</h3>
            </div>
            <div class="quick-grid">
              <router-link to="/career" class="quick-item"><i class="fas fa-compass"></i><span>职业探索</span></router-link>
              <router-link to="/interview" class="quick-item"><i class="fas fa-microphone"></i><span>面试模拟</span></router-link>
              <router-link to="/exam-practice" class="quick-item"><i class="fas fa-pen"></i><span>笔试练习</span></router-link>
              <router-link to="/resume" class="quick-item"><i class="fas fa-file-alt"></i><span>简历优化</span></router-link>
              <router-link to="/delivery-assistant" class="quick-item"><i class="fas fa-paper-plane"></i><span>投递助手</span></router-link>
              <router-link to="/settings" class="quick-item"><i class="fas fa-cog"></i><span>设置</span></router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCareerStore } from '../stores/career'
import axios from 'axios'

const store = useCareerStore()
const now = new Date()
const h = now.getHours()
const greeting = h < 12 ? '早上好' : h < 18 ? '下午好' : '晚上好'
const subtitle = '今天也要加油呀'

const displayName = ref('同学')
const initial = ref('同')

// ── 收藏数据 ──
const careerBookmarks = computed(() => {
  try { return store.validBookmarks.slice(0, 8) } catch { return [] }
})
const videoBookmarks = computed(() => {
  try { return store.videoBookmarks.slice(0, 4) } catch { return [] }
})
const interviewItems = ref([])
const examItems = ref([])

const stats = ref([
  { icon: 'fa-compass', num: 0, suffix: true, label: '探索职业', bg: 'rgba(61,90,128,0.1)' },
  { icon: 'fa-microphone', num: 0, suffix: true, label: '模拟面试', bg: 'rgba(200,90,32,0.1)' },
  { icon: 'fa-file-alt', num: 0, suffix: true, label: '简历优化', bg: 'rgba(191,168,149,0.2)' },
  { icon: 'fa-paper-plane', num: 0, suffix: true, label: '投递追踪', bg: 'rgba(142,160,184,0.2)' },
])

const activities = ref([])
const todos = ref([
  { text: '探索一个感兴趣的职业方向', done: false },
  { text: '完成一次模拟面试练习', done: false },
  { text: '上传简历进行AI优化', done: false },
])

onMounted(() => {
  const u = localStorage.getItem('user') || sessionStorage.getItem('user')
  if (u) {
    try {
      const user = JSON.parse(u)
      displayName.value = user.nickname || user.username || '同学'
      initial.value = displayName.value[0]
    } catch (e) {}
  }
  loadStats()
  loadActivities()
  loadSavedItems()
})

async function loadSavedItems() {
  try {
    const [ir, er] = await Promise.all([
      axios.get('/api/interview/saved-questions', { params: { page: 1, page_size: 10 } }),
      axios.get('/api/exam/saved-questions', { params: { page: 1, page_size: 10 } }),
    ])
    if (ir.data?.items) interviewItems.value = ir.data.items
    if (er.data?.items) examItems.value = er.data.items
  } catch { /* ignore */ }
}

function loadStats() {
  const careers = JSON.parse(localStorage.getItem('explored_careers') || '[]')
  const sessions = JSON.parse(localStorage.getItem('interview_sessions') || '[]')
  stats.value[0].num = careers.length
  stats.value[1].num = sessions.length || 0
}

function loadActivities() {
  const careers = JSON.parse(localStorage.getItem('explored_careers') || '[]')
  const sessions = JSON.parse(localStorage.getItem('interview_sessions') || '[]')
  const acts = []
  careers.slice(-3).forEach(c => {
    acts.push({ text: `探索了「${c.title || c}」职业方向`, time: '最近', color: '#3D5A80' })
  })
  sessions.slice(-2).forEach(s => {
    acts.push({ text: `完成了「${s.title || '面试'}」模拟面试`, time: '最近', color: '#C85A20' })
  })
  if (!acts.length) {
    acts.push({ text: '欢迎来到启途！开始你的求职之旅', time: '刚刚', color: '#8EA0B8' })
  }
  activities.value = acts
}
</script>

<style scoped>
/* ═══ 全宽欢迎横幅（对比3：深色渐变铺满） ═══ */
.welcome-banner-wrap {
  width: 100vw;
  margin-left: calc(-50vw + 50%);
  margin-top: -28px;
  /* 突破 app-main 的 padding，使横幅全屏宽 + 紧贴导航 */
}
.welcome-banner {
  background: var(--primary-gradient);
  position: relative;
  border-bottom: 1px solid rgba(255,255,255,.06);
  padding: 28px 0;
}
/* 发光装饰（对比3风格） */
.welcome-banner::before {
  content: '';
  position: absolute;
  top: -40%;
  right: -5%;
  width: 450px;
  height: 450px;
  background: radial-gradient(circle, rgba(61,90,128,.12) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}
/* 趴边小橘猫 — 趴在蓝白分界线上 */
.banner-cat {
  position: absolute;
  bottom: -5px;
  right: 320px;
  width: 140px;
  height: auto;
  pointer-events: none;
  z-index: 0;
}
.welcome-banner::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: -5%;
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(200,90,32,.06) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}
.wb-inner {
  width: 100%;
  padding: 0 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 1;
  box-sizing: border-box;
}
.wb-left { display: flex; align-items: center; gap: 16px; }
.wb-avatar {
  width: 46px; height: 46px;
  border-radius: 50%;
  background: rgba(255,255,255,0.12);
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; font-weight: 700; color: #fff;
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255,255,255,.08);
}
.wb-greeting { font-size: 18px; font-weight: 700; color: #fff; }
.wb-subtitle { font-size: 13px; color: rgba(255,255,255,.45); margin-top: 2px; }
.wb-right { display: flex; gap: 10px; }
.wb-btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 9px 20px; border-radius: 8px;
  background: rgba(255,255,255,0.08);
  color: rgba(255,255,255,.8);
  font-size: 13px; font-weight: 500;
  transition: all 0.2s; text-decoration: none;
}
.wb-btn:hover { background: rgba(255,255,255,0.15); color: #fff; }
.wb-btn-accent {
  background: rgba(200,90,32,.8);
  color: #fff;
}
.wb-btn-accent:hover { background: #C85A20; }

/* ═══ 内容容器（全宽，使用 app-main 自带的 padding） ═══ */
.dash-container {
  width: 100%;
  padding-top: 24px;
}

/* ═══ 统计卡片（对比3风格：白底+彩色图标底） ═══ */
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
.stat-card {
  background: #fff; border-radius: 12px; padding: 20px;
  display: flex; align-items: center; gap: 16px;
  border: 1px solid #f0f2f6; transition: all 0.25s;
}
.stat-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,.06); transform: translateY(-2px); }
.stat-icon-bg {
  width: 48px; height: 48px; border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; color: #3D5A80; flex-shrink: 0;
}
.stat-info { display: flex; align-items: baseline; gap: 2px; flex-wrap: wrap; }
.stat-num { font-size: 26px; font-weight: 800; color: #2C3E50; }
.stat-plus { font-size: 18px; font-weight: 700; color: #C85A20; }
.stat-label { font-size: 13px; color: #8EA0B8; width: 100%; margin-top: 2px; }

/* ═══ 两栏主体 ═══ */
.dash-main { display: grid; grid-template-columns: 1fr 360px; gap: 24px; }

.dash-card {
  background: #fff; border-radius: 12px; border: 1px solid #f0f2f6; padding: 20px 22px;
}
.dash-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.dash-card-header h3 { font-size: 15px; font-weight: 700; color: #2C3E50; display: flex; align-items: center; gap: 8px; }
.dash-more { font-size: 12px; color: #3D5A80; display: flex; align-items: center; gap: 4px; transition: opacity 0.2s; }
.dash-more i { font-size: 10px; }
.dash-more:hover { opacity: 0.7; }

.activity-list { display: flex; flex-direction: column; }
.activity-item {
  display: flex; align-items: flex-start; gap: 12px;
  padding: 10px 0; border-bottom: 1px solid #f0f2f6;
}
.activity-item:last-child { border-bottom: none; }
.act-dot { width: 10px; height: 10px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
.act-content { display: flex; flex-direction: column; gap: 2px; }
.act-text { font-size: 14px; color: #4A5568; }
.act-time { font-size: 12px; color: #8EA0B8; }

.todo-card { margin-bottom: 16px; }
.todo-list { display: flex; flex-direction: column; gap: 10px; }
.todo-item { display: flex; align-items: center; gap: 10px; cursor: pointer; user-select: none; font-size: 14px; color: #4A5568; }
.todo-item input { display: none; }
.todo-item i { font-size: 18px; color: #BFA895; transition: color 0.2s; }
.todo-item i.checked { color: #3D5A80; }
.todo-item .done { text-decoration: line-through; color: #BFA895; }

.quick-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.quick-item {
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  padding: 14px 8px; border-radius: 10px;
  background: #f4f6f9; color: #4A5568; font-size: 12px; font-weight: 500; transition: all 0.2s;
}
.quick-item i { font-size: 18px; color: #3D5A80; }
.quick-item:hover { background: #eaecf0; transform: translateY(-1px); }

.empty-state { text-align: center; padding: 40px 20px; color: #8EA0B8; }
.empty-icon { font-size: 40px; margin-bottom: 8px; display: block; }
.empty-state p { font-size: 14px; margin-bottom: 4px; }
.empty-hint { font-size: 13px; color: #8EA0B8; }

/* ═══ 收藏内容汇总（横向滚动卡片条） ═══ */
.fav-section { margin-bottom: 24px; }
.fav-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 14px;
}
.fav-title { font-size: 15px; font-weight: 700; color: #2C3E50; display: flex; align-items: center; gap: 6px; }
.fav-more { font-size: 12px; color: #3D5A80; display: flex; align-items: center; gap: 4px; }
.fav-more:hover { opacity: 0.7; }
.fav-scroll {
  display: flex; gap: 14px; overflow-x: auto;
  padding: 4px 0 10px;
  scroll-snap-type: x mandatory;
}
.fav-scroll::-webkit-scrollbar { height: 4px; }
.fav-scroll::-webkit-scrollbar-thumb { background: #d0d4de; border-radius: 4px; }

/* ── 收藏卡片：美化版 ── */
.fav-card {
  flex-shrink: 0;
  scroll-snap-align: start;
  min-width: 185px; max-width: 220px;
  border-radius: 14px;
  padding: 0;
  background: #fff;
  border: 1px solid #eaeef2;
  text-decoration: none; color: inherit;
  overflow: hidden;
  transition: all 0.28s cubic-bezier(.22,.61,.36,1);
  box-shadow: 0 1px 3px rgba(61,90,128,.04);
  display: flex;
  flex-direction: column;
}
.fav-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(61,90,128,.1);
  border-color: transparent;
}

/* 顶部色带 — 按类型 */
.fav-card-top {
  height: 6px;
  flex-shrink: 0;
}
.fav-card.career .fav-card-top { background: linear-gradient(90deg, #3D5A80, #54759C); }
.fav-card.video .fav-card-top { background: linear-gradient(90deg, #C85A20, #DA7530); }
.fav-card.interview .fav-card-top { background: linear-gradient(90deg, #3D5A80, #8EA0B8); }
.fav-card.exam .fav-card-top { background: linear-gradient(90deg, #BFA895, #CDB8A5); }

/* 卡片主体 */
.fav-card-body {
  padding: 14px 16px 16px;
  display: flex;
  flex-direction: column;
  flex: 1;
}

/* 图标行 */
.fav-badge-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}
.fav-badge-wrap {
  width: 34px; height: 34px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 15px;
}
.fav-card.career .fav-badge-wrap { background: rgba(61,90,128,.08); color: #3D5A80; }
.fav-card.video .fav-badge-wrap { background: rgba(200,90,32,.08); color: #C85A20; }
.fav-card.interview .fav-badge-wrap { background: rgba(61,90,128,.08); color: #3D5A80; }
.fav-card.exam .fav-badge-wrap { background: rgba(191,168,149,.12); color: #8A7560; }

/* 箭头 */
.fav-arrow {
  font-size: 12px; color: #bcc3d0;
  transition: transform 0.2s, color 0.2s;
}
.fav-card:hover .fav-arrow {
  transform: translateX(3px);
  color: #3D5A80;
}

/* 标题 */
.fav-name {
  font-size: 14px;
  font-weight: 600;
  color: #2C3E50;
  line-height: 1.35;
  margin-bottom: 6px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 元信息 */
.fav-meta-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: auto;
}
.fav-meta-dot {
  width: 5px; height: 5px; border-radius: 50%;
  flex-shrink: 0;
}
.fav-card.career .fav-meta-dot { background: #3D5A80; }
.fav-card.video .fav-meta-dot { background: #C85A20; }
.fav-card.interview .fav-meta-dot { background: #8EA0B8; }
.fav-card.exam .fav-meta-dot { background: #BFA895; }
.fav-meta {
  font-size: 11px; color: #8EA0B8;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.fav-empty {
  background: #fff; border-radius: 12px; border: 1px dashed #d0d4de;
  padding: 24px 20px; text-align: center; font-size: 14px; color: #8EA0B8;
  display: flex; align-items: center; justify-content: center; gap: 6px;
}

@media (max-width: 900px) {
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .dash-main { grid-template-columns: 1fr; }
  .wb-inner { flex-direction: column; gap: 16px; align-items: flex-start; }
}
@media (max-width: 480px) {
  .stats-grid { grid-template-columns: 1fr; }
  .wb-right { flex-direction: column; width: 100%; }
  .wb-btn { width: 100%; justify-content: center; }
}
</style>