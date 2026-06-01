<template>
  <div class="settings-page">
    <!-- ═══ 顶部 Banner ═══ -->
    <PageBanner fullwidth
      title="个人设置"
      description="完善个人信息，启途为你推荐更精准的职业方向"
      icon="fa-cog"
      variant="primary"
    />

    <!-- ═══ 两栏布局 ═══ -->
    <div class="settings-grid">
      <!-- 左栏：基础配置 -->
      <div class="settings-left">
        <!-- 👤 基础信息 -->
        <div class="set-card">
          <div class="set-card-header">
            <i class="fas fa-user" style="color:#3D5A80;"></i>
            <span>基础信息</span>
          </div>
          <div class="set-card-body">
            <!-- 头像上传 -->
            <div class="avatar-upload-area">
              <div class="avatar-preview-wrap" @click="triggerAvatarInput">
                <img v-if="avatarDataUrl" :src="avatarDataUrl" class="avatar-preview-img" />
                <div v-else class="avatar-preview-placeholder">
                  <i class="fas fa-user"></i>
                </div>
                <div class="avatar-overlay">
                  <i class="fas fa-camera"></i>
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

        <!-- 🎯 兴趣方向 -->
        <div class="set-card">
          <div class="set-card-header">
            <i class="fas fa-bullseye" style="color:#C85A20;"></i>
            <span>兴趣方向 <span class="set-optional">选填</span></span>
          </div>
          <div class="set-card-body">
            <div class="interest-tags">
              <span
                v-for="interest in interestOptions"
                :key="interest"
                class="interest-tag"
                :class="{ active: form.interests.includes(interest) }"
                @click="toggleInterest(interest)"
              >{{ interest }}</span>
            </div>
          </div>
        </div>

        <!-- 💡 学习困惑 -->
        <div class="set-card">
          <div class="set-card-header">
            <i class="fas fa-lightbulb" style="color:#BFA895;"></i>
            <span>学习困惑 <span class="set-optional">选填</span></span>
          </div>
          <div class="set-card-body">
            <el-input
              v-model="form.confusion"
              type="textarea"
              :rows="3"
              placeholder="目前对专业学习或未来方向最迷茫的问题…"
            />
          </div>
        </div>
      </div>

      <!-- 右栏：收藏管理 -->
      <div class="settings-right">
        <!-- ⭐ 收藏职业 -->
        <div class="set-card" v-if="bookmarks.length">
          <div class="set-card-header">
            <i class="fas fa-star" style="color:var(--accent);"></i>
            <span>收藏职业 <span class="set-badge">{{ bookmarks.length }}</span></span>
          </div>
          <div class="set-card-body">
            <div class="bm-list">
              <div v-for="b in bookmarks" :key="b.career" class="bm-item">
                <div class="bm-item-main" @click="showDetail(b)">
                  <div class="bm-name">{{ b.career }}</div>
                  <div class="bm-meta">{{ b.difficulty }} · {{ b.salary }}</div>
                </div>
                <div class="bm-item-actions">
                  <el-button
                    v-if="store.hasGeneratedPath(b.career)"
                    size="small"
                    text
                    type="warning"
                    @click.stop="goPath(b.career)"
                  ><i class="fas fa-map"></i> 路线</el-button>
                  <el-button size="small" text type="danger" @click.stop="store.removeBookmark(b.career)">
                    <i class="fas fa-times"></i>
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 📺 收藏视频 -->
        <div class="set-card" v-if="videoBookmarks.length">
          <div class="set-card-header">
            <i class="fas fa-video" style="color:#8EA0B8;"></i>
            <span>收藏视频 <span class="set-badge">{{ videoBookmarks.length }}</span></span>
          </div>
          <div class="set-card-body">
            <div class="vbm-list">
              <div v-for="v in videoBookmarks" :key="v.bvid" class="vbm-item">
                <div class="vbm-cover" v-if="v.pic">
                  <img :src="v.pic" :alt="v.title" @error="e=>e.target.style.display='none'" />
                </div>
                <div class="vbm-info">
                  <div class="vbm-title" :title="v.title">{{ v.title?.slice(0, 28) }}{{ v.title?.length > 28 ? '…' : '' }}</div>
                  <div class="vbm-meta">
                    <span v-if="v.career"><i class="fas fa-tag"></i> {{ v.career }}</span>
                    <span v-if="v.author"><i class="fas fa-user"></i> {{ v.author?.slice(0, 10) }}</span>
                  </div>
                  <div class="vbm-actions">
                    <el-button size="small" text type="primary" :href="v.url" target="_blank" tag="a" rel="noopener noreferrer">
                      <i class="fas fa-external-link-alt"></i> 观看
                    </el-button>
                    <el-button size="small" text type="danger" @click="store.removeVideoBookmark(v.bvid)">
                      <i class="fas fa-times"></i>
                    </el-button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右栏空状态 -->
        <div class="set-card set-empty" v-if="!bookmarks.length && !videoBookmarks.length">
          <div class="set-card-body" style="text-align:center;padding:30px 0;">
            <i class="fas fa-star" style="font-size:36px;color:#8EA0B8;margin-bottom:10px;display:block;"></i>
            <p style="color:#8EA0B8;font-size:14px;">还没有收藏的内容</p>
            <p style="color:#BFA895;font-size:13px;">去探索职业方向，收藏感兴趣的内容吧</p>
            <router-link to="/career" class="set-go-btn">去探索 <i class="fas fa-arrow-right"></i></router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══ 底部操作按钮 ═══ -->
    <div class="settings-actions">
      <el-button type="primary" size="large" @click="save" :loading="saving" round>
        <i class="fas fa-save"></i> 保存设置
      </el-button>
      <el-button size="large" @click="logout" plain round>
        <i class="fas fa-sign-out-alt"></i> 退出登录
      </el-button>
    </div>

    <!-- 收藏详情弹窗 -->
    <el-dialog v-model="dlgVisible" :title="dlgCareer?.career" width="500px" destroy-on-close>
      <div v-if="dlgCareer">
        <p><b>难度：</b>{{ dlgCareer.difficulty }}</p>
        <p><b>薪资：</b>{{ dlgCareer.salary }}</p>
        <p><b>趋势：</b>{{ dlgCareer.trend }}</p>
        <div v-if="dlgCareer.responsibilities?.length">
          <b>核心职责：</b>
          <li v-for="r in dlgCareer.responsibilities" :key="r">{{ r }}</li>
        </div>
        <div v-if="dlgCareer.growth_path?.length" style="margin-top:0.5rem">
          <b>成长路径：</b>
          <li v-for="g in dlgCareer.growth_path" :key="g">{{ g }}</li>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useCareerStore } from '../stores/career'
