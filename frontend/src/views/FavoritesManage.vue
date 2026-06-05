<template>
  <div class="page">
    <!-- ═══ 页面标题 ═══ -->
    <div class="section-header">
      <div class="section-title">
        <Star :size="16" :color="'var(--accent)'" />
        收藏管理
      </div>
    </div>

    <!-- ═══ 搜索栏 ═══ -->
    <div class="fav-search-bar">
      <Search :size="16" class="icon-blue" />
      <input
        type="text"
        v-model="searchQuery"
        placeholder="搜索收藏的职业、视频、面试题…"
        @input="onSearchChange"
      />
      <span v-if="searchQuery" class="fav-search-clear" @click="searchQuery='';onSearchChange()">
        <X :size="16" class="icon-blue" />
      </span>
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
        <span class="fav-tab-count">{{ tab.count }}</span>
      </span>
    </div>

    <!-- ═══ 加载态 ═══ -->
    <div v-if="loading" class="loading-state"><Loader :size="16" class="icon-blue" /> 加载中…</div>

    <!-- ═══ 空态 ═══ -->
    <div v-else-if="!filteredItems.length" class="empty-state">
      <span class="empty-icon">📂</span>
      <p v-if="activeTab === 'all'">还没有收藏任何内容</p>
      <p v-else>{{ tabs.find(t => t.key === activeTab)?.label }}还没有收藏</p>
      <p class="empty-hint">去职业探索或面试页收藏内容吧</p>
      <router-link to="/career" class="fav-go-btn">去探索 <ArrowRight :size="16" class="icon-blue" /></router-link>
    </div>

    <!-- ═══ 收藏列表 ═══ -->
    <template v-else>
      <div
        v-for="item in filteredItems"
        :key="item._id"
        class="fav-item-card"
      >
        <!-- 职业收藏 -->
        <template v-if="item._type === 'career'">
          <div class="fav-item-icon career">⭐</div>
          <div class="fav-item-info" @click="goCareer(item)">
            <div class="fav-item-title">{{ item.career }}</div>
            <div class="fav-item-meta">{{ item.difficulty || '中等' }} · {{ item.salary || '' }}</div>
          </div>
          <div class="fav-item-actions">
            <router-link :to="`/career/${encodeURIComponent(item.career)}`" class="fav-item-btn" title="查看详情"><Eye :size="16" class="icon-blue" /></router-link>
            <button class="fav-item-btn danger" @click="removeCareer(item)" title="取消收藏"><X :size="16" class="icon-blue" /></button>
          </div>
        </template>

        <!-- 视频收藏 -->
        <template v-else-if="item._type === 'video'">
          <div class="fav-item-icon video">📺</div>
          <div class="fav-item-info" @click="goUrl(item.url)">
            <div class="fav-item-title">{{ item.title || '未命名视频' }}</div>
            <div class="fav-item-meta">{{ item.author || 'B站' }}<span v-if="item.career"> · {{ item.career }}</span></div>
          </div>
          <div class="fav-item-actions">
            <a :href="item.url" target="_blank" class="fav-item-btn" title="观看"><ExternalLink :size="16" class="icon-blue" /></a>
            <button class="fav-item-btn danger" @click="removeVideo(item)" title="取消收藏"><X :size="16" class="icon-blue" /></button>
          </div>
        </template>

        <!-- 面试题收藏 -->
        <template v-else-if="item._type === 'interview'">
          <div class="fav-item-icon interview">🎙️</div>
          <div class="fav-item-info">
            <div class="fav-item-title">{{ item.question }}</div>
            <div class="fav-item-meta">
              <span class="tag-pill" :class="diffPill(item.difficulty)">{{ item.difficulty || '中等' }}</span>
              <span v-if="item.category"> · {{ item.category }}</span>
              <span> · {{ item.created_at }}</span>
            </div>
          </div>
          <div class="fav-item-actions">
            <button class="fav-item-btn danger" @click="removeInterview(item)" title="取消收藏"><X :size="16" class="icon-blue" /></button>
          </div>
        </template>

        <!-- 笔试收藏 -->
        <template v-else-if="item._type === 'exam'">
          <div class="fav-item-icon exam">📝</div>
          <div class="fav-item-info">
            <div class="fav-item-title">{{ item.question || item.title || '试题' }}</div>
            <div class="fav-item-meta">
              <span v-if="item.category">{{ item.category }}</span>
              <span v-if="item.question_type"> · {{ item.question_type }}</span>
            </div>
          </div>
          <div class="fav-item-actions">
            <button class="fav-item-btn danger" @click="removeExam(item)" title="取消收藏"><X :size="16" class="icon-blue" /></button>
          </div>
        </template>
      </div>
    </template>
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

