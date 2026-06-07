<template>
  <div class="career-list-page">
    <!-- ═══ 页面顶部 Banner ═══ -->
    <div class="banner-wrap">
      <PageBanner fullwidth
        title="职业探索"
        description="从兴趣到岗位，规划你的第一条职业路线"
        :icon="'Compass'"
        variant="primary"
        cat-src="/src/assets/new-explore-cat.png"
        cat-alt="小橘探路"
        :path-items="['探索方向', '成长路线', '收藏路线']"
      />
    </div>
    <!-- ═══ 主体：左侧平板职业清单 + 右侧视频推荐 ═══ -->
    <div class="explore-workbench">
      <aside class="career-tablet-shell">
        <div class="tablet-device">
          <div class="tablet-camera"></div>
          <div class="tablet-screen">
            <div class="tablet-statusbar">
              <span class="tablet-time">{{ tabletTime }}</span>
              <div class="tablet-system-icons" aria-hidden="true">
                <span class="tablet-signal"><i></i><i></i><i></i></span>
                <span class="tablet-wifi"></span>
                <span class="tablet-battery"><i></i></span>
              </div>
            </div>
            <div class="tablet-header">
              <span class="tablet-title">职业口袋清单</span>
              <div class="tablet-search">
                <Search :size="16" class="icon-blue" />
                <el-input
                  v-model="searchQuery"
                  placeholder="搜索岗位名称…"
                  clearable
                  size="large"
                />
              </div>
              <span class="career-count"><Briefcase :size="16" class="icon-blue" /> {{ filteredCareers.length }} 个</span>
            </div>

            <div class="tablet-categories">
              <button
                v-for="c in majorCategories"
                :key="c"
                class="major-chip"
                :class="{ active: selectedCategory === c }"
                @click="selectCategory(c)"
              >{{ c }}</button>
            </div>

            <div class="filter-bar">
              <div class="filter-line">
                <span class="filter-label"><Signal :size="16" class="icon-blue" /> 入门难度</span>
                <div class="filter-tags">
                  <span
                    v-for="d in difficultyOptions" :key="d"
                    class="filter-tag"
                    :class="{ active: selectedDifficulties.includes(d) }"
                    @click="toggleDifficulty(d)"
                  >{{ d }}</span>
                </div>
              </div>
              <div class="filter-line">
                <span class="filter-label"><Briefcase :size="16" class="icon-blue" /> 工作类型</span>
                <div class="filter-tags">
                  <span
                    v-for="t in workTypeOptions" :key="t"
                    class="filter-tag"
                    :class="{ active: selectedWorkTypes.includes(t) }"
                    @click="toggleWorkType(t)"
                  >{{ t }}</span>
                </div>
              </div>
              <div class="filter-line salary-filter-line">
                <span class="filter-label"><Coins :size="16" class="icon-blue" /> 薪资标签</span>
                <div class="filter-tags">
                  <span
                    v-for="s in salaryTagOptions" :key="s"
                    class="filter-tag"
                    :class="{ active: selectedSalaryTags.includes(s) }"
                    @click="toggleSalaryTag(s)"
                  >{{ s }}</span>
                </div>
              </div>
            </div>

            <div v-if="store.validBookmarks.length > 0" class="bookmark-band">
              <div class="bm-band-header">
                <span class="bm-band-title"><Star :size="16" class="icon-blue" /> 已收藏 <b>{{ store.validBookmarks.length }}</b></span>
                <el-button text size="small" @click="$router.push('/settings')">管理 <ArrowRight :size="16" class="icon-blue" /></el-button>
              </div>
              <div class="bm-band-scroll">
                <div
                  v-for="b in store.validBookmarks.slice(0, 4)"
                  :key="b.career"
                  class="bm-band-card"
                  @click="goDetail(b.career)"
                >
                  <div class="bm-band-top">
                    <span class="bm-band-name">{{ b.career }}</span>
                    <span class="bm-band-badge" v-if="store.hasGeneratedPath(b.career)" title="已生成成长路线"><Map :size="16" class="icon-blue" /></span>
                  </div>
                  <div class="bm-band-meta">{{ b.difficulty }} · {{ b.salary }}</div>
                </div>
              </div>
            </div>

            <div class="tablet-career-list">
              <div v-if="loading" class="loading-state"><Loader :size="16" class="icon-blue" /> 加载中…</div>
              <div v-else-if="aiSearchLoading" class="empty-state">
                <div class="ai-searching">
                  <span class="empty-icon"><Bot :size="16" class="icon-blue" /></span>
                  <p>正在补充该职业信息…</p>
                  <p class="empty-hint">AI正在生成 <b>{{ searchQuery }}</b></p>
                  <el-progress :percentage="80" :stroke-width="4" style="max-width:260px;margin:1rem auto" />
                </div>
              </div>
              <div v-else-if="filteredCareers.length === 0 && !searchQuery" class="empty-state">
                <span class="empty-icon"><Search :size="16" class="icon-blue" /></span>
                <p>没有找到匹配的岗位</p>
                <p class="empty-hint">试试调整筛选条件或选择其他专业</p>
              </div>
              <div v-else-if="aiSearchError" class="empty-state">
                <span class="empty-icon"><TriangleAlert :size="16" class="icon-blue" /></span>
                <p>搜索出错：{{ aiSearchError }}</p>
                <p class="empty-hint">请重试或换一个关键词</p>
              </div>
              <div v-else-if="filteredCareers.length === 0 && searchQuery" class="empty-state">
                <span class="empty-icon"><Search :size="16" class="icon-blue" /></span>
                <p>没搜到「{{ searchQuery }}」的结果</p>
                <p class="empty-hint">AI正在生成信息…</p>
              </div>
              <div v-else class="career-grid">
                <div
                  v-for="c in filteredCareers"
                  :key="c.career"
                  class="card career-card"
                  :class="{ 'is-bookmarked': store.isBookmarked(c.career), 'ai-gen-card': c.ai_generated }"
                  @click="goDetail(c.career)"
                >
                  <div class="card-ribbon" v-if="store.isBookmarked(c.career)"><Star :size="16" class="icon-blue" /> 已收藏</div>
                  <div class="card-body">
                    <div class="card-icon">{{ getIcon(c.career) }}</div>
                    <div class="card-title-area">
                      <div class="card-title-row">
                        <strong class="card-name">{{ c.career }}</strong>
                        <span class="card-path-badge" v-if="store.hasGeneratedPath(c.career)" title="已生成成长路线"><Map :size="16" class="icon-blue" /></span>
                        <el-tag v-if="c.ai_generated" size="small" type="danger" class="new-tag">新</el-tag>
                      </div>
                      <span class="card-intro">{{ c.short_intro || '' }}</span>
                    </div>
                  </div>
                  <div class="card-tag-row card-meta-row">
                    <span class="tag-pill" :class="difficultyType(c.difficulty) === 'success' ? 'green' : difficultyType(c.difficulty) === 'warning' ? 'orange' : difficultyType(c.difficulty) === 'danger' ? 'red' : 'gray'"><Signal :size="16" class="icon-blue" /> {{ c.difficulty }}</span>
                    <span class="tag-pill green"><Briefcase :size="16" class="icon-blue" /> {{ c.work_type || '技术类' }}</span>
                    <span v-if="c.keywords" v-for="kw in (c.keywords || []).slice(0,2)" :key="kw" class="tag-pill gray"><Tag :size="16" class="icon-blue" /> {{ kw }}</span>
                  </div>
                  <div class="card-tag-row card-salary-row">
                    <span class="tag-pill blue salary-pill"><Coins :size="16" class="icon-blue" /> {{ c.salary_tag || c.salary }}</span>
                    <div class="card-actions">
                      <el-button
                        size="small"
                        :type="store.isBookmarked(c.career) ? 'warning' : 'default'"
                        circle
                        @click.stop="toggleBookmark(c)"
                        :title="store.isBookmarked(c.career) ? '取消收藏' : '收藏岗位'"
                      ><Star :size="16" class="icon-blue" :class="store.isBookmarked(c.career) ? 'fas fa-star' : 'far fa-star'" /></el-button>
                      <el-button
                        size="small"
                        type="primary"
                        circle
                        plain
                        @click.stop="scrollToVideos(c.career)"
                        title="入门学习视频"
                      ><Monitor :size="16" class="icon-blue" /></el-button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </aside>

      <section class="video-recommend-section" ref="videoSection">
        <div class="video-panel-head">
          <div>
            <span class="section-kicker">LEARNING VIDEO</span>
            <h2>职业入门学习推荐视频</h2>
            <p>先看一个方向的视频，再去左侧平板清单里收藏岗位和生成路线。</p>
          </div>
          <span v-if="selectedVideoCareer" class="section-title-badge">{{ selectedVideoCareer }}</span>
        </div>
        <div class="video-section-controls">
          <el-radio-group v-model="videoSort" size="small" @change="loadVideos(selectedVideoCareer)">
            <el-radio-button value="hot"><Flame :size="16" class="icon-blue" /> 热门</el-radio-button>
            <el-radio-button value="new"><Star :size="16" class="icon-blue" /> 最新</el-radio-button>
          </el-radio-group>
        </div>

        <div v-if="videoLoading" class="loading-state video-loading"><Loader :size="16" class="icon-blue" /> 正在搜索B站视频…</div>

        <div v-else-if="videoList.length > 0" class="video-grid">
          <div
            v-for="(v, idx) in videoList"
            :key="v.bvid || idx"
            class="card video-card"
          >
            <div class="video-cover" v-if="v.pic" @click="openVideo(v)">
              <img :src="v.pic" :alt="v.title" @error="onCoverError($event, v)" />
              <span class="video-duration" v-if="v.duration">{{ v.duration }}</span>
              <div class="video-cover-overlay">
                <span class="overlay-play"><Play :size="16" class="icon-blue" /> 去B站学习</span>
              </div>
            </div>
            <div class="video-cover video-cover-placeholder" v-else @click="openVideo(v)">
              <span class="placeholder-icon"><Film :size="16" class="icon-blue" /></span>
              <span class="placeholder-title">{{ v.title?.slice(0, 12) || '入门视频' }}</span>
            </div>

            <div class="video-info">
              <div class="video-title-row">
                <span class="video-title" :title="cleanTitle(v.title)">{{ cleanTitle(v.title) }}</span>
                <el-button
                  size="small"
                  circle
                  :type="store.isVideoBookmarked(v.bvid) ? 'warning' : 'default'"
                  @click.stop="toggleVideoBookmark(v)"
                  class="video-star-btn"
                  :title="store.isVideoBookmarked(v.bvid) ? '取消收藏视频' : '收藏视频'"
                ><Star :size="16" class="icon-blue" :class="store.isVideoBookmarked(v.bvid) ? 'fas fa-star' : 'far fa-star'" /></el-button>
              </div>
              <div class="video-meta">
                <span class="video-author" v-if="v.author"><User :size="16" class="icon-blue" /> {{ v.author }}</span>
                <span class="video-stats" v-if="v.play">
                  <span><Play :size="16" class="icon-blue" /> {{ formatCount(v.play) }}</span>
                  <span v-if="v.danmaku"> <MessageSquare :size="16" class="icon-blue" /> {{ formatCount(v.danmaku) }}</span>
                </span>
              </div>
              <p class="video-description" v-if="v.description">{{ v.description?.slice(0, 34) }}{{ v.description?.length > 34 ? '…' : '' }}</p>
              <a
                :href="v.url"
                target="_blank"
                rel="noopener noreferrer"
                class="video-link-btn"
                @click.stop="onVideoClick(v)"
              >
                去B站学习 <ArrowRight :size="16" class="icon-blue" />
              </a>
            </div>
          </div>
        </div>

        <div v-else class="empty-state video-empty">
          <span class="empty-icon"><Video :size="16" class="icon-blue" /></span>
