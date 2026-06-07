<template>
  <div class="path-page">
    <section class="path-hero">
      <button class="path-back" @click="$router.back()">
        <ArrowLeft :size="16" />
        <span>返回职业详情</span>
      </button>
      <div class="path-hero-paper">
        <div class="path-copy">
          <span class="path-eyebrow">QITU CAREER ROADMAP</span>
          <h1>{{ careerTitle }}成长路线</h1>
          <p>把大一到大四要学的课程、证书、资源和任务拆成可以照着走的阶段计划，收藏后可以持续打卡追踪。</p>
          <div class="path-tags">
            <span>课程规划</span>
            <span>证书推荐</span>
            <span>学习资源</span>
            <span>阶段任务</span>
          </div>
        </div>
        <aside class="path-summary">
          <span class="summary-watermark">QITU</span>
          <div class="summary-card strong">
            <small>整体完成度</small>
            <strong>{{ totalProgress }}%</strong>
          </div>
          <div class="summary-row">
            <div class="summary-card">
              <small>阶段数</small>
              <strong>{{ routeData.length || 0 }}</strong>
            </div>
            <div class="summary-card">
              <small>路线类型</small>
              <strong>{{ careerTitle === '通用基础' ? '通用' : '专属' }}</strong>
            </div>
          </div>
        </aside>
      </div>
    </section>

    <section class="path-layout">
      <main class="path-main">
        <div v-if="loading" class="loading-state">
          <Loader :size="16" class="spin" />加载中…
        </div>
        <div v-else-if="routeData.length" class="semester-timeline">
          <article v-for="(sem, idx) in routeData" :key="sem.phase || idx" class="semester-card">
            <div class="sem-marker">
              <div class="sem-dot" :style="{ background: semColors[idx % semColors.length] }"></div>
              <div class="sem-line" v-if="idx < routeData.length - 1"></div>
            </div>
            <div class="sem-content">
              <div class="sem-head">
                <div>
                  <span class="sem-kicker">PHASE {{ String(idx + 1).padStart(2, '0') }}</span>
                  <h2>{{ sem.phase }}</h2>
                </div>
                <div class="sem-progress-pill">{{ phaseProgress[sem.phase] || 0 }}%</div>
              </div>
              <p class="sem-goal" v-if="sem.goals">{{ sem.goals }}</p>

              <div class="sem-grid">
                <div class="sem-block" v-if="sem.courses?.length">
                  <span class="block-label">推荐课程</span>
                  <div class="pill-list"><span v-for="c in sem.courses" :key="c">{{ c }}</span></div>
                </div>
                <div class="sem-block" v-if="sem.certificates?.length">
                  <span class="block-label">证书建议</span>
                  <div class="pill-list"><span v-for="cert in sem.certificates" :key="cert">{{ cert }}</span></div>
                </div>
                <div class="sem-block wide" v-if="sem.resources?.length">
                  <span class="block-label">学习资源</span>
                  <div class="pill-list"><span v-for="r in sem.resources" :key="r">{{ r }}</span></div>
                </div>
              </div>

              <div class="task-panel">
                <span class="block-label">阶段任务</span>
                <div class="task-list">
                  <button
                    v-for="(task, ti) in sem.tasks || []"
                    :key="ti"
                    class="task-item"
                    :class="{ done: getTaskDone(sem.phase, 'main', ti) }"
                    @click="toggleTask(sem.phase, 'main', ti)"
                  >
                    <CheckCircle v-if="getTaskDone(sem.phase, 'main', ti)" :size="16" />
                    <Square v-else :size="16" />
                    <span>{{ task }}</span>
                  </button>
                </div>
              </div>

              <div class="stage-video-panel" v-if="getStageKeywords(sem).length">
                <div class="stage-video-head">
                  <div>
                    <span class="block-label">阶段任务推荐学习视频</span>
                    <p>按这个阶段的课程和任务自动匹配，先看入门视频再做打卡任务。</p>
                  </div>
                  <button class="stage-video-btn" @click="loadPhaseVideos(idx, sem)">
                    {{ phaseVideos[idx]?.length ? '刷新推荐' : '加载视频' }}
                  </button>
                </div>
                <div class="stage-keywords">
                  <span v-for="kw in getStageKeywords(sem)" :key="kw">{{ kw }}</span>
                </div>
                <div v-if="phaseVideoLoading[idx]" class="stage-video-loading">正在找适合这个阶段的视频…</div>
                <div v-else-if="phaseVideos[idx]?.length" class="stage-video-grid">
                  <article
                    v-for="(v, vi) in phaseVideos[idx].slice(0, 3)"
                    :key="v.bvid || vi"
                    class="stage-video-card"
                    @click="openVideo(v)"
                  >
                    <div class="stage-video-thumb">
                      <img v-if="v.pic" :src="v.pic" :alt="cleanTitle(v.title)" @error="onCoverError" />
                      <span v-else>{{ vi + 1 }}</span>
                    </div>
                    <div class="stage-video-info">
                      <h4>{{ cleanTitle(v.title) || '阶段学习视频' }}</h4>
                      <p><span v-if="v.author">{{ v.author }}</span><span v-if="v.play">{{ formatCount(v.play) }}播放</span></p>
                    </div>
                  </article>
                </div>
                <div v-else class="stage-video-empty">点击加载视频，或换一个阶段关键词刷新推荐。</div>
              </div>

              <div class="sem-tips" v-if="sem.tips">{{ sem.tips }}</div>
            </div>
          </article>
        </div>
        <div v-else class="empty-state">暂时没有路线数据</div>
      </main>

      <aside class="path-rail">
        <section class="rail-card progress-card">
          <span class="rail-kicker">路线进度</span>
          <strong>{{ totalProgress }}%</strong>
          <div class="progress-track"><i :style="{ width: totalProgress + '%' }"></i></div>
          <p>点选阶段任务即可打卡，进度会保存在本地。</p>
        </section>
        <section class="rail-card">
          <span class="rail-kicker">学习节奏</span>
          <p>先把课程和小项目跑通，再补证书和岗位专项能力，不要一开始就堆太多工具。</p>
        </section>
        <section class="rail-card soft">
          <span class="rail-kicker">启途提示</span>
          <p>每个阶段至少留下一个可展示作品，后面简历和面试才有东西可讲。</p>
        </section>
      </aside>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { useRoute } from 'vue-router'
