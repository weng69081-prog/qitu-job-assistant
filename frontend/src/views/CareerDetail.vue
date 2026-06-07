<template>
  <div class="career-detail-page">
    <!-- ═══ 头部：职业封面区 ═══ -->
    <div class="detail-topbar detail-hero">
      <div class="detail-hero-paper">
        <div class="hero-copy">
          <button class="btn-back" @click="$router.back()">
            <ArrowLeft :size="16" class="icon-blue" />
            <span>返回职业探索</span>
          </button>
          <span class="hero-eyebrow">职业详情 · 启途方向卡</span>
          <div class="detail-topbar-center">
            <span class="detail-topbar-icon" aria-hidden="true">
              <svg viewBox="0 0 48 48" fill="none">
                <rect x="10" y="12" width="28" height="24" rx="7" fill="#EFF6FF" stroke="#2563EB" stroke-width="2.2" />
                <path d="M17 21h14M17 27h9" stroke="#2563EB" stroke-width="2.2" stroke-linecap="round" />
                <path d="M18 12c.8-4 3.1-6 6-6s5.2 2 6 6" stroke="#93C5FD" stroke-width="2.2" stroke-linecap="round" />
                <circle cx="34" cy="32" r="6.2" fill="#FFFFFF" stroke="#0EA5E9" stroke-width="2" />
                <path d="M31.5 32.2l1.8 1.8 3.5-4" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                <path d="M9 38h30" stroke="#BFDBFE" stroke-width="2" stroke-linecap="round" stroke-dasharray="4 4" />
              </svg>
            </span>
            <h1 class="detail-topbar-title">{{ careerData.career || '加载中…' }}</h1>
          </div>
          <p class="hero-desc">把岗位职责、能力要求、薪资参考和成长路线放在一张清晰的职业地图里。</p>
          <div class="hero-tag-strip">
            <span v-for="tag in (careerData.hard_requirements || []).slice(0, 4)" :key="tag">{{ tag }}</span>
            <span v-if="!(careerData.hard_requirements || []).length">岗位职责</span>
            <span v-if="!(careerData.hard_requirements || []).length">能力要求</span>
            <span v-if="!(careerData.hard_requirements || []).length">成长路线</span>
          </div>
        </div>

        <div class="hero-side">
          <div class="hero-watermark">QITU</div>
          <div class="hero-metrics">
            <div class="hero-metric">
              <span>薪资参考</span>
              <strong>{{ careerData.salary || '7K-20K' }}</strong>
            </div>
            <div class="hero-metric">
              <span>入门难度</span>
              <strong>{{ careerData.difficulty || '初级' }}</strong>
            </div>
            <div class="hero-metric">
              <span>匹配度</span>
              <strong>{{ careerData.match || 85 }}%</strong>
            </div>
          </div>
          <div class="hero-pathline">
            <span>了解岗位</span>
            <i></i>
            <span>补齐能力</span>
            <i></i>
            <span>收藏路线</span>
          </div>
          <button
            class="hero-bookmark-btn"
            :class="{ active: isBookmarked }"
            @click="toggleBookmark"
            :title="isBookmarked ? '取消收藏' : '收藏此岗位'"
          >
            <Star :size="17" class="icon-blue" :class="isBookmarked ? 'fas fa-star' : 'far fa-star'" />
            <span>{{ isBookmarked ? '已收藏路线' : '收藏并生成路线' }}</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-state detail-loading"><i class="fas fa-spinner fa-spin"></i> 加载中…</div>
    <template v-else-if="careerData.career">
      <div class="detail-main-grid">

      <aside class="detail-side-rail">
        <section class="side-card salary-side-card">
          <span class="side-kicker">薪资与趋势</span>
          <strong>{{ careerData.salary || '7K-20K' }}</strong>
          <p>{{ careerData.trend || '关注岗位能力要求，按阶段补齐项目经验。' }}</p>
        </section>
        <section class="side-card">
          <span class="side-kicker">适合这样的你</span>
          <p>{{ careerData.suitable_audience || '暂无' }}</p>
        </section>
        <section class="side-card side-card-soft">
          <span class="side-kicker">避坑提示</span>
          <p>{{ careerData.avoid_tips || '暂无' }}</p>
        </section>
        <section class="side-card side-video-card">
          <div class="side-video-head">
            <span class="side-kicker">职业入门视频推荐</span>
            <el-radio-group v-model="videoSort" size="small" @change="loadVideos">
              <el-radio-button value="hot">热门</el-radio-button>
              <el-radio-button value="new">最新</el-radio-button>
            </el-radio-group>
          </div>
          <div v-if="videoLoading" class="side-video-loading">正在搜索B站视频…</div>
          <div v-else-if="videoList.length > 0" class="side-video-list">
            <article v-for="(v, idx) in videoList.slice(0, 4)" :key="v.bvid || idx" class="side-video-item" @click="openVideo(v)">
              <div class="side-video-thumb">
                <img v-if="v.pic" :src="v.pic" :alt="cleanTitle(v.title)" @error="onCoverError($event, v)" />
                <span v-else>{{ idx + 1 }}</span>
              </div>
              <div class="side-video-info">
                <h4>{{ cleanTitle(v.title) || '入门视频' }}</h4>
                <p><span v-if="v.author">{{ v.author }}</span><span v-if="v.play">{{ formatCount(v.play) }}播放</span></p>
              </div>
            </article>
          </div>
          <div v-else class="side-video-empty">暂无推荐视频</div>
        </section>
      </aside>

      <div class="detail-content-flow">

      <!-- ═══ 模块1：岗位总览 ═══ -->
      <section class="card detail-section overview-panel">
        <div class="section-header">
          <h3 class="section-title"><i class="fas fa-clipboard-list"></i> 岗位总览</h3>
        </div>
        <p class="overview-text">{{ careerData.responsibilities?.join('；') || '暂无描述' }}</p>
        <div class="growth-ladder">
          <div class="ladder-title"><i class="fas fa-layer-group"></i> 晋升阶梯</div>
          <div class="ladder-steps">
            <div
              v-for="(step, i) in careerData.growth_path || []"
              :key="i"
              class="ladder-step"
            >
              <div class="step-dot" :style="{background: ladderColors[i % ladderColors.length]}"></div>
              <div class="step-line" v-if="i < (careerData.growth_path?.length || 0) - 1"></div>
              <span class="step-text">{{ step }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══ 模块2：日常工作流程 ═══ -->
      <section class="card detail-section">
        <div class="section-header">
          <h3 class="section-title"><i class="fas fa-exchange-alt"></i> 日常工作流程</h3>
        </div>
        <div class="workflow-timeline">
          <div
            v-for="(step, i) in (careerData.work_flow || [])"
            :key="i"
            class="wf-item"
          >
            <div class="wf-num" :style="{background: ladderColors[i % ladderColors.length]}">{{ i + 1 }}</div>
            <div class="wf-content">{{ step }}</div>
            <div class="wf-arrow" v-if="i < (careerData.work_flow?.length || 0) - 1"><ChevronDown :size="16" class="icon-blue" /></div>
          </div>
        </div>
      </section>

      <!-- ═══ 模块3：核心能力要求 ═══ -->
      <section class="card detail-section">
        <div class="section-header">
          <h3 class="section-title"><i class="fas fa-bullseye"></i> 核心能力要求</h3>
        </div>
        <div class="skill-section">
          <div class="skill-group">
            <span class="skill-group-label"><i class="fas fa-code"></i> 硬性技能</span>
            <div class="skill-tag-list">
              <el-tag v-for="r in (careerData.hard_requirements || [])" :key="r" type="primary" size="small">{{ r }}</el-tag>
            </div>
          </div>
          <div class="skill-group" style="margin-top:12px">
            <span class="skill-group-label"><i class="fas fa-handshake"></i> 软性技能</span>
            <div class="skill-tag-list">
              <el-tag v-for="r in (careerData.soft_requirements || [])" :key="r" type="success" size="small">{{ r }}</el-tag>
            </div>
          </div>
          <!-- 能力雷达条 -->
          <div class="radar-panel">
            <div class="radar-panel-title"><i class="fas fa-chart-pie"></i> 能力雷达（参考）</div>
            <div v-for="r in radarItems" :key="r.label" class="radar-bar">
              <span class="radar-label">{{ r.label }}</span>
              <div class="radar-track">
                <div class="radar-fill" :style="{width: r.value + '%', background: r.color}"></div>
              </div>
              <span class="radar-val">{{ r.value }}%</span>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══ 模块4：就业&薪资参考 ═══ -->
      <section class="card detail-section">
        <div class="section-header">
          <h3 class="section-title"><i class="fas fa-coins"></i> 就业&薪资参考</h3>
        </div>
        <p class="salary-desc">{{ careerData.trend || '' }}</p>
        <table class="salary-table" v-if="careerData.salary_table?.length">
          <thead>
            <tr><th>职级</th><th>薪资范围</th></tr>
          </thead>
          <tbody>
            <tr v-for="row in careerData.salary_table" :key="row.level">
              <td>{{ row.level }}</td>
              <td>{{ row.range }}</td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- ═══ ⚡ AI 智能分析 ═══ -->
      <section class="card detail-section ai-analysis-section">
        <div class="section-header">
          <h3 class="section-title"><Bot :size="16" class="icon-blue" /> AI 智能分析</h3>
          <span class="section-badge">MiMo</span>
        </div>
        <div v-if="aiLoading" class="loading-state" style="padding:16px 0">
          <i class="fas fa-spinner fa-spin"></i> 正在用 AI 分析…
        </div>
        <template v-else-if="aiAnalysis.summary">
          <div class="ai-summary">
            <div class="ai-label"><i class="fas fa-quote-left"></i> 一句话概括</div>
            <p class="ai-summary-text">{{ aiAnalysis.summary }}</p>
          </div>
          <div class="ai-grid">
            <div class="ai-item">
              <div class="ai-item-icon"><CheckCircle :size="16" class="icon-blue" /></div>
              <div class="ai-item-content">
                <div class="ai-item-label">为什么适合你</div>
                <p>{{ aiAnalysis.suitable_reason }}</p>
              </div>
            </div>
            <div class="ai-item">
              <div class="ai-item-icon"><Laptop :size="16" class="icon-blue" /></div>
              <div class="ai-item-content">
                <div class="ai-item-label">日常工作</div>
                <p>{{ aiAnalysis.daily_work }}</p>
              </div>
            </div>
          </div>
          <div class="ai-growth">
            <div class="ai-growth-title"><i class="fas fa-signal"></i> AI 推荐的成长路径</div>
            <div class="ai-growth-steps">
              <div v-for="(step, i) in aiAnalysis.growth_path" :key="i" class="ai-growth-step">
                <div class="ai-step-dot" :style="{background: ['#2563EB','#0EA5E9','#60A5FA'][i % 3]}"></div>
                <span>{{ step }}</span>
              </div>
            </div>
          </div>
          <div class="ai-footer">
            <i class="fas fa-microchip"></i> 由 MiMo AI 基于你的专业背景生成
          </div>
        </template>
        <div v-else class="ai-empty">
          <Bot :size="16" class="icon-blue" /> AI 分析加载失败，请稍后重试
        </div>
      </section>

      <!-- ═══ 模块6：成长路线入口 ═══ -->
      <section class="card detail-section roadmap-entry-section">
        <div class="roadmap-entry-copy">
          <span class="roadmap-kicker">成长路线</span>
          <h3>把课程、证书、任务和资源拆成一条能照着走的路线</h3>
          <p>详情页先保持轻盈，完整路线放到单独页面里看，更适合收藏后长期跟踪。</p>
        </div>
        <button class="roadmap-entry-btn" @click="goRoadmap">
          <span>查看完整成长路线</span>
          <i>→</i>
        </button>
      </section>


      <!-- ═══ AI生成内容反馈 ═══ -->
      <section class="card detail-section" v-if="careerData.ai_generated">
        <div class="section-header">
          <h3 class="section-title"><Bot :size="16" class="icon-blue" /> AI生成内容</h3>
        </div>
        <div class="ai-feedback-banner">
          <p><Info :size="16" class="icon-blue" /> 该职业信息由AI生成，仅供参考。如果内容<strong>不准确</strong>或需要<strong>补充</strong>，可以重新生成完善。</p>
          <div class="ai-feedback-btns">
            <el-button size="small" type="warning" plain @click="sendFeedback('不准确')"><i class="fas fa-times-circle"></i> 内容不准确</el-button>
            <el-button size="small" type="primary" plain @click="sendFeedback('需要补充')"><i class="fas fa-plus-circle"></i> 需要补充</el-button>
            <span v-if="feedbackMsg" class="feedback-msg">{{ feedbackMsg }}</span>
          </div>
        </div>
      </section>

      <!-- ═══ 收藏后底部提示 ═══ -->
      <div class="detail-footer" v-if="!isBookmarked">
        <el-button type="primary" size="large" class="footer-bookmark-btn" @click="toggleBookmark">
          <Star :size="16" class="icon-blue" /> 收藏此岗位，立即生成专属成长路线
        </el-button>
      </div>

      </div>
      </div>
    </template>
    <div v-else class="empty-state">
      <i class="fas fa-exclamation-circle"></i>
      <p>未找到该岗位信息</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCareerStore } from '../stores/career'
