<template>
  <div class="lpd-page">
    <!-- 顶部 -->
    <div class="lpd-top">
      <button class="back-btn" @click="$router.push('/learning-center')">← 返回学习中心</button>
      <div class="lpd-title-row">
        <h1 class="lpd-title">{{ session.job }} · 面试复盘</h1>
        <span class="lpd-score" :class="scoreClass(session.score)">{{ session.score }}分</span>
      </div>
      <p class="lpd-desc">
        {{ session.mode === 'stress' ? '💢 压力模式' : '📋 普通模式' }}
        · {{ session.question_count }}题 · {{ session.created_at }}
      </p>
      <!-- 维度分 -->
      <div v-if="Object.keys(session.dimensions || {}).length" class="lpd-dims">
        <span v-for="(v, k) in session.dimensions" :key="k" class="lpd-dim-tag">{{ k }}: {{ v }}</span>
      </div>
      <!-- 建议 -->
      <div v-if="session.suggestions && session.suggestions.length" class="lpd-suggestions">
        <span v-for="(s, i) in session.suggestions" :key="i" class="lpd-sug-item">💡 {{ s }}</span>
      </div>
    </div>

    <!-- 主体：左文档全文 + 右：薄弱点+视频+AI -->
    <div class="lpd-body">
      <!-- 左栏：文档全文（inline，不弹窗） -->
      <div class="lpd-left">
        <template v-if="selectedWeakData">
          <div class="ncd-section-header">
            <span class="ncd-section-title">{{ selectedWeakData.name }}</span>
            <button class="doc-edit-btn" @click="generateWeakDoc" :disabled="docGenLoading">{{ docGenLoading ? '生成中...' : '✏️ 生成文档' }}</button>
          </div>
          <div v-if="currentDoc" class="doc-body" v-html="renderMd(currentDoc.content)"></div>
          <div v-else class="doc-placeholder">暂无文档，点「生成文档」创建学习笔记</div>
        </template>
        <div v-else class="lpd-empty-lg">👉 从右侧选择一个薄弱点开始学习</div>
      </div>

      <!-- 右栏：薄弱点列表 + 视频 + AI -->
      <div class="lpd-right">
        <!-- 薄弱点列表 -->
        <div class="lpd-section">
          <div class="sec-title-row"><span class="sec-title">📋 待加强知识点</span></div>
          <div class="weak-list">
            <div v-for="w in weakItems" :key="w.name"
              class="weak-item" :class="{ active: selectedWeak === w.name }"
              @click="selectWeak(w)">
              <span class="weak-dot"></span>
              <span class="weak-name">{{ w.name }}</span>
            </div>
          </div>
          <div v-if="!weakItems.length" class="lpd-empty-sm" style="text-align:center;padding:12px;">暂无薄弱点数据</div>
        </div>

        <!-- 视频 -->
        <div class="lpd-section">
          <div class="sec-title-row">
            <span class="sec-title">📺 推荐视频</span>
            <button class="btn-tiny btn-outline" @click="searchVideos" :disabled="videoLoading">{{ videoLoading ? '搜索中...' : '🔄' }}</button>
          </div>
          <div v-if="videos.length" class="video-list">
            <a v-for="(v, i) in videos.slice(0, 3)" :key="i" :href="v.url" target="_blank" class="video-item">
              <div class="video-thumb" :style="{ backgroundImage: `url(${v.cover})` }"></div>
              <div class="video-info">
                <div class="video-name">{{ v.title }}</div>
                <div class="video-meta">{{ v.author }} · {{ v.playCount }}</div>
              </div>
            </a>
          </div>
          <div v-else class="lpd-empty-sm">点🔄搜索相关视频</div>
        </div>

        <!-- AI 对话 -->
        <div class="chat-section">
          <div class="sec-title-row"><span class="sec-title">💬 AI学习助手</span></div>
          <div class="chat-panel">
            <div class="chat-msgs" ref="chatBox">
              <div v-for="(m, i) in chatMessages" :key="i" class="chat-msg" :class="m.role">
                <div class="chat-bubble">{{ m.content }}</div>
              </div>
              <div v-if="chatLoading" class="chat-msg assistant">
                <div class="chat-bubble typing">思考中...</div>
              </div>
            </div>
            <div class="chat-input-row">
              <input v-model="chatInput" class="chat-field" placeholder="提问..." :disabled="chatLoading" @keydown.enter="sendChat" />
              <button class="btn-sm btn-blue" :disabled="chatLoading" @click="sendChat">{{ chatLoading ? '...' : '发送' }}</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const API = ''
const sessionId = route.params.sessionId

const session = ref({})
const weakItems = ref([])
const selectedWeak = ref(null)
const selectedWeakData = ref(null)
const currentDoc = ref(null)
const docGenLoading = ref(false)
const videos = ref([])
const videoLoading = ref(false)
const chatMessages = ref([])
const chatInput = ref('')
const chatLoading = ref(false)
const chatBox = ref(null)

