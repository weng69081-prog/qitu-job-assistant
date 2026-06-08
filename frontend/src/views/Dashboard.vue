<template>
  <div class="dashboard">
    <div class="dash-scene" ref="dashRef" :style="{ zoom: dashZoom }">
    <!-- ═══ 欢迎横幅（全宽撑满） ═══ -->
    <div class="welcome">
      <div class="banner-greeting">
        <h1>{{ greeting }}，<span class="hl-name">{{ displayName }}</span></h1>
        <img :src="paperPlane" class="banner-plane" alt="">
      </div>
      <div class="date">{{ todayStr }}</div>
      <img src="/src/assets/xiaoju-on-banner.png" class="banner-cat" alt="小橘">
    </div>

    <!-- ═══ 热力 + 卡片叠 ═══ -->
    <div class="heat-area">
      <!-- 左：活跃足迹（独立蓝底框） -->
      <div class="heat-card">
        <div class="heat-header">
          <div class="hl">活跃足迹</div>
          <div class="date-picker">
            <button class="dp-btn" @click="prevMonth">‹</button>
            <span class="dp-label">{{ heatYear }}年{{ monthNames[heatMonth] }}</span>
            <button class="dp-btn" @click="nextMonth">›</button>
          </div>
        </div>
        <div class="heat-grid">
          <div v-for="(level, i) in heatData" :key="i" class="hs" :class="[level, { today: i === todayCellIdx }]"></div>
        </div>
        <div class="heat-foot">
          <div class="hf-item"><span class="hf-num">{{ heatDaysMonth }}</span><span class="hf-lbl">天/本月</span></div>
          <div class="hf-item"><span class="hf-num">{{ heatDaysStreak }}</span><span class="hf-lbl">天连续</span></div>
          <div class="hf-item"><span class="hf-num">{{ heatWeekCount }}</span><span class="hf-lbl">次/本周</span></div>
        </div>
      </div>

      <!-- 右：4卡片叠 -->
      <div class="stack-wrapper">
        <div class="card-stack">
          <div
            v-for="(s, i) in s2stats"
            :key="s.label"
            class="stack-card"
            :class="{ active: activeCard === i }"
            :style="stackCardStyle(i)"
            @click="selectStackCard(i)"
          >
            <div class="sc-num">{{ s.num }}</div>
            <div class="sc-lbl">{{ s.label }}</div>
          </div>
          <div class="stack-click-tabs" aria-label="统计卡片切换">
            <button
              v-for="(s, i) in s2stats"
              :key="`stack-tab-${s.label}`"
              class="stack-tab"
              :class="{ active: activeCard === i }"
              type="button"
              :aria-label="`查看${s.label}`"
              @click="selectStackCard(i)"
            ></button>
          </div>
        </div>
        <div class="qitu-slogan" aria-label="启途标语">
          <span class="qs-brand">启途</span>
          <span class="qs-text">让每一步都有方向</span>
        </div>
      </div>
    </div>

    <!-- ═══ 主网格 ═══ -->
    <div class="main-grid">
      <!-- 左列 -->
      <div>
        <div class="light-card">
          <div class="lc-title">今日推荐</div>
          <router-link v-for="(item, i) in recommendations" :key="i" :to="item.url" class="rec-item">
            <span class="ri">{{ item.text }}</span>
            <span class="rt">{{ item.label }}</span>
          </router-link>
        </div>
        <div class="light-card">
          <div class="lc-title">操作记录</div>
          <div class="op-item" v-for="(a, i) in activities" :key="i">
            <span class="ot">{{ a.text }}</span>
            <span class="ots">{{ a.time }}</span>
          </div>
          <div class="empty-state op-empty" v-if="!activities.length">
            还没有操作记录
          </div>
        </div>
      </div>

      <!-- 右列 -->
      <div>
        <!-- 便利贴 -->
        <div class="sticky">
          <div class="pin"></div>
          <div class="sticky-scene">
            <div class="sticky-flipper" :class="{ flipped: stickyFlipped }">
              <!-- 正面：待办列表 -->
              <div class="sticky-front">
                <div class="st-title" @click="flipToBack">
                  今日待办
                </div>
                <div class="st-line"></div>
                <div id="todoList">
                  <div v-for="t in todos" :key="t.id">
                    <div class="st-item">
                      <div class="st-cb" :class="{ done: t.done }" @click="toggleTodo(t.id)"></div>
                      <span class="st-item-text" :class="{ done: t.done }" @click="flipToBack">{{ t.text }}</span>
                    </div>
                  </div>
                </div>
                <div class="st-hint" @click="flipToBack">+ 添加待办</div>
              </div>
              <!-- 背面：添加待办 -->
              <div class="sticky-back">
                <div class="back-title">添加待办事项</div>
                <div class="add-row">
                  <div class="add-wrap">
                    <input type="text" v-model="newTodoText" placeholder="输入新的待办..." @keydown.enter="addTodo" autocomplete="off">
                    <button @click="addTodo">添加</button>
                  </div>
                </div>
                <div class="back-list">
                  <div class="empty-msg" v-if="!editingTodos.length">还没有待办，输入上方添加吧～</div>
                  <div class="back-item" v-for="(t, idx) in editingTodos" :key="t.id">
                    <span class="bi-del" @click="removeEditTodo(idx)">×</span>
                    <span>{{ t.text }}</span>
                  </div>
                </div>
                <div class="back-actions">
                  <button class="back-save" @click="saveTodos">✓ 保存并返回</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 收藏 -->
        <div class="light-card">
          <div class="lc-title">
            收藏
            <router-link to="/favorites" class="lc-enter">进入 ›</router-link>
          </div>
          <div class="fav-item" v-for="b in careerBookmarks.slice(0, 4)" :key="b.career">
            <span class="fav-dot"></span>{{ b.career }}
          </div>
          <div class="fav-item" v-for="v in videoBookmarks.slice(0, 2)" :key="v.bvid">
            <span class="fav-dot"></span>{{ (v.title || '').slice(0, 16) }}
          </div>
          <div class="empty-state fav-empty" v-if="!careerBookmarks.length && !videoBookmarks.length">
            去探索收藏内容吧
          </div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="footer">
      <div>启途 · <span>QITU</span></div>
      <div>向上生长，自有答案</div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useCareerStore } from '../stores/career'
