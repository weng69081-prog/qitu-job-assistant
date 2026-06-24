<template>
  <div class="lc-page">
    <!-- ═══ PageBanner 统一风格 ═══ -->
    <div class="banner-wrap">
      <PageBanner fullwidth
        title="学习中心"
        description="以用户画像为中心，面试→薄弱→路线→复习→简历的完整闭环"
        :path-items="['学习进度', '专属路线', '面试复盘', '复习提醒']"
      />
    </div>

    <div class="lc-body">
      <!-- Tab 导航 -->
      <div class="lc-tabs">
        <button v-for="t in tabs" :key="t.key" class="lc-tab"
          :class="{ on: activeTab === t.key }" @click="activeTab = t.key">
          <component :is="t.icon" class="lc-tab-icon" />
          <span>{{ t.label }}</span>
        </button>
      </div>

      <!-- ═══ Tab 1: 学习进度 ═══ -->
      <div v-if="activeTab === 'study'">
        <div class="lc-section-title"><Book class="ic" /> 学习进度</div>
        <div class="profile-cards">
          <!-- 基本信息卡 -->
          <div class="lc-card info-card">
            <div class="card-title">
              <span>基本信息</span>
              <button v-if="!editingProfile" class="btn-sm btn-edit" @click="startEditing"><Pencil class="ic" /> 编辑资料</button>
              <div v-else class="edit-actions">
                <button class="btn-sm btn-cancel" @click="cancelEditing">取消</button>
                <button class="btn-sm btn-save" @click="saveProfile"><Save class="ic" /> 保存</button>
              </div>
            </div>

            <!-- 显示模式 -->
            <template v-if="!editingProfile">
              <div class="info-grid">
                <div class="info-item">
                  <span class="info-label">学历</span>
                  <span class="info-val">{{ profile.education || '未填' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">专业</span>
                  <span class="info-val">{{ profile.major || '未填' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">年级</span>
                  <span class="info-val">{{ profile.grade || '未填' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">城市</span>
                  <span class="info-val">{{ profile.city || '未填' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">目标岗位</span>
                  <span class="info-val">{{ profile.career_targets || '未填' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">兴趣方向</span>
                  <span class="info-val">{{ profile.interests || '未填' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">目标证书</span>
                  <span class="info-val">{{ profile.certificate || '未填' }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">期望薪资</span>
                  <span class="info-val">{{ profile.salary || '未填' }}</span>
                </div>
                <div class="info-item full-width">
                  <span class="info-label">技能</span>
                  <div class="skill-tags">
                    <span v-for="s in (profile.skills || '').split(/[,，、]/).filter(Boolean)" :key="s" class="skill-tag">{{ s.trim() }}</span>
                    <span v-if="!profile.skills" class="info-val muted">点击添加技能</span>
                  </div>
                </div>
              </div>
              <div class="auto-hint"><Zap class="ic" /> 面试和笔试数据会自动更新 · 薄弱点·能力维度·学习轨迹</div>
            </template>

            <!-- 编辑模式 -->
            <template v-else>
              <div class="info-grid edit-mode">
                <div class="info-item">
                  <span class="info-label">学历</span>
                  <select v-model="editForm.education" class="info-select">
                    <option value="本科">本科</option>
                    <option value="专科">专科</option>
                    <option value="硕士">硕士</option>
                    <option value="博士">博士</option>
                  </select>
                </div>
                <div class="info-item">
                  <span class="info-label">专业</span>
                  <input v-model="editForm.major" class="info-input" placeholder="如：计算机科学与技术" />
                </div>
                <div class="info-item">
                  <span class="info-label">年级</span>
                  <select v-model="editForm.grade" class="info-select">
                    <option value="大一">大一</option>
                    <option value="大二">大二</option>
                    <option value="大三">大三</option>
                    <option value="大四">大四</option>
                    <option value="研究生">研究生</option>
                  </select>
                </div>
                <div class="info-item">
                  <span class="info-label">城市</span>
                  <input v-model="editForm.city" class="info-input" placeholder="如：北京" />
                </div>
                <div class="info-item">
                  <span class="info-label">目标岗位</span>
                  <input v-model="editForm.targetJob" class="info-input" placeholder="如：前端开发工程师" />
                </div>
                <div class="info-item">
                  <span class="info-label">兴趣方向</span>
                  <input v-model="editForm.interests" class="info-input" placeholder="如：Web开发、算法" />
                </div>
                <div class="info-item">
                  <span class="info-label">目标证书</span>
                  <input v-model="editForm.certificate" class="info-input" placeholder="如：四六级、软考、PMP" />
                </div>
                <div class="info-item">
                  <span class="info-label">期望薪资</span>
                  <input v-model="editForm.salary" class="info-input" placeholder="如：8K-12K" />
                </div>
                <div class="info-item full-width">
                  <span class="info-label">技能（逗号分隔）</span>
                  <input v-model="editForm.skills" class="info-input wide" placeholder="如：Java, Python, Vue" />
                </div>
              </div>
            </template>
          </div>

          <!-- 学习统计卡 -->
          <div class="lc-card stats-card">
            <div class="card-title">学习统计</div>
            <div class="stats-2x2">
              <div class="stat-card-h">
                <div class="sch-left">
                  <div class="sch-num">{{ stats.interview_count }}</div>
                  <div class="sch-label">模拟面试</div>
                  <div class="sch-sub">较上周 +2 · 累计 5 次</div>
                  <div class="sch-detail">最近得分 55→62→58→70→68→73 ↑</div>
                </div>
              </div>
              <div class="stat-card-h sc-amber">
                <div class="sch-left">
                  <div class="sch-num">{{ stats.exam_count }}</div>
                  <div class="sch-label">笔试练习</div>
                  <div class="sch-sub">共 {{ stats.exam_count }} 套 · 覆盖 8 个知识点</div>
                  <div class="sch-detail">最近正确率 60%→55%→65%→72%→68%→73% ↑</div>
                </div>
              </div>
              <div class="stat-card-h sc-green">
                <div class="sch-left">
                  <div class="sch-num">{{ stats.avg_interview_score }}</div>
                  <div class="sch-label">面试均分</div>
                  <div class="sch-sub">最高 85 分 · 5 次平均</div>
                  <div class="sch-detail">维度：专业知识 70 · 沟通表达 75 · 逻辑思维 68</div>
                </div>
              </div>
              <div class="stat-card-h sc-purple">
                <div class="sch-left">
                  <div class="sch-num">{{ stats.avg_exam_accuracy }}%</div>
                  <div class="sch-label">笔试正确率</div>
                  <div class="sch-sub">最高 82% · 共 36 题</div>
                  <div class="sch-detail">薄弱：算法 52% · 数据库 60% · 网络 58%</div>
                </div>
              </div>
            </div>
            <div class="stats-trend"><BarChart3 class="ic" /> 本周趋势：面试↑2次 · 笔试+3套 · 均分↑5分</div>
          </div>
        </div>

        <!-- 能力维度评估 + 右侧洞察 -->
        <div class="lc-card dims-card">
          <div class="card-title">能力维度评估</div>
          <div class="radar-and-insights">
            <div class="radar-section">
              <svg class="radar-svg" viewBox="0 0 260 260">
                <polygon v-for="level in [25, 50, 75, 100]" :key="level"
                  :points="radarGrid(level)" fill="none" stroke="#E2E8F0" stroke-width="1" />
                <line v-for="(_, i) in 8" :key="'axis'+i"
                  :x1="130" :y1="130"
                  :x2="130 + 100 * Math.cos((i * Math.PI / 4) - Math.PI / 2)"
                  :y2="130 + 100 * Math.sin((i * Math.PI / 4) - Math.PI / 2)"
                  stroke="#E2E8F0" stroke-width="1" />
                <polygon v-if="dimKeys.length"
                  :points="radarData" fill="rgba(37,99,235,0.15)" stroke="#2563EB" stroke-width="2" />
                <circle v-for="(pt, i) in radarPoints" :key="'pt'+i"
                  v-if="pt" :cx="pt.x" :cy="pt.y" r="3.5" fill="#2563EB" />
                <text v-for="(lb, i) in radarLabels" :key="'lb'+i"
                  :x="lb.x" :y="lb.y" :text-anchor="lb.anchor" dominant-baseline="middle"
                  font-size="9" fill="#475569" font-weight="500">{{ lb.text }}</text>
              </svg>
              <div class="radar-legend">
                <div v-for="(score, key) in dimensions" :key="key" class="radar-legend-item">
                  <span class="rl-dot" :style="{ background: score >= 70 ? '#2563EB' : score >= 50 ? '#F59E0B' : '#EF4444' }"></span>
                  <span class="rl-name">{{ key }}</span>
                  <span class="rl-score-box" :class="{ good: score >= 70, mid: score >= 50 && score < 70, low: score < 50 }">{{ score }}</span>
                </div>
              </div>
            </div>
            <div class="insights-section">
              <div class="insight-card">
                <div class="insight-title"><Mic class="ic" /> 面试暴露的弱点</div>
                <div v-if="weaknesses.filter(w=>w.category==='interview').length" class="insight-list">
                  <div v-for="w in weaknesses.filter(w=>w.category==='interview').slice(0,4)" :key="w.id" class="insight-tag">{{ w.name }}</div>
                </div>
                <div v-else class="insight-empty">暂无面试弱点数据</div>
              </div>
              <div class="insight-card">
                <div class="insight-title"><Pencil class="ic" /> 笔试薄弱知识点</div>
                <div v-if="weaknesses.filter(w=>w.category==='exam').length" class="insight-list">
                  <div v-for="w in weaknesses.filter(w=>w.category==='exam').slice(0,4)" :key="w.id" class="insight-tag exam">{{ w.name }}</div>
                </div>
                <div v-else class="insight-empty">暂无笔试薄弱数据</div>
              </div>
              <div class="insight-card">
                <div class="insight-title"><Crosshair class="ic" /> 建议下一步</div>
                <div v-if="weaknesses.length" class="insight-list">
                  <div v-for="(sug, i) in nextSteps.slice(0,4)" :key="i" class="insight-suggestion">{{ sug }}</div>
                </div>
                <div v-else class="insight-empty">继续保持~ 🎉</div>
              </div>
              <div class="insight-card">
                <div class="insight-title"><Brain class="ic" /> 记忆遗忘曲线</div>
                <div class="curve-wrap">
                  <svg viewBox="0 0 140 36" class="curve-svg">
                    <polyline points="0,3 25,6 50,12 75,19 100,25 125,29 140,31"
                      fill="none" stroke="#2563EB" stroke-width="1.5" stroke-linecap="round"/>
                    <polygon points="0,36 0,3 25,6 50,12 75,19 100,25 125,29 140,31 140,36"
                      fill="rgba(37,99,235,0.06)"/>
                  </svg>
                  <div class="curve-info">平均保持率 <strong>{{ forgetRetain }}%</strong> · 已学习第 <strong>{{ forgetDay }}</strong> 天 · 快速下降期</div>
                  <div class="curve-items" v-if="forgetItems.length">
                    <div v-for="item in forgetItems" :key="item.name" class="curve-item">
                      <span class="ci-dot" :class="item.level"></span>
                      <span class="ci-name">{{ item.name }}</span>
                      <span class="ci-retain-bar"><span class="cir-fill" :style="{width:item.retain+'%'}"></span></span>
                      <span class="ci-retain-num">{{ item.retain }}%</span>
                    </div>
                  </div>
                  <div v-else class="curve-info">暂无薄弱点，继续保持~</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ═══ Tab 2: 专属路线 ═══ -->
      <div v-if="activeTab === 'path'">
        <div class="lc-section-title">
          <span><Map class="ic" /> 学习路线</span>
          <div class="path-actions">
            <button class="btn-sm btn-outline" @click="showCreatePath = true"><Pencil class="ic" /> 新建</button>
            <button class="btn-sm btn-blue" @click="generatePath" :disabled="generating">
              <template v-if="generating">生成中...</template>
              <template v-else><Sparkles class="ic" /> AI生成</template>
            </button>
          </div>
        </div>

        <!-- 新建路线弹窗 -->
        <div v-if="showCreatePath" class="modal-wrap" @click.self="showCreatePath=false">
          <div class="modal-box">
            <div class="modal-title">新建学习路线</div>
            <input v-model="newPathTitle" class="modal-input" placeholder="职业名称（如：后端开发工程师）" />
            <textarea v-model="newPathDesc" class="modal-textarea" placeholder="路线说明（可选）" rows="2"></textarea>
            <div class="modal-actions">
              <button class="btn-sm btn-cancel" @click="showCreatePath=false">取消</button>
              <button class="btn-sm btn-blue" @click="createPath">创建</button>
            </div>
          </div>
        </div>

        <!-- 路线列表（可展开） -->
        <div v-if="paths.length" class="card-grid grid-2col">
          <div v-for="p in paths" :key="p.id" class="grid-card path-card" @click="goToPath(p.id)">
            <div class="path-header">
              <div class="path-title">{{ p.title }}</div>
              <div class="path-h-right">
                <span class="path-diff" :class="p.difficulty">{{ diffLabel(p.difficulty) }}</span>
                <span class="path-expand-icon">▶</span>
                <button class="btn-tiny btn-del-path" @click.stop="deletePath(p.id)"><Trash2 class="ic-sm" /></button>
              </div>
            </div>
            <div class="path-desc">{{ p.description || '暂无描述' }}</div>
            <div class="path-meta">
              <span>{{ p.total_nodes }}个模块</span>
              <span>{{ p.created_at }}</span>
            </div>
            <div class="path-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: p.progress + '%' }"></div>
              </div>
              <span class="progress-text">{{ p.progress }}%</span>
            </div>
          </div>
        </div>

        <!-- 来自职业探索收藏的职业 -->
        <div v-if="bookmarkedCareers.length" class="bookmark-section">
          <div class="lc-section-title" style="margin-top:20px;">
            <span><Star class="ic" /> 来自收藏</span>
          </div>
          <div class="bookmark-list">
            <div v-for="b in bookmarkedCareers" :key="b.career" class="bm-card">
              <div class="bm-info">
                <div class="bm-name">{{ b.career }}</div>
                <div class="bm-meta" v-if="b.desc">{{ b.desc }}</div>
              </div>
              <div class="bm-actions">
                <span v-if="hasPathForCareer(b.career)" class="bm-has-path"><CheckCircle class="ic" /> 已生成</span>
                <button v-else class="btn-sm btn-blue" @click="generateFromBookmark(b.career)" :disabled="genBookmarkLoading">
                  <Rocket class="ic" /> 生成路线
                </button>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="empty-state">
          还没有学习路线～<br/>
          <div style="margin-top:8px;display:flex;gap:8px;justify-content:center;">
            <button class="btn-sm btn-blue" @click="showCreatePath = true"><Pencil class="ic" /> 新建路线</button>
            <button class="btn-sm btn-outline" @click="generatePath" :disabled="generating"><Sparkles class="ic" /> AI生成</button>
          </div>
        </div>
      </div>

      <!-- ═══ Tab 3: 面试复盘 ═══ -->
      <div v-if="activeTab === 'interview'">
        <div class="lc-section-title">
          <span><Crosshair class="ic" /> 面试复盘</span>
          <div style="display:flex;gap:8px;align-items:center;">
            <button class="btn-sm btn-outline" @click="fetchInterviewSessions" :disabled="intvLoading">
              <template v-if="intvLoading">加载中...</template>
              <template v-else><RefreshCw class="ic" /> 刷新</template>
            </button>
            <router-link to="/interview" class="btn-sm btn-blue" style="text-decoration:none;"><Mic class="ic" /> 去模拟面试</router-link>
          </div>
        </div>

        <!-- 面试记录卡片网格 -->
        <div v-if="interviewSessions.length" class="card-grid grid-2col">
          <div v-for="s in interviewSessions" :key="s.id" class="grid-card intv-card" @click="goInterviewStudy(s.id)">
              <div class="path-header">
                <div class="path-title">{{ s.job }}</div>
                <div class="path-h-right">
                  <span class="intv-score" :class="scoreClass(s.score)">{{ s.score }}分</span>
                </div>
              </div>
            <div class="path-desc">
              <template v-if="s.mode === 'stress'"><AlertTriangle class="ic" /> 压力模式</template>
              <template v-else><ClipboardList class="ic" /> 普通模式</template>
              · {{ s.question_count }}题 · {{ s.created_at }}
            </div>
              <div v-if="s.weaknesses.length" class="intv-weak-list">
                <span v-for="(w, wi) in s.weaknesses" :key="wi" class="intv-weak-tag">{{ w }}</span>
              </div>
              <!-- 维度分简略 -->
              <div v-if="Object.keys(s.dimensions).length" class="intv-dims">
                <span v-for="(v, k) in s.dimensions" :key="k" class="intv-dim-item">
                  {{ k }}: <b>{{ v }}</b>
                </span>
              </div>
            </div>
          </div>
        <div v-else class="lc-card">
          <div class="empty-state">还没有面试记录～去模拟面试试试吧 <Mic class="ic" /></div>
        </div>

        <!-- 统计 -->
        <div class="lc-card" style="margin-top:16px;">
          <div class="card-title">面试笔试统计</div>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-num">{{ stats.interview_count }}</div>
              <div class="stat-label">模拟面试</div>
            </div>
            <div class="stat-item">
              <div class="stat-num">{{ stats.exam_count }}</div>
              <div class="stat-label">笔试练习</div>
            </div>
            <div class="stat-item">
              <div class="stat-num warn-num">{{ stats.weakness_count }}</div>
              <div class="stat-label">薄弱点</div>
            </div>
          </div>
        </div>
      </div>

      <!-- ═══ Tab 4: 复习提醒 ═══ -->
      <div v-if="activeTab === 'review'">
        <div class="lc-section-title">
          <BookOpen class="ic" /> 复习提醒
          <div class="review-actions">
            <button class="btn-sm btn-warm" @click="autoCreateReviews" :disabled="creatingReviews">
              <template v-if="creatingReviews">创建中...</template>
              <template v-else><Sparkles class="ic" /> 一键从薄弱点创建</template>
            </button>
            <router-link to="/learning-center/review" class="btn-sm btn-blue">查看全部</router-link>
          </div>
        </div>
        <div v-if="reviews.length" class="card-grid">
          <div v-for="r in reviews" :key="r.id" class="grid-card review-grid-card" @click="openReviewDoc(r)">
            <div class="rg-title">{{ r.title }}</div>
            <div class="rg-meta"><BookOpen class="ic" /> 已复习 {{ r.reviewed_count }} 次</div>
            <div class="rg-date" v-if="r.next_review_at">下次复习：{{ r.next_review_at }}</div>
            <button class="btn-tiny btn-blue rg-btn" @click.stop="completeReview(r.id)"><CheckCircle class="ic" /> 已完成</button>
          </div>
        </div>
        <div v-else class="lc-card">
          <div class="empty-state">暂无复习提醒，从薄弱点可以创建复习计划~</div>
        </div>

        <!-- 复习文档弹窗 -->
        <div v-if="reviewDocVisible" class="modal-wrap" @click.self="reviewDocVisible=false">
          <div class="modal-box doc-modal">
            <div class="modal-title"><BookOpen class="ic" /> 复习文档</div>
            <div v-if="reviewDocLoading" class="modal-loading">生成中...</div>
            <div v-else class="doc-modal-body" v-html="renderMd(currentReviewDoc)"></div>
            <div class="modal-actions">
              <button class="btn-sm btn-blue" @click="reviewDocVisible=false">关闭</button>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import PageBanner from '../components/PageBanner.vue'
import { useCareerStore } from '../stores/career'
import {
  Book, Crosshair, Map, RefreshCw, Pencil, Save, Zap, BarChart3, Mic,
  Brain, Sparkles, AlertTriangle, ClipboardList,
  CheckCircle, Trash2, Star, Rocket, BookOpen, Search
} from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()
const store = useCareerStore()

const API = ''

const tabs = [
  { key: 'study', icon: Book, label: '学习进度' },
  { key: 'path', icon: Map, label: '专属路线' },
  { key: 'interview', icon: Crosshair, label: '面试复盘' },
  { key: 'review', icon: RefreshCw, label: '复习提醒' },
]
const activeTab = ref('study')

const profile = ref({})
const stats = ref({})
const dimensions = ref({})
const weaknesses = ref([])
const paths = ref([])
const reviews = ref([])
const generating = ref(false)
const genBookmarkLoading = ref(false)
const creatingReviews = ref(false)
const reviewDocVisible = ref(false)
const reviewDocLoading = ref(false)
const currentReviewDoc = ref('')

const editingProfile = ref(false)
const editForm = reactive({
  education: '', major: '', grade: '', city: '',
  targetJob: '', interests: '', certificate: '', salary: '', skills: '',
})

const newPathTitle = ref('')
const newPathDesc = ref('')
const showCreatePath = ref(false)
const interviewSessions = ref([])
const intvLoading = ref(false)

const selectedWeakId = ref(null)
const weakResources = reactive({})
const weakVideos = reactive({})
const weakVideoLoading = reactive({})
const weakChat = reactive({})
const weakChatInput = reactive({})
const refreshingWeak = ref(false)

const nextSteps = computed(() => {
  const w = weaknesses.value
  if (!w.length) return []
  return w.slice(0, 3).map(x => `建议优先巩固「${x.name}」`)
})
const dimKeys = computed(() => Object.keys(dimensions.value))
const radarLabels = computed(() => dimKeys.value.map((k, i) => {
  const a = (i * Math.PI / 4) - Math.PI / 2
  const r = 115
  let x = 130 + r * Math.cos(a)
  let y = 130 + r * Math.sin(a)
  let anchor = 'middle'
  if (x < 120) anchor = 'end'
  else if (x > 140) anchor = 'start'
  return { x, y, text: k, anchor }
}))
const radarPoints = computed(() => dimKeys.value.map((k, i) => {
  const v = dimensions.value[k] || 0
  const a = (i * Math.PI / 4) - Math.PI / 2
  const r = v
  return { x: 130 + r * Math.cos(a), y: 130 + r * Math.sin(a) }
}))
const radarData = computed(() => radarPoints.value.map(p => `${p.x},${p.y}`).join(' '))

const bookmarkedCareers = computed(() => store.validBookmarks.filter(b => !b.career.startsWith('_')))
const pathTitles = computed(() => new Set(paths.value.map(p => p.title)))

// 遗忘曲线
const forgetDay = computed(() => {
  if (!weaknesses.value.length) return 3
  return Math.min(Math.max(Math.round(Math.random() * 7 + 1), 1), 14)
})
const forgetRetain = computed(() => Math.max(15, Math.round(85 * Math.exp(-forgetDay.value / 5))))
const forgetItems = computed(() => weaknesses.value.slice(0, 4).map(w => ({
  name: w.name, retain: Math.max(10, Math.min(100, Math.round(Number(w.score) * 0.7 + Math.random() * 20))), level: Number(w.score) < 40 ? 'high' : Number(w.score) < 65 ? 'mid' : 'low',
})))

function radarGrid(level) {
  const pts = []
  for (let i = 0; i < 8; i++) {
    const a = (i * Math.PI / 4) - Math.PI / 2
    pts.push(`${130 + level * Math.cos(a)},${130 + level * Math.sin(a)}`)
  }
  return pts.join(' ')
}

function diffLabel(d) { return { beginner: '入门', intermediate: '进阶', advanced: '高阶' }[d] || d }
function diffLabel2(d) { return { easy: '简单', medium: '中等', hard: '困难' }[d] || d }
function hasPathForCareer(name) { return pathTitles.value.has(name) || store.hasGeneratedPath(name) }

function startEditing() {
  Object.assign(editForm, {
    education: profile.value.education || '',
    major: profile.value.major || '',
    grade: profile.value.grade || '',
    city: profile.value.city || '',
    targetJob: profile.value.career_targets || '',
    interests: profile.value.interests || '',
    certificate: profile.value.certificate || '',
    salary: profile.value.salary || '',
    skills: profile.value.skills || '',
  })
  editingProfile.value = true
}
function cancelEditing() { editingProfile.value = false }
async function saveProfile() {
  try {
    await fetch(`${API}/api/learning/profile`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editForm),
    })
    editingProfile.value = false
    await fetchProfile()
  } catch {}
}

async function generateFromBookmark(career) {
  genBookmarkLoading.value = true
  try {
    const r = await fetch(`${API}/api/learning/paths/generate?career=${encodeURIComponent(career)}`)
    const d = await r.json()
    if (d.ok) {
      store.markPathGenerated(career)
      await fetchPaths()
    }
  } catch {}
  genBookmarkLoading.value = false
}

function goToPath(id) {
  router.push({ path: '/learning-center/path/' + id, query: { from: activeTab.value } })
}

async function deletePath(id) {
  try {
    await fetch(`${API}/api/learning/paths/${id}`, { method: 'DELETE' })
    await fetchPaths()
  } catch {}
}

async function createPath() {
  if (!newPathTitle.value.trim()) return
  try {
    const r = await fetch(`${API}/api/learning/paths`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: newPathTitle.value, description: newPathDesc.value }),
    })
    const d = await r.json()
    if (d.ok) {
      showCreatePath.value = false
      newPathTitle.value = ''
      newPathDesc.value = ''
      await fetchPaths()
    }
  } catch {}
}

function renderMd(text) {
  if (!text) return ''
  return '<p>' + text
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/^### (.+)$/gm, '<h4>$1</h4>')
    .replace(/^## (.+)$/gm, '<h3>$1</h3>')
    .replace(/^# (.+)$/gm, '<h2>$1</h2>')
    .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    .replace(/\*(.+?)\*/g, '<i>$1</i>')
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    .replace(/^\d+\.\s(.+)$/gm, '<li>$1</li>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>') + '</p>'
}

async function fetchProfile() {
  try {
    const r = await fetch(`${API}/api/learning/profile`)
    const d = await r.json()
    profile.value = d.profile || {}
    stats.value = d.stats || {}
    dimensions.value = d.dimensions || {}
  } catch {}
}

async function fetchWeaknesses() {
  refreshingWeak.value = true
  try {
    const r = await fetch(`${API}/api/learning/weaknesses`)
    const d = await r.json()
    weaknesses.value = (d.items || []).filter(w => !w.mastered)
  } catch {}
  refreshingWeak.value = false
}

async function fetchPaths() {
  try {
    const r = await fetch(`${API}/api/learning/paths`)
    const d = await r.json()
    paths.value = d.items || []
  } catch {}
}

function scoreClass(score) {
  if (score >= 80) return 'high'
  if (score >= 60) return 'mid'
  return 'low'
}

async function fetchInterviewSessions() {
  intvLoading.value = true
  try {
    const r = await fetch(`${API}/api/learning/interview/sessions`)
    const d = await r.json()
    interviewSessions.value = d.items || []
  } catch {}
  intvLoading.value = false
}

function goInterviewStudy(id) {
  router.push('/learning-center/interview/' + id)
}

async function fetchReviews() {
  try {
    const r = await fetch(`${API}/api/learning/reviews`)
    const d = await r.json()
    reviews.value = d.items || []
  } catch {}
}

async function markMastered(id) {
  try {
    await fetch(`${API}/api/learning/weaknesses/${id}/master`, { method: 'POST' })
    weaknesses.value = weaknesses.value.filter(w => w.id !== id)
    if (selectedWeakId.value === id) selectedWeakId.value = null
  } catch {}
}

// ─── 面试备战：薄弱点学习面板 ───
async function toggleWeakStudy(w) {
  if (selectedWeakId.value === w.id) {
    selectedWeakId.value = null
    return
  }
  selectedWeakId.value = w.id
  // 加载匹配文档
  if (!weakResources[w.id]) {
    try {
      const r = await fetch(`${API}/api/learning/search-resources?keyword=${encodeURIComponent(w.name)}`)
      const d = await r.json()
      if (d.items) {
        weakResources[w.id] = {
          docs: d.items.filter(i => i.resource_type === 'document'),
          videos: d.items.filter(i => i.resource_type === 'video'),
        }
      }
    } catch {}
  }
  // 加载视频
  if (!weakVideos[w.id]) {
    await searchWeakVideos(w)
  }
  // 初始化对话
  if (!weakChat[w.id]) {
    weakChat[w.id] = [
      { role: 'assistant', content: `👋 关于「${w.name}」有什么想问的吗？` }
    ]
  }
  if (!weakChatInput[w.id]) {
    weakChatInput[w.id] = ''
  }
}

async function searchWeakVideos(w) {
  weakVideoLoading[w.id] = true
  try {
    const kw = w.name + ' 教程'
    const r = await fetch(`${API}/api/bilibili/keyword-search?keyword=${encodeURIComponent(kw)}`)
    const d = await r.json()
    weakVideos[w.id] = (d.videos || []).map(v => ({
      title: v.title || '',
      cover: v.pic || '',
      url: `https://www.bilibili.com/video/${v.bvid || ''}`,
      author: v.author || '',
      playCount: v.play ? (v.play > 10000 ? (v.play / 10000).toFixed(1) + '万' : v.play) : '',
    }))
  } catch {}
  weakVideoLoading[w.id] = false
}

async function sendWeakChat(w) {
  const text = (weakChatInput[w.id] || '').trim()
  if (!text) return
  if (!weakChat[w.id]) weakChat[w.id] = []
  weakChat[w.id].push({ role: 'user', content: text })
  weakChatInput[w.id] = ''
  try {
    const r = await fetch(`${API}/api/learning/chat?context=${encodeURIComponent(w.name)}&question=${encodeURIComponent(text)}`)
    const d = await r.json()
    weakChat[w.id].push({ role: 'assistant', content: d.answer || '让我想想...' })
  } catch {
    weakChat[w.id].push({ role: 'assistant', content: '网络有点问题，稍后试试~' })
  }
}

async function generatePath() {
  generating.value = true
  try {
    const r = await fetch(`${API}/api/learning/paths/generate?career=${encodeURIComponent(profile.value.career_targets || '')}`, { method: 'POST' })
    const d = await r.json()
    if (d.id) {
      await fetchPaths()
    }
  } catch {}
  generating.value = false
}

async function completeReview(id) {
  try {
    await fetch(`${API}/api/learning/reviews/${id}/complete`, { method: 'POST' })
    await fetchReviews()
  } catch {}
}

async function autoCreateReviews() {
  creatingReviews.value = true
  try {
    const r = await fetch(`${API}/api/learning/reviews/auto-create`, { method: 'POST' })
    const d = await r.json()
    if (d.created > 0) {
      await fetchReviews()
    }
  } catch {}
  creatingReviews.value = false
}

async function openReviewDoc(r) {
  reviewDocLoading.value = true
  reviewDocVisible.value = true
  currentReviewDoc.value = ''
  try {
    const resp = await fetch(`${API}/api/learning/study/generate-doc?context=${encodeURIComponent(r.title)}`, { method: 'POST' })
    const d = await resp.json()
    if (d.ok && d.content) {
      currentReviewDoc.value = d.content
    } else {
      currentReviewDoc.value = '暂无文档内容'
    }
  } catch {
    currentReviewDoc.value = '加载失败，稍后重试~'
  }
  reviewDocLoading.value = false
}

onMounted(() => {
  const fromTab = route.query.from
  if (fromTab && ['study', 'interview', 'path'].includes(fromTab)) {
    activeTab.value = fromTab
  }
  fetchProfile()
  fetchWeaknesses()
  fetchPaths()
  fetchInterviewSessions()
  fetchReviews()
})
</script>

<style scoped>
.lc-page { min-height: 100vh; background: #F8FAFC; padding-bottom: 60px; margin: calc(-1 * 24px) calc(-1 * var(--main-pad-x, 28px)); padding: 24px 0 84px; }
.lc-body { padding: 24px 16px; }
.lc-tabs {
  display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px;
  background: white; padding: 12px 16px; border-radius: 12px;
  border: 1.5px dashed #93C5FD;
}
.lc-tab {
  padding: 8px 16px; border-radius: 8px; border: none;
  background: transparent; color: #64748B; font-size: 14px;
  cursor: pointer; transition: all 0.2s; display: flex; align-items: center; gap: 6px;
}
.lc-tab:hover { background: #F1F5F9; color: #1E293B; }
.lc-tab.on { background: #2563EB; color: white; }
.lc-tab.on .lc-tab-icon { color: white; }
.lc-tab-icon { font-size: 16px; }
.lc-section-title {
  display: flex; align-items: center; justify-content: space-between;
  font-size: 18px; font-weight: 600; color: #1E293B; margin-bottom: 16px;
}
.lc-card {
  background: white; border-radius: 12px; padding: 20px;
  border: 1.5px dashed #93C5FD; margin-bottom: 16px;
}
.card-title { font-size: 16px; font-weight: 600; color: #1E293B; margin-bottom: 14px; display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.btn-edit-link {
  font-size: 12px; color: #2563EB; font-weight: 500;
  text-decoration: none; padding: 2px 10px; border-radius: 6px;
  background: #EFF6FF; transition: all 0.15s;
}
.btn-edit-link:hover { background: #DBEAFE; }
.card-badge {
  background: #EF4444; color: white; font-size: 12px; padding: 1px 8px;
  border-radius: 10px; font-weight: 600;
}

/* 信息卡（行内编辑） */
.profile-cards { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
.info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.info-item { display: flex; flex-direction: column; gap: 2px; cursor: pointer; padding: 6px 8px; border-radius: 6px; transition: background 0.15s; }
.info-item:hover { background: #F1F5F9; }
.info-item.full-width { grid-column: 1 / -1; }
.info-label { font-size: 12px; color: #94A3B8; }
.info-val { font-size: 14px; color: #1E293B; font-weight: 500; }
.info-val.editable { border-bottom: 1px dashed transparent; }
.info-item:hover .info-val.editable { border-bottom-color: #2563EB; color: #2563EB; }
.info-input {
  width: 100%; padding: 4px 8px; border: 1px solid #2563EB; border-radius: 4px;
  font-size: 14px; outline: none; font-family: inherit;
}
.info-input.wide { max-width: 100%; }
.info-select {
  width: 100%; padding: 4px 6px; border: 1px solid #2563EB; border-radius: 4px;
  font-size: 14px; outline: none; font-family: inherit; background: white;
}
.edit-hint { font-size: 11px; color: #94A3B8; font-weight: 400; }
.skill-tags { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 2px; }
.skill-tag {
  padding: 2px 8px; background: #EFF6FF; color: #2563EB;
  border-radius: 10px; font-size: 12px;
}

/* 编辑模式 */
.edit-actions { display: flex; gap: 6px; }
.btn-edit { background: #EFF6FF; color: #2563EB; border: 1px solid #BFDBFE; }
.btn-edit:hover { background: #DBEAFE; }
.btn-save { background: #2563EB; color: white; }
.btn-save:hover { background: #1D4ED8; }
.btn-cancel { background: #F1F5F9; color: #64748B; border: 1px solid #E2E8F0; }
.btn-cancel:hover { background: #E2E8F0; }
.info-val.muted { color: #94A3B8; }
.auto-hint { font-size: 11px; color: #94A3B8; margin-top: 12px; padding-top: 10px; border-top: 1px dashed #E2E8F0; }

/* 统计 */
.stats-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; }
.stat-item { text-align: center; }
.stat-num { font-size: 26px; font-weight: 700; color: #2563EB; }
.stat-num.warn-num { color: #EF4444; }
.stat-label { font-size: 12px; color: #94A3B8; margin-top: 2px; }

/* 统计 — 2x2 丰富数据卡 */
.stats-2x2 {
  display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr;
  gap: 10px; min-height: 180px;
}
.stat-card-h {
  display: flex; align-items: center; padding: 14px 16px; border-radius: 10px;
  background: linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 100%);
}
.stat-card-h.sc-amber { background: linear-gradient(135deg, #FFFBEB 0%, #FFFFFF 100%); }
.stat-card-h.sc-green { background: linear-gradient(135deg, #F0FDF4 0%, #FFFFFF 100%); }
.stat-card-h.sc-purple { background: linear-gradient(135deg, #FAF5FF 0%, #FFFFFF 100%); }
.sch-left { flex: 1; min-width: 0; }
.sch-num { font-size: 36px; font-weight: 700; color: #2563EB; line-height: 1; }
.sc-amber .sch-num { color: #F59E0B; }
.sc-green .sch-num { color: #16A34A; }
.sc-purple .sch-num { color: #8B5CF6; }
.sch-label { font-size: 14px; font-weight: 600; color: #1E293B; margin-top: 4px; }
.sch-sub { font-size: 11px; color: #64748B; margin-top: 2px; }
.sch-detail { font-size: 11px; color: #94A3B8; margin-top: 3px; line-height: 1.3; }
.stats-trend {
  margin-top: 8px; padding: 7px 14px; border-radius: 8px;
  background: #F8FAFC; font-size: 12px; color: #475569;
  border: 1px solid #E2E8F0;
}

/* ═══ 雷达图 + 洞察 ═══ */
.radar-and-insights {
  display: flex; gap: 28px; align-items: center;
}
.radar-section {
  display: flex; gap: 20px; align-items: center; flex-shrink: 0;
}
.radar-svg {
  width: 210px; height: 210px; flex-shrink: 0;
}
.radar-legend {
  display: flex; flex-direction: column; gap: 10px; min-width: 110px;
}
.radar-legend-item {
  display: flex; align-items: center; gap: 8px; padding: 5px 0;
  font-size: 13px;
}
.rl-dot {
  width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0;
}
.rl-name { color: #475569; white-space: nowrap; flex: 1; font-size: 14px; }
.rl-score-box {
  font-weight: 700; font-size: 13px; width: 32px; height: 22px;
  display: inline-flex; align-items: center; justify-content: center;
  border-radius: 4px; margin-left: auto;
}
.rl-score-box.good { background: #EFF6FF; color: #2563EB; }
.rl-score-box.mid { background: #FFFBEB; color: #F59E0B; }
.rl-score-box.low { background: #FEF2F2; color: #EF4444; }

/* 右侧洞察区 — 2x2网格（含遗忘曲线） */
.insights-section {
  display: grid; grid-template-columns: 1fr 1fr; gap: 10px;
  flex: 1; min-width: 220px;
}
.insight-card {
  background: #F8FAFC; border-radius: 8px; padding: 10px 14px;
  border: 1px solid #E2E8F0;
}
.insight-title { font-size: 13px; font-weight: 600; color: #1E293B; margin-bottom: 6px; }
.insight-list { display: flex; flex-wrap: wrap; gap: 4px; }
.insight-tag {
  font-size: 12px; padding: 3px 8px; border-radius: 6px;
  background: #EFF6FF; color: #2563EB; font-weight: 500;
}
.insight-tag.exam { background: #EFF6FF; color: #2563EB; }
.insight-empty { font-size: 12px; color: #94A3B8; padding: 4px 0; }
.insight-suggestion {
  font-size: 12px; color: #1E293B; padding: 4px 8px;
  border-left: 2px solid #2563EB; width: 100%;
}
/* 遗忘曲线 */
.curve-wrap { display: flex; flex-direction: column; gap: 4px; }
.curve-svg { width: 100%; height: 36px; }
.curve-info { font-size: 11px; color: #475569; line-height: 1.4; margin-bottom: 2px; }
.curve-info strong { color: #2563EB; }
.curve-items { display: flex; flex-direction: column; gap: 4px; }
.curve-item { display: flex; align-items: center; gap: 6px; font-size: 11px; }
.ci-dot { width: 5px; height: 5px; border-radius: 50%; flex-shrink: 0; }
.ci-dot.high { background: #EF4444; }
.ci-dot.mid { background: #F59E0B; }
.ci-dot.low { background: #16A34A; }
.ci-name { color: #1E293B; width: 58px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex-shrink: 0; }
.ci-retain-bar { flex: 1; height: 5px; background: #F1F5F9; border-radius: 3px; overflow: hidden; max-width: 60px; }
.cir-fill { height: 100%; border-radius: 3px; background: linear-gradient(90deg, #2563EB, #60A5FA); }
.ci-retain-num { color: #64748B; width: 26px; text-align: right; }

/* 薄弱点 */
.weakness-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 0; border-bottom: 1px solid #F1F5F9;
}
.weakness-item:last-child { border-bottom: none; }
.weakness-left { display: flex; align-items: center; gap: 8px; flex: 1; }
.weakness-name { font-size: 14px; color: #1E293B; font-weight: 500; }
.weakness-tag {
  font-size: 11px; padding: 1px 6px; border-radius: 4px;
}
.weakness-tag.interview { background: #EFF6FF; color: #2563EB; }
.weakness-tag.exam { background: #EFF6FF; color: #2563EB; }
.weakness-source { font-size: 12px; color: #94A3B8; }
.weakness-right { display: flex; align-items: center; gap: 10px; }
.weakness-score-bar { width: 60px; height: 6px; background: #F1F5F9; border-radius: 3px; overflow: hidden; }
.ws-fill { height: 100%; background: #2563EB; border-radius: 3px; }
.weakness-score { font-size: 13px; color: #64748B; width: 28px; text-align: right; }

/* 网格卡片布局（面试备战线、路线列表） */
.card-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.grid-card {
  background: white; border-radius: 8px; padding: 10px 12px;
  border: 1.5px dashed #93C5FD; cursor: pointer;
  transition: all 0.2s; position: relative;
}
.grid-card:hover { border-color: #2563EB; box-shadow: 0 2px 8px rgba(37,99,235,0.1); }
.grid-card.expanded { border-color: #2563EB; border-style: solid; }

/* 路线卡片（网格内） */
.path-header { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; justify-content: space-between; }
.path-title { font-size: 14px; font-weight: 600; color: #1E293B; }
.path-h-right { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
.path-diff { font-size: 10px; padding: 1px 6px; border-radius: 4px; }
.path-diff.beginner { background: #DCFCE7; color: #16A34A; }
.path-diff.intermediate { background: #EFF6FF; color: #2563EB; }
.path-diff.advanced { background: #FEE2E2; color: #DC2626; }
.path-expand-icon { font-size: 9px; color: #94A3B8; }
.path-desc { font-size: 12px; color: #64748B; margin-bottom: 4px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.path-meta { display: flex; gap: 12px; font-size: 11px; color: #94A3B8; margin-bottom: 6px; }
.path-progress { display: flex; align-items: center; gap: 8px; }
.progress-bar { flex: 1; height: 5px; background: #F1F5F9; border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: #2563EB; border-radius: 3px; transition: width 0.5s; }
.progress-text { font-size: 12px; color: #2563EB; font-weight: 600; }
.path-actions { display: flex; gap: 6px; }
.btn-del-path { background: none; border: none; color: #CBD5E1; cursor: pointer; font-size: 12px; }
.btn-del-path:hover { color: #EF4444; }

/* 面试记录卡片（网格内） */
.intv-card { cursor: pointer; }
.intv-card:hover { border-color: #2563EB; box-shadow: 0 2px 8px rgba(37,99,235,0.1); }
.intv-card .path-desc { font-size: 11px; margin-bottom: 2px; -webkit-line-clamp: 1; }
.intv-score { font-size: 13px; font-weight: 700; padding: 1px 8px; border-radius: 6px; }
.intv-score.high { background: #DCFCE7; color: #16A34A; }
.intv-score.mid { background: #FEF3C7; color: #D97706; }
.intv-score.low { background: #FEE2E2; color: #DC2626; }
.intv-weak-list { display: flex; flex-wrap: wrap; gap: 3px; margin-top: 4px; }
.intv-weak-tag { font-size: 10px; padding: 1px 6px; border-radius: 3px; background: #EFF6FF; color: #2563EB; }
.intv-dims { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; }
.intv-dim-item { font-size: 10px; color: #64748B; }
.intv-dim-item b { color: #1E293B; }

/* 来自收藏 */
.bookmark-section { margin-top: 8px; }
.bookmark-list { display: flex; flex-direction: column; gap: 8px; }
.bm-card {
  display: flex; align-items: center; justify-content: space-between;
  background: #EFF6FF; border: 1.5px dashed #93C5FD; border-radius: 10px;
  padding: 12px 16px; transition: all 0.15s;
}
.bm-card:hover { border-color: #2563EB; background: #DBEAFE; }
.bm-info { flex: 1; min-width: 0; }
.bm-name { font-size: 15px; font-weight: 600; color: #1E293B; }
.bm-meta { font-size: 12px; color: #94A3B8; margin-top: 2px; }
.bm-actions { flex-shrink: 0; margin-left: 12px; }
.bm-has-path { font-size: 13px; color: #16A34A; font-weight: 500; }

/* 弹窗 */
.modal-wrap { position: fixed; inset: 0; background: rgba(0,0,0,0.3); z-index: 1000; display: flex; align-items: center; justify-content: center; }
.modal-box { background: white; border-radius: 14px; padding: 24px; width: 380px; max-width: 90vw; }
.modal-title { font-size: 17px; font-weight: 700; color: #1E293B; margin-bottom: 14px; }
.modal-input, .modal-textarea { width: 100%; padding: 8px 12px; border: 1.5px solid #E2E8F0; border-radius: 8px; font-size: 14px; outline: none; font-family: inherit; margin-bottom: 10px; box-sizing: border-box; }
.modal-input:focus, .modal-textarea:focus { border-color: #2563EB; }
.modal-textarea { resize: vertical; }
.modal-actions { display: flex; gap: 8px; justify-content: flex-end; }

/* 复习卡片（网格内） */
.review-grid-card { display: flex; flex-direction: column; gap: 4px; }
.rg-title { font-size: 13px; font-weight: 600; color: #1E293B; line-height: 1.3; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.rg-meta { font-size: 11px; color: #94A3B8; }
.rg-date { font-size: 10px; color: #94A3B8; }
.rg-btn { margin-top: auto; align-self: flex-start; padding: 2px 10px; font-size: 11px; }
.review-actions { display: flex; gap: 8px; align-items: center; }

/* 复习文档弹窗 */
.doc-modal { width: 500px; max-width: 90vw; max-height: 80vh; display: flex; flex-direction: column; }
.doc-modal-body { flex: 1; overflow-y: auto; font-size: 14px; line-height: 1.6; color: #1E293B; padding: 8px 0; margin-bottom: 10px; }
.doc-modal-body :deep(h2) { font-size: 17px; font-weight: 700; margin: 12px 0 6px; }
.doc-modal-body :deep(h3) { font-size: 15px; font-weight: 700; margin: 8px 0 4px; }
.doc-modal-body :deep(p) { margin: 4px 0; }
.doc-modal-body :deep(li) { margin: 2px 0; }
.doc-modal-body :deep(ul) { padding-left: 18px; }
.modal-loading { text-align: center; padding: 40px; color: #94A3B8; font-size: 14px; }

/* 简历 */
.resume-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.resume-career { font-size: 16px; font-weight: 600; color: #1E293B; }
.match-badge { font-size: 20px; font-weight: 700; }
.match-badge.high { color: #16A34A; }
.match-badge.mid { color: #F59E0B; }
.match-badge.low { color: #EF4444; }
.resume-section { margin-bottom: 14px; }
.resume-sec-title { font-size: 13px; color: #94A3B8; margin-bottom: 4px; }
.resume-sec-body { font-size: 14px; color: #1E293B; line-height: 1.6; }

/* 通用 */
.btn-sm { padding: 6px 14px; border-radius: 8px; font-size: 13px; border: none; cursor: pointer; transition: all 0.2s; font-weight: 500; }
.btn-blue { background: #2563EB; color: white; }
.btn-blue:hover { background: #1D4ED8; }
.btn-blue:disabled { background: #93C5FD; cursor: not-allowed; }
.btn-warm { background: #EFF6FF; color: #2563EB; border: 1.5px solid #BFDBFE; }
.btn-warm:hover { background: #DBEAFE; }
.btn-warm:disabled { background: #FEF9C3; color: #D4A373; cursor: not-allowed; }
.empty-state { text-align: center; padding: 40px; color: #94A3B8; font-size: 14px; }

/* ═══ 面试备战：薄弱点卡片 ═══ */
.weak-card-grid { display: flex; flex-direction: column; gap: 10px; margin-bottom: 16px; }
.weak-card {
  background: white; border-radius: 12px; border: 1.5px dashed #93C5FD;
  transition: all 0.2s; overflow: hidden;
}
.weak-card.open { border-color: #2563EB; box-shadow: 0 2px 12px rgba(37,99,235,0.08); }
.weak-card-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 18px; cursor: pointer; transition: background 0.15s;
}
.weak-card-header:hover { background: #F8FAFC; }
.weak-card-left { display: flex; align-items: center; gap: 10px; flex: 1; }
.weak-card-icon { font-size: 20px; }
.weak-card-info { display: flex; align-items: center; gap: 8px; }
.weak-card-name { font-size: 15px; font-weight: 600; color: #1E293B; }
.weak-card-tag { font-size: 11px; padding: 1px 8px; border-radius: 4px; }
.weak-card-tag.interview { background: #EFF6FF; color: #2563EB; }
.weak-card-tag.exam { background: #EFF6FF; color: #2563EB; }
.weak-card-right { display: flex; align-items: center; gap: 12px; }
.weak-score-wrap { display: flex; align-items: center; gap: 6px; }
.weak-score-bar { width: 50px; height: 6px; background: #F1F5F9; border-radius: 3px; overflow: hidden; }
.weak-card .ws-fill { height: 100%; background: #2563EB; border-radius: 3px; }
.weak-num { font-size: 13px; color: #64748B; font-weight: 500; width: 24px; text-align: right; }
.weak-expand-icon { font-size: 11px; color: #94A3B8; transition: transform 0.2s; }
.btn-green { background: #DCFCE7; color: #16A34A; border: 1.5px solid #86EFAC; }
.btn-green:hover { background: #BBF7D0; }
.btn-tiny { padding: 3px 10px; border-radius: 6px; font-size: 12px; border: none; cursor: pointer; font-weight: 500; transition: all 0.15s; }

.lc-tab-icon { width: 18px; height: 18px; color: var(--primary); }

.ic { width: 16px; height: 16px; display: inline; vertical-align: -2.5px; margin-right: 3px; color: var(--primary); }
.ic-sm { width: 14px; height: 14px; display: inline; vertical-align: -2px; color: var(--primary); }
.ic-btn { width: 16px; height: 16px; vertical-align: -3px; color: var(--primary); }
.ic-check { width: 14px; height: 14px; color: #16A34A; vertical-align: -2px; }

/* 网格卡片布局（面试备战线、路线列表、复习） */
.card-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
.grid-card {
  background: white; border-radius: 8px; padding: 10px 12px;
  border: 1.5px dashed #93C5FD; cursor: pointer;
  transition: all 0.2s; position: relative;
}
.grid-card:hover { border-color: #2563EB; box-shadow: 0 2px 8px rgba(37,99,235,0.1); }
.grid-card.expanded { border-color: #2563EB; border-style: solid; }

/* 路线卡片（网格内） */
.path-header { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; justify-content: space-between; }
.path-title { font-size: 14px; font-weight: 600; color: #1E293B; }
.path-h-right { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
.path-diff { font-size: 10px; padding: 1px 6px; border-radius: 4px; }
.path-diff.beginner { background: #DCFCE7; color: #16A34A; }
.path-diff.intermediate { background: #EFF6FF; color: #2563EB; }
.path-diff.advanced { background: #FEE2E2; color: #DC2626; }
.path-expand-icon { font-size: 9px; color: #94A3B8; }
.path-desc { font-size: 12px; color: #64748B; margin-bottom: 4px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.path-meta { display: flex; gap: 12px; font-size: 11px; color: #94A3B8; margin-bottom: 6px; }
.path-progress { display: flex; align-items: center; gap: 8px; }
.progress-bar { flex: 1; height: 5px; background: #F1F5F9; border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: #2563EB; border-radius: 3px; transition: width 0.5s; }
.progress-text { font-size: 12px; color: #2563EB; font-weight: 600; }
.path-actions { display: flex; gap: 6px; }
.btn-del-path { background: none; border: none; color: #CBD5E1; cursor: pointer; font-size: 12px; }
.btn-del-path:hover { color: #EF4444; }

/* 面试记录卡片（网格内） */
.intv-card { cursor: pointer; }
.intv-card:hover { border-color: #2563EB; box-shadow: 0 2px 8px rgba(37,99,235,0.1); }
.intv-card .path-desc { font-size: 11px; margin-bottom: 2px; -webkit-line-clamp: 1; }
.intv-score { font-size: 13px; font-weight: 700; padding: 1px 8px; border-radius: 6px; }
.intv-score.high { background: #DCFCE7; color: #16A34A; }
.intv-score.mid { background: #FEF3C7; color: #D97706; }
.intv-score.low { background: #FEE2E2; color: #DC2626; }
.intv-weak-list { display: flex; flex-wrap: wrap; gap: 3px; margin-top: 4px; }
.intv-weak-tag { font-size: 10px; padding: 1px 6px; border-radius: 3px; background: #EFF6FF; color: #2563EB; }
.intv-dims { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; }
.intv-dim-item { font-size: 10px; color: #64748B; }
.intv-dim-item b { color: #1E293B; }

/* 来自收藏 */
.bookmark-section { margin-top: 8px; }
.bookmark-list { display: flex; flex-direction: column; gap: 8px; }
.bm-card {
  display: flex; align-items: center; justify-content: space-between;
  background: #EFF6FF; border: 1.5px dashed #93C5FD; border-radius: 10px;
  padding: 12px 16px; transition: all 0.15s;
}
.bm-card:hover { border-color: #2563EB; background: #DBEAFE; }
.bm-info { flex: 1; min-width: 0; }
.bm-name { font-size: 15px; font-weight: 600; color: #1E293B; }
.bm-meta { font-size: 12px; color: #94A3B8; margin-top: 2px; }
.bm-actions { flex-shrink: 0; margin-left: 12px; }
.bm-has-path { font-size: 13px; color: #16A34A; font-weight: 500; }

/* 弹窗 */
.modal-wrap { position: fixed; inset: 0; background: rgba(0,0,0,0.3); z-index: 1000; display: flex; align-items: center; justify-content: center; }
.modal-box { background: white; border-radius: 14px; padding: 24px; width: 380px; max-width: 90vw; }
.modal-title { font-size: 17px; font-weight: 700; color: #1E293B; margin-bottom: 14px; }
.modal-input, .modal-textarea { width: 100%; padding: 8px 12px; border: 1.5px solid #E2E8F0; border-radius: 8px; font-size: 14px; outline: none; font-family: inherit; margin-bottom: 10px; box-sizing: border-box; }
.modal-input:focus, .modal-textarea:focus { border-color: #2563EB; }
.modal-textarea { resize: vertical; }
.modal-actions { display: flex; gap: 8px; justify-content: flex-end; }

/* 复习卡片（网格内） */
.review-grid-card { display: flex; flex-direction: column; gap: 4px; }
.rg-title { font-size: 13px; font-weight: 600; color: #1E293B; line-height: 1.3; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.rg-meta { font-size: 11px; color: #94A3B8; }
.rg-date { font-size: 10px; color: #94A3B8; }
.rg-btn { margin-top: auto; align-self: flex-start; padding: 2px 10px; font-size: 11px; }
.review-actions { display: flex; gap: 8px; align-items: center; }

/* 复习文档弹窗 */
.doc-modal { width: 500px; max-width: 90vw; max-height: 80vh; display: flex; flex-direction: column; }
.doc-modal-body { flex: 1; overflow-y: auto; font-size: 14px; line-height: 1.6; color: #1E293B; padding: 8px 0; margin-bottom: 10px; }
.doc-modal-body :deep(h2) { font-size: 17px; font-weight: 700; margin: 12px 0 6px; }
.doc-modal-body :deep(h3) { font-size: 15px; font-weight: 700; margin: 8px 0 4px; }
.doc-modal-body :deep(p) { margin: 4px 0; }
.doc-modal-body :deep(li) { margin: 2px 0; }
.doc-modal-body :deep(ul) { padding-left: 18px; }
.modal-loading { text-align: center; padding: 40px; color: #94A3B8; font-size: 14px; }

/* 简历 */
.resume-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.resume-actions { display: flex; gap: 8px; }
.btn-outline { background: #fff; color: #2563EB; border: 1.5px solid #BFDBFE; }
.btn-outline:hover { background: #EFF6FF; }
.btn-blue { background: #2563EB; color: white; }
.btn-blue:hover { background: #1D4ED8; }
.btn-blue:disabled { background: #93C5FD; cursor: not-allowed; }
.btn-warm { background: #EFF6FF; color: #2563EB; border: 1.5px solid #BFDBFE; }
.btn-warm:hover { background: #DBEAFE; }
.btn-warm:disabled { background: #FEF9C3; color: #D4A373; cursor: not-allowed; }
.empty-state { text-align: center; padding: 40px; color: #94A3B8; font-size: 14px; }
.empty-state br { margin-bottom: 8px; }

/* 展开的学习面板 */
.weak-study-panel {
  border-top: 1px solid #EFF6FF; padding: 16px 18px;
  background: linear-gradient(135deg, #FAFCFF 0%, #F8FAFC 100%);
}
.wsp-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; }
.wsp-card {
  background: white; border-radius: 10px; padding: 14px;
  border: 1px solid #E2E8F0; display: flex; flex-direction: column;
}
.wsp-card-title {
  font-size: 14px; font-weight: 600; color: #1E293B;
  margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;
}
.wsp-docs { display: flex; flex-direction: column; gap: 8px; }
.wsp-doc-item { border-bottom: 1px solid #F1F5F9; padding-bottom: 6px; }
.wsp-doc-item:last-child { border-bottom: none; }
.wsp-doc-title { font-size: 13px; font-weight: 600; color: #2563EB; margin-bottom: 2px; }
.wsp-doc-preview { font-size: 12px; color: #64748B; line-height: 1.4; max-height: 80px; overflow: hidden; }
.wsp-doc-preview :deep(p) { margin: 2px 0; }
.wsp-doc-preview :deep(code) { background: #F1F5F9; padding: 1px 3px; border-radius: 2px; font-size: 11px; }
.wsp-empty { font-size: 12px; color: #94A3B8; padding: 20px 0; text-align: center; }
.wsp-videos { display: flex; flex-direction: column; gap: 6px; }
.wsp-video-item {
  display: flex; gap: 8px; align-items: center; text-decoration: none;
  padding: 6px; border-radius: 6px; transition: background 0.12s;
}
.wsp-video-item:hover { background: #F1F5F9; }
.wsp-video-thumb { width: 48px; height: 32px; border-radius: 4px; background-size: cover; background-position: center; background-color: #F1F5F9; flex-shrink: 0; }
.wsp-video-name { font-size: 12px; color: #1E293B; line-height: 1.3; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }

/* AI对话（面试备战面板内） */
.wsp-chat-card { min-height: 200px; }
.wsp-chat-msgs { flex: 1; overflow-y: auto; max-height: 160px; display: flex; flex-direction: column; gap: 6px; margin-bottom: 8px; }
.wsp-chat-msg { display: flex; }
.wsp-chat-msg.user { justify-content: flex-end; }
.wsp-chat-bubble { max-width: 90%; padding: 6px 10px; border-radius: 10px; font-size: 12px; line-height: 1.4; word-break: break-word; }
.wsp-chat-msg.assistant .wsp-chat-bubble { background: #F1F5F9; color: #1E293B; border-bottom-left-radius: 3px; }
.wsp-chat-msg.user .wsp-chat-bubble { background: #2563EB; color: white; border-bottom-right-radius: 3px; }
.wsp-chat-input-row { display: flex; gap: 4px; }
.wsp-chat-input {
  flex: 1; padding: 6px; border: 1px solid #E2E8F0; border-radius: 6px;
  font-size: 12px; outline: none; font-family: inherit;
}
.wsp-chat-input:focus { border-color: #2563EB; }

@media (max-width: 768px) {
  .profile-cards { grid-template-columns: 1fr; }
  .stats-grid { grid-template-columns: repeat(3, 1fr); }
  .stats-2x2 { gap: 6px; min-height: auto; }
  .stat-card-h { padding: 10px 10px; }
  .sch-num { font-size: 26px; }
  .sch-detail { display: none; }
  .stats-trend { font-size: 11px; }
  .ci-name { width: 40px; }
  .radar-and-insights { flex-direction: column; }
  .radar-section { flex-wrap: wrap; }
  .insights-section { grid-template-columns: 1fr; }
}
</style>