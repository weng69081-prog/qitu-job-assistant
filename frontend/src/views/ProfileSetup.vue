<template>
  <div class="setup-page">
    <!-- ═══ 背景云朵装饰 ═══ -->
    <div class="setup-sky">
      <div class="sky-cloud sc-1"></div>
      <div class="sky-cloud sc-2"></div>
      <div class="sky-cloud sc-3"></div>
      <div class="sky-cloud sc-4"></div>
      <div class="sky-cloud sc-5"></div>
      <div class="sky-cloud sc-6"></div>
    </div>

    <!-- ═══ 左侧品牌区（不动） ═══ -->
    <div class="brand-panel">
      <div class="brand-content">
        <div class="brand-logo">
          <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="22" height="22">
            <circle cx="12" cy="12" r="10"/>
            <polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>
          </svg>
        </div>
        <h1 class="brand-title">启途</h1>
        <p class="brand-sub">QITU · AI 求职助手</p>
        <p class="brand-tagline">完善基础信息 · 开启职业探索<br>更精准的推荐 · 从了解你开始</p>
        <div class="brand-features">
          <div class="brand-feature-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14">
              <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/>
            </svg>
            <span>昵称与专业</span>
          </div>
          <div class="brand-feature-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14">
              <circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>
            </svg>
            <span>兴趣方向</span>
          </div>
          <div class="brand-feature-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="14" height="14">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
            </svg>
            <span>学习困惑</span>
          </div>
        </div>
        <div class="brand-quote">「了解你，才能更好地帮你」</div>
      </div>
    </div>

    <!-- ═══ 右侧淡灰底 + 白卡片表单 ═══ -->
    <div class="form-panel">
      <div class="setup-welcome">
        <h2>完善资料</h2>
        <p>只需几分钟，让启途更懂你</p>
      </div>

      <div class="form-card">
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
/* ═══ 页面布局 ═══ */
.setup-page {
  display: flex;
  min-height: 100vh;
  width: 100%;
  position: relative;
  background: linear-gradient(180deg,#6FA3C8 0%,#8DB8D8 25%,#B0D0E4 50%,#D0E4F0 75%,#E8F0F5 100%);
  overflow: hidden;
}

/* ═══ 背景云朵 ═══ */
.setup-sky {
  position: absolute; inset:0;
  pointer-events:none; overflow:hidden;
}
.setup-sky .sky-cloud {
  position:absolute; border-radius:50%;
  background:rgba(255,255,255,.45); filter:blur(40px);
  will-change:transform;
}
.sc-1 { width:500px; height:120px; top:5%; left:-8%; animation:cloudA 120s linear infinite; }
.sc-2 { width:400px; height:100px; top:15%; left:40%; animation:cloudB 140s linear infinite; }
.sc-3 { width:350px; height:85px; top:55%; left:65%; animation:cloudA 100s linear infinite; }
.sc-4 { width:300px; height:70px; top:70%; left:20%; animation:cloudB 90s linear infinite; }
.sc-5 { width:180px; height:45px; top:40%; left:80%; animation:cloudA 70s linear infinite; }
.sc-6 { width:250px; height:60px; top:80%; left:-5%; animation:cloudB 85s linear infinite; }
@keyframes cloudA { 0%{transform:translateX(0)} 100%{transform:translateX(1200px)} }
@keyframes cloudB { 0%{transform:translateX(0)} 100%{transform:translateX(1000px)} }

/* ═══ 左侧品牌区 ═══ */
.brand-panel {
  width: 35%;
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(155deg, rgba(61,90,128,.88) 0%, rgba(74,107,148,.72) 60%, rgba(142,160,184,.55) 100%);
  backdrop-filter: blur(4px);
}
.brand-content {
  position:relative; z-index:1; text-align:center;
  color:#fff; padding:2rem; display:flex;
  flex-direction:column; align-items:center;
}
.brand-logo {
  width:56px; height:56px; border-radius:16px;
  background:rgba(255,255,255,.15); backdrop-filter:blur(8px);
  display:flex; align-items:center; justify-content:center;
  margin-bottom:8px;
}
.brand-title { font-size:2.2rem; font-weight:800; letter-spacing:6px; margin-bottom:2px; text-shadow:0 2px 12px rgba(0,0,0,.08); }
.brand-sub { font-size:.78rem; color:rgba(255,255,255,.55); letter-spacing:4px; margin-bottom:14px; }
.brand-tagline { font-size:.85rem; color:rgba(255,255,255,.75); line-height:1.7; max-width:240px; margin:0 auto 24px; }
.brand-features { display:flex; flex-wrap:wrap; justify-content:center; gap:8px 14px; margin-bottom:20px; }
.brand-feature-item {
  display:flex; align-items:center; gap:6px; font-size:.8rem;
  color:rgba(255,255,255,.7); background:rgba(255,255,255,.1);
  padding:5px 12px; border-radius:20px; backdrop-filter:blur(4px);
  border:1px solid rgba(255,255,255,.06);
}
.brand-feature-item svg { color:#8EA0B8; flex-shrink:0; }
.brand-quote { font-size:.82rem; color:rgba(255,255,255,.4); font-style:italic; letter-spacing:1px; margin-top:6px; }

/* ═══ 表单上方趴边猫 ═══ */
.setup-cat {
  position: absolute;
  top: -70px;
  right: 20px;
  width: 90px;
  z-index: 5;
  pointer-events: none;
}

/* ═══ 白色卡片 ═══ */
.form-card {
  width: 100%;
  max-width: 480px;
  background: #ffffff;
  border-radius: 18px;
  padding: 2.4rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, .08);
  position: relative;
  animation: fadeIn .3s ease;
}

/* ═══ 右侧 — 淡灰底 ═══ */
.form-panel {
  flex: 1;
  position: relative;
  z-index: 1;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow-y: auto;
}

/* ═══ 白色区域左上角的欢迎文字 ═══ */
.setup-welcome {
  position: absolute;
  top: 4.5rem;
  left: 3.5rem;
  text-align: left;
  z-index: 2;
}
.setup-welcome h2 {
  font-size: 2.6rem;
  font-weight: 800;
  color: #1a2744;
  margin: 0 0 6px 0;
}
.setup-welcome p {
  font-size: 1.1rem;
  color: #8EA0B8;
  margin: 0;
}

@keyframes fadeIn { from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:translateY(0)} }

