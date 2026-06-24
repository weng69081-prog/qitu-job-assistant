<template>
  <div class="rb-page">
    <div class="rb-banner">
      <button class="back-btn" @click="$router.push('/learning-center')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>
        返回学习中心
      </button>
      <h1 class="rb-title">复习本</h1>
      <p class="rb-sub">管理所有复习提醒，按时回顾巩固知识</p>
    </div>

    <div class="rb-controls">
      <button class="btn-sm btn-blue" @click="fetchReviews">刷新</button>
    </div>

    <div class="rb-body">
      <div v-if="reviews.length" class="review-grid">
        <div v-for="r in reviews" :key="r.id" class="review-card">
          <div class="rc-header">
            <div class="rc-title">{{ r.title || '待复习' }}</div>
            <span class="rc-count">{{ r.reviewed_count }}次</span>
          </div>
          <div class="rc-info">
            <div class="rc-row">
              <span class="rc-label">间隔</span>
              <span>{{ r.review_interval }}天</span>
            </div>
            <div class="rc-row">
              <span class="rc-label">上次复习</span>
              <span>{{ r.last_reviewed_at || '未复习' }}</span>
            </div>
            <div class="rc-row">
              <span class="rc-label">下次复习</span>
              <span class="rc-next" :class="{ overdue: isOverdue(r.next_review_at) }">{{ r.next_review_at || '未设定' }}</span>
            </div>
          </div>
          <button class="btn-sm btn-blue rc-btn" @click="completeReview(r.id)">✓ 已完成</button>
        </div>
      </div>
      <div v-else class="empty-state">还没有复习提醒，去学习中心从薄弱点创建吧~ 📚</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API = ''
const reviews = ref([])

function isOverdue(dateStr) {
  if (!dateStr) return false
  return dateStr < new Date().toISOString().slice(0, 10)
}

async function fetchReviews() {
  try {
    const r = await fetch(`${API}/api/learning/reviews`)
    const d = await r.json()
    reviews.value = d.items || []
  } catch {}
}

async function completeReview(id) {
  try {
    await fetch(`${API}/api/learning/reviews/${id}/complete`, { method: 'POST' })
    await fetchReviews()
  } catch {}
}

onMounted(fetchReviews)
</script>

<style scoped>
.rb-page { min-height: 100vh; background: #F8FAFC; padding-bottom: 60px; }
.rb-banner {
  background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
  padding: 24px 40px;
  border-bottom: 1.5px dashed #93C5FD;
}
.back-btn {
  display: flex; align-items: center; gap: 6px;
  background: none; border: none; color: #2563EB;
  font-size: 14px; cursor: pointer; padding: 0; margin-bottom: 12px;
}
.rb-title { font-size: 22px; font-weight: 700; color: #1E293B; margin-bottom: 6px; }
.rb-sub { font-size: 14px; color: #64748B; }
.rb-controls { max-width: 900px; margin: 16px auto; padding: 0 16px; }
.rb-body { max-width: 900px; margin: 0 auto; padding: 0 16px 40px; }
.review-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }
.review-card {
  background: white; border-radius: 12px; padding: 20px;
  border: 1.5px dashed #93C5FD; transition: all 0.2s;
}
.review-card:hover { border-color: #2563EB; }
.rc-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.rc-title { font-size: 16px; font-weight: 600; color: #1E293B; }
.rc-count { font-size: 12px; color: #94A3B8; }
.rc-info { display: flex; flex-direction: column; gap: 6px; margin-bottom: 14px; }
.rc-row { display: flex; justify-content: space-between; font-size: 13px; color: #64748B; }
.rc-label { color: #94A3B8; }
.rc-next { font-weight: 500; color: #2563EB; }
.rc-next.overdue { color: #EF4444; }
.rc-btn { width: 100%; }
.btn-sm { padding: 6px 14px; border-radius: 8px; font-size: 13px; border: none; cursor: pointer; font-weight: 500; }
.btn-blue { background: #2563EB; color: white; }
.btn-blue:hover { background: #1D4ED8; }
.empty-state { text-align: center; padding: 60px; color: #94A3B8; }
</style>
