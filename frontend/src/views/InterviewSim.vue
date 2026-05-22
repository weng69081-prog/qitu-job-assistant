<template>
  <div class="page">
    <h2>🎤 面试模拟</h2>
    <p class="hint">⭐ 核心功能 — 完整的AI模拟面试与多维度评测</p>

    <!-- 初始化 -->
    <div v-if="step === 'init'" class="card">
      <div class="form-group"><label>目标岗位</label>
        <select v-model="position"><option>前端开发工程师</option><option>后端开发工程师</option><option>算法工程师</option></select>
      </div>
      <div class="form-group"><label>面试题型</label>
        <select v-model="questionType"><option>基础知识</option><option>算法题</option><option>项目经验</option></select>
      </div>
      <div class="form-group"><label>面试时长</label>
        <select v-model="duration"><option :value="15">15分钟</option><option :value="30">30分钟</option></select>
      </div>
      <button @click="startInterview">🎬 开始面试</button>
    </div>

    <!-- 面试中 -->
    <div v-else-if="step === 'answering'" class="card">
      <div class="question-box">
        <p class="q-label">第 {{ currentQ }} / {{ totalQ }} 题</p>
        <p class="q-text">{{ question }}</p>
      </div>
      <div class="form-group">
        <label>你的回答（后续将支持语音输入）</label>
        <textarea v-model="answer" rows="4" placeholder="请输入你的回答..."></textarea>
      </div>
      <button @click="submitAnswer">📤 提交回答</button>
    </div>

    <!-- 打分结果 -->
    <div v-else-if="step === 'scoring'" class="card">
      <h3>📊 本题得分</h3>
      <div class="scores">
        <div class="score-item">技术 <b>{{ score.tech }}</b></div>
        <div class="score-item">表达 <b>{{ score.express }}</b></div>
        <div class="score-item">仪态 <b>{{ score.emotion }}</b></div>
      </div>
      <p class="comment">💬 {{ comment }}</p>
      <button @click="nextQuestion" v-if="currentQ < totalQ">➡️ 下一题</button>
      <button @click="finishInterview" v-else>📋 查看报告</button>
    </div>

    <!-- 最终报告 -->
    <div v-else-if="step === 'report'" class="card">
      <h3>📋 面试报告</h3>
      <p class="overall">综合得分：<b>{{ overall }}</b></p>
      <div class="scores">
        <div class="score-item">技术：{{ scores.tech }}</div>
        <div class="score-item">表达：{{ scores.express }}</div>
        <div class="score-item">仪态：{{ scores.emotion }}</div>
      </div>
      <div class="suggestions">
        <h4>💡 改进建议</h4>
        <li v-for="s in suggestions" :key="s">{{ s }}</li>
      </div>
      <button @click="reset">🔄 重新面试</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const step = ref('init')
const position = ref('前端开发工程师')
const questionType = ref('基础知识')
const duration = ref(15)
const question = ref('')
const currentQ = ref(1)
const totalQ = ref(5)
const answer = ref('')
const score = ref({ tech: 0, express: 0, emotion: 0 })
const comment = ref('')
const overall = ref(0)
const scores = ref({ tech: 0, express: 0, emotion: 0 })
const suggestions = ref([])

async function startInterview() {
  const res = await fetch(`/api/interview/start?position=${position.value}&question_type=${questionType.value}&duration=${duration.value}`, { method: 'POST' })
  const data = await res.json()
  question.value = data.question; totalQ.value = data.total_questions; currentQ.value = 1
  step.value = 'answering'
}
async function submitAnswer() {
  const res = await fetch(`/api/interview/submit?answer_text=${answer.value}`, { method: 'POST' })
  const data = await res.json()
  score.value = { tech: data.score_tech, express: data.score_express, emotion: data.score_emotion }
  comment.value = data.comment; answer.value = ''
  step.value = 'scoring'
}
async function nextQuestion() {
  currentQ.value++
  const res = await fetch('/api/interview/start', { method: 'POST' })
  const data = await res.json()
  question.value = data.question
  step.value = 'answering'
}
async function finishInterview() {
  const res = await fetch('/api/interview/report', { method: 'POST' })
  const data = await res.json()
  overall.value = data.overall_score; scores.value = data.scores; suggestions.value = data.suggestions
  step.value = 'report'
}
function reset() { step.value = 'init' }
</script>

<style scoped>
.page { padding: 1rem; } .hint { color: #666; margin-bottom: 1rem; }
.card { background: white; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.form-group { margin-bottom: 1rem; } label { display: block; margin-bottom: 0.3rem; font-weight: 600; font-size: 0.9rem; }
select, textarea, input { width: 100%; padding: 0.6rem; border: 1px solid #ddd; border-radius: 8px; font-size: 0.95rem; }
button { background: #667eea; color: white; border: none; padding: 0.7rem 2rem; border-radius: 8px; font-size: 1rem; cursor: pointer; margin-top: 0.5rem; margin-right: 0.5rem; }
.question-box { background: #f0f2ff; border-radius: 10px; padding: 1rem; margin-bottom: 1rem; }
.q-label { font-size: 0.8rem; color: #888; }
.q-text { font-size: 1.1rem; margin-top: 0.5rem; }
.scores { display: flex; gap: 1rem; margin: 1rem 0; }
.score-item { background: #f0f2ff; padding: 0.5rem 1rem; border-radius: 8px; }
.comment { color: #555; margin: 0.5rem 0; }
.overall { font-size: 1.3rem; margin: 0.5rem 0; }
.suggestions { margin-top: 1rem; } .suggestions li { margin: 0.3rem 0; color: #555; }
</style>