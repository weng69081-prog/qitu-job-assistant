<template>
  <div class="career-detail-page">
    <!-- ═══ 头部：返回 + 岗位名称 + 收藏按钮 ═══ -->
    <div class="detail-topbar">
      <button class="btn-back" @click="$router.back()">
        <i class="fas fa-arrow-left"></i>
        <span>返回</span>
      </button>
      <div class="detail-topbar-center">
        <span class="detail-topbar-icon"><i :class="getIcon(careerData.career || '')"></i></span>
        <h1 class="detail-topbar-title">{{ careerData.career || '加载中…' }}</h1>
      </div>
      <el-button
        size="small"
        :type="isBookmarked ? 'warning' : 'default'"
        circle
        @click="toggleBookmark"
        :title="isBookmarked ? '取消收藏' : '收藏此岗位'"
      >
        <i :class="isBookmarked ? 'fas fa-star' : 'far fa-star'"></i>
      </el-button>
    </div>

    <div v-if="loading" class="loading-state"><i class="fas fa-spinner fa-spin"></i> 加载中…</div>
    <template v-else-if="careerData.career">

      <!-- ═══ 模块1：岗位总览 ═══ -->
      <section class="card detail-section">
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
            <div class="wf-arrow" v-if="i < (careerData.work_flow?.length || 0) - 1"><i class="fas fa-chevron-down"></i></div>
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

      <!-- ═══ 模块5：适配人群&避坑提示 ═══ -->
      <section class="card detail-section">
        <div class="section-header">
          <h3 class="section-title"><i class="fas fa-users"></i> 适配人群 &amp; 避坑提示</h3>
        </div>
        <div class="tip-block suitable">
          <div class="tip-icon"><i class="fas fa-check-circle" style="color:#059669"></i></div>
          <div>
            <strong>适合这样的你</strong>
            <p>{{ careerData.suitable_audience || '暂无' }}</p>
          </div>
        </div>
        <div class="tip-block avoid">
          <div class="tip-icon"><i class="fas fa-exclamation-triangle" style="color:#C85A20"></i></div>
          <div>
            <strong>避坑提示</strong>
            <p>{{ careerData.avoid_tips || '暂无' }}</p>
          </div>
        </div>
      </section>

      <!-- ═══ 模块6：📺 职业入门学习视频推荐 ═══ -->
      <section class="card detail-section">
        <div class="section-header">
          <h3 class="section-title"><i class="fas fa-tv"></i> 职业入门学习视频推荐</h3>
        </div>
        <div class="video-filter-bar">
          <el-radio-group v-model="videoSort" size="small" @change="loadVideos">
            <el-radio-button value="hot"><i class="fas fa-fire"></i> 热门</el-radio-button>
            <el-radio-button value="new"><i class="fas fa-clock"></i> 最新</el-radio-button>
          </el-radio-group>
        </div>
        <div v-if="videoLoading" class="loading-state" style="padding:20px 0"><i class="fas fa-spinner fa-spin"></i> 正在搜索B站视频…</div>
        <div v-else-if="videoList.length > 0" class="detail-video-grid">
          <div v-for="(v, idx) in videoList" :key="v.bvid || idx" class="detail-video-card">
            <!-- 封面 -->
            <div class="dv-cover" v-if="v.pic" @click="openVideo(v)">
              <img :src="v.pic" :alt="v.title" @error="onCoverError($event, v)" />
              <span class="dv-duration" v-if="v.duration">{{ v.duration }}</span>
              <div class="dv-overlay"><i class="fas fa-play-circle"></i> 去B站学习</div>
            </div>
            <div class="dv-cover dv-cover-placeholder" v-else @click="openVideo(v)">
              <div class="dv-placeholder-icon"><i class="fas fa-film"></i></div>
              <span class="dv-placeholder-title">{{ cleanTitle(v.title).slice(0, 10) || '入门视频' }}</span>
            </div>
            <!-- 信息 -->
            <div class="dv-info">
              <div class="dv-title" :title="cleanTitle(v.title)">{{ cleanTitle(v.title) }}</div>
              <div class="dv-meta">
                <span v-if="v.author"><i class="fas fa-user"></i> {{ v.author }}</span>
                <span v-if="v.play"><i class="fas fa-play"></i> {{ formatCount(v.play) }}</span>
                <el-button
                  size="small"
                  circle
                  :type="store.isVideoBookmarked(v.bvid) ? 'warning' : 'default'"
                  @click.stop="toggleVideoBookmark(v)"
                  class="dv-star-btn"
                >
                  <i :class="store.isVideoBookmarked(v.bvid) ? 'fas fa-star' : 'far fa-star'"></i>
                </el-button>
              </div>
              <a :href="v.url" target="_blank" rel="noopener noreferrer" class="dv-link" @click.stop="store.recordVideoClick(careerData.career)">
                <i class="fas fa-external-link-alt"></i> 去B站学习
              </a>
            </div>
          </div>
        </div>
        <div v-else class="empty-state" style="padding:20px 0">
          <i class="fas fa-video-slash"></i>
          <p>暂无推荐视频</p>
        </div>
      </section>

      <!-- ═══ 模块7：成长路线（收藏岗位直接展示） ═══ -->
      <section class="card detail-section" v-if="isBookmarked && pathData.length">
        <div class="section-header">
          <h3 class="section-title">
            <i class="fas fa-map-signs"></i> 成长路线
            <span class="path-subtitle">（{{ careerData.career }}方向专属规划）</span>
          </h3>
        </div>
        <div v-if="pathLoading" class="loading-state"><i class="fas fa-spinner fa-spin"></i> 加载中…</div>
        <div v-else class="semester-timeline">
          <div v-for="(sem, idx) in pathData" :key="sem.phase" class="sem-item">
            <div class="sem-marker">
              <div class="sem-dot" :style="{background: semColors[idx % semColors.length]}"></div>
              <div class="sem-line" v-if="idx < pathData.length - 1"></div>
            </div>
            <div class="sem-content card">
              <div class="sem-header">
                <span class="sem-phase">{{ sem.phase }}</span>
                <span class="sem-goal" v-if="sem.goals"><i class="fas fa-bullseye" style="font-size:11px"></i> {{ sem.goals }}</span>
              </div>
              <div class="sem-courses" v-if="sem.courses?.length">
                <div class="sem-subtitle"><i class="fas fa-book"></i> 推荐课程</div>
                <el-tag v-for="c in sem.courses" :key="c" size="small" type="primary" effect="plain">{{ c }}</el-tag>
              </div>
              <div class="sem-certs" v-if="sem.certificates?.length">
                <div class="sem-subtitle"><i class="fas fa-medal"></i> 推荐证书</div>
                <el-tag v-for="cert in sem.certificates" :key="cert" size="small" type="warning" effect="plain">{{ cert }}</el-tag>
              </div>
              <div class="sem-resources" v-if="sem.resources?.length">
                <div class="sem-subtitle"><i class="fas fa-book-open"></i> 推荐资源</div>
                <el-tag v-for="r in sem.resources" :key="r" size="small" type="success" effect="plain">{{ r }}</el-tag>
              </div>
              <div class="sem-tasks">
                <div v-for="(task, ti) in sem.tasks" :key="ti" class="task-item" @click="toggleTask(sem.phase, ti)">
                  <span class="task-cb">
                    <i :class="getTaskDone(sem.phase, ti) ? 'fas fa-check-circle' : 'far fa-square'" :style="{color: getTaskDone(sem.phase, ti) ? '#059669' : '#94a3b8'}"></i>
                  </span>
                  <span :class="['task-text', { done: getTaskDone(sem.phase, ti) }]">{{ task }}</span>
                </div>
              </div>
              <div class="sem-tips" v-if="sem.tips"><i class="fas fa-lightbulb"></i> {{ sem.tips }}</div>
              <!-- 📺 该阶段推荐视频 -->
              <div class="sem-videos">
                <div class="sem-video-toggle" @click="togglePhaseVideos(idx)">
                  <span><i class="fas fa-tv"></i> 推荐学习视频</span>
                  <span class="sem-video-arrow"><i :class="expandedPhaseIdx === idx ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i> {{ expandedPhaseIdx === idx ? '收起' : '展开' }}</span>
                </div>
                <div v-if="expandedPhaseIdx === idx" class="sem-video-list">
                  <div v-if="phaseVideoLoading[idx]" class="sem-video-loading"><i class="fas fa-spinner fa-spin"></i> 搜索视频中…</div>
                  <div v-else-if="(phaseVideos[idx] || []).length === 0" class="sem-video-empty"><i class="fas fa-video-slash"></i> 暂无相关视频</div>
                  <div v-else v-for="(v, vi) in phaseVideos[idx]" :key="v.bvid || vi" class="sem-video-card">
                    <div class="sv-cover" v-if="v.pic" @click="openVideo(v)">
                      <img :src="v.pic" :alt="v.title" />
                      <span class="sv-duration" v-if="v.duration">{{ v.duration }}</span>
                    </div>
                    <div class="sv-info">
                      <div class="sv-title" :title="cleanTitle(v.title)">{{ cleanTitle(v.title) }}</div>
                      <div class="sv-meta">
                        <span v-if="v.author"><i class="fas fa-user"></i> {{ v.author }}</span>
                        <span v-if="v.play"><i class="fas fa-play"></i> {{ formatCount(v.play) }}</span>
                      </div>
                      <div class="sv-actions">
                        <a :href="v.url" target="_blank" rel="noopener noreferrer" class="sv-link"><i class="fas fa-external-link-alt"></i> 去B站学习</a>
                        <el-button
                          size="small"
                          circle
                          :type="store.isVideoBookmarked(v.bvid) ? 'warning' : 'default'"
                          @click.stop="togglePhaseVideoBookmark(v)"
                          class="sv-star"
                        >
                          <i :class="store.isVideoBookmarked(v.bvid) ? 'fas fa-star' : 'far fa-star'"></i>
                        </el-button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ═══ AI生成内容反馈 ═══ -->
      <section class="card detail-section" v-if="careerData.ai_generated">
        <div class="section-header">
          <h3 class="section-title"><i class="fas fa-robot"></i> AI生成内容</h3>
        </div>
        <div class="ai-feedback-banner">
          <p><i class="fas fa-info-circle"></i> 该职业信息由AI生成，仅供参考。如果内容<strong>不准确</strong>或需要<strong>补充</strong>，可以重新生成完善。</p>
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
          <i class="fas fa-star"></i> 收藏此岗位，立即生成专属成长路线
        </el-button>
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