import { useCareerStore } from '../stores/career'
import axios from 'axios'
import { ArrowLeft, CheckCircle, Loader, Square } from 'lucide-vue-next'

const API = '/api'
const route = useRoute()
const store = useCareerStore()

const loading = ref(true)
const routeData = ref([])
const doneMap = ref(JSON.parse(localStorage.getItem('path_done_map') || '{}'))
const phaseVideos = reactive({})
const phaseVideoLoading = reactive({})
const semColors = ['#2563EB', '#0EA5E9', '#3B82F6', '#60A5FA', '#1D4ED8', '#38BDF8']

const careerTitle = computed(() => {
  const id = route.params.careerId
  return id ? decodeURIComponent(id) : '通用基础'
})

function getTaskKey(phase, type, idx) {
  return `${careerTitle.value}_${phase}_${type}_${idx}`
}
function getTaskDone(phase, type, idx) {
  return doneMap.value[getTaskKey(phase, type, idx)] === true
}
function toggleTask(phase, type, idx) {
  const key = getTaskKey(phase, type, idx)
  doneMap.value[key] = !doneMap.value[key]
  localStorage.setItem('path_done_map', JSON.stringify(doneMap.value))
}

function getStageKeywords(sem) {
  const source = sem?.video_keywords?.length
    ? sem.video_keywords
    : [...(sem?.courses || []), ...(sem?.tasks || [])]
  const keywords = Array.isArray(source) ? source : [source]
  return keywords.filter(Boolean).slice(0, 3)
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

function onCoverError(e) {
  e.target.style.display = 'none'
}

async function loadPhaseVideos(idx, sem) {
  const keywords = getStageKeywords(sem)
  if (!keywords.length) return
  phaseVideoLoading[idx] = true
  try {
    const { data } = await axios.get(`${API}/bilibili/keyword-search`, {
      params: { keyword: keywords[0], sort: 'hot' }
    })
    phaseVideos[idx] = data.videos || []
  } catch {
    phaseVideos[idx] = []
  } finally {
    phaseVideoLoading[idx] = false
  }
}

const phaseProgress = computed(() => {
  const result = {}
  for (const sem of routeData.value) {
    const tasks = sem.tasks || []
    if (!tasks.length) {
      result[sem.phase] = 0
      continue
    }
    const done = tasks.filter((_, idx) => getTaskDone(sem.phase, 'main', idx)).length
    result[sem.phase] = Math.round((done / tasks.length) * 100)
  }
  return result
})

const totalProgress = computed(() => {
  const phases = Object.keys(phaseProgress.value)
  if (!phases.length) return 0
  const sum = phases.reduce((acc, phase) => acc + (phaseProgress.value[phase] || 0), 0)
  return Math.round(sum / phases.length)
})

async function loadData() {
  loading.value = true
  try {
    const careerId = route.params.careerId
    if (careerId && typeof careerId === 'string') {
      const careerName = decodeURIComponent(careerId)
      const saved = await axios.get(`${API}/career/saved-path/${encodeURIComponent(careerName)}`)
      if (saved.data.saved && saved.data.path?.length) {
        routeData.value = saved.data.path
      } else {
        const gen = await axios.post(`${API}/career/save-path`, { career: careerName })
        routeData.value = gen.data.path || []
      }
      store.markPathGenerated(careerName)
    } else {
      const majorCat = localStorage.getItem('major_category') || '计算机类'
      const res = await axios.get(`${API}/career/static-home`, { params: { major_category: majorCat } })
      routeData.value = res.data.growth_path || []
    }
  } catch (e) {
    console.error('加载路线数据失败', e)
    routeData.value = []
  } finally {
    loading.value = false
    routeData.value.forEach((sem, idx) => loadPhaseVideos(idx, sem))
  }
}

onMounted(loadData)
</script>

<style scoped>
.path-page {
  width: auto;
  max-width: none;
  margin: 0 calc(var(--main-pad-x, 28px) * -1);
  padding: 0 18px 96px;
  color: #1E293B;
}
.path-hero {
  margin-bottom: 22px;
}
.path-back {
  min-height: 38px;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 10px;
  padding: 0 14px;
  border: 1px solid #BFDBFE;
  border-radius: 999px;
  background: #FFFFFF;
  color: #2563EB;
  font-size: 13px;
  font-weight: 900;
  cursor: pointer;
  box-shadow: 0 10px 24px rgba(37,99,235,.08);
}
.path-hero-paper {
  position: relative;
  min-height: 250px;
  display: grid;
  grid-template-columns: minmax(0, 1.45fr) minmax(440px, .55fr);
  gap: 46px;
  padding: 28px 42px 32px;
  overflow: hidden;
  background: radial-gradient(circle at 86% 8%, rgba(147,197,253,.26), transparent 32%), linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 48%, #F8FBFF 100%);
  border: 1px solid #CFE4FF;
  border-radius: 30px 30px 12px 30px;
  box-shadow: 0 22px 50px rgba(37,99,235,.11), inset 0 1px 0 rgba(255,255,255,.88);
}
.path-hero-paper::after {
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
}
.path-copy,
.path-summary {
  position: relative;
  z-index: 1;
}
.path-eyebrow {
  display: inline-flex;
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
.path-copy h1 {
  max-width: 760px;
  margin: 0;
  color: #1E293B;
  font-size: clamp(38px, 4vw, 56px);
  line-height: 1.03;
  font-weight: 900;
  letter-spacing: -0.04em;
}
.path-copy p {
  max-width: 68ch;
  margin: 18px 0 0;
  color: #475569;
  font-size: 17px;
  line-height: 1.9;
}
.path-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 18px;
}
.path-tags span {
  display: inline-flex;
  min-height: 30px;
  align-items: center;
  padding: 0 12px;
  border-radius: 999px;
  background: rgba(255,255,255,.78);
  border: 1px solid #BFDBFE;
  color: #2563EB;
  font-size: 14px;
  font-weight: 900;
}
.path-summary {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 12px;
}
.summary-watermark {
  position: absolute;
  right: 0;
  top: -14px;
  color: rgba(37,99,235,.10);
  font-size: 68px;
  font-weight: 900;
  letter-spacing: .10em;
}
.summary-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}
.summary-card {
  position: relative;
  padding: 14px 16px;
  border: 1px solid #DBEAFE;
  border-radius: 16px;
  background: rgba(255,255,255,.78);
  box-shadow: 0 10px 24px rgba(37,99,235,.055);
}
.summary-card.strong strong {
  font-size: 34px;
}
.summary-card small {
  display: block;
  margin-bottom: 6px;
  color: #64748B;
  font-size: 13px;
  font-weight: 800;
}
.summary-card strong {
  color: #2563EB;
  font-size: 22px;
  line-height: 1;
  font-weight: 900;
}
.path-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) clamp(420px, 28vw, 500px);
  gap: 28px;
  align-items: start;
}
.path-main {
  min-width: 0;
}
.semester-timeline {
  display: grid;
  gap: 18px;
}
.semester-card {
  display: grid;
  grid-template-columns: 28px minmax(0, 1fr);
  gap: 14px;
}
.sem-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 28px;
}
.sem-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  box-shadow: 0 0 0 5px #EFF6FF;
}
.sem-line {
  width: 2px;
  flex: 1;
  min-height: 100%;
  margin-top: 8px;
  background: #BFDBFE;
}
.sem-content {
  padding: 24px 26px;
  border: 1px solid #DBEAFE;
  border-radius: 22px;
  background: #FFFFFF;
  box-shadow: 0 14px 34px rgba(15,23,42,.04);
}
.sem-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
  margin-bottom: 12px;
}
.sem-kicker {
  display: block;
  margin-bottom: 6px;
  color: #2563EB;
  font-size: 13px;
  font-weight: 900;
  letter-spacing: .08em;
}
.sem-head h2 {
  margin: 0;
  color: #1E293B;
  font-size: 28px;
  line-height: 1.15;
  font-weight: 900;
}
.sem-progress-pill {
  flex: none;
  min-width: 58px;
  padding: 7px 10px;
  border-radius: 999px;
  background: #EFF6FF;
  color: #2563EB;
  text-align: center;
  font-size: 14px;
  font-weight: 900;
}
.sem-goal {
  margin: 0 0 16px;
  color: #475569;
  font-size: 17px;
  line-height: 1.75;
}
.sem-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 16px;
}
.sem-block,
.task-panel {
  padding: 14px;
  border: 1px dashed #BFDBFE;
  border-radius: 16px;
  background: #F8FBFF;
}
.sem-block.wide {
  grid-column: span 2;
}
.block-label,
.rail-kicker {
  display: block;
  margin-bottom: 9px;
  color: #2563EB;
  font-size: 14px;
  font-weight: 900;
}
.pill-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.pill-list span {
  display: inline-flex;
  min-height: 28px;
  align-items: center;
  padding: 0 10px;
  border-radius: 999px;
  background: #FFFFFF;
  border: 1px solid #DBEAFE;
  color: #1D4ED8;
  font-size: 13px;
  font-weight: 800;
}
.task-list {
  display: grid;
  gap: 8px;
}
.task-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #DBEAFE;
  border-radius: 12px;
  background: #FFFFFF;
  color: #334155;
  text-align: left;
  font-size: 16px;
  line-height: 1.5;
  font-weight: 800;
  cursor: pointer;
}
.task-item svg {
  flex: none;
  color: #2563EB;
}
.task-item.done {
  background: #EFF6FF;
  color: #64748B;
  text-decoration: line-through;
}
.stage-video-panel {
  margin-top: 14px;
  padding: 15px;
  border: 1px solid #DBEAFE;
  border-radius: 18px;
  background: linear-gradient(135deg, #FFFFFF 0%, #F8FBFF 100%);
}
.stage-video-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 10px;
}
.stage-video-head .block-label {
  margin-bottom: 6px;
}
.stage-video-head p {
  margin: 0;
  color: #64748B;
  font-size: 15px;
  line-height: 1.6;
  font-weight: 700;
}
.stage-video-btn {
  flex: none;
  min-height: 34px;
  padding: 0 13px;
  border: 1px solid #BFDBFE;
  border-radius: 999px;
  background: #EFF6FF;
  color: #2563EB;
  font-size: 13px;
  font-weight: 900;
  cursor: pointer;
}
.stage-keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin-bottom: 12px;
}
.stage-keywords span {
  min-height: 24px;
  display: inline-flex;
  align-items: center;
  padding: 0 9px;
  border-radius: 999px;
  background: #EFF6FF;
  color: #2563EB;
  font-size: 12px;
  font-weight: 900;
}
.stage-video-loading,
.stage-video-empty {
  min-height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px dashed #BFDBFE;
  border-radius: 14px;
  background: #F8FBFF;
  color: #2563EB;
  font-size: 13px;
  font-weight: 900;
}
.stage-video-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}
.stage-video-card {
  min-width: 0;
  display: grid;
  grid-template-columns: 88px minmax(0, 1fr);
  gap: 10px;
  align-items: center;
  min-height: 82px;
  padding: 9px;
  border: 1px solid #DBEAFE;
  border-radius: 14px;
  background: #FFFFFF;
  cursor: pointer;
  transition: transform .2s, border-color .2s, box-shadow .2s;
}
.stage-video-card:hover {
  transform: translateY(-1px);
  border-color: #93C5FD;
  box-shadow: 0 12px 24px rgba(37,99,235,.08);
}
.stage-video-thumb {
  width: 88px;
  height: 58px;
  overflow: hidden;
  border-radius: 11px;
  background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2563EB;
  font-weight: 900;
}
.stage-video-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.stage-video-info {
  min-width: 0;
}
.stage-video-info h4 {
  margin: 0 0 5px;
  color: #1E293B;
  font-size: 14px;
  line-height: 1.35;
  font-weight: 900;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.stage-video-info p {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin: 0;
  color: #64748B;
  font-size: 12px;
  line-height: 1.35;
}
.sem-tips {
  margin-top: 14px;
  padding: 12px 14px;
  border: 1px solid #BFDBFE;
  border-radius: 14px;
  background: #EFF6FF;
  color: #1D4ED8;
  font-size: 16px;
  line-height: 1.7;
  font-weight: 800;
}
.path-rail {
  position: sticky;
  top: 22px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.rail-card {
  padding: 18px;
  border: 1px solid #DBEAFE;
  border-radius: 18px;
  background: #FFFFFF;
  box-shadow: 0 14px 32px rgba(37,99,235,.06);
}
.rail-card.soft,
.progress-card {
  background: linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 78%);
}
.rail-card strong {
  display: block;
  color: #1E293B;
  font-size: 34px;
  line-height: 1;
  font-weight: 900;
}
.rail-card p {
  margin: 10px 0 0;
  color: #475569;
  font-size: 15px;
  line-height: 1.75;
}
.progress-track {
  height: 10px;
  margin-top: 12px;
  overflow: hidden;
  border-radius: 999px;
  background: #DBEAFE;
}
.progress-track i {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: #2563EB;
}
.loading-state,
.empty-state {
  min-height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: 1px dashed #BFDBFE;
  border-radius: 22px;
  background: #F8FBFF;
  color: #2563EB;
  font-weight: 900;
}
.spin {
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 1180px) {
  .path-page {
    padding-inline: 0;
  }
  .path-hero-paper,
  .path-layout {
    grid-template-columns: 1fr;
  }
  .path-rail {
    position: static;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
@media (max-width: 900px) {
  .stage-video-grid {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 720px) {
  .path-hero-paper {
    padding: 24px 22px 28px;
  }
  .path-summary,
  .path-rail,
  .sem-grid {
    grid-template-columns: 1fr;
  }
  .sem-block.wide {
    grid-column: auto;
  }
  .semester-card {
    grid-template-columns: 1fr;
  }
  .sem-marker {
    display: none;
  }
  .stage-video-head {
    flex-direction: column;
  }
  .stage-video-card {
    grid-template-columns: 84px minmax(0, 1fr);
  }
  .stage-video-thumb {
    width: 84px;
    height: 56px;
  }
}
</style>
