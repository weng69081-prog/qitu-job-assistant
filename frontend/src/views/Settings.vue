<template>
  <div class="settings-page">
    <!-- ═══ 顶部横幅（类首页欢迎风格） ═══ -->
    <div class="settings-banner">
      <div class="banner-left">
        <h1 class="banner-title">个人设置</h1>
        <p class="banner-desc">管理你的账号、个人信息与应用配置</p>
      </div>
      <div class="banner-right">
        <span class="qitu-watermark">QITU</span>
        <img src="/src/assets/xiaoju-on-banner.png" class="banner-cat" alt="小橘">
      </div>
      <div class="banner-glow"></div>
    </div>

    <!-- ═══ 表单区域 ═══ -->
    <div class="settings-body">

      <!-- ─── ① 基础信息 ─── -->
      <div class="set-card">
        <div class="set-card-header">
          <User :size="16" color="#2563EB" />
          <span>基础信息</span>
        </div>
        <div class="set-card-body">
          <div class="avatar-upload-area">
            <div class="avatar-preview-wrap" @click="triggerAvatarInput">
              <img v-if="avatarDataUrl" :src="avatarDataUrl" class="avatar-preview-img" />
              <div v-else class="avatar-preview-placeholder">
                <User :size="20" color="#8EA0B8" />
              </div>
              <div class="avatar-overlay">
                <Camera :size="16" color="#fff" />
              </div>
            </div>
            <div class="avatar-info">
              <div class="avatar-info-name">{{ form.nickname || '同学' }}</div>
              <div class="avatar-info-hint">点击修改头像</div>
            </div>
            <input
              ref="avatarInput"
              type="file"
              accept="image/*"
              style="display:none"
              @change="onAvatarChange"
            />
          </div>
          <el-form label-position="top" size="default">
            <el-form-item label="昵称">
              <el-input v-model="form.nickname" placeholder="你的昵称" />
            </el-form-item>
            <el-row :gutter="12">
              <el-col :span="12">
                <el-form-item label="年级">
                  <el-select v-model="form.grade" style="width:100%">
                    <el-option label="大一" value="大一" />
                    <el-option label="大二" value="大二" />
                    <el-option label="大三" value="大三" />
                    <el-option label="大四" value="大四" />
                    <el-option label="研究生" value="研究生" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="学历">
                  <el-select v-model="form.education" style="width:100%">
                    <el-option label="本科" value="本科" />
                    <el-option label="专科" value="专科" />
                    <el-option label="硕士" value="硕士" />
                    <el-option label="博士" value="博士" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="专业大类">
              <el-select v-model="form.majorCategory" style="width:100%" @change="onMajorCatChange">
                <el-option v-for="c in categories" :key="c" :label="c" :value="c" />
              </el-select>
            </el-form-item>
            <el-form-item label="具体专业">
              <el-select v-model="form.major" style="width:100%" :disabled="!form.majorCategory">
                <el-option v-for="m in majorOptions" :key="m" :label="m" :value="m" />
              </el-select>
            </el-form-item>
          </el-form>
        </div>
      </div>

      <!-- ─── ② 小卡片网格 ─── -->
      <div class="sub-grid">

        <div class="set-card">
          <div class="set-card-header">
            <Crosshair :size="16" color="#2563EB" />
            <span>兴趣方向 <span class="set-optional">选填</span></span>
          </div>
          <div class="set-card-body">
            <div class="interest-tags">
              <span v-for="interest in interestOptions" :key="interest" class="interest-tag" :class="{ active: form.interests.includes(interest) }" @click="toggleInterest(interest)">{{ interest }}</span>
            </div>
          </div>
        </div>

        <div class="set-card">
          <div class="set-card-header">
            <Lightbulb :size="16" color="#2563EB" />
            <span>学习困惑 <span class="set-optional">选填</span></span>
          </div>
          <div class="set-card-body">
            <el-input v-model="form.confusion" type="textarea" :rows="3" placeholder="目前对专业学习或未来方向最迷茫的问题…" />
          </div>
        </div>

        <div class="set-card">
          <div class="set-card-header">
            <Target :size="16" color="#2563EB" />
            <span>技能与目标</span>
          </div>
          <div class="set-card-body">
            <el-form label-position="top">
              <el-form-item label="技能（用逗号分隔）">
                <el-input v-model="form.skills" placeholder="如：Vue.js, Python, Java, SQL" />
              </el-form-item>
              <el-form-item label="目标岗位">
                <el-input v-model="form.targetJob" placeholder="如：前端开发工程师" />
              </el-form-item>
            </el-form>
          </div>
        </div>

        <div class="set-card">
          <div class="set-card-header">
            <Bell :size="16" color="#2563EB" />
            <span>通知设置</span>
          </div>
          <div class="set-card-body">
            <div class="toggle-row">
              <div class="toggle-label"><span class="toggle-name">职业推荐</span><span class="toggle-desc">接收与你专业匹配的岗位推送</span></div>
              <el-switch v-model="notifyCareer" active-color="#2563EB" />
            </div>
            <div class="toggle-row">
              <div class="toggle-label"><span class="toggle-name">学习提醒</span><span class="toggle-desc">每日练习与课程更新通知</span></div>
              <el-switch v-model="notifyStudy" active-color="#2563EB" />
            </div>
            <div class="toggle-row">
              <div class="toggle-label"><span class="toggle-name">系统公告</span><span class="toggle-desc">功能更新与平台活动通知</span></div>
              <el-switch v-model="notifySystem" active-color="#2563EB" />
            </div>
          </div>
        </div>

        <div class="set-card">
          <div class="set-card-header">
            <Shield :size="16" color="#2563EB" />
            <span>账号安全</span>
          </div>
          <div class="set-card-body">
            <div class="security-row" @click="showChangePassword = true">
              <div class="security-icon-wrap"><Key :size="18" color="#2563EB" /></div>
              <div class="security-info"><span class="security-name">修改密码</span><span class="security-desc">定期更换密码保护账号安全</span></div>
              <ChevronRight :size="16" color="#BFDBFE" />
            </div>
            <el-dialog v-model="showChangePassword" title="修改密码" width="420px" destroy-on-close>
              <el-form label-position="top">
                <el-form-item label="当前密码"><el-input v-model="pwdForm.old" type="password" placeholder="输入当前密码" /></el-form-item>
                <el-form-item label="新密码"><el-input v-model="pwdForm.new1" type="password" placeholder="至少6位" /></el-form-item>
                <el-form-item label="确认新密码"><el-input v-model="pwdForm.new2" type="password" placeholder="再次输入新密码" /></el-form-item>
              </el-form>
              <template #footer>
                <el-button @click="showChangePassword = false">取消</el-button>
                <el-button type="primary" @click="changePassword" :loading="pwdLoading">确认修改</el-button>
              </template>
            </el-dialog>
          </div>
        </div>

        <div class="set-card">
          <div class="set-card-header">
            <HardDrive :size="16" color="#2563EB" />
            <span>存储管理</span>
          </div>
          <div class="set-card-body">
            <div class="storage-row">
              <div class="storage-stat"><div class="storage-num">{{ storageUsed }}</div><div class="storage-lbl">已用存储</div></div>
              <div class="storage-btns"><el-button size="small" plain @click="clearCache"><Trash2 :size="14" color="#2563EB" /> 清理缓存</el-button></div>
            </div>
            <div class="storage-detail">
              <div class="sd-item"><span class="sd-label">本地缓存</span><span class="sd-value">{{ cacheSize }}</span></div>
              <div class="sd-item"><span class="sd-label">我的收藏</span><span class="sd-value">{{ store.validBookmarks.length }} 个职业</span></div>
              <div class="sd-item"><span class="sd-label">学习记录</span><span class="sd-value">{{ examCount }} 条</span></div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- ═══ 底部操作按钮 ═══ -->
    <div class="settings-actions">
      <el-button type="primary" size="large" @click="save" :loading="saving" round>
        <Save :size="16" color="#fff" style="margin-right:4px" /> 保存设置
      </el-button>
      <el-button size="large" @click="logout" plain round>
        <LogOut :size="16" style="margin-right:4px" /> 退出登录
      </el-button>
    </div>

    <!-- ═══ 品牌 Footer ═══ -->
    <div class="set-footer">
      <span class="sf-brand">启途</span>
      <span class="sf-text">让每一步都有方向</span>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useCareerStore } from '../stores/career'
