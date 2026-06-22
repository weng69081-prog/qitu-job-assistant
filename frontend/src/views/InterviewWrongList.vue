<template>
  <div class="wronglist-page">
    <!-- ═══ 返回按钮（左上） ═══ -->
    <button class="back-circle-btn" @click="$router.back()">
      <ArrowLeft :size="16" class="icon-blue" /> 返回
    </button>

    <!-- ═══ Banner ═══ -->
    <PageBanner fullwidth
      title="面试错题本"
      description="回顾每次面试中的失误，针对性强化训练，提升面试表现"
      icon="fa-xmark"
      variant="primary"
    />

    <!-- ═══ 紧凑统计条 ═══ -->
    <section class="stat-ribbon">
      <div class="stat-cell">
        <div class="sc-icon"><AlertCircle :size="16" class="icon-blue" /></div>
        <div class="sc-body">
          <span class="sc-num">{{ interviewWrongTotal }}</span>
          <span class="sc-label">总错题</span>
        </div>
      </div>
      <div class="stat-cell">
        <div class="sc-icon sc-done"><CheckCircle :size="16" class="icon-blue" /></div>
        <div class="sc-body">
          <span class="sc-num">{{ masteredCount }}</span>
          <span class="sc-label">已掌握</span>
        </div>
        <div class="sc-bar">
          <span class="sc-bar-fill" :style="{ width: masteryPct + '%' }"></span>
        </div>
      </div>
      <div class="stat-cell">
        <div class="sc-icon sc-pending"><Hourglass :size="16" class="icon-blue" /></div>
        <div class="sc-body">
          <span class="sc-num">{{ interviewWrongTotal - masteredCount }}</span>
          <span class="sc-label">待回顾</span>
        </div>
      </div>
      <div class="stat-cell stat-cell-highlight">
        <div class="sc-icon"><TrendingUp :size="16" class="icon-blue" /></div>
        <div class="sc-body">
          <span class="sc-num">{{ masteryPct }}%</span>
          <span class="sc-label">掌握率</span>
        </div>
      </div>
    </section>

    <!-- ═══ 筛选项 ═══ -->
    <section class="zone-list">
      <div class="list-toolbar">
        <div class="filter-tabs">
          <button v-for="f in filters" :key="f.key"
            class="filter-tab" :class="{ active: activeFilter === f.key }"
            @click="activeFilter = f.key; loadInterviewWrong(1)">
            <i :class="f.icon"></i> {{ f.label }}
          </button>
        </div>
        <button v-if="interviewWrong.length" class="btn-text-sm" @click="reviewAllPending" :disabled="interviewWrongTotal - masteredCount === 0">
          <Play :size="16" class="icon-blue" /> 逐一回顾
        </button>
      </div>

      <!-- ═══ 加载态 ═══ -->
      <div v-if="wrongLoading" class="loading-state">
        <Loader :size="16" class="icon-blue" /> 加载中…
      </div>

      <!-- ═══ 错题列表 ═══ -->
      <template v-else-if="interviewWrong.length">
        <div class="wrong-card" v-for="row in interviewWrong" :key="row.id">
          <div class="wc-top">
            <div class="wc-question">{{ row.question }}</div>
            <div class="wc-badges">
              <span class="tag-pill" :class="diffPill(row.difficulty)">{{ row.difficulty || '中等' }}</span>
              <span class="tag-pill" :class="row.mastered ? 'green' : 'orange'">
                <CheckCircle :size="16" class="icon-blue" :class="row.mastered ? 'fas fa-check-circle' : 'fas fa-times-circle'" />
                {{ row.mastered ? '已掌握' : '未掌握' }}
              </span>
            </div>
          </div>
          <div class="wc-meta">
            <span class="meta-item"><Layers :size="16" class="icon-blue" /> {{ row.category || '通用' }}</span>
            <span class="meta-item"><XCircle :size="16" class="icon-blue" /> 答错 <b>{{ row.wrong_count }}</b> 次</span>
            <span class="meta-item"><Clock :size="16" class="icon-blue" /> {{ row.last_wrong_at }}</span>
          </div>
          <div class="wc-preview">
            <div class="wp-row">
              <span class="wp-label">你的回答</span>
              <span class="wp-text">{{ row.user_answer || '无记录' }}</span>
            </div>
            <div class="wp-row">
              <span class="wp-label">参考回答</span>
              <span class="wp-text">{{ row.correct_answer || '暂无' }}</span>
            </div>
          </div>
          <div class="wc-actions">
            <button class="btn-outline btn-sm" @click="reviewWrong(row)">
              <BookOpen :size="16" class="icon-blue" /> 详细回顾
            </button>
            <button class="btn-outline btn-sm" :class="{ 'btn-mastered': row.mastered }"
              @click="masterInterviewWrong(row)" :disabled="row.mastered">
              <Check :size="16" class="icon-blue" /> {{ row.mastered ? '已掌握' : '标记掌握' }}
            </button>
            <button class="btn-outline btn-sm btn-danger" @click="deleteInterviewWrong(row)">
              <Trash2 :size="16" class="icon-blue" />
            </button>
          </div>
        </div>

        <!-- ═══ 分页 ═══ -->
        <div class="pagination-wrap" v-if="interviewWrongTotal > 20">
          <el-pagination layout="prev,pager,next" :total="interviewWrongTotal" :page-size="20"
            @current-change="p => loadInterviewWrong(p)" background />
        </div>
      </template>

      <!-- ═══ 空态 ═══ -->
      <div v-else class="empty-state">
        <div class="empty-icon-wrap"><CheckCircle :size="16" class="icon-blue" /></div>
        <p class="empty-title">暂无面试错题</p>
        <p class="empty-hint">继续加油，保持学习！错题会自动记录</p>
      </div>
    </section>

    <!-- ═══ 错题回顾弹窗 ═══ -->
    <el-dialog v-model="reviewVisible" title="📖 错题详细回顾" width="680px" destroy-on-close
      class="review-dialog">
      <div v-if="reviewItem" class="review-content">
        <div class="review-badges">
          <span class="tag-pill" :class="diffPill(reviewItem.difficulty)">{{ reviewItem.difficulty || '中等' }}</span>
          <span class="tag-pill" :class="reviewItem.mastered ? 'green' : 'orange'">
            {{ reviewItem.mastered ? '✅ 已掌握' : '⏳ 待巩固' }}
          </span>
          <span class="tag-pill gray"><Layers :size="16" class="icon-blue" /> {{ reviewItem.category || '通用' }}</span>
        </div>

        <div class="review-block">
          <div class="review-label">
            <CircleHelp :size="16" class="icon-blue" /> 题目
          </div>
          <div class="review-value">{{ reviewItem.question }}</div>
        </div>

        <div class="review-block" v-if="reviewItem.source">
          <div class="review-label"><Link :size="16" class="icon-blue" /> 来源</div>
          <div class="review-value review-source">{{ reviewItem.source }}</div>
        </div>

        <div class="review-block">
          <div class="review-label">
            <UserPen :size="16" class="icon-blue" /> 你的回答
          </div>
          <div class="review-value review-answer-wrong">{{ reviewItem.user_answer || '未记录' }}</div>
        </div>

        <div class="review-block">
          <div class="review-label">
            <CheckCheck :size="16" class="icon-blue" /> 参考回答
          </div>
          <div class="review-value review-answer-correct">{{ reviewItem.correct_answer || reviewItem.sample_answer || '暂无参考回答' }}</div>
        </div>

        <!-- 错因分析 -->
        <div class="review-block review-analysis-block">
          <div class="review-label">
            <FileText :size="16" class="icon-blue" /> AI分析
          </div>
          <div class="review-value review-analysis">{{ reviewItem.analysis || '暂无AI分析。开始面试模拟后，AI会分析你的回答并给出改进建议。' }}</div>
        </div>

        <!-- 答题记录 -->
        <div class="review-meta-grid">
          <div class="review-meta-item">
            <XCircle :size="16" class="icon-blue" />
            <span>答错 <b>{{ reviewItem.wrong_count || 1 }}</b> 次</span>
          </div>
          <div class="review-meta-item" v-if="reviewItem.last_wrong_at">
            <Clock :size="16" class="icon-blue" />
            <span>最近出错 <b>{{ reviewItem.last_wrong_at }}</b></span>
          </div>
          <div class="review-meta-item" v-if="reviewItem.category">
            <Layers :size="16" class="icon-blue" />
            <span>知识点分类：<b>{{ reviewItem.category }}</b></span>
          </div>
        </div>

        <!-- 提升建议（固定展示结构，就算暂空也显示框架） -->
        <div class="review-tip-block">
          <div class="review-label">
            <Lightbulb :size="16" class="icon-blue" /> 提升建议
          </div>
          <ul class="review-tip-list">
            <li><b>梳理思路</b> — 先明确问题的核心考点，再组织回答结构</li>
            <li><b>积累术语</b> — 把相关关键词和常用表达记录下来</li>
            <li><b>模拟练习</b> — 回到面试模块再练一题同类题目巩固</li>
          </ul>
        </div>

        <div class="review-footer">
          <button class="btn-primary" @click="reviewVisible = false">
            <Check :size="16" class="icon-blue" /> 关闭回顾
          </button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import PageBanner from '../components/PageBanner.vue'

