<template>
  <div class="wrong-page">
    <!-- ═══════ 页面标题 ═══════ -->
    <div class="section-header">
      <div class="section-title">
        <i class="fas fa-xmark"></i>
        笔试错题本
        <span class="badge">{{ stats.total }} 题</span>
      </div>
      <button class="btn-outline" style="padding:6px 16px" @click="goBack">
        <i class="fas fa-arrow-left"></i> 返回
      </button>
    </div>

    <!-- ═══════ 统计概览 ═══════ -->
    <div class="grid-3" style="margin-bottom:20px">
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-list"></i></div>
        <div class="stat-num">{{ stats.total }}</div>
        <div class="stat-label">总错题数</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-clock"></i></div>
        <div class="stat-num" style="color:#d97706">{{ stats.unmastered }}</div>
        <div class="stat-label">未掌握</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon"><i class="fas fa-check-circle"></i></div>
        <div class="stat-num" style="color:#059669">{{ stats.mastered }}</div>
        <div class="stat-label">已掌握</div>
      </div>
    </div>

    <!-- ═══════ 筛选区 ═══════ -->
    <div class="filter-bar" style="background:var(--bg-card);padding:14px 16px;border-radius:var(--radius-md);border:1px solid var(--border);margin-bottom:20px">
      <div style="display:flex;flex-wrap:wrap;gap:10px;width:100%">
        <div class="filter-group" style="flex:2;min-width:200px">
          <span class="filter-label"><i class="fas fa-briefcase"></i> 岗位</span>
          <el-select
            v-model="filterCareer"
            placeholder="全部岗位"
            clearable
            filterable
            style="width:100%"
            @change="onFilterChange">
            <el-option-group v-if="store.validBookmarks.length" label="⭐ 已收藏">
              <el-option
                v-for="b in store.validBookmarks"
                :key="b.career"
                :label="b.career"
                :value="b.career" />
            </el-option-group>
            <el-option-group
              v-for="group in careerGroups"
              :key="group.label"
              :label="group.label">
              <el-option
                v-for="c in group.list"
                :key="c"
                :label="c"
                :value="c" />
            </el-option-group>
          </el-select>
        </div>
        <div class="filter-group" style="flex:1.5;min-width:160px">
          <span class="filter-label"><i class="fas fa-tag"></i> 考点</span>
          <el-select
            v-model="filterCategory"
            placeholder="全部考点"
            clearable
            filterable
            allow-create
            style="width:100%"
            @change="onFilterChange">
            <el-option
              v-for="kp in knowledgePoints"
              :key="kp"
              :label="kp"
              :value="kp" />
          </el-select>
        </div>
        <div class="filter-group" style="flex:1;min-width:120px">
          <span class="filter-label"><i class="fas fa-signal"></i> 难度</span>
          <el-select
            v-model="filterDifficulty"
            placeholder="全部难度"
            clearable
            style="width:100%"
            @change="onFilterChange">
            <el-option label="简单" value="easy" />
            <el-option label="中等" value="medium" />
            <el-option label="困难" value="hard" />
          </el-select>
        </div>
        <div class="filter-group" style="flex:1;min-width:120px">
          <span class="filter-label"><i class="fas fa-flag"></i> 状态</span>
          <el-select
            v-model="filterStatus"
            placeholder="全部状态"
            clearable
            style="width:100%"
            @change="onFilterChange">
            <el-option label="未掌握" value="unmastered" />
            <el-option label="已掌握" value="mastered" />
          </el-select>
        </div>
      </div>
    </div>

    <!-- ═══════ 加载中 ═══════ -->
    <div v-if="loading" class="loading-state">
      <i class="fas fa-spinner fa-pulse" style="margin-right:8px"></i>加载中…
    </div>

    <!-- ═══════ 空状态 ═══════ -->
    <div v-else-if="items.length === 0" class="empty-state">
      <span class="empty-icon"><i class="fas fa-check-double"></i></span>
      <p>暂无错题，继续保持！</p>
      <p class="empty-hint">再接再厉，全对通关</p>
      <button class="btn-outline" style="margin-top:14px;padding:6px 20px" @click="goBack">
        <i class="fas fa-arrow-left"></i> 返回笔试练习
      </button>
    </div>

    <!-- ═══════ 错题卡片列表 ═══════ -->
    <div v-else class="wrong-list">
      <div v-for="item in items" :key="item.id" class="wrong-card card">
        <!-- 标签行 -->
        <div class="wc-badges">
          <span class="tag-pill blue">
            <i class="fas fa-tag"></i> {{ typeLabel(item.question_type) }}
          </span>
          <span v-if="item.knowledge_point" class="tag-pill gray">
            <i class="fas fa-bookmark"></i> {{ item.knowledge_point }}
          </span>
          <span class="tag-pill" :class="diffPill(item.difficulty)">
            <i class="fas" :class="diffIcon(item.difficulty)"></i>
            {{ difficultyLabel(item.difficulty) }}
          </span>
          <span class="tag-pill" :class="item.mastered ? 'green' : 'orange'">
            <i class="fas" :class="item.mastered ? 'fa-check-circle' : 'fa-clock'"></i>
            {{ item.mastered ? '已掌握' : '未掌握' }}
          </span>
        </div>

        <!-- 题目文本 -->
        <div class="wc-question">{{ item.question }}</div>

        <!-- 答案区 -->
        <div class="answer-section">
          <div class="answer-row">
            <i class="fas fa-check-circle" style="color:#059669;font-size:13px"></i>
            <span class="answer-label">正确答案：</span>
            <span class="answer-value correct">{{ item.correct_answer }}</span>
          </div>
          <div class="answer-row">
            <i class="fas fa-times-circle" style="color:#dc2626;font-size:13px"></i>
            <span class="answer-label">我的答案：</span>
            <span class="answer-value wrong">{{ item.user_answer }}</span>
          </div>
        </div>

        <!-- 解析折叠面板 -->
        <el-collapse class="analysis-collapse">
          <el-collapse-item name="analysis">
            <template #title>
              <i class="fas fa-book-open" style="margin-right:6px;color:var(--primary)"></i>
              <span style="font-size:13px;color:var(--primary);font-weight:500">查看解析</span>
            </template>
            <div class="analysis-content">{{ item.analysis || '暂无解析' }}</div>
          </el-collapse-item>
        </el-collapse>

        <!-- 操作按钮 -->
        <div class="wc-actions">
          <button
            class="btn-outline"
            style="padding:5px 14px;font-size:12px"
            :class="{ 'is-mastered': item.mastered }"
            :disabled="item.mastered"
            @click="markMastered(item)">
            <i class="fas" :class="item.mastered ? 'fa-check-circle' : 'fa-check'"></i>
            {{ item.mastered ? '已掌握' : '标记已掌握' }}
          </button>
          <button class="btn-primary" style="padding:5px 14px;font-size:12px" @click="openReanswer(item)">
            <i class="fas fa-rotate-right"></i> 重做此题
          </button>
          <button class="btn-outline" style="padding:5px 14px;font-size:12px;border-color:#fecaca;color:#dc2626" @click="confirmRemove(item)">
            <i class="fas fa-trash-can"></i> 移除记录
          </button>
        </div>
      </div>
    </div>

    <!-- ═══════ 分页 ═══════ -->
    <div v-if="total > pageSize" class="pagination-wrap">
      <el-pagination
        layout="prev, pager, next"
        :total="total"
        :page-size="pageSize"
        :current-page="currentPage"
        @current-change="onPageChange"
        background />
    </div>

    <!-- ═══════ 重做弹窗 ═══════ -->
    <el-dialog v-model="reanswerVisible" title="🔄 重做错题" width="550px" destroy-on-close>
      <div v-if="reanswerItem" class="reanswer-content">
        <p class="reanswer-q"><b>{{ reanswerItem.question }}</b></p>

        <!-- 有选项的题目 -->
        <div v-if="reanswerOptions.length > 0" class="reanswer-options">
          <div
            v-for="(opt, oi) in reanswerOptions"
            :key="oi"
            class="reanswer-opt"
            :class="reanswerOptionClass(opt.key)"
            @click="submitReanswer(opt.key)">
            <span class="opt-key">{{ opt.key }}.</span>
            <span class="opt-text">{{ opt.value }}</span>
          </div>
        </div>

        <!-- 判断题 -->
        <div v-else class="judge-wrap">
          <div class="judge-options">
            <div
              class="judge-item"
              :class="reanswerJudgeClass('对')"
              @click="submitReanswer('对')">
              <i class="fas fa-check-circle" style="margin-right:4px"></i> 对
            </div>
            <div
              class="judge-item"
              :class="reanswerJudgeClass('错')"
              @click="submitReanswer('错')">
              <i class="fas fa-times-circle" style="margin-right:4px"></i> 错
            </div>
          </div>
        </div>

        <!-- 反馈 -->
        <div v-if="reanswerResult !== null" class="reanswer-feedback">
          <el-alert
            :title="reanswerResult ? '✅ 回答正确！' : '❌ 回答错误'"
            :type="reanswerResult ? 'success' : 'error'"
            :closable="false"
            show-icon />
          <div v-if="!reanswerResult && reanswerCorrect" class="feedback-correct">
            <i class="fas fa-check-circle" style="margin-right:4px"></i>
            正确答案：<b>{{ reanswerCorrect }}</b>
          </div>
          <div v-if="reanswerAnalysis" class="analysis-box">
            <h4><i class="fas fa-book-open"></i> 解析</h4>
            <p>{{ reanswerAnalysis }}</p>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import { useCareerStore } from '../stores/career'