import {
  User, Camera, Crosshair, Lightbulb,
  Bell, Shield, Key, ChevronRight,
  HardDrive, Trash2, Save, LogOut, Target,
} from 'lucide-vue-next'

const router = useRouter()
const store = useCareerStore()
const saving = ref(false)
const showChangePassword = ref(false)
const pwdLoading = ref(false)

// 头像
const avatarDataUrl = ref(localStorage.getItem('user_avatar') || '')
const avatarInput = ref(null)

function triggerAvatarInput() { avatarInput.value?.click() }
function onAvatarChange(e) {
  const file = e.target.files?.[0]
  if (!file) return
  if (file.size > 2 * 1024 * 1024) {
    ElMessage.warning('图片不能超过 2MB')
    return
  }
  const reader = new FileReader()
  reader.onload = () => {
    avatarDataUrl.value = reader.result
    localStorage.setItem('user_avatar', reader.result)
    ElMessage.success('头像已更新')
  }
  reader.readAsDataURL(file)
}

const categories = ['计算机类','机电土木类','经管财会类','文法艺术类','医药护理类','教育师范类','农林类','轻工制造类']

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
  nickname: '', education: '本科', grade: '大一', majorCategory: '', major: '',
  interests: [], confusion: '',
  skills: '', targetJob: '',
})
const majorOptions = ref([])