import axios from 'axios'
import bg1 from '../assets/cards/card-bg-1.jpg'
import bg2 from '../assets/cards/card-bg-2.jpg'
import bg3 from '../assets/cards/card-bg-3.jpg'
import bg4 from '../assets/cards/card-bg-4.jpg'
import paperPlane from '../assets/paper-plane.png'

const store = useCareerStore()

// ── 等比缩放 ──
const dashRef = ref(null)
const DASH_REF_W = 1160
const dashZoom = ref(1)

function updateDashZoom() {
  if (!dashRef.value) return
  const parent = dashRef.value.parentElement
  if (!parent) return
  const availW = parent.clientWidth
  // 实际容器宽度 / 参考宽度 = 缩放系数
  const scale = availW / DASH_REF_W
  // 窄于参考宽度时不缩放，宽于参考宽度时等比放大
  dashZoom.value = Math.max(1, scale)
}

let resizeTimer = null
function onResize() {
  clearTimeout(resizeTimer)
  resizeTimer = setTimeout(updateDashZoom, 60)
}

onMounted(() => {
  updateDashZoom()
  window.addEventListener('resize', onResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', onResize)
  clearTimeout(resizeTimer)
})

// ── 用户信息 ──
const now = new Date()
const h = now.getHours()
const greeting = h < 12 ? '早上好' : h < 18 ? '下午好' : '晚上好'
const displayName = ref('同学')
const initial = ref('同')
const todayStr = now.toLocaleDateString('zh-CN', { weekday: 'short', month: 'short', day: 'numeric' }).toUpperCase()

// ── 热力图 ──
const nowDate = new Date()
const heatYear = ref(nowDate.getFullYear())
const heatMonth = ref(nowDate.getMonth()) // 0-indexed

const monthNames = ['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月']

// 用年月做种子，生成稳定随机热力数据（196格，28×7）
function seededRand(seed) {
  let s = seed
  return function() {
    s = (s * 9301 + 49297) % 233280
    return s / 233280
  }
}
const heatData = computed(() => {
  const seed = heatYear.value * 100 + heatMonth.value + 1
  const rand = seededRand(seed)
  const data = []
  for (let i = 0; i < 196; i++) {
    const r = rand()
    if (r < 0.35) data.push('')
    else if (r < 0.6) data.push('l1')
    else if (r < 0.78) data.push('l2')
    else if (r < 0.9) data.push('l3')
    else data.push('l4')
  }
  return data
})

// 今天是第几天（当月），用于标记格子
const todayCellIdx = computed(() => {
  const today = new Date()
  if (heatYear.value !== today.getFullYear() || heatMonth.value !== today.getMonth()) return -1
  return today.getDate() - 1 // 0-indexed
})

const heatDaysMonth = computed(() => heatData.value.filter(l => l !== '').length)
const heatDaysStreak = computed(() => {
  // 用 heatData 算连续活跃天数
  let maxStreak = 0, cur = 0
  for (const l of heatData.value) {
    if (l !== '') { cur++; maxStreak = Math.max(maxStreak, cur) }
    else cur = 0
  }
  return maxStreak
})
const heatWeekCount = computed(() => {
  // 取后28个（最近一周）中的活跃数
  return heatData.value.slice(-28).filter(l => l !== '').length
})

function prevMonth() {
  if (heatMonth.value === 0) {
    heatMonth.value = 11
    heatYear.value--
  } else {
    heatMonth.value--
  }
}
function nextMonth() {
  if (heatMonth.value === 11) {
    heatMonth.value = 0
    heatYear.value++
  } else {
    heatMonth.value++
  }
}
function goToToday() {
  heatYear.value = nowDate.getFullYear()
  heatMonth.value = nowDate.getMonth()
}

// ── 4统计 ──
const s2stats = ref([
  { num: 12, label: '个已探索' },
  { num: 8, label: '次面试' },
  { num: 23, label: '次优化' },
  { num: 76, label: '平均分' },
])

// ── 今日推荐（从后端加载） ──
const recommendations = ref([])

// ── 从后端加载数据 ──
async function loadDashboardData() {
  try {
    const [recRes, statsRes, actRes] = await Promise.all([
      axios.get('/api/dashboard/recommendations'),
      axios.get('/api/dashboard/stats'),
      axios.get('/api/dashboard/activities'),
    ])
    if (recRes.data?.items) recommendations.value = recRes.data.items
    if (statsRes.data) {
      s2stats.value[0].num = statsRes.data.explored_count
      s2stats.value[1].num = statsRes.data.interview_count
      s2stats.value[2].num = statsRes.data.optimize_count
      s2stats.value[3].num = statsRes.data.avg_score
    }
    if (actRes.data?.items) activities.value = actRes.data.items
  } catch (e) {
    // API 不可用时 fallback 到 localStorage
    const careers = JSON.parse(localStorage.getItem('explored_careers') || '[]')
    const sessions = JSON.parse(localStorage.getItem('interview_sessions') || '[]')
    s2stats.value[0].num = careers.length || 0
    s2stats.value[1].num = sessions.length || 0
    s2stats.value[2].num = 0
    s2stats.value[3].num = 0
    const acts = []
    careers.slice(-3).forEach(c => acts.push({ text: `探索了「${c.title || c}」职业方向`, time: '最近' }))
    sessions.slice(-2).forEach(s => acts.push({ text: `完成了「${s.title || '面试'}」模拟面试`, time: '最近' }))
    if (!acts.length) acts.push({ text: '欢迎来到启途！开始你的求职之旅', time: '刚刚' })
    activities.value = acts
  }
}

// ── 卡片叠交互 ──
const activeCard = ref(0)

const bgImgs = [bg1, bg2, bg3, bg4]

function getStackOffset(i) {
  const total = s2stats.value.length || 4
  return (i - activeCard.value + total) % total
}

function stackCardStyle(i) {
  const offset = getStackOffset(i)
  return {
    '--stack-offset': offset,
    '--stack-z': 20 - offset,
    backgroundImage: `url(${bgImgs[i]})`,
  }
}

function selectStackCard(i) {
  activeCard.value = i
}

// ── 收藏数据 ──
const careerBookmarks = computed(() => {
  try { return store.validBookmarks.slice(0, 8) } catch { return [] }
})
const videoBookmarks = computed(() => {
  try { return store.videoBookmarks.slice(0, 4) } catch { return [] }
})

// ── 活动 ──
const activities = ref([])

// ── 便利贴待办 ──
const STORAGE_KEY = 'qitu_todos'
const stickyFlipped = ref(false)
const newTodoText = ref('')

function getDefaultTodos() {
  return [
    { id: 'd1', text: '继续探索职业方向', done: true },
    { id: 'd2', text: '完成今日面试题', done: false },
    { id: 'd3', text: '优化简历项目', done: false },
  ]
}

function loadTodos() {
  try {
    const data = localStorage.getItem(STORAGE_KEY)
    return data ? JSON.parse(data) : getDefaultTodos()
  } catch (e) { return getDefaultTodos() }
}

function saveTodosToStorage(t) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(t))
}

