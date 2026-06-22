<template>
  <div class="lpd-page">
    <!-- 顶部 -->
    <div class="lpd-top">
      <button class="back-btn" @click="$router.back()">← 返回学习中心</button>
      <div class="lpd-title-row">
        <h1 class="lpd-title">{{ path.title }}</h1>
        <span class="lpd-diff-tag" :class="path.difficulty">{{ diffLabel(path.difficulty) }}</span>
      </div>
      <p class="lpd-desc">{{ path.description || '' }}</p>
      <div class="lpd-progress-row">
        <div class="progress-bar"><div class="progress-fill" :style="{ width: path.progress + '%' }"></div></div>
        <span class="progress-text">{{ path.progress }}%</span>
        <span class="lpd-node-count">{{ chapters.length }}章 · {{ totalLeafNodes }}个知识点</span>
      </div>
    </div>

    <!-- 主体：左目录 + 右卡片 -->
    <div class="lpd-body">
      <!-- === 左栏：两级树目录 === -->
      <div class="lpd-left">
        <div class="lpd-panel-title"><BookOpen class="lpd-icon" /> 学习目录</div>
        <div class="lpd-tree-list">
          <template v-for="ch in chapters" :key="ch.id">
            <!-- 阶段（章）行 -->
            <div class="lpd-tree-chapter">
              <span class="lpd-tree-arrow" @click="toggleChapter(ch.id)">{{ expandedChapters.has(ch.id) ? '▼' : '▶' }}</span>
              <span class="lpd-tree-dot"></span>
              <span class="lpd-tree-ch-title" @click="toggleChapter(ch.id)">{{ ch.title }}</span>
              <span class="lpd-tree-count">{{ chapterChildren(ch.id).length }}</span>
              <button class="lpd-tree-add-btn" @click.stop="openChapterDialog(ch)" title="为此章节创建学习卡片">＋</button>
            </div>
            <!-- 知识子节点 -->
            <div v-for="kp in chapterChildren(ch.id)" :key="kp.id"
              class="lpd-tree-kp" :class="{ active: selectedKp === kp.id }"
              @click="selectKp(kp)"
              v-show="expandedChapters.has(ch.id)">
              <span class="lpd-tree-kp-dot" :class="kp.status"></span>
              <span class="lpd-tree-kp-name">{{ kp.title }}</span>
              <span class="lpd-tree-kp-stat" :class="kp.status">{{ kp.status === 'completed' ? '✓' : '' }}</span>
            </div>
          </template>
        </div>
        <!-- 添加章 -->
        <div class="lpd-add-section">
          <input v-model="newChapterTitle" class="lpd-add-input" placeholder="+ 添加章节" @keydown.enter="addChapter" />
        </div>
      </div>

      <!-- === 右栏：知识点下的学习卡片 === -->
      <div class="lpd-right">
        <template v-if="selectedKp">
          <div class="lpd-right-header">
            <div class="lpd-right-title">
              <span class="lpd-rp-dot" :class="selectedKpData.status"></span>
              <span>{{ selectedKpData.title }}</span>
            </div>
            <!-- 添加卡片按钮：弹窗输入名称 -->
            <button class="lpd-btn-quick" @click="showAddDialog = true">+ 添加学习卡片</button>

            <!-- 搜索框 -->
            <div class="lpd-search-row">
              <input v-model="cardSearch" class="lpd-search-input" placeholder="🔍 搜索已有卡片..." />
            </div>
          </div>

          <div v-if="!filteredCards.length" class="lpd-empty-sm">
            {{ cards.length ? '没有匹配的卡片' : '还没有学习卡片，点「+ 添加学习卡片」创建一张' }}
          </div>

          <div class="lpd-card-grid">
            <div v-for="card in filteredCards" :key="card.id" class="lpd-card-item"
              @click="goCard(card)">
              <div class="lpd-card-icon"><FileText class="lpd-icon-lg" /></div>
              <div class="lpd-card-title">{{ card.title }}</div>
              <div class="lpd-card-type">{{ card.resource_type }}</div>
              <button class="lpd-card-del" @click.stop="delCard(card)">✕</button>
            </div>
          </div>
        </template>

        <div v-else class="lpd-empty-lg">
          👈 从左侧目录选择一个知识点开始学习
        </div>
      </div>
    </div>

    <!-- 知识点添加卡片弹窗 -->
    <div class="lpd-overlay" v-if="showAddDialog" @click.self="showAddDialog = false">
      <div class="lpd-dialog">
        <div class="lpd-dialog-title">添加学习卡片</div>
        <div class="lpd-dialog-sub">为「{{ selectedKpData.title }}」创建学习卡片</div>
        <input v-model="dialogCardName" class="lpd-dialog-input" placeholder="输入卡片名称..."
          @keydown.enter="confirmAddCard" ref="dialogInput" />
        <div class="lpd-dialog-actions">
          <button class="lpd-dialog-cancel" @click="showAddDialog = false">取消</button>
          <button class="lpd-dialog-confirm" @click="confirmAddCard">确定</button>
        </div>
      </div>
    </div>

    <!-- 章节创建卡片弹窗 -->
    <div class="lpd-overlay" v-if="showChapterDialog" @click.self="showChapterDialog = false">
      <div class="lpd-dialog">
        <div class="lpd-dialog-title">从章节创建卡片</div>
        <div class="lpd-dialog-sub">为「{{ chapterDialogData.title }}」创建同名学习卡片</div>
        <input v-model="chapterDialogName" class="lpd-dialog-input" placeholder="卡片名称..."
          @keydown.enter="confirmChapterCard" />
        <div class="lpd-dialog-actions">
          <button class="lpd-dialog-cancel" @click="showChapterDialog = false">取消</button>
          <button class="lpd-dialog-confirm" @click="confirmChapterCard">确认添加</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { BookOpen, FileText } from 'lucide-vue-next'