const store = useCareerStore()
const router = useRouter()

// ═══════════════════════════════════════════════
// 岗位数据
// ═══════════════════════════════════════════════
const careerGroups = [
  {
    label: '计算机类',
    list: [
      '前端开发工程师', '后端开发工程师', '全栈开发工程师',
      '数据分析师', '软件测试工程师', '网络安全工程师',
      '运维工程师', 'AI算法工程师', '产品经理',
    ],
  },
  {
    label: '机电土木类',
    list: [
      '机械工程师', '电气工程师', '土木工程师', '建筑设计师',
      '自动化工程师', '结构工程师',
    ],
  },
  {
    label: '金融财会类',
    list: [
      '金融分析师', '会计师', '审计师', '税务专员',
      '风险管理师', '投资顾问',
    ],
  },
  {
    label: '市场运营类',
    list: [
      '市场营销', '新媒体运营', '品牌策划', '广告投放',
      '电商运营', '内容运营',
    ],
  },
  {
    label: '管理咨询类',
    list: [
      '管理咨询师', '人力资源', '行政管理', '项目经理',
      '战略分析师',
    ],
  },
  {
    label: '设计类',
    list: [
      'UI/UX设计师', '平面设计师', '工业设计师', '交互设计师',
      '视觉设计师',
    ],
  },
  {
    label: '其他',
    list: ['公务员', '教师', '医生', '律师', '科研人员'],
  },
]