<p>暂无推荐视频</p>
          <p class="empty-hint">先在左侧选一个岗位查看推荐</p>
        </div>
      </section>
    </div>
  </div>
    <!-- ═══ 品牌 Footer ═══ -->
    <div class="brand-footer">
      <div>启途 · <span class="qitu-up">QITU</span></div>
      <div class="qitu-sl">向上生长，自有答案</div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useCareerStore } from '../stores/career'
import axios from 'axios'
import PageBanner from '../components/PageBanner.vue'

const API = '/api'
const router = useRouter()
const store = useCareerStore()

// 数据
const selectedCategory = ref('计算机类')
const majorCategories = ['计算机类', '机电土木类', '经管财会类', '文法艺术类', '医药护理类', '教育师范类', '农林类', '轻工制造类']
const allCareers = ref([])
const loading = ref(false)

// AI搜索兜底
const aiSearchLoading = ref(false)
const aiSearchError = ref('')

// 搜索 & 筛选
const searchQuery = ref('')
const selectedDifficulties = ref([])
const selectedWorkTypes = ref([])
const selectedSalaryTags = ref([])

const difficultyOptions = ['低', '中', '高']
const workTypeOptions = ['技术类', '设计类', '运营类', '市场类', '职能类', '研究类']
const salaryTagOptions = ['8K起', '10K起', '15K起', '20K起']
const tabletTime = computed(() => {
  const now = new Date()
  return now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', hour12: false })
})

