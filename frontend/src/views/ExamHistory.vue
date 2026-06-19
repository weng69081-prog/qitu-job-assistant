<template>
  <div class="eh-center-page">
    <div class="eh-card">
      <!-- ═══ 返回按钮 ═══ -->
      <button class="back-circle-btn" @click="$router.push('/exam-practice')">
        <ArrowLeft :size="16" class="icon-blue" /> 返回
      </button>

<!-- ═══ 标题+小猫 ═══ -->
      <div class="eh-header">
        <img src="/src/assets/exam-cat.png" class="eh-cat" alt="" />
        <h1 class="eh-title">练习记录</h1>
      </div>

      <div class="eh-summary" v-if="records.length">
        <span>共 <b>{{ records.length }}</b> 次练习</span>
        <span>总刷题 <b>{{ totalQ }}</b> 道</span>
        <span>平均正确率 <b>{{ avgAccuracy }}%</b></span>
      </div>

      <!-- 加载态 -->
      <div v-if="loading" class="eh-loading">
        <div v-for="i in 3" :key="i" class="skeleton-row" />
      </div>

      <!-- 空状态 -->
      <div v-else-if="records.length === 0" class="eh-empty">
        <FileClock :size="32" class="icon-blue" style="opacity:.4" />
        <p>还没有练习记录</p>
        <p class="eh-hint">完成一次笔试练习后，记录会自动保存在这里</p>
      </div>

      <!-- 列表 -->
      <div v-else class="eh-list">
        <div v-for="r in records" :key="r.id" class="eh-record" @click="toggleDetail(r.id)">
          <div class="eh-r-left">
            <div class="eh-r-date">{{ r.created_at || '—' }}</div>
            <div class="eh-r-meta">
              <span class="eh-tag">{{ r.career || '通用' }}</span>
              <span class="eh-tag eh-tag-mode">{{ r.mode || '随机刷题' }}</span>
            </div>
          </div>
          <div class="eh-r-stats">
            <div class="eh-stat"><span class="eh-num">{{ r.total_questions }}</span><span class="eh-lbl">题</span></div>
            <div class="eh-stat"><span class="eh-num" :style="{color: r.accuracy >= 70 ? '#2563EB' : '#0EA5E9'}">{{ r.accuracy }}%</span><span class="eh-lbl">正确率</span></div>
            <div class="eh-stat"><span class="eh-num">{{ Math.floor((r.duration_seconds || 0) / 60) }}′</span><span class="eh-lbl">用时</span></div>
          </div>
          <div class="eh-arrow"><ChevronRight :size="14" class="icon-blue" /></div>
          <!-- ═══ 展开详情 ═══ -->
          <div v-if="expandedId === r.id" class="eh-detail">
            <div v-if="detailLoading" class="eh-d-loading">加载中...</div>
            <div v-else-if="detailData" class="eh-d-body">
              <div class="eh-d-header">
                <span>正确 <b>{{ detailData.correct_count || 0 }}</b> /  错误 <b>{{ detailData.wrong_count || 0 }}</b></span>
              </div>
              <div v-if="detailData.answers && detailData.answers.length" class="eh-d-list">
                <div v-for="(a, i) in detailData.answers" :key="i" class="eh-d-item" :class="a.is_correct ? 'eh-d-correct' : 'eh-d-wrong'">
                  <div class="eh-d-q">{{ i+1 }}. {{ a.question || a.content || '题目' }}</div>
                  <div class="eh-d-ans">
                    <span v-if="!a.is_correct">✗ 你的答案：{{ a.user_answer || '—' }}</span>
                    <span v-if="!a.is_correct" class="eh-d-correction">✓ 正确答案：{{ a.correct_answer }}</span>
                    <span v-else>✓ 正确</span>
                  </div>
                  <div class="eh-d-analysis" v-if="a.analysis">
                    <i class="fa-solid fa-book-open"></i> {{ a.analysis }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ArrowLeft, FileClock, ChevronRight } from 'lucide-vue-next'
const router = useRouter()
const records = ref([])
const loading = ref(true)
const expandedId = ref(null)
const detailData = ref(null)
const detailLoading = ref(false)

async function toggleDetail(rid) {
  if (expandedId.value === rid) {
    expandedId.value = null; detailData.value = null; return
  }
  expandedId.value = rid; detailLoading.value = true; detailData.value = null
  try {
    const { data } = await axios.get(`/api/exam/records/${rid}`)
    detailData.value = data
  } catch { detailData.value = null }
  detailLoading.value = false
}

