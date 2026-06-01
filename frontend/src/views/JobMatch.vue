<template>
  <div class="page">
    <!-- ═══ 页面标题 ═══ -->
    <div class="section-header">
      <div class="section-title">
        <i class="fas fa-chart-bar"></i>
        投递分析
      </div>
    </div>
    <p class="page-hint">填写你想投的职位和城市，看哪些公司适合你、成功率多少</p>

    <!-- ═══ 收藏的职业 ═══ -->
    <div v-if="bookmarks.length" class="bookmark-band">
      <div class="bm-band-header">
        <span class="bm-band-title"><i class="fas fa-star"></i> 我的收藏职业</span>
      </div>
      <div class="bm-band-scroll">
        <el-tag
          v-for="b in bookmarks"
          :key="b.career"
          type="warning"
          style="cursor:pointer;margin:3px;flex-shrink:0"
          @click="addCareerFromBookmark(b.career)"
        >{{ b.career }}</el-tag>
      </div>
    </div>

    <!-- ═══ 求职信息表单 ═══ -->
    <div class="card" style="padding:24px;margin-top:1rem">
      <div class="section-title" style="margin-bottom:1.25rem">
        <i class="fas fa-bullseye"></i>
        求职信息
      </div>

      <el-row :gutter="16">
        <el-col :xs="24" :sm="12">
          <el-form-item label="目标职业（可填1-3个）" required>
            <el-tag
              v-for="(c,i) in targetCareers"
              :key="i"
              closable
              @close="removeCareer(i)"
              style="margin:3px"
            >{{ c }}</el-tag>
            <el-input
              v-if="targetCareers.length < 3"
              v-model="careerInput"
              placeholder="输入后回车添加"
              @keyup.enter="addCareer"
              style="width:140px;margin-left:4px"
              size="small"
            />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="6">
          <el-form-item label="意向城市">
            <el-select v-model="form.city" style="width:100%" filterable>
              <el-option v-for="c in optionCities" :key="c" :label="c" :value="c"/>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="6">
          <el-form-item label="最高学历">
            <el-select v-model="form.education" style="width:100%">
              <el-option v-for="e in ['高中','大专','本科','硕士','博士']" :key="e" :label="e" :value="e"/>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="16">
        <el-col :xs="24" :sm="12">
          <el-form-item label="技能标签">
            <el-input v-model="form.skills" placeholder="如 Python,Java,MySQL,沟通表达" />
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="6">
          <el-form-item label="期望薪资">
            <el-select v-model="form.salary" style="width:100%">
              <el-option v-for="s in ['5K-8K','8K-12K','12K-18K','18K-25K','25K+']" :key="s" :label="s" :value="s"/>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :xs="24" :sm="6">
          <el-form-item label="求职类型">
            <el-select v-model="form.jobType" style="width:100%">
              <el-option label="全职" value="全职"/>
              <el-option label="实习" value="实习"/>
              <el-option label="校招" value="校招"/>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <div class="form-actions">
        <button
          class="btn-primary"
          @click="startAnalyze"
          :disabled="!targetCareers.length || analyzing"
        >
          <i class="fas fa-rocket"></i>
          {{ analyzing ? '分析中…' : '开始分析' }}
        </button>
      </div>
    </div>

    <!-- ═══ 结果区域 ═══ -->
    <div v-if="result" style="margin-top:1.5rem">
      <div class="card" style="padding:16px 20px;margin-bottom:1rem;border-left:3px solid var(--primary);">
        <div style="display:flex;align-items:center;gap:10px">
          <i class="fas fa-check-circle" style="color:var(--primary);font-size:18px"></i>
          <span style="font-weight:600;color:var(--text-heading)">{{ result.summary }}</span>
        </div>
      </div>

      <div v-for="(tier, key) in result.tiers" :key="key" v-show="tier.items.length" class="tier-section">
        <div :class="['tier-header', 'tier-'+key]">
          <i v-if="key==='high'" class="fas fa-thumbs-up"></i>
          <i v-else-if="key==='potential'" class="fas fa-chart-line"></i>
          <i v-else class="fas fa-archive"></i>
          {{ tier.label }}
        </div>
        <div class="tier-desc">{{ tier.desc }}</div>
        <div class="grid-3">
          <div
            v-for="co in tier.items"
            :key="co.name"
            class="card company-card"
            :class="'company-'+key"
          >
            <div class="mc-header">
              <strong>{{ co.name }}</strong>
              <span :class="['tag-pill', co.recruit_status.includes('进行')||co.recruit_status.includes('开放') ? 'green' : 'gray']">
                <i class="fas fa-circle" style="font-size:6px;margin-right:4px"></i>
                {{ co.recruit_status }}
              </span>
            </div>
            <div class="mc-meta">
              <i class="fas fa-tag"></i> {{ co.tier }}
              <i class="fas fa-building" style="margin-left:8px"></i> {{ co.scale }}
              <i class="fas fa-coins" style="margin-left:8px"></i> {{ co.campus_salary }}
            </div>
            <div class="mc-desc">{{ co.description }}</div>
            <div class="mc-reason">
              <span
                v-for="r in co.recommend_reason?.split(',')"
                :key="r"
                class="tag-pill orange"
                style="margin:2px"
              ><i class="fas fa-lightbulb"></i> {{ r.trim() }}</span>
            </div>
            <div class="mc-match-bar">
              <div class="mc-bar-fill" :style="{width:co._rs+'%'}"></div>
            </div>
            <div class="mc-score">
              <i class="fas fa-percentage"></i> {{ co._rs }}% 匹配
            </div>
          </div>
        </div>
      </div>

      <div v-if="!hasAny" class="empty-state">
        <i class="fas fa-frown empty-icon"></i>
        <p>未找到匹配的企业，试试放宽条件或换城市</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useCareerStore } from '../stores/career'