function renderMd(text) {
  if (!text) return ''
  let html = text
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
    .replace(/\n/g, '<br>')
  return '<p>' + html + '</p>'
}

function scoreClass(s) {
  if (s >= 80) return 'high'
  if (s >= 60) return 'mid'
  return 'low'
}

async function loadStudy() {
  try {
    const r = await fetch(`${API}/api/learning/interview/${sessionId}/study`)
    const d = await r.json()
    session.value = d.session || {}
    weakItems.value = d.weak_items || []
    // 默认选第一个薄弱点
    if (weakItems.value.length) {
      await selectWeak(weakItems.value[0])
    }
  } catch {}
}

async function selectWeak(w) {
  selectedWeak.value = w.name
  selectedWeakData.value = w
  currentDoc.value = null
  chatMessages.value = [
    { role: 'assistant', content: `👋 关于「${w.name}」有什么想问的吗？我会帮你巩固这个知识点。` }
  ]
  videos.value = []
  // 自动生成文档
  await generateWeakDoc()
}

async function generateWeakDoc() {
  if (!selectedWeakData.value) return
  docGenLoading.value = true
  try {
    const name = selectedWeakData.value.name
    const r = await fetch(`${API}/api/learning/study/generate-doc?context=${encodeURIComponent(name)}`, { method: 'POST' })
    const d = await r.json()
    if (d.ok && d.content) {
      currentDoc.value = { id: 'gen_' + Date.now(), title: name + ' 学习笔记', content: d.content }
    }
  } catch {}
  docGenLoading.value = false
}

async function searchVideos() {
  if (!selectedWeakData.value) return
  videoLoading.value = true
  try {
    const kw = selectedWeakData.value.name + ' 教程'
    const r = await fetch(`${API}/api/bilibili/keyword-search?keyword=${encodeURIComponent(kw)}`)
    const d = await r.json()
    videos.value = (d.videos || []).map(v => ({
      title: v.title || '',
      cover: v.pic || '',
      url: `https://www.bilibili.com/video/${v.bvid || ''}`,
      author: v.author || '',
      playCount: v.play ? (v.play > 10000 ? (v.play / 10000).toFixed(1) + '万' : v.play) : '',
    }))
  } catch {}
  videoLoading.value = false
}

async function sendChat() {
  const text = chatInput.value.trim()
  if (!text || chatLoading.value) return
  chatLoading.value = true
  chatMessages.value.push({ role: 'user', content: text })
  chatInput.value = ''
  try {
    const context = selectedWeakData.value?.name || ''
    const r = await fetch(`${API}/api/learning/chat?context=${encodeURIComponent(context)}&question=${encodeURIComponent(text)}`)
    const d = await r.json()
    chatMessages.value.push({ role: 'assistant', content: d.answer || '让我想想...' })
  } catch {
    chatMessages.value.push({ role: 'assistant', content: '网络有点问题，稍后试试~' })
  }
  chatLoading.value = false
  await nextTick()
  if (chatBox.value) chatBox.value.scrollTop = chatBox.value.scrollHeight
}

onMounted(loadStudy)
</script>