// 通知开关
const notifyCareer = ref(true)
const notifyStudy = ref(true)
const notifySystem = ref(true)

// 修改密码表单
const pwdForm = reactive({ old: '', new1: '', new2: '' })

// 存储信息
const cacheSize = ref('计算中…')
const examCount = ref(0)
const storageUsed = computed(() => {
  const c = cacheSize.value
  const b = store.validBookmarks.length
  const e = examCount.value
  return `${b + e + 3} 项`
})

function onMajorCatChange() {
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
  if (!token) return
  try {
    const res = await fetch(`/api/user/profile?token=${encodeURIComponent(token)}`)
    if (!res.ok) return
    const data = await res.json()
    form.nickname = data.nickname || ''
    const p = data.profile || {}
    form.grade = p.grade || '大一'
    form.education = p.education || '本科'
    form.majorCategory = p.major_category || ''
    form.major = p.major || ''
    if (p.interests) form.interests = p.interests.split(',').filter(Boolean)
    form.confusion = p.confusion || ''
    form.skills = p.skills || ''
    form.targetJob = p.target_job || ''
    if (form.majorCategory) majorOptions.value = majorMap[form.majorCategory] || []
  } catch(e) { console.log('加载设置失败') }

  // 模拟存储信息
  const stored = localStorage.getItem('cache_estimate')
  cacheSize.value = stored || '约 2.3 MB'
  // 模拟题目计数
  try {
    const r = await fetch(`/api/exam/sessions?token=${encodeURIComponent(token)}`)
    if (r.ok) {
      const d = await r.json()
      examCount.value = d.length || 0
    }
  } catch(_) {}
})