/* ═══ 表单字段 ═══ */
.form-field {
  display:flex; align-items:center;
  background:#fff; border:1.5px solid #D8DCE6; border-radius:12px;
  padding:0 1.1rem; margin-bottom:.6rem;
  transition:border-color .2s, box-shadow .2s;
}
.form-field:focus-within { border-color:#3D5A80; box-shadow:0 0 0 3px rgba(61,90,128,.08); }
.form-field.error { border-color:#f56c6c; }

.inp-icon {
  width:18px; height:18px; color:#8EA0B8; flex-shrink:0; margin-right:.75rem;
  transition:color .2s;
}
.form-field:focus-within .inp-icon { color:#3D5A80; }

.form-field input,
.form-field select {
  flex:1; border:none; outline:none; font-size:1rem;
  padding:.95rem 0; background:transparent; color:#4A5568;
  -webkit-appearance:none; appearance:none;
}
.form-field select { cursor:pointer; }
.form-field select option:first-child { color:#9AAEC2; }
.form-field input::placeholder { color:#9AAEC2; }

.form-field.textarea-field { padding:.5rem 1.1rem; }
.form-field textarea {
  flex:1; border:none; outline:none; font-size:.9rem;
  padding:.45rem 0; background:transparent; color:#4A5568;
  resize:vertical; min-height:46px; font-family:inherit; line-height:1.4;
}
.form-field textarea::placeholder { color:#9AAEC2; }

.error-msg {
  color:#f56c6c; font-size:.8rem;
  margin:-.2rem 0 .6rem .3rem;
  display:flex; align-items:center; gap:.3rem;
}

/* ═══ 字段标签 ═══ */
.field-label {
  display:flex; align-items:center; gap:.35rem;
  font-size:.82rem; font-weight:600; color:#1a2744;
  margin:.6rem 0 .35rem;
}

/* ═══ 兴趣标签 ═══ */
.tags-grid { display:flex; flex-wrap:wrap; gap:.4rem; }
.tag-item {
  display:inline-block; padding:.38rem .65rem; border-radius:20px;
  font-size:.8rem; cursor:pointer; border:1.5px solid #D8DCE6;
  background:#fff; color:#8EA0B8; transition:all .2s;
}
.tag-item:hover { border-color:#3D5A80; color:#3D5A80; }
.tag-item.active { background:#3D5A80; color:#fff; border-color:#3D5A80; }

/* ═══ 提交按钮 ═══ */
.submit-btn {
  width:100%; padding:.95rem; border:none; border-radius:12px;
  background:linear-gradient(135deg,#3D5A80,#2C4460);
  color:#fff; font-size:1rem; font-weight:600;
  cursor:pointer; transition:transform .15s, box-shadow .2s, opacity .2s;
  display:flex; align-items:center; justify-content:center; gap:.4rem;
  margin-top:1.2rem;
}
.submit-btn:hover:not(:disabled) { transform:translateY(-1px); box-shadow:0 6px 20px rgba(61,90,128,.25); }
.submit-btn:disabled { opacity:.7; cursor:not-allowed; }
.submit-btn.loading { pointer-events:none; }
.submit-btn svg { flex-shrink:0; }

.spin { animation: spin 1s linear infinite; }
@keyframes spin { to{transform:rotate(360deg)} }

/* ═══ 响应式 ═══ */
@media (max-width:1100px) {
  .brand-panel { width: 32%; }
}
@media (max-width:900px) {
  .setup-page { flex-direction: column; }
  .brand-panel { width:100%; min-height:170px; }
  .brand-title { font-size:1.6rem; }
  .form-panel { padding:2rem 1rem; }
  .setup-welcome { position: static; text-align: center; margin-bottom: 1rem; }
  .form-card { max-width:480px; }
}
@media (max-width:480px) {
  .brand-panel { min-height:140px; }
  .form-card { padding:1.6rem 1.2rem; }
  .form-field input,
  .form-field select { font-size:.95rem; padding:.8rem 0; }
  .submit-btn { padding:.8rem; font-size:.95rem; }
}
</style>