const todos = ref(loadTodos())
const editingTodos = ref([])

function toggleTodo(id) {
  const t = todos.value.find(x => x.id === id)
  if (t) {
    t.done = !t.done
    saveTodosToStorage(todos.value)
  }
}

function flipToBack() {
  editingTodos.value = todos.value.map(t => ({ ...t }))
  stickyFlipped.value = true
}

function flipToFront() {
  stickyFlipped.value = false
}

function addTodo() {
  const text = newTodoText.value.trim()
  if (!text) return
  editingTodos.value.push({ id: 't' + Date.now(), text, done: false })
  newTodoText.value = ''
}

function removeEditTodo(idx) {
  editingTodos.value.splice(idx, 1)
}

function saveTodos() {
  todos.value = editingTodos.value.map(t => ({ ...t }))
  saveTodosToStorage(todos.value)
  flipToFront()
}

// ── 初始化 ──
onMounted(() => {
  const u = localStorage.getItem('user') || sessionStorage.getItem('user')
  if (u) {
    try {
      const user = JSON.parse(u)
      displayName.value = user.nickname || user.username || '同学'
      initial.value = displayName.value[0]
    } catch (e) {}
  }

  // 从后端加载首页数据（推荐、统计、活动）
  loadDashboardData()
})
</script>

