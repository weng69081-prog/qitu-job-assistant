<template>
  <div class="ncd-page">
    <!-- 顶部 -->
    <div class="ncd-header">
      <button class="back-btn" @click="$router.back()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>
        返回
      </button>
      <div class="ncd-title-row">
        <h1 class="ncd-title">{{ nodeTitle }}</h1>
        <button class="ncd-done-btn" @click="markDone"><CheckCircle class="ic-sm" /> 标记完成</button>
      </div>
      <div class="ncd-sub">{{ nodeDesc }}</div>
    </div>

    <div class="ncd-body">
      <!-- 左栏：文档内容（可编辑） -->
      <div class="ncd-left">
        <div v-if="documents.length" class="ncd-section doc-section">
          <div class="doc-section-header">
            <span class="doc-section-title"><FileText class="ncd-ic" /> 文档</span>
            <button v-if="editingDocId" class="doc-edit-btn cancel" @click="cancelDocEdits(editingDocId)">取消编辑</button>
            <button v-else class="doc-edit-btn" @click="startEditDoc(documents[0])"><Pencil class="ncd-ic" /> 编辑</button>
          </div>
          <div v-for="doc in documents" :key="doc.id" class="doc-block">
            <div class="doc-title">{{ doc.title }}</div>

            <!-- 编辑工具栏（编辑模式显示） -->
            <div v-if="editingDocId === doc.id" class="doc-toolbar" @click.stop>
              <button class="tb-btn" @click="execCmd('bold')" title="加粗"><b>B</b></button>
              <button class="tb-btn" @click="execCmd('italic')" title="斜体"><i>I</i></button>
              <button class="tb-btn" @click="execCmd('underline')" title="下划线"><u>U</u></button>
              <span class="tb-sep"></span>
              <button class="tb-btn" @click="execCmd('formatBlock', 'h3')" title="标题1">H1</button>
              <button class="tb-btn" @click="execCmd('formatBlock', 'h4')" title="标题2">H2</button>
              <button class="tb-btn" @click="execCmd('insertUnorderedList')" title="列表">•列表</button>
              <span class="tb-sep"></span>
              <!-- 字体颜色 -->
              <div class="tb-color-wrap">
                <button class="tb-btn tb-color-btn" :style="{ color: editFontColor }" @click.stop="showColorPicker = !showColorPicker">🅰️</button>
                <div v-if="showColorPicker" class="color-picker-droplist" @click.stop>
                  <span v-for="c in fontColors" :key="c.value"
                    class="cp-item" :class="{ on: editFontColor === c.value }"
                    :style="{ color: c.value }"
                    @click="setFontColor(c.value)">
                    {{ c.name }}
                  </span>
                </div>
              </div>
              <span class="tb-sep"></span>
              <button class="tb-btn tb-save" @click="saveDocEdits(doc.id)"><Save class="ncd-ic" /> 保存</button>
              <button class="tb-btn tb-cancel" @click="cancelDocEdits(doc.id)">取消</button>
            </div>

            <!-- 编辑区域 -->
            <div
              v-if="editingDocId === doc.id"
              class="doc-body editable-area"
              :contenteditable="true"
              ref="editRefs"
              @keydown="onEditKeydown"
              v-html="mdToHtml(editContents[doc.id] || doc.content)"
            ></div>
            <!-- 预览区域 -->
            <div v-else class="doc-body" :style="{ color: fontColor }" v-html="mdToHtml(showContents[doc.id] || doc.content)"></div>
          </div>
        </div>
        <div v-else class="ncd-section"><div class="ncd-placeholder">暂无学习文档</div></div>
      </div>

      <!-- 右栏 -->
      <div class="ncd-right">
        <!-- 右上：推荐视频 -->
        <div class="ncd-section video-section">
          <div class="sec-title-row">
            <span class="sec-title"><Monitor class="ncd-ic" /> 推荐视频</span>
            <button class="btn-tiny btn-outline" @click="searchVideos" :disabled="videosLoading">
              <template v-if="videosLoading">搜索中...</template>
              <template v-else><RefreshCw class="ncd-ic-sm" /> 刷新视频</template>
            </button>
          </div>
          <div v-if="videos.length" class="video-list">
            <a v-for="(v, i) in videos.slice(0, 4)" :key="i" :href="v.url" target="_blank" class="video-item">
              <div class="video-thumb" :style="{ backgroundImage: `url(${v.cover})` }"></div>
              <div class="video-info">
                <div class="video-name">{{ v.title }}</div>
                <div class="video-meta">{{ v.author }} · {{ v.playCount }}</div>
              </div>
            </a>
          </div>
          <div v-else class="ncd-hint">暂无推荐视频，点「刷新视频」搜索</div>
        </div>

        <!-- 右下：AI对话 -->
        <div class="chat-panel">
          <div class="chat-title"><MessageSquare class="ncd-ic" /> AI学习助手 <span class="chat-ctx">{{ chatContext }}</span></div>
          <div class="chat-msgs" ref="chatBox">
            <div v-for="(m, i) in chatMessages" :key="i" class="chat-msg" :class="m.role">
              <div class="chat-bubble">{{ m.content }}</div>
            </div>
            <div v-if="chatLoading" class="chat-msg assistant">
              <div class="chat-bubble typing">思考中...</div>
            </div>
          </div>
          <div class="chat-input-row">
            <input v-model="chatInput" class="chat-field" placeholder="问关于这个知识点的问题..." :disabled="chatLoading" @keydown.enter="sendChat" />
            <button class="btn-sm btn-blue" :disabled="chatLoading" @click="sendChat">{{ chatLoading ? '发送中...' : '发送' }}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { FileText, Pencil, Save, Monitor, RefreshCw, MessageSquare, CheckCircle } from 'lucide-vue-next'

