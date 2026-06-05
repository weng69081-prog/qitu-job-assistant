<template>
  <div class="fav-page">
    <!-- ═══ 欢迎横幅 ═══ -->
    <div class="welcome">
      <div>
        <h1>{{ greeting }}，<span class="hl-name">{{ displayName }}</span></h1>
      </div>
      <div class="date">{{ todayStr }}</div>
      <img src="/src/assets/xiaoju-on-banner.png" class="banner-cat" alt="小橘">
    </div>

    <!-- ═══ 分类标签 ═══ -->
    <div class="fav-tabs">
      <span
        v-for="tab in tabs"
        :key="tab.key"
        class="fav-tab"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key"
      >
        {{ tab.label }}
        <span class="tab-count">{{ tab.count }}</span>
      </span>
    </div>

    <!-- ═══ 加载态 ═══ -->
    <div v-if="loading" class="loading-state">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation:spin 1s linear infinite"><line x1="12" y1="2" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="22"/><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"/><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"/><line x1="2" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="22" y2="12"/><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"/><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"/></svg>
      加载中…
    </div>

    <!-- ═══ 空态 ═══ -->
    <div v-else-if="!filteredItems.length" class="empty-state">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#CBD5E1" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="empty-icon"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
      <p v-if="activeTab === 'all'">还没有收藏任何内容</p>
      <p v-else>{{ tabs.find(t => t.key === activeTab)?.label }}还没有收藏</p>
      <p class="empty-hint">去职业探索或面试页收藏内容吧</p>
      <router-link to="/career" class="explore-btn">去探索 ›</router-link>
    </div>

    <!-- ═══ 收藏列表 ═══ -->
    <div v-else class="fav-list">
      <div
        v-for="item in filteredItems"
        :key="item._id"
        class="fav-item"
      >
        <!-- 职业收藏 -->
        <template v-if="item._type === 'career'">
          <div class="fav-type-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          </div>
          <div class="fav-info" @click="goCareer(item)">
            <div class="fav-title">{{ item.career }}</div>
            <div class="fav-meta">{{ item.difficulty || '中等' }} · {{ item.salary || '' }}</div>
          </div>
          <div class="fav-actions">
            <router-link :to="`/career/${encodeURIComponent(item.career)}`" class="fav-btn" title="查看详情">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
            </router-link>
            <button class="fav-btn danger" @click="removeCareer(item)" title="取消收藏">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>
        </template>

        <!-- 视频收藏 -->
        <template v-else-if="item._type === 'video'">
          <div class="fav-type-icon video">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="23 7 16 12 23 17 23 7"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/></svg>
          </div>
          <div class="fav-info" @click="goUrl(item.url)">
            <div class="fav-title">{{ item.title || '未命名视频' }}</div>
            <div class="fav-meta">{{ item.author || 'B站' }}<span v-if="item.career"> · {{ item.career }}</span></div>
          </div>
          <div class="fav-actions">
            <a :href="item.url" target="_blank" class="fav-btn" title="观看">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
            </a>
            <button class="fav-btn danger" @click="removeVideo(item)" title="取消收藏">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>
        </template>

        <!-- 面试题收藏 -->
        <template v-else-if="item._type === 'interview'">
          <div class="fav-type-icon interview">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          </div>
          <div class="fav-info">
            <div class="fav-title">{{ item.question }}</div>
            <div class="fav-meta">
              <span class="tag-pill" :class="diffPill(item.difficulty)">{{ item.difficulty || '中等' }}</span>
              <span v-if="item.category"> · {{ item.category }}</span>
              <span> · {{ item.created_at }}</span>
            </div>
          </div>
          <div class="fav-actions">
            <button class="fav-btn danger" @click="removeInterview(item)" title="取消收藏">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>
        </template>

        <!-- 笔试收藏 -->
        <template v-else-if="item._type === 'exam'">
          <div class="fav-type-icon exam">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
          </div>
          <div class="fav-info">
            <div class="fav-title">{{ item.question || item.title || '试题' }}</div>
            <div class="fav-meta">
              <span v-if="item.category">{{ item.category }}</span>
              <span v-if="item.question_type"> · {{ item.question_type }}</span>
            </div>
          </div>
          <div class="fav-actions">
            <button class="fav-btn danger" @click="removeExam(item)" title="取消收藏">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useCareerStore } from '../stores/career'