const searchQuery = ref('')
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

// 搜索过滤
const filteredItems = computed(() => {
  let items = allItems.value
  if (activeTab.value !== 'all') {
    items = items.filter(i => i._type === activeTab.value)
  }
  const q = searchQuery.value.trim().toLowerCase()
  if (q) {
    items = items.filter(i => {
      const text = JSON.stringify(i).toLowerCase()
      return text.includes(q)
    })
  }
  return items
})

function onSearchChange() { /* 计算属性自动响应 */ }
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
.page { max-width: 960px; margin: 0 auto; }

/* ═══ 搜索栏 ═══ */
.fav-search-bar {
  display: flex; align-items: center;
  background: #fff; border: 1px solid #e0e4ea; border-radius: 10px;
  padding: 0 14px; height: 44px; margin-bottom: 18px;
  transition: border-color 0.2s;
}
.fav-search-bar:focus-within { border-color: #3D5A80; }
.fav-search-bar i { font-size: 15px; color: #8EA0B8; margin-right: 10px; }
.fav-search-bar input {
  flex: 1; border: none; outline: none; font-size: 14px; color: #2C3E50;
  background: transparent;
}
.fav-search-bar input::placeholder { color: #A0B4CC; }
.fav-search-clear {
  cursor: pointer; color: #8EA0B8; font-size: 14px; padding: 4px;
}
.fav-search-clear:hover { color: #C85A20; }

/* ═══ 分类标签 ═══ */
.fav-tabs {
  display: flex; gap: 8px; margin-bottom: 18px; flex-wrap: wrap;
}
.fav-tab {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 16px; border-radius: 20px;
  font-size: 13px; font-weight: 500; cursor: pointer;
  background: #f4f6f9; color: #4A5568; border: 1px solid transparent;
  transition: all 0.2s;
}
.fav-tab:hover { background: #eaecf0; }
.fav-tab.active { background: #3D5A80; color: #fff; border-color: #3D5A80; }
.fav-tab-count {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 18px; height: 18px; border-radius: 9px;
  background: rgba(0,0,0,.08); font-size: 11px; padding: 0 5px;
}
.fav-tab.active .fav-tab-count { background: rgba(255,255,255,.2); }

/* ═══ 收藏卡片 ═══ */
.fav-item-card {
  display: flex; align-items: center; gap: 14px;
  background: #fff; border: 1px solid #f0f2f6; border-radius: 12px;
  padding: 14px 18px; margin-bottom: 10px;
  transition: box-shadow 0.2s;
}
.fav-item-card:hover { box-shadow: 0 2px 10px rgba(0,0,0,.05); }
.fav-item-icon {
  width: 42px; height: 42px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; flex-shrink: 0;
}
.fav-item-icon.career { background: rgba(61,90,128,.08); }
.fav-item-icon.video { background: rgba(200,90,32,.08); }
.fav-item-icon.interview { background: rgba(61,90,128,.08); }
.fav-item-icon.exam { background: rgba(191,168,149,.15); }
.fav-item-info { flex: 1; min-width: 0; cursor: pointer; }
.fav-item-title { font-size: 14px; font-weight: 600; color: #2C3E50; margin-bottom: 4px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.fav-item-meta { font-size: 12px; color: #8EA0B8; display: flex; align-items: center; gap: 4px; flex-wrap: wrap; }
.fav-item-actions { display: flex; gap: 4px; flex-shrink: 0; }
.fav-item-btn {
  width: 32px; height: 32px; border-radius: 8px;
  display: inline-flex; align-items: center; justify-content: center;
  border: 1px solid #e0e4ea; background: #fff;
  color: #4A5568; font-size: 13px; cursor: pointer;
  transition: all 0.2s; text-decoration: none;
}
.fav-item-btn:hover { border-color: #3D5A80; color: #3D5A80; }
.fav-item-btn.danger:hover { border-color: #fca5a5; color: #dc2626; }

/* ═══ 空状态 ═══ */
.fav-go-btn {
  display: inline-block; margin-top: 12px;
  padding: 8px 20px; border-radius: 20px;
  background: #3D5A80; color: #fff; font-size: 13px; font-weight: 500;
  transition: opacity 0.2s;
}
.fav-go-btn:hover { opacity: .85; }
</style>