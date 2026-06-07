<template>
  <div class="fm-center-page">
    <div class="fm-card">
    <!-- ═══ 返回按钮 ═══ -->
    <button class="back-circle-btn" type="button" aria-label="返回上一页" @click="goBack">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>
    </button>

    <!-- ═══ 标题+小猫 ═══ -->
    <div class="fm-header">
      <img src="/src/assets/exam-cat.png" class="fm-cat" alt="" />
      <h1 class="fm-title">我的收藏</h1>
    </div>

    <!-- ═══ 搜索栏 ═══ -->
    <div class="search-section">
      <div class="search-wrap">
        <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input
          v-model="searchText"
          type="text"
          class="search-input"
          placeholder="搜索收藏的笔试题目…"
          autocomplete="off"
        />
      </div>
    </div>

    <!-- ═══ 空状态 / 列表 ═══ -->
    <div v-if="loading" class="loading-state">加载中…</div>
    <div v-else-if="!filteredItems.length" class="empty-state">
      <p>{{ searchText ? '没有匹配的收藏' : '还没有收藏笔试题目' }}</p>
      <p class="empty-hint">完成笔试练习后可收藏题目到这里</p>
    </div>
    <div v-else class="fav-list">
<div v-for="(item, idx) in filteredItems" :key="item.id || idx" class="fav-item" @click="toggleItem(item.id || idx)">
        <div class="fi-q">{{ item.question }}</div>
        <div class="fi-meta">
          <span class="fi-tag" v-if="item.career">{{ item.career }}</span>
          <span class="fi-tag fi-tag-kp" v-if="item.category">{{ item.category }}</span>
          <span class="fi-tag fi-tag-cnt" v-if="item.wrong_count > 0">错{{ item.wrong_count }}次</span>
          <span class="fi-date" v-if="item.last_wrong_at">{{ item.last_wrong_at.slice(0,10) }}</span>
        </div>
        <!-- ═══ 展开详情 ═══ -->
        <div v-if="(expandedId === item.id || expandedId === idx) && item.options" class="fi-detail">
          <div class="fi-result" :class="item.user_answer === item.correct_answer ? 'fi-result-right' : 'fi-result-wrong'">
            {{ item.user_answer === item.correct_answer ? '✓ 回答正确' : '✗ 回答错误' }}
          </div>
          <div class="fi-choice-row" v-if="item.user_answer && item.user_answer !== item.correct_answer">
            <span class="fi-lbl">你的答案：</span><span class="fi-val fi-val-user">{{ item.user_answer }}. {{ getOptText(item.options, item.user_answer) }}</span>
          </div>
          <div class="fi-choice-row">
            <span class="fi-lbl">正确答案：</span><span class="fi-val fi-val-correct">{{ item.correct_answer }}. {{ getOptText(item.options, item.correct_answer) }}</span>
          </div>
          <div class="fi-opt-list" v-if="item.options.length > 2">
            <div v-for="opt in item.options" :key="opt.key" class="fi-opt"
              :class="{ 'fi-opt-correct': opt.key === item.correct_answer, 'fi-opt-user': opt.key === item.user_answer && opt.key !== item.correct_answer }">
              <span class="fi-opt-key">{{ opt.key }}.</span>
              <span class="fi-opt-val">{{ opt.value }}</span>
            </div>
          </div>
          <div v-if="item.analysis" class="fi-analysis">
            <span class="fi-analysis-lbl">📖 解析</span>
            <p>{{ item.analysis }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══ 分页 ═══ -->
    <el-pagination
      v-if="totalItems > pageSize"
      layout="prev, pager, next"
      :total="totalItems"
      :page-size="pageSize"
      background
      small
      style="margin-top:16px;justify-content:center"
    />
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

const el = ElMessage

// ── 数据 ──
const searchText = ref('')
const loading = ref(false)
const examItems = ref([])
const pageSize = 10
const expandedId = ref(null)
function toggleItem(id) {
  expandedId.value = expandedId.value === id ? null : id
}
function getOptText(options, key) {
  if (!options) return ''
  const opt = options.find(o => o.key === key)
  return opt ? opt.value : ''
}

// ── 过滤：只看笔试题目 ──
const filteredItems = computed(() => {
  let items = examItems.value
  const q = searchText.value.trim().toLowerCase()
  if (q) {
    items = items.filter(i => {
      const text = (i.question || i.title || '').toLowerCase()
      return text.includes(q)
    })
  }
  return items
})
const totalItems = computed(() => filteredItems.value.length)

// ── 操作 ──
function goBack() {
  if (window.history.length > 1) router.back()
  else router.push('/dashboard')
}

// ── 加载 ──
async function loadExamSaved() {
  try {
    const { data } = await axios.get('/api/exam/wrong-questions', { params: { page: 1, page_size: 50 } })
    examItems.value = data.wrong_questions || []
  } catch { /* ignore */ }
}

onMounted(async () => {
  loading.value = true
  await loadExamSaved()
  loading.value = false
})
</script>

<style scoped>
/* ═══════ 页面居中容器 ═══════ */
.fm-center-page {
  --text-heading: #1e293b;
  --text-body: #475569;
  --text-muted: #94a3b8;
  --border: #bfdbfe;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100%;
  padding: 32px 0;
}
.fm-card {
  width: min(720px, calc(100vw - 60px));
  padding: 52px 32px 36px;
  background: #fff;
  border: 1.5px dashed var(--border);
  border-radius: 22px;
  box-shadow: 0 16px 36px rgba(37,99,235,.06);
  position: relative;
  overflow: hidden;
}
/* ═══ 折角 ═══ */
.fm-card::before {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 48px; height: 48px;
  background: linear-gradient(135deg, transparent 50%, #EFF6FF 50%);
  border-radius: 0 22px 0 0;
}
.fm-card::after {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 48px; height: 48px;
  background: linear-gradient(135deg, transparent 50%, #BFDBFE 50%);
  border-radius: 0 22px 0 0;
  opacity: .15;
}

/* ═══ 标题区 ═══ */
.fm-header { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.fm-cat { width: 36px; height: 36px; object-fit: contain; }
.fm-title { font-size: 20px; font-weight: 900; color: var(--text-heading); }

/* ═══ 返回按钮 ═══ */
.back-circle-btn {
  position: absolute;
  left: 0;
  top: 8px;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  border: 2px solid #2563EB;
  border-radius: 999px;
  background: #fff;
  color: #2563EB;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: background .2s;
}
.back-circle-btn:hover { background: #EFF6FF; }

/* ═══ 搜索栏 ═══ */
.search-section { margin-bottom: 16px; }
.search-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: #F8FAFF;
  border: 1px solid #DBEAFE;
  border-radius: 12px;
}
.search-icon { color: #94A3B8; flex-shrink: 0; }
.search-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 14px;
  color: #1E293B;
}
.search-input::placeholder { color: #94A3B8; }

/* ═══ 空状态 ═══ */
.empty-state { text-align: center; padding: 40px 0 20px; color: var(--text-body); }
.empty-state p { margin: 6px 0; }
.empty-hint { font-size: 13px; color: var(--text-muted); }
.loading-state { text-align: center; padding: 40px; color: var(--text-muted); }

/* ═══ 收藏列表 ═══ */
.fav-list { display: flex; flex-direction: column; gap: 8px; }
.fav-item {
  padding: 14px 16px;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  transition: box-shadow .2s;
}
.fav-item:hover { box-shadow: 0 4px 12px rgba(37,99,235,.06); }
.fi-q { font-size: 14px; font-weight: 600; color: var(--text-heading); margin-bottom: 6px; line-height: 1.6; }
.fi-meta { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.fi-tag {
  font-size: 11px; padding: 2px 10px; border-radius: 99px;
  background: #EFF6FF; color: #2563EB; font-weight: 600;
}
.fi-tag-kp { background: #F0FDF4; color: #16A34A; }
.fi-tag-cnt { background: #FEF2F2; color: #DC2626; }
.fi-date { font-size: 12px; color: var(--text-muted); margin-left: auto; }

/* ═══ 展开详情 ═══ */
.fi-detail {
  margin-top: 12px;
  padding: 14px 16px;
  background: #F8FAFF;
  border-radius: 14px;
  border: 1px solid #DBEAFE;
}
.fi-result {
  padding: 8px 12px;
  border-radius: 10px;
  font-weight: 800;
  font-size: 14px;
  margin-bottom: 10px;
}
.fi-result-right { background: #F0FDF4; color: #16A34A; }
.fi-result-wrong { background: #FEF2F2; color: #DC2626; }
.fi-choice-row { display: flex; align-items: baseline; gap: 4px; font-size: 13px; margin-bottom: 6px; }
.fi-lbl { font-weight: 700; color: #475569; flex-shrink: 0; }
.fi-val { color: #1E293B; flex: 1; }
.fi-val-user { color: #DC2626; }
.fi-val-correct { color: #16A34A; }
.fi-opt-list { margin-top: 8px; }
.fi-opt { display: flex; gap: 6px; padding: 4px 8px; margin-bottom: 2px; border-radius: 6px; font-size: 13px; }
.fi-opt-correct { background: #F0FDF4; }
.fi-opt-user { background: #FEF2F2; }
.fi-opt-key { font-weight: 700; color: #475569; flex-shrink: 0; }
.fi-opt-val { color: #1E293B; }
.fi-analysis { margin-top: 12px; padding-top: 12px; border-top: 1px solid #DBEAFE; }
.fi-analysis-lbl { display: block; font-weight: 700; font-size: 13px; color: #2563EB; margin-bottom: 6px; }
.fi-analysis p { font-size: 13px; color: #475569; line-height: 1.7; margin: 0; }
</style>