import PageBanner from '../components/PageBanner.vue'

const router = useRouter()
const store = useCareerStore()
const saving = ref(false)
const dlgVisible = ref(false)
const dlgCareer = ref(null)
const bookmarks = computed(() => store.validBookmarks)
const videoBookmarks = computed(() => store.videoBookmarks)
const majorOptions = ref([])

// 头像
const avatarDataUrl = ref(localStorage.getItem('user_avatar') || '')
const avatarInput = ref(null)

function triggerAvatarInput() {
  avatarInput.value?.click()
}
function onAvatarChange(e) {
  const file = e.target.files?.[0]
  if (!file) return
  // 限制大小 2MB
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
    if (form.majorCategory) majorOptions.value = majorMap[form.majorCategory] || []
  } catch(e) { console.log('加载设置失败') }
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
    })
    await fetch('/api/user/profile?' + qs, { method:'POST' })
    localStorage.removeItem('needs_profile')
    ElMessage.success('设置已保存！')
  } catch(e) {
    ElMessage.error('保存失败')
  } finally { saving.value = false }
}

function showDetail(c) { dlgCareer.value = c; dlgVisible.value = true }
function goPath(careerName) { router.push(`/career/path/${encodeURIComponent(careerName)}`) }

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  sessionStorage.removeItem('user')
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.settings-page { max-width: 960px; margin: 0 auto; }

/* ═══ 两栏网格 ═══ */
.settings-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 20px;
  align-items: start;
}
.settings-left { display: flex; flex-direction: column; gap: 16px; }
.settings-right { display: flex; flex-direction: column; gap: 16px; }

/* ═══ 设置卡片 ═══ */
.set-card {
  background: #fff;
  border: 1px solid #EDE7DE;
  border-radius: 12px;
  overflow: hidden;
}
.set-card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 18px;
  font-size: 14px;
  font-weight: 700;
  color: #2C3E50;
  border-bottom: 1px solid #F5F0E8;
  background: #FAF8F5;
}
.set-card-header i { font-size: 16px; }
.set-card-body { padding: 16px 18px; }

