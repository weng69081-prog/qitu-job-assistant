<template>
  <div class="session-page">
    <!-- ═══════ 顶部栏 ═══════ -->
    <div class="session-topbar">
      <el-button text @click="backToEntry"><i class="fa-solid fa-arrow-left"></i> 返回面试与笔试</el-button>
      <span class="session-title"><i class="fa-solid fa-video"></i> 对话式模拟面试</span>
      <div class="topbar-actions">
        <el-button v-if="phase === 'chatting'" size="small" type="danger" plain @click="handleEndInterview"><i class="fa-solid fa-stop"></i> 结束面试</el-button>
      </div>
    </div>

    <!-- ═══════ 阶段 1：设置（多步骤表单） ═══════ -->
    <div v-if="phase === 'setup'" class="section-panel">
      <el-card shadow="never" class="setup-card">
        <template #header>
          <span style="font-weight:600;font-size:1rem"><i class="fa-solid fa-gear"></i> 开始对话式面试</span>
          <span class="setup-step-indicator">步骤 {{ setupStep }} / 3</span>
        </template>

        <!-- Step 1: 岗位与类别 -->
        <div v-if="setupStep === 1">
          <el-form label-position="top">
            <el-form-item>
              <template #label><i class="fa-solid fa-crosshairs"></i> 目标岗位</template>
              <el-select v-model="career" placeholder="选择岗位" style="width:100%">
                <el-option-group v-if="store.validBookmarks.length">
                  <template #label><i class="fa-solid fa-star" style="color:var(--el-color-warning)"></i> 已收藏</template>
                  <el-option v-for="b in store.validBookmarks" :key="b.career" :label="b.career" :value="b.career" />
                </el-option-group>
                <el-option label="前端开发工程师" value="前端开发工程师" />
                <el-option label="后端开发工程师" value="后端开发工程师" />
                <el-option label="数据分析师" value="数据分析师" />
                <el-option label="产品经理" value="产品经理" />
                <el-option label="软件测试工程师" value="软件测试工程师" />
                <el-option label="UI设计师" value="UI设计师" />
                <el-option label="运营专员" value="运营专员" />
                <el-option label="市场营销" value="市场营销" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <template #label><i class="fa-regular fa-folder-open"></i> 面试分类</template>
              <el-select v-model="category" style="width:100%" placeholder="选择分类（默认同岗位）">
                <el-option label="同岗位名称" :value="career" />
                <el-option label="技术基础" value="技术基础" />
                <el-option label="项目经验" value="项目经验" />
                <el-option label="行为面试" value="行为面试" />
                <el-option label="综合面试" value="综合面试" />
              </el-select>
            </el-form-item>
          </el-form>
          <div class="setup-nav">
            <el-button type="primary" @click="setupStep = 2" :disabled="!career">下一步 <i class="fa-solid fa-arrow-right"></i></el-button>
          </div>
        </div>

        <!-- Step 2: 简历上传 -->
        <div v-if="setupStep === 2">
          <el-form label-position="top">
            <el-form-item>
              <template #label><i class="fa-regular fa-file"></i> 上传简历（可选 — 简历驱动模式下强烈推荐）</template>
              <div class="resume-upload-area">
                <input type="file" ref="resumeInput" accept=".pdf,.doc,.docx,.txt" style="display:none" @change="onResumeUpload" />
                <el-button size="small" @click="$refs.resumeInput.click()">
                  {{ resumeFileName ? '重新选择' : '选择文件' }}
                </el-button>
                <span v-if="resumeFileName" class="resume-file-name">{{ resumeFileName }}</span>
                <el-tag v-if="resumeFileName" type="success" size="small" effect="plain"><i class="fa-regular fa-check-circle"></i> 已上传</el-tag>
                <el-button v-if="resumeFileName" size="small" text type="danger" @click="clearResume">移除</el-button>
              </div>
            </el-form-item>
            <el-collapse v-if="resumeParsedText" style="margin-top:8px">
              <el-collapse-item name="preview">
              <template #title><i class="fa-solid fa-book-open"></i> 预览解析内容</template>
                <pre class="resume-preview">{{ resumeParsedText }}</pre>
              </el-collapse-item>
            </el-collapse>
            <div v-if="resumeUploading" class="resume-uploading">
              <el-progress :percentage="resumeUploadProgress" :stroke-width="6" />
              <span>正在上传并解析简历…</span>
            </div>
          </el-form>
          <div class="setup-nav">
            <el-button @click="setupStep = 1"><i class="fa-solid fa-arrow-left"></i> 上一步</el-button>
            <el-button type="primary" @click="setupStep = 3">下一步 <i class="fa-solid fa-arrow-right"></i></el-button>
          </div>
        </div>

        <!-- Step 3: 模式选择 + 开始 -->
        <div v-if="setupStep === 3">
          <el-form label-position="top">
            <el-form-item>
              <template #label><i class="fa-solid fa-gamepad"></i> 面试模式</template>
              <el-radio-group v-model="mode" class="mode-radio-group">
                <el-radio-button value="basic">
                  <div class="mode-option">
                    <span class="mode-icon"><i class="fa-regular fa-clipboard"></i></span>
                    <div>
                      <strong>基础模式</strong>
                      <p class="mode-desc">固定问题，覆盖常见面试题</p>
                    </div>
                  </div>
                </el-radio-button>
                <el-radio-button value="resume">
                  <div class="mode-option">
                    <span class="mode-icon"><i class="fa-regular fa-file"></i></span>
                    <div>
                      <strong>简历驱动</strong>
                      <p class="mode-desc">基于简历内容生成个性化问题</p>
                    </div>
                  </div>
                </el-radio-button>
                <el-radio-button value="stress">
                  <div class="mode-option">
                    <span class="mode-icon"><i class="fa-solid fa-fire"></i></span>
                    <div>
                      <strong>压力面试</strong>
                      <p class="mode-desc">挑战性追问，模拟高压场景</p>
                    </div>
                  </div>
                </el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-form-item>
              <template #label><i class="fa-regular fa-clock"></i> 面试时长</template>
              <el-select v-model="interviewDuration" style="width:200px">
                <el-option label="15 分钟" :value="15" />
                <el-option label="30 分钟" :value="30" />
                <el-option label="45 分钟" :value="45" />
                <el-option label="60 分钟" :value="60" />
              </el-select>
            </el-form-item>
          </el-form>
          <div class="setup-nav">
            <el-button @click="setupStep = 2"><i class="fa-solid fa-arrow-left"></i> 上一步</el-button>
            <el-button type="primary" size="large" @click="handleStartInterview" :loading="startLoading">
              <i class="fa-solid fa-play"></i> 开始面试
            </el-button>
          </div>
        </div>
      </el-card>
    </div>

    <!-- ═══════ 阶段 2：面试中 ═══════ -->
    <div v-if="phase === 'chatting' || phase === 'loading'" class="section-panel interview-phase">
      <!-- 顶部控制栏 -->
      <div class="interview-topbar">
        <div class="it-left">
          <el-tag :type="modeTagType" size="small" effect="dark">
            {{ modeLabel }}
          </el-tag>
          <span class="it-career">{{ career }}</span>
        </div>
        <div class="it-center">
          <div class="countdown-timer" :class="{ 'countdown-warning': remainingSeconds <= 120 }">
            <el-icon><Timer /></el-icon>
            <span>{{ formattedTime }}</span>
          </div>
          <el-button size="small" :icon="paused ? 'VideoPlay' : 'VideoPause'" circle @click="togglePause" :title="paused ? '继续' : '暂停'" />
          <el-button size="small" icon="Right" circle @click="skipQuestion" :disabled="aiLoading" title="跳过本题" />
        </div>
        <div class="it-right">
          <span class="round-badge">第 {{ chatRound }} 轮</span>
          <el-button size="small" type="danger" @click="handleEndInterview"><i class="fa-solid fa-stop"></i> 结束面试</el-button>
        </div>
      </div>

      <div class="chat-layout">
        <!-- 左：对话区 -->
        <div class="chat-main">
          <div class="chat-messages" ref="chatRef">
            <div v-if="startLoading" class="chat-loading-msg">
              <p><i class="fa-solid fa-hourglass-half"></i> AI 面试官正在准备…</p>
            </div>
            <div v-for="(msg, i) in messages" :key="i"
                 :class="['chat-bubble', msg.role === 'assistant' ? 'ai' : 'user']">
              <div class="chat-avatar"><i :class="msg.role === 'assistant' ? 'fa-solid fa-robot' : 'fa-solid fa-user'"></i></div>
              <div class="chat-content">
                <div class="chat-text" v-html="msg.content"></div>
                <div v-if="msg.role === 'assistant'" class="chat-msg-actions">
                  <el-button text size="small" @click="speakText(msg.content)" :disabled="!speechSynthSupported" title="朗读">
                    <i class="fa-solid fa-volume-high"></i>
                  </el-button>
                </div>
              </div>
            </div>
            <div v-if="aiLoading" class="chat-bubble ai">
              <div class="chat-avatar"><i class="fa-solid fa-robot"></i></div>
              <div class="chat-content"><span class="typing-dots">思考中<span>.</span><span>.</span><span>.</span></span></div>
            </div>
          </div>

          <!-- 语音活动指示器 -->
          <div v-if="voiceActive" class="voice-indicator">
            <span class="voice-pulse"></span>
            <span>正在聆听…</span>
          </div>

          <div class="chat-input-bar">
            <div class="chat-input-row">
              <el-input
                v-model="userInput"
                type="textarea"
                :rows="2"
                placeholder="输入你的回答… 或点击🎤语音输入"
                :disabled="aiLoading || paused"
                @keydown.enter.exact.prevent="sendMessage"
              />
            </div>
            <div class="chat-input-actions">
              <div class="cia-left">
                <el-button
                  size="small"
                  :type="isRecording ? 'danger' : 'default'"
                  @click="toggleVoiceInput"
                  :disabled="aiLoading || !speechRecogSupported"
                  :title="isRecording ? '停止录音' : '语音输入'"
                >
                  <template v-if="isRecording"><i class="fa-solid fa-stop"></i> 停止</template>
                  <template v-else><i class="fa-solid fa-microphone"></i></template>
                </el-button>
                <el-button
                  size="small"
                  :type="autoSpeakEnabled ? 'primary' : 'default'"
                  @click="autoSpeakEnabled = !autoSpeakEnabled"
                  title="自动朗读AI回复"
                >
                  <i class="fa-solid fa-volume-high"></i> {{ autoSpeakEnabled ? '已开启' : '已关闭' }}
                </el-button>
              </div>
              <el-button
                type="primary"
                @click="sendMessage"
                :loading="aiLoading"
                :disabled="!userInput.trim() || paused"
              >
                发送
              </el-button>
            </div>
          </div>
        </div>

        <!-- 右：摄像头 + 录制控制 -->
        <div class="chat-sidebar">
          <!-- 摄像头区域 -->
          <div class="camera-card">
            <div class="camera-header">
              <span><i class="fa-solid fa-camera"></i> 实时画面</span>
              <div class="camera-controls">
                <el-switch
                  v-model="cameraOn"
                  :loading="cameraToggling"
                  size="small"
                  active-text="开"
                  inactive-text="关"
                  @change="toggleCamera"
                />
              </div>
            </div>
            <div class="camera-wrapper" v-if="cameraOn && cameraReady">
              <video ref="videoRef" autoplay muted playsinline class="user-video"></video>
              <div class="emotion-overlay" v-if="currentEmotion">
                <div class="emotion-badge" :class="'emo-' + currentEmotion.emotion">
                  {{ currentEmotion.emotion }} {{ currentEmotion.confidence }}%
                </div>
              </div>
              <!-- 录制状态覆盖 -->
              <div v-if="isRecordingVideo" class="recording-badge">
                <span class="rec-dot"></span> REC {{ recordingDuration }}
              </div>
            </div>
            <div class="camera-placeholder" v-else>
              <div class="camera-placeholder-icon"><i class="fa-solid fa-camera"></i></div>
              <p class="camera-placeholder-text">摄像头未开启</p>
              <p class="camera-placeholder-sub">AI 会分析你的表情</p>
            </div>
            <div class="emotion-details" v-if="currentEmotion?.details">
              <div v-for="(val, key) in currentEmotion.details" :key="key" class="ed-row">
                <span class="ed-label">{{ key }}</span>
                <div class="ed-bar-track"><div class="ed-bar-fill" :style="{ width: val + '%', background: edBarColor(key, val) }"></div></div>
                <span class="ed-val">{{ val }}%</span>
              </div>
            </div>
          </div>

          <!-- 录制控制区 -->
          <div class="recording-controls">
            <div class="recording-header">
              <span><i class="fa-solid fa-film"></i> 录制控制</span>
            </div>
            <div class="recording-buttons">
              <div class="rec-btn-group">
                <el-button
                  size="small"
                  :type="micOn ? 'primary' : 'default'"
                  @click="toggleMic"
                  :disabled="!cameraOn"
                  title="麦克风开关"
                >
                  <template v-if="micOn"><i class="fa-solid fa-microphone"></i> 麦克风开</template>
                  <template v-else><i class="fa-solid fa-volume-xmark"></i> 麦克风关</template>
                </el-button>
                <el-button
                  size="small"
                  :type="isRecordingVideo ? 'danger' : 'success'"
                  @click="toggleRecording"
                  :disabled="!cameraOn || !micOn"
                >
                  <template v-if="isRecordingVideo"><i class="fa-solid fa-stop"></i> 停止录制</template>
                  <template v-else><i class="fa-solid fa-circle"></i> 开始录制</template>
                </el-button>
              </div>
            </div>
          </div>

          <!-- 关键词提示（简历驱动模式） -->
          <div v-if="mode === 'resume' && currentKeywords.length" class="keyword-hints">
            <div class="keyword-header"><i class="fa-solid fa-lightbulb"></i> 关键词提示</div>
            <div class="keyword-tags">
              <el-tag
                v-for="(kw, i) in currentKeywords"
                :key="i"
                size="small"
                :type="kw.type || 'info'"
                effect="plain"
                class="kw-tag"
              >
                {{ kw.text }}
              </el-tag>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════ 阶段 3：报告 ═══════ -->
    <div v-if="phase === 'report'" class="section-panel">
      <div v-if="reportLoading" class="report-loading">
        <el-progress type="circle" :percentage="reportLoadProgress" :width="100" status="warning" />
        <p class="report-loading-text"><i class="fa-solid fa-robot"></i> AI 正在分析你的面试表现…</p>
      </div>
      <el-card v-else shadow="never" class="report-card">
        <template #header>
          <span style="font-weight:600"><i class="fa-solid fa-chart-simple"></i> 面试评估报告</span>
          <el-button text size="small" @click="goToHistory" style="float:right"><i class="fa-regular fa-clipboard"></i> 查看面试记录</el-button>
        </template>
        <div class="report-top-info">
          <span class="report-job">{{ career }}</span>
          <el-tag :type="modeTagType" size="small" effect="dark">{{ modeLabel }}</el-tag>
          <span class="report-rounds">共 {{ messages.filter(m => m.role === 'assistant').length }} 轮对话</span>
        </div>
        <div class="report-summary" v-if="report.summary">{{ report.summary }}</div>
        <div class="overall-score-area">
          <el-progress type="circle" :percentage="report.overall_score || 0" :width="130" :color="scoreColor(report.overall_score || 0)" />
          <h3>综合得分 {{ report.overall_score || 0 }}</h3>
        </div>
        <div class="dimensions-grid" v-if="Object.keys(report.dimensions).length">
          <div v-for="(v, k) in report.dimensions" :key="k" class="dim-card">
            <div class="dim-header"><span>{{ k }}</span><b :style="{color:scoreColor(v.score||0)}">{{ v.score || 0 }}</b></div>
            <el-progress :percentage="v.score || 0" :stroke-width="8" :color="scoreColor(v.score || 0)" />
            <p class="dim-comment">{{ v.comment || '' }}</p>
          </div>
        </div>
        <el-divider />
        <div class="report-lists" v-if="report.strengths?.length">
          <h3><i class="fa-regular fa-check-circle" style="color:var(--el-color-success)"></i> 优点</h3>
          <ul><li v-for="s in report.strengths" :key="s">{{ s }}</li></ul>
        </div>
        <div class="report-lists" v-if="report.weaknesses?.length">
          <h3><i class="fa-solid fa-triangle-exclamation" style="color:var(--el-color-warning)"></i> 待改进</h3>
          <ul><li v-for="w in report.weaknesses" :key="w">{{ w }}</li></ul>
        </div>
        <div class="report-lists" v-if="report.suggestions?.length">
          <h3><i class="fa-solid fa-lightbulb" style="color:var(--el-color-primary)"></i> 建议</h3>
          <ul><li v-for="s in report.suggestions" :key="s">{{ s }}</li></ul>
        </div>
        <div class="report-actions">
          <el-button @click="resetToSetup"><i class="fa-solid fa-rotate"></i> 再来一次</el-button>
          <el-button type="primary" @click="goToHistory"><i class="fa-solid fa-chart-simple"></i> 查看面试记录</el-button>
          <el-button v-if="report.sessionId" text type="info" @click="goToDetail(report.sessionId)"><i class="fa-regular fa-file"></i> 查看完整报告</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Timer } from '@element-plus/icons-vue'