// 视频推荐模块
const videoSection = ref(null)
const selectedVideoCareer = ref('')
const videoList = ref([])
const videoLoading = ref(false)
const videoSort = ref('hot')

// 收藏 — 使用 Pinia store
function toggleBookmark(career) {
  if (store.isBookmarked(career.career)) {
    store.removeBookmark(career.career)
  } else {
    store.addBookmark(career)
    // 收藏时自动生成并保存成长路线
    axios.post('/api/career/save-path', { career: career.career }).catch(() => {})
  }
}

// 视频加载
async function loadVideos(careerName) {
  if (!careerName) {
    // 优先展示收藏岗位的视频
    for (const b of store.validBookmarks) {
      careerName = b.career
      break
    }
    if (!careerName && filteredCareers.value.length > 0) {
      careerName = filteredCareers.value[0].career
    } else if (!careerName) {
      return
    }
  }
  selectedVideoCareer.value = careerName
  videoLoading.value = true
  try {
    const resp = await axios.get(`${API}/bilibili/search`, {
      params: { career: careerName, major_category: selectedCategory.value, sort: videoSort.value }
    })
    videoList.value = resp.data.videos || []
  } catch (e) {
    console.error('加载视频失败', e)
    videoList.value = []
  } finally {
    videoLoading.value = false
  }
}

