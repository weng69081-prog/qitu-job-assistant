<template>
  <div class="path-page">
    <!-- ═══ 顶部：路线切换 ═══ -->
    <div class="section-header">
      <div class="section-title">
        <i class="fas fa-map-signs"></i>
        <span>成长路线规划</span>
      </div>
      <el-button class="btn-outline" size="small" @click="$router.back()">
        <i class="fas fa-arrow-left"></i> 返回
      </el-button>
    </div>

    <div class="path-top-bar">
      <el-select v-model="selectedRoute" placeholder="选择路线" size="large" style="width:280px" @change="onRouteChange">
        <el-option label="通用基础路线（课内必学）" value="main">
          <span><i class="fas fa-book" style="margin-right:6px;color:var(--primary)"></i>通用基础路线（课内必学）</span>
        </el-option>
        <el-option
          v-if="bookmarkedCareers.length > 0"
          :label="`${bookmarkedCareers.length}个收藏岗位专属分支`"
          value="branch"
        >
          <span><i class="fas fa-star" style="margin-right:6px;color:#e6a23c"></i>{{ bookmarkedCareers.length }}个收藏岗位专属分支</span>
        </el-option>
      </el-select>
      <!-- 整体进度 -->
      <div class="overall-progress" v-if="totalProgress >= 0">
        <span class="progress-label">整体完成度</span>
        <el-progress :percentage="totalProgress" :stroke-width="10" :color="progressColor" style="width:160px" />
      </div>
    </div>

    <p class="path-hint" v-if="selectedRoute === 'branch'">
      <i class="fas fa-star" style="color:#e6a23c;margin-right:4px"></i>
      已在通用路线基础上追加收藏岗位的专属分支任务
    </p>

    <!-- ═══ 主体：学期时间轴 ═══ -->
    <div v-if="loading" class="loading-state">
      <i class="fas fa-spinner fa-pulse" style="margin-right:8px"></i>加载中…
    </div>
    <div v-else class="semester-timeline">
      <div
        v-for="(sem, idx) in routeData"
        :key="sem.phase"
        class="semester-card"
      >
        <!-- 左侧：学期标记 -->
        <div class="sem-marker">
          <div class="sem-dot" :style="{background: semColors[idx % semColors.length]}"></div>
          <div class="sem-line" v-if="idx < routeData.length - 1"></div>
        </div>
        <!-- 右侧：卡片内容 -->
        <div class="sem-content card">
          <div class="sem-header">
            <span class="sem-phase">{{ sem.phase }}</span>
            <span class="sem-goal" v-if="sem.goals">
              <i class="fas fa-bullseye" style="margin-right:4px;color:var(--primary)"></i>{{ sem.goals }}
            </span>
          </div>

          <!-- 单阶段进度条 -->
          <div class="sem-progress">
            <el-progress
              :percentage="phaseProgress[sem.phase] || 0"
              :stroke-width="6"
              :color="semColors[idx % semColors.length]"
              style="width:160px"
            />
          </div>

          <!-- 必修课程清单 -->
          <div class="sem-block" v-if="sem.courses?.length">
            <div class="block-label">
              <i class="fas fa-book" style="margin-right:6px;color:var(--primary)"></i>必修课程
            </div>
            <div class="course-tags">
              <span class="tag-pill blue" v-for="c in sem.courses" :key="c">{{ c }}</span>
            </div>
          </div>

          <!-- 可打卡必做任务（主干） -->
          <div class="sem-block">
            <div class="block-label">
              <i class="fas fa-check-circle" style="margin-right:6px;color:#059669"></i>必做任务
            </div>
            <div class="task-list">
              <div
                v-for="(task, ti) in sem.tasks"
                :key="ti"
                class="task-item"
                @click="toggleTask(sem.phase, 'main', ti)"
              >
                <span class="task-checkbox">
                  <i v-if="getTaskDone(sem.phase, 'main', ti)" class="fas fa-check-circle" style="color:#059669"></i>
                  <i v-else class="far fa-square" style="color:var(--text-muted)"></i>
                </span>
                <span :class="['task-text', {done: getTaskDone(sem.phase, 'main', ti)}]">{{ task }}</span>
              </div>
            </div>
          </div>

          <!-- 岗位专属补充任务（仅分支路线时显示） -->
          <div class="sem-block branch-block" v-if="branchTasks[sem.phase]?.length">
            <div class="block-label">
              <i class="fas fa-star" style="margin-right:6px;color:#e6a23c"></i>收藏岗位专属补充任务
            </div>
            <div class="task-list">
              <div
                v-for="(task, ti) in branchTasks[sem.phase]"
                :key="'b'+ti"
                class="task-item branch-item"
                @click="toggleTask(sem.phase, 'branch', ti)"
              >
                <span class="task-checkbox">
                  <i v-if="getTaskDone(sem.phase, 'branch', ti)" class="fas fa-check-circle" style="color:#059669"></i>
                  <i v-else class="far fa-square" style="color:var(--text-muted)"></i>
                </span>
                <span :class="['task-text', {done: getTaskDone(sem.phase, 'branch', ti)}]">{{ task.text }}</span>
              </div>
            </div>
          </div>

          <!-- 学习建议 -->
          <div class="sem-tips" v-if="sem.tips">
            <i class="fas fa-lightbulb tips-icon" style="color:#e6a23c"></i>
            <span>{{ sem.tips }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCareerStore } from '../stores/career'
