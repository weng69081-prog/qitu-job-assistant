<template>
  <div class="ai-assistant" :class="{ dragging }" :style="{ left: posX + 'px', top: posY + 'px' }">
    <!-- 悬浮按钮（可拖拽） -->
    <button class="ai-fab" :class="{ walking, speaking: !!speech }" @mousedown.prevent="startDrag"
      @touchstart.prevent="startDrag"
      @click="onFabClick">
      <span class="fab-icon"><img :src="imgFab" class="fab-img" alt="小橘"></span>
    </button>
    <!-- 打招呼气泡 -->
    <Transition name="speech">
      <div class="speech-bubble" v-if="speech" @click.stop>
        {{ speech }}
      </div>
    </Transition>

    <!-- 聊天面板 -->
    <Transition name="panel">
      <div class="ai-panel" v-if="visible">
        <!-- 顶栏 -->
        <div class="ai-header">
          <div class="ai-title">
            <img :src="imgHeader" class="ai-header-icon" alt="小橘">
            <span>小橘 · 智能助手</span>
          </div>
          <button class="ai-close" @click="visible = false"><Minus :size="16" class="icon-blue" /></button>
        </div>

        <!-- 消息区 -->
        <div class="ai-messages" ref="msgRef">
          <div v-for="(msg, i) in messages" :key="i"
               class="ai-msg"
               :class="msg.role === 'assistant' ? 'ai-msg-assistant' : 'ai-msg-user'">
            <div class="ai-msg-avatar">
              <img :src="imgMsg" class="ai-msg-img" alt="小橘" v-if="msg.role === 'assistant'">
              <User :size="16" class="icon-blue" />
            </div>
            <div class="ai-msg-bubble">
              <div class="ai-msg-text" v-html="renderMarkdown(msg.content)"></div>
            </div>
          </div>
          <!-- 加载中 -->
          <div class="ai-msg ai-msg-assistant" v-if="loading">
            <div class="ai-msg-avatar"><img :src="imgMsg" class="ai-msg-img" alt="小橘"></div>
            <div class="ai-msg-bubble">
              <span class="typing-dots"><span>.</span><span>.</span><span>.</span></span>
            </div>
          </div>
        </div>

        <!-- 推荐问题 -->
        <div class="ai-suggestions" v-if="!hasChatted && !loading">
          <button class="ai-suggestion" v-for="(q, i) in suggestions" :key="i" @click="sendQuick(q)">
            {{ q }}
          </button>
        </div>

        <!-- 输入区 -->
        <div class="ai-input-area">
          <input
            v-model="inputText"
            @keydown.enter="send"
            placeholder="给小橘发消息..."
            class="ai-input"
            :disabled="loading"
          />
          <button class="ai-send" @click="send" :disabled="loading || !inputText.trim()">
            <Send :size="16" class="icon-blue" />
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onBeforeUnmount } from 'vue'

const inputText = ref('')
const visible = ref(false)
const loading = ref(false)
const msgRef = ref(null)
const hasChatted = ref(false)
const outfitIndex = ref(0)  // 0=普通, 1=蝴蝶结, 2=快递猫

const fabImages = [
  '/src/assets/xiaoju-fab.png',
  '/src/assets/xiaoju-bow-fab.png',
  '/src/assets/xiaoju-delivery-fab.png'
]
const headerImages = [
  '/src/assets/xiaoju-header.png',
  '/src/assets/xiaoju-bow-header.png',
  '/src/assets/xiaoju-delivery-header.png'
]
const msgImages = [
  '/src/assets/xiaoju-msg.png',
  '/src/assets/xiaoju-bow-msg.png',
  '/src/assets/xiaoju-delivery-msg.png'
]

const imgFab = computed(() => fabImages[outfitIndex.value])
const imgHeader = computed(() => headerImages[outfitIndex.value])
const imgMsg = computed(() => msgImages[outfitIndex.value])

// 拖拽+漫步状态
const posX = ref(window.innerWidth - 72 - 24)
const posY = ref(window.innerHeight - 72 - 24)
const dragging = ref(false)
const dragStartX = ref(0)
const dragStartY = ref(0)
const dragOrigX = ref(0)
const dragOrigY = ref(0)
const walking = ref(true)
let wasDragged = false
const FAB_SIZE = 72
const PADDING = 24

onMounted(() => {
  posX.value = window.innerWidth - FAB_SIZE - PADDING
  posY.value = window.innerHeight - FAB_SIZE - PADDING
  startWalking()
  startAutoEncourage()
})

onBeforeUnmount(() => {
  stopWalking()
  stopAutoEncourage()
  endDrag()
  if (clickTimer) clearTimeout(clickTimer)
})

// ── 漫步逻辑 ──
const walkTarget = ref({ x: 0, y: 0 })
let stepTimer = null