import axios from 'axios'

const API = '/api'
const route = useRoute()
const router = useRouter()
const store = useCareerStore()

const careerData = ref({})
const loading = ref(true)
const aiAnalysis = ref({})
const aiLoading = ref(false)

// 视频推荐 + 本地缓存
const videoCache = {}
const videoList = ref([])
const videoLoading = ref(false)
const videoSort = ref('hot')

async function loadVideos() {
  const name = careerData.value.career
  if (!name) return
  const cacheKey = `${name}::${videoSort.value}`
  if (videoCache[cacheKey]) {
    videoList.value = videoCache[cacheKey]
    return
  }
  videoLoading.value = true
  try {
    const resp = await axios.get(`${API}/bilibili/search`, {
      params: { career: name, sort: videoSort.value }
    })
    videoList.value = resp.data.videos || []
    videoCache[cacheKey] = videoList.value
  } catch {
    videoList.value = []
  } finally {
    videoLoading.value = false
  }
}

function cleanTitle(title) {
  if (!title) return ''
  return title.replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'")
}

function formatCount(n) {
  if (!n) return '0'
  n = parseInt(n)
  if (n >= 10000) return (n / 10000).toFixed(1) + '万'
  if (n >= 1000) return (n / 1000).toFixed(1) + 'k'
  return n.toString()
}