import axios from 'axios'

const API = 'http://localhost:8000/api'
const route = useRoute()
const store = useCareerStore()

const selectedRoute = ref('main')
const loading = ref(true)
const mainRoute = ref([])         // 通用主干
const routeData = ref([])         // 当前显示的路线
const allCareers = ref([])        // 当前专业的所有岗位（用于生成分支任务）

// 收藏的岗位
const bookmarkStore = ref(JSON.parse(localStorage.getItem('career_bookmarks') || '[]'))
const bookmarkedCareers = computed(() => bookmarkStore.value)

// 分支任务的文本映射
const branchTaskMap = {
  '前端开发工程师': {
    '大一下': ['学习Vue3或React框架', '完成一个静态页面项目'],
    '大二上': ['深入Vue3/React源码学习', '学习TypeScript', '实现一个SPA应用'],
    '大二下': ['投递前端暑期实习', '学习前端性能优化', '参与开源UI组件库贡献'],
    '大三上': ['深入研究工程化工具（Webpack/Vite）', '刷前端面试题', '完成高复杂度项目'],
    '大三下': ['准备前端校招面试', '完善作品集'],
    '大四': ['了解入职公司前端技术栈', '学习职场协作规范'],
  },
  '后端开发工程师': {
    '大一下': ['学习Python/Java基础', '实现一个REST API'],
    '大二上': ['深入学习数据库设计和SQL', '学习Django/Spring Boot', '完成一个带后端的全栈项目'],
    '大二下': ['投递后端暑期实习', '学习Redis缓存', '了解微服务基础概念'],
    '大三上': ['深入学习高并发系统设计', '刷后端面试题', '学习Kubernetes基础'],
    '大三下': ['准备后端校招面试', '优化项目中的性能问题'],
    '大四': ['了解入职公司技术栈', '学习分布式系统基础'],
  }
}

// 根据收藏岗位生成分支任务
const branchTasks = computed(() => {
  const result = {}
  for (const careerName of bookmarkedCareers.value) {
    const tasks = branchTaskMap[careerName]
    if (!tasks) continue
    for (const [phase, taskList] of Object.entries(tasks)) {
      if (!result[phase]) result[phase] = []
      for (const t of taskList) {
        result[phase].push({ text: `[${careerName}] ${t}`, career: careerName })
      }
    }
  }
  return result
})

// 打卡状态
const doneMap = ref(JSON.parse(localStorage.getItem('path_done_map') || '{}'))

function getTaskKey(phase, type, idx) {
  return `${phase}_${type}_${idx}`
}
function getTaskDone(phase, type, idx) {
  return doneMap.value[getTaskKey(phase, type, idx)] === true
}
function toggleTask(phase, type, idx) {
  const key = getTaskKey(phase, type, idx)
  doneMap.value[key] = !doneMap.value[key]
  localStorage.setItem('path_done_map', JSON.stringify(doneMap.value))
}

// 各阶段进度
const phaseProgress = computed(() => {
  const result = {}
  for (const sem of routeData.value) {
    const mainCount = sem.tasks?.length || 0
    const branchCount = branchTasks.value[sem.phase]?.length || 0
    const total = mainCount + branchCount
    if (total === 0) {
      result[sem.phase] = 0
      continue
    }
    let done = 0
    for (let i = 0; i < mainCount; i++) {
      if (getTaskDone(sem.phase, 'main', i)) done++
    }
    for (let i = 0; i < branchCount; i++) {
      if (getTaskDone(sem.phase, 'branch', i)) done++
    }
    result[sem.phase] = Math.round((done / total) * 100)
  }
  return result
})

