<template>
  <div class="exam-practice-page">
    <!-- ═══ PageBanner（带猫+路径条，跟面试模拟一样） ═══ -->
    <PageBanner fullwidth
      title="笔试练习"
      description="刷题、复盘、巩固基础能力。海量真题分类练习，覆盖主流技术岗位"
      :icon="'exam'"
      variant="primary"
      cat-src="/src/assets/exam-cat.png"
      cat-alt="小橘笔试"
      :path-items="['选岗位', '开始练', '查漏补缺']"
    />

    <!-- ═══ Hero 刷题入口 ═══ -->
    <section class="interview-shell">
      <div class="stage-card" @click="$router.push('/exam/session')">
        <div class="stage-copy">
          <div class="stage-kicker"><Book :size="16" class="icon-blue" /> 笔试专项练习</div>
          <h2>笔试练习</h2>
          <p>刷题、复盘、巩固基础能力。海量真题分类练习，覆盖主流技术岗位，针对性刷题提升笔试能力。</p>
          <div class="stage-tags">
            <span><Book :size="16" class="icon-blue" /> 专项练习</span>
            <span><Timer :size="16" class="icon-blue" /> 计时模考</span>
            <span><Shuffle :size="16" class="icon-blue" /> 随机刷题</span>
          </div>
        </div>
        <div class="stage-visual" aria-hidden="true">
          <div class="screen-card stats-preview">
            <div class="sp-header">今日练习概览</div>
            <div class="sp-row"><span class="sp-label">已完成</span><span class="sp-value">{{ dashData.totalQuestions }}题</span></div>
            <div class="sp-row"><span class="sp-label">正确率</span><span class="sp-value" :style="{ color: dashData.weekAccuracy > 70 ? '#2563EB' : '#C85A20' }">{{ dashData.weekAccuracy }}%</span></div>
            <div class="sp-row"><span class="sp-label">连续打卡</span><span class="sp-value">{{ dashData.streakDays }}天</span></div>
            <div class="sp-divider"></div>
            <div class="sp-empty" v-if="!dashData.totalQuestions">刷题后自动生成统计</div>
          </div>
        </div>
        <button class="start-button" @click.stop="$router.push('/exam/session')">
          开始刷题 <ArrowRight :size="16" class="icon-white" />
        </button>
      </div>

      <!-- ═══════ 看板 + 侧栏（同一排） ═══════ -->
      <div class="exam-dashboard-row">
        <!-- 左：练习统计看板 -->
        <div class="dashboard-section">
          <div class="section-header" style="margin-bottom:12px">
            <div class="section-title">
              <BarChart :size="16" class="icon-blue" /> 练习统计看板
            </div>
            <span class="section-more">一页看尽近况</span>
          </div>

          <div class="dash-cards">
            <div class="stat-card dash-card-hover" @mouseenter="dashHover=0" @mouseleave="dashHover=-1">
              <div class="stat-icon"><Pen :size="16" class="icon-blue" /></div>
              <div class="stat-num">{{ dashData.totalQuestions }}</div>
              <div class="stat-label">总刷题量</div>
              <div class="dc-mini-chart">
                <svg viewBox="0 0 100 36" class="mini-trend" v-if="dashTrendData.length > 1">
                  <path :d="dashTrendPath" fill="none" stroke="#2563EB" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <div v-else class="mini-empty">暂无</div>
              </div>
              <div class="dc-tooltip" v-if="dashHover === 0">
                <div v-for="d in dashTrendData.slice(-7)" :key="d.date" class="tt-row">
                  <span class="tt-date">{{ d.date.slice(5) }}</span>
                  <span class="tt-val">{{ d.questions }}题</span>
                </div>
              </div>
            </div>

            <div class="stat-card dash-card-hover" @mouseenter="dashHover=1" @mouseleave="dashHover=-1">
              <div class="stat-icon"><Crosshair :size="16" class="icon-blue" /></div>
              <div class="stat-num">{{ dashData.weekAccuracy }}</div>
              <div class="stat-label">近7天正确率</div>
              <div class="dc-mini-chart chart-ring">
                <svg viewBox="0 0 40 40" class="ring-svg">
                  <circle cx="20" cy="20" r="16" fill="none" stroke="#DBEAFE" stroke-width="4" />
                  <circle cx="20" cy="20" r="16" fill="none" stroke="#2563EB" stroke-width="4"
                    :stroke-dasharray="circumference" :stroke-dashoffset="ringOffset"
                    stroke-linecap="round" transform="rotate(-90 20 20)" />
                  <text x="20" y="20" text-anchor="middle" dominant-baseline="central"
                    font-size="9" font-weight="700" :fill="dashData.weekAccuracy > 70 ? '#2563EB' : '#0EA5E9'">
                    {{ dashData.weekAccuracy }}%
                  </text>
                </svg>
              </div>
            </div>

            <div class="stat-card dash-card-hover" @mouseenter="dashHover=2" @mouseleave="dashHover=-1">
              <div class="stat-icon"><Flame :size="16" :color="'#0EA5E9'" /></div>
              <div class="stat-num">{{ dashData.streakDays }}</div>
              <div class="stat-label">连续打卡</div>
              <div class="dc-mini-chart streak-vis">
                <div v-for="i in 7" :key="i" class="streak-dot"
                  :class="{ active: i <= dashData.streakDays, max: i === dashData.streakDays && dashData.streakDays > 0 }"
                  :style="{ opacity: i <= dashData.streakDays ? 0.4 + (i / 7) * 0.6 : 0.15 }">
                </div>
                <span class="streak-suffix" v-if="dashData.streakDays > 0"><Flame :size="16" class="icon-blue" /> {{ dashData.streakDays }}天连击</span>
              </div>
            </div>

            <div class="stat-card dash-card-hover" @mouseenter="dashHover=3" @mouseleave="dashHover=-1">
              <div class="stat-icon"><Footprints :size="16" class="icon-blue" /></div>
              <div class="stat-num">{{ dashData.weekCompletion }}</div>
              <div class="stat-label">本周完成率</div>
              <div class="dc-mini-chart completion-bar-wrap">
                <div class="completion-track">
                  <div class="completion-fill" :style="{ width: dashData.weekCompletion + '%' }"></div>
                </div>
                <span class="completion-hint">{{ dashData.weekDone }}/{{ dashData.weekGoal }}天</span>
              </div>
            </div>
          </div>

          <div class="dash-weak-tip" v-if="dashWeakModules.length">
            <TriangleAlert :size="16" class="icon-blue" style="margin-right:6px" />
            近3天薄弱模块：<b>{{ dashWeakModules }}</b>
          </div>
        </div>

        <!-- 右：错题+收藏（上下叠） -->
        <aside class="exam-review-bar">
          <router-link to="/exam/wrong" class="sidelink-card">
            <div class="sl-icon"><AlertCircle :size="20" class="icon-blue" /></div>
            <div class="sl-body">
              <span class="sl-title">全部笔试错题</span>
              <span class="sl-sub">{{ wrongTotal }} 道待回顾</span>
            </div>
          </router-link>
          <router-link to="/favorites?tab=exam" class="sidelink-card">
            <div class="sl-icon"><Star :size="20" class="icon-blue" /></div>
            <div class="sl-body">
              <span class="sl-title">我的收藏</span>
              <span class="sl-sub">{{ savedTotal }} 道已收藏</span>
            </div>
          </router-link>
          <router-link to="/exam/history" class="sidelink-card">
            <div class="sl-icon"><Clock :size="20" class="icon-blue" /></div>
            <div class="sl-body">
              <span class="sl-title">练习记录</span>
              <span class="sl-sub">历史成绩与分析</span>
            </div>
          </router-link>
        </aside>
      </div>
    </section>
    <!-- ═══ 品牌 Footer ═══ -->
    <div class="brand-footer">
      <div>启途 · <span class="qitu-up">QITU</span></div>
      <div class="qitu-sl">向上生长，自有答案</div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import PageBanner from '../components/PageBanner.vue'