<style scoped>
.dashboard {
  width: 100%;
}

/* 等比缩放容器 — 固定1160px参考宽度，按容器宽度缩放 */
.dash-scene {
  width: 100%;
  max-width: 1160px;
  transform-origin: top left;
}

/* ═══ 欢迎横幅 ═══ */
.welcome {
  background: transparent;
  padding: 32px 32px;
  margin: 0 -28px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}
.welcome::before {
  content: '';
  position: absolute;
  top: 0;
  left: calc(-1 * (var(--sidebar-width) + 28px));
  right: -28px;
  bottom: 0;
  background: var(--bg-light);
  z-index: -1;
  border-radius: inherit;
  pointer-events: none;
}
.welcome h1 { font-size: 24px; color: var(--text-heading); font-weight: 400; }
.welcome h1 .hl-name { color: var(--primary); }
.welcome .date { font-size: 13px; color: var(--text-muted); letter-spacing: 0.05em; }
.banner-cat {
  position: absolute;
  bottom: -5px;
  right: 320px;
  width: 140px;
  height: auto;
  pointer-events: none;
  z-index: 0;
}
.banner-greeting {
  display: flex;
  align-items: center;
  gap: 10px;
}
.banner-plane {
  height: 48px;
  width: auto;
  opacity: 0.95;
  margin-left: 30px;
}