function viewDetail(rid) { toggleDetail(rid) }
const totalQ = computed(() => records.value.reduce((s, r) => s + (r.total_questions || 0), 0))
const avgAccuracy = computed(() => {
  if (!records.value.length) return 0
  const sum = records.value.reduce((s, r) => s + (r.accuracy || 0), 0)
  return (sum / records.value.length).toFixed(1)
})

async function loadRecords() {
  try {
    const { data } = await axios.get('/api/exam/records')
    records.value = data.records || data.data || []
  } catch {
    records.value = []
  } finally {
    loading.value = false
  }
}

onMounted(loadRecords)
</script>

<style scoped>
/* ═══════ 页面居中容器 ═══════ */
.eh-center-page {
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
.eh-card {
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
.eh-card::before {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 48px; height: 48px;
  background: linear-gradient(135deg, transparent 50%, #EFF6FF 50%);
  border-radius: 0 22px 0 0;
}
.eh-card::after {
  content: '';
  position: absolute;
  top: 0; right: 0;
  width: 48px; height: 48px;
  background: linear-gradient(135deg, transparent 50%, #BFDBFE 50%);
  border-radius: 0 22px 0 0;
  opacity: .15;
}

/* ═══ 标题区 ═══ */
.eh-header { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.eh-cat { width: 36px; height: 36px; object-fit: contain; }
.eh-title { font-size: 20px; font-weight: 900; color: var(--text-heading); }
.eh-summary { display: flex; gap: 20px; font-size: 13px; color: var(--text-muted); margin-bottom: 16px; flex-wrap: wrap; }

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

/* ═══ 空状态 ═══ */
.eh-empty { text-align: center; padding: 40px 0; color: var(--text-body); }
.eh-empty p { margin: 8px 0; }
.eh-hint { font-size: 13px; color: var(--text-muted); }

/* ═══ 骨架 ═══ */
.skeleton-row {
  height: 60px;
  border-radius: 14px;
  background: linear-gradient(90deg, #F1F5F9 25%, #E2E8F0 50%, #F1F5F9 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  margin-bottom: 10px;
}
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* ═══ 记录列表 ═══ */
.eh-list { display: flex; flex-direction: column; gap: 12px; }
.eh-record {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px 20px;
  border-radius: 18px;
  border: 1px solid #E2E8F0;
  background: #fff;
  cursor: pointer;
  transition: box-shadow .2s, transform .2s;
}
.eh-record:hover { box-shadow: 0 8px 20px rgba(37,99,235,.08); transform: translateX(3px); }
.eh-r-left { flex: 1; min-width: 0; }
.eh-r-date { font-size: 13px; font-weight: 700; color: var(--text-heading); margin-bottom: 3px; }
.eh-r-meta { display: flex; gap: 6px; flex-wrap: wrap; }
.eh-tag {
  font-size: 11px; padding: 2px 10px; border-radius: 99px;
  background: #EFF6FF; color: #2563EB; font-weight: 600;
}
.eh-tag-mode { background: #F0FDF4; color: #16A34A; }
.eh-r-stats { display: flex; gap: 14px; flex-shrink: 0; }
.eh-stat { text-align: center; }
.eh-num { display: block; font-size: 15px; font-weight: 800; color: var(--text-heading); }
.eh-lbl { font-size: 11px; color: var(--text-muted); }
.eh-arrow { flex-shrink: 0; opacity: .35; }

/* ═══ 展开详情 ═══ */
.eh-detail { width: 100%; margin-top: 10px; padding-top: 10px; border-top: 1px solid #E2E8F0; }
.eh-d-loading { text-align: center; padding: 16px; color: #94A3B8; font-size: 13px; }
.eh-d-header { font-size: 13px; color: #475569; margin-bottom: 8px; }
.eh-d-list { display: flex; flex-direction: column; gap: 6px; }
.eh-d-item { padding: 10px 14px; border-radius: 12px; font-size: 13px; }
.eh-d-correct { background: #F0FDF4; }
.eh-d-wrong { background: #FEF2F2; }
.eh-d-q { font-weight: 600; color: #1E293B; margin-bottom: 4px; line-height: 1.5; }
.eh-d-ans { display: flex; gap: 10px; flex-wrap: wrap; font-size: 12px; }
.eh-d-analysis {
  margin-top: 6px;
  padding: 6px 10px;
  background: #f1f5f9;
  border-radius: 8px;
  font-size: 12px;
  color: #475569;
  line-height: 1.5;
}
.eh-d-correction { color: #16A34A; font-weight: 700; }
</style>