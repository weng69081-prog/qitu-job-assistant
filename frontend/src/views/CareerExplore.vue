<template>
  <div class="career-list-page">
    <!-- ═══ 页面顶部 Banner ═══ -->
    <div class="banner-wrap">
      <PageBanner fullwidth
        title="职业探索"
        description="探索适合你的职业方向，了解岗位要求与发展路径"
        icon="fa-compass"
        variant="primary"
      />
      <img src="/src/assets/new-explore-cat.png" class="banner-cat" alt="小橘探路">
    </div>
    <!-- ═══ 顶部：专业选择 + 全局搜索 ═══ -->
    <div class="list-top-bar">
      <div class="top-left">
        <el-select v-model="selectedCategory" placeholder="选择专业大类" size="large" style="width:200px" @change="onCategoryChange">
          <el-option v-for="c in majorCategories" :key="c" :label="c" :value="c" />
        </el-select>
        <span class="career-count"><i class="fas fa-briefcase"></i> 共 <b>{{ filteredCareers.length }}</b> 个岗位</span>
      </div>
      <div class="search-input-wrap">
        <i class="fas fa-search search-input-icon"></i>
        <el-input
          v-model="searchQuery"
          placeholder="搜索岗位名称或关键词…"
          clearable
          size="large"
        />
      </div>
    </div>

    <!-- ═══ 筛选区：标签式多选 ═══ -->
    <div class="filter-bar">
      <div class="filter-group">
        <span class="filter-label"><i class="fas fa-signal"></i> 入门难度</span>
        <div class="filter-tags">
          <span
            v-for="d in difficultyOptions" :key="d"
            class="filter-tag"
            :class="{ active: selectedDifficulties.includes(d) }"
            @click="toggleDifficulty(d)"
          >{{ d }}</span>
        </div>
      </div>
      <div class="filter-group">
        <span class="filter-label"><i class="fas fa-briefcase"></i> 工作类型</span>
        <div class="filter-tags">
          <span
            v-for="t in workTypeOptions" :key="t"
            class="filter-tag"
            :class="{ active: selectedWorkTypes.includes(t) }"
            @click="toggleWorkType(t)"
          >{{ t }}</span>
        </div>
      </div>
      <div class="filter-group">
        <span class="filter-label"><i class="fas fa-coins"></i> 薪资标签</span>
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

    <!-- ═══ 已收藏岗位专区 ═══ -->
    <div v-if="store.validBookmarks.length > 0" class="bookmark-band">
      <div class="bm-band-header">
        <span class="bm-band-title"><i class="fas fa-star"></i> 已收藏岗位 <b>({{ store.validBookmarks.length }})</b></span>
        <el-button text size="small" @click="$router.push('/settings')">管理收藏 <i class="fas fa-arrow-right"></i></el-button>
      </div>
      <div class="bm-band-scroll">
        <div
          v-for="b in store.validBookmarks"
          :key="b.career"
          class="bm-band-card"
          @click="goDetail(b.career)"
        >
          <div class="bm-band-top">
            <span class="bm-band-name">{{ b.career }}</span>
            <span class="bm-band-badge" v-if="store.hasGeneratedPath(b.career)" title="已生成成长路线"><i class="fas fa-map"></i></span>
          </div>
          <div class="bm-band-meta">{{ b.difficulty }} · {{ b.salary }}</div>
        </div>
      </div>
    </div>

    <!-- ═══ 主体：网格布局岗位卡片 ═══ -->
    <div v-if="loading" class="loading-state"><i class="fas fa-spinner fa-spin"></i> 加载中…</div>
    <div v-else-if="aiSearchLoading" class="empty-state">
      <div class="ai-searching">
        <span class="empty-icon"><i class="fas fa-robot"></i></span>
        <p style="font-size:1.2rem;margin-bottom:0.5rem">正在为你补充该职业信息，请稍候…</p>
        <p class="empty-hint">AI正在生成 <b>{{ searchQuery }}</b> 的详细资料</p>
        <el-progress :percentage="80" :stroke-width="4" style="max-width:300px;margin:1rem auto" />
      </div>
    </div>
    <div v-else-if="filteredCareers.length === 0 && !searchQuery" class="empty-state">
      <span class="empty-icon"><i class="fas fa-search-minus"></i></span>
      <p>没有找到匹配的岗位</p>
      <p class="empty-hint">试试调整筛选条件或选择其他专业</p>
    </div>
    <div v-else-if="aiSearchError" class="empty-state">
      <span class="empty-icon"><i class="fas fa-exclamation-triangle"></i></span>
      <p>搜索出错：{{ aiSearchError }}</p>
      <p class="empty-hint">请重试或换一个关键词</p>
    </div>
    <div v-else-if="filteredCareers.length === 0 && searchQuery" class="empty-state">
      <span class="empty-icon"><i class="fas fa-search"></i></span>
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
        <div class="card-ribbon" v-if="store.isBookmarked(c.career)"><i class="fas fa-star"></i> 已收藏</div>
        <div class="card-body">
          <div class="card-icon">{{ getIcon(c.career) }}</div>
          <div class="card-title-area">
            <div class="card-title-row">
              <strong class="card-name">{{ c.career }}</strong>
              <span class="card-path-badge" v-if="store.hasGeneratedPath(c.career)" title="已生成成长路线"><i class="fas fa-map"></i></span>
              <el-tag v-if="c.ai_generated" size="small" type="danger" class="new-tag">新</el-tag>
            </div>
            <span class="card-intro">{{ c.short_intro || '' }}</span>
          </div>
          <div class="card-actions">
            <el-button
              size="small"
              :type="store.isBookmarked(c.career) ? 'warning' : 'default'"
              circle
              @click.stop="toggleBookmark(c)"
              :title="store.isBookmarked(c.career) ? '取消收藏' : '收藏岗位'"
            ><i :class="store.isBookmarked(c.career) ? 'fas fa-star' : 'far fa-star'"></i></el-button>
            <el-button
              size="small"
              type="primary"
              circle
              plain
              @click.stop="scrollToVideos(c.career)"
              title="入门学习视频"
            ><i class="fas fa-tv"></i></el-button>
          </div>
        </div>
        <div class="card-tags">
          <span class="tag-pill" :class="difficultyType(c.difficulty) === 'success' ? 'green' : difficultyType(c.difficulty) === 'warning' ? 'orange' : difficultyType(c.difficulty) === 'danger' ? 'red' : 'gray'"><i class="fas fa-signal"></i> {{ c.difficulty }}</span>
          <span class="tag-pill blue"><i class="fas fa-coins"></i> {{ c.salary_tag || c.salary }}</span>
          <span class="tag-pill green"><i class="fas fa-briefcase"></i> {{ c.work_type || '技术类' }}</span>
          <span v-if="c.keywords" v-for="kw in (c.keywords || []).slice(0,2)" :key="kw" class="tag-pill gray"><i class="fas fa-tag"></i> {{ kw }}</span>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════════════ -->
    <!-- 📺 职业入门学习视频推荐模块          -->
    <!-- ═══════════════════════════════════ -->
    <div class="card video-recommend-section" ref="videoSection">
      <div class="section-header">
        <div class="section-title">
          <i class="fas fa-tv"></i>
          <span>职业入门学习视频推荐</span>
          <span v-if="selectedVideoCareer" class="section-title-badge">{{ selectedVideoCareer }}</span>
        </div>
        <div class="video-section-controls">
          <el-radio-group v-model="videoSort" size="small" @change="loadVideos(selectedVideoCareer)">
            <el-radio-button value="hot"><i class="fas fa-fire"></i> 热门</el-radio-button>
            <el-radio-button value="new"><i class="fas fa-star"></i> 最新</el-radio-button>
          </el-radio-group>
        </div>
      </div>

      <!-- 视频卡片加载状态 -->
      <div v-if="videoLoading" class="loading-state"><i class="fas fa-spinner fa-spin"></i> 正在搜索B站视频…</div>

      <!-- 视频卡片网格 -->
      <div v-else-if="videoList.length > 0" class="video-grid">
        <div
          v-for="(v, idx) in videoList"
          :key="v.bvid || idx"
          class="card video-card"
        >
          <!-- 封面图 -->
          <div class="video-cover" v-if="v.pic">
            <img :src="v.pic" :alt="v.title" @error="onCoverError($event, v)" />
            <span class="video-duration" v-if="v.duration">{{ v.duration }}</span>
            <div class="video-cover-overlay">
              <span class="overlay-play"><i class="fas fa-play"></i> 去B站学习</span>
            </div>
          </div>
          <div class="video-cover video-cover-placeholder" v-else @click="openVideo(v)">
            <span class="placeholder-icon"><i class="fas fa-film"></i></span>
            <span class="placeholder-title">{{ v.title?.slice(0, 12) || '入门视频' }}</span>
          </div>

          <!-- 相关信息 -->
          <div class="video-info">
            <div class="video-title-row">
              <span class="video-title" :title="cleanTitle(v.title)">{{ cleanTitle(v.title) }}</span>
              <el-tag v-if="store.isBookmarked(selectedVideoCareer)" size="small" type="warning" class="bookmark-video-tag"><i class="fas fa-star"></i> 收藏岗位专属</el-tag>
              <el-button
                size="small"
                circle
                :type="store.isVideoBookmarked(v.bvid) ? 'warning' : 'default'"
                @click.stop="toggleVideoBookmark(v)"
                class="video-star-btn"
                :title="store.isVideoBookmarked(v.bvid) ? '取消收藏视频' : '收藏视频'"
              ><i :class="store.isVideoBookmarked(v.bvid) ? 'fas fa-star' : 'far fa-star'"></i></el-button>
            </div>
            <div class="video-meta">
              <span class="video-author" v-if="v.author"><i class="fas fa-user"></i> {{ v.author }}</span>
              <span class="video-stats" v-if="v.play">
                <span><i class="fas fa-play"></i> {{ formatCount(v.play) }}</span>
                <span v-if="v.danmaku"> <i class="fas fa-comment"></i> {{ formatCount(v.danmaku) }}</span>
              </span>
            </div>
            <p class="video-description" v-if="v.description">{{ v.description?.slice(0, 60) }}{{ v.description?.length > 60 ? '…' : '' }}</p>
            <a
              :href="v.url"
              target="_blank"
              rel="noopener noreferrer"
              class="video-link-btn"
              @click.stop="onVideoClick(v)"
            >
              去B站学习 <i class="fas fa-arrow-right"></i>
            </a>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="empty-state" style="padding:30px 0">
        <span class="empty-icon"><i class="fas fa-video"></i></span>
        <p>暂无推荐视频</p>
        <p class="empty-hint">先选择一个岗位查看推荐</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useCareerStore } from '../stores/career'
