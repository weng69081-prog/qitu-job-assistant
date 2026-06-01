<template>
  <div class="savedlist-page">
    <!-- ═══ Banner ═══ -->
    <PageBanner fullwidth
      title="面试收藏夹"
      description="收藏值得反复练习的面试题目，随时回顾，稳步提升"
      icon="fa-star"
      variant="primary"
    >
      <template #actions>
        <button class="banner-back-btn" @click="$router.back()">
          <i class="fas fa-arrow-left"></i> 返回
        </button>
      </template>
    </PageBanner>

    <!-- ═══ 紧凑统计条 ═══ -->
    <section class="stat-ribbon">
      <div class="stat-cell">
        <div class="sc-icon"><i class="fas fa-star"></i></div>
        <div class="sc-body">
          <span class="sc-num">{{ interviewSavedTotal }}</span>
          <span class="sc-label">总收藏</span>
        </div>
      </div>
      <div class="stat-cell">
        <div class="sc-icon sc-cat"><i class="fas fa-layer-group"></i></div>
        <div class="sc-body">
          <span class="sc-num">{{ categoryCount }}</span>
          <span class="sc-label">覆盖方向</span>
        </div>
      </div>
      <div class="stat-cell">
        <div class="sc-icon sc-date"><i class="fas fa-calendar-day"></i></div>
        <div class="sc-body">
          <span class="sc-num sc-date-num">{{ latestDay }}</span>
          <span class="sc-label">最近收藏</span>
        </div>
      </div>
      <div class="stat-cell" v-if="noteCount">
        <div class="sc-icon sc-note"><i class="fas fa-pencil"></i></div>
        <div class="sc-body">
          <span class="sc-num">{{ noteCount }}</span>
          <span class="sc-label">有备注</span>
        </div>
      </div>
    </section>

    <!-- ═══ 收藏列表 ═══ -->
    <section class="zone-list">
      <!-- 加载态 -->
      <div v-if="savedLoading" class="loading-state">
        <i class="fas fa-spinner fa-spin"></i> 加载中…
      </div>

      <!-- 空态 -->
      <div v-else-if="!interviewSaved.length" class="empty-state">
        <div class="empty-icon-wrap"><i class="fas fa-star empty-icon"></i></div>
        <p class="empty-title">暂无面试收藏</p>
        <p class="empty-hint">在面试过程中可以收藏感兴趣的题目，方便日后回顾练习</p>
      </div>

      <!-- 收藏列表 -->
      <template v-else>
        <div class="saved-card" v-for="item in interviewSaved" :key="item.id">
          <div class="sc-top">
            <div class="sc-question">{{ item.question }}</div>
            <div class="sc-badges">
              <span class="tag-pill" :class="diffPillClass(item.difficulty)">{{ item.difficulty || '中等' }}</span>
              <span v-if="item.category" class="tag-pill gray"><i class="fas fa-layer-group"></i> {{ item.category }}</span>
            </div>
          </div>
          <div class="sc-meta">
            <span class="meta-item" v-if="item.source"><i class="fas fa-link"></i> {{ item.source }}</span>
            <span class="meta-item"><i class="fas fa-clock"></i> {{ item.created_at }}</span>
          </div>
          <div class="sc-note" v-if="item.note">
            <i class="fas fa-pencil"></i> {{ item.note }}
          </div>
          <div class="sc-actions">
            <button class="btn-outline btn-sm btn-primary-outline" @click="practiceItem(item)">
              <i class="fas fa-play"></i> 练习此题
            </button>
            <button class="btn-outline btn-sm btn-danger" @click="deleteInterviewSaved(item)">
              <i class="fas fa-trash-can"></i> 取消收藏
            </button>
          </div>
        </div>

        <!-- 分页 -->
        <div class="pagination-wrap" v-if="interviewSavedTotal > 20">
          <el-pagination layout="prev,pager,next" :total="interviewSavedTotal" :page-size="20"
            @current-change="p => loadInterviewSaved(p)" background />
        </div>
      </template>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import PageBanner from '../components/PageBanner.vue'

const router = useRouter()
const interviewSaved = ref([])
const interviewSavedTotal = ref(0)
const savedLoading = ref(false)

const categoryCount = computed(() => {
  const cats = new Set(interviewSaved.value.map(i => i.category).filter(Boolean))
  return cats.size
})
const noteCount = computed(() => interviewSaved.value.filter(i => i.note).length)