/* ═══ 热力+卡片叠 ═══ */
.heat-area {
  display: flex;
  gap: 4px;
  margin-bottom: 20px;
}
.heat-card {
  flex: 1;
  max-width: 650px;
  min-width: 0;
  background: var(--bg-light);
  border-radius: 12px;
  padding: 14px 20px;
  border: 1.5px solid var(--border-dashed);
}
.heat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}
.date-picker {
  display: flex;
  align-items: center;
  gap: 6px;
}
.dp-btn {
  width: 24px;
  height: 24px;
  border: 1px solid var(--border-dashed);
  border-radius: 6px;
  background: #fff;
  color: var(--primary);
  font-size: 14px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}
.dp-btn:hover {
  background: var(--bg-light);
}
.dp-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text);
  min-width: 64px;
  text-align: center;
}
.hl {
  font-size: 13px;
  font-weight: 700;
  color: var(--primary);
  letter-spacing: 0.06em;
}
.heat-grid {
  display: grid;
  grid-template-columns: repeat(28, 1fr);
  grid-template-rows: repeat(7, 1fr);
  gap: 3px;
  max-width: 520px;
  margin: 0 auto;
}
.hs {
  aspect-ratio: 1;
  border-radius: 3px;
  background: rgba(37,99,235,0.06);
}
.hs.l1 { background: rgba(37,99,235,0.15); }
.hs.l2 { background: rgba(37,99,235,0.35); }
.hs.l3 { background: rgba(37,99,235,0.6); }
.hs.l4 { background: var(--primary); }
.hs.today {
  outline: 2px solid #2563EB;
  outline-offset: -2px;
  border-radius: 3px;
  position: relative;
  z-index: 1;
}
.heat-foot {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-top: 10px;
  padding-top: 8px;
  position: relative;
}
.heat-foot::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: calc(100% - 50px);
  height: 1px;
  background: rgba(37,99,235,0.10);
}
.hf-item { display: flex; align-items: baseline; gap: 4px; }
.hf-num { font-size: 14px; font-weight: 700; color: var(--primary); }
.hf-lbl { font-size: 11px; color: var(--text-muted); }

