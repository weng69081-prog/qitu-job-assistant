<template>
  <div class="setup-page">
    <div class="sign-wrapper">
      <!-- ═══ 品牌 ═══ -->
      <div class="brand-logo-area">
        <div class="brand-title">启途</div>
        <div class="brand-slogan">完善资料 · 开启职业探索</div>
      </div>

      <!-- ═══ 磨砂玻璃卡片 ═══ -->
      <div class="setup-card">
        <img src="/src/assets/auth-cat.png" class="setup-cat" alt="" />

        <!-- 昵称 + 年级 -->
        <div class="form-field">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inp-icon"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          <input v-model="form.nickname" placeholder="你的昵称" @focus="errs.nickname=''" />
        </div>
        <p v-if="errs.nickname" class="error-msg">
          <svg viewBox="0 0 24 24" fill="none" stroke="#f56c6c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          {{ errs.nickname }}
        </p>

        <div class="form-field">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inp-icon"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
          <select v-model="form.grade">
            <option value="大一">大一</option>
            <option value="大二">大二</option>
            <option value="大三">大三</option>
            <option value="大四">大四</option>
            <option value="研一">研一</option>
            <option value="研二">研二</option>
            <option value="研三">研三</option>
            <option value="已毕业">已毕业</option>
          </select>
        </div>

        <!-- 专业大类 + 具体专业 -->
        <div class="form-field" :class="{error: errs.majorCategory}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inp-icon"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg>
          <select v-model="form.majorCategory" @change="onMajorCategoryChange">
            <option value="">选择专业大类</option>
            <option v-for="c in majorCategories" :key="c" :value="c">{{ c }}</option>
          </select>
        </div>
        <p v-if="errs.majorCategory" class="error-msg">
          <svg viewBox="0 0 24 24" fill="none" stroke="#f56c6c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          请选择专业大类
        </p>

        <div class="form-field" :class="{error: errs.major}">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="inp-icon"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/><line x1="8" y1="7" x2="16" y2="7"/><line x1="8" y1="11" x2="12" y2="11"/></svg>
          <select v-model="form.major">
            <option value="">选择具体专业</option>
            <option v-for="m in majorOptions" :key="m" :value="m">{{ m }}</option>
          </select>
        </div>
        <p v-if="errs.major" class="error-msg">
          <svg viewBox="0 0 24 24" fill="none" stroke="#f56c6c" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="13" height="13"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          请选择具体专业
        </p>

        <!-- 兴趣方向（标签选择） -->
        <p class="field-label">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
          兴趣方向（选填）
        </p>
        <div class="tags-grid">
          <span v-for="interest in interestOptions" :key="interest"
                class="tag-item" :class="{active: form.interests.includes(interest)}"
                @click="toggleInterest(interest)">{{ interest }}</span>
        </div>

        <!-- 学习困惑 -->
        <p class="field-label" style="margin-top:.9rem">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          学习困惑（选填）
        </p>
        <div class="form-field textarea-field">
          <textarea v-model="form.confusion" :rows="2" placeholder="目前对专业学习/未来方向最迷茫的问题…（如：不知道该学什么编程语言）"></textarea>
        </div>

        <!-- 提交 -->
        <button class="submit-btn" :class="{loading}" @click="save" :disabled="loading">
          <svg v-if="loading" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin" width="16" height="16"><path d="M21 12a9 9 0 1 1-6.219-8.56"/></svg>
          <template v-else>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
            保存信息，开启探索
          </template>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loading = ref(false)
const errs = reactive({ nickname: '', majorCategory: '', major: '' })
const majorOptions = ref([])

const majorCategories = ['计算机类','机电土木类','经管财会类','文法艺术类','医药护理类','教育师范类','农林类','轻工制造类']

const interestOptions = [
  '前端开发', '后端开发', '移动开发', '网络安全',
  '人工智能', '大数据', '软件测试', '产品经理',
  'UI/UX设计', '运维技术', '新媒体运营', '暂无明确兴趣'
]

