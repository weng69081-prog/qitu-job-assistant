<template>
  <div class="page">
    <!-- ═══ 页面标题 ═══ -->
    <div class="section-header">
      <div class="section-title">
        <el-button text @click="$router.back()" style="margin-right:8px;padding:0 4px;font-size:1rem">
          <i class="fas fa-arrow-left"></i>
        </el-button>
        <i class="fas fa-history"></i>
        面试历史记录
      </div>
    </div>

    <!-- ═══ 分数趋势柱状图 ═══ -->
    <div class="card trend-card" v-if="trendData.labels.length">
      <div class="section-header" style="margin-bottom:16px;">
        <div class="section-title" style="font-size:0.95rem;">
          <i class="fas fa-chart-line"></i>
          分数趋势
        </div>
      </div>
      <div class="trend-chart">
        <div class="trend-bars">
          <div v-for="(s, i) in trendData.scores" :key="i" class="trend-bar-wrap" :title="trendData.labels[i] + ': ' + s + '分'">
            <div class="trend-bar" :style="{ height: Math.max(s * 3, 10) + 'px', background: barColor(s) }"></div>
            <span class="trend-label">{{ trendData.labels[i].slice(5,10) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══ 面试会话列表 ═══ -->
    <div v-if="loading" class="loading-state">
      <i class="fas fa-spinner fa-spin"></i> 加载中…
    </div>
    <template v-else>
      <div
        v-for="s in sessions"
        :key="s.id"
        class="card session-card"
        @click="$router.push('/interview/history/' + s.id)"
      >
        <div class="sc-left">
          <div class="sc-score" :style="{ color: barColor(s.average_score) }">{{ s.average_score }}</div>
          <div class="sc-label">分</div>
        </div>
        <div class="sc-body">
          <div class="sc-job">{{ s.job || '未命名面试' }}</div>
          <div class="sc-meta">
            <span class="meta-item"><i class="fas fa-file-alt"></i> {{ s.total_questions }}题</span>
            <span class="meta-item"><i class="fas fa-arrow-up" style="color:#67c23a"></i> {{ s.highest_score }}</span>
            <span class="meta-item"><i class="fas fa-arrow-down" style="color:#f56c6c"></i> {{ s.lowest_score }}</span>
            <span class="meta-item"><i class="fas fa-calendar"></i> {{ s.date }}</span>
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
        <div class="sc-arrow"><i class="fas fa-chevron-right"></i></div>
      </div>
      <div v-if="!sessions.length" class="empty-state">
        <i class="fas fa-inbox"></i> 暂无面试记录
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const API = 'http://localhost:8000/api'
const $router = useRouter()

const sessions = ref([])
const loading = ref(true)
const trendData = ref({ labels: [], scores: [] })

function barColor(v) { return v >= 70 ? '#67c23a' : v >= 50 ? '#e6a23c' : '#f56c6c' }

onMounted(async () => {
  try {
    const [hRes, tRes] = await Promise.all([
      axios.get(`${API}/interview/history`, { params: { limit: 20 } }),
      axios.get(`${API}/interview/trend`)
    ])
    sessions.value = hRes.data.sessions || []
    trendData.value = tRes.data || { labels: [], scores: [] }
  } catch { /* ignore */ }
  loading.value = false
})
</script>

<style scoped>
/* ─── Page Layout ─── */
.page {
  max-width: 780px;
  margin: 0 auto;
  padding: 0 1rem 2rem;
}

/* ─── Section Header ─── */
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.8rem 0;
}
.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 1.05rem;
  color: var(--text-primary, #1f2937);
}
.section-title i {
  font-size: 1rem;
  color: var(--primary, #3D5A80);
}

/* ─── Trend Card ─── */
.trend-card {
  padding: 1rem;
  margin-bottom: 1rem;
}
.trend-bars {
  display: flex;
  align-items: flex-end;
  gap: 6px;
  height: 130px;
  padding: 0 4px;
}
.trend-bar-wrap {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
}
.trend-bar {
  width: 24px;
  border-radius: 6px 6px 0 0;
  transition: height 0.3s;
  min-height: 6px;
}
.trend-label {
  font-size: 0.6rem;
  color: #999;
  writing-mode: vertical-lr;
}

/* ─── Session Card ─── */
.session-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: box-shadow 0.2s;
}
.session-card:hover {
  box-shadow: 0 2px 16px rgba(0,0,0,0.1);
}
.sc-left {
  text-align: center;
  min-width: 48px;
}
.sc-score {
  font-size: 1.5rem;
  font-weight: 700;
  line-height: 1;
}
.sc-label {
  font-size: 0.72rem;
  color: #999;
}
.sc-body {
  flex: 1;
  min-width: 0;
}
.sc-job {
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--text-primary, #333);
}
.sc-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 14px;
  margin-top: 4px;
  font-size: 0.78rem;
  color: #888;
}
.sc-dims {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-top: 6px;
}
.sc-arrow {
  flex-shrink: 0;
  color: #ccc;
  font-size: 0.9rem;
}

/* ─── States ─── */
.loading-state,
.empty-state {
  text-align: center;
  padding: 80px 0;
  color: #999;
}
.loading-state i,
.empty-state i {
  margin-right: 6px;
}
</style>