const store = useCareerStore()
const bookmarks = computed(() => store.validBookmarks)

const targetCareers = ref([])
const careerInput = ref('')
const analyzing = ref(false)
const result = ref(null)
const optionCities = ['北京','上海','深圳','杭州','广州','成都','武汉','南京','西安','郑州','长沙','合肥','苏州','重庆','天津','青岛','大连','厦门','福州','济南']

const form = reactive({
  city:'北京', education:'本科', skills:'', salary:'8K-12K', jobType:'全职'
})

const hasAny = computed(() => {
  if (!result.value) return false
  const t = result.value.tiers
  return (t.high?.items?.length||0) + (t.potential?.items?.length||0) + (t.backup?.items?.length||0) > 0
})

function addCareer() {
  const name = careerInput.value.trim()
  if (!name) return
  if (targetCareers.value.includes(name)) { ElMessage.warning('已添加该职业'); return }
  if (targetCareers.value.length >= 3) { ElMessage.warning('最多添加3个目标职业'); return }
  targetCareers.value.push(name)
  careerInput.value = ''
}

function removeCareer(i) { targetCareers.value.splice(i, 1) }

function addCareerFromBookmark(name) {
  if (targetCareers.value.includes(name)) { ElMessage.warning('已添加'); return }
  if (targetCareers.value.length >= 3) { ElMessage.warning('最多3个'); return }
  targetCareers.value.push(name)
}

async function startAnalyze() {
  analyzing.value = true
  try {
    const params = new URLSearchParams({
      careers: targetCareers.value.join(','),
      city: form.city,
      education: form.education,
      skills: form.skills,
      salary: form.salary,
      job_type: form.jobType,
    })
    const res = await fetch(`/api/career/match-companies?${params}`, { method:'POST' })
    result.value = await res.json()
    window.scrollTo(0, 350)
  } catch(e) {
    ElMessage.error('分析失败，请重试')
  } finally {
    analyzing.value = false
  }
}
</script>

<style scoped>
.page-hint {
  font-size: 14px;
  color: var(--text-muted);
  margin-bottom: 1.25rem;
}

.form-actions {
  text-align: center;
  margin-top: 1rem;
}

/* ── Tier sections ── */
.tier-section {
  margin-bottom: 1.5rem;
}

.tier-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  font-size: 0.85rem;
  padding: 0.4rem 0.75rem;
  border-radius: 8px;
  margin-bottom: 0.2rem;
}

.tier-high {
  background: #ecfdf5;
  color: #059669;
}

.tier-potential {
  background: #fffbeb;
  color: #C85A20;
}

.tier-backup {
  background: #eff6ff;
  color: #3D5A80;
}

.tier-desc {
  font-size: 0.72rem;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
  padding-left: 0.75rem;
}

/* ── Company cards ── */
.company-card {
  padding: 16px 18px;
  cursor: default;
  transition: all 0.25s;
}

.company-card:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-2px);
}

.company-high {
  border-left: 3px solid #059669;
}

.company-potential {
  border-left: 3px solid #C85A20;
}

.company-backup {
  border-left: 3px solid #64748b;
}

.mc-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.3rem;
}

.mc-header strong {
  color: var(--text-heading);
  font-size: 15px;
}

.mc-meta {
  font-size: 0.72rem;
  color: var(--text-muted);
  margin-bottom: 0.4rem;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
}

.mc-desc {
  font-size: 0.78rem;
  color: var(--text-body);
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.mc-reason {
  margin-bottom: 0.6rem;
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.mc-match-bar {
  height: 5px;
  background: var(--border-light);
  border-radius: 3px;
  margin-bottom: 0.3rem;
  overflow: hidden;
}

.mc-bar-fill {
  height: 100%;
  border-radius: 3px;
  background: linear-gradient(90deg, #059669, #3D5A80);
  transition: width 0.5s ease;
}

.mc-score {
  font-size: 0.72rem;
  color: var(--primary);
  text-align: right;
  font-weight: 600;
}

/* Responsive handled globally in App.vue (.grid-3, .grid-2 breakpoints) */
</style>