const majorMap = {
  '计算机类': ['计算机科学与技术','软件工程','人工智能','数据科学与大数据','网络工程','信息安全','物联网工程','数字媒体技术','智能科学与技术'],
  '机电土木类': ['机械工程','电气工程','自动化','土木工程','车辆工程','测控技术','能源动力','机器人工程'],
  '经管财会类': ['金融学','会计学','工商管理','市场营销','人力资源管理','国际经济与贸易','电子商务','物流管理'],
  '文法艺术类': ['法学','新闻学','汉语言文学','广告学','视觉传达设计','数字媒体艺术','英语','行政管理'],
  '医药护理类': ['临床医学','护理学','药学','医学检验技术','口腔医学','预防医学','中医学','康复治疗学'],
  '教育师范类': ['教育学','学前教育','小学教育','学科教学(数学)','学科教学(语文)','学科教学(英语)','教育技术学','特殊教育'],
  '农林类': ['农学','园艺','植物保护','动物科学','食品科学与工程','林学','农业资源与环境','水产养殖学'],
  '轻工制造类': ['工业设计','材料科学与工程','纺织工程','包装工程','化学工程与工艺','环境工程','生物工程','安全工程'],
}

const form = reactive({
  nickname: '',
  grade: '大一',
  majorCategory: '',
  major: '',
  interests: [],
  confusion: '',
})

function onMajorCategoryChange() {
  form.major = ''
  majorOptions.value = majorMap[form.majorCategory] || []
}

function toggleInterest(interest) {
  const idx = form.interests.indexOf(interest)
  if (idx >= 0) form.interests.splice(idx, 1)
  else form.interests.push(interest)
}

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) { router.push('/login'); return }
  try {
    const res = await fetch(`/api/user/profile?token=${encodeURIComponent(token)}`)
    if (!res.ok) return
    const data = await res.json()
    form.nickname = data.nickname || ''
    const p = data.profile || {}
    if (p.major_category || p.major || p.interests) {
      form.majorCategory = p.major_category || ''
      form.major = p.major || ''
      form.grade = p.grade || '大一'
      if (p.interests) form.interests = p.interests.split(',').filter(Boolean)
      form.confusion = p.confusion || ''
      if (form.majorCategory) majorOptions.value = majorMap[form.majorCategory] || []
    }
  } catch(e) {}
})

async function save() {
  const token = localStorage.getItem('token')
  if (!token) { ElMessage.warning('请先登录'); return }
  errs.nickname = errs.majorCategory = errs.major = ''
  if (!form.nickname.trim()) { errs.nickname = '请输入你的昵称'; return ElMessage.warning('请填写你的昵称') }
  if (!form.majorCategory) { errs.majorCategory = '请选择专业大类'; return ElMessage.warning('请选择专业大类') }
  if (!form.major) { errs.major = '请选择具体专业'; return ElMessage.warning('请选择具体专业') }
  loading.value = true
  try {
    const qs = new URLSearchParams({
      token,
      nickname: form.nickname,
      major_category: form.majorCategory,
      major: form.major,
      grade: form.grade,
      interests: form.interests.join(','),
      confusion: form.confusion,
      education: '本科',
    })
    const res = await fetch('/api/user/profile?' + qs, { method:'POST' })
    if (!res.ok) {
      const errBody = await res.text()
      throw new Error(`服务器返回 ${res.status}: ${errBody}`)
    }
    localStorage.removeItem('needs_profile')
    ElMessage.success('信息已保存！开启你的专业探索之旅 🚀')
    router.push('/career')
  } catch(e) {
    ElMessage.error('保存失败：' + e.message)
  } finally { loading.value = false }
}
</script>