function startWalking() {
  walking.value = true
  setNewTarget()
}

function stopWalking() {
  walking.value = false
  if (stepTimer) {
    clearInterval(stepTimer)
    stepTimer = null
  }
}

function setNewTarget() {
  if (!walking.value || dragging.value) return
  const margin = 80
  const tx = margin + Math.random() * (window.innerWidth - FAB_SIZE - margin * 2)
  const ty = margin + Math.random() * (window.innerHeight - FAB_SIZE - margin * 2)
  walkTarget.value = { x: tx, y: ty }
  startStepping()
}

function startStepping() {
  if (stepTimer) clearInterval(stepTimer)
  stepTimer = setInterval(takeStep, 1200) // 慢悠悠迈步
}

function takeStep() {
  if (!walking.value || dragging.value) {
    clearInterval(stepTimer)
    stepTimer = null
    return
  }
  const dx = walkTarget.value.x - posX.value
  const dy = walkTarget.value.y - posY.value
  const dist = Math.sqrt(dx*dx + dy*dy)
  if (dist < 20) {
    // 走到了，打个招呼再找新目标
    clearInterval(stepTimer)
    stepTimer = null
    sayHi()
    setTimeout(setNewTarget, 3000 + Math.random() * 4000)
    return
  }
  // 每步走15~25px（轻轻走）
  const step = Math.min(15 + Math.random() * 10, dist)
  const angle = Math.atan2(dy, dx)
  posX.value += Math.cos(angle) * step
  posY.value += Math.sin(angle) * step
  posX.value = Math.max(0, Math.min(window.innerWidth - FAB_SIZE, posX.value))
  posY.value = Math.max(0, Math.min(window.innerHeight - FAB_SIZE, posY.value))
}

// ── 打招呼 ──
const speech = ref('')
let speechTimer = null
const greetings = ['嗨！', 'Hi~', '喵！', '你好呀！', 'Hi!', '嘿嘿！', '喵呜~', '嗨～']
const encouragements = [
  '加油！今天也很棒！💪',
  '别灰心，机会多着呢！✨',
  '面试没问题的，咪相信你！😸',
  '休息一下，继续冲！⚡',
  '你已经很棒啦！🌟',
  '今天也要加油呀！🌞',
  '每一次尝试都是进步！📈',
  '你可以的！💯',
  '慢慢来，比较快～🐾',
  '相信自己！你最亮眼！✨',
  '咪给你打气！🎉',
  '今天状态很好呢！😎',
  '好事即将发生～🍀',
  '下一个offer就是你的！🎯',
]
let autoEncourageTimer = null

function sayHi() {
  speech.value = greetings[Math.floor(Math.random() * greetings.length)]
  if (speechTimer) clearTimeout(speechTimer)
  speechTimer = setTimeout(() => { speech.value = '' }, 2500)
  waving.value = true
  setTimeout(() => { waving.value = false }, 1500)
}

function sayEncouragement() {
  speech.value = encouragements[Math.floor(Math.random() * encouragements.length)]
  if (speechTimer) clearTimeout(speechTimer)
  speechTimer = setTimeout(() => { speech.value = '' }, 3000)
  // 说话时挥爪
  waving.value = true
  setTimeout(() => { waving.value = false }, 1500)
}

// ── 定时鼓励 ──
function startAutoEncourage() {
  stopAutoEncourage()
  const delay = 25000 + Math.random() * 35000  // 25~60秒随机
  autoEncourageTimer = setTimeout(() => {
    if (!visible.value && !dragging.value) {
      sayEncouragement()
    }
    startAutoEncourage()  // 循环
  }, delay)
}
function stopAutoEncourage() {
  if (autoEncourageTimer) {
    clearTimeout(autoEncourageTimer)
    autoEncourageTimer = null
  }
}

// ── 拖拽逻辑 ──
function startDrag(e) {
  dragging.value = true
  wasDragged = false
  stopWalking()
  const cx = e.clientX ?? e.touches[0].clientX
  const cy = e.clientY ?? e.touches[0].clientY
  dragStartX.value = cx
  dragStartY.value = cy
  dragOrigX.value = posX.value
  dragOrigY.value = posY.value
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', endDrag)
  document.addEventListener('touchmove', onDrag, { passive: false })
  document.addEventListener('touchend', endDrag)
}

function onDrag(e) {
  const cx = e.clientX ?? e.touches[0].clientX
  const cy = e.clientY ?? e.touches[0].clientY
  const dx = cx - dragStartX.value
  const dy = cy - dragStartY.value
  if (Math.abs(dx) > 3 || Math.abs(dy) > 3) wasDragged = true
  const newX = Math.max(0, Math.min(window.innerWidth - FAB_SIZE, dragOrigX.value + dx))
  const newY = Math.max(0, Math.min(window.innerHeight - FAB_SIZE, dragOrigY.value + dy))
  posX.value = newX
  posY.value = newY
}

