<template>
  <div class="interview-sim">
    <PageBanner fullwidth
      title="面试模拟"
      description="像真实面试一样练习表达，复盘弱项"
      :icon="'Mic'"
      variant="primary"
      cat-src="/src/assets/auth-cat.png"
      cat-alt="小橘面试官"
      :path-items="['选择岗位', '开始模拟', '复盘记录']"
    />

    <section class="interview-shell">
      <div class="stage-card start-stage" @click="$router.push('/interview/session')">
        <div class="stage-copy">
          <div class="stage-kicker"><Mic :size="16" class="icon-blue" /> 多模态模拟面试</div>
          <h2>选岗位、设模式，然后开始模拟面试</h2>
          <p>岗位、简历、语音、摄像头和复盘记录放在同一条练习线上，启途会先说明流程，再陪人一轮一轮练表达。</p>
          <div class="stage-tags">
            <span><Mic :size="16" class="icon-blue" /> 语音对话</span>
            <span><Camera :size="16" class="icon-blue" /> 摄像头录制</span>
            <span><BarChart :size="16" class="icon-blue" /> 表现评估</span>
          </div>
        </div>
        <div class="stage-visual" aria-hidden="true">
          <div class="screen-card interviewer-card">
            <span class="screen-dot"></span>
            <strong>AI 面试官</strong>
            <p>你好，我会先确认岗位和流程，再从基础问题开始。</p>
          </div>
          <img src="/src/assets/xiaoju-glasses.png" class="stage-cat" alt="小橘面试官">
        </div>
        <button class="start-button" @click.stop="$router.push('/interview/session')">
          开始面试 <ArrowRight :size="16" class="icon-blue" />
        </button>
      </div>

      <section class="interview-board">
        <div class="board-main">
          <div class="board-head">
            <span><Flame :size="16" class="icon-blue" /> 热门面经速览</span>
            <button class="refresh-link" @click="refreshExperiences"><RefreshCw :size="16" class="icon-blue" /> 换一批</button>
          </div>
          <div class="experience-rail">
            <button
              v-for="(exp, i) in displayedExperiences"
              :key="i"
              class="experience-row"
              @click="openExperience(exp)"
            >
              <span class="exp-index">0{{ i + 1 }}</span>
              <span class="exp-company" :style="{ color: exp.tagColor }">{{ exp.tag }}</span>
              <span class="exp-title">{{ exp.title }}</span>
              <ChevronRight :size="16" class="icon-blue" />
            </button>
          </div>
        </div>

        <aside class="review-panel">
          <div class="review-panel-title"><History :size="16" class="icon-blue" /> 复盘工具</div>
          <button class="review-link primary" @click="$router.push('/interview/history')">
            <span>
              <b>面试历史记录</b>
              <small>已完成 {{ stats.total_interview_sessions }} 次模拟</small>
            </span>
            <ArrowRight :size="16" class="icon-blue" />
          </button>
          <button class="review-link" @click="$router.push('/interview/wrong-questions')">
            <span>
              <b>全部错题回顾</b>
              <small>{{ interviewWrongTotal }} 道待回顾</small>
            </span>
            <ArrowRight :size="16" class="icon-blue" />
          </button>
          <button class="review-link" @click="$router.push('/interview/saved-questions')">
            <span>
              <b>我的收藏</b>
              <small>{{ interviewSavedTotal }} 道已收藏</small>
            </span>
            <ArrowRight :size="16" class="icon-blue" />
          </button>
        </aside>
      </section>

    <!-- ═══ 品牌 Footer ═══ -->
    <div class="brand-footer">
      <div>启途 · <span class="qitu-up">QITU</span></div>
      <div class="qitu-slogan">向上生长，自有答案</div>
    </div>
    </section>

    <el-dialog v-model="showHelp" width="480px" destroy-on-close>
      <template #title>
        <CircleHelp :size="16" class="icon-blue" /> 使用帮助
      </template>
      <div class="help-content">
        <div class="help-item"><span class="help-num">1</span><span>点击「开始面试」进入岗位选择和模式设置。</span></div>
        <div class="help-item"><span class="help-num">2</span><span>选择岗位后，可上传简历让问题更贴合个人经历。</span></div>
        <div class="help-item"><span class="help-num">3</span><span>支持语音回答和文字输入，结束后生成评估报告。</span></div>
        <div class="help-item"><span class="help-num">4</span><span>历史记录、错题和收藏会沉淀到复盘工具里。</span></div>
        <div class="help-note">启途陪人把每次练习都变成下一次的底气。</div>
      </div>
    </el-dialog>

    <el-dialog v-model="showFeedback" width="480px" destroy-on-close>
      <template #title>
        <MessageSquare :size="16" class="icon-blue" /> 意见反馈
      </template>
      <div class="feedback-content">
        <el-input v-model="feedbackText" type="textarea" :rows="5" placeholder="请描述你的建议或遇到的问题..." />
        <div class="feedback-actions">
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
.interview-sim {
  padding: 0 0 46px;
  color: var(--text-body);
}
.interview-shell {
  width: calc(100vw - var(--sidebar-width) - 40px);
  max-width: 1500px;
  margin: 24px auto 0;
}
.stage-card {
  position: relative;
  min-height: 280px;
  display: grid;
  grid-template-columns: minmax(0, 1.18fr) 430px;
  gap: 36px;
  padding: 26px 40px 20px;
  border-radius: 26px 26px 12px 26px;
  background:
    linear-gradient(135deg, rgba(239,246,255,.98), rgba(255,255,255,.96) 58%),
    radial-gradient(circle at 82% 12%, rgba(37,99,235,.16), transparent 32%);
  border: 1.5px dashed #93C5FD;
  box-shadow: 0 20px 48px rgba(37,99,235,.08);
  cursor: pointer;
  margin-bottom: 24px;
}
.stage-card .start-button {
  position: absolute;
  right: 42px;
  bottom: 34px;
  z-index: 5;
}
.stage-card::after {
  content: '';
  position: absolute;
  right: 0;
  bottom: 0;
  width: 78px;
  height: 78px;
  background: linear-gradient(135deg, rgba(191,219,254,.9), #fff 58%);
  clip-path: polygon(100% 0, 0 100%, 100% 100%);
  border-left: 1px dashed #93C5FD;
}
.stage-copy {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  min-height: 250px;
}
.stage-kicker,
.strip-title,
.board-head,
.review-panel-title {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--primary);
  font-size: 15px;
  font-weight: 900;
  letter-spacing: .04em;
}
.stage-copy h2 {
  margin: 16px 0 12px;
  max-width: 560px;
  color: var(--text-heading);
  font-size: 36px;
  line-height: 1.2;
  font-weight: 900;
  letter-spacing: .02em;
}
.stage-copy p {
  max-width: 560px;
  color: var(--text-light);
  font-size: 17px;
  line-height: 1.75;
}
.stage-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 24px;
}
.stage-tags span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 34px;
  padding: 0 14px;
  border-radius: 999px;
  background: #fff;
  color: var(--primary);
  border: 1px solid #BFDBFE;
  box-shadow: 6px 6px 14px rgba(147,197,253,.18), -6px -6px 14px rgba(255,255,255,.9);
  font-size: 14px;
  font-weight: 800;
}
.stage-visual {
  position: relative;
  min-height: 240px;
  z-index: 2;
}
.screen-card {
  position: absolute;
  top: 18px;
  right: 26px;
  width: 230px;
  padding: 18px 18px 16px;
  border-radius: 18px;
  background: #fff;
  border: 1.5px dashed #93C5FD;
  box-shadow: 0 18px 36px rgba(37,99,235,.12);
}
.screen-dot {
  display: none;
}
.screen-card strong {
  display: block;
  color: var(--primary);
  font-size: 20px;
  font-weight: 900;
}
.screen-card p {
  margin-top: 8px;
  color: var(--text-light);
  font-size: 14px;
  line-height: 1.5;
}
.stage-cat {
  position: absolute;
  right: 208px;
  bottom: -10px;
  width: 116px;
  filter: drop-shadow(0 10px 18px rgba(37,99,235,.16));
  transform: rotate(-3deg);
}
.start-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 46px;
  padding: 0 24px;
  border: 0;
  border-radius: 16px;
  background: linear-gradient(145deg, #0EA5E9, #2563EB);
  color: #fff;
  font: inherit;
  font-size: 17px;
  font-weight: 900;
  box-shadow: 10px 10px 22px rgba(37,99,235,.20), -8px -8px 18px rgba(255,255,255,.85);
  cursor: pointer;
}
.start-button .icon-blue { color: #fff !important; stroke: #fff !important; }
.stage-card:hover .start-button { transform: translateX(4px); }
.interview-board {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 340px;
  gap: 24px;
  align-items: stretch;
}
.board-main,
.review-panel {
  min-height: 258px;
  background: #fff;
  border: 1.5px dashed #BFDBFE;
  border-radius: 22px;
  padding: 22px;
}
.board-head {
  justify-content: space-between;
  width: 100%;
  margin-bottom: 16px;
}
.refresh-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--text-light);
  font-size: 14px;
}
.experience-rail {
  display: flex;
  flex-direction: column;
  gap: 0;
}
.experience-row {
  display: grid;
  grid-template-columns: 42px 86px minmax(0, 1fr) 22px;
  align-items: center;
  gap: 12px;
  width: 100%;
  min-height: 58px;
  border: 0;
  border-top: 1px dashed #DBEAFE;
  background: transparent;
  color: inherit;
  text-align: left;
  font: inherit;
  cursor: pointer;
}
.experience-row:first-child { border-top: 0; }
.experience-row:hover { background: linear-gradient(90deg, rgba(239,246,255,.9), transparent); }
.exp-index {
  color: #BFDBFE;
  font-size: 24px;
  font-weight: 900;
}
.exp-company {
  font-size: 14px;
  font-weight: 900;
}
.exp-title {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--text-heading);
  font-size: 16px;
  font-weight: 800;
}
.review-panel {
  position: sticky;
  top: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: linear-gradient(180deg, #fff, #F8FBFF);
}
.review-panel-title { margin-bottom: 4px; }
.review-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  width: 100%;
  padding: 16px;
  border-radius: 16px;
  border: 1px solid #DBEAFE;
  background: #fff;
  text-align: left;
  font: inherit;
  cursor: pointer;
}
.review-link.primary {
  background: var(--primary-light);
  border-color: #BFDBFE;
}
.review-link b {
  display: block;
  color: var(--text-heading);
  font-size: 17px;
  font-weight: 900;
}
.review-link small {
  display: block;
  margin-top: 2px;
  color: var(--text-light);
  font-size: 13px;
}
/* ═══ 品牌 Footer ═══ */
.brand-footer {
  text-align: center;
  padding: 32px 0 24px;
  color: #94A3B8;
  font-size: 13px;
  letter-spacing: 1px;
}
.brand-footer .qitu-up {
  color: #2563EB;
  font-weight: 800;
}
.brand-footer .qitu-slogan {
  margin-top: 4px;
  font-size: 11px;
  color: #BFDBFE;
}
.help-content { padding: 0 4px; }
.help-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 14px;
  font-size: 15px;
  line-height: 1.6;
  color: var(--text-body);
}
.help-num {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--primary);
  color: white;
  font-size: 13px;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
}
.help-note {
  text-align: center;
  font-size: 14px;
  color: var(--primary);
  margin-top: 16px;
  font-weight: 900;
}
.feedback-actions {
  margin-top: 16px;
  text-align: right;
}
@media (max-width: 1080px) {
  .interview-shell { width: calc(100vw - var(--sidebar-width) - 28px); }
  .stage-card { grid-template-columns: 1fr; }
  .stage-visual { display: none; }
  .interview-board { grid-template-columns: 1fr; }
  .review-panel { position: static; }
}
@media (max-width: 760px) {
  .interview-shell { width: calc(100vw - 28px); margin-top: 22px; }
  .stage-card { padding: 18px 18px 20px; }
  .stage-copy { min-height: 240px; }
  .stage-copy h2 { font-size: 28px; }
  .experience-row { grid-template-columns: 38px minmax(0, 1fr) 20px; }
  .exp-company { display: none; }
}
</style>