import axios from 'axios'

const router = useRouter()
const store = useCareerStore()

// ── 问候 ──
const now = new Date()
const h = now.getHours()
const greeting = h < 12 ? '早上好' : h < 18 ? '下午好' : '晚上好'
const displayName = ref('同学')
const todayStr = now.toLocaleDateString('zh-CN', { weekday: 'short', month: 'short', day: 'numeric' }).toUpperCase()

const activeTab = ref('all')
const loading = ref(false)

// 收藏数据源
const interviewItems = ref([])
const examItems = ref([])

const tabs = computed(() => [
  { key: 'all',    label: '全部',    count: allItems.value.length },
  { key: 'career', label: '职业',    count: store.validBookmarks.length },
  { key: 'video',  label: '视频',    count: store.videoBookmarks.length },
  { key: 'interview', label: '面试题', count: interviewItems.value.length },
  { key: 'exam',   label: '笔试',    count: examItems.value.length },
])

// 把所有收藏汇总成一个统一列表
const allItems = computed(() => {
  const items = []
  // 职业收藏
  store.validBookmarks.forEach(b => {
    items.push({ ...b, _type: 'career', _id: `career-${b.career}` })
  })
  // 视频收藏
  store.videoBookmarks.forEach(v => {
    items.push({ ...v, _type: 'video', _id: `video-${v.bvid}` })
  })
  // 面试题
  interviewItems.value.forEach(q => {
    items.push({ ...q, _type: 'interview', _id: `interview-${q.id}` })
  })
  // 笔试
  examItems.value.forEach(q => {
    items.push({ ...q, _type: 'exam', _id: `exam-${q.id}` })
  })
  return items
})

// 按分类过滤
const filteredItems = computed(() => {
  let items = allItems.value
  if (activeTab.value !== 'all') {
    items = items.filter(i => i._type === activeTab.value)
  }
  return items
})
function diffPill(d) {
  const m = { easy: 'green', 简单: 'green', medium: 'orange', 中等: 'orange', hard: 'red', 困难: 'red' }
  return m[d] || 'gray'
}

// ── 操作 ──
function goCareer(item) { router.push(`/career/${encodeURIComponent(item.career)}`) }
function goUrl(url) { if (url) window.open(url, '_blank') }

function removeCareer(item) {
  store.removeBookmark(item.career)
  ElMessage.success('已取消收藏')
}
function removeVideo(item) {
  store.removeVideoBookmark(item.bvid)
  ElMessage.success('已取消收藏')
}
async function removeInterview(item) {
  try {
    await axios.delete(`/api/interview/saved-questions/${item.id}`)
    interviewItems.value = interviewItems.value.filter(q => q.id !== item.id)
    ElMessage.success('已取消收藏')
  } catch { ElMessage.error('取消失败') }
}
async function removeExam(item) {
  try {
    await axios.delete(`/api/exam/saved-questions/${item.id}`)
    examItems.value = examItems.value.filter(q => q.id !== item.id)
    ElMessage.success('已取消收藏')
  } catch { ElMessage.error('取消失败') }
}

// ── 加载数据 ──
async function loadInterviewSaved() {
  try {
    const { data } = await axios.get('/api/interview/saved-questions', { params: { page: 1, page_size: 200 } })
    interviewItems.value = data.items || []
  } catch { /* ignore */ }
}
async function loadExamSaved() {
  try {
    const { data } = await axios.get('/api/exam/saved-questions', { params: { page: 1, page_size: 200 } })
    examItems.value = data.items || []
  } catch { /* ignore */ }
}

onMounted(async () => {
  loading.value = true
  await Promise.all([loadInterviewSaved(), loadExamSaved()])
  loading.value = false
})
</script>