function endDrag(e) {
  dragging.value = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', endDrag)
  document.removeEventListener('touchmove', onDrag)
  document.removeEventListener('touchend', endDrag)
  if (wasDragged) {
    startWalking()
  }
}

let clickTimer = null

function onFabClick() {
  if (wasDragged) return
  if (clickTimer) {
    // 第二次点击（双击）→ 切换造型
    clearTimeout(clickTimer)
    clickTimer = null
    outfitIndex.value = (outfitIndex.value + 1) % 3
    sayEncouragement()
  } else {
    // 第一次点击 → 等300ms看看是不是双击
    clickTimer = setTimeout(() => {
      clickTimer = null
      togglePanel()
    }, 300)
  }
}

const messages = ref([
  {
    role: 'assistant',
    content: '喵！我是小橘，你的AI求职小助手～有什么问题尽管问我吧！关于职业规划、面试技巧、简历修改我都能帮忙！'
  }
])

const suggestions = [
  '自我介绍应该怎么写？',
  '面试前需要准备什么？',
  '零经验怎么找实习？',
  '给我推荐一个职业方向',
]

function togglePanel() {
  visible.value = !visible.value
  if (visible.value) {
    stopWalking()
    stopAutoEncourage()  // 聊天时不说
  } else {
    startWalking()
    startAutoEncourage()  // 关掉面板恢复定时鼓励
  }
}

async function send() {
  const text = inputText.value.trim()
  if (!text || loading.value) return
  inputText.value = ''

  messages.value.push({ role: 'user', content: text })
  hasChatted.value = true
  loading.value = true
  scrollBottom()

  try {
    const raw = await fetch('/api/assistant/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages: messages.value.slice(1).map(m => ({ role: m.role, content: m.content })) })
    })
    const data = await raw.json()
    messages.value.push({ role: 'assistant', content: data.reply || '喵……小橘需要再想想。' })
  } catch {
    messages.value.push({ role: 'assistant', content: '喵……网络好像出了点问题，等下再试试？' })
  } finally {
    loading.value = false
    scrollBottom()
  }
}

function sendQuick(text) {
  inputText.value = text
  send()
}

function scrollBottom() {
  nextTick(() => {
    if (msgRef.value) msgRef.value.scrollTop = msgRef.value.scrollHeight
  })
}

function renderMarkdown(text) {
  if (!text) return ''
  // 简单渲染：代码块、粗体、列表、换行
  let html = text
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    // 代码块
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    // 行内代码
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // 粗体
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    // 换行
    .replace(/\n/g, '<br/>')
  return html
}

// 页面加载时自动挂载，但初始隐藏
</script>

<style scoped>
.ai-assistant {
  position: fixed;
  z-index: 9999;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
.ai-assistant.dragging {
  transition: none;
}
.ai-assistant.dragging .ai-fab { cursor: grabbing; }
.ai-assistant.dragging .ai-fab:hover { transform: none; }

/* ═══ 悬浮按钮 ═══ */
.ai-assistant .ai-fab {
  position: relative;
}
.ai-fab {
  width: 72px; height: 72px;
  border-radius: 16px;
  border: none;
  background: transparent;
  cursor: grab;
  transition: transform 0.25s;
  display: flex; align-items: center; justify-content: center;
  padding: 0;
  user-select: none;
  -webkit-user-select: none;
  z-index: 2;
}
/* 影子 */
.ai-assistant::after {
  content: '';
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 10px;
  background: radial-gradient(ellipse, rgba(0,0,0,0.15) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}
.ai-fab:hover { transform: scale(1.1); }
.fab-img { width: 72px; height: 72px; }

/* ═══ 打招呼气泡 ═══ */
.speech-bubble {
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  background: #fff;
  color: #3D5A80;
  padding: 6px 14px;
  border-radius: 18px;
  font-size: 14px;
  font-weight: 700;
  white-space: nowrap;
  box-shadow: 0 3px 12px rgba(0,0,0,0.1);
  pointer-events: none;
  z-index: 10;
}
.speech-bubble::after {
  content: '';
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 6px solid #fff;
}
.speech-enter-active { animation: pop-in 0.3s ease; }
.speech-leave-active { animation: pop-in 0.2s ease reverse; }
@keyframes pop-in {
  0% { opacity: 0; transform: translateX(-50%) scale(0.5); }
  100% { opacity: 1; transform: translateX(-50%) scale(1); }
}

/* 走路动画：不动画面，只移动位置 */
@keyframes cat-walk {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-2px); }
}

@keyframes cat-idle {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-2px) rotate(1deg); }
  75% { transform: translateY(-2px) rotate(-1deg); }
}