// 收藏/取消收藏视频
function toggleVideoBookmark(video) {
  const v = { ...video, career: selectedVideoCareer.value }
  if (store.isVideoBookmarked(video.bvid)) {
    store.removeVideoBookmark(video.bvid)
  } else {
    store.addVideoBookmark(v)
  }
}

// 点击去B站学习 → 记录点击
function onVideoClick(v) {
  store.recordVideoClick(selectedVideoCareer.value)
  // 跳转由 a 标签的 href 自动处理
}

// 滚动到视频区
async function scrollToVideos(careerName) {
  await loadVideos(careerName)
  nextTick(() => {
    if (videoSection.value) {
      videoSection.value.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  })
}

// 封面图加载失败时显示占位
function onCoverError(e, v) {
  e.target.style.display = 'none'
  const parent = e.target.parentElement
  if (parent) {
    parent.classList.add('video-cover-placeholder')
    parent.innerHTML = `<div class="placeholder-icon">🎬</div><span class="placeholder-title">${(v.title || '').slice(0, 12) || '入门视频'}</span>`
  }
}

// 打开 B 站视频
function openVideo(v) {
  if (v.url) {
    window.open(v.url, '_blank', 'noopener,noreferrer')
  }
}

// 清理标题中的HTML标签
function cleanTitle(title) {
  if (!title) return ''
  return title.replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'")
}

// 格式化播放量
function formatCount(n) {
  if (!n) return '0'
  n = parseInt(n)
  if (n >= 10000) return (n / 10000).toFixed(1) + '万'
  if (n >= 1000) return (n / 1000).toFixed(1) + 'k'
  return n.toString()
}

// 筛选逻辑
const filteredCareers = computed(() => {
  let list = allCareers.value
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(c =>
      c.career.toLowerCase().includes(q) ||
      (c.keywords || []).some(k => k.toLowerCase().includes(q)) ||
      (c.responsibilities || []).some(r => r.toLowerCase().includes(q))
    )
  }
  if (selectedDifficulties.value.length) {
    list = list.filter(c => selectedDifficulties.value.includes(c.difficulty))
  }
  if (selectedWorkTypes.value.length) {
    list = list.filter(c => selectedWorkTypes.value.includes(c.work_type || '技术类'))
  }
  if (selectedSalaryTags.value.length) {
    list = list.filter(c => selectedSalaryTags.value.some(s => (c.salary_tag || c.salary || '').includes(s.replace('K起',''))))
  }
  return list
})

function toggleDifficulty(d) {
  const idx = selectedDifficulties.value.indexOf(d)
  idx >= 0 ? selectedDifficulties.value.splice(idx, 1) : selectedDifficulties.value.push(d)
}
function toggleWorkType(t) {
  const idx = selectedWorkTypes.value.indexOf(t)
  idx >= 0 ? selectedWorkTypes.value.splice(idx, 1) : selectedWorkTypes.value.push(t)
}
function toggleSalaryTag(s) {
  const idx = selectedSalaryTags.value.indexOf(s)
  idx >= 0 ? selectedSalaryTags.value.splice(idx, 1) : selectedSalaryTags.value.push(s)
}

// 工具函数
function getIcon(name) {
  const icons = { '前端':'🌐','后端':'⚙️','数据':'📊','测试':'🔍','安全':'🛡️','产品':'📱','运营':'📈','设计':'🎨','算法':'🧠','运维':'🔧','工程':'🏗️','管理':'👔' }
  for (const [k, v] of Object.entries(icons)) {
    if (name.includes(k)) return v
  }
  return '💼'
}
function difficultyType(d) {
  return { '低':'success','初级':'success','中':'warning','中级':'warning','高':'danger','高级':'danger' }[d] || 'info'
}

// 跳转详情
function goDetail(name) {
  router.push(`/career/${encodeURIComponent(name)}`)
}

// 切换专业
function selectCategory(category) {
  if (selectedCategory.value === category) return
  selectedCategory.value = category
  loadCareers()
}

// 搜索监听 — 本地没结果时触发AI兜底
let searchTimer = null
watch(searchQuery, (val) => {
  if (searchTimer) clearTimeout(searchTimer)
  aiSearchError.value = ''
  if (!val || !val.trim()) {
    aiSearchLoading.value = false
    return
  }
  // 延迟300ms，等客户端过滤完成
  searchTimer = setTimeout(async () => {
    if (filteredCareers.value.length > 0) {
      aiSearchLoading.value = false
      return
    }
    // 客户端过滤为空 → 调用后端AI搜索
    aiSearchLoading.value = true
    try {
      const res = await axios.get(`${API}/career/search`, {
        params: { q: val.trim(), major_category: selectedCategory.value }
      })
      if (res.data.careers && res.data.careers.length > 0) {
        const aiCareer = res.data.careers[0]
        // 检查是否已存在
        const exists = allCareers.value.some(c => c.career.toLowerCase() === aiCareer.career.toLowerCase())
        if (!exists) {
          allCareers.value.unshift(aiCareer)
        }
      }
    } catch (e) {
      console.error('AI搜索失败', e)
      aiSearchError.value = 'AI搜索失败，请重试'
    } finally {
      aiSearchLoading.value = false
    }
  }, 300)
})