const route = useRoute()
const router = useRouter()
const API = 'http://localhost:8000'
const pathId = route.params.pathId

const path = ref({})
const allNodes = ref([])
const expandedChapters = ref(new Set())
const selectedKp = ref(null)
const selectedKpData = ref({})
const newChapterTitle = ref('')
const cards = ref([])
const cardSearch = ref('')

// 弹窗（知识点添加卡片）
const showAddDialog = ref(false)
const dialogCardName = ref('')
const dialogInput = ref(null)

// 弹窗（章节创建卡片）
const showChapterDialog = ref(false)
const chapterDialogData = ref({})
const chapterDialogName = ref('')

const chapters = computed(() =>
  allNodes.value.filter(n => n.parent_id === 0)
)

const totalLeafNodes = computed(() =>
  allNodes.value.filter(n => n.parent_id > 0).length
)

const filteredCards = computed(() => {
  const q = cardSearch.value.trim().toLowerCase()
  if (!q) return cards.value
  return cards.value.filter(c => c.title.toLowerCase().includes(q))
})

function chapterChildren(chapterId) {
  return allNodes.value
    .filter(n => n.parent_id === chapterId)
    .sort((a, b) => a.order_index - b.order_index)
}

function toggleChapter(chId) {
  const s = new Set(expandedChapters.value)
  if (s.has(chId)) s.delete(chId)
  else s.add(chId)
  expandedChapters.value = s
}

function diffLabel(d) {
  return { beginner: '入门', intermediate: '进阶', advanced: '高级' }[d] || d
}

async function selectKp(kp) {
  selectedKp.value = kp.id
  selectedKpData.value = kp
  await loadCards(kp.id)
  // 如果没有卡片，自动创建一张并跳转进去
  if (cards.value.length === 0) {
    await autoCreateAndGo(kp)
  }
}

async function autoCreateAndGo(kp) {
  try {
    const r = await fetch(`${API}/api/learning/resources?node_id=${kp.id}&title=${encodeURIComponent(kp.title)}&resource_type=card`, { method: 'POST' })
    const d = await r.json()
    if (d.id) {
      router.push(`/learning-center/node-content/${kp.id}?resourceId=${d.id}`)
    }
  } catch {}
}