/* ═══ 头像上传 ═══ */
.avatar-upload-area {
  display: flex; align-items: center; gap: 16px;
  margin-bottom: 18px; padding-bottom: 18px;
  border-bottom: 1px solid #F5F0E8;
}
.avatar-preview-wrap {
  position: relative; cursor: pointer;
  width: 64px; height: 64px; border-radius: 50%;
  overflow: hidden; flex-shrink: 0;
  background: #e4e8ee;
  transition: transform 0.2s;
}
.avatar-preview-wrap:hover { transform: scale(1.05); }
.avatar-preview-img { width: 100%; height: 100%; object-fit: cover; }
.avatar-preview-placeholder {
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: center;
  font-size: 28px; color: #8EA0B8;
}
.avatar-overlay {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  background: rgba(0,0,0,.35);
  color: #fff; font-size: 20px; opacity: 0;
  transition: opacity 0.2s;
}
.avatar-preview-wrap:hover .avatar-overlay { opacity: 1; }
.avatar-info { flex: 1; }
.avatar-info-name { font-size: 16px; font-weight: 700; color: #2C3E50; }
.avatar-info-hint { font-size: 12px; color: #8EA0B8; margin-top: 2px; }

.set-optional { font-size: 12px; color: #8EA0B8; font-weight: 400; }
.set-badge {
  display: inline-flex; align-items: center; justify-content: center;
  min-width: 20px; height: 20px; border-radius: 10px;
  background: #3D5A80; color: #fff; font-size: 11px;
  padding: 0 6px; margin-left: 4px;
}

/* ═══ 收藏职业列表 ═══ */
.bm-list { display: flex; flex-direction: column; gap: 2px; }
.bm-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 0; border-bottom: 1px solid #F5F0E8; cursor: pointer;
}
.bm-item:last-child { border-bottom: none; }
.bm-item-main { flex: 1; min-width: 0; }
.bm-name { font-size: 14px; font-weight: 600; color: #2C3E50; }
.bm-meta { font-size: 12px; color: #8EA0B8; margin-top: 2px; }
.bm-item-actions { display: flex; align-items: center; gap: 2px; flex-shrink: 0; }

/* ═══ 收藏视频列表 ═══ */
.vbm-list { display: flex; flex-direction: column; gap: 8px; }
.vbm-item { display: flex; gap: 10px; padding: 8px 0; border-bottom: 1px solid #F5F0E8; }
.vbm-item:last-child { border-bottom: none; }
.vbm-cover {
  width: 80px; height: 50px; flex-shrink: 0;
  border-radius: 6px; overflow: hidden; background: #EDE7DE;
}
.vbm-cover img { width: 100%; height: 100%; object-fit: cover; }
.vbm-info { flex: 1; min-width: 0; }
.vbm-title { font-size: 13px; font-weight: 600; color: #2C3E50; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.vbm-meta { font-size: 11px; color: #8EA0B8; margin: 2px 0 4px; display: flex; gap: 8px; }
.vbm-actions { display: flex; gap: 4px; }

/* ═══ 兴趣标签 ═══ */
.interest-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.interest-tag {
  display: inline-flex; align-items: center;
  padding: 5px 12px; border-radius: 16px;
  font-size: 12px; font-weight: 500; cursor: pointer;
  border: 1.5px solid #EDE7DE; background: #F5F0E8; color: #4A5568;
  transition: all 0.2s;
}
.interest-tag:hover { border-color: #3D5A80; color: #3D5A80; background: rgba(61,90,128,0.06); }
.interest-tag.active { background: #3D5A80; color: #fff; border-color: #3D5A80; }

/* ═══ 空状态 ═══ */
.set-empty { border-style: dashed; }
.set-go-btn {
  display: inline-block; margin-top: 10px;
  padding: 8px 20px; border-radius: 20px;
  background: #3D5A80; color: #fff; font-size: 13px; font-weight: 500;
  transition: opacity 0.2s;
}
.set-go-btn:hover { opacity: 0.85; }

/* ═══ 底部操作按钮 ═══ */
.settings-actions {
  display: flex; justify-content: center; gap: 12px;
  margin-top: 28px; padding: 20px 0 40px;
}

/* ═══ 响应式 ═══ */
@media (max-width: 720px) {
  .settings-grid { grid-template-columns: 1fr; }
}
</style>