import axios from 'axios'
import { useCareerStore } from '../stores/career'

const store = useCareerStore()
const $router = useRouter()

// ==================== API Base ====================
const API = 'http://localhost:8000/api'

// ==================== Setup State ====================
const career = ref('')
const category = ref('')
const mode = ref('basic')
const setupStep = ref(1)
const interviewDuration = ref(30) // minutes
const resumeInput = ref(null)
const resumeFileName = ref('')
const resumeContent = ref('')
const resumeParsedText = ref('')
const resumeFileId = ref('')
const resumeUploading = ref(false)
const resumeUploadProgress = ref(0)

function clearResume() {
  resumeFileName.value = ''
  resumeContent.value = ''
  resumeParsedText.value = ''
  resumeFileId.value = ''
  if (resumeInput.value) resumeInput.value.value = ''
}

async function onResumeUpload(e) {
  const f = e.target.files?.[0]
  if (!f) return
  resumeFileName.value = f.name
  resumeContent.value = f

  // Try reading as text for preview
  if (f.type === 'text/plain') {
    const reader = new FileReader()
    reader.onload = ev => { resumeParsedText.value = ev.target?.result || '' }
    reader.readAsText(f)
  }

  // Upload to backend
  resumeUploading.value = true
  resumeUploadProgress.value = 10
  try {
    const formData = new FormData()
    formData.append('file', f)
    const { data } = await axios.post(`${API}/interview/upload-resume`, formData, {
      onUploadProgress: (pe) => {
        resumeUploadProgress.value = Math.round((pe.loaded / pe.total) * 80) + 10
      }
    })
    resumeUploadProgress.value = 100
    resumeFileId.value = data.file_id
    if (data.text) resumeParsedText.value = data.text
    ElMessage.success(`简历已上传并解析：${f.name}`)
  } catch (err) {
    ElMessage.error('简历上传失败，可跳过此步')
    resumeParsedText.value = resumeParsedText.value || '（解析失败，无法预览全文）'
  }
  resumeUploading.value = false
}

