<template>
  <div class="page history-page">
    <!-- ═══ 页面标题 ═══ -->
    <section class="history-hero">
      <button class="hero-back" @click="$router.back()">
        <ArrowLeft :size="16" class="icon-blue" /> 返回
      </button>
      <div class="hero-copy">
        <span class="hero-kicker">INTERVIEW REVIEW</span>
        <h1><History :size="16" class="icon-blue" /> 面试历史记录</h1>
        <p>把每次模拟面试沉淀成可复盘的记录，看见分数趋势，也看见下一次该练哪里。</p>
      </div>
      <div class="hero-route">
        <span>选择岗位</span>
        <i></i>
        <span>开始模拟</span>
        <i></i>
        <span>复盘记录</span>
      </div>
    </section>

    <!-- ═══ 分数趋势 + 分析图表 ═══ -->
    <div class="history-grid" :class="{ 'single-column': !trendData.labels.length }">
      <!-- 左列：图表区，与右列等高 -->
      <div class="charts-column">
        <!-- 趋势折线面积图 -->
        <div class="card trend-card" v-if="trendData.labels.length">
          <div class="section-header">
            <div class="section-title">
              <ChartLine :size="16" class="icon-blue" />
              分数趋势
            </div>
            <span class="trend-note">最近 {{ trendData.labels.length }} 次</span>
          </div>
          <div class="trend-chart">
            <svg class="trend-svg" viewBox="0 0 360 140" preserveAspectRatio="none">
              <!-- Y轴参考线 -->
              <line x1="0" y1="35" x2="360" y2="35" stroke="#E2E8F0" stroke-width="1" />
              <line x1="0" y1="70" x2="360" y2="70" stroke="#E2E8F0" stroke-width="1" />
              <line x1="0" y1="105" x2="360" y2="105" stroke="#E2E8F0" stroke-width="1" />
              <!-- 渐变面积 -->
              <defs>
                <linearGradient id="trendFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="#2563EB" stop-opacity="0.35" />
                  <stop offset="100%" stop-color="#2563EB" stop-opacity="0.02" />
                </linearGradient>
              </defs>
              <!-- 面积填充 -->
              <path :d="trendAreaPath" fill="url(#trendFill)" stroke="none" />
              <!-- 平滑折线 -->
              <path :d="trendLinePath" fill="none" stroke="#2563EB" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
              <!-- 数据点 -->
              <circle v-for="(pt, i) in trendPoints" :key="i"
                :cx="pt.x" :cy="pt.y" r="4" fill="#fff" stroke="#2563EB" stroke-width="2.5" />
              <circle v-for="(pt, i) in trendPoints" :key="'dot-'+i"
                :cx="pt.x" :cy="pt.y" r="1.5" fill="#2563EB" />
            </svg>
            <!-- 底部日期标签 -->
            <div class="trend-xlabels">
              <span v-for="(l, i) in trendData.labels" :key="i" class="trend-xlabel">
                {{ l.slice(5,10) }}
              </span>
            </div>
          </div>
        </div>
        <div class="card trend-card trend-placeholder" v-else>
          <div class="section-header">
            <div class="section-title">
              <ChartLine :size="16" class="icon-blue" />
              分数趋势
            </div>
          </div>
          <div class="trend-empty">
            <div class="trend-empty-icon"><ChartLine :size="32" class="icon-blue" /></div>
            <p class="trend-empty-title">还没有面试记录</p>
            <p class="trend-empty-hint">完成一次模拟面试后，这里会显示你的分数变化趋势</p>
          </div>
        </div>

        <!-- 下方分析图表面板（与趋势卡片等高分布） -->
        <div class="chart-sub-row">
          <!-- 维度平均分雷达 -->
          <div class="card sub-chart-card">
            <div class="section-header sub-chart-head">
              <div class="section-title" style="font-size:14px;">
                <PieChart :size="14" class="icon-blue" />
                维度表现
              </div>
            </div>
            <div class="sub-chart-body">
              <div v-for="(v, k) in dimensionAverages" :key="k" class="dim-item">
                <span class="dim-label">{{ k }}</span>
                <div class="dim-bar-track">
                  <div class="dim-bar-fill" :style="{ width: v + '%', background: dimBarColor(v) }"></div>
                </div>
                <span class="dim-val" :style="{ color: dimBarColor(v) }">{{ v }}</span>
              </div>
            </div>
          </div>

          <!-- 综合指标 -->
          <div class="card sub-chart-card">
            <div class="section-header sub-chart-head">
              <div class="section-title" style="font-size:14px;">
                <TrendingUp :size="14" class="icon-blue" />
                综合指标
              </div>
            </div>
            <div class="sub-chart-body stats-grid">
              <div class="stat-cell">
                <span class="stat-num">{{ overallStats.avg }}</span>
                <span class="stat-desc">平均分</span>
              </div>
              <div class="stat-cell">
                <span class="stat-num" style="color:#22c55e">{{ overallStats.high }}</span>
                <span class="stat-desc">最高分</span>
              </div>
              <div class="stat-cell">
                <span class="stat-num" style="color:#f56c6c">{{ overallStats.low }}</span>
                <span class="stat-desc">最低分</span>
              </div>
              <div class="stat-cell">
                <span class="stat-num" :style="{ color: overallStats.improvement >= 0 ? '#22c55e' : '#f56c6c' }">
                  {{ overallStats.improvement >= 0 ? '+' : '' }}{{ overallStats.improvement }}
                </span>
                <span class="stat-desc">变化趋势</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ═══ 面试会话列表（右列） ═══ -->
      <section class="records-panel">
        <div class="section-header records-head">
          <div class="section-title">
            <FileText :size="16" class="icon-blue" />
            全部记录
          </div>
          <span class="records-count">{{ sessions.length }} 条</span>
        </div>
        <div v-if="loading" class="loading-state">
          <Loader :size="16" class="icon-blue" /> 加载中…
        </div>
        <template v-else>
          <div
            v-for="s in sessions"
            :key="s.id"
            class="session-card"
            @click="$router.push('/interview/history/' + s.id)"
          >
            <div class="sc-left">
              <div class="sc-score" :style="{ color: barColor(s.average_score) }">{{ s.average_score }}</div>
              <div class="sc-label">综合分</div>
            </div>
            <div class="sc-body">
              <div class="sc-job">{{ s.job || '未命名面试' }}</div>
              <div class="sc-meta">
                <span class="meta-item"><FileText :size="16" class="icon-blue" /> {{ s.total_questions }}题</span>
                <span class="meta-item"><ArrowUp :size="16" :color="'#22c55e'" /> 最高 {{ s.highest_score }}</span>
                <span class="meta-item"><ArrowDown :size="16" :color="'#f56c6c'" /> 最低 {{ s.lowest_score }}</span>
                <span class="meta-item"><Calendar :size="16" class="icon-blue" /> {{ s.date }}</span>
              </div>
              <div class="sc-dims" v-if="Object.keys(s.dimensions || {}).length">
                <el-tag
                  v-for="(v, k) in s.dimensions"
                  :key="k"
                  size="small"
                  :type="v >= 70 ? 'success' : v >= 50 ? 'warning' : 'danger'"
                  effect="plain"
                >{{ k }}:{{ v }}</el-tag>
              </div>
            </div>
            <div class="sc-arrow"><ChevronRight :size="16" class="icon-blue" /></div>
          </div>
          <div v-if="!sessions.length" class="empty-state">
            <Inbox :size="16" class="icon-blue" /> 暂无面试记录
          </div>
        </template>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const API = '/api'