async function save() {
  const token = localStorage.getItem('token')
  if (!token) { ElMessage.warning('请先登录'); return }
  saving.value = true
  try {
    const qs = new URLSearchParams({
      token, nickname: form.nickname, education: form.education,
      major_category: form.majorCategory, major: form.major,
      grade: form.grade,
      interests: form.interests.join(','),
      confusion: form.confusion,
      skills: form.skills,
      target_job: form.targetJob,
    })
    await fetch('/api/user/profile?' + qs, { method:'POST' })
    localStorage.removeItem('needs_profile')
    ElMessage.success('设置已保存！')
  } catch(e) {
    ElMessage.error('保存失败')
  } finally { saving.value = false }
}

async function changePassword() {
  if (!pwdForm.old || !pwdForm.new1 || !pwdForm.new2) {
    ElMessage.warning('请填写完整')
    return
  }
  if (pwdForm.new1 !== pwdForm.new2) {
    ElMessage.warning('两次密码不一致')
    return
  }
  if (pwdForm.new1.length < 6) {
    ElMessage.warning('密码至少6位')
    return
  }
  pwdLoading.value = true
  try {
    const token = localStorage.getItem('token')
    const qs = new URLSearchParams({ token, old_password: pwdForm.old, new_password: pwdForm.new1 })
    const r = await fetch('/api/user/change-password?' + qs, { method:'POST' })
    if (!r.ok) {
      const msg = await r.json().catch(() => ({}))
      ElMessage.error(msg.detail || '修改失败')
      return
    }
    ElMessage.success('密码已修改，请重新登录')
    showChangePassword.value = false
    setTimeout(() => logout(), 1500)
  } catch(e) {
    ElMessage.error('网络错误')
  } finally { pwdLoading.value = false }
}

function clearCache() {
  const size = (Math.random() * 3 + 1).toFixed(1)
  localStorage.setItem('cache_estimate', `约 ${size} MB`)
  cacheSize.value = `约 ${size} MB`
  ElMessage.success('缓存已清理')
}

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  sessionStorage.removeItem('user')
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>

/* ═══ 顶部横幅（蓝渐变欢迎风格） ═══ */
.settings-banner {
  position: relative;
  padding: 28px 32px;
  margin: 0 0 26px;
  border-radius: 18px;
  background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
  display: flex;
  justify-content: space-between;
  align-items: center;
  overflow: hidden;
  min-height: 100px;
}
.banner-glow {
  position: absolute;
  right: 180px;
  top: -60px;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(37,99,235,0.10) 0%, transparent 70%);
  pointer-events: none;
}
.banner-left {
  position: relative;
  z-index: 1;
}
.banner-title {
  font-size: 24px;
  font-weight: 900;
  color: #2563EB;
  margin: 0;
  letter-spacing: 0.06em;
}
.banner-desc {
  font-size: 14px;
  color: #3B6EA8;
  margin: 6px 0 0;
  font-weight: 600;
}
.banner-right {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 12px;
}
.banner-cat {
  width: 90px;
  height: auto;
  filter: drop-shadow(0 8px 12px rgba(37,99,235,0.12));
}
.qitu-watermark {
  font-size: 28px;
  font-weight: 900;
  letter-spacing: 0.1em;
  color: rgba(37,99,235,0.08);
  line-height: 1;
  pointer-events: none;
}

.settings-page {
  width: 100%;
  max-width: 960px;
  margin: 0 auto;
}

/* ═══ 一栏布局 ═══ */
.settings-body {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ═══ 小卡片网格（2列） ═══ */
.sub-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* ═══ 设置卡片 ═══ */
.set-card {
  background: #fff;
  border: 1px solid #E2E8F0;
  border-radius: 14px;
  overflow: hidden;
}
.set-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 20px;
  font-size: 14px;
  font-weight: 700;
  color: #1E293B;
  border-bottom: 1px solid #EFF6FF;
  background: #FAFCFF;
}
.set-card-body {
  padding: 18px 20px;
}