// ==================== Phase & Session ====================
const phase = ref('setup') // setup | chatting | loading | report
const startLoading = ref(false)
const sessionId = ref('')
const messages = ref([])
const userInput = ref('')
const aiLoading = ref(false)
const chatRound = ref(0)
const chatRef = ref(null)
const paused = ref(false)
const report = reactive({
  overall_score: 0,
  dimensions: {},
  strengths: [],
  weaknesses: [],
  suggestions: [],
  summary: '',
  sessionId: ''
})
const reportLoading = ref(false)
const reportLoadProgress = ref(0)

// ==================== Countdown Timer ====================
const remainingSeconds = ref(0)
let countdownInterval = null

const formattedTime = computed(() => {
  const m = Math.floor(remainingSeconds.value / 60)
  const s = remainingSeconds.value % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
})

function startCountdown() {
  remainingSeconds.value = interviewDuration.value * 60
  countdownInterval = setInterval(() => {
    if (paused.value) return
    if (remainingSeconds.value > 0) {
      remainingSeconds.value--
    } else {
      // Time's up — auto-end interview
      ElMessage.warning('⏰ 面试时间到！')
      handleEndInterview()
    }
  }, 1000)
}

function stopCountdown() {
  if (countdownInterval) {
    clearInterval(countdownInterval)
    countdownInterval = null
  }
}