// Lucide icons
import { Pen, Book, Timer, Shuffle, ArrowRight, BarChart, Crosshair, Flame, Footprints, TriangleAlert, AlertCircle, Star, Clock } from 'lucide-vue-next'

const router = useRouter()

// ═══════ 数据看板 ═══════
const dashData = reactive({
  totalQuestions: 0,
  weekAccuracy: 0,
  streakDays: 0,
  weekCompletion: 0,
  weekDone: 0,
  weekGoal: 7
})
const dashHover = ref(-1)
const dashTrendData = ref([])
const dashWeakModules = ref('')

// ═══════ 复盘统计 ═══════
const wrongTotal = ref(0)
const savedTotal = ref(0)
async function loadStats() {
  try {
    const { data } = await axios.get('/api/exam/stats')
    wrongTotal.value = data.wrong_total || data.total_wrong || 0
    savedTotal.value = data.saved_total || data.total_saved || 0
  } catch { /* ignore */ }
}

// 环形进度条
const circumference = Math.PI * 32
const ringOffset = computed(() => {
  const pct = Math.min(dashData.weekAccuracy, 100)
  return circumference - (circumference * pct / 100)
})

// 看板迷你趋势折线
const dashTrendPath = computed(() => {
  const data = dashTrendData.value
  if (data.length < 2) return ''
  const maxQ = Math.max(...data.map(d => d.questions), 1)
  const w = data.length > 1 ? 98 / (data.length - 1) : 49
  const pts = data.map((d, i) => ({
    x: 1 + i * w,
    y: 34 - (d.questions / maxQ) * 28
  }))
  return pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ')
})