function openVideo(v) {
  if (v.url) window.open(v.url, '_blank', 'noopener,noreferrer')
}

function onCoverError(e, v) {
  e.target.style.display = 'none'
  const parent = e.target.parentElement
  if (parent) {
    parent.innerHTML = `<span>${cleanTitle(v.title).slice(0, 2) || '课'}</span>`
  }
}

function toggleVideoBookmark(video) {
  const v = { ...video, career: careerData.value.career }
  if (store.isVideoBookmarked(video.bvid)) {
    store.removeVideoBookmark(video.bvid)
  } else {
    store.addVideoBookmark(v)
  }
}

const isBookmarked = computed(() => store.isBookmarked(careerData.value.career))

const ladderColors = ['#2563EB','#0EA5E9','#60A5FA','#93C5FD','#2563EB','#0EA5E9']

function getIcon(name) {
  const icons = {
    '前端':'fas fa-globe','后端':'fas fa-cogs','数据':'fas fa-chart-bar',
    '测试':'fas fa-vial','安全':'fas fa-shield-alt','产品':'fas fa-mobile-alt',
    '运营':'fas fa-chart-line','设计':'fas fa-paint-brush','算法':'fas fa-brain',
    '运维':'fas fa-wrench','工程':'fas fa-building','管理':'fas fa-user-tie'
  }
  for (const [k, v] of Object.entries(icons)) { if (name?.includes(k)) return v }
  return 'fas fa-briefcase'
}

const radarItems = computed(() => {
  return [
    { label: '专业技能', value: 80, color: '#2563EB' },
    { label: '沟通协作', value: 65, color: '#0EA5E9' },
    { label: '学习能力', value: 75, color: '#60A5FA' },
    { label: '解决问题', value: 70, color: '#2563EB' },
    { label: '抗压能力', value: 60, color: '#93C5FD' },
  ]
})

// ===== 成长路线（收藏岗位直接展示） =====
const pathData = ref([])
const pathLoading = ref(false)
const doneMap = ref({})
const semColors = ['#2563EB','#0EA5E9','#60A5FA','#93C5FD','#2563EB','#0EA5E9','#60A5FA']