async function loadCards(nodeId) {
  try {
    const r = await fetch(`${API}/api/learning/resources?node_id=${nodeId}`)
    const d = await r.json()
    cards.value = d.items || []
  } catch { cards.value = [] }
}

// 弹窗自动聚焦输入框
watch(showAddDialog, async (val) => {
  if (val) {
    dialogCardName.value = selectedKpData.value.title || ''
    await nextTick()
    dialogInput.value?.focus()
  }
})

async function confirmAddCard() {
  const t = dialogCardName.value.trim()
  if (!t || !selectedKp.value) return
  try {
    await fetch(`${API}/api/learning/resources?node_id=${selectedKp.value}&title=${encodeURIComponent(t)}&resource_type=card`, { method: 'POST' })
    dialogCardName.value = ''
    showAddDialog.value = false
    await loadCards(selectedKp.value)
  } catch {}
}

function openChapterDialog(ch) {
  chapterDialogData.value = ch
  chapterDialogName.value = ch.title
  showChapterDialog.value = true
}

async function confirmChapterCard() {
  const t = chapterDialogName.value.trim()
  if (!t || !chapterDialogData.value.id) return
  const ch = chapterDialogData.value
  showChapterDialog.value = false
  // 在弹出的知识点列表中选择第一个知识点（如果有）
  const firstKp = allNodes.value.find(n => n.parent_id === ch.id)
  const targetNodeId = firstKp ? firstKp.id : chapterDialogData.value.id
  // 如果知识点列表为空则选章节本身
  try {
    await fetch(`${API}/api/learning/resources?node_id=${targetNodeId}&title=${encodeURIComponent(t)}&resource_type=card`, { method: 'POST' })
    // 自动选中并加载
    if (firstKp) {
      await selectKp(firstKp)
    }
    await loadCards(targetNodeId)
  } catch {}
}

async function delCard(card) {
  try {
    await fetch(`${API}/api/learning/resources/${card.id}`, { method: 'DELETE' })
    await loadCards(selectedKp.value)
  } catch {}
}

function goCard(card) {
  router.push(`/learning-center/node-content/${selectedKp.value}?resourceId=${card.id}`)
}

async function addChapter() {
  const t = newChapterTitle.value.trim()
  if (!t) return
  await fetch(`${API}/api/learning/paths/${pathId}/nodes?title=${encodeURIComponent(t)}&parent_id=0`)
  newChapterTitle.value = ''
  await loadPath()
}

async function loadPath() {
  try {
    const r = await fetch(`${API}/api/learning/paths/${pathId}`)
    const d = await r.json()
    path.value = d
    allNodes.value = d.nodes || []

    // 默认展开所有章节
    const chIds = chapters.value.map(c => c.id)
    expandedChapters.value = new Set(chIds)

    // 如果还没有选中的知识点，默认选第一个
    if (!selectedKp.value) {
      const firstChild = allNodes.value.find(n => n.parent_id > 0)
      if (firstChild) {
        await selectKp(firstChild)
      }
    }
  } catch {}
}

onMounted(loadPath)
</script>

