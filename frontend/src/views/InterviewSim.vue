<template>
  <div class="interview-sim">
    <!-- ═══ 页面顶部 Banner ═══ -->
    <PageBanner fullwidth
      title="面试模拟"
      description="AI 面试官实时对话，模拟真实面试场景，多维评估报告"
      :icon="'Mic'"
      variant="primary"
    />
    <!-- ============================================================
         一、顶部标题区
         ============================================================ -->
    <section class="section-header">
      <Mic :size="16" class="icon-blue" />
      <h2 class="section-title">面试模拟</h2>
      <p class="header-desc">多模态 AI 模拟面试，语音 + 视频 + 表情分析，真实还原面试场景</p>
    </section>

    <!-- ============================================================
         二、核心操作区（Hero Card）
         ============================================================ -->
    <section class="zone-core">
      <div class="zone-label"><Zap :size="16" class="icon-blue" /> 核心操作</div>
      <div class="hero-card" @click="$router.push('/interview/session')">
        <div class="hero-bg-glow"></div>
        <img src="/src/assets/xiaoju-glasses.png" class="hero-cat" alt="小橘面试官">
        <div class="hero-content">
          <div class="hero-icon-block">
            <Video :size="16" class="icon-blue" />
          </div>
          <div class="hero-text-block">
            <div class="hero-title">多模态 AI 模拟面试</div>
            <div class="hero-desc">AI 面试官实时对话 · 语音互动 · 摄像头录制 · 多维评估报告</div>
            <div class="hero-tags">
              <span class="tag-pill"><Mic :size="16" class="icon-blue" /> 语音对话</span>
              <span class="tag-pill"><Camera :size="16" class="icon-blue" /> 摄像头录制</span>
              <span class="tag-pill"><BarChart :size="16" class="icon-blue" /> 多维评估</span>
            </div>
          </div>