const latestDay = computed(() => {
  if (!interviewSaved.value.length) return '-'
  const dates = interviewSaved.value.map(i => i.created_at).filter(Boolean).sort().reverse()
  return dates[0]?.slice(0, 10) || '-'
})

async function loadInterviewSaved(page = 1) {
  savedLoading.value = true
  try {
    const { data } = await axios.get('/api/interview/saved-questions', { params: { page, page_size: 20 } })
    interviewSaved.value = data.items || []
    interviewSavedTotal.value = data.total || 0
  } catch { /* ignore */ }
  savedLoading.value = false
}
async function deleteInterviewSaved(row) {
  try {
    await axios.delete(`/api/interview/saved-questions/${row.id}`)
    ElMessage.success('已取消收藏')
    loadInterviewSaved()
  } catch { ElMessage.error('取消收藏失败') }
}

function practiceItem(item) {
  router.push({
    path: '/interview/session',
    query: { practice: item.id, question: item.question }
  })
}

function diffPillClass(d) {
  const m = { easy: 'green', 简单: 'green', medium: 'orange', 中等: 'orange', hard: 'red', 困难: 'red' }
  return m[d] || 'gray'
}

onMounted(() => { loadInterviewSaved() })
</script>

<style scoped>
.savedlist-page { }

/* ═══ 紧凑统计条 ═══ */
.stat-ribbon {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 6px;
  margin-bottom: 16px;
}
.stat-cell {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 5px 10px;
  transition: all 0.2s;
}
.stat-cell:hover {
  border-color: rgba(61,90,128,.2);
  box-shadow: 0 2px 8px rgba(61,90,128,.06);
}
.sc-icon {
  width: 22px; height: 22px;
  border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px;
  background: rgba(232,168,56,.1);
  color: #E8A838;
  flex-shrink: 0;
}
.sc-icon.sc-cat { background: rgba(61,90,128,.1); color: #3D5A80; }
.sc-icon.sc-date { background: rgba(191,168,149,.1); color: #BFA895; }
.sc-icon.sc-note { background: rgba(103,194,58,.1); color: #67c23a; }
.sc-body {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}
.sc-num { font-size: 15px; font-weight: 700; color: var(--text-heading); }
.sc-date-num { font-size: 12px; }
.sc-label { font-size: 10px; color: var(--text-muted); margin-top: 1px; }

/* ── 收藏卡片 ── */
.saved-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 16px 18px;
  margin-bottom: 10px;
  box-shadow: var(--shadow-sm);
  transition: all 0.25s;
  border: 1px solid var(--border-light);
}
.saved-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
  border-color: rgba(61,90,128,.15);
}

.sc-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 8px;
}
.sc-question {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-heading);
  line-height: 1.5;
  flex: 1;
  min-width: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.sc-badges {
  display: flex;
  gap: 5px;
  flex-shrink: 0;
  flex-wrap: wrap;
}

/* ── 元信息 ── */
.sc-meta {
  display: flex;
  gap: 14px;
  color: var(--text-muted);
  font-size: 11px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}
.meta-item {
  display: flex;
  align-items: center;
  gap: 3px;
}
.meta-item i { font-size: 10px; }

/* ── 备注 ── */
.sc-note {
  font-size: 12px;
  color: var(--text-body);
  background: rgba(61,90,128,.04);
  border-radius: var(--radius-sm);
  padding: 6px 10px;
  margin-bottom: 10px;
  border: 1px solid rgba(61,90,128,.08);
  display: flex;
  align-items: flex-start;
  gap: 5px;
}
.sc-note i { color: #BFA895; font-size: 11px; margin-top: 1px; }

/* ── 操作按钮 ── */
.sc-actions {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

/* ── Banner 返回按钮 ── */
.banner-back-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,.12);
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255,255,255,.15);
  color: #fff;
  padding: 7px 16px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all .2s;
}
.banner-back-btn:hover { background: rgba(255,255,255,.2); }

.btn-sm { padding: 4px 10px !important; font-size: 11px !important; }
.btn-primary-outline { border-color: #3D5A80 !important; color: #3D5A80 !important; }
.btn-danger { border-color: #fecaca !important; color: #dc2626 !important; }

/* ── 分页 ── */
.pagination-wrap {
  display: flex;
  justify-content: center;
  padding: 16px 0;
}

/* ── 空态 ── */
.empty-icon-wrap {
  width: 52px; height: 52px;
  border-radius: 50%;
  background: rgba(232,168,56,.08);
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 10px;
}
.empty-icon { font-size: 22px; color: #E8A838; }
</style>