import axios from 'axios'
import PageBanner from '../components/PageBanner.vue'

const API = 'http://localhost:8000/api'
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
function onCategoryChange() {
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
.list-top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  flex-wrap: wrap;
  gap: 12px;
}
.top-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.career-count {
  font-size: 0.82rem;
  color: var(--text-muted);
}
.career-count i {
  margin-right: 4px;
}
.search-input-wrap {
  position: relative;
  width: 320px;
}
.search-input-wrap .el-input {
  width: 100%;
}
.search-input-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
  font-size: 14px;
  z-index: 1;
  pointer-events: none;
}
.search-input-wrap .el-input :deep(.el-input__wrapper) {
  padding-left: 36px;
}

/* 岗位网格 */
.career-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 14px;
}

/* 岗位卡片 */
.career-card {
  position: relative;
  padding: 16px;
  cursor: pointer;
  transition: all 0.2s;
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
  margin-bottom: 12px;
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
  margin-left: 4px;
}
.card-tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

/* ════════════════════════════════════ */
/* 视频推荐模块                        */
/* ════════════════════════════════════ */
.video-recommend-section {
  margin-top: 28px;
  padding: 20px 16px;
}
.section-title-badge {
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--primary);
  background: var(--primary-bg);
  padding: 2px 10px;
  border-radius: 12px;
}
.video-section-controls {
  flex-shrink: 0;
}