// ═══════════════════════════════════════════════
// 固定考点列表
// ═══════════════════════════════════════════════
const knowledgePoints = [
  '言语理解', '判断推理', '数量关系', '资料分析', '常识判断',
  '数据结构', '算法', '计算机网络', '操作系统', '数据库',
  '编程语言', '软件工程', '设计模式', '系统设计',
  '机器学习', '深度学习', '自然语言处理', '计算机视觉',
  '产品设计', '用户研究', '数据分析', '项目管理',
]

// ═══════════════════════════════════════════════
// 状态
// ═══════════════════════════════════════════════
const loading = ref(false)
const items = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = 20

const filterCareer = ref('')
const filterCategory = ref('')
const filterDifficulty = ref('')
const filterStatus = ref('')

const stats = reactive({ total: 0, unmastered: 0, mastered: 0 })

// 重做弹窗
const reanswerVisible = ref(false)
const reanswerItem = ref(null)
const reanswerSelected = ref('')
const reanswerResult = ref(null)
const reanswerCorrect = ref('')
const reanswerAnalysis = ref('')

// ═══════════════════════════════════════════════
// 计算属性
// ═══════════════════════════════════════════════
const reanswerOptions = computed(() => {
  if (!reanswerItem.value) return []
  return parseOptions(reanswerItem.value.options_json || reanswerItem.value.options || [])
})

// ═══════════════════════════════════════════════
// 工具函数
// ═══════════════════════════════════════════════
function typeLabel(type) {
  const map = { single_choice: '单选题', multi_choice: '多选题', judge: '判断题' }
  return map[type] || type || '未知'
}

function diffPill(d) {
  const map = { easy: 'green', 简单: 'green', medium: 'orange', 中等: 'orange', hard: 'red', 困难: 'red' }
  return map[d] || 'blue'
}

function diffIcon(d) {
  const map = { easy: 'fa-chevron-up', 简单: 'fa-chevron-up', medium: 'fa-equals', 中等: 'fa-equals', hard: 'fa-chevron-down', 困难: 'fa-chevron-down' }
  return map[d] || 'fa-circle'
}

function difficultyLabel(d) {
  const map = { easy: '简单', medium: '中等', hard: '困难' }
  return map[d] || d || '未知'
}

function parseOptions(json) {
  try {
    const p = typeof json === 'string' ? JSON.parse(json) : json
    if (Array.isArray(p)) return p
    if (p && typeof p === 'object') {
      return Object.entries(p).map(([k, v]) => ({ key: k, value: v }))
    }
    return []
  } catch {
    return []
  }
}