.ai-fab .fab-img {
  animation: cat-idle 3s ease-in-out infinite;
}

.ai-fab.walking .fab-img {
  animation: cat-walk 2.4s ease-in-out infinite;
}

/* 说话时挥爪 */
@keyframes cat-wave {
  0%, 100% { transform: rotate(0deg) translateY(0); }
  20% { transform: rotate(-8deg) translateY(-4px); }
  40% { transform: rotate(8deg) translateY(-4px); }
  60% { transform: rotate(-5deg) translateY(-2px); }
  80% { transform: rotate(5deg) translateY(-2px); }
}
.ai-fab.speaking .fab-img {
  animation: cat-wave 0.6s ease-in-out 3;
}

/* ═══ 聊天面板 ═══ */
.ai-panel {
  position: absolute;
  bottom: 62px;
  right: 0;
  width: 360px;
  height: 500px;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.12);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid #EDE7DE;
}

/* ═══ 过渡动画 ═══ */
.panel-enter-active, .panel-leave-active { transition: all 0.25s ease; }
.panel-enter-from, .panel-leave-to { opacity: 0; transform: translateY(10px) scale(0.95); }

/* ═══ 顶栏 ═══ */
.ai-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 14px 16px;
  background: linear-gradient(135deg, #3D5A80 0%, #2C4460 100%);
  color: #fff;
}
.ai-title { display: flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 700; }
.ai-title i { font-size: 18px; }
.ai-close { background: none; border: none; color: rgba(255,255,255,0.6); cursor: pointer; font-size: 14px; transition: color 0.2s; }
.ai-close:hover { color: #fff; }

/* ═══ 消息区 ═══ */
.ai-messages {
  flex: 1;
  overflow-y: auto;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  background: #F5F0E8;
}
.ai-msg { display: flex; gap: 8px; max-width: 90%; }
.ai-msg-user { align-self: flex-end; flex-direction: row-reverse; }
.ai-msg-avatar {
  width: 48px; height: 48px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
  font-size: 13px;
}
.ai-msg-img { width: 100%; height: 100%; }
.ai-header-icon { width: 28px; height: 28px; }
.ai-msg-assistant .ai-msg-avatar { background: transparent; }
.ai-msg-user .ai-msg-avatar { background: rgba(200,90,32,0.15); color: #C85A20; }
.ai-msg-bubble {
  padding: 10px 14px;
  border-radius: 14px;
  font-size: 13px;
  line-height: 1.6;
}
.ai-msg-assistant .ai-msg-bubble {
  background: #fff;
  color: #4A5568;
  border-bottom-left-radius: 4px;
}
.ai-msg-user .ai-msg-bubble {
  background: linear-gradient(135deg, #3D5A80, #4A6B94);
  color: #fff;
  border-bottom-right-radius: 4px;
}
.ai-msg-text :deep(code) { background: rgba(61,90,128,0.1); padding: 1px 5px; border-radius: 3px; font-size: 12px; }
.ai-msg-text :deep(pre) { background: #2C3E50; color: #E0E7E; padding: 10px; border-radius: 8px; overflow-x: auto; font-size: 12px; margin: 4px 0; }
.ai-msg-text :deep(pre code) { background: none; padding: 0; }

/* ═══ 输入区域 ═══ */
.ai-input-area {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-top: 1px solid #EDE7DE;
  background: #fff;
}
.ai-input {
  flex: 1;
  border: 1px solid #E0D8CC;
  border-radius: 20px;
  padding: 8px 14px;
  font-size: 13px;
  outline: none;
  transition: border-color 0.2s;
}
.ai-input:focus { border-color: #3D5A80; }
.ai-input:disabled { opacity: 0.5; }
.ai-send {
  width: 36px; height: 36px;
  border-radius: 50%;
  border: none;
  background: #3D5A80;
  color: #fff;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}
.ai-send:hover { background: #2C4460; }
.ai-send:disabled { opacity: 0.4; cursor: default; }

/* ═══ 推荐问题 ═══ */
.ai-suggestions {
  padding: 10px 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  border-top: 1px solid #EDE7DE;
  background: #FAF8F5;
}
.ai-suggestion {
  font-size: 12px;
  color: #3D5A80;
  background: rgba(61,90,128,0.08);
  border: 1px solid rgba(61,90,128,0.15);
  border-radius: 14px;
  padding: 5px 12px;
  cursor: pointer;
  transition: all 0.2s;
}
.ai-suggestion:hover { background: #3D5A80; color: #fff; border-color: #3D5A80; }

/* ═══ 打字动画 ═══ */
.typing-dots span { animation: blink 1.4s infinite both; font-size: 24px; line-height: 0.5; color: #8EA0B8; }
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink { 0%, 80%, 100% { opacity: 0; } 40% { opacity: 1; } }
</style>