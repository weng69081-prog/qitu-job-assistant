<template>
  <div class="lnd-page">
    <div class="lnd-banner">
      <button class="back-btn" @click="$router.push('/learning-center')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>
        返回学习中心
      </button>
      <h1 class="lnd-title">{{ pathData.title || '学习路线' }}</h1>
      <p class="lnd-desc">{{ pathData.description }}</p>
      <div class="lnd-progress">
        <div class="progress-bar"><div class="progress-fill" :style="{ width: pathData.progress + '%' }"></div></div>
        <span>{{ pathData.progress }}%</span>
      </div>
    </div>

    <div class="lnd-body">
      <!-- 搜索框 -->
      <div class="search-bar">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
        <input v-model="searchQuery" class="search-input" placeholder="搜索节点名称..." />
      </div>

      <!-- 节点卡片网格 -->
      <div class="node-grid">
        <div v-for="(node, i) in filteredNodes" :key="node.id" class="node-card" :class="node.status" @click="goDetail(node.id)">
          <div class="node-index">{{ i + 1 }}</div>
          <div class="node-content">
            <div class="node-header">
              <span class="node-title">{{ node.title }}</span>
              <span class="node-diff" :class="node.difficulty">{{ diffLabel(node.difficulty) }}</span>
              <span class="node-status-tag" :class="node.status">{{ statusLabel(node.status) }}</span>
            </div>
            <div class="node-desc">{{ node.description }}</div>
            <div class="node-meta">
              <span>⏱ {{ node.duration }}</span>
              <span v-if="nodeResources[node.id]"><BookOpen class="ic-sm" /> {{ nodeResources[node.id].length }}个资源</span>
            </div>
          </div>
        </div>
      </div>
      <div v-if="!nodes.length" class="empty-state">暂无节点数据</div>
      <div v-if="nodes.length && !filteredNodes.length" class="empty-state">没有匹配的节点</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { BookOpen } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const API = 'http://localhost:8000'
const pathId = route.params.nodeId
const pathData = ref({})
const nodes = ref([])
const nodeResources = ref({})
const searchQuery = ref('')

const filteredNodes = computed(() => {
  if (!searchQuery.value.trim()) return nodes.value
  const q = searchQuery.value.trim().toLowerCase()
  return nodes.value.filter(n => n.title.toLowerCase().includes(q) || n.description.toLowerCase().includes(q))
})

function diffLabel(d) {
  return { easy: '入门', medium: '中等', hard: '困难' }[d] || d
}
function statusLabel(s) {
  return { pending: '待开始', in_progress: '进行中', completed: '已完成' }[s] || s
}

function goDetail(nodeId) {
  router.push('/learning-center/node-content/' + nodeId)
}

async function fetchDetail() {
  try {
    const r = await fetch(`${API}/api/learning/paths/${pathId}`)
    const d = await r.json()
    if (d.error) return
    pathData.value = d
    nodes.value = d.nodes || []
    const promises = (d.nodes || []).map(async (node) => {
      try {
        const rr = await fetch(`${API}/api/learning/resources?node_id=${node.id}`)
        const rd = await rr.json()
        if (rd.items && rd.items.length) {
          nodeResources.value[node.id] = rd.items
        }
      } catch {}
    })
    await Promise.all(promises)
  } catch {}
}

onMounted(fetchDetail)
</script>

<style scoped>
.lnd-page { min-height: 100vh; background: #F8FAFC; padding-bottom: 60px; }
.lnd-banner {
  background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
  padding: 24px 40px; border-bottom: 1.5px dashed #93C5FD;
}
.back-btn {
  display: flex; align-items: center; gap: 6px;
  background: none; border: none; color: #2563EB;
  font-size: 14px; cursor: pointer; padding: 0; margin-bottom: 12px;
}
.lnd-title { font-size: 22px; font-weight: 700; color: #1E293B; margin-bottom: 6px; }
.lnd-desc { font-size: 14px; color: #64748B; margin-bottom: 12px; }
.lnd-progress { display: flex; align-items: center; gap: 10px; max-width: 300px; }
.progress-bar { flex: 1; height: 6px; background: #DBEAFE; border-radius: 3px; overflow: hidden; }
.progress-fill { height: 100%; background: #2563EB; border-radius: 3px; }
.lnd-body { padding: 24px 32px; }

/* 搜索框 */
.search-bar {
  display: flex; align-items: center; gap: 8px;
  background: white; border: 1.5px solid #E2E8F0; border-radius: 10px;
  padding: 10px 14px; margin-bottom: 20px; transition: border-color 0.2s;
}
.search-bar:focus-within { border-color: #2563EB; }
.search-input {
  flex: 1; border: none; outline: none; font-size: 14px; font-family: inherit; color: #1E293B;
}
.search-input::placeholder { color: #94A3B8; }

/* 节点卡片网格 */
.node-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 14px; }
.node-card {
  display: flex; gap: 14px; background: white; border-radius: 12px;
  padding: 18px; border: 1.5px dashed #93C5FD; cursor: pointer;
  transition: all 0.2s;
}
.node-card:hover { border-color: #2563EB; box-shadow: 0 2px 12px rgba(37,99,235,0.1); transform: translateY(-1px); }
.node-card.completed { opacity: 0.7; border-color: #86EFAC; background: #F0FDF4; }
.node-index {
  width: 32px; height: 32px; min-width: 32px; background: #2563EB; color: white;
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-size: 14px; font-weight: 700;
}
.node-card.completed .node-index { background: #16A34A; }
.node-content { flex: 1; min-width: 0; }
.node-header { display: flex; align-items: center; gap: 6px; margin-bottom: 4px; flex-wrap: wrap; }
.node-title { font-size: 15px; font-weight: 600; color: #1E293B; }
.node-diff { font-size: 11px; padding: 1px 8px; border-radius: 4px; }
.node-diff.easy { background: #DCFCE7; color: #16A34A; }
.node-diff.medium { background: #FEF3C7; color: #D97706; }
.node-diff.hard { background: #FEE2E2; color: #DC2626; }
.node-status-tag { font-size: 11px; padding: 1px 8px; border-radius: 4px; }
.node-status-tag.completed { background: #DCFCE7; color: #16A34A; }
.node-status-tag.in_progress { background: #DBEAFE; color: #2563EB; }
.node-status-tag.pending { background: #F1F5F9; color: #94A3B8; }
.node-desc { font-size: 13px; color: #64748B; margin: 4px 0; }
.node-meta { display: flex; gap: 14px; font-size: 12px; color: #94A3B8; }
.empty-state { text-align: center; padding: 40px; color: #94A3B8; }
</style>