<div class="hero-action-block">
            <span class="btn-primary hero-btn">开始面试</span>
            <ArrowRight :size="16" class="icon-blue" />
          </div>
        </div>
      </div>
    </section>

    <!-- ============================================================
         三、成长辅助区（今日任务 + 热门面经 + 折叠）
         ============================================================ -->
    <section class="zone-growth" :class="{ 'is-collapsed': growthCollapsed }">
      <!-- 引导提示 -->
      <transition name="guide-fade">
        <div class="growth-guide" v-if="showGrowthGuide">
          <Lightbulb :size="16" class="icon-blue" /> 这里可以领每日练习、看大厂面经
        </div>
      </transition>

      <!-- 区域头 -->
      <div class="zone-growth-header">
        <div class="zone-label" style="margin-bottom:0">
          <Sprout :size="16" class="icon-blue" /> 成长辅助
        </div>
        <div class="growth-toggle" @click="growthCollapsed = !growthCollapsed">
          <span>{{ growthCollapsed ? '展开' : '收起' }}</span>
          <ChevronDown :size="16" class="icon-blue" :class="{ up: !growthCollapsed }" />
        </div>
      </div>

      <div class="growth-body" v-show="!growthCollapsed">
        <!-- 左侧：今日面试小任务 -->
        <div class="growth-left">
          <div class="card daily-task-card">
            <div class="daily-task-header">
              <ClipboardList :size="16" class="icon-blue" />
              <span class="daily-task-title">今日面试小任务</span>
            </div>
            <div class="daily-task-content">
              <div class="daily-task-name">{{ dailyTask.title }}</div>
              <div class="daily-task-desc">{{ dailyTask.desc }}</div>
              <div class="daily-task-meta"><Clock :size="16" class="icon-blue" /> 预计 {{ dailyTask.time }}</div>
            </div>
            <button class="btn-primary daily-task-btn" @click="$router.push(dailyTask.link)">
              开始练习 <ArrowRight :size="16" class="icon-blue" />
            </button>
          </div>
        </div>

        <!-- 右侧：热门面经速览 -->
        <div class="growth-right">
          <div class="experience-header">
            <span class="experience-title"><Flame :size="16" class="icon-blue" /> 热门面经速览</span>
            <button class="btn-outline experience-refresh" @click="refreshExperiences">
              <RefreshCw :size="16" class="icon-blue" /> 换一批
            </button>
          </div>
          <div class="experience-list">
            <div
              v-for="(exp, i) in displayedExperiences"
              :key="i"
              class="card experience-item"
              @click="openExperience(exp)"
            >
              <span class="tag-pill exp-tag" :style="{ background: exp.tagColor + '18', color: exp.tagColor }">{{ exp.tag }}</span>
              <span class="exp-title">{{ exp.title }}</span>
              <ChevronRight :size="16" class="icon-blue" />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ============================================================
         四、复盘记录区（等宽三卡片）
         ============================================================ -->
    <section class="zone-review">
      <div class="section-header" style="margin-bottom:1rem;padding:0;">
        <History :size="16" class="icon-blue" />
        <h3 class="section-title" style="font-size:1.1rem;">复盘工具</h3>
      </div>
      <div class="grid-3 review-cards">
        <!-- 面试历史记录 -->
        <div class="card stat-card review-card" @click="$router.push('/interview/history')">
          <div class="review-card-icon-wrap" style="background:var(--primary-bg)">
            <BarChart :size="16" :color="'var(--primary)'" />
          </div>
          <div class="review-card-title">面试历史记录</div>
          <div class="review-card-stat">已完成 <b>{{ stats.total_interview_sessions }}</b> 次模拟</div>
          <div class="review-card-hint">历次问答、表情分析、成绩趋势</div>
          <div class="review-card-cta">查看详情 <ArrowRight :size="16" class="icon-blue" /></div>
        </div>

        <!-- 全部错题回顾 -->
        <div class="card stat-card review-card" @click="$router.push('/interview/wrong-questions')">
          <div class="review-card-icon-wrap" style="background:var(--accent-bg)">
            <X :size="16" :color="'var(--accent)'" />
          </div>
          <div class="review-card-title">全部错题回顾</div>
          <div class="review-card-stat">共 <b>{{ interviewWrongTotal }}</b> 道待回顾</div>
          <div class="review-card-hint">重新练习、标记掌握、清除错题</div>
          <div class="review-card-cta">查看详情 <ArrowRight :size="16" class="icon-blue" /></div>
        </div>

        <!-- 我的收藏 -->
        <div class="card stat-card review-card" @click="$router.push('/interview/saved-questions')">
          <div class="review-card-icon-wrap" style="background:var(--accent-bg)">
            <Star :size="16" :color="'var(--accent)'" />
          </div>
          <div class="review-card-title">我的收藏</div>
          <div class="review-card-stat">已收藏 <b>{{ interviewSavedTotal }}</b> 道题</div>
          <div class="review-card-hint">收藏的优质面试题，方便复习</div>
          <div class="review-card-cta">查看详情 <ArrowRight :size="16" class="icon-blue" /></div>
        </div>
      </div>
    </section>

    <!-- ============================================================
         五、底部辅助区
         ============================================================ -->
    <section class="helper-section">
      <div class="helper-item" @click="showHelp = !showHelp">
        <CircleHelp :size="16" class="icon-blue" />
        <span>使用帮助</span>
      </div>
      <span class="helper-dot">·</span>
      <div class="helper-item" @click="showFeedback = !showFeedback">
        <MessageSquare :size="16" class="icon-blue" />
        <span>意见反馈</span>
      </div>
    </section>

    <!-- 使用帮助弹窗 -->
    <el-dialog v-model="showHelp" width="480px" destroy-on-close>
      <template #title>
        <CircleHelp :size="16" class="icon-blue" /> 使用帮助
      </template>
      <div class="help-content">
        <div class="help-item">
          <span class="help-num">1</span>
          <span>点击「多模态 AI 模拟面试」开启一次完整的 AI 面试体验</span>
        </div>
        <div class="help-item">
          <span class="help-num">2</span>
          <span>选择岗位类型，AI 面试官会根据岗位进行针对性提问</span>
        </div>
        <div class="help-item">
          <span class="help-num">3</span>
          <span>支持语音回答和文字输入两种方式，自由切换</span>
        </div>
        <div class="help-item">
          <span class="help-num">4</span>
          <span>面试结束后生成完整评估报告，查看表情分析数据</span>
        </div>
        <div class="help-item">
          <span class="help-num">5</span>
          <span>错题可以回顾重练，收藏好题方便日后复习</span>
        </div>
        <div class="help-note">如有问题请联系项目团队</div>
      </div>
    </el-dialog>

    <!-- 意见反馈弹窗 -->
    <el-dialog v-model="showFeedback" width="480px" destroy-on-close>
      <template #title>
        <MessageSquare :size="16" class="icon-blue" /> 意见反馈
      </template>
      <div class="feedback-content">
        <el-input v-model="feedbackText" type="textarea" :rows="5" placeholder="请描述你的建议或遇到的问题..." />
        <div class="feedback-actions" style="margin-top:1rem;text-align:right">
          <el-button @click="showFeedback = false">取消</el-button>
          <el-button type="primary" @click="submitFeedback">提交反馈</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import PageBanner from '../components/PageBanner.vue'