const interviewWrong = ref([])
const interviewWrongTotal = ref(0)
const wrongLoading = ref(false)
const activeFilter = ref('all')

const filters = [
  { key: 'all', label: '全部', icon: 'fas fa-list' },
  { key: 'pending', label: '待回顾', icon: 'fas fa-hourglass-half' },
  { key: 'mastered', label: '已掌握', icon: 'fas fa-check-circle' },
]

const masteredCount = computed(() => interviewWrong.value.filter(w => w.mastered).length)
const masteryPct = computed(() => {
  if (!interviewWrongTotal.value) return 0
  return Math.round((masteredCount.value / interviewWrongTotal.value) * 100)
})

async function loadInterviewWrong(page = 1) {
  wrongLoading.value = true
  try {
    const params = { page, page_size: 20 }
    const { data } = await axios.get('/api/interview/wrong-questions', { params })
    let items = data.items || []
    if (activeFilter.value === 'pending') items = items.filter(w => !w.mastered)
    else if (activeFilter.value === 'mastered') items = items.filter(w => w.mastered)
    interviewWrong.value = items
    interviewWrongTotal.value = data.total || 0
  } catch { /* ignore */ }
  wrongLoading.value = false
}
async function masterInterviewWrong(row) {
  try {
    await axios.put(`/api/interview/wrong-questions/${row.id}/master`)
    ElMessage.success('✅ 已标记为掌握！继续保持')
    loadInterviewWrong()
  } catch { ElMessage.error('操作失败') }
}
async function deleteInterviewWrong(row) {
  try {
    await axios.delete(`/api/interview/wrong-questions/${row.id}`)
    ElMessage.success('已删除')
    loadInterviewWrong()
  } catch { ElMessage.error('删除失败') }
}