// 整体进度
const totalProgress = computed(() => {
  const phases = Object.keys(phaseProgress.value)
  if (phases.length === 0) return 0
  const sum = phases.reduce((a, p) => a + (phaseProgress.value[p] || 0), 0)
  return Math.round(sum / phases.length)
})

function progressColor(pct) {
  if (pct < 30) return '#f56c6c'
  if (pct < 70) return '#e6a23c'
  return '#67c23a'
}

const semColors = ['#3D5A80','#3D5A80','#3D5A80','#3D5A80','#3D5A80','#3D5A80','#3D5A80']

// 切换路线
function onRouteChange() {
  if (selectedRoute.value === 'main') {
    routeData.value = mainRoute.value
  } else {
    routeData.value = mainRoute.value  // 分支只是在主干上加补充任务
  }
}

async function loadData() {
  loading.value = true
  try {
    const majorCat = localStorage.getItem('major_category') || '计算机类'
    const careerId = route.params.careerId
    let growth
    
    if (careerId && typeof careerId === 'string') {
      // 职业专属：调用职业专属成长路线接口
      const careerName = decodeURIComponent(careerId)
      const res = await axios.get(`${API}/career/career-path/${encodeURIComponent(careerName)}`)
      growth = res.data.path || []
    } else {
      // 通用：加载该专业大类的基础路线
      const res = await axios.get(`${API}/career/static-home`, {
        params: { major_category: majorCat }
      })
      growth = res.data.growth_path || []
    }
    
    mainRoute.value = growth
    routeData.value = growth
    allCareers.value = []  // 后续可按需加载
  } catch (e) {
    console.error('加载路线数据失败', e)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadData()
  // 记录已生成路线
  const careerId = route.params.careerId
  if (careerId && typeof careerId === 'string') {
    store.markPathGenerated(decodeURIComponent(careerId))
  }
})
</script>

<style scoped>
.path-page {
  max-width: 800px;
  margin: 0 auto;
}

/* ── 顶部操作栏 ── */
.path-top-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}
.overall-progress {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}
.progress-label {
  font-size: 0.82rem;
  color: var(--text-muted);
  white-space: nowrap;
}

/* ── 分支提示 ── */
.path-hint {
  font-size: 0.85rem;
  color: #d97706;
  background: #fffbeb;
  border: 1px solid #fde68a;
  padding: 10px 16px;
  border-radius: var(--radius-md);
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* ═══ 学期时间轴 ═══ */
.semester-timeline {
  position: relative;
  padding-left: 20px;
}
.semester-card {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

/* ── 左侧时间轴 ── */
.sem-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 24px;
  flex-shrink: 0;
}
.sem-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 22px;
  box-shadow: 0 0 0 3px rgba(255,255,255,0.8), 0 2px 6px rgba(0,0,0,0.1);
}
.sem-line {
  width: 2px;
  flex: 1;
  background: var(--border);
  min-height: 20px;
}

/* ── 右侧内容卡片 ── */
.sem-content {
  flex: 1;
  padding: 20px;
  margin-bottom: 4px;
}
.sem-header {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
.sem-phase {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-heading);
}
.sem-goal {
  font-size: 0.85rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 4px;
}
.sem-progress {
  margin-bottom: 16px;
}

/* ── 板块 ── */
.sem-block {
  margin-bottom: 14px;
}
.block-label {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 8px;
  display: flex;
  align-items: center;
}
.course-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

/* ── 任务列表 ── */
.task-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.task-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 8px;
  cursor: pointer;
  border-radius: var(--radius-sm);
  transition: background 0.15s;
}
.task-item:hover {
  background: var(--bg-hover);
}
.task-checkbox {
  flex-shrink: 0;
  font-size: 1rem;
  display: flex;
  align-items: center;
}
.task-text {
  font-size: 0.88rem;
  color: var(--text-body);
  line-height: 1.4;
}
.task-text.done {
  text-decoration: line-through;
  color: var(--text-light);
}

/* ── 分支专属区块 ── */
.branch-block {
  border-left: 3px solid #e6a23c;
  padding-left: 12px;
  margin-top: 6px;
  background: #fffbeb;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}
.branch-item .task-text {
  color: #b8860b;
}

/* ── 学习建议 ── */
.sem-tips {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  padding: 10px 12px;
  background: var(--primary-bg);
  border: 1px solid #bfdbfe;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  color: var(--text-body);
  margin-top: 12px;
  line-height: 1.5;
}
.tips-icon {
  flex-shrink: 0;
  margin-top: 1px;
  font-size: 0.9rem;
}
</style>