const API = 'http://localhost:8000/api'
const route = useRoute()
const router = useRouter()
const store = useCareerStore()

const careerData = ref({})
const loading = ref(true)

// 视频推荐
const videoList = ref([])
const videoLoading = ref(false)
const videoSort = ref('hot')

async function loadVideos() {
  const name = careerData.value.career
  if (!name) return
  videoLoading.value = true
  try {
    const resp = await axios.get(`${API}/bilibili/search`, {
      params: { career: name, sort: videoSort.value }
    })
    videoList.value = resp.data.videos || []
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
    parent.classList.add('dv-cover-placeholder')
    parent.innerHTML = `<div class="dv-placeholder-icon"><i class="fas fa-film"></i></div><span class="dv-placeholder-title">${(v.title || '').slice(0, 10) || '入门视频'}</span>`
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

const ladderColors = ['#3D5A80','#3D5A80','#3D5A80','#3D5A80','#3D5A80','#3D5A80']

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
    { label: '专业技能', value: 80, color: '#3D5A80' },
    { label: '沟通协作', value: 65, color: '#3D5A80' },
    { label: '学习能力', value: 75, color: '#3D5A80' },
    { label: '解决问题', value: 70, color: '#3D5A80' },
    { label: '抗压能力', value: 60, color: '#3D5A80' },
  ]
})