<style scoped>
.lpd-page { min-height: 100vh; background: #F8FAFC; padding-bottom: 60px; margin: calc(-1 * 24px) calc(-1 * var(--main-pad-x, 28px)); padding: 24px 0 84px; }
.lpd-top {
  background: linear-gradient(135deg, #EFF6FF, #FFFFFF);
  padding: 18px 28px 14px; border-bottom: 1.5px dashed #93C5FD;
}
.back-btn { background: none; border: none; color: #2563EB; font-size: 14px; cursor: pointer; padding: 0; margin-bottom: 8px; }
.back-btn:hover { color: #1D4ED8; }
.lpd-title-row { display: flex; align-items: center; gap: 10px; margin-bottom: 2px; }
.lpd-title { font-size: 20px; font-weight: 700; color: #1E293B; margin: 0; }
.lpd-diff-tag { font-size: 11px; padding: 2px 10px; border-radius: 4px; }
.lpd-diff-tag.beginner { background: #DCFCE7; color: #16A34A; }
.lpd-diff-tag.intermediate { background: #FEF3C7; color: #D97706; }
.lpd-diff-tag.advanced { background: #FEE2E2; color: #DC2626; }
.lpd-desc { font-size: 13px; color: #64748B; margin: 2px 0 8px; }
.lpd-progress-row { display: flex; align-items: center; gap: 10px; }
.lpd-progress-row .progress-bar { flex: 1; max-width: 180px; height: 5px; background: #E2E8F0; border-radius: 3px; overflow: hidden; }
.lpd-progress-row .progress-fill { height: 100%; background: #2563EB; border-radius: 3px; }
.lpd-progress-row .progress-text { font-size: 12px; color: #2563EB; font-weight: 600; }
.lpd-node-count { font-size: 12px; color: #94A3B8; }

/* 双栏 */
.lpd-body { display: flex; gap: 16px; max-width: 1000px; margin: 18px auto; padding: 0 16px; min-height: 500px; }
.lpd-left { width: 260px; min-width: 260px; }
.lpd-right { flex: 1; }
.lpd-panel-title { font-size: 14px; font-weight: 600; color: #1E293B; margin-bottom: 10px; }
.lpd-icon { width: 15px; height: 15px; color: #2563EB; vertical-align: -2.5px; margin-right: 3px; }
.lpd-icon-lg { width: 24px; height: 24px; color: #2563EB; }

/* 左：两级树 */
.lpd-tree-list { margin-bottom: 8px; }
.lpd-tree-chapter {
  display: flex; align-items: center; gap: 6px; padding: 7px 8px;
  border-radius: 6px; cursor: pointer; transition: all 0.12s;
  background: white; border: 1px solid transparent; margin-bottom: 2px;
}
.lpd-tree-chapter:hover { background: #EFF6FF; border-color: #BFDBFE; }
.lpd-tree-arrow { font-size: 9px; color: #94A3B8; width: 12px; flex-shrink: 0; }
.lpd-tree-dot { width: 7px; height: 7px; border-radius: 50%; background: #2563EB; flex-shrink: 0; }
.lpd-tree-ch-title { flex: 1; font-size: 13px; font-weight: 600; color: #1E293B; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.lpd-tree-count { font-size: 10px; color: #94A3B8; background: #F1F5F9; padding: 0 5px; border-radius: 5px; }
.lpd-tree-add-btn {
  background: none; border: none; color: #2563EB; cursor: pointer;
  font-size: 14px; font-weight: 700; padding: 0 2px; line-height: 1;
  opacity: 0; transition: opacity 0.12s;
}
.lpd-tree-chapter:hover .lpd-tree-add-btn { opacity: 1; }
.lpd-tree-add-btn:hover { color: #1D4ED8; }

.lpd-tree-kp {
  display: flex; align-items: center; gap: 6px; padding: 5px 8px 5px 30px;
  border-radius: 6px; cursor: pointer; transition: all 0.12s;
  background: transparent; border: 1px solid transparent; margin-bottom: 1px;
}
.lpd-tree-kp:hover { background: #F1F5F9; }
.lpd-tree-kp.active { background: #EFF6FF; border-color: #BFDBFE; font-weight: 500; }
.lpd-tree-kp-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }
.lpd-tree-kp-dot.pending { background: #CBD5E1; }
.lpd-tree-kp-dot.in_progress { background: #F59E0B; }
.lpd-tree-kp-dot.completed { background: #16A34A; }
.lpd-tree-kp-name { flex: 1; font-size: 12px; color: #334155; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.lpd-tree-kp-stat { font-size: 9px; color: #94A3B8; }
.lpd-tree-kp-stat.completed { color: #16A34A; }

/* 添加 */
.lpd-add-section { margin-top: 6px; }
.lpd-add-input {
  width: 100%; padding: 6px 8px; border: 1.5px dashed #CBD5E1; border-radius: 8px;
  font-size: 12px; outline: none; font-family: inherit; box-sizing: border-box; background: white;
}
.lpd-add-input:focus { border-color: #2563EB; border-style: solid; }

/* 右：卡片 */
.lpd-right-header { margin-bottom: 12px; }
.lpd-right-title {
  display: flex; align-items: center; gap: 8px; font-size: 16px; font-weight: 600; color: #1E293B; margin-bottom: 8px;
}
.lpd-rp-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.lpd-rp-dot.pending { background: #CBD5E1; }
.lpd-rp-dot.in_progress { background: #F59E0B; }
.lpd-rp-dot.completed { background: #16A34A; }
.lpd-btn-quick {
  display: block; width: 100%; padding: 10px 0; margin-bottom: 12px;
  background: #2563EB; color: white; border: none;
  border-radius: 8px; font-size: 15px; font-weight: 600; cursor: pointer;
  font-family: inherit; transition: all 0.15s;
}
.lpd-btn-quick:hover { background: #1D4ED8; box-shadow: 0 2px 8px rgba(37,99,235,0.2); }
.lpd-search-row { margin-bottom: 10px; }
.lpd-search-input {
  width: 100%; padding: 7px 10px; border: 1.5px solid #E2E8F0; border-radius: 8px;
  font-size: 12px; outline: none; font-family: inherit; box-sizing: border-box; background: white;
}
.lpd-search-input:focus { border-color: #2563EB; }
.lpd-empty-sm { text-align: center; color: #94A3B8; padding: 40px 0; font-size: 13px; }
.lpd-empty-lg { text-align: center; color: #94A3B8; padding: 80px 0; font-size: 14px; }

.lpd-card-grid { display: flex; flex-wrap: wrap; gap: 10px; }
.lpd-card-item {
  position: relative; width: 160px; min-height: 100px;
  background: white; border: 1.5px dashed #CBD5E1; border-radius: 10px;
  padding: 14px; cursor: pointer; transition: all 0.12s;
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px;
}
.lpd-card-item:hover { border-color: #2563EB; box-shadow: 0 2px 8px rgba(37,99,235,0.1); }
.lpd-card-icon { font-size: 24px; }
.lpd-card-title { font-size: 13px; font-weight: 500; color: #1E293B; text-align: center; line-height: 1.3; }
.lpd-card-type { font-size: 10px; color: #94A3B8; background: #F1F5F9; padding: 1px 6px; border-radius: 4px; }
.lpd-card-del {
  position: absolute; top: 4px; right: 4px;
  background: none; border: none; color: #CBD5E1; cursor: pointer; font-size: 11px; padding: 2px;
}
.lpd-card-del:hover { color: #EF4444; }

/* 弹窗 */
.lpd-overlay {
  position: fixed; inset: 0; background: rgba(15,23,42,0.4);
  display: flex; align-items: center; justify-content: center;
  z-index: 1000;
}
.lpd-dialog {
  background: white; border-radius: 12px; padding: 24px;
  width: 380px; max-width: 90vw; box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}
.lpd-dialog-title { font-size: 17px; font-weight: 700; color: #1E293B; margin-bottom: 4px; }
.lpd-dialog-sub { font-size: 12px; color: #64748B; margin-bottom: 16px; }
.lpd-dialog-input {
  width: 100%; padding: 10px 12px; border: 1.5px solid #CBD5E1; border-radius: 8px;
  font-size: 14px; outline: none; font-family: inherit; box-sizing: border-box;
}
.lpd-dialog-input:focus { border-color: #2563EB; }
.lpd-dialog-actions { display: flex; justify-content: flex-end; gap: 8px; margin-top: 16px; }
.lpd-dialog-cancel {
  padding: 8px 16px; background: #F1F5F9; color: #475569; border: none;
  border-radius: 8px; font-size: 13px; cursor: pointer; font-family: inherit;
}
.lpd-dialog-cancel:hover { background: #E2E8F0; }
.lpd-dialog-confirm {
  padding: 8px 16px; background: #2563EB; color: white; border: none;
  border-radius: 8px; font-size: 13px; cursor: pointer; font-family: inherit;
}
.lpd-dialog-confirm:hover { background: #1D4ED8; }
</style>
