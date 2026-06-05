<template>
  <div class="dashboard">
    <!-- ═══ 全宽欢迎横幅（浅蓝清爽风格） ═══ -->
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
            <router-link to="/career" class="wb-btn">探索职业</router-link>
            <router-link to="/interview" class="wb-btn wb-btn-primary">模拟面试</router-link>
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
          <div class="stat-num">{{ s.num }}{{ s.suffix ? '+' : '' }}</div>
          <div class="stat-label">{{ s.label }}</div>
        </div>
      </div>

      <!-- ═══ 收藏内容汇总 ═══ -->
      <div class="fav-section">
        <div class="fav-header">
          <span class="fav-title">收藏内容</span>
          <router-link to="/favorites" class="fav-more">管理收藏 ›</router-link>
        </div>
        <template v-if="careerBookmarks.length || videoBookmarks.length || interviewItems.length || examItems.length">
          <div class="fav-scroll">
            <!-- 收藏职业 -->
            <router-link
              v-for="b in careerBookmarks"
              :key="b.career"
              :to="`/career/${encodeURIComponent(b.career)}`"
              class="fav-card"
            >
              <div class="fav-name">{{ b.career }}</div>
              <div class="fav-meta">{{ b.difficulty || '中等' }} · {{ b.salary || '' }}</div>
            </router-link>
            <!-- 收藏视频 -->
            <router-link
              v-for="v in videoBookmarks"
              :key="v.bvid"
              :to="v.url || '/career'"
              class="fav-card"
            >
              <div class="fav-name">{{ (v.title || '').slice(0, 20) }}{{ (v.title || '').length > 20 ? '…' : '' }}</div>
              <div class="fav-meta">{{ v.author || 'B站' }}</div>
            </router-link>
            <!-- 面试题收藏 -->
            <router-link
              v-for="q in interviewItems"
              :key="`iq-${q.id}`"
              to="/favorites"
              class="fav-card"
            >
              <div class="fav-name">{{ (q.question || '').slice(0, 22) }}{{ (q.question || '').length > 22 ? '…' : '' }}</div>
              <div class="fav-meta">{{ q.difficulty || '中等' }}</div>
            </router-link>
            <!-- 笔试收藏 -->
            <router-link
              v-for="q in examItems"
              :key="`eq-${q.id}`"
              to="/favorites"
              class="fav-card"
            >
              <div class="fav-name">{{ (q.question || q.title || '试题').slice(0, 20) }}{{ (q.question || '').length > 20 ? '…' : '' }}</div>
              <div class="fav-meta">{{ q.category || '笔试' }}</div>
            </router-link>
          </div>
        </template>
        <div v-else class="fav-empty">
          去职业探索或面试页收藏内容，就会出现在这里
        </div>
      </div>

      <!-- 主体：两栏布局 -->
      <div class="dash-main">
        <!-- 左栏：最近活动 -->
        <div class="dash-card activity-card">
          <div class="dash-card-header">
            <h3>最近活动</h3>
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
            <p>还没有活动记录</p>
            <p class="empty-hint">先去探索一个职业方向吧</p>
          </div>
        </div>

        <!-- 右栏：便利贴待办 + 快捷入口 -->
        <div class="dash-right">
          <div class="todo-stickynote">
            <div class="todo-pin"></div>
            <div class="todo-header">
              <h4>今日待办</h4>
            </div>
            <div class="todo-body">
              <div class="todo-list" v-if="todos.length">
                <label class="todo-item" v-for="(t, i) in todos" :key="i">
                  <input type="checkbox" v-model="t.done" />
                  <span class="todo-check" :class="{ checked: t.done }">✓</span>
                  <span :class="{ done: t.done }">{{ t.text }}</span>
                </label>
              </div>
              <div class="todo-empty" v-else>没有待办~ 给自己加个任务吧</div>
            </div>
          </div>

          <div class="dash-card quick-card">
            <div class="dash-card-header">
              <h3>快捷入口</h3>
            </div>
            <div class="quick-grid">
              <router-link to="/career" class="quick-item"><span>职业探索</span></router-link>
              <router-link to="/interview" class="quick-item"><span>面试模拟</span></router-link>
              <router-link to="/exam-practice" class="quick-item"><span>笔试练习</span></router-link>
              <router-link to="/resume" class="quick-item"><span>简历优化</span></router-link>
              <router-link to="/delivery-assistant" class="quick-item"><span>投递助手</span></router-link>
              <router-link to="/favorites" class="quick-item"><span>收藏</span></router-link>
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
  { lucide: 'Compass', num: 0, suffix: true, label: '探索职业', bg: 'rgba(37,99,235,0.08)' },
  { lucide: 'Mic', num: 0, suffix: true, label: '模拟面试', bg: 'rgba(37,99,235,0.08)' },
  { lucide: 'FileText', num: 0, suffix: true, label: '简历优化', bg: 'rgba(37,99,235,0.08)' },
  { lucide: 'Send', num: 0, suffix: true, label: '投递追踪', bg: 'rgba(37,99,235,0.08)' },
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
    acts.push({ text: `探索了「${c.title || c}」职业方向`, time: '最近', color: '#2563EB' })
  })
  sessions.slice(-2).forEach(s => {
    acts.push({ text: `完成了「${s.title || '面试'}」模拟面试`, time: '最近', color: '#0EA5E9' })
  })
  if (!acts.length) {
    acts.push({ text: '欢迎来到启途！开始你的求职之旅', time: '刚刚', color: '#94A3B8' })
  }
  activities.value = acts
}
</script>