// ===== 成长路线（收藏岗位直接展示） =====
const pathData = ref([])
const pathLoading = ref(false)
const doneMap = ref({})
const semColors = ['#3D5A80','#3D5A80','#3D5A80','#3D5A80','#3D5A80','#3D5A80','#3D5A80']

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
  max-width: 800px;
  margin: 0 auto;
  padding-bottom: 100px;
}

/* ── 顶部导航条 ── */
.detail-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  gap: 12px;
}
.btn-back {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-body);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}
.btn-back:hover {
  background: var(--primary-bg);
  border-color: var(--primary);
  color: var(--primary);
}
.detail-topbar-center {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  min-width: 0;
}
.detail-topbar-icon {
  width: 38px;
  height: 38px;
  border-radius: var(--radius-sm);
  background: var(--primary-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
  font-size: 17px;
  flex-shrink: 0;
}
.detail-topbar-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-heading);
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ── 模块卡片 ── */
.detail-section {
  margin-bottom: 16px;
}
.detail-section:deep(.section-header) {
  margin-bottom: 14px;
}

/* ── 岗位总览 ── */
.overview-text {
  color: var(--text-body);
  line-height: 1.7;
  font-size: 14px;
  margin-bottom: 16px;
}
.growth-ladder {
  margin-top: 12px;
  padding-top: 14px;
  border-top: 1px solid var(--border-light);
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
  padding: 16px;
  background: var(--bg-alt);
  border-radius: var(--radius-md);
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

/* ── 适配人群 ── */
.tip-block {
  display: flex;
  gap: 12px;
  padding: 14px 16px;
  border-radius: var(--radius-sm);
  margin-bottom: 10px;
}
.tip-block.suitable {
  background: #ecfdf5;
  border: 1px solid #a7f3d0;
}
.tip-block.avoid {
  background: #fffbeb;
  border: 1px solid #fde68a;
}
.tip-icon {
  font-size: 20px;
  flex-shrink: 0;
  margin-top: 1px;
}
.tip-block strong {
  display: block;
  font-size: 14px;
  color: var(--text-heading);
  margin-bottom: 4px;
}
.tip-block p {
  font-size: 13px;
  color: var(--text-body);
  line-height: 1.6;
  margin: 0;
}

/* ── 底部固定按钮 ── */
.detail-footer {
  position: fixed;
  bottom: 0;
  left: 248px;
  right: 0;
  padding: 14px 28px;
  background: var(--bg-card);
  border-top: 1px solid var(--border);
  z-index: 10;
  box-shadow: 0 -2px 8px rgba(0,0,0,0.04);
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

/* ── 视频推荐模块 ── */
.video-filter-bar {
  margin-bottom: 14px;
}
.detail-video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 14px;
}
.detail-video-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: all 0.25s;
}
.detail-video-card:hover {
  border-color: var(--primary-light);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}