/* 右：卡片叠 */
.stack-wrapper {
  display: flex;
  align-items: center;
  padding-top: 18px;
  padding-right: 8px;
  margin-left: 40px;
  gap: 20px;
}
.card-stack {
  width: 224px;
  flex-shrink: 0;
  position: relative;
  height: 238px;
}
.qitu-slogan {
  flex: none;
  width: 320px;
  min-height: 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  white-space: nowrap;
  position: relative;
  margin-left: 22px;
  padding: 0 10px;
}
.qitu-slogan::before {
  content: '';
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  top: 46px;
  width: 168px;
  height: 28px;
  border-radius: 999px;
  background: linear-gradient(90deg, rgba(37,99,235,0.14), rgba(14,165,233,0.06));
  z-index: 0;
}
.qitu-slogan::after {
  content: '';
  width: 252px;
  height: 12px;
  background: url("data:image/svg+xml,%3Csvg width='252' height='12' viewBox='0 0 252 12' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M2 6 C42 2 76 10 116 6 S190 2 232 6' stroke='%2393C5FD' stroke-width='1.7' stroke-dasharray='7 5' stroke-linecap='round' fill='none'/%3E%3Cpath d='M238 3 L249 6 L238 9' stroke='%2393C5FD' stroke-width='1.7' stroke-linecap='round' stroke-linejoin='round' fill='none'/%3E%3C/svg%3E") center/contain no-repeat;
  opacity: .82;
  margin-top: 2px;
}
.qs-brand {
  position: relative;
  z-index: 1;
  color: #2563EB;
  font-size: 58px;
  font-weight: 900;
  letter-spacing: 0.12em;
  line-height: .9;
  text-shadow: 0 10px 24px rgba(37,99,235,0.12);
}
.qs-text {
  position: relative;
  z-index: 1;
  color: #475569;
  font-size: 23px;
  font-weight: 800;
  letter-spacing: 0.04em;
  line-height: 1.15;
  font-style: italic;
  transform: none;
  margin-left: 0;
}
.stack-card {
  position: absolute;
  top: 0;
  left: calc(var(--stack-offset) * 22px);
  width: calc(100% - 54px);
  height: 210px;
  z-index: var(--stack-z);
  border-radius: 12px;
  padding: 20px 14px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  cursor: pointer;
  transition: left 0.45s cubic-bezier(0.34, 1.3, 0.5, 1),
              transform 0.55s cubic-bezier(0.34, 1.3, 0.5, 1),
              box-shadow 0.4s ease,
              z-index 0s linear 0.25s;
  box-shadow: 0 4px 14px rgba(37,99,235,0.10);
  color: #fff;
  will-change: left, transform;
  background-size: cover;
  background-position: center;
  overflow: hidden;
}
/* 半透明覆盖层，保证文字可读 */
.stack-card::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.20) 0%, rgba(255,255,255,0.06) 58%, rgba(37,99,235,0.04) 100%);
  border-radius: 12px;
  z-index: 0;
  pointer-events: none;
}
.stack-card > * {
  position: relative;
  z-index: 1;
}
.stack-card.active {
  left: 0;
  z-index: 30;
  box-shadow: 0 12px 32px rgba(37,99,235,0.18);
  transform: scale(1.05) translateY(-2px);
  transition: left 0.45s cubic-bezier(0.34, 1.3, 0.5, 1),
              transform 0.55s cubic-bezier(0.34, 1.3, 0.5, 1),
              box-shadow 0.4s ease,
              z-index 0s linear 0s;
}
.stack-card.active::before {
  background: linear-gradient(135deg, rgba(255,255,255,0.26) 0%, rgba(255,255,255,0.10) 56%, rgba(14,165,233,0.05) 100%);
}
.stack-click-tabs {
  position: absolute;
  left: 18px;
  right: 18px;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 9px;
  z-index: 20;
}
.stack-tab {
  width: 34px;
  height: 18px;
  border: 0;
  border-radius: 999px;
  background: transparent;
  padding: 0;
  cursor: pointer;
  position: relative;
  transition: transform 0.18s ease;
}
.stack-tab::before {
  content: '';
  position: absolute;
  left: 3px;
  right: 3px;
  top: 50%;
  height: 3px;
  border-radius: 999px;
  background: #BFDBFE;
  transform: translateY(-50%);
  box-shadow: 0 1px 4px rgba(37,99,235,0.10);
}
.stack-tab:hover,
.stack-tab.active {
  transform: translateY(-1px);
}
.stack-tab:hover::before,
.stack-tab.active::before {
  height: 4px;
  background: #2563EB;
  box-shadow: 0 3px 8px rgba(37,99,235,0.22);
}
.sc-num {
  font-size: 30px;
  font-weight: 900;
  color: #fff;
  line-height: 1.1;
  letter-spacing: 0.02em;
  text-shadow: 0 2px 6px rgba(0,0,0,0.3);
}
.sc-lbl {
  font-size: 13px;
  font-weight: 600;
  color: rgba(255,255,255,0.92);
  letter-spacing: 0.04em;
  text-shadow: 0 1px 4px rgba(0,0,0,0.3);
}

/* ═══ 主网格 ═══ */
.main-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 40px;
}
.main-grid > div {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.main-grid > div:first-child > .light-card:last-child {
  flex: 1;
}
.light-card {
  background: var(--bg-light);
  border-radius: 12px;
  padding: 14px 16px;
  border: 1.5px solid var(--border-dashed);
}
.lc-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 10px;
  letter-spacing: 0.06em;
  display: flex;
  align-items: center;
  gap: 5px;
}
.lc-enter {
  margin-left: auto;
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 11px;
  color: var(--primary);
  text-decoration: none;
  opacity: 0.6;
  transition: opacity 0.2s;
}
.lc-enter:hover { opacity: 1; }