function reanswerOptionClass(key) {
  if (reanswerResult.value === null) {
    return { sel: reanswerSelected.value === key }
  }
  return {
    cor: key === reanswerCorrect.value,
    wrg: reanswerSelected.value === key && key !== reanswerCorrect.value,
  }
}

function reanswerJudgeClass(val) {
  if (reanswerResult.value === null) {
    return { sel: reanswerSelected.value === val }
  }
  return {
    cor: reanswerResult.value && val === reanswerCorrect.value,
    wrg: reanswerResult.value === false && reanswerSelected.value === val,
  }
}

// ═══════════════════════════════════════════════
// API 调用
// ═══════════════════════════════════════════════
async function loadData(page = 1) {
  loading.value = true
  currentPage.value = page
  try {
    const params = { page, page_size: pageSize }
    if (filterCareer.value) params.career = filterCareer.value
    if (filterCategory.value) params.category = filterCategory.value
    if (filterDifficulty.value) params.difficulty = filterDifficulty.value
    if (filterStatus.value) params.status = filterStatus.value

    const { data } = await axios.get('/api/exam/wrong-questions', { params })
    items.value = data.items || []
    total.value = data.total || data.count || 0
  } catch (e) {
    console.error('加载错题失败', e)
    ElMessage.error('加载错题失败')
    items.value = []
    total.value = 0
  }
  loading.value = false
}

async function loadStats() {
  try {
    const params = { page: 1, page_size: 1 }
    if (filterCareer.value) params.career = filterCareer.value
    const { data } = await axios.get('/api/exam/wrong-questions', { params })
    stats.total = data.total || data.count || 0
    stats.unmastered = data.unmastered || data.unmastered_count || 0
    stats.mastered = data.mastered || 0
  } catch {
    // ignore
  }
}

async function markMastered(item) {
  try {
    await axios.put(`/api/exam/wrong-questions/${item.id}/master`)
    ElMessage.success('✅ 已标记为掌握')
    item.mastered = true
    loadStats()
  } catch {
    ElMessage.error('操作失败，请重试')
  }
}

async function confirmRemove(item) {
  try {
    await ElMessageBox.confirm('确定要移除该错题记录吗？', '确认删除', {
      type: 'warning',
      confirmButtonText: '删除',
      cancelButtonText: '取消',
    })
    await axios.delete(`/api/exam/wrong-questions/${item.id}`)
    ElMessage.success('已删除')
    loadData(currentPage.value)
    loadStats()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

function openReanswer(item) {
  reanswerItem.value = item
  reanswerSelected.value = ''
  reanswerResult.value = null
  reanswerCorrect.value = ''
  reanswerAnalysis.value = ''
  reanswerVisible.value = true
}

async function submitReanswer(selected) {
  if (reanswerResult.value !== null) return
  reanswerSelected.value = selected
  try {
    const { data } = await axios.post(`/api/exam/wrong-questions/${reanswerItem.value.id}/reanswer`, {
      user_answer: selected,
    })
    reanswerResult.value = data.correct
    reanswerCorrect.value = data.correct_answer || ''
    reanswerAnalysis.value = data.analysis || ''
    if (data.correct) {
      ElMessage.success('✅ 回答正确！')
      // 刷新列表
      loadData(currentPage.value)
      loadStats()
    } else {
      ElMessage.warning('❌ 回答错误')
    }
  } catch {
    ElMessage.error('提交失败，请重试')
  }
}

// ═══════════════════════════════════════════════
// 交互事件
// ═══════════════════════════════════════════════
function onFilterChange() {
  currentPage.value = 1
  loadData(1)
  loadStats()
}

function onPageChange(page) {
  loadData(page)
}

function goBack() {
  router.push('/exam-practice')
}

// ═══════════════════════════════════════════════
// 生命周期
// ═══════════════════════════════════════════════
onMounted(() => {
  loadData()
  loadStats()
})
</script>

<style scoped>
/* ═══════════════════════════════════════════════
   页面容器
   ═══════════════════════════════════════════════ */
.wrong-page {
  max-width: 860px;
  margin: 0 auto;
}

/* ═══════════════════════════════════════════════
   错题卡片列表
   ═══════════════════════════════════════════════ */
.wrong-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.wrong-card {
  padding: 18px 20px;
  transition: all 0.25s;
}
.wrong-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

/* ── 标签行 ── */
.wc-badges {
  display: flex;
  gap: 6px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}

/* ── 题目文本 ── */
.wc-question {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-heading);
  line-height: 1.7;
  margin-bottom: 12px;
  white-space: pre-wrap;
}

/* ── 答案区 ── */
.answer-section {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 12px;
  padding: 10px 14px;
  background: var(--bg-alt);
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-light);
}
.answer-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
}
.answer-label {
  color: var(--text-muted);
  font-weight: 500;
  flex-shrink: 0;
}
.answer-value {
  font-weight: 600;
}
.answer-value.correct {
  color: #059669;
}
.answer-value.wrong {
  color: #dc2626;
}

