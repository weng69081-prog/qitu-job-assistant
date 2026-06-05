<template>
  <div class="dashboard">
    <!-- ═══ 欢迎横幅（全宽撑满） ═══ -->
    <div class="welcome">
      <div>
        <h1>{{ greeting }}，<span class="hl-name">{{ displayName }}</span></h1>
      </div>
      <div class="date">{{ todayStr }}</div>
      <img src="/src/assets/xiaoju-on-banner.png" class="banner-cat" alt="小橘">
    </div>

    <!-- ═══ 热力 + 4统计 ═══ -->
    <div class="heat-row">
      <!-- 左：活跃足迹 -->
      <div class="heat-left">
        <div class="hl">活跃足迹</div>
        <div class="heat-grid">
          <div v-for="i in 196" :key="i" class="hs" :class="heatLevel(i)"></div>
        </div>
        <div class="heat-foot">
          <div class="hf-item"><span class="hf-num">{{ heatDaysMonth }}</span><span class="hf-lbl">天/本月</span></div>
          <div class="hf-item"><span class="hf-num">{{ heatDaysStreak }}</span><span class="hf-lbl">天连续</span></div>
          <div class="hf-item"><span class="hf-num">{{ heatWeekCount }}</span><span class="hf-lbl">次/本周</span></div>
        </div>
      </div>

      <!-- 右：4统计 2×2 -->
      <div class="heat-right">
        <div class="s2-item" v-for="s in s2stats" :key="s.label">
          <span class="s2-num">{{ s.num }}</span>
          <span class="s2-lbl">{{ s.label }}</span>
        </div>
      </div>
    </div>

    <!-- ═══ 主网格 ═══ -->
    <div class="main-grid">
      <!-- 左列 -->
      <div>
        <div class="light-card">
          <div class="lc-title">今日推荐</div>
          <div class="rec-item">
            <span class="ri">URL 到渲染：浏览器做了什么？</span>
            <span class="rt">立即练习 ›</span>
          </div>
          <div class="rec-item"><span class="ri">HTTP 缓存策略详解</span><span class="rt">今天 · 新</span></div>
          <div class="rec-item"><span class="ri">前端模块化发展史</span><span class="rt">明天截止</span></div>
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
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useCareerStore } from '../stores/career'
import axios from 'axios'

const store = useCareerStore()

// ── 用户信息 ──
const now = new Date()
const h = now.getHours()
const greeting = h < 12 ? '早上好' : h < 18 ? '下午好' : '晚上好'
const displayName = ref('同学')
const initial = ref('同')
const todayStr = now.toLocaleDateString('zh-CN', { weekday: 'short', month: 'short', day: 'numeric' }).toUpperCase()

// ── 热力图 ──
const heatDaysMonth = 23
const heatDaysStreak = 12
const heatWeekCount = 8

function heatLevel(i) {
  const r = Math.random()
  if (r < 0.35) return ''
  if (r < 0.6) return 'l1'
  if (r < 0.78) return 'l2'
  if (r < 0.9) return 'l3'
  return 'l4'
}

// ── 4统计 ──
const s2stats = ref([
  { num: 0, label: '个已探索' },
  { num: 0, label: '次面试' },
  { num: 0, label: '次优化' },
  { num: 0, label: '平均分' },
])

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

  // 加载统计
  const careers = JSON.parse(localStorage.getItem('explored_careers') || '[]')
  const sessions = JSON.parse(localStorage.getItem('interview_sessions') || '[]')
  s2stats.value[0].num = careers.length || 0
  s2stats.value[1].num = sessions.length || 0
  s2stats.value[2].num = 0
  s2stats.value[3].num = 0

  // 加载活动
  const acts = []
  careers.slice(-3).forEach(c => {
    acts.push({ text: `探索了「${c.title || c}」职业方向`, time: '最近' })
  })
  sessions.slice(-2).forEach(s => {
    acts.push({ text: `完成了「${s.title || '面试'}」模拟面试`, time: '最近' })
  })
  if (!acts.length) {
    acts.push({ text: '欢迎来到启途！开始你的求职之旅', time: '刚刚' })
  }
  activities.value = acts
})
</script>

<style scoped>
.dashboard { overflow-x: hidden; }

/* ═══ 欢迎横幅 ═══ */
.welcome {
  background: var(--bg-light);
  padding: 32px 32px;
  margin: -24px -28px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
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

/* ═══ 热力 ═══ */
.heat-row {
  display: flex;
  background: var(--bg-light);
  border-radius: 12px;
  margin-bottom: 20px;
  overflow: hidden;
  border: 1.5px dashed var(--border-dashed);
}
.heat-left {
  flex: 1;
  padding: 14px 0 14px 20px;
  min-width: 0;
}
.hl {
  font-size: 13px;
  font-weight: 700;
  color: var(--primary);
  margin-bottom: 6px;
  letter-spacing: 0.06em;
}
.heat-grid {
  display: grid;
  grid-template-columns: repeat(28, 1fr);
  grid-template-rows: repeat(7, 1fr);
  gap: 3px;
  max-width: 520px;
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

/* 右：4统计 2×2 */
.heat-right {
  width: 240px;
  flex-shrink: 0;
  padding: 12px 16px 12px 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  align-content: center;
}
.s2-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 3px;
  background: rgba(255,255,255,0.65);
  border-radius: 8px;
  padding: 12px 6px 10px;
}
.s2-num {
  font-size: 22px;
  font-weight: 800;
  color: var(--primary);
  line-height: 1.1;
}
.s2-lbl {
  font-size: 11px;
  color: var(--text-muted);
}

/* ═══ 主网格 ═══ */
.main-grid {
  display: grid;
  grid-template-columns: 1fr 260px;
  gap: 16px;
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
  padding: 18px;
  border: 1.5px dashed var(--border-dashed);
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
  padding: 10px 0;
  border-bottom: 1px solid rgba(37,99,235,0.10);
}
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
  padding: 8px 0;
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