function getDoneKey(phase, idx) {
  return `${careerData.value.career || 'default'}_${phase}_${idx}`
}
function loadDoneMap() {
  try {
    doneMap.value = JSON.parse(localStorage.getItem('path_done_map') || '{}')
  } catch { doneMap.value = {} }
}
function saveDoneMap() {
  localStorage.setItem('path_done_map', JSON.stringify(doneMap.value))
}
function getTaskDone(phase, idx) {
  return doneMap.value[getDoneKey(phase, idx)] === true
}
function toggleTask(phase, idx) {
  const key = getDoneKey(phase, idx)
  doneMap.value[key] = !doneMap.value[key]
  saveDoneMap()
}

async function loadSavedPath() {
  if (!careerData.value.career) return
  pathLoading.value = true
  try {
    const { data } = await axios.get(`${API}/career/saved-path/${encodeURIComponent(careerData.value.career)}`)
    if (data.saved && data.path?.length) {
      pathData.value = data.path
    } else if (store.isBookmarked(careerData.value.career)) {
      // 已收藏但没保存过路线 → 实时生成
      const { data: gen } = await axios.post(`${API}/career/save-path`, { career: careerData.value.career })
      pathData.value = gen.path || []
    }
  } catch {
    // fallback 也尝试生成
    try {
      if (store.isBookmarked(careerData.value.career)) {
        const { data: gen } = await axios.post(`${API}/career/save-path`, { career: careerData.value.career })
        pathData.value = gen.path || []
      }
    } catch {}
  }
  pathLoading.value = false
}

// 📺 路线阶段视频推荐
const phaseVideos = reactive({})
const phaseVideoLoading = reactive({})
const expandedPhaseIdx = ref(null)

function goRoadmap() {
  const name = careerData.value.career || route.params.careerId
  if (!name) return
  router.push(`/career/path/${encodeURIComponent(name)}`)
}

async function togglePhaseVideos(idx) {
  if (expandedPhaseIdx.value === idx) {
    expandedPhaseIdx.value = null
    return
  }
  expandedPhaseIdx.value = idx
  // 已缓存的直接显示
  if (phaseVideos[idx] && phaseVideos[idx].length > 0) return
  // 取该阶段的视频关键词
  const sem = pathData.value[idx]
  const keywords = sem?.video_keywords || sem?.courses?.slice(0, 2) || []
  if (!keywords.length) return
  phaseVideoLoading[idx] = true
  // 用第一个关键词搜索
  try {
    const kw = keywords[0]
    const { data } = await axios.get(`${API}/bilibili/keyword-search`, {
      params: { keyword: kw, sort: 'hot' }
    })
    phaseVideos[idx] = data.videos || []
  } catch {
    phaseVideos[idx] = []
  } finally {
    phaseVideoLoading[idx] = false
  }
}

function togglePhaseVideoBookmark(v) {
  const video = { ...v, career: careerData.value.career }
  if (store.isVideoBookmarked(v.bvid)) {
    store.removeVideoBookmark(v.bvid)
  } else {
    store.addVideoBookmark(video)
  }
}

async function toggleBookmark() {
  const name = careerData.value.career
  if (!name) return
  if (store.isBookmarked(name)) {
    store.removeBookmark(name)
    pathData.value = []
  } else {
    store.addBookmark(careerData.value)
    // 收藏时异步生成并保存成长路线
    axios.post(`${API}/career/save-path`, { career: name }).then(res => {
      if (res.data.path?.length) {
        pathData.value = res.data.path
      }
    }).catch(() => {})
  }
}

// AI生成内容反馈
const feedbackMsg = ref('')
async function sendFeedback(type) {
  const name = careerData.value.career
  if (!name) return
  feedbackMsg.value = '正在重新生成…'
  try {
    const { data } = await axios.post(`${API}/career/ai-feedback`, {
      career: name,
      feedback: type
    })
    if (data.career) {
      careerData.value = data.career
      feedbackMsg.value = '✅ 已更新！内容已重新生成'
      setTimeout(() => { feedbackMsg.value = '' }, 3000)
    }
  } catch {
    feedbackMsg.value = '❌ 重新生成失败，请重试'
  }
}