const $router = useRouter()

const sessions = ref([])
const loading = ref(true)
const trendData = ref({ labels: [], scores: [] })

function barColor(v) { return v >= 70 ? '#2563EB' : v >= 50 ? '#0EA5E9' : '#f56c6c' }
function dimBarColor(v) { return v >= 70 ? '#2563EB' : v >= 50 ? '#0EA5E9' : '#f56c6c' }

// SVG 折线图计算
const trendPoints = computed(() => {
  const scores = trendData.value.scores
  if (!scores.length) return []
  const w = 340 // effective chart width
  const h = 120 // chart height (140 - 20 top/bottom padding)
  const minScore = Math.min(...scores) - 5
  const maxScore = Math.max(...scores) + 5
  const range = Math.max(maxScore - minScore, 20)
  return scores.map((s, i) => ({
    x: 10 + (w / (Math.max(scores.length - 1, 1))) * i,
    y: 130 - ((s - minScore) / range) * h,
  }))
})

const trendLinePath = computed(() => {
  const pts = trendPoints.value
  if (pts.length < 2) return ''
  // 平滑贝塞尔曲线
  let d = `M${pts[0].x},${pts[0].y}`
  for (let i = 1; i < pts.length; i++) {
    const cx1 = (pts[i-1].x + pts[i].x) / 2
    d += ` C${cx1},${pts[i-1].y} ${cx1},${pts[i].y} ${pts[i].x},${pts[i].y}`
  }
  return d
})