function togglePause() {
  paused.value = !paused.value
  ElMessage.info(paused.value ? '⏸️ 面试已暂停' : '▶️ 面试继续')
}

// ==================== Camera ====================
const videoRef = ref(null)
const cameraOn = ref(false)
const cameraReady = ref(false)
const cameraToggling = ref(false)
let cameraStream = null
const currentEmotion = ref(null)
const allExpressions = ref([])
let captureTimer = null
let captureCanvas = null

async function toggleCamera(val) {
  cameraToggling.value = true
  try {
    if (val) {
      await startCamera()
    } else {
      stopCamera()
    }
  } catch (err) {
    ElMessage.warning('摄像头操作失败')
    cameraOn.value = false
  }
  cameraToggling.value = false
}

async function startCamera() {
  try {
    cameraStream = await navigator.mediaDevices.getUserMedia({
      video: { width: 320, height: 240, facingMode: 'user' },
      audio: true
    })
    if (videoRef.value) {
      videoRef.value.srcObject = cameraStream
      cameraReady.value = true
    }
    cameraOn.value = true
    // Start emotion capture
    captureTimer = setInterval(captureAndAnalyze, 10000)
  } catch (err) {
    ElMessage.warning('无法开启摄像头：' + (err.message || '权限被拒绝'))
    throw err
  }
}

function stopCamera() {
  if (captureTimer) {
    clearInterval(captureTimer)
    captureTimer = null
  }
  if (cameraStream) {
    cameraStream.getTracks().forEach(t => t.stop())
    cameraStream = null
  }
  cameraOn.value = false
  cameraReady.value = false
  currentEmotion.value = null
}

async function captureAndAnalyze() {
  if (!videoRef.value || !cameraOn.value) return
  try {
    if (!captureCanvas) captureCanvas = document.createElement('canvas')
    captureCanvas.width = 320
    captureCanvas.height = 240
    const ctx = captureCanvas.getContext('2d')
    ctx.drawImage(videoRef.value, 0, 0, 320, 240)
    const base64 = captureCanvas.toDataURL('image/jpeg', 0.7).split(',')[1]
    const { data } = await axios.post(`${API}/interview/analyze-expression`, { image: base64 })
    currentEmotion.value = data
    allExpressions.value.push({ ...data, time: Date.now(), round: chatRound.value })
  } catch { /* silent */ }
}

// ==================== Microphone + Recording ====================
const micOn = ref(false)
let micStream = null

async function toggleMic() {
  if (micOn.value) {
    if (micStream) {
      micStream.getAudioTracks().forEach(t => t.stop())
      micStream = null
    }
    micOn.value = false
    return
  }
  try {
    micStream = await navigator.mediaDevices.getUserMedia({ audio: true })
    micOn.value = true
    ElMessage.success('🎙️ 麦克风已开启')
  } catch {
    ElMessage.warning('无法开启麦克风')
  }
}

// ==================== Video Recording ====================
const isRecordingVideo = ref(false)
const recordingDuration = ref('00:00')
let mediaRecorder = null
let recordedChunks = []
let recordingTimer = null
let recordingStartTime = 0

async function toggleRecording() {
  if (isRecordingVideo.value) {
    stopRecording()
  } else {
    startRecording()
  }
}

async function startRecording() {
  if (!cameraStream) {
    ElMessage.warning('请先开启摄像头')
    return
  }
  if (!micOn.value) {
    ElMessage.warning('请先开启麦克风')
    return
  }
  try {
    // Create combined stream from camera (already includes audio if available)
    recordedChunks = []
    const combinedStream = cameraStream // cameraStream already has audio from getUserMedia

    // Check if we need to add microphone audio separately
    const audioTracks = cameraStream.getAudioTracks()
    if (!audioTracks.length && micStream) {
      // If camera stream has no audio, try to combine
      const tracks = [...cameraStream.getVideoTracks(), ...micStream.getAudioTracks()]
      combinedStream = new MediaStream(tracks)
    }

    const mimeType = MediaRecorder.isTypeSupported('video/webm;codecs=vp9,opus')
      ? 'video/webm;codecs=vp9,opus'
      : MediaRecorder.isTypeSupported('video/webm;codecs=vp8,opus')
        ? 'video/webm;codecs=vp8,opus'
        : 'video/webm'

    mediaRecorder = new MediaRecorder(combinedStream, { mimeType })

    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) recordedChunks.push(e.data)
    }

    mediaRecorder.onstop = async () => {
      await uploadRecording()
    }

    mediaRecorder.onerror = () => {
      ElMessage.error('录制出错')
      isRecordingVideo.value = false
    }

    mediaRecorder.start(1000) // collect data every second
    isRecordingVideo.value = true
    recordingStartTime = Date.now()

    // Start timer
    recordingTimer = setInterval(() => {
      const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000)
      const m = String(Math.floor(elapsed / 60)).padStart(2, '0')
      const s = String(elapsed % 60).padStart(2, '0')
      recordingDuration.value = `${m}:${s}`
    }, 1000)

    ElMessage.success('⏺️ 开始录制')
  } catch (err) {
    ElMessage.error('启动录制失败：' + (err.message || '未知错误'))
  }
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop()
  }
  isRecordingVideo.value = false
  if (recordingTimer) {
    clearInterval(recordingTimer)
    recordingTimer = null
  }
}