onMounted(async () => {
  loadDoneMap()
  try {
    const name = decodeURIComponent(route.params.careerId)
    const res = await axios.get(`${API}/career/career-detail/${encodeURIComponent(name)}`)
    careerData.value = res.data
    // 自动加载视频推荐
    loadVideos()
    // 异步加载 AI 分析（不阻塞页面）
    aiLoading.value = true
    axios.get(`${API}/career/ai-analysis`, {
      params: { career: name, major: '计算机科学与技术', city: '郑州', education: '本科' }
    }).then(resp => {
      if (resp.data.summary) aiAnalysis.value = resp.data
    }).catch(() => {}).finally(() => { aiLoading.value = false })
    // 如果已收藏，直接加载保存的成长路线
    if (store.isBookmarked(careerData.value.career)) {
      await loadSavedPath()
    }
  } catch (e) {
    console.error('加载岗位详情失败', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
/* ════════════════════════════════════════════
   CareerDetail — 使用全局设计系统变量
   ════════════════════════════════════════════ */

.career-detail-page {
  width: auto;
  max-width: none;
  margin: 0 calc(var(--main-pad-x, 28px) * -1);
  padding: 0 18px 100px;
  color: #1E293B;
}

/* ── 顶部职业纸张栏 ── */
.detail-topbar.detail-hero {
  display: block;
  margin-bottom: 18px;
}
.btn-back {
  align-self: start;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  min-height: 38px;
  margin-bottom: 10px;
  padding: 0 14px;
  background: rgba(255, 255, 255, .82);
  border: 1px solid #BFDBFE;
  border-radius: 999px;
  color: #2563EB;
  font-size: 14px;
  font-weight: 900;
  cursor: pointer;
  transition: transform .22s cubic-bezier(.16, 1, .3, 1), box-shadow .22s, border-color .22s;
  white-space: nowrap;
  box-shadow: 0 10px 24px rgba(37, 99, 235, .08);
}
.btn-back:hover {
  transform: translateY(-1px);
  border-color: #93C5FD;
  box-shadow: 0 14px 28px rgba(37, 99, 235, .10);
}
.detail-hero-paper {
  position: relative;
  min-height: 232px;
  display: grid;
  grid-template-columns: minmax(0, 1.45fr) minmax(440px, .55fr);
  gap: 46px;
  padding: 24px 42px 30px;
  overflow: hidden;
  background:
    radial-gradient(circle at 86% 8%, rgba(147, 197, 253, .26), transparent 32%),
    linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 48%, #F8FBFF 100%);
  border: 1px solid #CFE4FF;
  border-radius: 30px 30px 12px 30px;
  box-shadow: 0 22px 50px rgba(37, 99, 235, .11), inset 0 1px 0 rgba(255,255,255,.88);
}
.detail-hero-paper::after {
  content: '';
  position: absolute;
  right: -1px;
  bottom: -1px;
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, rgba(191,219,254,.25) 0%, #fff 52%, #DBEAFE 53%, #BFDBFE 100%);
  border-left: 1px solid #BFDBFE;
  border-top: 1px solid #BFDBFE;
  border-radius: 12px 0 0 0;
  box-shadow: -8px -8px 18px rgba(37,99,235,.08);
}
.hero-copy,
.hero-side {
  position: relative;
  z-index: 1;
}
.hero-eyebrow {
  display: inline-flex;
  width: max-content;
  margin-bottom: 14px;
  padding: 6px 12px;
  border-radius: 999px;
  background: #FFFFFF;
  border: 1px solid #BFDBFE;
  color: #2563EB;
  font-size: 14px;
  font-weight: 900;
  letter-spacing: .08em;
}
.detail-topbar-center {
  display: flex;
  align-items: center;
  gap: 16px;
  min-width: 0;
}
.detail-topbar-icon {
  width: 66px;
  height: 66px;
  border-radius: 20px;
  background: #FFFFFF;
  border: 1px solid #BFDBFE;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2563EB;
  flex-shrink: 0;
  box-shadow: 0 14px 30px rgba(37,99,235,.10);
}
.detail-topbar-icon svg {
  width: 46px;
  height: 46px;
  display: block;
}
.detail-topbar-title {
  font-size: clamp(38px, 4vw, 56px);
  font-weight: 900;
  color: #1E293B;
  margin: 0;
  letter-spacing: -0.04em;
  line-height: 1.02;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.hero-desc {
  max-width: 66ch;
  margin: 18px 0 0 82px;
  color: #475569;
  font-size: 17px;
  line-height: 1.9;
}
.hero-tag-strip {
  margin: 18px 0 0 82px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  max-width: 680px;
}
.hero-tag-strip span {
  display: inline-flex;
  align-items: center;
  min-height: 30px;
  padding: 0 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, .74);
  border: 1px solid #BFDBFE;
  color: #2563EB;
  font-size: 14px;
  font-weight: 900;
}
.hero-side {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 18px;
  min-width: 0;
  padding-right: 92px;
}
.hero-watermark {
  position: absolute;
  right: -8px;
  top: -22px;
  color: rgba(37, 99, 235, .10);
  font-size: 68px;
  font-weight: 900;
  letter-spacing: .10em;
  line-height: 1;
}
.hero-metrics {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  width: min(100%, 362px);
}
.hero-metric {
  position: relative;
  min-height: 58px;
  padding: 11px 14px;
  background: rgba(255, 255, 255, .76);
  border: 1px solid #DBEAFE;
  border-radius: 16px;
  box-shadow: 0 10px 24px rgba(37, 99, 235, .055);
}
.hero-metric span {
  display: block;
  margin-bottom: 4px;
  color: #64748B;
  font-size: 13px;
  font-weight: 800;
}
.hero-metric strong {
  color: #2563EB;
  font-size: 23px;
  line-height: 1;
  font-weight: 900;
}
.hero-pathline {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  width: min(100%, 362px);
  color: #2563EB;
  font-size: 15px;
  font-weight: 900;
}
.hero-pathline i {
  flex: 1;
  min-width: 30px;
  height: 2px;
  background-image: linear-gradient(to right, #93C5FD 55%, transparent 0);
  background-size: 9px 2px;
}
.hero-bookmark-btn {
  min-height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 0 20px;
  width: min(100%, 362px);
  border: 1px solid #BFDBFE;
  border-radius: 16px;
  background: #FFFFFF;
  color: #2563EB;
  font-size: 16px;
  font-weight: 900;
  cursor: pointer;
  transition: transform .22s cubic-bezier(.16, 1, .3, 1), background .22s, box-shadow .22s;
  box-shadow: 0 12px 26px rgba(37,99,235,.10);
}
.hero-bookmark-btn:hover {
  transform: translateY(-1px);
  background: #EFF6FF;
}
.hero-bookmark-btn.active {
  background: #2563EB;
  border-color: #2563EB;
  color: #FFFFFF;
}
.hero-bookmark-btn.active .icon-blue {
  color: #FFFFFF;
}
.detail-loading {
  min-height: 260px;
}
.detail-main-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) clamp(500px, 32vw, 560px);
  gap: 28px;
  align-items: start;
}
.detail-content-flow {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  gap: 18px;
  min-width: 0;
}
.detail-side-rail {
  position: sticky;
  top: 22px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-height: calc(100vh - 44px);
  order: 2;
}
.detail-content-flow > .detail-section {
  grid-column: span 12;
}
.detail-content-flow > .detail-section:nth-of-type(2),
.detail-content-flow > .detail-section:nth-of-type(3) {
  grid-column: span 6;
}
.side-card {
  position: relative;
  padding: 18px 18px 17px;
  background: #FFFFFF;
  border: 1px solid #DBEAFE;
  border-radius: 18px;
  box-shadow: 0 14px 32px rgba(37, 99, 235, .06);
}
.side-card::before {
  content: none;
}
.side-kicker {
  display: block;
  margin-bottom: 9px;
  color: #2563EB;
  font-size: 14px;
  font-weight: 900;
}
.side-card strong {
  display: block;
  margin-bottom: 8px;
  color: #1E293B;
  font-size: 25px;
  line-height: 1.05;
  font-weight: 900;
}
.side-card p {
  margin: 0;
  color: #475569;
  font-size: 15px;
  line-height: 1.75;
}
.salary-side-card {
  background: linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 78%);
}
.side-card-soft {
  border-style: dashed;
  background: #F8FBFF;
}

/* ── 模块卡片 ── */
.detail-section {
  margin-bottom: 0;
  position: relative;
  background: #FFFFFF;
  border: 1px solid #DBEAFE;
  border-radius: 18px;
  padding: 24px 26px;
  box-shadow: 0 14px 34px rgba(15, 23, 42, .04);
}
.detail-section:deep(.section-header) {
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px dashed #BFDBFE;
}
.detail-section:deep(.section-title) {
  color: #1E293B;
  font-size: 19px;
  font-weight: 900;
  letter-spacing: -0.01em;
}

/* ── 岗位总览 ── */
.overview-text {
  color: #334155;
  line-height: 1.85;
  font-size: 17px;
  margin-bottom: 18px;
}
.growth-ladder {
  margin-top: 14px;
  padding: 16px;
  border-top: 1px dashed #BFDBFE;
  background: #F8FBFF;
  border-radius: 14px;
}
.ladder-title {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.ladder-steps {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.ladder-step {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  position: relative;
  padding-left: 6px;
}
.step-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 5px;
}
.step-line {
  position: absolute;
  left: 10px;
  top: 15px;
  width: 2px;
  height: calc(100% - 4px);
  background: var(--border);
}
.step-text {
  font-size: 13px;
  color: var(--text-body);
  padding: 2px 0 8px;
  line-height: 1.4;
}

/* ── 日常工作流程 ── */
.workflow-timeline {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.wf-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px dashed #E0ECFF;
}
.wf-item:last-child {
  border-bottom: 0;
}
.wf-num {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  color: white;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.wf-content {
  font-size: 14px;
  color: var(--text-body);
  flex: 1;
  line-height: 1.4;
}
.wf-arrow {
  color: var(--text-light);
  font-size: 14px;
  padding: 2px 0;
  width: 16px;
  text-align: center;
}

/* ── 核心能力要求 ── */
.skill-group-label {
  font-size: 13px;
  color: var(--text-muted);
  display: block;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.skill-tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.radar-panel {
  margin-top: 16px;
  padding: 18px;
  background: #EFF6FF;
  border: 1px dashed #BFDBFE;
  border-radius: 16px;
}
.radar-panel-title {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.radar-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}
.radar-label {
  font-size: 12px;
  color: var(--text-body);
  min-width: 68px;
  text-align: right;
  font-weight: 500;
}
.radar-track {
  flex: 1;
  height: 10px;
  background: var(--border-light);
  border-radius: 5px;
  overflow: hidden;
}
.radar-fill {
  height: 100%;
  border-radius: 5px;
  transition: width 0.5s ease;
}
.radar-val {
  font-size: 11px;
  color: var(--text-muted);
  min-width: 34px;
  font-weight: 600;
}

/* ── 就业薪资 ── */
.salary-desc {
  color: var(--text-body);
  font-size: 14px;
  margin-bottom: 12px;
  line-height: 1.6;
}
.salary-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
.salary-table th {
  background: var(--bg-alt);
  color: var(--text-body);
  padding: 10px 14px;
  text-align: left;
  border-bottom: 2px solid var(--border);
  font-weight: 600;
}
.salary-table td {
  padding: 10px 14px;
  border-bottom: 1px solid var(--border-light);
  color: var(--text-body);
}

/* ── 底部固定按钮 ── */
.detail-footer {
  grid-column: span 12;
  position: static;
  padding: 18px;
  background: #EFF6FF;
  border: 1px dashed #93C5FD;
  border-radius: 18px;
  z-index: auto;
  box-shadow: none;
}
.footer-bookmark-btn {
  width: 100%;
  height: 48px;
  font-size: 15px;
  font-weight: 600;
}
.footer-bookmark-btn i {
  margin-right: 4px;
}

/* ═══ AI 智能分析模块 ═══ */
.ai-analysis-section {
  border: 1px solid #BFDBFE;
  background: linear-gradient(135deg, #FFFFFF 0%, #EFF6FF 100%);
}
.section-badge {
  font-size: 11px;
  background: #2563EB;
  color: #fff;
  padding: 3px 10px;
  border-radius: 999px;
  font-weight: 800;
  letter-spacing: 0.5px;
}
.ai-summary {
  background: #FFFFFF;
  border: 1px dashed #BFDBFE;
  border-radius: 14px;
  padding: 18px;
  margin-bottom: 16px;
}
.ai-label {
  font-size: 12px;
  color: #2563EB;
  font-weight: 900;
  margin-bottom: 6px;
}
.ai-label i {
  margin-right: 4px;
}
.ai-summary-text {
  font-size: 15px;
  font-weight: 500;
  color: #1a1a2e;
  line-height: 1.6;
  margin: 0;
}
.ai-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}
.ai-item {
  background: #f8f9fb;
  border-radius: 10px;
  padding: 14px;
  display: flex;
  gap: 10px;
  align-items: flex-start;
}
.ai-item-icon {
  width: 32px;
  height: 32px;
  min-width: 32px;
  border-radius: 10px;
  background: #DBEAFE;
  border: 1px solid #BFDBFE;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2563EB;
  font-size: 14px;
}
.ai-item-label {
  font-size: 12px;
  color: #8EA0B8;
  font-weight: 600;
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.ai-item-content p {
  margin: 0;
  font-size: 13px;
  color: #333;
  line-height: 1.5;
}
.ai-growth {
  background: #FFFFFF;
  border: 1px solid #DBEAFE;
  border-radius: 14px;
  padding: 16px 18px;
  margin-bottom: 12px;
}
.ai-growth-title {
  font-size: 12px;
  font-weight: 900;
  color: #2563EB;
  margin-bottom: 10px;
}
.ai-growth-title i {
  margin-right: 4px;
}
.ai-growth-steps {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.ai-growth-step {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: #444;
  line-height: 1.4;
}
.ai-step-dot {
  width: 10px;
  height: 10px;
  min-width: 10px;
  border-radius: 50%;
}
.ai-footer {
  font-size: 11px;
  color: #8EA0B8;
  text-align: right;
  padding-top: 8px;
  border-top: 1px solid #eee;
}
.ai-footer i {
  margin-right: 4px;
}
.ai-empty {
  text-align: center;
  padding: 20px;
  color: #8EA0B8;
  font-size: 13px;
}

/* ── 视频推荐模块（右侧栏小卡） ── */
.side-video-card {
  padding: 16px 17px 18px;
  flex: 1;
  min-height: 390px;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #FFFFFF 0%, #F8FBFF 100%);
}
.side-video-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
}
.side-video-head .side-kicker {
  margin-bottom: 0;
}
.side-video-head :deep(.el-radio-button__inner) {
  padding: 6px 10px;
  font-size: 12px;
  border-radius: 8px !important;
}
.side-video-loading,
.side-video-empty {
  flex: 1;
  min-height: 86px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748B;
  font-size: 14px;
  background: #F8FBFF;
  border: 1px dashed #BFDBFE;
  border-radius: 14px;
}
.side-video-list {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  align-content: start;
}
.side-video-item {
  min-width: 0;
  display: grid;
  grid-template-columns: 132px minmax(0, 1fr);
  gap: 14px;
  align-items: center;
  min-height: 84px;
  height: auto;
  padding: 9px 12px 9px 9px;
  background: #FFFFFF;
  border: 1px solid #DBEAFE;
  border-radius: 14px;
  cursor: pointer;
  transition: transform .2s, border-color .2s, box-shadow .2s;
}
.side-video-item:hover {
  transform: translateY(-1px);
  border-color: #93C5FD;
  box-shadow: 0 12px 24px rgba(37,99,235,.08);
}
.side-video-thumb {
  width: 132px;
  height: 74px;
  border-radius: 12px;
  overflow: hidden;
  background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2563EB;
  font-weight: 900;
}
.side-video-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.side-video-info {
  min-width: 0;
}
.side-video-info h4 {
  margin: 0 0 7px;
  color: #1E293B;
  font-size: 15px;
  line-height: 1.35;
  font-weight: 900;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.side-video-info p {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin: 0;
  color: #64748B;
  font-size: 12px;
  line-height: 1.35;
}

/* ── 成长路线入口 ── */
.roadmap-entry-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 26px 30px;
  background:
    radial-gradient(circle at 92% 18%, rgba(147,197,253,.22), transparent 28%),
    linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 72%);
}
.roadmap-kicker {
  display: inline-flex;
  margin-bottom: 8px;
  padding: 5px 12px;
  border-radius: 999px;
  background: #FFFFFF;
  border: 1px solid #BFDBFE;
  color: #2563EB;
  font-size: 12px;
  font-weight: 900;
}
.roadmap-entry-copy h3 {
  max-width: 620px;
  margin: 0 0 8px;
  color: #1E293B;
  font-size: 24px;
  line-height: 1.22;
  font-weight: 900;
}
.roadmap-entry-copy p {
  margin: 0;
  color: #475569;
  font-size: 14px;
  line-height: 1.7;
}
.roadmap-entry-btn {
  flex: none;
  min-height: 52px;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 0 22px;
  border: 0;
  border-radius: 16px;
  background: #2563EB;
  color: #FFFFFF;
  font-size: 15px;
  font-weight: 900;
  cursor: pointer;
  box-shadow: 0 16px 30px rgba(37,99,235,.22);
  transition: transform .22s, box-shadow .22s, background .22s;
}
.roadmap-entry-btn:hover {
  transform: translateY(-2px);
  background: #1D4ED8;
  box-shadow: 0 20px 36px rgba(37,99,235,.26);
}
.roadmap-entry-btn i {
  font-style: normal;
  font-size: 18px;
}

/* ── 成长路线（嵌入详情页） ── */
.path-subtitle {
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 400;
}
.semester-timeline {
  position: relative;
  padding-left: 4px;
}
.sem-item {
  display: flex;
  gap: 14px;
  margin-bottom: 6px;
}
.sem-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 20px;
  flex-shrink: 0;
  padding-top: 4px;
}
.sem-dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 12px;
}
.sem-line {
  width: 2px;
  flex: 1;
  background: var(--border);
  min-height: 12px;
}
.sem-content {
  flex: 1;
  padding: 14px;
  margin-bottom: 4px;
}
.sem-content.card {
  border-color: #DBEAFE;
  background: #F8FBFF;
  box-shadow: none;
}
.sem-header {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}
.sem-phase {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-heading);
}
.sem-goal {
  font-size: 12px;
  color: var(--text-muted);
}
.sem-courses,
.sem-certs,
.sem-resources {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 8px;
}
.sem-subtitle {
  width: 100%;
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 500;
  margin-bottom: 2px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.sem-tasks {
  display: flex;
  flex-direction: column;
  gap: 3px;
  margin-bottom: 6px;
}
.task-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 3px 0;
  cursor: pointer;
  border-radius: 4px;
}
.task-item:hover {
  background: var(--bg-hover);
}
.task-cb {
  font-size: 14px;
  flex-shrink: 0;
  line-height: 1;
}
.task-text {
  font-size: 13px;
  color: var(--text-body);
  line-height: 1.4;
}
.task-text.done {
  text-decoration: line-through;
  color: var(--text-muted);
}
.sem-tips {
  font-size: 12px;
  color: #6b7280;
  background: var(--primary-bg);
  padding: 8px 12px;
  border-radius: var(--radius-sm);
  margin-top: 6px;
  display: flex;
  align-items: center;
  gap: 6px;
}

/* ── AI生成内容反馈 ── */
.ai-feedback-banner {
  background: #EFF6FF;
  border: 1px dashed #93C5FD;
  border-radius: 16px;
  padding: 16px;
}
.ai-feedback-banner p {
  font-size: 13px;
  color: #2563EB;
  margin-bottom: 12px;
  display: flex;
  align-items: flex-start;
  gap: 6px;
}
.ai-feedback-banner p i {
  margin-top: 2px;
  flex-shrink: 0;
}
.ai-feedback-btns {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.feedback-msg {
  font-size: 13px;
  color: #059669;
  font-weight: 500;
}

/* ── 路线阶段视频推荐 ── */
.sem-videos {
  margin-top: 12px;
  border-top: 1px dashed var(--border);
  padding-top: 10px;
}
.sem-video-toggle {
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  font-size: 13px;
  color: var(--primary);
  padding: 4px 0;
  user-select: none;
  transition: color 0.2s;
}
.sem-video-toggle:hover {
  color: var(--primary-dark);
}
.sem-video-arrow {
  font-size: 11px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 4px;
}
.sem-video-loading,
.sem-video-empty {
  font-size: 12px;
  color: var(--text-muted);
  text-align: center;
  padding: 10px 0;
}
.sem-video-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
}
.sem-video-card {
  display: flex;
  gap: 10px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 8px;
}
.sv-cover {
  width: 100px;
  flex-shrink: 0;
  position: relative;
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
}
.sv-cover img {
  width: 100%;
  height: 64px;
  object-fit: cover;
}
.sv-duration {
  position: absolute;
  bottom: 3px;
  right: 4px;
  background: rgba(0,0,0,0.6);
  color: white;
  font-size: 9px;
  padding: 1px 5px;
  border-radius: 3px;
}
.sv-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.sv-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-heading);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.3;
}
.sv-meta {
  font-size: 10px;
  color: var(--text-muted);
  display: flex;
  gap: 8px;
}
.sv-meta i {
  margin-right: 2px;
}
.sv-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
}
.sv-link {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  background: #2563EB;
  color: white;
  font-size: 10px;
  padding: 5px 10px;
  border-radius: 999px;
  text-decoration: none;
  font-weight: 800;
  transition: background 0.2s, transform .2s;
}
.sv-link:hover {
  background: #1D4ED8;
  transform: translateY(-1px);
}
.sv-star {
  width: 24px !important;
  height: 24px !important;
  font-size: 10px !important;
}