const trendAreaPath = computed(() => {
  const pts = trendPoints.value
  if (pts.length < 2) return ''
  const line = trendLinePath.value
  if (!line) return ''
  // 闭合到底部形成面积
  const last = pts[pts.length - 1]
  const first = pts[0]
  return `${line} L${last.x},130 L${first.x},130 Z`
})

// 维度平均
const dimensionAverages = computed(() => {
  const dims = {}
  let count = 0
  for (const s of sessions.value) {
    if (s.dimensions) {
      for (const [k, v] of Object.entries(s.dimensions)) {
        dims[k] = (dims[k] || 0) + v
      }
      count++
    }
  }
  if (!count) return { '暂无维度数据': 0 }
  const result = {}
  for (const [k, v] of Object.entries(dims)) {
    result[k] = Math.round(v / count)
  }
  return result
})

// 综合指标
const overallStats = computed(() => {
  const scores = sessions.value.map(s => s.average_score).filter(Boolean)
  if (!scores.length) return { avg: 0, high: 0, low: 0, improvement: 0 }
  const avg = Math.round(scores.reduce((a, b) => a + b, 0) / scores.length)
  const high = Math.round(Math.max(...scores))
  const low = Math.round(Math.min(...scores))
  const improvement = scores.length >= 2 ? Math.round(scores[scores.length - 1] - scores[0]) : 0
  return { avg, high, low, improvement }
})

onMounted(async () => {
  try {
    const [hRes, tRes] = await Promise.all([
      axios.get(`${API}/interview/history`, { params: { limit: 20 } }),
      axios.get(`${API}/interview/trend`)
    ])
    sessions.value = hRes.data.sessions || []
    trendData.value = {
      labels: tRes.data?.labels || [],
      scores: tRes.data?.overall_scores || tRes.data?.scores || [],
    }
  } catch { /* ignore */ }
  loading.value = false
})
</script>

<style scoped>
/* ─── Page Layout ─── */
.page {
  width: min(1280px, calc(100vw - 48px));
  margin: 0 auto;
  padding: 0 0 2.4rem;
}
.history-hero {
  position: relative;
  overflow: hidden;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 28px;
  align-items: end;
  margin: 4px 0 22px;
  padding: 28px 30px;
  border-radius: 28px 28px 10px 28px;
  background: linear-gradient(155deg, #EFF6FF 0%, #FFFFFF 74%);
  border: 1.5px dashed #93C5FD;
  box-shadow: 0 18px 42px rgba(37,99,235,.07);
}
.history-hero::after {
  content: 'QITU';
  position: absolute;
  right: 22px;
  top: 12px;
  font-size: 56px;
  font-weight: 900;
  letter-spacing: .12em;
  color: rgba(37,99,235,.05);
}
.hero-back {
  position: absolute;
  left: 22px;
  top: 18px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: 0;
  background: transparent;
  color: var(--primary);
  font: inherit;
  font-weight: 900;
  cursor: pointer;
  z-index: 1;
}
.hero-copy { padding-top: 26px; position: relative; z-index: 1; }
.hero-kicker {
  color: var(--primary);
  font-size: 13px;
  font-weight: 900;
  letter-spacing: .12em;
}
.hero-copy h1 {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 8px 0 8px;
  color: var(--text-heading);
  font-size: 32px;
  line-height: 1.2;
  font-weight: 900;
}
.hero-copy p {
  max-width: 560px;
  color: var(--text-light);
  font-size: 15px;
  line-height: 1.7;
}
.hero-route {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--primary);
  font-size: 14px;
  font-weight: 900;
  white-space: nowrap;
}
.hero-route i {
  width: 42px;
  height: 1.5px;
  background-image: linear-gradient(to right, #93C5FD 50%, transparent 0);
  background-size: 8px 1.5px;
}
.history-grid {
  display: grid;
  grid-template-columns: 380px minmax(0, 1fr);
  gap: 22px;
  align-items: stretch;
}
.history-grid.single-column { grid-template-columns: 1fr; }

/* ─── Section Header ─── */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 0 14px;
}
.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 900;
  font-size: 18px;
  color: var(--text-primary, #1f2937);
}
.trend-note,
.records-count {
  padding: 4px 10px;
  border-radius: 999px;
  background: var(--primary-light);
  color: var(--primary);
  font-size: 12px;
  font-weight: 900;
}