// ===== 统计 =====
const stats = reactive({ total_interview_sessions: 0, total_saved: 0 })
async function loadStats() {
  try { const { data } = await axios.get('/api/exam/stats'); Object.assign(stats, data) } catch { /* ignore */ }
}

// ===== 面试错题统计 =====
const interviewWrongTotal = ref(0)
async function loadInterviewWrongCount() {
  try {
    const { data } = await axios.get('/api/interview/wrong-questions', { params: { page: 1, page_size: 1 } })
    interviewWrongTotal.value = data.total || 0
  } catch { /* ignore */ }
}

// ===== 面试收藏统计 =====
const interviewSavedTotal = ref(0)
async function loadInterviewSavedCount() {
  try {
    const { data } = await axios.get('/api/interview/saved-questions', { params: { page: 1, page_size: 1 } })
    interviewSavedTotal.value = data.total || 0
  } catch { /* ignore */ }
}

// ===== 弹窗 =====
const showHelp = ref(false)
const showFeedback = ref(false)
const feedbackText = ref('')

// ===== 🌱 成长辅助区 =====
// 每日任务池（按日期轮换）
const taskPool = [
  { title: '自我介绍练习', desc: '用1分钟介绍你的专业背景、项目经历和求职动机', time: '3分钟', link: '/interview/session' },
  { title: '项目亮点梳理', desc: '准备好3个关键词概括你最满意的项目经历', time: '5分钟', link: '/interview/session' },
  { title: '岗位认知问答', desc: '说说你对目标岗位的理解，为什么适合这份工作', time: '3分钟', link: '/interview/session' },
  { title: '行为面试准备', desc: '用STAR法则梳理一个克服困难的团队经历', time: '5分钟', link: '/interview/session' },
  { title: '技术面预热', desc: '快速回顾你所学专业最核心的2个知识点', time: '4分钟', link: '/interview/session' },
  { title: '职业规划表达', desc: '准备1分钟简洁回答：你未来3年的职业目标是什么', time: '3分钟', link: '/interview/session' },
]
// 用日期取模选今日任务
const todayIdx = new Date().getDate() % taskPool.length
const dailyTask = ref(taskPool[todayIdx])

// 面经池
const experiencePool = [
  { title: '字节后端三面常问的Redis核心问题', tag: '字节跳动', tagColor: '#e74c3c' },
  { title: '腾讯产品经理群面全流程复盘', tag: '腾讯', tagColor: '#2196F3' },
  { title: '阿里前端一面手写题与场景题汇总', tag: '阿里巴巴', tagColor: '#ff6a00' },
  { title: '美团后端二面项目深挖实录', tag: '美团', tagColor: '#00b894' },
  { title: '百度产品运营群面案例题解析', tag: '百度', tagColor: '#2962ff' },
  { title: '华为技术面代码手撕与系统设计', tag: '华为', tagColor: '#cf1322' },
  { title: '拼多多后端高频算法题整理', tag: '拼多多', tagColor: '#e74c3c' },
  { title: '蔚来汽车自动驾驶算法面试复盘', tag: '蔚来', tagColor: '#00b894' },
  { title: '小红书数据分析SQL与AB测试真题', tag: '小红书', tagColor: '#ff6a00' },
  { title: '快手前端React原理与性能优化', tag: '快手', tagColor: '#ff6a00' },
  { title: '京东后端分布式与微服务面试题', tag: '京东', tagColor: '#e74c3c' },
  { title: '网易游戏策划岗案例分析题攻略', tag: '网易', tagColor: '#cf1322' },
]
const displayedExperiences = ref([])
function refreshExperiences() {
  const shuffled = [...experiencePool].sort(() => Math.random() - 0.5)
  displayedExperiences.value = shuffled.slice(0, 3)
}
refreshExperiences() // 初始化

