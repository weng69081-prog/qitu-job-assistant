<template>
  <div class="page">
    <h2>📝 简历优化</h2>
    <p class="hint">上传现有简历进行AI润色，或填写信息自动生成简历</p>

    <!-- 模式切换 -->
    <div class="tabs">
      <button :class="{ active: mode === 'optimize' }" @click="mode = 'optimize'">📄 简历润色</button>
      <button :class="{ active: mode === 'generate' }" @click="mode = 'generate'">✨ 智能生成</button>
    </div>

    <!-- 润色模式 -->
    <div v-if="mode === 'optimize'" class="card">
      <div class="form-group">
        <label>粘贴简历文本</label>
        <textarea v-model="resumeText" rows="8" placeholder="请粘贴你的简历内容..."></textarea>
      </div>
      <button @click="optimize">🔧 AI 润色</button>
      <div v-if="result.optimized" class="result-box">
        <h4>✨ 优化结果</h4>
        <pre>{{ result.optimized }}</pre>
        <h4>💡 修改建议</h4>
        <li v-for="s in result.suggestions" :key="s">{{ s }}</li>
      </div>
    </div>

    <!-- 生成模式 -->
    <div v-if="mode === 'generate'" class="card">
      <div class="form-group"><label>教育背景</label><input v-model="edu" placeholder="例如：郑州西亚斯学院 计算机科学 本科" /></div>
      <div class="form-group"><label>技能标签</label><input v-model="skills" placeholder="例如：Python, JavaScript, Vue, SQL" /></div>
      <div class="form-group"><label>项目经历</label><textarea v-model="projects" rows="3" placeholder="描述你参与过的项目..."></textarea></div>
      <div class="form-group"><label>实习经历</label><textarea v-model="experience" rows="3" placeholder="描述你的实习经历..."></textarea></div>
      <button @click="generate">✨ 生成简历</button>
      <div v-if="genResult" class="result-box">
        <h4>📋 生成的简历</h4>
        <pre>{{ genResult }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const mode = ref('optimize')
const resumeText = ref('')
const result = ref({})
const edu = ref(''), skills = ref(''), projects = ref(''), experience = ref('')
const genResult = ref('')

async function optimize() {
  const res = await fetch('/api/resume/optimize?original_text=' + encodeURIComponent(resumeText.value), { method: 'POST' })
  result.value = await res.json()
}
async function generate() {
  const res = await fetch(`/api/resume/generate?education=${encodeURIComponent(edu.value)}&skills=${encodeURIComponent(skills.value)}&projects=${encodeURIComponent(projects.value)}&experience=${encodeURIComponent(experience.value)}`, { method: 'POST' })
  const data = await res.json()
  genResult.value = data.resume
}
</script>

<style scoped>
.page { padding: 1rem; } .hint { color: #666; margin-bottom: 1rem; }
.card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.tabs { display: flex; gap: 0.5rem; margin-bottom: 1rem; }
.tabs button { background: #eee; color: #333; border: none; padding: 0.5rem 1rem; border-radius: 8px; cursor: pointer; }
.tabs button.active { background: #667eea; color: white; }
.form-group { margin-bottom: 1rem; } label { display: block; margin-bottom: 0.3rem; font-weight: 600; font-size: 0.9rem; }
input, textarea { width: 100%; padding: 0.6rem; border: 1px solid #ddd; border-radius: 8px; font-size: 0.95rem; }
button { background: #667eea; color: white; border: none; padding: 0.7rem 1.5rem; border-radius: 8px; font-size: 0.95rem; cursor: pointer; }
.result-box { margin-top: 1rem; background: #f8f9ff; border-radius: 10px; padding: 1rem; }
.result-box pre { white-space: pre-wrap; font-size: 0.9rem; }
.result-box li { color: #555; margin: 0.2rem 0; }
</style>