// 加载数据
async function loadCareers() {
  loading.value = true
  try {
    const res = await axios.get(`${API}/career/static-home`, {
      params: { major_category: selectedCategory.value }
    })
    allCareers.value = res.data.careers || []
  } catch (e) {
    console.error('加载职业数据失败', e)
    allCareers.value = []
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadCareers()
  // 自动加载视频 — 优先展示收藏岗位的视频
  nextTick(() => {
    if (filteredCareers.value.length > 0) {
      // ① 有收藏且有点击记录 → 选点击最多的收藏岗位
      // ② 有收藏无点击 → 第一个收藏岗位
      // ③ 无收藏 → 列表第一个
      let targetCareer = null
      
      // 先选点击最多的收藏岗位
      const clickedBookmark = store.bookmarksSortedByClicks[0]
      if (clickedBookmark && filteredCareers.value.find(c => c.career === clickedBookmark.career)) {
        targetCareer = clickedBookmark.career
      }
      
      // 没有匹配的 → 第一个收藏岗位（在当前筛选列表里的）
      if (!targetCareer) {
        for (const b of store.validBookmarks) {
          if (filteredCareers.value.find(c => c.career === b.career)) {
            targetCareer = b.career
            break
          }
        }
      }
      
      // 还没找到 → 列表第一个
      if (!targetCareer) {
        targetCareer = filteredCareers.value[0].career
      }
      
      loadVideos(targetCareer)
    }
  })
})
</script>

<style scoped>
.career-list-page {
  padding: 0 0 8px;
  position: relative;
}
.banner-wrap {
  position: relative;
  margin-top: 0;
}

/* 顶部搜索栏 */
.career-count {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.82rem;
  color: #2563EB;
  font-weight: 800;
}