<style scoped>
/* ═══ 收藏管理页面 ═══ */
.fav-page { max-width: 860px; }

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

/* ── 分类标签 ── */
.fav-tabs {
  display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap;
}
.fav-tab {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 7px 18px; border-radius: 20px;
  font-size: 14px; font-weight: 700; cursor: pointer;
  background: var(--bg-light); color: var(--primary);
  border: 1.5px dashed transparent;
  transition: all 0.2s;
}
.fav-tab:hover { border-color: var(--border-dashed); }
.fav-tab.active { background: var(--primary); color: #fff; border-color: var(--primary); }
.fav-tab .tab-count {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 20px; height: 20px; border-radius: 10px;
  background: rgba(37,99,235,0.10);
  font-size: 11px; padding: 0 6px; color: var(--primary);
}
.fav-tab.active .tab-count { background: rgba(255,255,255,0.2); color: #fff; }

/* ── 加载态 ── */
.loading-state {
  text-align: center; padding: 60px 0;
  color: var(--text-muted); font-size: 14px;
  display: flex; align-items: center; justify-content: center; gap: 8px;
}

/* ── 收藏列表 ── */
.fav-list { display: flex; flex-direction: column; gap: 10px; }

/* ── 收藏项卡片 ── */
.fav-item {
  display: flex; align-items: center; gap: 14px;
  background: var(--bg-light);
  border-radius: 12px;
  padding: 14px 18px;
  border: 1.5px dashed var(--border-dashed);
  transition: box-shadow 0.2s;
}
.fav-item:hover { box-shadow: 0 2px 10px rgba(37,99,235,0.08); }
.fav-type-icon {
  width: 40px; height: 40px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  background: rgba(255,255,255,0.65);
  color: var(--primary);
}
.fav-type-icon.video { color: var(--accent); }
.fav-type-icon.interview { color: #7C3AED; }
.fav-type-icon.exam { color: #059669; }
.fav-info { flex: 1; min-width: 0; cursor: pointer; }
.fav-title { font-size: 14px; font-weight: 700; color: var(--text-heading); margin-bottom: 3px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.fav-meta { font-size: 12px; color: var(--text-muted); display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.tag-pill {
  display: inline-flex; padding: 1px 8px; border-radius: 10px; font-size: 11px;
  background: rgba(37,99,235,0.10); color: var(--primary);
}
.tag-pill.green { background: rgba(5,150,105,0.1); color: #059669; }
.tag-pill.orange { background: rgba(234,179,8,0.12); color: #B45309; }
.tag-pill.red { background: rgba(220,38,38,0.1); color: #DC2626; }
.fav-actions { display: flex; gap: 4px; flex-shrink: 0; }
.fav-btn {
  width: 32px; height: 32px; border-radius: 8px;
  display: inline-flex; align-items: center; justify-content: center;
  border: 1.5px dashed var(--border-dashed);
  background: rgba(255,255,255,0.65);
  color: var(--primary); cursor: pointer;
  transition: all 0.2s;
}
.fav-btn:hover { border-color: var(--primary); background: #fff; }
.fav-btn.danger:hover { border-color: #FCA5A5; color: #DC2626; background: rgba(220,38,38,0.05); }

/* ── 空状态 ── */
.empty-state {
  text-align: center; padding: 80px 20px;
  color: var(--text-muted);
}
.empty-state .empty-icon { margin-bottom: 12px; }
.empty-state p { font-size: 14px; margin-bottom: 6px; }
.empty-state .empty-hint { font-size: 12px; color: var(--text-muted); }
.explore-btn {
  display: inline-flex; align-items: center; gap: 6px;
  margin-top: 16px; padding: 10px 24px; border-radius: 10px;
  background: var(--primary); color: #fff;
  font-size: 14px; font-weight: 700;
  text-decoration: none; transition: opacity 0.2s;
  font-family: inherit;
}
.explore-btn:hover { opacity: 0.85; }

@keyframes spin { to { transform: rotate(360deg); } }
</style>