async function uploadRecording() {
  if (!recordedChunks.length || !sessionId.value) {
    recordedChunks = []
    return
  }
  try {
    const blob = new Blob(recordedChunks, { type: 'video/webm' })
    const formData = new FormData()
    formData.append('file', blob, `interview_${sessionId.value}_${Date.now()}.webm`)
    formData.append('session_id', sessionId.value)
    await axios.post(`${API}/interview/upload-recording`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    ElMessage.success('✅ 录制已上传')
  } catch {
    ElMessage.warning('录制上传失败')
  }
  recordedChunks = []
}

// ==================== Voice Input (SpeechRecognition) ====================
const isRecording = ref(false)
const voiceActive = ref(false)
let recognition = null
const speechRecogSupported = computed(() => {
  return !!(window.SpeechRecognition || window.webkitSpeechRecognition)
})

function toggleVoiceInput() {
  if (isRecording.value) {
    stopVoiceInput()
  } else {
    startVoiceInput()
  }
}

function startVoiceInput() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition
  if (!SR) {
    ElMessage.warning('当前浏览器不支持语音输入')
    return
  }
  if (isRecording.value) return

  recognition = new SR()
  recognition.lang = 'zh-CN'
  recognition.interimResults = true
  recognition.continuous = true

  isRecording.value = true
  voiceActive.value = true

  recognition.onresult = (e) => {
    let transcript = ''
    for (let i = e.resultIndex; i < e.results.length; i++) {
      transcript += e.results[i][0].transcript
    }
    userInput.value += transcript
  }

  recognition.onerror = (evt) => {
    console.warn('SpeechRecognition error:', evt.error)
    if (evt.error === 'not-allowed') {
      ElMessage.warning('麦克风权限被拒绝，请使用文字输入')
    }
    isRecording.value = false
    voiceActive.value = false
  }

  recognition.onend = () => {
    isRecording.value = false
    voiceActive.value = false
  }

  try {
    recognition.start()
  } catch {
    isRecording.value = false
    voiceActive.value = false
    ElMessage.warning('语音输入启动失败')
  }
}

function stopVoiceInput() {
  if (recognition) {
    try { recognition.stop() } catch { /* ignore */ }
    recognition = null
  }
  isRecording.value = false
  voiceActive.value = false
}

// ==================== SpeechSynthesis (TTS) ====================
const autoSpeakEnabled = ref(true)
const speechSynthSupported = computed(() => {
  return !!window.speechSynthesis
})

function speakText(text) {
  if (!window.speechSynthesis) return
  // Clean HTML tags from text
  const cleanText = text.replace(/<[^>]*>/g, '')
  // Split into smaller chunks for better handling
  const maxLen = 200
  if (cleanText.length <= maxLen) {
    const utterance = new SpeechSynthesisUtterance(cleanText)
    utterance.lang = 'zh-CN'
    utterance.rate = 1.0
    utterance.pitch = 1.0
    window.speechSynthesis.speak(utterance)
  } else {
    // Speak in chunks
    const chunks = []
    for (let i = 0; i < cleanText.length; i += maxLen) {
      chunks.push(cleanText.slice(i, i + maxLen))
    }
    let idx = 0
    function speakNext() {
      if (idx >= chunks.length) return
      const u = new SpeechSynthesisUtterance(chunks[idx])
      u.lang = 'zh-CN'
      u.rate = 1.0
      u.pitch = 1.0
      u.onend = () => { idx++; speakNext() }
      window.speechSynthesis.speak(u)
    }
    speakNext()
  }
}

// ==================== Resume-driven keywords ====================
const currentKeywords = ref([])
const resumeQuestions = ref([])
let resumeQuestionIndex = 0

// ==================== Computed ====================
const modeLabel = computed(() => {
  const map = { basic: '基础模式', resume: '简历驱动', stress: '压力面试' }
  return map[mode.value] || mode.value
})
const modeTagType = computed(() => {
  const map = { basic: 'primary', resume: 'success', stress: 'danger' }
  return map[mode.value] || 'info'
})

function scoreColor(v) {
  return v >= 80 ? '#67c23a' : v >= 60 ? '#e6a23c' : '#f56c6c'
}

function emotionTagType(e) {
  const m = { '开心': 'success', '自信': 'success', '平静': 'info', '困惑': 'warning', '紧张': 'danger', '焦虑': 'danger' }
  return m[e] || 'info'
}

function edBarColor(k, v) {
  if (['开心', '自信', '平静'].includes(k)) return `rgba(103,194,58,${0.4 + v / 150})`
  return `rgba(245,108,108,${0.4 + v / 150})`
}

// ==================== Chat Core ====================
function scrollToBottom() {
  nextTick(() => {
    if (chatRef.value) {
      chatRef.value.scrollTop = chatRef.value.scrollHeight
    }
  })
}

function backToEntry() {
  cleanupAll()
  window.location.href = '/interview'
}

function goToHistory() {
  cleanupAll()
  $router.push('/interview/history')
}

function goToDetail(id) {
  cleanupAll()
  $router.push(`/interview/history/${id}`)
}

// ==================== Start Interview ====================
async function handleStartInterview() {
  if (!career.value) {
    ElMessage.warning('请先选择目标岗位')
    return
  }

  startLoading.value = true
  messages.value = []
  phase.value = 'chatting'
  chatRound.value = 0
  paused.value = false

  // If resume mode and we have a resume, fetch resume questions first
  if (mode.value === 'resume' && resumeParsedText.value) {
    try {
      const { data } = await axios.post(`${API}/interview/resume-questions`, {
        resume_text: resumeParsedText.value,
        count: 10
      })
      resumeQuestions.value = data.questions || []
      resumeQuestionIndex = 0
    } catch {
      ElMessage.warning('简历问题生成失败，将使用默认问题')
      resumeQuestions.value = []
    }
  }

  try {
    const { data } = await axios.post(`${API}/interview/chat/start`, {
      job: career.value,
      category: category.value || career.value,
      mode: mode.value
    })
    sessionId.value = data.session_id
    const firstMsg = data.message || `你好！欢迎参加${modeLabel.value}面试。请先简单介绍一下你自己。`
    messages.value.push({ role: 'assistant', content: firstMsg, time: Date.now() })

    // Auto-speak the first message
    if (autoSpeakEnabled.value) {
      speakText(firstMsg)
    }

    // Extract keywords from first message for resume mode
    updateKeywords(firstMsg)

    // Start camera automatically
    try {
      await startCamera()
      // Also open mic
      if (!micOn.value) await toggleMic()
    } catch { /* optional */ }

    // Start countdown
    startCountdown()

    scrollToBottom()
  } catch (err) {
    ElMessage.error('启动面试失败：' + (err.response?.data?.detail || err.message || '未知错误'))
    phase.value = 'setup'
  }
  startLoading.value = false
}