function reviewAllPending() {
  const first = interviewWrong.value.find(w => !w.mastered)
  if (first) reviewWrong(first)
}

const reviewVisible = ref(false)
const reviewItem = ref(null)
function reviewWrong(row) { reviewItem.value = row; reviewVisible.value = true }

function diffPill(d) {
  const m = { easy: 'green', 简单: 'green', medium: 'orange', 中等: 'orange', hard: 'red', 困难: 'red' }
  return m[d] || 'blue'
}

onMounted(() => { loadInterviewWrong() })
</script>

<style scoped>
.wronglist-page {
  position: relative;
  width: min(960px, calc(100vw - 48px));
  margin: 0 auto;
  padding: 0 0 2.4rem;
}
.back-circle-btn {
  position: absolute;
  left: 0;
  top: 8px;
  z-index: 10;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 18px;
  border: 2px solid var(--primary);
  border-radius: 999px;
  background: #fff;
  color: var(--primary);
  font: inherit;
  font-weight: 900;
  font-size: 14px;
  cursor: pointer;
  transition: box-shadow .2s;
}
.back-circle-btn:hover {
  box-shadow: 0 4px 14px rgba(37,99,235,.18);
}
.stat-ribbon,
.zone-list {
  width: min(960px, calc(100vw - 48px));
  margin-left: auto;
  margin-right: auto;
}

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
  position: relative;
  overflow: hidden;
}
.stat-cell:hover {
  border-color: rgba(37,99,235,.22);
  box-shadow: 0 2px 8px rgba(37,99,235,.08);
}
.sc-icon {
  width: 22px; height: 22px;
  border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px;
  background: rgba(245,108,108,.1);
  color: #f56c6c;
  flex-shrink: 0;
}
.sc-icon.sc-done { background: rgba(103,194,58,.1); color: #67c23a; }
.sc-icon.sc-pending { background: rgba(230,162,60,.1); color: #e6a23c; }
.stat-cell-highlight .sc-icon { background: #EFF6FF; color: #2563EB; }
.sc-body {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}
.sc-num { font-size: 15px; font-weight: 700; color: var(--text-heading); }
.sc-label { font-size: 10px; color: var(--text-muted); margin-top: 1px; }
.sc-bar {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 2px;
  background: rgba(200,200,200,.2);
}
.sc-bar-fill {
  display: block;
  height: 100%;
  background: linear-gradient(90deg, #67c23a, #85ce61);
  border-radius: 0 1px 0 0;
  transition: width 0.6s ease;
}

/* ── 筛选项 ── */
.list-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  flex-wrap: wrap;
  gap: 10px;
}
.filter-tabs {
  display: flex;
  gap: 3px;
  background: rgba(240,242,246,.8);
  border-radius: 8px;
  padding: 3px;
  border: 1px solid rgba(0,0,0,.03);
}
.filter-tab {
  display: flex;
  align-items: center;
  gap: 4px;
  background: transparent;
  border: none;
  font-size: .78rem;
  color: #8EA0B8;
  cursor: pointer;
  padding: .4rem .7rem;
  font-weight: 500;
  border-radius: 6px;
  transition: all .25s ease;
}
.filter-tab i { font-size: .7rem; }
.filter-tab.active {
  background: #fff;
  color: #2563EB;
  font-weight: 600;
  box-shadow: 0 1px 3px #BFDBFE;
}
.filter-tab:hover:not(.active) { color: #2563EB; }
.btn-text-sm {
  background: transparent;
  border: 1px solid var(--border);
  padding: 5px 12px;
  border-radius: 7px;
  font-size: 12px;
  color: #2563EB;
  cursor: pointer;
  transition: all .2s;
  display: flex;
  align-items: center;
  gap: 4px;
}
.btn-text-sm:hover { background: rgba(37,99,235,.08); border-color: #2563EB; }

/* ── 错题卡片 ── */
.wrong-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 16px 18px;
  margin-bottom: 10px;
  box-shadow: var(--shadow-sm);
  transition: all 0.25s;
  border: 1px solid var(--border-light);
}
.wrong-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
  border-color: rgba(37,99,235,.18);
}

.wc-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 8px;
}
.wc-question {
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
.wc-badges {
  display: flex;
  gap: 5px;
  flex-shrink: 0;
  flex-wrap: wrap;
}

/* ── 元信息行 ── */
.wc-meta {
  display: flex;
  gap: 14px;
  color: var(--text-muted);
  font-size: 11px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}
.meta-item {
  display: flex;
  align-items: center;
  gap: 3px;
}
.meta-item i { font-size: 10px; }
.meta-item b { color: var(--text-body); font-weight: 600; }

/* ── 回答预览 ── */
.wc-preview {
  background: var(--bg-alt);
  border-radius: var(--radius-sm);
  padding: 8px 12px;
  margin-bottom: 10px;
  border: 1px solid var(--border-light);
}
.wp-row {
  display: flex;
  gap: 8px;
  font-size: 12px;
  line-height: 1.5;
  margin-bottom: 4px;
}
.wp-row:last-child { margin-bottom: 0; }
.wp-label {
  flex-shrink: 0;
  font-weight: 600;
  color: var(--text-muted);
  min-width: 52px;
  font-size: 11px;
}
.wp-text {
  color: var(--text-body);
  display: -webkit-box;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* ── 操作按钮行 ── */
.wc-actions {
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

/* ── 按钮变小变体 ── */
.btn-sm { padding: 4px 10px !important; font-size: 11px !important; }
.btn-mastered { opacity: .5; cursor: not-allowed !important; }
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
  background: rgba(37,99,235,.08);
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 10px;
}
.empty-icon { font-size: 22px; color: #2563EB; }

/* ── 回顾弹窗 ── */
.review-dialog :deep(.el-dialog__header) { padding-bottom: 6px; }
.review-dialog :deep(.el-dialog__body) { padding-top: 6px; }
.review-content { padding: 4px 0; }
.review-badges { display: flex; gap: 6px; margin-bottom: 14px; flex-wrap: wrap; }
.review-block { margin-bottom: 14px; }
.review-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 3px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.review-label i { font-size: 10px; }
.review-value {
  font-size: 13px;
  color: var(--text-body);
  line-height: 1.6;
  background: var(--bg-alt);
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-light);
}
.review-source { font-size: 12px; color: #8EA0B8; }
.review-answer-wrong {
  border-left: 3px solid #f56c6c;
  background: rgba(245,108,108,.04);
}
.review-answer-correct {
  border-left: 3px solid #67c23a;
  background: rgba(103,194,58,.04);
}
.review-analysis {
  border-left: 3px solid #2563EB;
  background: #EFF6FF;
}
.review-analysis-block { margin-top: -6px; }
.review-meta-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  padding: 10px 12px;
  background: #F8FAFC;
  border-radius: 10px;
  margin-bottom: 14px;
}
.review-meta-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-muted);
}
.review-meta-item b { color: var(--text-body); font-weight: 700; }
.review-tip-block {
  margin-bottom: 14px;
  padding: 12px 14px;
  background: #FFF7ED;
  border: 1.5px dashed #FED7AA;
  border-radius: 14px;
}
.review-tip-block .review-label { color: #C2410C; }
.review-tip-list {
  margin: 8px 0 0;
  padding: 0;
  list-style: none;
}
.review-tip-list li {
  position: relative;
  padding-left: 18px;
  margin-bottom: 6px;
  font-size: 13px;
  color: #9A3412;
  line-height: 1.5;
}
.review-tip-list li::before {
  content: '💡';
  position: absolute;
  left: 0;
  top: 0;
  font-size: 12px;
}
.review-tip-list li:last-child { margin-bottom: 0; }
.review-tip-list li b { font-weight: 700; color: #7C2D12; }
.review-footer { text-align: center; margin-top: 6px; }
</style>