/* ── 解析折叠 ── */
.analysis-collapse {
  margin-bottom: 12px;
}
.analysis-collapse :deep(.el-collapse-item__header) {
  padding-left: 2px;
  height: auto;
  line-height: 1.4;
  padding-bottom: 2px;
}
.analysis-collapse :deep(.el-collapse-item__wrap) {
  border-bottom: none;
}
.analysis-content {
  font-size: 13px;
  line-height: 1.7;
  color: var(--text-body);
  white-space: pre-wrap;
  padding: 6px 0 2px;
}

/* ── 操作按钮 ── */
.wc-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  padding-top: 10px;
  border-top: 1px solid var(--border-light);
}
.wc-actions .btn-outline.is-mastered,
.wc-actions .btn-outline:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ═══════════════════════════════════════════════
   分页
   ═══════════════════════════════════════════════ */
.pagination-wrap {
  display: flex;
  justify-content: center;
  padding: 24px 0 12px;
}

/* ═══════════════════════════════════════════════
   重做弹窗内容
   ═══════════════════════════════════════════════ */
.reanswer-content {
  padding: 4px 0;
}
.reanswer-q {
  font-size: 14px;
  margin-bottom: 16px;
  line-height: 1.7;
  color: var(--text-heading);
}
.reanswer-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.reanswer-opt {
  padding: 10px 14px;
  border: 2px solid var(--border);
  border-radius: var(--radius-md);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
  font-size: 14px;
  color: var(--text-body);
}
.reanswer-opt:hover {
  border-color: var(--primary);
  background: var(--primary-bg);
}
.reanswer-opt.sel {
  border-color: var(--primary);
  background: var(--primary-bg);
}
.reanswer-opt.cor {
  border-color: #a7f3d0;
  background: #ecfdf5;
}
.reanswer-opt.wrg {
  border-color: #fecaca;
  background: #fef2f2;
}
.opt-key {
  font-weight: 700;
  color: var(--text-heading);
  min-width: 24px;
}
.opt-text {
  flex: 1;
}
.judge-wrap {
  margin-top: 8px;
}
.judge-options {
  display: flex;
  gap: 20px;
  justify-content: center;
}
.judge-item {
  padding: 14px 36px;
  border: 2px solid var(--border);
  border-radius: var(--radius-md);
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.2s;
  min-width: 120px;
  text-align: center;
  color: var(--text-body);
}
.judge-item:hover {
  border-color: var(--primary);
  background: var(--primary-bg);
}
.judge-item.sel {
  border-color: var(--primary);
  background: var(--primary-bg);
}
.judge-item.cor {
  border-color: #a7f3d0;
  background: #ecfdf5;
}
.judge-item.wrg {
  border-color: #fecaca;
  background: #fef2f2;
}
.reanswer-feedback {
  margin-top: 16px;
}
.feedback-correct {
  margin-top: 10px;
  font-size: 14px;
  color: #059669;
  display: flex;
  align-items: center;
}
.analysis-box {
  background: var(--bg-alt);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-light);
  padding: 14px 16px;
  margin-top: 12px;
}
.analysis-box h4 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: var(--primary);
  display: flex;
  align-items: center;
  gap: 6px;
}
.analysis-box p {
  font-size: 13px;
  color: var(--text-body);
  line-height: 1.7;
  margin: 0;
}

/* ═══════════════════════════════════════════════
   响应式
   ═══════════════════════════════════════════════ */
@media (max-width: 640px) {
  .wrong-page {
    padding: 0;
  }
  .filter-bar .filter-group {
    min-width: 100% !important;
    flex: auto !important;
  }
  .wrong-card {
    padding: 14px 14px;
  }
  .wc-actions {
    flex-direction: column;
  }
  .wc-actions .btn-outline,
  .wc-actions .btn-primary {
    width: 100%;
    justify-content: center;
  }
  .judge-options {
    flex-direction: column;
    gap: 12px;
  }
  .judge-item {
    padding: 12px 20px;
  }
}
</style>