@media (max-width: 1180px) {
  .career-detail-page {
    max-width: 100%;
    padding-inline: 0;
  }
  .detail-topbar.detail-hero {
    grid-template-columns: 1fr;
  }
  .btn-back {
    width: max-content;
  }
  .detail-hero-paper {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  .hero-desc,
  .hero-tag-strip {
    margin-left: 0;
  }
  .hero-side {
    align-items: stretch;
    padding-right: 0;
  }
  .hero-metrics,
  .hero-pathline,
  .hero-bookmark-btn {
    width: 100%;
  }
  .hero-watermark {
    right: 0;
    top: -10px;
  }
  .detail-main-grid {
    grid-template-columns: 1fr;
  }
  .detail-side-rail {
    position: static;
    order: 0;
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    min-height: 0;
  }
  .side-video-card {
    grid-column: span 2;
    min-height: 0;
  }
  .detail-content-flow > .detail-section,
  .detail-content-flow > .detail-section:nth-of-type(2),
  .detail-content-flow > .detail-section:nth-of-type(3) {
    grid-column: span 12;
  }
}

@media (max-width: 720px) {
  .career-detail-page {
    padding-bottom: 72px;
  }
  .detail-hero-paper {
    padding: 22px 20px 24px;
    border-radius: 22px 22px 10px 22px;
  }
  .detail-topbar-center {
    align-items: flex-start;
  }
  .detail-topbar-title {
    white-space: normal;
    font-size: 30px;
  }
  .hero-pathline {
    align-items: flex-start;
  }
  .hero-pathline i {
    display: none;
  }
  .detail-section {
    padding: 18px;
    border-radius: 16px;
  }
  .detail-side-rail {
    grid-template-columns: 1fr;
  }
  .side-video-card {
    grid-column: auto;
  }
  .side-video-list {
    grid-template-columns: 1fr;
  }
  .ai-grid {
    grid-template-columns: 1fr;
  }
  .detail-video-grid {
    grid-template-columns: 1fr;
  }
}
</style>