/* 今日推荐 */
.rec-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 7px 12px;
  border-bottom: 1px solid rgba(37,99,235,0.10);
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  transition: background 0.15s, padding-left 0.15s;
  border-radius: 4px;
  margin: 0 -12px;
}
.rec-item:hover { background: rgba(37,99,235,0.04); padding-left: 16px; }
.rec-item:last-child { border-bottom: none; }
.rec-item .ri { font-size: 13px; color: var(--primary); }
.rec-item .rt {
  font-size: 11px;
  font-weight: 700;
  color: var(--primary);
  padding: 3px 10px;
  border-radius: 4px;
  background: #fff;
  white-space: nowrap;
}

/* 操作记录 */
.op-item {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px solid rgba(37,99,235,0.10);
}
.op-item:last-child { border-bottom: none; }
.op-item .ot { font-size: 13px; color: var(--primary); }
.op-item .ots { font-size: 11px; color: var(--primary); opacity: 0.5; }
.op-empty { padding: 12px 0 !important; font-size: 12px; }

/* ═══ 便利贴 ═══ */
.sticky {
  position: relative;
  background: var(--primary);
  border-radius: 3px;
  box-shadow: 2px 3px 6px rgba(37,99,235,0.15), 0 0 0 1px rgba(37,99,235,0.05);
  transform: rotate(-1deg);
  transition: transform 0.3s;
}
.sticky:hover { transform: rotate(0deg) scale(1.02); }
.sticky::before {
  content: '';
  position: absolute;
  top: 0; right: 0; z-index: 5;
  width: 0; height: 0;
  border-style: solid;
  border-width: 0 18px 18px 0;
  border-color: transparent #1D4ED8 transparent transparent;
  filter: drop-shadow(-1px 1px 1px rgba(0,0,0,0.06));
  pointer-events: none;
}
.pin {
  position: absolute;
  top: -6px; left: 50%;
  margin-left: -5px; z-index: 10;
  width: 10px; height: 10px;
  border-radius: 50%;
  background: linear-gradient(135deg, #888, #bbb);
  box-shadow: 0 1px 2px rgba(0,0,0,0.3);
  border: 1px solid rgba(255,255,255,0.3);
  pointer-events: none;
}

.sticky-scene { position: relative; perspective: 800px; }
.sticky-flipper { position: relative; width: 100%; }

.sticky-flipper.flipped .sticky-front {
  transform: scale(0.88) rotateY(-6deg);
  opacity: 0;
  pointer-events: none;
}
.sticky-flipper.flipped .sticky-back {
  transform: scale(1) rotateY(0deg);
  opacity: 1;
  pointer-events: auto;
}

.sticky-front {
  position: relative;
  padding: 18px 18px 20px;
  z-index: 2;
  min-height: 220px;
  transform-origin: left center;
  transition: transform 0.4s ease, opacity 0.4s ease;
}
.sticky-back {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  padding: 18px 18px 20px;
  z-index: 1;
  transform: scale(0.92) rotateY(4deg);
  transform-origin: right center;
  opacity: 0;
  pointer-events: none;
  transition: transform 0.4s ease, opacity 0.4s ease;
}

.st-line { height: 1px; background: linear-gradient(to right, rgba(255,255,255,0.12) 90%, transparent 100%); margin: 6px 0; }
#todoList { max-height: 105px; overflow-y: auto; }
#todoList::-webkit-scrollbar { width: 3px; }
#todoList::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 2px; }

.sticky-front .st-title {
  font-size: 13px;
  color: rgba(255,255,255,0.75);
  letter-spacing: 0.04em;
  margin-bottom: 6px;
  cursor: pointer;
  user-select: none;
}

.sticky-front .st-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 0;
  font-size: 14px;
  color: #fff;
}
.st-cb {
  width: 14px; height: 14px;
  border-radius: 50%;
  border: 2px solid rgba(255,255,255,0.6);
  flex-shrink: 0;
  cursor: pointer;
  transition: all 0.2s;
}
.st-cb:hover { border-color: #fff; background: rgba(255,255,255,0.1); }
.st-cb.done {
  background: rgba(255,255,255,0.2);
  border-color: rgba(255,255,255,0.8);
  position: relative;
}
.st-cb.done::after {
  content: '✓';
  position: absolute;
  top: -4px; left: 2px;
  font-size: 11px; color: #fff; font-weight: 700;
  pointer-events: none;
}
.st-item-text { cursor: pointer; flex: 1; }
.st-item-text.done { text-decoration: line-through; opacity: 0.5; }

.sticky-front .st-hint {
  font-size: 10px;
  color: rgba(255,255,255,0.35);
  text-align: center;
  padding-top: 8px;
  margin-top: 4px;
  border-top: 1px solid rgba(255,255,255,0.08);
  cursor: pointer;
  user-select: none;
  transition: color 0.2s;
}
.sticky-front .st-hint:hover { color: rgba(255,255,255,0.6); }

/* 背面 */
.sticky-back .back-title {
  font-size: 12px;
  color: rgba(255,255,255,0.75);
  letter-spacing: 0.04em;
  margin-bottom: 10px;
}
.sticky-back .add-row { display: flex; gap: 0; margin-bottom: 10px; }
.sticky-back .add-wrap { position: relative; width: 100%; }
.sticky-back .add-row input {
  flex: 1;
  width: 100%;
  background: rgba(255,255,255,0.15);
  border: 1px solid rgba(255,255,255,0.25);
  border-radius: 4px;
  padding: 6px 52px 6px 8px;
  font-family: inherit;
  font-size: 12px; color: #fff;
  outline: none;
  transition: border 0.2s;
}
.sticky-back .add-row input::placeholder { color: rgba(255,255,255,0.35); }
.sticky-back .add-row input:focus { border-color: rgba(255,255,255,0.6); }
.sticky-back .add-wrap button {
  position: absolute;
  right: 3px; top: 3px; bottom: 3px;
  background: rgba(255,255,255,0.2);
  border: none; border-radius: 3px;
  color: #fff;
  font-family: inherit;
  font-size: 11px; padding: 0 10px;
  cursor: pointer;
  transition: background 0.2s;
  white-space: nowrap;
}
.sticky-back .add-wrap button:hover { background: rgba(255,255,255,0.3); }
.sticky-back .back-list { max-height: 120px; overflow-y: auto; }
.sticky-back .back-list::-webkit-scrollbar { width: 3px; }
.sticky-back .back-list::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 2px; }
.sticky-back .back-item {
  display: flex; align-items: center; gap: 6px;
  padding: 3px 0; font-size: 12px; color: rgba(255,255,255,0.85);
}
.sticky-back .bi-del {
  width: 14px; height: 14px; border-radius: 50%;
  border: 1.5px solid rgba(255,255,255,0.35);
  flex-shrink: 0; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 10px; color: rgba(255,255,255,0.5);
  transition: all 0.2s;
}
.sticky-back .bi-del:hover { border-color: rgba(255,255,255,0.8); color: #fff; }
.sticky-back .back-actions { margin-top: 10px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: center; }
.sticky-back .back-save {
  background: rgba(255,255,255,0.2);
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 4px;
  color: #fff;
  font-family: inherit;
  font-size: 12px;
  padding: 6px 20px;
  cursor: pointer;
  transition: background 0.2s;
}
.sticky-back .back-save:hover { background: rgba(255,255,255,0.35); }
.sticky-back .empty-msg { font-size: 11px; color: rgba(255,255,255,0.35); text-align: center; padding: 10px 0; }

/* 收藏 */
.fav-item {
  padding: 8px 0;
  border-bottom: 1px solid rgba(37,99,235,0.10);
  font-size: 13px;
  color: var(--primary);
  display: flex;
  align-items: center;
  gap: 6px;
}
.fav-item:last-child { border-bottom: none; }
.fav-dot { width: 3px; height: 3px; border-radius: 50%; background: var(--primary); flex-shrink: 0; }
.fav-empty { padding: 12px 0 !important; font-size: 12px; }

/* Footer */
.footer {
  border-top: 1px solid rgba(37,99,235,0.10);
  padding: 16px 0;
  margin-top: 24px;
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: var(--text-muted);
  letter-spacing: 0.04em;
}
.footer span { color: var(--primary); font-weight: 700; }

/* Empty state */
.empty-state { text-align: center; color: var(--text-muted); }
</style>