// 折叠状态
const growthCollapsed = ref(false)

// 引导提示（首次进入显示1秒）
const showGrowthGuide = ref(false)
function showGuideOnce() {
  const seen = localStorage.getItem('growth_guide_done')
  if (!seen) {
    showGrowthGuide.value = true
    localStorage.setItem('growth_guide_done', '1')
    setTimeout(() => { showGrowthGuide.value = false }, 1500)
  }
}

// 点击面经弹窗查看
function openExperience(exp) {
  ElMessage.info(`📄 ${exp.tag} · ${exp.title}\n（模拟面经预览功能，正式版将对接真实面经平台）`)
}

function submitFeedback() {
  if (!feedbackText.value.trim()) { ElMessage.warning('请填写反馈内容'); return }
  ElMessage.success('感谢你的反馈！我们会尽快处理 🙏')
  showFeedback.value = false
  feedbackText.value = ''
}

// ===== 生命周期 =====
onMounted(() => {
  loadStats()
  loadInterviewWrongCount()
  loadInterviewSavedCount()
  showGuideOnce()
})
</script>

<style scoped>
/* ═══════════════════════════ 布局 & 容器 ═══════════════════════════ */
.interview-sim {
  padding: 0 0 3rem;
}

/* ═══════════════════════════ 一、顶部标题区 ═══════════════════════════ */
.section-header {
  text-align: center;
  padding: 2rem 0 0.6rem;
}
.header-icon {
  font-size: 2.8rem;
  color: var(--primary);
  margin-bottom: 0.2rem;
}
.section-title {
  font-size: 1.7rem;
  font-weight: 700;
  margin: 0.3rem 0;
  background: var(--primary-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  color: transparent;
}
.header-desc {
  color: var(--text-muted, #999);
  font-size: 0.85rem;
  max-width: 480px;
  margin: 0 auto 0.8rem;
  line-height: 1.5;
}

/* ═══════════════════════════ 区域标签 ═══════════════════════════ */
.zone-label {
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--text-muted, #bbb);
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 10px;
  padding-left: 4px;
}

/* ═══════════════════════════ 二、核心操作区 ═══════════════════════════ */
.zone-core {
  margin: 20px 0 36px;
  padding: 20px;
  border-radius: var(--radius-lg, 16px);
  background: var(--primary-bg, var(--primary-bg));
  border: 1px solid var(--border-light, #E8ECF2);
}

.hero-card {
  position: relative;
  border-radius: 18px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: var(--primary-gradient);
  border: none;
}
.hero-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(61, 90, 128, 0.35);
}
.hero-bg-glow {
  position: absolute;
  top: -60%;
  right: -20%;
  width: 400px;
  height: 400px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255,255,255,0.15) 0%, transparent 70%);
  pointer-events: none;
}
.hero-content {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 28px 32px;
  position: relative;
  z-index: 1;
}
.hero-icon-block {
  width: 72px;
  height: 72px;
  border-radius: 18px;
  background: rgba(255,255,255,0.18);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  backdrop-filter: blur(4px);
}
.hero-main-icon { font-size: 2.4rem; color: #fff; }

.hero-text-block { flex: 1; min-width: 0; }
.hero-text-block .hero-title {
  font-weight: 700;
  font-size: 1.3rem;
  color: #fff;
  margin-bottom: 4px;
}
.hero-text-block .hero-desc {
  font-size: 0.85rem;
  color: rgba(255,255,255,0.7);
  line-height: 1.4;
  margin-bottom: 10px;
}
.hero-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.hero-tags .tag-pill {
  font-size: 0.75rem;
  padding: 3px 12px;
  border-radius: 20px;
  background: rgba(255,255,255,0.15);
  color: rgba(255,255,255,0.9);
  backdrop-filter: blur(4px);
  border: none;
}

/* ═══ 面试猫助手 ═══ */
.hero-cat {
  height: 100px;
  width: auto;
  opacity: 0.95;
  filter: drop-shadow(0 3px 10px rgba(0,0,0,0.2));
  transition: transform 0.3s ease;
  position: absolute;
  right: 220px;
  bottom: -5px;
  z-index: 2;
}
.hero-cat:hover {
  transform: scale(1.08) rotate(3deg);
}
.hero-action-block {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
  padding: 10px 20px;
  background: rgba(255,255,255,0.2);
  border-radius: 12px;
  transition: all 0.2s;
  position: relative;
  overflow: visible;
}
.hero-card:hover .hero-action-block {
  background: rgba(255,255,255,0.3);
  transform: scale(1.03);
}

/* 开始面试按钮 */
.hero-btn.btn-primary {
  font-size: 0.95rem;
  font-weight: 600;
  color: #fff;
  background: transparent;
  border: none;
  padding: 0;
  box-shadow: none;
}
.hero-btn-arrow {
  font-size: 1.1rem;
  color: #fff;
  transition: transform 0.2s;
}
.hero-card:hover .hero-btn-arrow {
  transform: translateX(4px);
}

/* ═══════════════════════════ 三、成长辅助区 ═══════════════════════════ */
.zone-growth {
  margin: 0 0 24px;
  padding: 16px 20px 20px;
  border-radius: var(--radius-lg, 16px);
  background: var(--bg-alt, var(--bg-alt));
  border: 1px solid var(--border-light, #eef0ff);
  position: relative;
}
.zone-growth.is-collapsed {
  padding-bottom: 12px;
}

/* 引导提示 */
.growth-guide {
  position: absolute;
  top: -14px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--primary-gradient);
  color: #fff;
  font-size: 0.82rem;
  padding: 6px 22px;
  border-radius: 30px;
  box-shadow: 0 4px 16px rgba(61, 90, 128, 0.25);
  white-space: nowrap;
  z-index: 5;
}
.guide-fade-enter-active { transition: all 0.4s ease; }
.guide-fade-leave-active { transition: all 0.5s ease; }
.guide-fade-enter-from,
.guide-fade-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-8px);
}