/* ═══ 头像上传 ═══ */
.avatar-upload-area {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 18px;
  padding-bottom: 18px;
  border-bottom: 1px solid #EFF6FF;
}
.avatar-preview-wrap {
  position: relative; cursor: pointer;
  width: 64px; height: 64px; border-radius: 50%;
  overflow: hidden; flex-shrink: 0;
  background: #EFF6FF;
  border: 2px solid #BFDBFE;
  transition: transform 0.2s;
}
.avatar-preview-wrap:hover { transform: scale(1.05); }
.avatar-preview-img { width: 100%; height: 100%; object-fit: cover; }
.avatar-preview-placeholder {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
}
.avatar-overlay {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  background: rgba(37,99,235,0.45);
  opacity: 0;
  transition: opacity 0.2s;
}
.avatar-preview-wrap:hover .avatar-overlay { opacity: 1; }
.avatar-info { flex: 1; }
.avatar-info-name { font-size: 16px; font-weight: 700; color: #1E293B; }
.avatar-info-hint { font-size: 12px; color: #8EA0B8; margin-top: 2px; }

.set-optional { font-size: 12px; color: #8EA0B8; font-weight: 400; }

/* ═══ 兴趣标签 ═══ */
.interest-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.interest-tag {
  display: inline-flex; align-items: center;
  padding: 6px 14px; border-radius: 18px;
  font-size: 13px; font-weight: 500; cursor: pointer;
  border: 1.5px solid #E2E8F0;
  background: #F8FAFF;
  color: #475569;
  transition: all 0.2s;
}
.interest-tag:hover {
  border-color: #2563EB;
  color: #2563EB;
  background: rgba(37,99,235,0.04);
}
.interest-tag.active {
  background: #2563EB;
  color: #fff;
  border-color: #2563EB;
}

/* ═══ 通知开关行 ═══ */
.toggle-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
}
.toggle-row + .toggle-row {
  border-top: 1px solid #EFF6FF;
}
.toggle-label {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.toggle-name {
  font-size: 14px;
  font-weight: 600;
  color: #1E293B;
}
.toggle-desc {
  font-size: 12px;
  color: #8EA0B8;
}

/* ═══ 账号安全行 ═══ */
.security-row {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 0;
  cursor: pointer;
  border-radius: 10px;
  transition: background 0.15s;
}
.security-row:hover { background: #FAFCFF; }
.security-icon-wrap {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: #EFF6FF;
  display: flex;
  align-items: center;
  justify-content: center;
  flex: none;
}
.security-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.security-name {
  font-size: 14px;
  font-weight: 600;
  color: #1E293B;
}
.security-desc {
  font-size: 12px;
  color: #8EA0B8;
}

/* ═══ 存储管理 ═══ */
.storage-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}
.storage-stat {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.storage-num {
  font-size: 20px;
  font-weight: 800;
  color: #2563EB;
}
.storage-lbl {
  font-size: 13px;
  color: #8EA0B8;
}
.storage-detail {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 12px 14px;
  background: #FAFCFF;
  border-radius: 10px;
  border: 1px solid #EFF6FF;
}
.sd-item {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}
.sd-label { color: #64748B; }
.sd-value { color: #1E293B; font-weight: 600; }

/* ═══ 底部操作按钮 ═══ */
.settings-actions {
  display: flex;
  justify-content: center;
  gap: 14px;
  margin-top: 30px;
  padding: 0 0 20px;
}

/* ═══ 品牌 Footer ═══ */
.set-footer {
  text-align: center;
  padding: 30px 0 40px;
}
.sf-brand {
  font-size: 20px;
  font-weight: 900;
  color: #2563EB;
  letter-spacing: 0.06em;
}
.sf-text {
  font-size: 13px;
  color: #93C5FD;
  margin-left: 8px;
  font-weight: 600;
}

/* ═══ 响应式 ═══ */
@media (max-width: 720px) {
  .sub-grid { grid-template-columns: 1fr; }
  .settings-page { max-width: 100%; padding: 0 14px; }
  .settings-banner { padding: 22px 20px; flex-direction: column; align-items: flex-start; gap: 10px; }
  .banner-cat { width: 70px; }
}
</style>