function updateKeywords(aiMsg) {
  if (mode.value !== 'resume') {
    currentKeywords.value = []
    return
  }
  // Extract meaningful keywords from AI message for hints
  const commonWords = ['的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '他', '她', '它', '们', '那', '什么', '怎么', '为什么', '请', '可以', '能', '吗', '吧', '呢', '啊']
  const words = aiMsg.split(/[\s,，。、；：！？?()（）\[\]【】""''"《》\n]+/).filter(w => w.length > 1 && !commonWords.includes(w))
  const uniqueWords = [...new Set(words)].slice(0, 6)
  currentKeywords.value = uniqueWords.map(w => ({
    text: w,
    type: 'info'
  }))

  // Also add resume-related keywords if available
  if (resumeParsedText.value) {
    const resumeWords = resumeParsedText.value.split(/[\s,，。、；：\n]+/).filter(w => w.length > 1 && w.length <= 10)
    const resumeKeywords = resumeWords.filter(w => !commonWords.includes(w))
    const selectedResume = [...new Set(resumeKeywords)].slice(0, 4)
    selectedResume.forEach(w => {
      if (!currentKeywords.value.find(k => k.text === w)) {
        currentKeywords.value.push({ text: w, type: 'success' })
      }
    })
    // Limit total
    if (currentKeywords.value.length > 10) {
      currentKeywords.value = currentKeywords.value.slice(0, 10)
    }
  }
}

// ==================== Send Message ====================
async function sendMessage() {
  const msg = userInput.value.trim()
  if (!msg || aiLoading.value || !sessionId.value || paused.value) return

  userInput.value = ''
  messages.value.push({ role: 'user', content: msg, time: Date.now() })
  aiLoading.value = true
  scrollToBottom()

  try {
    // For resume mode, if we have pre-generated questions, use them
    if (mode.value === 'resume' && resumeQuestions.value.length > 0 && resumeQuestionIndex < resumeQuestions.value.length) {
      // Normal chat but the AI handles it
    }

    const { data } = await axios.post(`${API}/interview/chat`, {
      session_id: sessionId.value,
      message: msg
    })

    if (data.error) {
      ElMessage.error(data.error)
      aiLoading.value = false
      return
    }

    const aiMsg = data.message || '好的，让我们继续。'
    messages.value.push({ role: 'assistant', content: aiMsg, time: Date.now() })
    chatRound.value = data.round || chatRound.value + 1

    // Auto-speak
    if (autoSpeakEnabled.value) {
      speakText(aiMsg)
    }

    // Update keyword hints
    updateKeywords(aiMsg)
  } catch (err) {
    ElMessage.error('发送失败，请重试')
  }
  aiLoading.value = false
  scrollToBottom()
}

// ==================== Skip Question ====================
async function skipQuestion() {
  if (aiLoading.value || !sessionId.value) return
  aiLoading.value = true
  try {
    const { data } = await axios.post(`${API}/interview/chat`, {
      session_id: sessionId.value,
      message: '跳过本题，请换一个问题'
    })
    if (data.error) {
      ElMessage.error(data.error)
      aiLoading.value = false
      return
    }
    const aiMsg = data.message || '好的，我们换一个问题。'
    messages.value.push({ role: 'assistant', content: aiMsg, time: Date.now() })
    chatRound.value = data.round || chatRound.value + 1
    if (autoSpeakEnabled.value) speakText(aiMsg)
    updateKeywords(aiMsg)
  } catch {
    ElMessage.error('操作失败')
  }
  aiLoading.value = false
  scrollToBottom()
}

// ==================== End Interview ====================
async function handleEndInterview() {
  if (!sessionId.value) return

  try {
    await ElMessageBox.confirm('确定要结束当前面试吗？结束后将生成评估报告。', '确认结束', {
      confirmButtonText: '结束面试',
      cancelButtonText: '继续面试',
      type: 'warning'
    })
  } catch {
    return // cancelled
  }

  // Stop recording if active
  if (isRecordingVideo.value) {
    stopRecording()
  }

  stopCountdown()
  aiLoading.value = true
  phase.value = 'loading'
  reportLoading.value = true
  reportLoadProgress.value = 0

  // Progress animation
  const progressInterval = setInterval(() => {
    if (reportLoadProgress.value < 90) {
      reportLoadProgress.value += Math.random() * 8 + 2
    }
  }, 300)

  try {
    const { data } = await axios.post(`${API}/interview/chat/end`, {
      session_id: sessionId.value
    })

    clearInterval(progressInterval)
    reportLoadProgress.value = 100

    if (data.error) {
      ElMessage.error(data.error)
      aiLoading.value = false
      phase.value = 'chatting'
      reportLoading.value = false
      return
    }

    Object.assign(report, data)
    report.sessionId = sessionId.value
    stopCamera()
    stopVoiceInput()
    if (micOn.value) await toggleMic()

    // Save to database
    try {
      const scores = Object.values(data.dimensions || {}).map(d => d.score || 0)
      await axios.post(`${API}/interview/save-session`, {
        job: data.job || career.value,
        category: category.value || career.value,
        mode: mode.value,
        total_questions: data.total_questions || Math.floor(messages.value.filter(m => m.role === 'user').length),
        average_score: String(data.overall_score || 0),
        highest_score: String(Math.max(...scores, data.overall_score || 0)),
        lowest_score: String(Math.min(...scores, data.overall_score || 0)),
        answers_json: JSON.stringify(messages.value.map(m => ({ role: m.role, content: m.content }))),
        dimensions_json: JSON.stringify(data.dimensions || {}),
        strengths_json: JSON.stringify(data.strengths || []),
        weaknesses_json: JSON.stringify(data.weaknesses || []),
        suggestions_json: JSON.stringify(data.suggestions || [])
      })
    } catch { /* silent */ }

    // Small delay to show 100%
    await new Promise(r => setTimeout(r, 500))
    phase.value = 'report'
  } catch (err) {
    clearInterval(progressInterval)
    ElMessage.error('生成报告失败')
    phase.value = 'chatting'
  }
  aiLoading.value = false
  reportLoading.value = false
}

// ==================== Reset ====================
function resetToSetup() {
  cleanupAll()
  phase.value = 'setup'
  setupStep.value = 1
  messages.value = []
  sessionId.value = ''
  report.overall_score = 0
  report.dimensions = {}
  report.strengths = []
  report.weaknesses = []
  report.suggestions = []
  report.summary = ''
  report.sessionId = ''
  currentKeywords.value = []
  resumeQuestions.value = []
  resumeQuestionIndex = 0
}

// ==================== Cleanup ====================
function cleanupAll() {
  stopCamera()
  stopVoiceInput()
  stopCountdown()
  if (isRecordingVideo.value) stopRecording()
  if (micOn.value && micStream) {
    micStream.getAudioTracks().forEach(t => t.stop())
    micStream = null
    micOn.value = false
  }
  if (window.speechSynthesis) {
    window.speechSynthesis.cancel()
  }
}

onUnmounted(() => {
  cleanupAll()
})
</script>

<style scoped>
/* ==================== Global CSS Variables ==================== */
:root {
  --session-bg: var(--bg-body, #f5f6fa);
  --session-card-bg: var(--bg-card, #ffffff);
  --session-border: var(--border-light, #ebeef5);
  --session-text: var(--text-body, #333);
  --session-text-muted: var(--text-muted, #999);
  --session-shadow: var(--shadow-sm, 0 1px 4px rgba(0,0,0,0.06));
  --session-radius: var(--radius-md, 10px);
}

/* ==================== Full-width Layout ==================== */
.session-page {
  width: 100%;
  min-height: 100vh;
  padding: 0 2rem 2rem;
  background: var(--session-bg);
}
.session-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 0;
}
.session-title {
  font-weight: 600;
  font-size: 1rem;
  color: var(--text-heading, #333);
}
.session-title i {
  margin-right: 6px;
  color: var(--primary, #3D5A80);
}
.topbar-actions {
  display: flex;
  gap: 8px;
}
.section-panel {
  min-height: 200px;
}

/* ==================== Setup Card ==================== */
.setup-card {
  border-radius: var(--session-radius);
  max-width: 620px;
  margin: 0 auto;
  border: 1px solid var(--session-border);
}
.setup-card :deep(.el-card__header) {
  border-bottom: 1px solid var(--session-border);
  padding: 14px 20px;
}
.setup-step-indicator {
  float: right;
  font-size: 0.8rem;
  color: var(--session-text-muted);
  font-weight: 400;
}
.setup-nav {
  display: flex;
  justify-content: center;
  gap: 12px;
  padding-top: 1.2rem;
}
.resume-upload-area {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}
.resume-file-name {
  font-size: 0.85rem;
  color: var(--session-text);
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.resume-preview {
  font-size: 0.78rem;
  color: var(--text-body, #444);
  background: var(--bg-alt, #f8f9fa);
  padding: 0.8rem;
  border-radius: var(--radius-sm, 8px);
  max-height: 200px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
}
.resume-uploading {
  text-align: center;
  padding: 0.5rem 0;
  color: var(--session-text-muted);
  font-size: 0.85rem;
}
.mode-radio-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}
.mode-radio-group :deep(.el-radio-button) {
  width: 100%;
}
.mode-radio-group :deep(.el-radio-button__inner) {
  width: 100%;
  text-align: left;
  border-radius: var(--radius-sm, 8px) !important;
  padding: 12px 16px;
  height: auto;
  border-left: 1px solid var(--border, #dcdfe6);
}
.mode-option {
  display: flex;
  align-items: center;
  gap: 12px;
}
.mode-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
  width: 32px;
  text-align: center;
  color: var(--primary, #3D5A80);
}
.mode-desc {
  font-size: 0.75rem;
  color: var(--text-muted, #999);
  margin: 2px 0 0;
  font-weight: 400;
}

/* ==================== Interview Topbar ==================== */
.interview-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: var(--session-card-bg);
  border-radius: var(--session-radius);
  margin-bottom: 0.8rem;
  box-shadow: var(--session-shadow);
  gap: 12px;
  border: 1px solid var(--session-border);
}
.it-left {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}
.it-career {
  font-weight: 600;
  font-size: 0.85rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 120px;
}
.it-center {
  display: flex;
  align-items: center;
  gap: 8px;
}
.countdown-timer {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 1rem;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  color: var(--text-heading, #333);
  padding: 2px 10px;
  background: var(--bg-alt, #f5f5f5);
  border-radius: 6px;
}
.countdown-warning {
  color: #C85A20 !important;
  background: #fef0f0 !important;
  animation: pulse 1s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
.it-right {
  display: flex;
  align-items: center;
  gap: 8px;
}
.round-badge {
  font-size: 0.78rem;
  color: var(--session-text-muted);
  background: var(--bg-alt, #f5f5f5);
  padding: 2px 8px;
  border-radius: 10px;
}

/* ==================== Chat Layout ==================== */
.interview-phase {
  height: calc(100vh - 150px);
  display: flex;
  flex-direction: column;
}
.chat-layout {
  flex: 1;
  display: flex;
  gap: 16px;
  min-height: 0;
  overflow: hidden;
}
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--session-card-bg);
  border-radius: var(--session-radius);
  box-shadow: var(--shadow-md, 0 2px 12px rgba(0,0,0,0.06));
  overflow: hidden;
  border: 1px solid var(--session-border);
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}
.chat-loading-msg {
  text-align: center;
  padding: 3rem;
  color: var(--session-text-muted);
}
.chat-bubble {
  display: flex;
  gap: 10px;
  margin-bottom: 1rem;
  max-width: 85%;
}
.chat-bubble.user {
  flex-direction: row-reverse;
  margin-left: auto;
}
.chat-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  background: var(--bg-alt, #f0f0f0);
  flex-shrink: 0;
  color: var(--text-body, #555);
}
.chat-bubble.ai .chat-avatar {
  background: #ede8ff;
  color: var(--primary, #3D5A80);
}
.chat-bubble.user .chat-avatar {
  background: #e3f2fd;
  color: #3D5A80;
}
.chat-content {
  padding: 0.6rem 1rem;
  border-radius: 12px;
  font-size: 0.9rem;
  line-height: 1.7;
  position: relative;
}
.chat-bubble.ai .chat-content {
  background: #f5f3ff;
  color: var(--text-body, #333);
  border-top-left-radius: 2px;
}
.chat-bubble.user .chat-content {
  background: #3D5A80;
  color: white;
  border-top-right-radius: 2px;
}
.chat-msg-actions {
  margin-top: 4px;
  display: flex;
  gap: 4px;
}
.chat-msg-actions .el-button {
  font-size: 0.75rem;
  padding: 2px 6px;
  min-height: auto;
  color: var(--text-muted, #999);
}

/* Voice indicator */
.voice-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 6px;
  background: #fef0f0;
  color: #C85A20;
  font-size: 0.8rem;
  font-weight: 500;
}
.voice-pulse {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #C85A20;
  animation: voicePulse 1s infinite;
}
@keyframes voicePulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.4); opacity: 0.5; }
}

/* Input bar */
.chat-input-bar {
  border-top: 1px solid var(--session-border);
  padding: 0.6rem;
  background: var(--bg-alt, #fafbfc);
}
.chat-input-row {
  margin-bottom: 6px;
}
.chat-input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.cia-left {
  display: flex;
  gap: 6px;
}

/* Typing animation */
.typing-dots span {
  animation: dotPulse 1.2s infinite;
  opacity: 0;
}
.typing-dots span:nth-child(2) {
  animation-delay: 0.4s;
}
.typing-dots span:nth-child(3) {
  animation-delay: 0.8s;
}
@keyframes dotPulse {
  0%, 60%, 100% { opacity: 0; }
  30% { opacity: 1; }
}

/* ==================== Sidebar ==================== */
.chat-sidebar {
  flex: 0 0 300px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
}

/* Camera */
.camera-card {
  background: var(--session-card-bg);
  border-radius: var(--session-radius);
  overflow: hidden;
  box-shadow: var(--shadow-md, 0 2px 12px rgba(0,0,0,0.08));
  border: 1px solid var(--session-border);
}
.camera-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: var(--bg-alt, #f8f9fc);
  font-size: 0.8rem;
  font-weight: 600;
}
.camera-header i {
  margin-right: 6px;
  color: var(--primary, #3D5A80);
}
.camera-controls {
  display: flex;
  align-items: center;
  gap: 6px;
}
.camera-wrapper {
  position: relative;
  background: #000;
  aspect-ratio: 4/3;
  overflow: hidden;
}
.user-video {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}
.emotion-overlay {
  position: absolute;
  top: 6px;
  right: 6px;
}
.emotion-badge {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.72rem;
  font-weight: 700;
  backdrop-filter: blur(4px);
}
.recording-badge {
  position: absolute;
  top: 6px;
  left: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
  background: rgba(245, 108, 108, 0.85);
  color: white;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 700;
}
.rec-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #fff;
  animation: recPulse 1s infinite;
}
@keyframes recPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}
.camera-placeholder {
  background: var(--bg-alt, #f8f9fa);
  aspect-ratio: 4/3;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
}
.camera-placeholder-icon {
  font-size: 2.5rem;
  opacity: 0.5;
  color: var(--text-muted, #999);
}
.camera-placeholder-text {
  font-size: 0.85rem;
  color: var(--text-muted, #bbb);
}
.camera-placeholder-sub {
  font-size: 0.75rem;
  color: var(--text-muted, #bbb);
}
.emotion-details {
  padding: 8px 12px;
}
.ed-row {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 2px;
}
.ed-label {
  font-size: 0.7rem;
  color: var(--text-muted, #888);
  width: 28px;
  text-align: right;
  flex-shrink: 0;
}
.ed-bar-track {
  flex: 1;
  height: 5px;
  background: var(--bg-alt, #f0f0f0);
  border-radius: 3px;
}
.ed-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}
.ed-val {
  font-size: 0.65rem;
  color: var(--text-muted, #888);
  width: 26px;
  text-align: right;
}
.emo-开心, .emo-自信 {
  background: rgba(103, 194, 58, 0.8);
  color: white;
}
.emo-平静 {
  background: rgba(144, 147, 153, 0.7);
  color: white;
}
.emo-困惑 {
  background: rgba(230, 162, 60, 0.8);
  color: white;
}
.emo-紧张, .emo-焦虑, .emo-未知 {
  background: rgba(245, 108, 108, 0.85);
  color: white;
}

/* Recording controls */
.recording-controls {
  background: var(--session-card-bg);
  border-radius: var(--session-radius);
  padding: 10px 12px;
  box-shadow: var(--shadow-md, 0 2px 12px rgba(0,0,0,0.08));
  border: 1px solid var(--session-border);
}
.recording-header {
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 8px;
}
.recording-header i {
  margin-right: 6px;
  color: var(--primary, #3D5A80);
}
.recording-buttons {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.rec-btn-group {
  display: flex;
  gap: 6px;
}

/* Keyword hints */
.keyword-hints {
  background: var(--session-card-bg);
  border-radius: var(--session-radius);
  padding: 10px 12px;
  box-shadow: var(--shadow-md, 0 2px 12px rgba(0,0,0,0.08));
  border: 1px solid var(--session-border);
}
.keyword-header {
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--primary, #3D5A80);
}
.keyword-header i {
  margin-right: 6px;
}
.keyword-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.kw-tag {
  margin: 0;
}

/* ==================== Report ==================== */
.report-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
}
.report-loading-text {
  margin-top: 1rem;
  color: var(--text-muted, #888);
}
.report-loading-text i {
  margin-right: 6px;
}
.report-card {
  border-radius: var(--session-radius);
  max-width: 720px;
  margin: 0 auto;
  border: 1px solid var(--session-border);
}
.report-top-info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 0.5rem;
  font-size: 0.85rem;
}
.report-job {
  font-weight: 600;
}
.report-rounds {
  color: var(--text-muted, #999);
  font-size: 0.78rem;
}
.report-summary {
  text-align: center;
  font-size: 0.9rem;
  color: var(--primary, #3D5A80);
  padding: 0.5rem 0;
  font-weight: 500;
}
.overall-score-area {
  text-align: center;
  padding: 1rem 0;
}
.overall-score-area h3 {
  margin-top: 0.6rem;
}
.dimensions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.8rem;
  margin: 1rem 0;
}
.dim-card {
  background: var(--bg-alt, #f8f9fa);
  border-radius: var(--radius-sm, 10px);
  padding: 0.8rem;
}
.dim-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.4rem;
  font-size: 0.85rem;
}
.dim-comment {
  font-size: 0.78rem;
  color: var(--text-muted, #888);
  margin-top: 4px;
}
.report-lists {
  margin: 1rem 0;
}
.report-lists ul {
  padding-left: 1.2rem;
  color: var(--text-body, #555);
  line-height: 1.8;
  font-size: 0.9rem;
}
.report-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  padding-top: 1.5rem;
}

/* ==================== Responsive ==================== */
@media (max-width: 960px) {
  .chat-layout {
    flex-direction: column;
    overflow-y: auto;
  }
  .chat-sidebar {
    flex: 0 0 auto;
    flex-direction: row;
    flex-wrap: wrap;
  }
  .chat-sidebar > * {
    flex: 1 1 200px;
    min-width: 0;
  }
  .interview-topbar {
    flex-wrap: wrap;
    gap: 6px;
  }
  .it-left {
    flex: 1;
  }
  .it-center {
    order: 3;
    width: 100%;
    justify-content: center;
  }
}
</style>