/* 区域头 */
.zone-growth-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.growth-toggle {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.75rem;
  color: var(--text-muted, #bbb);
  cursor: pointer;
  padding: 2px 10px;
  border-radius: 6px;
  transition: all 0.15s;
  user-select: none;
}
.growth-toggle:hover { color: var(--primary, #3D5A80); background: var(--primary-bg, var(--primary-bg)); }
.toggle-arrow {
  font-size: 0.7rem;
  transition: transform 0.2s;
}
.toggle-arrow.up { transform: rotate(180deg); }

/* 主体：左右两栏 */
.growth-body {
  display: flex;
  gap: 16px;
}
.growth-left {
  flex: 1;
  min-width: 0;
}
.growth-right {
  flex: 1.6;
  min-width: 0;
}

/* 每日任务卡片 */
.card.daily-task-card {
  padding: 16px;
  display: flex;
  flex-direction: column;
  height: 100%;
}
.daily-task-card:hover {
  box-shadow: var(--shadow-hover, 0 4px 16px rgba(61, 90, 128, 0.08));
}
.daily-task-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 10px;
}
.daily-task-icon {
  font-size: 1.1rem;
  color: var(--primary, #3D5A80);
}
.daily-task-title {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-muted, #888);
}
.daily-task-content {
  flex: 1;
  margin-bottom: 12px;
}
.daily-task-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-heading, #444);
  margin-bottom: 4px;
}
.daily-task-desc {
  font-size: 0.8rem;
  color: var(--text-muted, #999);
  line-height: 1.4;
  margin-bottom: 6px;
}
.daily-task-meta {
  font-size: 0.75rem;
  color: var(--text-muted, #bbb);
}

/* 右侧面经 */
.experience-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}
.experience-title {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-muted, #888);
}
.btn-outline.experience-refresh {
  font-size: 0.75rem;
  padding: 2px 10px;
  border: 1px solid var(--border, #e0e0e0);
  background: transparent;
  cursor: pointer;
  border-radius: 6px;
  color: var(--text-muted, #aaa);
  transition: all 0.15s;
}
.btn-outline.experience-refresh:hover {
  color: var(--primary, #3D5A80);
  border-color: var(--primary, #3D5A80);
  background: var(--primary-bg, var(--primary-bg));
}

.experience-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.card.experience-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  cursor: pointer;
  transition: all 0.2s;
}
.card.experience-item:hover {
  border-color: var(--border, #ddd);
  background: var(--bg-alt, var(--bg-hover));
  transform: translateX(2px);
}
.exp-tag.tag-pill {
  font-size: 0.68rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 4px;
  flex-shrink: 0;
  white-space: nowrap;
}
.exp-title {
  flex: 1;
  font-size: 0.82rem;
  color: var(--text-body, #555);
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.exp-arrow {
  font-size: 0.75rem;
  color: var(--text-muted, #ccc);
  flex-shrink: 0;
  transition: transform 0.15s;
}
.card.experience-item:hover .exp-arrow {
  color: var(--primary, #3D5A80);
  transform: translateX(2px);
}

/* ═══════════════════════════ 四、复盘记录区 ═══════════════════════════ */
.zone-review {
  margin-bottom: 30px;
  padding: 20px;
  border-radius: var(--radius-lg, 16px);
  background: var(--bg-card, var(--bg-card));
  border: 1px solid var(--border, #f0f0f0);
}

.review-cards {
  gap: 14px;
}
.card.stat-card.review-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 24px 16px 20px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.card.stat-card.review-card:hover {
  border-color: var(--border, #ddd);
  box-shadow: var(--shadow-hover, 0 4px 18px rgba(0,0,0,0.06));
  transform: translateY(-3px);
}
.review-card-icon-wrap {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}
.review-card-icon { font-size: 1.6rem; }
.review-card-title {
  font-weight: 600;
  font-size: 1rem;
  color: var(--text-heading, #444);
  margin-bottom: 6px;
}
.review-card-stat {
  font-size: 0.78rem;
  color: var(--text-muted, #999);
  margin-bottom: 4px;
}
.review-card-stat b {
  font-size: 1rem;
  color: var(--primary, #3D5A80);
}
.review-card-hint {
  font-size: 0.72rem;
  color: var(--text-muted, #ccc);
  line-height: 1.3;
  margin-bottom: 12px;
}
.review-card-cta {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--primary, #3D5A80);
  padding: 4px 16px;
  border-radius: 8px;
  background: var(--primary-bg, var(--primary-bg));
  transition: all 0.15s;
}
.card.stat-card.review-card:hover .review-card-cta {
  background: var(--primary, #3D5A80);
  color: #fff;
}

/* ═══════════════════════════ 五、弹窗 ═══════════════════════════ */
.help-content { padding: 0 4px; }
.help-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 14px;
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--text-body, #444);
}
.help-num {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--primary, #3D5A80);
  color: white;
  font-size: 0.8rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
}
.help-note {
  text-align: center;
  font-size: 0.82rem;
  color: var(--text-muted, #bbb);
  margin-top: 16px;
}

/* ═══════════════════════════ 六、底部辅助区 ═══════════════════════════ */
.helper-section {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  padding: 18px 0 4px;
  border-top: 1px solid var(--border, #f0f0f0);
}
.helper-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.82rem;
  color: var(--text-muted, #ccc);
  cursor: pointer;
  padding: 4px 12px;
  border-radius: 6px;
  transition: all 0.15s;
}
.helper-item:hover { color: var(--primary, #3D5A80); background: var(--primary-bg, var(--bg-hover)); }
.helper-icon { font-size: 0.9rem; }
.helper-dot { color: var(--text-muted, #ddd); font-size: 0.9rem; padding: 0 4px; }

/* ═══════════════════════════ 响应式 ═══════════════════════════ */
@media (max-width: 768px) {
  .grid-3 { grid-template-columns: 1fr; }
  .hero-text-block .hero-desc { display: none; }
  .hero-tags { display: none; }
  .hero-action-block { padding: 8px 14px; }
  .hero-btn { font-size: 0.85rem; }
}
</style>