// 加载看板数据
async function loadDashboard() {
  try {
    const [overview, trend, errorDist] = await Promise.all([
      axios.get('/api/exam/stats/overview').then(r => r.data),
      axios.get('/api/exam/stats/trend', { params: { days: 7 } }).then(r => r.data),
      axios.get('/api/exam/stats/error-distribution').then(r => r.data),
    ])
    dashData.totalQuestions = overview.total_questions || 0
    dashData.weekAccuracy = overview.avg_accuracy || 0
    dashData.streakDays = overview.streak_days || 0
    const grow = await axios.get('/api/exam/stats/growth').then(r => r.data).catch(() => null)
    if (grow && grow.this_week) {
      dashData.weekDone = Math.min(grow.this_week.days || 0, 7)
      dashData.weekGoal = 7
      dashData.weekCompletion = Math.round((dashData.weekDone / 7) * 100)
    } else {
      dashData.weekDone = 0
      dashData.weekCompletion = 0
    }
    dashTrendData.value = (trend.trend || []).slice(-7)
    const weekDaysWithPractice = dashTrendData.value.filter(d => (d.questions || 0) > 0).length
    dashData.weekDone = Math.min(weekDaysWithPractice, 7)
    dashData.weekGoal = 7
    dashData.weekCompletion = Math.round((weekDaysWithPractice / 7) * 100)
    if (errorDist.distribution && errorDist.distribution.length > 0) {
      const top3 = errorDist.distribution.slice(0, 3).map(d => d.name)
      dashWeakModules.value = top3.join('、')
    }
  } catch { /* ignore */ }
}

// ═══════ 生命周期 ═══════
onMounted(() => {
  loadDashboard()
  loadStats()
})
</script>

<style scoped>
.exam-practice-page {
  padding: 0 0 46px;
  color: var(--text-body);
}

/* ═══════ Shell Wrapper ═══════ */
.interview-shell {
  width: calc(100vw - var(--sidebar-width) - 40px);
  max-width: 1480px;
  margin: 24px auto 0;
}