.dv-cover {
  position: relative;
  width: 100%;
  aspect-ratio: 16/9;
  overflow: hidden;
  background: var(--bg-alt);
  cursor: pointer;
}
.dv-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}
.detail-video-card:hover .dv-cover img {
  transform: scale(1.05);
}
.dv-duration {
  position: absolute;
  bottom: 6px;
  right: 6px;
  background: rgba(0,0,0,0.7);
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 500;
}
.dv-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  opacity: 0;
  transition: opacity 0.25s;
  color: white;
  font-size: 13px;
  font-weight: 600;
}
.detail-video-card:hover .dv-overlay {
  opacity: 1;
}
.dv-cover-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #eef0ff, #f0f8ff);
  cursor: pointer;
}
.dv-placeholder-icon {
  font-size: 28px;
  color: var(--primary-light);
  margin-bottom: 4px;
}
.dv-placeholder-title {
  font-size: 11px;
  color: var(--text-muted);
}
.dv-info {
  padding: 10px 12px 12px;
}
.dv-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-heading);
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 6px;
  line-height: 1.4;
}
.dv-meta {
  display: flex;
  gap: 10px;
  font-size: 11px;
  color: var(--text-muted);
  margin-bottom: 8px;
  align-items: center;
}
.dv-meta i {
  margin-right: 2px;
}
.dv-star-btn {
  margin-left: auto;
  width: 24px !important;
  height: 24px !important;
  font-size: 11px !important;
}
.dv-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: #C85A20;
  color: white;
  font-size: 11px;
  padding: 5px 12px;
  border-radius: 20px;
  text-decoration: none;
  font-weight: 500;
  transition: background 0.2s;
}
.dv-link:hover {
  background: #B54E1A;
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
  border-color: var(--border-light);
  background: var(--bg-alt);
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
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: var(--radius-md);
  padding: 16px;
}
.ai-feedback-banner p {
  font-size: 13px;
  color: #92400e;
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
  background: #C85A20;
  color: white;
  font-size: 10px;
  padding: 4px 10px;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 500;
  transition: background 0.2s;
}
.sv-link:hover {
  background: #B54E1A;
}
.sv-star {
  width: 24px !important;
  height: 24px !important;
  font-size: 10px !important;
}
</style>