/* 视频卡片网格 */
.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 14px;
}
.video-card {
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: all 0.2s;
  border: 1px solid var(--border);
}
.video-card:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
}

/* 封面 */
.video-cover {
  position: relative;
  width: 100%;
  aspect-ratio: 16/9;
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
  padding: 10px 12px 12px;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.video-title-row {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  margin-bottom: 4px;
}
.video-title {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-heading);
  line-height: 1.4;
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
  width: 24px !important;
  height: 24px !important;
  font-size: 0.7rem !important;
}
.video-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.72rem;
  color: var(--text-muted);
  margin-bottom: 4px;
}
.video-author {
  color: var(--primary);
}
.video-stats {
  display: flex;
  gap: 6px;
}
.video-description {
  font-size: 0.72rem;
  color: var(--text-muted);
  line-height: 1.4;
  margin: 2px 0 8px;
  flex: 1;
  opacity: 0.7;
}
.video-link-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--accent);
  color: white;
  font-size: 0.75rem;
  font-weight: 500;
  padding: 5px 12px;
  border-radius: 16px;
  text-decoration: none;
  text-align: center;
  transition: all 0.15s;
  align-self: flex-start;
}
.video-link-btn:hover {
  background: #B54E1A;
  box-shadow: 0 2px 8px rgba(200, 90, 32, 0.3);
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

@media (max-width: 640px) {
  .career-grid { grid-template-columns: 1fr; }
  .list-top-bar { flex-direction: column; align-items: stretch; }
  .search-input-wrap { width: 100%; }
  .video-grid { grid-template-columns: 1fr; }
  .video-section-header { flex-direction: column; align-items: flex-start; }
}

/* ═══ 职业探索猫：趴banner底边（同首页风格） ═══ */
.banner-wrap {
  position: relative;
}
.banner-cat {
  position: absolute;
  bottom: 0px;
  right: 320px;
  width: 60px;
  height: auto;
  pointer-events: none;
  z-index: 0;
  filter: drop-shadow(0 2px 8px rgba(0,0,0,0.18));
  transition: transform 0.3s ease;
}
.banner-cat:hover {
  transform: scale(1.08) rotate(-3deg);
}
</style>