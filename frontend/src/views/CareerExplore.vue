<template>
  <div class="page">
    <h2>🔍 职业探索</h2>
    <p class="hint">根据你的专业和兴趣，AI 为你推荐适合的职业方向</p>
    
    <div class="card">
      <div class="form-group">
        <label>你的专业</label>
        <input v-model="major" placeholder="例如：计算机科学与技术" />
      </div>
      <div class="form-group">
        <label>兴趣标签</label>
        <input v-model="interests" placeholder="例如：编程、设计、数据分析" />
      </div>
      <button @click="explore">🚀 开始探索</button>
    </div>

    <div v-if="results.length" class="results">
      <div v-for="(item, i) in results" :key="i" class="result-card">
        <h3>📌 {{ item.career }}</h3>
        <p class="reason">{{ item.reason }}</p>
        <div class="skills">
          <span v-for="s in item.skills" :key="s" class="tag">{{ s }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const major = ref('')
const interests = ref('')
const results = ref([])

async function explore() {
  const res = await fetch(`/api/career/explore?major=${major.value}&interests=${interests.value}`, { method: 'POST' })
  const data = await res.json()
  results.value = data.recommendations
}
</script>

<style scoped>
.page { padding: 1rem; }
.hint { color: #666; margin-bottom: 1rem; }
.card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.form-group { margin-bottom: 1rem; }
label { display: block; margin-bottom: 0.3rem; font-weight: 600; font-size: 0.9rem; }
input { width: 100%; padding: 0.6rem; border: 1px solid #ddd; border-radius: 8px; font-size: 0.95rem; }
button { background: #667eea; color: white; border: none; padding: 0.7rem 2rem; border-radius: 8px; font-size: 1rem; cursor: pointer; }
.results { margin-top: 1.5rem; }
.result-card { background: white; border-radius: 12px; padding: 1rem 1.5rem; margin-bottom: 0.8rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.reason { color: #666; font-size: 0.85rem; margin: 0.3rem 0; }
.skills { margin-top: 0.5rem; }
.tag { display: inline-block; background: #e8ecff; color: #667eea; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.8rem; margin-right: 0.4rem; }
</style>