/* ═══════ Stage Card ═══════ */
.stage-card {
  position: relative;
  min-height: 280px;
  display: grid;
  grid-template-columns: minmax(0, 1.18fr) 430px;
  gap: 36px;
  padding: 26px 40px 20px;
  border-radius: 26px 26px 12px 26px;
  background:
    linear-gradient(135deg, rgba(239,246,255,.98), rgba(255,255,255,.96) 58%),
    radial-gradient(circle at 82% 12%, rgba(37,99,235,.16), transparent 32%);
  border: 1.5px dashed #93C5FD;
  box-shadow: 0 20px 48px rgba(37,99,235,.08);
}
.stage-card .start-button {
  position: absolute;
  right: 42px;
  bottom: 34px;
  z-index: 5;
}
.stage-card::after {
  content: '';
  position: absolute;
  right: 0;
  bottom: 0;
  width: 78px;
  height: 78px;
  background: linear-gradient(135deg, rgba(191,219,254,.9), #fff 58%);
  clip-path: polygon(100% 0, 0 100%, 100% 100%);
  border-left: 1px dashed #93C5FD;
}
.stage-copy {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  min-height: 250px;
}
.stage-kicker,
.section-title {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #2563EB;
  font-size: 15px;
  font-weight: 900;
  letter-spacing: .04em;
}
.stage-copy h2 {
  margin: 16px 0 12px;
  max-width: 560px;
  color: var(--text-heading);
  font-size: 36px;
  line-height: 1.2;
  font-weight: 900;
  letter-spacing: .02em;
}
.stage-copy p {
  max-width: 560px;
  color: var(--text-light);
  font-size: 17px;
  line-height: 1.75;
}
.stage-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 24px;
}
.stage-tags span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 34px;
  padding: 0 14px;
  border-radius: 999px;
  background: #fff;
  color: #2563EB;
  border: 1px solid #BFDBFE;
  box-shadow: 6px 6px 14px rgba(147,197,253,.18), -6px -6px 14px rgba(255,255,255,.9);
  font-size: 14px;
  font-weight: 800;
}
.stage-visual {
  position: relative;
  min-height: 240px;
  z-index: 2;
}
.screen-card {
  position: absolute;
  left: 20px;
  top: 18px;
  width: 220px;
  padding: 18px 18px 16px;
  border-radius: 18px;
  background: #fff;
  border: 1.5px dashed #93C5FD;
  box-shadow: 0 18px 36px rgba(37,99,235,.12);
}
.stats-preview .sp-header {
  font-size: 15px;
  font-weight: 900;
  color: #2563EB;
  margin-bottom: 12px;
}
.stats-preview .sp-row {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
  font-size: 14px;
}
.stats-preview .sp-label {
  color: var(--text-light);
}
.stats-preview .sp-value {
  font-weight: 700;
  color: var(--text-heading);
}
.stats-preview .sp-divider {
  height: 1px;
  background: #DBEAFE;
  margin: 8px 0;
}
.stats-preview .sp-empty {
  text-align: center;
  color: var(--text-muted);
  font-size: 13px;
  padding: 8px 0;
}
/* ─── Stats Preview Card ─── */