<style scoped>
/* ═══ 页面 — 全屏背景图 ═══ */
.setup-page {
  min-height: 100vh;
  width: 100%;
  background: url('/auth-bg-watercolor-clean.png') center/cover no-repeat fixed;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

/* ═══ 微遮罩（同登录页） ═══ */
.setup-page::before {
  content: '';
  position: fixed; inset:0;
  background: rgba(0,0,0,0.05);
  z-index: 0;
}

/* ═══ 外层容器 ═══ */
.sign-wrapper {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  padding: 20px;
}

/* ═══ 品牌 ═══ */
.brand-logo-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 26px;
}
.brand-title {
  font-size: 52px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 10px;
  line-height: 1;
  text-shadow: 0 2px 8px rgba(0,0,0,0.12);
}
.brand-slogan {
  font-size: 16px;
  color: rgba(255,255,255,0.75);
  margin-top: 10px;
  text-shadow: 0 1px 4px rgba(0,0,0,0.08);
}

/* ═══ 磨砂玻璃卡片 ═══ */
.setup-card {
  width: 480px;
  max-width: 100%;
  background: rgba(255,255,255,0.05);
  border-radius: 14px;
  padding: 28px 30px 30px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.45);
  position: relative;
  border: 1px solid rgba(255,255,255,0.35);
}

/* ═══ 小猫 ═══ */
.setup-cat {
  position: absolute;
  top: -66px;
  right: 10px;
  width: 80px;
  z-index: 2;
  pointer-events: none;
}

/* ═══ 字段提示 ═══ */
.field-label {
  font-size: 13px;
  color: rgba(25,27,31,0.65);
  margin: 0 0 8px 0;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* ═══ 表单字段 ═══ */
.form-field {
  display: flex;
  align-items: center;
  background: rgba(255,255,255,0.5);
  border: 1px solid rgba(235,236,237,0.7);
  border-radius: 10px;
  padding: 0 14px;
  margin-bottom: 10px;
  transition: border-color .2s, box-shadow .2s;
}
.form-field:focus-within {
  border-color: #1772f6;
  box-shadow: 0 0 0 3px rgba(23,114,246,0.08);
}
.form-field.error { border-color: #f56c6c; }

.inp-icon {
  width: 17px;
  height: 17px;
  color: #8590a6;
  flex-shrink: 0;
  margin-right: 10px;
  transition: color .2s;
}
.form-field:focus-within .inp-icon { color: #1772f6; }

.form-field input,
.form-field select {
  flex: 1;
  border: none;
  outline: none;
  font-size: 14px;
  padding: 11px 0;
  background: transparent;
  color: #191b1f;
  font-family: inherit;
}
.form-field input::placeholder { color: #8590a6; }
.form-field select { cursor: pointer; }
.form-field select option:first-child { color: #8590a6; }

.form-field.textarea-field { padding: 8px 14px; }
.form-field textarea {
  flex: 1; border: none; outline: none;
  font-size: 14px; padding: 3px 0;
  background: transparent; color: #191b1f;
  resize: vertical; min-height: 44px;
  font-family: inherit; line-height: 1.4;
}
.form-field textarea::placeholder { color: #8590a6; }

.error-msg {
  color: #f56c6c;
  font-size: 12px;
  margin: -6px 0 8px 2px;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* ═══ 兴趣标签 ═══ */
.tags-grid { display: flex; flex-wrap: wrap; gap: 6px; }
.tag-item {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  border: 1.5px solid rgba(235,236,237,0.7);
  background: rgba(255,255,255,0.4);
  color: #8590a6;
  transition: all .2s;
}
.tag-item:hover { border-color: #1772f6; color: #1772f6; }
.tag-item.active { background: #1772f6; color: #fff; border-color: #1772f6; }

/* ═══ 提交按钮（同登录页） ═══ */
.submit-btn {
  width: 100%;
  height: 42px;
  border: none;
  border-radius: 8px;
  background: #1772f6;
  color: #fff;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  font-family: inherit;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 12px;
  transition: background .2s, transform .15s;
}
.submit-btn:hover:not(:disabled) { background: #1565db; transform: translateY(-1px); }
.submit-btn:disabled { opacity: .7; cursor: not-allowed; }
.submit-btn.loading { pointer-events: none; }

.spin { animation: spin 1s linear infinite; }
@keyframes spin { to{transform:rotate(360deg)} }
</style>