<style scoped>
.lpd-page { min-height: 100vh; background: #F8FAFC; padding-bottom: 40px; }
.lpd-top {
  background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
  padding: 20px 32px; border-bottom: 1.5px dashed #93C5FD;
}
.back-btn { display: flex; align-items: center; gap: 6px; background: none; border: none; color: #2563EB; font-size: 14px; cursor: pointer; padding: 0; margin-bottom: 8px; }
.lpd-title-row { display: flex; align-items: center; gap: 12px; }
.lpd-title { font-size: 20px; font-weight: 700; color: #1E293B; flex: 1; }
.lpd-score { font-size: 14px; font-weight: 700; padding: 2px 12px; border-radius: 8px; }
.lpd-score.high { background: #DCFCE7; color: #16A34A; }
.lpd-score.mid { background: #FEF3C7; color: #D97706; }
.lpd-score.low { background: #FEE2E2; color: #DC2626; }
.lpd-desc { font-size: 14px; color: #64748B; margin-top: 4px; }
.lpd-dims { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
.lpd-dim-tag { font-size: 11px; padding: 2px 8px; border-radius: 4px; background: white; color: #475569; border: 1px solid #E2E8F0; }
.lpd-suggestions { display: flex; flex-direction: column; gap: 4px; margin-top: 8px; }
.lpd-sug-item { font-size: 13px; color: #2563EB; }

/* 两栏布局 */
.lpd-body { display: grid; grid-template-columns: 1.8fr 1.2fr; gap: 14px; padding: 16px 24px; max-width: 1200px; margin: 0 auto; height: calc(100vh - 200px); }
.lpd-left { display: flex; flex-direction: column; gap: 10px; overflow-y: auto; padding-right: 4px; }
.lpd-left::-webkit-scrollbar { width: 4px; }
.lpd-left::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 2px; }
.lpd-right { display: flex; flex-direction: column; gap: 12px; overflow-y: auto; padding-right: 4px; }
.lpd-right::-webkit-scrollbar { width: 4px; }
.lpd-right::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 2px; }

.lpd-section { background: white; border-radius: 10px; padding: 14px; border: 1.5px dashed #93C5FD; }
.sec-title-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 8px; }
.sec-title { font-size: 14px; font-weight: 600; color: #1E293B; }

.video-list { display: flex; flex-direction: column; gap: 6px; }
.video-item { display: flex; gap: 8px; background: #F8FAFC; border-radius: 6px; padding: 6px; text-decoration: none; }
.video-item:hover { background: #EFF6FF; }
.video-thumb { width: 72px; height: 44px; border-radius: 5px; background-size: cover; background-position: center; background-color: #F1F5F9; flex-shrink: 0; }
.video-info { flex: 1; min-width: 0; }
.video-name { font-size: 13px; color: #1E293B; font-weight: 500; line-height: 1.3; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.video-meta { font-size: 11px; color: #94A3B8; margin-top: 2px; }

.chat-panel { flex: 1; display: flex; flex-direction: column; background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%); border-radius: 10px; border: 1.5px dashed #93C5FD; min-height: 100px; }
.chat-msgs { flex: 1; padding: 8px 10px; overflow-y: auto; display: flex; flex-direction: column; gap: 4px; max-height: 160px; }
.chat-msg { display: flex; }
.chat-msg.user { justify-content: flex-end; }
.chat-bubble { max-width: 85%; padding: 5px 8px; border-radius: 8px; font-size: 13px; line-height: 1.4; word-break: break-word; }
.chat-msg.assistant .chat-bubble { background: white; color: #1E293B; border-bottom-left-radius: 3px; border: 1px solid #E2E8F0; }
.chat-msg.user .chat-bubble { background: #2563EB; color: white; border-bottom-right-radius: 3px; }
.chat-input-row { display: flex; gap: 4px; padding: 5px 8px; border-top: 1px solid #DBEAFE; }
.chat-field { flex: 1; padding: 5px 8px; border: 1px solid #E2E8F0; border-radius: 6px; font-size: 12px; outline: none; font-family: inherit; background: white; }
.chat-field:focus { border-color: #2563EB; }

.lpd-empty-sm { font-size: 13px; color: #94A3B8; }
.lpd-empty-lg { display: flex; align-items: center; justify-content: center; height: 100%; font-size: 14px; color: #94A3B8; }

/* 文档区（inline，像NodeContentDetail一样） */
.ncd-section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.ncd-section-title { font-size: 16px; font-weight: 700; color: #2563EB; }
.doc-edit-btn { padding: 4px 12px; border-radius: 6px; border: 1.5px dashed #93C5FD; background: transparent; color: #2563EB; font-size: 12px; cursor: pointer; }
.doc-edit-btn:hover { background: #EFF6FF; border-color: #2563EB; }
.doc-body { font-size: 14px; line-height: 1.7; color: #1E293B; }
.doc-body :deep(h2) { font-size: 18px; font-weight: 700; margin: 16px 0 8px; }
.doc-body :deep(h3) { font-size: 16px; font-weight: 700; margin: 12px 0 6px; }
.doc-body :deep(h4) { font-size: 14px; font-weight: 600; margin: 8px 0 4px; }
.doc-body :deep(p) { margin: 6px 0; }
.doc-body :deep(pre) { background: #F1F5F9; padding: 10px; border-radius: 6px; font-size: 13px; overflow-x: auto; }
.doc-body :deep(code) { background: #F1F5F9; padding: 1px 4px; border-radius: 3px; font-size: 13px; }
.doc-body :deep(ul) { margin: 6px 0; padding-left: 20px; }
.doc-body :deep(li) { margin: 3px 0; }
.doc-placeholder { text-align: center; padding: 40px 20px; color: #94A3B8; font-size: 14px; }

/* 薄弱点列表 */
.weak-list { display: flex; flex-direction: column; gap: 2px; }
.weak-item { display: flex; align-items: center; gap: 8px; padding: 6px 10px; border-radius: 6px; cursor: pointer; transition: all 0.12s; background: #F8FAFC; }
.weak-item:hover { background: #EFF6FF; }
.weak-item.active { background: #EFF6FF; border: 1px solid #93C5FD; }
.weak-dot { width: 6px; height: 6px; border-radius: 50%; background: #F59E0B; flex-shrink: 0; }
.weak-name { font-size: 13px; color: #1E293B; flex: 1; }

.chat-section { flex: 1; display: flex; flex-direction: column; min-height: 0; }

.btn-sm { padding: 6px 14px; border-radius: 8px; font-size: 13px; border: none; cursor: pointer; font-weight: 500; }
.btn-blue { background: #2563EB; color: white; }
.btn-blue:hover { background: #1D4ED8; }
.btn-outline { background: #fff; color: #2563EB; border: 1.5px solid #BFDBFE; }
.btn-outline:hover { background: #EFF6FF; }
.btn-tiny { padding: 3px 10px; border-radius: 6px; font-size: 12px; border: none; cursor: pointer; font-weight: 500; }
</style>