/* ─── Start Button ─── */
.start-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 46px;
  padding: 0 24px;
  border: 0;
  border-radius: 16px;
  background: linear-gradient(145deg, #0EA5E9, #2563EB);
  color: #fff;
  font: inherit;
  font-size: 17px;
  font-weight: 900;
  box-shadow: 10px 10px 22px rgba(37,99,235,.20), -8px -8px 18px rgba(255,255,255,.85);
  cursor: pointer;
  transition: transform 0.2s;
}
.start-button .icon-blue { color: #fff !important; stroke: #fff !important; }
.icon-white { color: #fff !important; stroke: #fff !important; }

/* ═══════ 看板+侧栏容器 ═══════ */
.exam-dashboard-row {
  display: flex;
  gap: 16px;
  margin-top: 42px;
  align-items: stretch;
}
.exam-dashboard-row .dashboard-section {
  flex: 1;
  min-width: 0;
  margin: 0;
}
.exam-review-bar {
  display: flex;
  flex-direction: column;
  gap: 10px;
  width: 200px;
  flex-shrink: 0;
}
.sidelink-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 14px;
  border-radius: 18px;
  border: 1.5px dashed #BFDBFE;
  background: #fff;
  box-shadow: 0 12px 28px rgba(37,99,235,.05);
  text-decoration: none;
  transition: box-shadow .2s, transform .2s;
  flex: 1;
}
.sidelink-card:hover {
  box-shadow: 0 16px 36px rgba(37,99,235,.12);
  transform: translateY(-2px);
}
.sidelink-card .sl-icon {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: #EFF6FF;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.sidelink-card .sl-body { display: flex; flex-direction: column; }
.sl-title { font-size: 15px; font-weight: 800; color: #1E293B; }
.sl-sub { font-size: 12px; color: #94A3B8; margin-top: 2px; }
.stage-card:hover .start-button { transform: translateX(4px); }

/* ═══════ 数据看板 ═══════ */
.dashboard-section {
  background: linear-gradient(135deg, #EFF6FF, #fff);
  border: 1.5px dashed #BFDBFE;
  border-radius: 22px;
  padding: 16px 20px 12px;
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0;
}
.section-more {
  font-size: 0.72rem;
  color: var(--text-muted);
}
.dash-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}
.stat-card {
  background: #fff;
  border: 1.5px dashed #BFDBFE;
  border-radius: 18px;
  padding: 14px 14px 10px;
  text-align: center;
  transition: all 0.2s;
  position: relative;
}
.dash-card-hover {
  cursor: default;
}
.dash-card-hover:hover {
  border-color: #2563EB;
  box-shadow: 0 2px 8px rgba(37,99,235,0.1);
}
.stat-icon { margin-bottom: 4px; }
.stat-num {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--text-heading);
}
.stat-label {
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-top: 2px;
}
.dc-mini-chart {
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 4px;
}
.mini-trend { width: 100%; height: 36px; }
.mini-empty { font-size: 0.7rem; color: var(--text-muted); }
.chart-ring { padding: 0; }
.ring-svg { width: 44px; height: 44px; }

/* 连续打卡 dots */
.streak-vis {
  flex-direction: row;
  gap: 4px;
  flex-wrap: wrap;
  padding: 6px 0;
}
.streak-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0EA5E9, #2563EB);
  transition: transform 0.2s;
}
.streak-dot.active { transform: scale(1.2); }
.streak-dot.max { box-shadow: 0 0 0 3px rgba(37,99,235,0.2); }
.streak-suffix {
  width: 100%;
  text-align: center;
  font-size: 0.68rem;
  color: #0EA5E9;
  font-weight: 600;
  margin-top: 2px;
}

/* 完成率进度条 */
.completion-bar-wrap {
  flex-direction: column;
  gap: 4px;
  padding: 0;
}
.completion-track {
  width: 100%;
  height: 8px;
  background: #DBEAFE;
  border-radius: 4px;
  overflow: hidden;
}
.completion-fill {
  height: 100%;
  background: linear-gradient(90deg, #2563EB, #1D4ED8);
  border-radius: 4px;
  transition: width 0.4s;
}
.completion-hint { font-size: 0.68rem; color: var(--text-muted); }

/* hover tooltip */
.dc-tooltip {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: #333;
  color: white;
  padding: 6px 10px;
  border-radius: 8px;
  font-size: 0.72rem;
  z-index: 20;
  white-space: nowrap;
  margin-top: 6px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.15);
}
.tt-row { display: flex; justify-content: space-between; gap: 10px; padding: 2px 0; }
.tt-date { color: #aaa; }
.tt-val { font-weight: 600; }

/* 薄弱模块提示 */
.dash-weak-tip {
  margin-top: 10px;
  padding: 6px 12px;
  background: #FFF7ED;
  border-radius: 8px;
  font-size: 0.78rem;
  color: #0EA5E9;
}
.dash-weak-tip b { color: #0EA5E9; }

/* ─── 响应式 ─── */
@media (max-width: 1080px) {
  .interview-shell { width: calc(100vw - var(--sidebar-width) - 28px); }
  .stage-card { grid-template-columns: 1fr; }
  .stage-visual { display: none; }
  .review-panel { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
  .interview-shell { width: calc(100vw - 28px); }
  .stage-card { padding: 18px 18px 20px; }
  .stage-copy { min-height: 240px; }
  .stage-copy h2 { font-size: 28px; }
  .dash-cards { grid-template-columns: repeat(2, 1fr); }
  .review-card { padding: 14px 16px; }
  .review-title { font-size: 15px; }
}
</style>