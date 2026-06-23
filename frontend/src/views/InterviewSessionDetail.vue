<template>
  <div class="report-page">
    <!-- ═══ Back Button ═══ -->
    <div class="section-header">
      <div class="section-title">
        <el-button text @click="$router.back()" class="back-btn">
          <ArrowLeft :size="16" class="icon-blue" />
          返回面试记录
        </el-button>
      </div>
    </div>

    <!-- ═══ Loading ═══ -->
    <div v-if="loading" class="loading-state">
      <Loader :size="16" class="icon-blue" /> 加载中…
    </div>

    <template v-if="!loading && session">
      <!-- ════════════════════════════════════════════════════════ -->
      <!-- SECTION 1: REPORT HEADER — 综合评分圆形进度 + 核心统计 -->
      <!-- ════════════════════════════════════════════════════════ -->
      <div class="card core-stats-card">
        <div class="core-score-section">
          <div class="score-ring" :style="bigRingGradient">
            <div class="score-ring-inner">
              <span class="score-number">{{ overallScore }}</span>
              <span class="score-unit">/100</span>
            </div>
          </div>
          <span class="score-label">综合评分</span>
        </div>
        <div class="core-stats-grid grid-2">
          <div class="stat-card">
            <ListChecks :size="16" class="icon-blue" />
            <div class="stat-info">
              <span class="stat-value">{{ session.total_questions || 0 }}</span>
              <span class="stat-label">答题数</span>
            </div>
          </div>
          <div class="stat-card">
            <Trophy :size="16" class="icon-blue" />
            <div class="stat-info">
              <span class="stat-value stat-high">{{ highestScore }}</span>
              <span class="stat-label">最高分</span>
            </div>
          </div>
          <div class="stat-card">
            <ArrowDown :size="16" class="icon-blue" />
            <div class="stat-info">
              <span class="stat-value stat-low">{{ lowestScore }}</span>
              <span class="stat-label">最低分</span>
            </div>
          </div>
          <div class="stat-card">
            <Clock :size="16" class="icon-blue" />
            <div class="stat-info">
              <span class="stat-value">{{ relativeTime }}</span>
              <span class="stat-label">用时</span>
            </div>
          </div>
        </div>
      </div>

      <!-- ════════════════════════════════════════════════════════ -->
      <!-- SECTION 2: 维度分析 — 雷达图 + 各维度评分条           -->
      <!-- ════════════════════════════════════════════════════════ -->
      <div class="card dim-analysis-card">
        <div class="section-header">
          <div class="section-title">
            <PieChart :size="16" class="icon-blue" />
            维度分析
          </div>
        </div>

        <!-- Radar Chart -->
        <div class="radar-section" v-if="Object.keys(dimensions).length > 0">
          <div class="radar-chart-wrap">
            <svg viewBox="0 0 200 200" class="radar-svg">
              <!-- Grid polygons -->
              <polygon
                v-for="(g, gi) in radarGrids"
                :key="'g' + gi"
                :points="g"
                fill="none"
                stroke="var(--border, #e5e7eb)"
                stroke-width="0.8"
              />
              <!-- Axis lines -->
              <line
                v-for="(a, ai) in radarAxes"
                :key="'a' + ai"
                :x1="100" :y1="100"
                :x2="a.x2" :y2="a.y2"
                stroke="var(--border, #e5e7eb)"
                stroke-width="0.6"
              />
              <!-- Data polygon -->
              <polygon
                :points="radarDataPoints"
                fill="var(--primary, #2563EB)"
                fill-opacity="0.15"
                stroke="var(--primary, #2563EB)"
                stroke-width="1.8"
              />
              <!-- Data points -->
              <circle
                v-for="(pt, pi) in radarPoints"
                :key="'pt' + pi"
                :cx="pt.cx" :cy="pt.cy"
                r="3"
                fill="var(--primary, #2563EB)"
              />
              <!-- Labels -->
              <text
                v-for="(lb, li) in radarLabels"
                :key="'lb' + li"
                :x="lb.x" :y="lb.y"
                text-anchor="middle"
                dominant-baseline="middle"
                font-size="9"
                fill="var(--text-body, #4b5563)"
                font-weight="500"
              >{{ lb.text }}</text>
            </svg>
          </div>
        </div>

        <!-- Dimension Score Bars -->
        <div class="dim-bar-chart">
          <div v-for="(val, key, i) in dimensions" :key="key" class="dim-bar-row">
            <span class="dim-bar-label">{{ key }}</span>
            <div class="dim-bar-track">
              <div
                class="dim-bar-fill"
                :style="{ width: val + '%', background: dimColors[i % dimColors.length] }"
              ></div>
            </div>
            <span class="dim-bar-value" :style="{ color: barColor(val) }">{{ val.toFixed(1) }}</span>
          </div>
          <div v-if="Object.keys(dimensions).length === 0" class="empty-state">
            <BarChart :size="16" class="icon-blue" /> 暂无维度数据
          </div>
        </div>

        <!-- Small Ring Charts (kept from original) -->
        <div class="ring-charts-row">
          <div class="ring-chart-item">
            <div class="ring-chart" :style="ringGradient(75)"></div>
            <span class="ring-chart-label"><Mic :size="16" class="icon-blue" /> 语音评分</span>
            <span class="ring-chart-value">75</span>
          </div>
          <div class="ring-chart-item">
            <div class="ring-chart" :style="ringGradient(averageScore)"></div>
            <span class="ring-chart-label"><MessageSquare :size="16" class="icon-blue" /> 回答评分</span>
            <span class="ring-chart-value">{{ averageScore }}</span>
          </div>
          <div class="ring-chart-item">
            <div class="ring-chart" :style="ringGradient(averageScore, '#2563EB')"></div>
            <span class="ring-chart-label"><BarChart :size="16" class="icon-blue" /> 综合表现</span>
            <span class="ring-chart-value">{{ averageScore }}</span>
          </div>
        </div>
      </div>

      <!-- ════════════════════════════════════════════════════════ -->
      <!-- SECTION 3: 答题详情 — 每题评分 + 答案对比              -->
      <!-- ════════════════════════════════════════════════════════ -->
      <div class="card qa-card">
        <div class="section-header">
          <div class="section-title">
            <FileText :size="16" class="icon-blue" />
            答题详情
          </div>
          <span class="tag-pill tag-count">{{ qaItems.length }} 题</span>
        </div>

        <div v-if="qaItems.length === 0" class="empty-state">
          <FileWarning :size="16" class="icon-blue" /> 暂无详细记录
        </div>

        <div v-for="(qa, idx) in qaItems" :key="idx" class="qa-item">
          <div class="qa-top-row">
            <div class="qa-left">
              <span class="qa-badge">Q{{ idx + 1 }}</span>
              <span class="qa-score-badge" :style="{ background: scoreBg(qa.score || 0) }">
                <Star :size="16" class="icon-blue" /> {{ qa.score || 0 }}分
              </span>
            </div>
          </div>
          <div class="qa-body">
            <div class="qa-question-section">
              <span class="qa-label">
                <CircleHelp :size="16" class="icon-blue" /> 题目
              </span>
              <div class="qa-text" :class="{ 'qa-collapsed': !expandedQA[idx + '-q'] }">
                {{ qa.question || '暂无题目' }}
              </div>
              <button v-if="(qa.question || '').length > 100" class="qa-expand-btn" @click="toggleQA(idx + '-q')">
                <ChevronUp :size="16" class="icon-blue" :class="expandedQA[idx + '-q'] ? 'fas fa-chevron-up' : 'fas fa-chevron-down'" />
                {{ expandedQA[idx + '-q'] ? '收起' : '展开' }}
              </button>
            </div>
            <div class="qa-answer-section">
              <span class="qa-label">
                <MessageSquare :size="16" class="icon-blue" /> 回答
              </span>
              <div v-if="qa.answer" class="qa-text" :class="{ 'qa-collapsed': !expandedQA[idx + '-a'] }">
                {{ qa.answer }}
              </div>
              <div v-else class="qa-empty-text">
                <Info :size="16" class="icon-blue" /> 暂无详细记录
              </div>
              <button v-if="(qa.answer || '').length > 100" class="qa-expand-btn" @click="toggleQA(idx + '-a')">
                <ChevronUp :size="16" class="icon-blue" :class="expandedQA[idx + '-a'] ? 'fas fa-chevron-up' : 'fas fa-chevron-down'" />
                {{ expandedQA[idx + '-a'] ? '收起' : '展开' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- ════════════════════════════════════════════════════════ -->
      <!-- SECTION 4: 综合建议 — strengths / weaknesses / suggestions -->
      <!-- ════════════════════════════════════════════════════════ -->
      <div class="card suggestion-card">
        <div class="section-header">
          <div class="section-title">
            <Lightbulb :size="16" class="icon-blue" />
            综合建议
          </div>
        </div>

        <div class="grid-3 analysis-cards-row">
          <div class="analysis-card analysis-strength">
            <div class="analysis-card-header">
              <ThumbsUp :size="16" class="icon-blue" />
              <span class="analysis-card-title">优势亮点</span>
            </div>
            <ul class="analysis-list">
              <li v-for="(s, i) in strengths" :key="i">{{ s }}</li>
              <li v-if="strengths.length === 0" class="analysis-empty">
                <Minus :size="16" class="icon-blue" /> 暂无数据
              </li>
            </ul>
          </div>
          <div class="analysis-card analysis-weakness">
            <div class="analysis-card-header">
              <TriangleAlert :size="16" class="icon-blue" />
              <span class="analysis-card-title">待改进</span>
            </div>
            <ul class="analysis-list">
              <li v-for="(s, i) in weaknesses" :key="i">{{ s }}</li>
              <li v-if="weaknesses.length === 0" class="analysis-empty">
                <Minus :size="16" class="icon-blue" /> 暂无数据
              </li>
            </ul>
          </div>
          <div class="analysis-card analysis-suggestion">
            <div class="analysis-card-header">
              <WandSparkles :size="16" class="icon-blue" />
              <span class="analysis-card-title">改进建议</span>
            </div>
            <ul class="analysis-list">
              <li v-for="(s, i) in suggestions" :key="i">{{ s }}</li>
              <li v-if="suggestions.length === 0" class="analysis-empty">
                <Minus :size="16" class="icon-blue" /> 暂无数据
              </li>
            </ul>
          </div>
        </div>

        <!-- Special Analysis Grid (kept from original) -->
        <div class="special-grid grid-4">
          <div class="special-card">
            <div class="special-circle" :style="ringGradient(specialScores.emotion, '#2563EB')">
              <div class="special-circle-inner">
                <Smile :size="16" class="icon-blue" />
              </div>
            </div>
            <span class="special-label">情绪分析</span>
            <span class="special-score">{{ specialScores.emotion }}</span>
          </div>
          <div class="special-card">
            <div class="special-circle" :style="ringGradient(specialScores.body, '#2563EB')">
              <div class="special-circle-inner">
                <User :size="16" class="icon-blue" />
              </div>
            </div>
            <span class="special-label">肢体分析</span>
            <span class="special-score">{{ specialScores.body }}</span>
          </div>
          <div class="special-card">
            <div class="special-circle" :style="ringGradient(specialScores.overall, '#2563EB')">
              <div class="special-circle-inner">
                <BarChart :size="16" class="icon-blue" />
              </div>
            </div>
            <span class="special-label">整体分析</span>
            <span class="special-score">{{ specialScores.overall }}</span>
          </div>
          <div class="special-card">
            <div class="special-circle" :style="ringGradient(specialScores.comprehensive, '#2563EB')">
              <div class="special-circle-inner">
                <Trophy :size="16" class="icon-blue" />
              </div>
            </div>
            <span class="special-label">综合表现</span>
            <span class="special-score">{{ specialScores.comprehensive }}</span>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const API = '/api'

const session = ref(null)
const loading = ref(true)

// Expand states for Q&A
const expandedQA = ref({})
function toggleQA(idx) { expandedQA.value[idx] = !expandedQA.value[idx] }

// Helpers
function barColor(val) { return val >= 70 ? '#67c23a' : val >= 50 ? '#e6a23c' : '#f56c6c' }
function scoreBg(val) { return val >= 70 ? '#67c23a' : val >= 50 ? '#e6a23c' : '#f56c6c' }
function ringGradient(val, color = '#2563EB') {
  const pct = Math.min(100, Math.max(0, val))
  return `background: conic-gradient(${color} 0deg ${pct * 3.6}deg, #f0f0f0 ${pct * 3.6}deg 360deg)`
}
const dimColors = ['#2563EB', '#2563EB', '#2563EB', '#2563EB', '#2563EB']

// Computed
const overallScore = computed(() => {
  const avg = session.value?.average_score
  return avg != null ? parseFloat(avg.toFixed(1)) : 0
})

const averageScore = computed(() => {
  const avg = session.value?.average_score
  return avg != null ? Math.round(avg) : 0
})

const highestScore = computed(() => {
  const h = session.value?.highest_score
  return h != null ? h : 0
})

const lowestScore = computed(() => {
  const l = session.value?.lowest_score
  return l != null ? l : 0
})

const qaItems = computed(() => {
  // Try qa_items first, fall back to answers
  return session.value?.qa_items || session.value?.answers || []
})

const dimensions = computed(() => {
  const raw = session.value?.dimensions || {}
  // 兼容两种格式：纯数字 或 {score: 数字}
  const normalized = {}
  for (const [k, v] of Object.entries(raw)) {
    normalized[k] = typeof v === 'object' && v !== null ? (v.score ?? 0) : (v ?? 0)
  }
  return normalized
})

const strengths = computed(() => {
  return session.value?.strengths || []
})

const weaknesses = computed(() => {
  return session.value?.weaknesses || []
})

const suggestions = computed(() => {
  return session.value?.suggestions || []
})

const emotions = computed(() => {
  return session.value?.emotions || []
})

const relativeTime = computed(() => {
  if (!session.value?.createdAt && !session.value?.date) return '--'
  const dateStr = session.value.createdAt || session.value.date
  const created = new Date(dateStr)
  const now = new Date()
  const diffMs = now - created
  const diffMin = Math.floor(diffMs / 60000)
  if (diffMin < 1) return '刚刚'
  if (diffMin < 60) return `${diffMin}分钟`
  const diffHr = Math.floor(diffMin / 60)
  if (diffHr < 24) return `${diffHr}小时`
  const diffDay = Math.floor(diffHr / 24)
  return `${diffDay}天前`
})

const bigRingGradient = computed(() => {
  const pct = Math.min(100, Math.max(0, overallScore.value))
  return { background: `conic-gradient(#2563EB 0deg ${pct * 3.6}deg, #e8e8f8 ${pct * 3.6}deg 360deg)` }
})

const specialScores = computed(() => {
  // Derive from available data
  const dims = dimensions.value
  const avg = averageScore.value
  const dimVals = Object.values(dims)
  const dimAvg = dimVals.length > 0 ? Math.round(dimVals.reduce((a, b) => a + b, 0) / dimVals.length) : avg

  // Real emotion score from accumulated camera readings
  const emoList = emotions.value
  let emotionScore = avg
  if (emoList.length > 0) {
    const weights = { '开心': 90, '自信': 85, '平静': 75, '困惑': 50, '紧张': 35, '焦虑': 30 }
    const sum = emoList.reduce((acc, e) => acc + (weights[e.emotion] || 60), 0)
    emotionScore = Math.round(sum / emoList.length)
  }

  return {
    emotion: Math.min(100, Math.max(0, emotionScore)),
    body: Math.min(100, Math.max(0, dimAvg + 3)),
    overall: Math.min(100, Math.max(0, dimAvg)),
    comprehensive: Math.min(100, Math.max(0, avg))
  }
})

// ─── Radar Chart Computed ───
const dimKeys = computed(() => Object.keys(dimensions.value))
const dimValsArr = computed(() => Object.values(dimensions.value))

const radarGrids = computed(() => {
  const keys = dimKeys.value
  if (keys.length < 3) return []
  const n = keys.length
  const levels = [0.25, 0.5, 0.75, 1]
  return levels.map(level => {
    return keys.map((_, i) => {
      const angle = (Math.PI * 2 * i) / n - Math.PI / 2
      const r = 80 * level
      const x = 100 + r * Math.cos(angle)
      const y = 100 + r * Math.sin(angle)
      return `${x},${y}`
    }).join(' ')
  })
})

const radarAxes = computed(() => {
  const keys = dimKeys.value
  if (keys.length < 3) return []
  const n = keys.length
  return keys.map((_, i) => {
    const angle = (Math.PI * 2 * i) / n - Math.PI / 2
    return { x2: 100 + 80 * Math.cos(angle), y2: 100 + 80 * Math.sin(angle) }
  })
})

const radarDataPoints = computed(() => {
  const vals = dimValsArr.value
  const keys = dimKeys.value
  if (keys.length < 3) return ''
  const n = keys.length
  return keys.map((_, i) => {
    const angle = (Math.PI * 2 * i) / n - Math.PI / 2
    const r = (vals[i] / 100) * 80
    const x = 100 + r * Math.cos(angle)
    const y = 100 + r * Math.sin(angle)
    return `${x},${y}`
  }).join(' ')
})

const radarPoints = computed(() => {
  const vals = dimValsArr.value
  const keys = dimKeys.value
  if (keys.length < 3) return []
  const n = keys.length
  return keys.map((_, i) => {
    const angle = (Math.PI * 2 * i) / n - Math.PI / 2
    const r = (vals[i] / 100) * 80
    return { cx: 100 + r * Math.cos(angle), cy: 100 + r * Math.sin(angle) }
  })
})

const radarLabels = computed(() => {
  const keys = dimKeys.value
  if (keys.length < 3) return []
  const n = keys.length
  return keys.map((key, i) => {
    const angle = (Math.PI * 2 * i) / n - Math.PI / 2
    const r = 92
    return {
      x: 100 + r * Math.cos(angle),
      y: 100 + r * Math.sin(angle),
      text: key
    }
  })
})

onMounted(async () => {
  try {
    const id = route.params.id
    const { data } = await axios.get(`${API}/interview/session/${id}`)
    session.value = data
  } catch { /* ignore */ }
  loading.value = false
})
</script>

<style scoped>
/* ═══════════════════════════════════════════
   Report Page — InterviewSessionDetail
   Design: new design system with CSS variables
   ═══════════════════════════════════════════ */

/* ─── Page Layout ─── */
.report-page {
  width: min(1100px, calc(100vw - var(--sidebar-width) - 40px));
  margin: 0 auto;
  padding: 0 0 2.4rem;
}

/* ─── Back Button ─── */
.back-btn {
  padding: 0 4px;
  font-size: 0.95rem;
}
.back-btn i {
  margin-right: 6px;
  font-size: 0.9rem;
}

/* ─── Loading State ─── */
.loading-state {
  text-align: center;
  padding: 80px 0;
  color: var(--text-muted, #9ca3af);
  font-size: 0.95rem;
}

/* ─── Core Stats Card (环形评分 + 核心统计) ─── */
.core-stats-card {
  display: grid;
  grid-template-columns: 140px 1fr;
  align-items: center;
  gap: 1.6rem;
  padding: 1.6rem 1.8rem;
  margin-bottom: 1.2rem;
  border: 1.5px dashed #BFDBFE;
  background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);
}

.core-score-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 120px;
  flex-shrink: 0;
}

/* Ring score */
.score-ring {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  flex-shrink: 0;
}

.score-ring-inner {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: var(--bg-card, #fff);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.score-number {
  font-size: 1.6rem;
  font-weight: 800;
  color: var(--primary, #2563EB);
  line-height: 1.2;
}

.score-unit {
  font-size: 0.7rem;
  color: var(--text-muted, #9ca3af);
  font-weight: 400;
}

.score-label {
  margin-top: 0.4rem;
  font-size: 0.82rem;
  color: var(--text-body, #6b7280);
  font-weight: 500;
}

/* Stats grid */
.core-stats-grid {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.7rem;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: var(--primary-bg, #eff6ff);
  border-radius: var(--radius-md, 10px);
  padding: 0.7rem 0.9rem;
  transition: background 0.2s;
}

.stat-icon {
  font-size: 1.15rem;
  color: var(--primary, #2563EB);
  width: 24px;
  text-align: center;
  flex-shrink: 0;
}

.stat-icon.stat-high {
  color: #67c23a;
}

.stat-icon.stat-low {
  color: #f56c6c;
}

.stat-info {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.stat-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-heading, #1f2937);
  line-height: 1.2;
}

.stat-value.stat-high { color: #67c23a; }
.stat-value.stat-low { color: #f56c6c; }

.stat-label {
  font-size: 0.72rem;
  color: var(--text-muted, #9ca3af);
}

/* ─── Card Base ─── */
.card {
  background: var(--bg-card, #fff);
  border-radius: 20px;
  box-shadow: 0 16px 36px rgba(37,99,235,.06);
  border: 1px solid #DBEAFE;
  padding: 1.6rem 1.8rem;
  margin-bottom: 1.2rem;
}

/* ─── Section Header / Title ─── */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 1rem;
  color: var(--text-heading, #1f2937);
}

.section-title i {
  font-size: 1rem;
  color: var(--primary, #2563EB);
}

/* ─── Tag Pill (count badge) ─── */
.tag-pill.tag-count {
  font-size: 0.78rem;
  color: var(--text-muted, #9ca3af);
  background: var(--primary-bg, #eff6ff);
  padding: 0.2rem 0.65rem;
  border-radius: 20px;
  font-weight: 500;
  flex-shrink: 0;
}

/* ─── Loading / Empty States ─── */
.loading-state,
.empty-state {
  text-align: center;
  padding: 48px 0;
  color: var(--text-muted, #9ca3af);
  font-size: 0.9rem;
}
.loading-state i,
.empty-state i {
  margin-right: 6px;
}

/* ─── Radar Chart ─── */
.dim-analysis-card .section-header {
  margin-bottom: 0.8rem;
}

.radar-section {
  display: flex;
  justify-content: center;
  margin-bottom: 1.4rem;
}

.radar-chart-wrap {
  width: 210px;
  height: 210px;
}

.radar-svg {
  width: 100%;
  height: 100%;
}

/* ─── Dimension Bar Chart ─── */
.dim-bar-chart {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  margin-bottom: 1.2rem;
}

.dim-bar-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.dim-bar-label {
  width: 120px;
  font-size: 0.8rem;
  color: var(--text-body, #6b7280);
  text-align: right;
  flex-shrink: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dim-bar-track {
  flex: 1;
  height: 8px;
  background: var(--border, #f0f0f0);
  border-radius: var(--radius-sm, 4px);
  overflow: hidden;
}

.dim-bar-fill {
  height: 100%;
  border-radius: var(--radius-sm, 4px);
  transition: width 0.4s ease;
}

.dim-bar-value {
  width: 36px;
  font-size: 0.8rem;
  font-weight: 700;
  text-align: right;
  flex-shrink: 0;
}

/* ─── Small Ring Charts ─── */
.ring-charts-row {
  display: flex;
  justify-content: center;
  gap: 2rem;
  padding-top: 0.6rem;
  border-top: 1px solid var(--border, #f0f0f0);
}

.ring-chart-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
}

.ring-chart {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  flex-shrink: 0;
}

.ring-chart-label {
  font-size: 0.75rem;
  color: var(--text-muted, #9ca3af);
  font-weight: 500;
}
.ring-chart-label i {
  margin-right: 3px;
  font-size: 0.7rem;
}

.ring-chart-value {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-heading, #1f2937);
}

/* ─── QA Section ─── */
.qa-card .section-header {
  margin-bottom: 0.8rem;
}

.qa-item {
  background: var(--primary-bg, #f8f9ff);
  border-radius: var(--radius-md, 10px);
  padding: 0.9rem 1rem;
  margin-bottom: 0.7rem;
  border-left: 3px solid var(--primary, #2563EB);
  transition: box-shadow 0.2s;
}

.qa-top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.qa-left {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.qa-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: var(--primary, #2563EB);
  color: #fff;
  font-size: 0.72rem;
  font-weight: 600;
  border-radius: 8px;
  padding: 0.15rem 0.55rem;
  min-width: 28px;
}

.qa-score-badge {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #fff;
  padding: 0.12rem 0.5rem;
  border-radius: 8px;
}
.qa-score-badge i {
  font-size: 0.65rem;
}

.qa-body {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.qa-label {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-muted, #9ca3af);
  display: block;
  margin-bottom: 0.2rem;
}
.qa-label i {
  margin-right: 4px;
}

.qa-text {
  font-size: 0.88rem;
  color: var(--text-body, #4b5563);
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
}

.qa-collapsed {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.qa-empty-text {
  font-size: 0.85rem;
  color: var(--text-muted, #9ca3af);
  font-style: italic;
}
.qa-empty-text i {
  margin-right: 4px;
}

.qa-expand-btn {
  background: none;
  border: none;
  color: var(--primary, #2563EB);
  font-size: 0.78rem;
  cursor: pointer;
  padding: 0;
  margin-top: 0.2rem;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.qa-expand-btn:hover {
  color: #5b6ab8;
}

.qa-question-section,
.qa-answer-section {
  display: flex;
  flex-direction: column;
}

/* ─── Analysis Cards (综合建议) ─── */
.analysis-cards-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 0.8rem;
  margin-bottom: 1.2rem;
}

.analysis-card {
  border-radius: var(--radius-md, 10px);
  padding: 0.9rem 1rem;
}

.analysis-strength {
  background: #f0f9f0;
  border: 1px solid #d4edda;
}

.analysis-weakness {
  background: #fef6f0;
  border: 1px solid #fde8d0;
}

.analysis-suggestion {
  background: #f0f4ff;
  border: 1px solid #d4e0ff;
}

.analysis-card-header {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-bottom: 0.5rem;
}

.analysis-card-icon {
  font-size: 1rem;
  width: 20px;
  text-align: center;
}

.analysis-strength .analysis-card-icon { color: #67c23a; }
.analysis-weakness .analysis-card-icon { color: #e6a23c; }
.analysis-suggestion .analysis-card-icon { color: var(--primary, #2563EB); }

.analysis-card-title {
  font-size: 0.88rem;
  font-weight: 600;
  color: var(--text-heading, #1f2937);
}

.analysis-list {
  margin: 0;
  padding-left: 1rem;
  font-size: 0.82rem;
  color: var(--text-body, #6b7280);
  line-height: 1.7;
  list-style: disc;
}

.analysis-empty {
  list-style: none;
  color: var(--text-muted, #9ca3af);
  font-style: italic;
  padding-left: 0;
}
.analysis-empty i {
  margin-right: 4px;
}

/* ─── Special Grid (专项分析) ─── */
.special-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.8rem;
}

.special-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  background: var(--primary-bg, #f8f9fc);
  border-radius: var(--radius-md, 10px);
  padding: 1rem 0.5rem;
}

.special-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.special-circle-inner {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--bg-card, #fff);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.15rem;
  color: var(--primary, #2563EB);
}

.special-label {
  font-size: 0.78rem;
  color: var(--text-muted, #9ca3af);
  font-weight: 500;
}

.special-score {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-heading, #1f2937);
}

/* ═══════════════════════════════════════════
   Responsive
   ═══════════════════════════════════════════ */
@media (max-width: 700px) {
  .core-stats-card {
    flex-direction: column;
    gap: 1rem;
  }

  .core-stats-grid {
    width: 100%;
  }

  .analysis-cards-row {
    grid-template-columns: 1fr;
  }

  .ring-charts-row {
    gap: 1rem;
    flex-wrap: wrap;
  }

  .special-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .dim-bar-label {
    width: 100px;
  }
}

@media (max-width: 480px) {
  .core-stats-card {
    padding: 1rem;
  }

  .card {
    padding: 1rem 1.2rem;
  }

  .special-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.6rem;
  }

  .qa-item {
    padding: 0.7rem 0.8rem;
  }
}
</style>