const route = useRoute()
const API = 'http://localhost:8000'
const nodeId = route.params.nodeId
const nodeTitle = ref('学习节点')
const nodeDesc = ref('')
const documents = ref([])
const videos = ref([])
const videosLoading = ref(false)
const fontColor = ref('#1E293B')
const fontColors = [
  { name: '深灰', value: '#1E293B' },
  { name: '经典蓝', value: '#2563EB' },
  { name: '暖棕', value: '#6B4226' },
  { name: '墨绿', value: '#166534' },
  { name: '紫色', value: '#7C3AED' },
]
const chatMessages = ref([])
const chatInput = ref('')
const chatBox = ref(null)
const chatContext = ref('')
const chatLoading = ref(false)

// 文档编辑状态
const editingDocId = ref(null)       // 当前编辑的文档ID
const editContents = reactive({})    // 编辑中的内容（key: doc.id）
const showContents = reactive({})    // 保存后的展示内容（key: doc.id）
const editFontColor = ref('#1E293B')
const showColorPicker = ref(false)
const editRefs = ref(null)

// 简易 Markdown → HTML 转换
function mdToHtml(text) {
  if (!text) return ''
  let html = text
    // 代码块
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    // 行内代码
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // 标题
    .replace(/^### (.+)$/gm, '<h4>$1</h4>')
    .replace(/^## (.+)$/gm, '<h3>$1</h3>')
    .replace(/^# (.+)$/gm, '<h2>$1</h2>')
    // 粗体
    .replace(/\*\*(.+?)\*\*/g, '<b>$1</b>')
    // 斜体
    .replace(/\*(.+?)\*/g, '<i>$1</i>')
    // 无序列表
    .replace(/^- (.+)$/gm, '<li>$1</li>')
    // 有序列表
    .replace(/^\d+\.\s(.+)$/gm, '<li>$1</li>')
    // 换行
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>')
  return '<p>' + html + '</p>'
}

function execCmd(cmd, val) {
  document.execCommand(cmd, false, val || null)
  nextTick(() => { showColorPicker.value = false })
}

function setFontColor(color) {
  editFontColor.value = color
  document.execCommand('foreColor', false, color)
  showColorPicker.value = false
}

function startEditDoc(doc) {
  editingDocId.value = doc.id
  editContents[doc.id] = showContents[doc.id] || doc.content
  editFontColor.value = showContents[doc.id] ? fontColor.value : '#1E293B'
  showColorPicker.value = false
  nextTick(() => {
    // 聚焦到可编辑区域
    const el = document.querySelector('.editable-area')
    if (el) el.focus()
  })
}

function onEditKeydown(e) {
  if (e.key === 'Escape') {
    cancelDocEdits(editingDocId.value)
  }
  // Ctrl+S 保存
  if ((e.ctrlKey || e.metaKey) && e.key === 's') {
    e.preventDefault()
    saveDocEdits(editingDocId.value)
  }
}

async function saveDocEdits(docId) {
  const el = document.querySelector('.editable-area')
  const html = el ? el.innerHTML : ''
  if (!html.trim()) return

  const doc = documents.value.find(d => d.id === docId)
  if (!doc) return

  try {
    const r = await fetch(`${API}/api/learning/notes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: 1,
        node_id: parseInt(nodeId),
        resource_id: docId,
        title: doc.title + ' - 笔记',
        content: html
      })
    })
    const d = await r.json()
    if (d.ok) {
      showContents[docId] = html
      editingDocId.value = null
    }
  } catch {}
}

function cancelDocEdits(docId) {
  editingDocId.value = null
  showColorPicker.value = false
}

const CHAT_LIMIT = 100  // 消息达到100条时自动打包

async function loadChatHistory() {
  try {
    const r = await fetch(`${API}/api/learning/chat/${nodeId}/history`)
    const d = await r.json()
    if (d.messages && d.messages.length) {
      chatMessages.value = d.messages
      if (!d.is_archived) {
        // 多条消息时追加一句续聊提示
        chatMessages.value.push({ role: 'assistant', content: '👋 接着上次继续聊～有什么问题尽管问！' })
      }
    } else {
      chatMessages.value = [
        { role: 'assistant', content: '👋 你好！关于这个知识点有什么想问的吗？我会根据当前文档内容回答你。' }
      ]
    }
  } catch {
    chatMessages.value = [
      { role: 'assistant', content: '👋 你好！关于这个知识点有什么想问的吗？我会根据当前文档内容回答你。' }
    ]
  }
  await nextTick()
  if (chatBox.value) chatBox.value.scrollTop = chatBox.value.scrollHeight
}

async function saveMessage(role, content) {
  try {
    await fetch(`${API}/api/learning/chat/${nodeId}/save?role=${role}&content=${encodeURIComponent(content)}`, { method: 'POST' })
  } catch {}
}

async function tryArchiveChat() {
  // 检查是否达到上限
  const total = chatMessages.value.length
  if (total < CHAT_LIMIT) return false
  try {
    const r = await fetch(`${API}/api/learning/chat/${nodeId}/archive`, { method: 'POST' })
    const d = await r.json()
    if (d.ok) {
      // 重新加载文档资源
      const r2 = await fetch(`${API}/api/learning/resources?node_id=${nodeId}`)
      const d2 = await r2.json()
      if (d2.items) {
        documents.value = d2.items.filter(item => item.resource_type === 'document' || item.resource_type === 'card')
      }
      // 清空聊天准备新对话
      chatMessages.value = [
        { role: 'assistant', content: `📦 刚才的对话已打包成知识卡片「${d.title}」！可以继续问新问题～` }
      ]
      return true
    }
  } catch {}
  return false
}

async function loadData() {
  // 先加载聊天历史
  await loadChatHistory()
  try {
    const r = await fetch(`${API}/api/learning/resources?node_id=${nodeId}`)
    const d = await r.json()
    if (d.items && d.items.length) {
      // 卡片和文档都展示
      documents.value = d.items.filter(item => item.resource_type === 'document' || item.resource_type === 'card')
      if (documents.value.length) {
        const current = documents.value[0]
        nodeTitle.value = current.title
        chatContext.value = current.title
      }
    }

    // 如果当前卡片还没有文档内容，自动生成
    const resourceId = route.query.resourceId
    if (resourceId) {
      const targetDoc = documents.value.find(d => d.id == resourceId)
      if (targetDoc && !targetDoc.content) {
        // 触发自动生成文档
        const genR = await fetch(`${API}/api/learning/nodes/${nodeId}/generate-doc?resource_id=${resourceId}`, { method: 'POST' })
        const genD = await genR.json()
        if (genD.ok) {
          // 重新加载
          const r2 = await fetch(`${API}/api/learning/resources?node_id=${nodeId}`)
          const d2 = await r2.json()
          if (d2.items) {
            documents.value = d2.items.filter(item => item.resource_type === 'document' || item.resource_type === 'card')
          }
        }
      }
    }
  } catch {}
  // 加载已有笔记（用于展示编辑过的文档）
  try {
    const r = await fetch(`${API}/api/learning/notes?node_id=${nodeId}`)
    const d = await r.json()
    if (d.items) {
      for (const n of d.items) {
        if (n.resource_id) {
          showContents[n.resource_id] = n.content
        }
      }
    }
  } catch {}
  // 搜视频
  await searchVideos()
}

async function searchVideos() {
  videosLoading.value = true
  try {
    const kw = nodeTitle.value + ' 教程'
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
  videosLoading.value = false
}

async function markDone() {
  try {
    await fetch(`${API}/api/learning/nodes/${nodeId}/progress?status=completed`, { method: 'POST' })
    alert('✅ 已标记完成！')
  } catch {}
}

async function sendChat() {
  const text = chatInput.value.trim()
  if (!text || chatLoading.value) return
  chatLoading.value = true

  // 保存用户消息
  chatMessages.value.push({ role: 'user', content: text })
  await saveMessage('user', text)
  chatInput.value = ''

  try {
    const context = chatContext.value || nodeTitle.value
    const r = await fetch(`${API}/api/learning/chat?context=${encodeURIComponent(context)}&question=${encodeURIComponent(text)}`)
    const d = await r.json()
    const answer = d.answer || '让我想想...'
    chatMessages.value.push({ role: 'assistant', content: answer })
    await saveMessage('assistant', answer)

    // 检查是否达到打包上限
    await tryArchiveChat()
  } catch {
    chatMessages.value.push({ role: 'assistant', content: '网络有点问题，稍后试试~' })
  }
  chatLoading.value = false
  await nextTick()
  if (chatBox.value) chatBox.value.scrollTop = chatBox.value.scrollHeight
}

onMounted(() => loadData())
</script>

<style scoped>
/* Lucide 图标 */
.ncd-ic { width: 15px; height: 15px; color: #2563EB; vertical-align: -2.5px; margin-right: 3px; }
.ncd-ic-sm { width: 13px; height: 13px; color: #2563EB; vertical-align: -2px; margin-right: 2px; }

.ncd-page { min-height: 100vh; background: #F8FAFC; padding-bottom: 40px; margin: calc(-1 * 24px) calc(-1 * var(--main-pad-x, 28px)); padding: 24px 0 64px; }
.ncd-header {
  background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
  padding: 20px 28px; border-bottom: 1.5px dashed #93C5FD;
}
.back-btn {
  display: flex; align-items: center; gap: 6px;
  background: none; border: none; color: #2563EB;
  font-size: 14px; cursor: pointer; padding: 0; margin-bottom: 8px;
}
.ncd-title-row { display: flex; align-items: center; gap: 12px; }
.ncd-title { font-size: 20px; font-weight: 700; color: #1E293B; flex: 1; }
.ncd-done-btn {
  padding: 5px 14px; border-radius: 8px; border: none;
  background: #DCFCE7; color: #16A34A; font-size: 13px; font-weight: 600;
  cursor: pointer; white-space: nowrap; transition: all 0.15s;
}
.ncd-done-btn:hover { background: #BBF7D0; }
.ncd-sub { font-size: 14px; color: #64748B; }

/* 两栏 - 等高 + 滚动 */
.ncd-body {
  display: grid; grid-template-columns: 1.5fr 1fr; gap: 14px;
  padding: 16px 24px; max-width: 1200px; margin: 0 auto;
  height: calc(100vh - 160px);
}
.ncd-left {
  display: flex; flex-direction: column; gap: 10px;
  overflow-y: auto; padding-right: 4px;
}
.ncd-left::-webkit-scrollbar { width: 4px; }
.ncd-left::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 2px; }

/* 文档框内的标题栏（标题左 + 编辑按钮右） */
.doc-section-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 10px;
}
.doc-section-title {
  font-size: 15px; font-weight: 600; color: #1E293B;
}
.doc-edit-btn.cancel {
  background: #FEE2E2; border-color: #FCA5A5; color: #DC2626;
}
.doc-edit-btn.cancel:hover { background: #FECACA; }
.ncd-right {
  display: flex; flex-direction: column; gap: 10px;
  overflow: hidden;
}

.ncd-section {
  background: white; border-radius: 10px; padding: 14px;
  border: 1.5px dashed #93C5FD;
}
.sec-title-row {
  display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 6px;
}
.sec-title { font-size: 16px; font-weight: 600; color: #1E293B; }

/* 文档 */
.doc-block { margin-bottom: 16px; }
.doc-title { font-size: 16px; font-weight: 700; color: #2563EB; margin-bottom: 8px; }
.doc-body { font-size: 14px; line-height: 1.7; overflow-x: auto; transition: color 0.2s; }
.doc-body :deep(h3) { font-size: 16px; font-weight: 700; margin: 12px 0 6px; }
.doc-body :deep(h4) { font-size: 14px; font-weight: 600; margin: 8px 0 4px; }
.doc-body :deep(p) { margin: 6px 0; }
.doc-body :deep(pre) { background: #F1F5F9; padding: 10px; border-radius: 6px; font-size: 13px; overflow-x: auto; }
.doc-body :deep(code) { background: #F1F5F9; padding: 1px 4px; border-radius: 3px; font-size: 13px; }
.doc-body :deep(ul), .doc-body :deep(ol) { margin: 6px 0; padding-left: 20px; }
.doc-body :deep(li) { margin: 3px 0; }

/* 编辑工具栏 */
.doc-toolbar {
  display: flex; align-items: center; gap: 2px; flex-wrap: wrap;
  padding: 6px 10px; margin-bottom: 8px;
  background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px;
}
.tb-btn {
  padding: 4px 10px; border-radius: 4px; border: 1px solid transparent;
  background: transparent; font-size: 13px; cursor: pointer; color: #475569; transition: all 0.12s;
}
.tb-btn:hover { background: #E2E8F0; border-color: #CBD5E1; }
.tb-sep { width: 1px; height: 20px; background: #E2E8F0; margin: 0 4px; display: inline-block; }
.tb-save { color: #16A34A; font-weight: 600; }
.tb-save:hover { background: #DCFCE7; border-color: #86EFAC; }
.tb-cancel { color: #64748B; }
.tb-cancel:hover { background: #F1F5F9; }

/* 字体颜色选择器（浮在工具栏内） */
.tb-color-wrap { position: relative; display: inline-flex; }
.color-picker-droplist {
  position: absolute; top: 100%; left: 0; z-index: 20; margin-top: 4px;
  background: white; border: 1px solid #E2E8F0; border-radius: 8px;
  padding: 6px 8px; display: flex; gap: 4px; flex-wrap: wrap;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1); min-width: 180px;
}
.cp-item {
  padding: 4px 10px; border-radius: 5px; font-size: 12px; font-weight: 500;
  cursor: pointer; border: 1px solid transparent; transition: all 0.12s;
}
.cp-item:hover { border-color: #CBD5E1; background: #F8FAFC; }
.cp-item.on { border-color: currentColor; background: #EFF6FF; }

/* 可编辑区 */
.editable-area {
  min-height: 120px; outline: none; padding: 8px;
  border: 1.5px solid #2563EB; border-radius: 8px; background: #FAFCFF;
}
.editable-area:focus { box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }

/* 编辑按钮 */
.doc-edit-btn {
  margin-top: 8px; padding: 5px 14px; border-radius: 6px;
  border: 1.5px dashed #93C5FD; background: transparent;
  color: #2563EB; font-size: 12px; cursor: pointer; transition: all 0.15s;
}
.doc-edit-btn:hover { background: #EFF6FF; border-color: #2563EB; }

/* 视频 */
.video-list { display: flex; flex-direction: column; gap: 6px; }
.video-item {
  display: flex; gap: 8px; background: #F8FAFC; border-radius: 6px;
  padding: 6px; text-decoration: none; transition: all 0.15s;
}
.video-item:hover { background: #EFF6FF; }
.video-thumb { width: 72px; height: 44px; border-radius: 5px; background-size: cover; background-position: center; background-color: #F1F5F9; flex-shrink: 0; }
.video-info { flex: 1; min-width: 0; }
.video-name { font-size: 13px; color: #1E293B; font-weight: 500; line-height: 1.3; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
.video-meta { font-size: 11px; color: #94A3B8; margin-top: 2px; }
.ncd-hint { font-size: 13px; color: #94A3B8; margin-top: 8px; }

/* AI对话 - 浅色渐变背景 */
.chat-panel {
  background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%);
  border-radius: 12px; border: 1.5px dashed #93C5FD;
  display: flex; flex-direction: column; flex: 1; min-height: 0;
}
.chat-title {
  padding: 6px 12px; font-size: 13px; font-weight: 600; color: #1E293B;
  border-bottom: 1px solid #DBEAFE;
}
.chat-ctx { font-size: 11px; color: #94A3B8; font-weight: 400; margin-left: 6px; }
.chat-msgs {
  flex: 1; padding: 6px 10px; overflow-y: auto; max-height: 160px;
  display: flex; flex-direction: column; gap: 4px;
}
.chat-msg { display: flex; }
.chat-msg.user { justify-content: flex-end; }
.chat-bubble { max-width: 85%; padding: 5px 8px; border-radius: 8px; font-size: 13px; line-height: 1.4; word-break: break-word; }
.chat-msg.assistant .chat-bubble { background: white; color: #1E293B; border-bottom-left-radius: 3px; border: 1px solid #E2E8F0; }
.chat-msg.user .chat-bubble { background: #2563EB; color: white; border-bottom-right-radius: 3px; }
.chat-input-row {
  display: flex; gap: 4px; padding: 5px 8px; border-top: 1px solid #DBEAFE;
}
.chat-field {
  flex: 1; padding: 5px 8px; border: 1px solid #E2E8F0; border-radius: 6px;
  font-size: 12px; outline: none; font-family: inherit; background: white;
}
.chat-field:focus { border-color: #2563EB; }

.ncd-placeholder { text-align: center; padding: 20px; color: #94A3B8; font-size: 14px; }

/* 通用按钮 */
.btn-sm { padding: 6px 14px; border-radius: 8px; font-size: 13px; border: none; cursor: pointer; font-weight: 500; transition: all 0.15s; }
.btn-blue { background: #2563EB; color: white; }
.btn-blue:hover { background: #1D4ED8; }
.btn-outline { background: #fff; color: #2563EB; border: 1.5px solid #BFDBFE; }
.btn-outline:hover { background: #EFF6FF; }
.btn-tiny { padding: 3px 10px; border-radius: 6px; font-size: 12px; border: none; cursor: pointer; font-weight: 500; transition: all 0.15s; }
</style>