/* ─── 图表列（等高容器） ─── */
.charts-column {
  display: flex;
  flex-direction: column;
  gap: 14px;
  height: 100%;
}
.trend-card {
  flex: 0 0 auto;
}
.trend-card .trend-chart {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.trend-card .trend-svg {
  flex: 1;
  height: auto;
  min-height: 100px;
}
.trend-card .trend-xlabels {
  flex-shrink: 0;
}

/* ─── Trend Card ─── */
.trend-card,
.records-panel {
  padding: 18px;
  border-radius: 22px;
  background: #fff;
  border: 1.5px dashed #BFDBFE;
  box-shadow: 0 16px 36px rgba(37,99,235,.06);
}
.trend-chart { padding: 4px 0 0; }
.trend-svg {
  width: 100%;
  height: 150px;
  display: block;
}
.trend-xlabels {
  display: flex;
  justify-content: space-around;
  margin-top: 2px;
  padding: 0 6px;
}
.trend-xlabel {
  font-size: 10px;
  color: var(--text-muted);
  text-align: center;
  flex: 1;
}
.trend-placeholder {
  min-height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.trend-empty {
  text-align: center;
  padding: 20px;
  color: var(--text-muted);
}
.trend-empty-icon {
  margin-bottom: 12px;
  opacity: 0.4;
}
.trend-empty-icon :deep(.icon-blue) { color: var(--primary) !important; }
.trend-empty-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-light);
  margin-bottom: 6px;
}
.trend-empty-hint {
  font-size: 13px;
  color: var(--text-muted);
}

/* ─── 子图表卡片 ─── */
.chart-sub-row {
  display: flex;
  gap: 14px;
  flex: 1;
}
.sub-chart-card {
  flex: 1;
  min-width: 0;
  padding: 14px 16px;
  border-radius: 18px;
  background: #fff;
  border: 1.5px dashed #BFDBFE;
  box-shadow: 0 12px 28px rgba(37,99,235,.05);
  display: flex;
  flex-direction: column;
}
.sub-chart-head {
  padding: 0 0 10px;
}
.sub-chart-body {
  padding: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* 维度表现条 */
.dim-item {
  display: grid;
  grid-template-columns: 48px 1fr 30px;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
}
.dim-item:last-child { margin-bottom: 0; }
.dim-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--text-light);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.dim-bar-track {
  height: 8px;
  background: #F1F5F9;
  border-radius: 999px;
  overflow: hidden;
}
.dim-bar-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.3s;
}
.dim-val {
  font-size: 11px;
  font-weight: 800;
  text-align: right;
}

/* 综合指标网格 */
.stats-grid {
  display: flex;
  gap: 6px;
  justify-content: space-between;
}
.stat-cell {
  text-align: center;
  padding: 6px 4px;
  flex: 1;
  background: #F8FAFC;
  border-radius: 12px;
}
.stat-num {
  display: block;
  font-size: 22px;
  font-weight: 900;
  color: var(--text-heading);
  line-height: 1.2;
}
.stat-desc {
  display: block;
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 2px;
}

/* ─── Session Card ─── */
.session-card {
  display: grid;
  grid-template-columns: 78px minmax(0, 1fr) 28px;
  align-items: center;
  gap: 16px;
  padding: 16px 18px;
  margin-bottom: 12px;
  cursor: pointer;
  background: linear-gradient(180deg, #FFFFFF 0%, #F8FBFF 100%);
  border: 1px solid #DBEAFE;
  border-radius: 18px;
  transition: transform 0.2s, box-shadow 0.2s, border-color .2s;
}
.session-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 28px rgba(37,99,235,.09);
  border-color: #93C5FD;
}
.sc-left {
  text-align: center;
  min-width: 64px;
  padding: 10px 8px;
  border-radius: 16px;
  background: var(--primary-light);
}
.sc-score {
  font-size: 28px;
  font-weight: 900;
  line-height: 1;
}
.sc-label {
  margin-top: 4px;
  font-size: 12px;
  color: var(--primary);
  font-weight: 900;
}
.sc-body {
  flex: 1;
  min-width: 0;
}
.sc-job {
  font-weight: 900;
  font-size: 17px;
  color: var(--text-primary, #333);
}
.sc-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 7px 14px;
  margin-top: 7px;
  font-size: 13px;
  color: var(--text-light);
}
.sc-dims {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 8px;
}
.sc-arrow {
  flex-shrink: 0;
  color: var(--primary);
  font-size: 0.9rem;
}

/* ─── States ─── */
.loading-state,
.empty-state {
  text-align: center;
  padding: 80px 0;
  color: var(--text-muted);
}
@media (max-width: 900px) {
  .history-hero,
  .history-grid { grid-template-columns: 1fr; }
  .hero-route { flex-wrap: wrap; }
  .session-card { grid-template-columns: 70px minmax(0,1fr); }
  .sc-arrow { display: none; }
}
</style>