<style scoped>
/* ═══ 全宽欢迎横幅（浅蓝清爽） ═══ */
.welcome-banner-wrap {
  width: 100vw;
  margin-left: calc(-50vw + 50%);
  margin-top: -24px;
}
.welcome-banner {
  background: var(--bg-light);
  position: relative;
  padding: 32px 0;
}
/* 趴边小橘猫 */
.banner-cat {
  position: absolute;
  bottom: -5px;
  right: 320px;
  width: 140px;
  height: auto;
  pointer-events: none;
  z-index: 0;
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
  background: var(--primary);
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; font-weight: 700; color: #fff;
}
.wb-greeting { font-size: 20px; font-weight: 700; color: var(--primary); }
.wb-subtitle { font-size: 13px; color: var(--text-muted); margin-top: 2px; }
.wb-right { display: flex; gap: 10px; }
.wb-btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 9px 20px; border-radius: 8px;
  background: #fff;
  color: var(--primary);
  font-size: 13px; font-weight: 500;
  border: 1.5px dashed var(--border-dashed);
  transition: all 0.2s; text-decoration: none;
  font-family: inherit;
}
.wb-btn:hover { background: var(--primary); color: #fff; border-color: var(--primary); }
.wb-btn-primary {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}
.wb-btn-primary:hover { background: var(--primary-dark); border-color: var(--primary-dark); }

/* ═══ 内容容器 ═══ */
.dash-container { width: 100%; padding-top: 24px; }

/* ═══ 统计卡片（浅蓝底虚线边框 + 大数字） ═══ */
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
.stat-card {
  background: var(--bg-light);
  border-radius: var(--radius-md);
  border: 1.5px dashed var(--border-dashed);
  padding: 20px 16px;
  text-align: center;
  transition: all 0.25s;
}
.stat-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.stat-num { font-size: 26px; font-weight: 800; color: var(--primary); }
.stat-label { font-size: 13px; color: var(--text-muted); margin-top: 4px; }

/* ═══ 收藏内容汇总（横向滚动卡片条） ═══ */
.fav-section { margin-bottom: 24px; }
.fav-header {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 14px;
}
.fav-title { font-size: 15px; font-weight: 700; color: var(--text-heading); display: flex; align-items: center; gap: 6px; }
.fav-more { font-size: 12px; color: var(--primary); display: flex; align-items: center; gap: 4px; }
.fav-more:hover { opacity: 0.7; }
.fav-scroll {
  display: flex; gap: 12px; overflow-x: auto;
  padding: 4px 0 10px;
  scroll-snap-type: x mandatory;
}
.fav-scroll::-webkit-scrollbar { height: 4px; }
.fav-scroll::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
.fav-card {
  flex-shrink: 0;
  scroll-snap-align: start;
  min-width: 170px; max-width: 210px;
  background: var(--bg-light);
  border-radius: var(--radius-md);
  border: 1.5px dashed var(--border-dashed);
  padding: 14px 16px;
  text-decoration: none;
  transition: all 0.25s;
  box-sizing: border-box;
}
.fav-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
  background: #fff;
}
.fav-name { font-size: 14px; font-weight: 600; color: var(--text-heading); line-height: 1.35; margin-bottom: 6px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.fav-meta { font-size: 11px; color: var(--text-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.fav-empty {
  background: var(--bg-light);
  border-radius: var(--radius-md);
  border: 1.5px dashed var(--border-dashed);
  padding: 24px 20px; text-align: center; font-size: 14px; color: var(--text-muted);
}

/* ═══ 两栏主体 ═══ */
.dash-main { display: grid; grid-template-columns: 1fr 340px; gap: 24px; }

.dash-card {
  background: var(--bg-light);
  border-radius: var(--radius-md);
  border: 1.5px dashed var(--border-dashed);
  padding: 20px 22px;
}
.dash-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.dash-card-header h3 { font-size: 15px; font-weight: 700; color: var(--primary); }

/* 活动列表 */
.activity-list { display: flex; flex-direction: column; }
.activity-item {
  display: flex; align-items: flex-start; gap: 12px;
  padding: 10px 0; border-bottom: 1px solid var(--border);
}
.activity-item:last-child { border-bottom: none; }
.act-dot { width: 10px; height: 10px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
.act-content { display: flex; flex-direction: column; gap: 2px; }
.act-text { font-size: 14px; color: var(--text-body); }
.act-time { font-size: 12px; color: var(--text-muted); }

/* ═══ 便利贴待办（蓝色便签） ═══ */
.todo-stickynote {
  background: #DBEAFE;
  border-radius: var(--radius-md);
  padding: 24px 20px 20px;
  position: relative;
  margin-bottom: 16px;
  transform: rotate(-0.5deg);
  box-shadow: 2px 3px 8px rgba(37,99,235,0.1);
}
.todo-pin {
  position: absolute;
  top: -6px;
  left: 50%;
  margin-left: -8px;
  width: 16px; height: 16px;
  background: radial-gradient(circle at 35% 35%, #60A5FA, #2563EB);
  border-radius: 50%;
  box-shadow: 0 1px 3px rgba(0,0,0,0.15);
}
.todo-header h4 {
  font-size: 15px;
  font-weight: 700;
  color: var(--primary);
  text-align: center;
  margin-bottom: 14px;
}
.todo-list { display: flex; flex-direction: column; gap: 10px; }
.todo-item { display: flex; align-items: center; gap: 10px; cursor: pointer; user-select: none; font-size: 14px; color: var(--text-body); }
.todo-item input { display: none; }
.todo-check {
  width: 18px; height: 18px; border-radius: 4px;
  border: 2px solid var(--primary);
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; color: transparent; flex-shrink: 0;
  transition: all 0.2s;
}
.todo-check.checked {
  background: var(--primary);
  color: #fff;
}
.todo-item .done { text-decoration: line-through; color: var(--text-muted); }
.todo-empty { text-align: center; font-size: 13px; color: var(--text-muted); padding: 20px 0; }

/* 快捷入口 */
.quick-card { margin-top: 0; }
.quick-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.quick-item {
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  padding: 14px 8px; border-radius: 10px;
  background: #fff;
  color: var(--text-body); font-size: 12px; font-weight: 500;
  border: 1.5px dashed var(--border-dashed);
  transition: all 0.2s;
  font-family: inherit;
}
.quick-item:hover { background: var(--primary); color: #fff; border-color: var(--primary); transform: translateY(-1px); }

/* 空状态 */
.empty-state { text-align: center; padding: 40px 20px; color: var(--text-muted); }
.empty-state p { font-size: 14px; margin-bottom: 4px; }
.empty-hint { font-size: 13px; color: var(--text-muted); }

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