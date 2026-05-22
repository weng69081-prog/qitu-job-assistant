<template>
  <div class="page">
    <h2>📊 投递分析</h2>
    <p class="hint">对比你的简历和目标岗位，查看匹配度并获得公司推荐</p>

    <div class="card">
      <div class="form-group">
        <label>目标岗位 JD</label>
        <textarea v-model="jdText" rows="6" placeholder="请粘贴目标岗位的职位描述..."></textarea>
      </div>
      <div class="form-group">
        <label>你的简历</label>
        <textarea v-model="resumeText2" rows="6" placeholder="请粘贴你的简历内容..."></textarea>
      </div>
      <button @click="analyze">🔍 开始分析</button>
    </div>

    <div v-if="matchScore !== null" class="results">
      <!-- 匹配度 -->
      <div class="card match-card">
        <h3>📊 匹配度：<span class="big-score">{{ matchScore }}%</span></h3>
        <div class="bar"><div class="bar-fill" :style="{ width: matchScore + '%' }"></div></div>
      </div>

      <!-- 逐项分析 -->
      <div class="card">
        <h4>📋 逐项分析</h4>
        <div v-for="(d, i) in details" :key="i" class="detail-item" :class="d.status">
          <span>{{ d.requirement }}</span>
          <span class="status-badge">{{ d.status === 'match' ? '✅' : d.status === 'partial' ? '⚠️' : '❌' }}</span>
          <span class="detail-comment">{{ d.comment }}</span>
        </div>
      </div>

      <!-- 公司推荐 -->
      <div class="card">
        <h4>🏢 推荐公司</h4>
        <div v-for="(c, i) in companies" :key="i" class="company-item">
          <h5>{{ c.name }}</h5>
          <p>匹配度：{{ c.match }}% — {{ c.reason }}</p>
        </div>
      </div>

      <!-- 建议 -->
      <div class="card">
        <h4>💡 提升建议</h4>
        <li v-for="(s, i) in suggestions2" :key="i">{{ s }}</li>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const jdText = ref('')
const resumeText2 = ref('')
const matchScore = ref(null)
const details = ref([])
const companies = ref([])
const suggestions2 = ref([])

async function analyze() {
  const res = await fetch(`/api/jobmatch/analyze?jd_text=${encodeURIComponent(jdText.value)}&resume_text=${encodeURIComponent(resumeText2.value)}`, { method: 'POST' })
  const data = await res.json()
  matchScore.value = data.match_score
  details.value = data.details
  companies.value = data.companies
  suggestions2.value = data.suggestions
}
</script>

<style scoped>
.page { padding: 1rem; } .hint { color: #666; margin-bottom: 1rem; }
.card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 1rem; }
.form-group { margin-bottom: 1rem; } label { display: block; margin-bottom: 0.3rem; font-weight: 600; font-size: 0.9rem; }
textarea { width: 100%; padding: 0.6rem; border: 1px solid #ddd; border-radius: 8px; font-size: 0.95rem; }
button { background: #667eea; color: white; border: none; padding: 0.7rem 2rem; border-radius: 8px; font-size: 1rem; cursor: pointer; }
.big-score { font-size: 2rem; color: #667eea; }
.bar { background: #eee; border-radius: 10px; height: 10px; margin-top: 0.5rem; }
.bar-fill { background: linear-gradient(90deg, #667eea, #764ba2); height: 100%; border-radius: 10px; transition: width 0.5s; }
.detail-item { display: flex; gap: 0.5rem; padding: 0.5rem 0; border-bottom: 1px solid #f0f0f0; align-items: center; }
.detail-item.match .status-badge { color: #22c55e; } .detail-item.partial .status-badge { color: #f59e0b; } .detail-item.miss .status-badge { color: #ef4444; }
.detail-comment { color: #888; font-size: 0.8rem; }
.company-item { padding: 0.5rem 0; border-bottom: 1px solid #f0f0f0; }
.company-item h5 { color: #667eea; } .company-item p { color: #666; font-size: 0.85rem; }
li { color: #555; margin: 0.2rem 0; }
</style>