/* 顶部框下方：左侧平板职业清单 + 右侧窄视频推荐栏 */
.explore-workbench {
  display: grid;
  grid-template-columns: minmax(0, 2.05fr) minmax(270px, .74fr);
  gap: 40px;
  align-items: start;
  margin-top: 58px;
}
.career-tablet-shell {
  min-width: 0;
}
.tablet-device {
  position: relative;
  width: 100%;
  min-height: 0;
  padding: 12px;
  border-radius: 30px;
  background: linear-gradient(145deg, #DCEBFA 0%, #FFFFFF 45%, #CFE2F7 100%);
  border: 1px solid rgba(147,197,253,.76);
  box-shadow: 18px 22px 44px rgba(37,99,235,.12), inset 0 0 0 1px rgba(255,255,255,.88);
}
.tablet-device::after {
  content: '';
  position: absolute;
  inset: 8px;
  border-radius: 24px;
  border: 1px dashed rgba(37,99,235,.18);
  pointer-events: none;
}
.tablet-camera {
  position: absolute;
  top: 18px;
  left: 50%;
  width: 12px;
  height: 12px;
  transform: translateX(-50%);
  border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, #64748B 0 18%, #1E293B 42%, #0F172A 100%);
  z-index: 2;
  box-shadow: 0 0 0 4px rgba(255,255,255,.72), inset 0 -1px 0 rgba(255,255,255,.20);
}
.tablet-screen {
  position: relative;
  z-index: 1;
  height: min(68vh, 680px);
  min-height: 610px;
  overflow-y: auto;
  padding: 0 18px 18px;
  border-radius: 22px;
  background: linear-gradient(180deg, #FFFFFF 0%, #F8FBFF 54%, #EFF6FF 100%);
  border: 1px solid rgba(255,255,255,.92);
  overflow-x: hidden;
}
.tablet-screen::-webkit-scrollbar { width: 0; }
.tablet-statusbar {
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 38px;
  margin: 0 -18px 12px;
  padding: 8px 18px 9px;
  border-radius: 22px 22px 14px 14px;
  background: linear-gradient(180deg, #FFFFFF 0%, #F8FBFF 72%, rgba(248,251,255,.96) 100%);
  border-bottom: 2px solid rgba(37,99,235,.24);
  box-shadow: 0 1px 0 rgba(255,255,255,.95), 0 10px 18px rgba(37,99,235,.08);
  backdrop-filter: blur(16px);
  color: #2563EB;
  font-size: 12px;
  font-weight: 900;
}
.tablet-statusbar::before {
  content: '';
  position: absolute;
  left: 18px;
  right: 18px;
  bottom: -2px;
  height: 2px;
  border-radius: 999px;
  background: linear-gradient(90deg, rgba(37,99,235,.12), rgba(37,99,235,.52), rgba(14,165,233,.28), rgba(37,99,235,.12));
  pointer-events: none;
}
.tablet-statusbar::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -18px;
  height: 18px;
  background: linear-gradient(180deg, rgba(248,251,255,.95), rgba(248,251,255,0));
  pointer-events: none;
}
.tablet-system-icons {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
.tablet-signal {
  display: inline-flex;
  align-items: flex-end;
  gap: 2px;
  height: 12px;
}
.tablet-signal i {
  display: block;
  width: 3px;
  border-radius: 3px;
  background: #2563EB;
}
.tablet-signal i:nth-child(1) { height: 5px; opacity: .45; }
.tablet-signal i:nth-child(2) { height: 8px; opacity: .7; }
.tablet-signal i:nth-child(3) { height: 11px; }
.tablet-wifi {
  width: 14px;
  height: 10px;
  border: 2px solid #2563EB;
  border-left-color: transparent;
  border-right-color: transparent;
  border-bottom: 0;
  border-radius: 12px 12px 0 0;
  position: relative;
}
.tablet-wifi::after {
  content: '';
  position: absolute;
  left: 50%;
  bottom: -3px;
  width: 4px;
  height: 4px;
  transform: translateX(-50%);
  border-radius: 50%;
  background: #2563EB;
}
.tablet-battery {
  position: relative;
  width: 24px;
  height: 12px;
  border: 1.6px solid #2563EB;
  border-radius: 4px;
  padding: 2px;
}
.tablet-battery::after {
  content: '';
  position: absolute;
  right: -4px;
  top: 3px;
  width: 2px;
  height: 5px;
  border-radius: 0 2px 2px 0;
  background: #2563EB;
}
.tablet-battery i {
  display: block;
  height: 100%;
  width: 72%;
  border-radius: 2px;
  background: linear-gradient(90deg, #38BDF8, #2563EB);
}
.tablet-header {
  display: grid;
  grid-template-columns: auto minmax(280px, 1fr) auto;
  align-items: center;
  gap: 18px;
  margin-bottom: 10px;
}
.tablet-title {
  color: #1E293B;
  font-size: 23px;
  font-weight: 900;
  letter-spacing: .03em;
}
.tablet-search {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
  padding: 8px 12px;
  border-radius: 18px;
  background: #F8FBFF;
  border: 1px solid #DBEAFE;
  box-shadow: inset 4px 4px 9px rgba(37,99,235,.08), inset -4px -4px 9px rgba(255,255,255,.95);
}
.tablet-search .el-input { flex: 1; }
.tablet-search :deep(.el-input__wrapper) {
  padding: 0;
  background: transparent;
  box-shadow: none;
}
.tablet-categories {
  display: flex;
  gap: 8px;
  padding: 8px 0 2px;
  overflow-x: auto;
}
.tablet-categories::-webkit-scrollbar { height: 0; }
.major-chip {
  flex: 0 0 auto;
  border: 0;
  border-radius: 999px;
  padding: 8px 14px;
  color: #2563EB;
  background: #EFF6FF;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 4px 4px 10px rgba(37,99,235,.10), -4px -4px 10px rgba(255,255,255,.92);
}
.major-chip.active {
  color: #fff;
  background: linear-gradient(145deg, #38BDF8, #2563EB);
}

/* 新拟态胶囊筛选区：启途浅蓝白软凸起 / 激活蓝色浅凹陷 */
.filter-bar {
  display: grid;
  grid-template-columns: minmax(138px, .58fr) minmax(320px, 1.34fr) minmax(210px, .86fr);
  column-gap: 18px;
  row-gap: 14px;
  align-items: stretch;
  margin: 10px 0 14px;
  padding: 12px;
  border-radius: 22px;
  background: linear-gradient(145deg, #F8FBFF 0%, #EFF6FF 100%);
  border: 1px solid rgba(191,219,254,.72);
  box-shadow:
    inset 1px 1px 0 rgba(255,255,255,.92),
    10px 10px 22px rgba(37,99,235,.08),
    -8px -8px 18px rgba(255,255,255,.92);
}
.filter-line {
  display: flex;
  align-items: flex-start;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
}
.salary-filter-line {
  padding-top: 2px;
}
.filter-label {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: #2563EB;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: .02em;
  white-space: nowrap;
}
.filter-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.filter-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 30px;
  padding: 6px 13px;
  border: 0;
  border-radius: 999px;
  background: #F8FBFF;
  color: #2563EB;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: .01em;
  cursor: pointer;
  user-select: none;
  box-shadow:
    5px 5px 12px rgba(37,99,235,.12),
    -5px -5px 12px rgba(255,255,255,.98),
    inset 1px 1px 0 rgba(255,255,255,.78);
  transition: transform .16s ease, color .16s ease, box-shadow .16s ease, background .16s ease;
}
.filter-tag:hover {
  color: #0EA5E9;
  transform: translateY(-1px);
  box-shadow:
    7px 7px 15px rgba(37,99,235,.14),
    -7px -7px 15px rgba(255,255,255,1),
    inset 1px 1px 0 rgba(255,255,255,.86);
}
.filter-tag.active {
  color: #FFFFFF;
  background: linear-gradient(145deg, #38BDF8 0%, #2563EB 100%);
  box-shadow:
    inset 4px 4px 9px rgba(30,64,175,.25),
    inset -4px -4px 9px rgba(255,255,255,.20),
    3px 3px 8px rgba(37,99,235,.18);
  transform: translateY(0);
}

/* 岗位网格 */
.career-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

/* 岗位卡片 */
.career-card {
  position: relative;
  padding: 12px;
  cursor: pointer;
  transition: all 0.2s;
  border-radius: 20px;
  background: rgba(255,255,255,.86);
}
.career-card:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
}
.career-card.is-bookmarked {
  border-color: var(--accent);
  background: linear-gradient(135deg, var(--accent-bg) 0%, var(--bg-card) 100%);
}
.card-ribbon {
  position: absolute;
  top: -1px;
  left: -1px;
  background: var(--accent);
  color: white;
  font-size: 0.65rem;
  padding: 4px 10px;
  border-radius: 10px 0 8px 0;
  z-index: 1;
}
.card-ribbon i {
  margin-right: 3px;
}
.card-body {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 10px;
}
.card-icon {
  font-size: 1.5rem;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--primary-bg);
  border-radius: 8px;
  flex-shrink: 0;
  margin-top: 2px;
}
.card-title-area {
  flex: 1;
  min-width: 0;
}
.card-title-row {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 2px;
}
.card-name {
  font-size: 0.92rem;
  color: var(--text-heading);
}
.card-path-badge {
  font-size: 0.75rem;
  cursor: help;
  color: var(--primary);
}
.card-intro {
  font-size: 0.78rem;
  color: var(--text-muted);
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.card-actions {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
  margin-left: auto;
}
.card-tag-row {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.card-meta-row { margin-bottom: 8px; }
.card-salary-row {
  align-items: center;
  justify-content: space-between;
  padding-top: 8px;
  border-top: 1px dashed #BFDBFE;
}
.salary-pill {
  font-size: 12px;
  font-weight: 900;
}
.tag-pill.blue { background: #EFF6FF; color: #2563EB; }
.tag-pill.green { background: #ECFDF5; color: #059669; }
.tag-pill.orange { background: #FFF7ED; color: #C2410C; }
.tag-pill.red { background: #FEF2F2; color: #DC2626; }
.tag-pill.gray { background: #F1F5F9; color: #64748B; }

/* ════════════════════════════════════ */
/* 视频推荐模块                        */
/* ════════════════════════════════════ */
.video-recommend-section {
  position: sticky;
  top: 24px;
  margin-top: 0;
  padding: 14px;
  min-height: 0;
  max-height: 72vh;
  overflow-y: auto;
  border-radius: 24px;
  background:
    radial-gradient(circle at 12% 0%, rgba(14,165,233,.12), transparent 30%),
    linear-gradient(180deg, #FFFFFF 0%, #F8FBFF 100%);
  border: 1px solid #DBEAFE;
  box-shadow: 0 16px 34px rgba(37,99,235,.08);
}
.video-recommend-section::-webkit-scrollbar { width: 0; }
.video-panel-head {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  padding-bottom: 10px;
  margin-bottom: 10px;
  border-bottom: 1px dashed #BFDBFE;
}
.section-kicker {
  display: inline-flex;
  margin-bottom: 5px;
  color: #2563EB;
  font-size: 12px;
  font-weight: 900;
  letter-spacing: .12em;
}
.video-panel-head h2 {
  margin: 0;
  color: #1E293B;
  font-size: 20px;
  line-height: 1.2;
  font-weight: 900;
  letter-spacing: .02em;
}
.video-panel-head p {
  max-width: none;
  margin: 4px 0 0;
  color: #64748B;
  font-size: 12px;
  line-height: 1.5;
}
.section-title-badge {
  flex: none;
  font-size: 13px;
  font-weight: 900;
  color: var(--primary);
  background: #EFF6FF;
  padding: 6px 11px;
  border-radius: 999px;
  border: 1px solid #BFDBFE;
}
.video-section-controls {
  display: flex;
  justify-content: flex-end;
  flex-shrink: 0;
  margin-bottom: 10px;
}

/* 视频卡片网格 */
.video-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}
.video-card {
  overflow: hidden;
  display: grid;
  grid-template-columns: 112px minmax(0, 1fr);
  transition: all 0.2s;
  border: 1px solid #DBEAFE;
  border-radius: 16px;
  background: #fff;
}
.video-card:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
}

/* 封面 */
.video-cover {
  position: relative;
  width: 100%;
  height: 86px;
  aspect-ratio: auto;
  overflow: hidden;
  background: var(--primary-bg);
  cursor: pointer;
}
.video-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}
.video-card:hover .video-cover img {
  transform: scale(1.05);
}
.video-duration {
  position: absolute;
  bottom: 6px;
  right: 6px;
  background: rgba(0,0,0,0.7);
  color: white;
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 4px;
}
.video-cover-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s;
}
.video-card:hover .video-cover-overlay {
  opacity: 1;
}
.overlay-play {
  color: white;
  font-size: 0.9rem;
  font-weight: 600;
  background: rgba(0,0,0,0.5);
  padding: 6px 16px;
  border-radius: 20px;
}
.overlay-play i {
  margin-right: 6px;
}

/* 封面占位（没图时） */
.video-cover-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  background: linear-gradient(135deg, var(--primary-bg) 0%, var(--primary-bg) 100%);
}
.placeholder-icon {
  font-size: 2rem;
  margin-bottom: 6px;
  color: var(--primary);
}
.placeholder-title {
  font-size: 0.78rem;
  color: var(--text-muted);
}

/* 视频信息 */
.video-info {
  min-width: 0;
  padding: 8px 10px;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.video-title-row {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  margin-bottom: 3px;
}
.video-title {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-heading);
  line-height: 1.35;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}
.bookmark-video-tag {
  flex-shrink: 0;
  font-size: 0.6rem !important;
}
.bookmark-video-tag i {
  margin-right: 2px;
}
.video-star-btn {
  flex-shrink: 0;
  margin-left: auto;
  width: 22px !important;
  height: 22px !important;
  font-size: 0.66rem !important;
}
.video-meta {
  display: flex;
  align-items: center;
  gap: 7px;
  font-size: 0.66rem;
  color: var(--text-muted);
  margin-bottom: 2px;
}
.video-author {
  color: var(--primary);
}
.video-stats {
  display: flex;
  gap: 6px;
}
.video-description {
  font-size: 0.66rem;
  color: var(--text-muted);
  line-height: 1.3;
  margin: 1px 0 6px;
  flex: 1;
  opacity: 0.7;
}
.video-link-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: linear-gradient(145deg, #38BDF8 0%, #2563EB 100%);
  color: white;
  font-size: 0.68rem;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: 16px;
  text-decoration: none;
  text-align: center;
  transition: all 0.15s;
  align-self: flex-start;
}
.video-link-btn:hover {
  background: linear-gradient(145deg, #0EA5E9 0%, #1D4ED8 100%);
  box-shadow: 0 8px 18px rgba(37,99,235,0.18);
}

/* AI生成职业相关 */
.new-tag {
  margin-left: 4px;
  font-size: 0.6rem !important;
  animation: newTagPulse 2s ease-in-out infinite;
}
@keyframes newTagPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
.ai-gen-card {
  border: 1px dashed var(--accent) !important;
  position: relative;
}
.ai-gen-card::before {
  content: 'AI生成';
  position: absolute;
  top: -1px;
  right: -1px;
  background: var(--accent-gradient);
  color: white;
  font-size: 0.55rem;
  padding: 1px 6px;
  border-radius: 0 8px 0 8px;
  z-index: 2;
}
.ai-searching {
  text-align: center;
  padding: 2rem 0;
}

@media (max-width: 1180px) {
  .explore-workbench {
    grid-template-columns: 1fr;
  }
  .video-recommend-section {
    position: relative;
    top: auto;
    max-height: none;
  }
}

@media (max-width: 760px) {
  .tablet-header {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  .tablet-search {
    order: 3;
  }
  .career-count {
    justify-self: start;
  }
  .filter-bar {
    grid-template-columns: 1fr;
  }
  .career-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .explore-workbench { gap: 18px; }
  .video-panel-head { flex-direction: column; }
  .video-panel-head h2 { font-size: 22px; }
  .video-panel-head p { font-size: 14px; }
  .video-recommend-section { padding: 18px; border-radius: 22px; }
  .video-grid { grid-template-columns: 1fr; }
  .video-card { grid-template-columns: 1fr; }
  .video-cover { height: auto; aspect-ratio: 16/9; }
  .tablet-device { padding: 10px; border-radius: 26px; min-height: 0; }
  .tablet-screen { padding: 0 12px 14px; min-height: 620px; border-radius: 20px; }
  .tablet-statusbar { margin: 0 -12px 12px; padding: 8px 12px 9px; border-radius: 20px 20px 12px 12px; }
  .tablet-title { font-size: 20px; }
  .filter-bar { padding: 12px; border-radius: 22px; }
  .filter-tag { min-height: 34px; padding: 7px 14px; }
  .card-salary-row { align-items: flex-start; flex-direction: column; gap: 8px; }
  .card-actions { margin-left: 0; }
}

</style>