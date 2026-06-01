<template>
  <div class="page resume-page">
    <!-- ═══ 页面顶部 Banner ═══ -->
    <div class="banner-wrap">
      <PageBanner fullwidth
        title="简历优化"
        description="智能润色或 AI 生成简历，模板可视化预览，一键导出"
        icon="fa-file-pen"
        variant="primary"
      >
        <template #actions>
          <el-button size="small" @click="showHistory = true" style="background:rgba(255,255,255,0.15);border:none;color:#fff;">
            <i class="fas fa-folder-open"></i> 简历历史
          </el-button>
        </template>
      </PageBanner>
      <img src="/src/assets/resume-cat.png" class="banner-cat" alt="小橘简历">
    </div>

    <!-- ═══ 收藏岗位快捷选择 ═══ -->
    <div v-if="bookmarks.length" class="bookmark-band">
      <div class="bm-band-header">
        <span class="bm-band-title"><i class="fas fa-star"></i> 收藏岗位：</span>
        <div v-if="targetCareer" class="bm-active">
          <i class="fas fa-check-circle" style="color: var(--primary);margin-right:4px"></i>
          已选「{{ targetCareer }}」
        </div>
      </div>
      <div class="bm-band-scroll">
        <el-tag
          v-for="b in bookmarks"
          :key="b.career"
          :type="targetCareer === b.career ? 'warning' : 'info'"
          effect="plain"
          style="cursor:pointer;margin:2px;flex-shrink:0"
          @click="targetCareer = b.career"
        >{{ b.career }}</el-tag>
      </div>
    </div>

    <!-- ═══ 模式切换（润色/生成） ═══ -->
    <div class="filter-bar" style="margin:18px 0">
      <div class="filter-tags">
        <span
          :class="['filter-tag', { active: mode === 'optimize' }]"
          @click="mode='optimize'"
        >
          <i class="fas fa-file-lines"></i> 简历润色
        </span>
        <span
          :class="['filter-tag', { active: mode === 'generate' }]"
          @click="mode='generate'"
        >
          <i class="fas fa-wand-magic-sparkles"></i> 智能生成
        </span>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════════
         模板选择（可视预览）
         ══════════════════════════════════════════════════════════════ -->
    <div class="template-section">
      <div class="template-label">
        <i class="fas fa-palette"></i> 选择简历模板 — 点击即可预览布局
      </div>
      <div class="template-track">
        <div
          v-for="tpl in templates"
          :key="tpl.id"
          :class="['tpl-card', { active: selectedTemplate === tpl.id }]"
          :style="{ '--accent': tpl.color }"
          @click="selectedTemplate = tpl.id"
        >
          <div class="tpl-preview" v-html="tpl.preview"></div>
          <div class="tpl-name">{{ tpl.name }}</div>
          <div class="tpl-desc">{{ tpl.desc }}</div>
        </div>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════════
         润色模式
         ══════════════════════════════════════════════════════════════ -->
    <div v-if="mode === 'optimize'" class="card section-card">
      <div class="section-title-sm"><i class="fas fa-cloud-upload-alt"></i> 上传或粘贴简历</div>

      <div
        class="upload-zone"
        :class="{ dragging: isDragging }"
        @dragenter.prevent="isDragging = true"
        @dragover.prevent
        @dragleave.prevent="isDragging = false"
        @drop.prevent="onDropFile"
        @click="triggerFileInput"
      >
        <input ref="fileInput" type="file" accept=".txt,.pdf,.docx" style="display:none" @change="onFileChange" />
        <div class="upload-icon"><i class="fas fa-file-upload"></i></div>
        <div class="upload-text">
          <span v-if="!uploadedFile"><i class="fas fa-cloud-upload-alt" style="margin-right:6px;color:var(--primary)"></i>点击或拖拽上传简历文件（.txt / .pdf / .docx）</span>
          <span v-else style="color:var(--primary)"><i class="fas fa-check-circle"></i> {{ uploadedFile }}</span>
        </div>
      </div>

      <div class="opt-divider"><i class="fas fa-ellipsis-h"></i> 或者直接粘贴文本 <i class="fas fa-ellipsis-h"></i></div>

      <el-input v-model="resumeText" type="textarea" :rows="6" placeholder="请粘贴你的简历文本内容…" class="resume-input" />

      <!-- 定制要求 -->
      <div class="req-section">
        <div class="section-title-sm" style="font-size:0.9rem;margin-bottom:0.6rem">
          <i class="fas fa-lightbulb"></i> 输入定制要求（可选）
        </div>
        <div class="req-row">
          <el-input v-model="reqText" type="textarea" :rows="3" placeholder="例如：我想突出项目经验，把技能放最后。或者：帮我精简到一页。" class="req-input" />
          <div class="req-upload" @click="triggerReqInput">
            <input ref="reqFileInput" type="file" accept=".txt" style="display:none" @change="onReqFileChange" />
            <el-button text size="small"><i class="fas fa-paperclip"></i> 传文件</el-button>
          </div>
        </div>
        <div v-if="reqFileName" class="req-file-name"><i class="fas fa-paperclip"></i> {{ reqFileName }}</div>
      </div>

      <div class="action-row">
        <el-button type="primary" :loading="optLoading" @click="generateWithTemplate">
          <i class="fas fa-magic"></i> 按模板生成简历
        </el-button>
      </div>

      <div v-if="optResult" class="result-box">
        <div class="result-header">
          <h4><i class="fas fa-file-alt"></i> AI 生成的简历</h4>
          <div class="result-actions">
            <el-button size="small" @click="copyResult(optResult)"><i class="fas fa-copy"></i> 复制全文</el-button>
          </div>
        </div>
        <pre class="result-pre">{{ optResult }}</pre>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════════
         智能生成模式
         ══════════════════════════════════════════════════════════════ -->
    <div v-if="mode === 'generate'" class="generate-wrap">
      <el-alert
        v-if="targetCareer"
        :title="'🎯 正在为「' + targetCareer + '」生成简历'"
        type="info"
        :closable="false"
        show-icon
        class="gen-tip"
      />

      <!-- 个性化需求 -->
      <div class="card info-card">
        <div class="info-card-header">
          <i class="fas fa-lightbulb"></i> 个性化需求 <span class="field-note">（可选）</span>
        </div>
        <div class="card-body">
          <div class="req-row">
            <el-input v-model="reqTextGen" type="textarea" :rows="3" placeholder="例如：在校大学生找前端实习，突出Vue项目。或：要一页纸简历。" class="req-input" />
            <div class="req-upload" @click="triggerGenReqInput">
              <input ref="genReqFileInput" type="file" accept=".txt" style="display:none" @change="onGenReqFileChange" />
              <el-button text size="small"><i class="fas fa-paperclip"></i> 传文件</el-button>
            </div>
          </div>
          <div v-if="genReqFileName" class="req-file-name"><i class="fas fa-paperclip"></i> {{ genReqFileName }}</div>
        </div>
      </div>

      <!-- ══ 基础信息 ══ -->
      <div class="section-badge"><i class="fas fa-id-card"></i> 基础信息（必填）</div>

      <div class="card info-card">
        <div class="info-card-header"><i class="fas fa-user"></i> ① 个人基本信息</div>
        <div class="card-body">
          <el-row :gutter="16">
            <el-col :span="8"><el-input v-model="f.name" placeholder="姓名" /></el-col>
            <el-col :span="8">
              <el-select v-model="f.gender" placeholder="性别" style="width:100%">
                <el-option label="男" value="男" /><el-option label="女" value="女" />
              </el-select>
            </el-col>
            <el-col :span="8"><el-input v-model="f.age" placeholder="年龄" type="number" /></el-col>
          </el-row>
          <el-row :gutter="16" style="margin-top:12px">
            <el-col :span="8"><el-input v-model="f.phone" placeholder="联系电话" /></el-col>
            <el-col :span="8"><el-input v-model="f.email" placeholder="邮箱" /></el-col>
            <el-col :span="8"><el-input v-model="f.address" placeholder="现居地址" /></el-col>
          </el-row>
          <el-row :gutter="16" style="margin-top:12px">
            <el-col :span="8"><el-input v-model="f.job_intention" placeholder="求职意向岗位" /></el-col>
            <el-col :span="8"><el-input v-model="f.target_location" placeholder="期望工作地点" /></el-col>
            <el-col :span="8"><el-input v-model="f.wechat" placeholder="微信号（可选）" /></el-col>
          </el-row>
          <!-- 照片上传 -->
          <div class="photo-upload-row">
            <div class="photo-upload-area" @click="triggerPhotoInput">
              <img v-if="f.photo" :src="f.photo" class="photo-preview" />
              <div v-else class="photo-placeholder">
                <i class="fas fa-camera photo-icon"></i>
                <span class="photo-hint">上传证件照</span>
              </div>
            </div>
            <div class="photo-info">
              <div class="photo-label"><i class="fas fa-image"></i> 证件照片</div>
              <div class="photo-desc">标准证件照，白底/蓝底均可<br/>JPG / PNG，建议 2.5×3.5cm</div>
              <el-button v-if="f.photo" text size="small" type="danger" @click.stop="f.photo = ''">
                <i class="fas fa-trash-alt"></i> 删除照片
              </el-button>
            </div>
            <input ref="photoInput" type="file" accept="image/*" style="display:none" @change="onPhotoChange" />
          </div>
        </div>
      </div>

      <div class="card info-card">
        <div class="info-card-header"><i class="fas fa-graduation-cap"></i> ② 教育经历</div>
        <div class="card-body">
          <el-row :gutter="16">
            <el-col :span="8"><el-input v-model="f.edu.school" placeholder="就读院校" /></el-col>
            <el-col :span="8"><el-input v-model="f.edu.major" placeholder="专业" /></el-col>
            <el-col :span="8">
              <el-select v-model="f.edu.degree" placeholder="学历" style="width:100%">
                <el-option label="大专" value="大专" /><el-option label="本科" value="本科" />
                <el-option label="硕士" value="硕士" /><el-option label="博士" value="博士" />
              </el-select>
            </el-col>
          </el-row>
          <el-row :gutter="16" style="margin-top:12px">
            <el-col :span="8"><el-input v-model="f.edu.start_date" placeholder="入学时间" /></el-col>
            <el-col :span="8"><el-input v-model="f.edu.end_date" placeholder="毕业时间" /></el-col>
          </el-row>
          <div class="field-dense" style="margin-top:12px">
            <label>主修课程 <span class="field-note">（选与岗位相关的写）</span></label>
            <el-input v-model="f.edu.courses" placeholder="如：数据结构、操作系统、计算机网络" />
          </div>
        </div>
      </div>

      <div class="card info-card">
        <div class="info-card-header"><i class="fas fa-briefcase"></i> ③ 工作/实习经历</div>
        <div class="card-body">
          <div v-for="(e, i) in f.experiences" :key="i" class="multi-item">
            <div class="multi-header">
              <span class="multi-num">#{{ i + 1 }}</span>
              <el-button text type="danger" size="small" @click="f.experiences.splice(i, 1)">
                <i class="fas fa-trash-alt"></i> 删除
              </el-button>
            </div>
            <el-row :gutter="12">
              <el-col :span="7"><el-input v-model="e.company" placeholder="单位名称" size="small" /></el-col>
              <el-col :span="7"><el-input v-model="e.position" placeholder="岗位" size="small" /></el-col>
              <el-col :span="10"><el-input v-model="e.period" placeholder="时间" size="small" /></el-col>
            </el-row>
            <div class="field-dense" style="margin-top:8px">
              <label>内容 + 成果 <span class="field-note">（用数据、短句）</span></label>
              <el-input v-model="e.content" type="textarea" :rows="3" placeholder="一行一个要点" />
            </div>
          </div>
          <el-button text type="primary" @click="addExperience">
            <i class="fas fa-plus-circle"></i> 添加一条经历
          </el-button>
        </div>
      </div>

      <div class="card info-card">
        <div class="info-card-header"><i class="fas fa-code-branch"></i> ④ 项目经历</div>
        <div class="card-body">
          <div v-for="(p, i) in f.projects" :key="i" class="multi-item">
            <div class="multi-header">
              <span class="multi-num">#{{ i + 1 }}</span>
              <el-button text type="danger" size="small" @click="f.projects.splice(i, 1)">
                <i class="fas fa-trash-alt"></i> 删除
              </el-button>
            </div>
            <el-row :gutter="12">
              <el-col :span="8"><el-input v-model="p.name" placeholder="项目名称" size="small" /></el-col>
              <el-col :span="8"><el-input v-model="p.period" placeholder="参与时间" size="small" /></el-col>
              <el-col :span="8"><el-input v-model="p.role" placeholder="个人职责" size="small" /></el-col>
            </el-row>
            <div class="field-dense" style="margin-top:8px">
              <label>项目成果 / 收获</label>
              <el-input v-model="p.achievement" type="textarea" :rows="3" placeholder="成果描述，一行一个要点" />
            </div>
          </div>
          <el-button text type="primary" @click="addProject">
            <i class="fas fa-plus-circle"></i> 添加一个项目
          </el-button>
        </div>
      </div>

      <div class="card info-card">
        <div class="info-card-header"><i class="fas fa-cogs"></i> ⑤ 专业技能</div>
        <div class="card-body">
          <el-row :gutter="16">
            <el-col :span="12" style="margin-bottom:12px">
              <label>办公软件</label><el-input v-model="f.skills.office" placeholder="如：Word、Excel、PPT" />
            </el-col>
            <el-col :span="12" style="margin-bottom:12px">
              <label>专业软件</label><el-input v-model="f.skills.professional" placeholder="如：PS、CAD、Figma" />
            </el-col>
          </el-row>
          <el-row :gutter="16">
            <el-col :span="12" style="margin-bottom:12px">
              <label>编程语言</label><el-input v-model="f.skills.programming" placeholder="如：Python、JavaScript、Java" />
            </el-col>
            <el-col :span="12" style="margin-bottom:12px">
              <label>证书</label><el-input v-model="f.skills.certificates" placeholder="如：CET-4、计算机二级" />
            </el-col>
          </el-row>
          <el-row :gutter="16">
            <el-col :span="12"><label>语言能力</label><el-input v-model="f.skills.languages" placeholder="如：普通话二甲、CET-6" /></el-col>
          </el-row>
        </div>
      </div>

      <!-- ══ 加分项 ══ -->
      <div class="section-badge bonus"><i class="fas fa-star"></i> 加分项（可选）</div>

      <div class="card info-card">
        <div class="info-card-header"><i class="fas fa-school"></i> ⑥ 校园经历 <span class="field-note">（应届生重点）</span></div>
        <div class="card-body">
          <div v-for="(c, i) in f.campus_activities" :key="i" class="multi-item">
            <div class="multi-header">
              <span class="multi-num">#{{ i + 1 }}</span>
              <el-button text type="danger" size="small" @click="f.campus_activities.splice(i, 1)">
                <i class="fas fa-trash-alt"></i> 删除
              </el-button>
            </div>
            <el-row :gutter="12">
              <el-col :span="8"><el-input v-model="c.name" placeholder="活动/组织名称" size="small" /></el-col>
              <el-col :span="8"><el-input v-model="c.period" placeholder="时间" size="small" /></el-col>
              <el-col :span="8"><el-input v-model="c.role" placeholder="职责描述" size="small" /></el-col>
            </el-row>
          </div>
          <el-button text type="primary" @click="addCampus">
            <i class="fas fa-plus-circle"></i> 添加校园经历
          </el-button>
        </div>
      </div>

      <div class="card info-card">
        <div class="info-card-header"><i class="fas fa-trophy"></i> ⑦ 荣誉奖项</div>
        <div class="card-body">
          <div v-for="(a, i) in f.awards" :key="i" class="multi-item">
            <div class="multi-header">
              <span class="multi-num">#{{ i + 1 }}</span>
              <el-button text type="danger" size="small" @click="f.awards.splice(i, 1)">
                <i class="fas fa-trash-alt"></i> 删除
              </el-button>
            </div>
            <el-row :gutter="12">
              <el-col :span="8"><el-input v-model="a.name" placeholder="奖项名称" size="small" /></el-col>
              <el-col :span="8"><el-input v-model="a.period" placeholder="获奖时间" size="small" /></el-col>
              <el-col :span="8"><el-input v-model="a.issuer" placeholder="颁发单位（可选）" size="small" /></el-col>
            </el-row>
          </div>
          <el-button text type="primary" @click="addAward">
            <i class="fas fa-plus-circle"></i> 添加奖项
          </el-button>
        </div>
      </div>

      <div class="card info-card">
        <div class="info-card-header"><i class="fas fa-comment"></i> ⑧ 自我评价 <span class="field-note">（简短，贴合岗位）</span></div>
        <div class="card-body">
          <el-input v-model="f.self_evaluation" type="textarea" :rows="4" placeholder="总结个人优势、性格、职业态度，避免空话套话" />
        </div>
      </div>

      <!-- 生成按钮 -->
      <div class="gen-action">
        <el-button type="primary" size="large" :loading="genLoading" @click="generateSmart">
          <i class="fas fa-magic"></i> 生成简历
        </el-button>
      </div>

      <!-- 生成结果 -->
      <div v-if="genResult" class="result-box">
        <div class="result-header">
          <h4><i class="fas fa-file-alt"></i> 预览</h4>
          <div class="result-actions">
            <el-button size="small" type="primary" :loading="dlLoading" @click="downloadDocx">
              <i class="fas fa-download"></i> 下载 Word 文档
            </el-button>
            <el-button size="small" @click="copyResult(genResult)">
              <i class="fas fa-copy"></i> 复制全文
            </el-button>
          </div>
        </div>
        <pre class="result-pre">{{ genResult }}</pre>
      </div>
    </div>

    <!-- ═══ 简历历史弹窗 ═══ -->
    <el-dialog v-model="showHistory" width="640px" destroy-on-close class="history-dialog">
      <template #header>
        <span class="dialog-title"><i class="fas fa-folder-open"></i> 简历历史</span>
      </template>
      <div v-if="historyLoading" class="loading-state"><i class="fas fa-spinner fa-spin"></i> 加载中...</div>
      <div v-else-if="historyRecords.length === 0" class="empty-state">
        <i class="fas fa-inbox empty-icon"></i>
        <p>暂无保存的简历</p>
        <p class="empty-hint">生成简历后会自动保存到历史中</p>
      </div>
      <div v-else class="history-list">
        <div v-for="r in historyRecords" :key="r.id" class="history-item">
          <div class="history-info">
            <div class="history-name">{{ r.name || '未命名' }}</div>
            <div class="history-meta">
              <span class="history-tpl">{{ r.template_name }}</span>
              <span v-if="r.career" class="history-career"><i class="fas fa-bullseye"></i> {{ r.career }}</span>
              <span class="history-date">{{ r.created_at }}</span>
            </div>
          </div>
          <div class="history-actions">
            <el-button size="small" text @click="restoreHistory(r.id)">
              <i class="fas fa-undo-alt"></i> 恢复
            </el-button>
            <el-button size="small" text type="danger" @click="deleteHistory(r.id)">
              <i class="fas fa-trash-alt"></i> 删除
            </el-button>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useCareerStore } from '../stores/career'
import PageBanner from '../components/PageBanner.vue'

const store = useCareerStore()
const bookmarks = computed(() => store.validBookmarks)

const mode = ref('generate')
const targetCareer = ref('')
const selectedTemplate = ref('classic')

// ── 模板数据（含可视预览 SVG） ──
const templates = [
  {
    id: 'classic', name: '简约经典', color: '#667eea',
    desc: '标准垂直结构，横线分隔，适合所有岗位',
    preview: `<svg viewBox="0 0 200 280" xmlns="http://www.w3.org/2000/svg">
      <rect x="2" y="2" width="196" height="276" rx="6" fill="#fafafa" stroke="#e0e0e0" stroke-width="1"/>
      <rect x="30" y="18" width="140" height="8" rx="4" fill="#667eea" opacity="0.6"/>
      <line x1="20" y1="40" x2="180" y2="40" stroke="#ddd" stroke-width="0.5"/>
      <rect x="20" y="48" width="160" height="24" rx="3" fill="#e8ecf8"/>
      <text x="28" y="63" font-size="8" fill="#667eea" font-weight="bold">个人信息</text>
      <rect x="20" y="78" width="160" height="36" rx="3" fill="#f0f0f0"/>
      <text x="28" y="93" font-size="8" fill="#888">教育经历</text>
      <rect x="20" y="120" width="160" height="56" rx="3" fill="#f0f0f0"/>
      <text x="28" y="135" font-size="8" fill="#888">工作/实习经历</text>
      <rect x="20" y="182" width="160" height="40" rx="3" fill="#f0f0f0"/>
      <text x="28" y="197" font-size="8" fill="#888">项目经历</text>
      <rect x="20" y="228" width="160" height="24" rx="3" fill="#f0f0f0"/>
      <text x="28" y="243" font-size="8" fill="#888">专业技能</text>
    </svg>`,
  },
  {
    id: 'skill-first', name: '技能突出', color: '#f59e0b',
    desc: '左栏技能+信息，右栏经历，技术岗首选',
    preview: `<svg viewBox="0 0 200 280" xmlns="http://www.w3.org/2000/svg">
      <rect x="2" y="2" width="196" height="276" rx="6" fill="#fafafa" stroke="#e0e0e0" stroke-width="1"/>
      <rect x="20" y="16" width="160" height="8" rx="4" fill="#f59e0b" opacity="0.6"/>
      <!-- 左栏 -->
      <rect x="10" y="34" width="66" height="200" rx="4" fill="#fef7e6"/>
      <text x="20" y="54" font-size="7.5" fill="#d4890b" font-weight="bold">个人信息</text>
      <rect x="16" y="62" width="54" height="4" rx="2" fill="#eee"/>
      <rect x="16" y="70" width="48" height="4" rx="2" fill="#eee"/>
      <text x="20" y="90" font-size="7.5" fill="#d4890b" font-weight="bold">专业技能</text>
      <rect x="16" y="98" width="54" height="24" rx="3" fill="#f5d68a" opacity="0.5"/>
      <rect x="16" y="126" width="54" height="24" rx="3" fill="#f5d68a" opacity="0.5"/>
      <rect x="16" y="154" width="54" height="24" rx="3" fill="#f5d68a" opacity="0.5"/>
      <rect x="16" y="182" width="54" height="24" rx="3" fill="#f5d68a" opacity="0.5"/>
      <!-- 右栏 -->
      <rect x="84" y="34" width="108" height="40" rx="3" fill="#f0f0f0"/>
      <text x="92" y="52" font-size="7.5" fill="#888">教育经历</text>
      <rect x="84" y="80" width="108" height="54" rx="3" fill="#f0f0f0"/>
      <text x="92" y="98" font-size="7.5" fill="#888">工作经历</text>
      <rect x="84" y="140" width="108" height="54" rx="3" fill="#f0f0f0"/>
      <text x="92" y="158" font-size="7.5" fill="#888">项目经历</text>
      <rect x="84" y="200" width="108" height="34" rx="3" fill="#f0f0f0"/>
      <text x="92" y="218" font-size="7.5" fill="#888">荣誉奖项</text>
    </svg>`,
  },
  {
    id: 'project-focused', name: '项目驱动', color: '#10b981',
    desc: '项目详细展开，左侧日期标记，适合有经验',
    preview: `<svg viewBox="0 0 200 280" xmlns="http://www.w3.org/2000/svg">
      <rect x="2" y="2" width="196" height="276" rx="6" fill="#fafafa" stroke="#e0e0e0" stroke-width="1"/>
      <rect x="30" y="18" width="140" height="8" rx="4" fill="#10b981" opacity="0.6"/>
      <rect x="20" y="38" width="160" height="22" rx="3" fill="#e8f5ed"/>
      <text x="28" y="52" font-size="8" fill="#10b981" font-weight="bold">个人信息</text>
      <rect x="20" y="65" width="160" height="22" rx="3" fill="#f0f0f0"/>
      <text x="28" y="79" font-size="8" fill="#888">教育经历</text>
      <!-- 项目1 -->
      <rect x="15" y="94" width="22" height="52" rx="3" fill="#10b981" opacity="0.25"/>
      <text x="17" y="160" font-size="5" fill="#10b981">2024</text>
      <rect x="42" y="94" width="138" height="20" rx="3" fill="#e8f5ed"/>
      <text x="50" y="107" font-size="7.5" fill="#333">项目 A — 主要职责</text>
      <rect x="42" y="118" width="138" height="28" rx="3" fill="#f0f0f0"/>
      <line x1="50" y1="127" x2="120" y2="127" stroke="#ccc" stroke-width="1"/>
      <line x1="50" y1="133" x2="110" y2="133" stroke="#ccc" stroke-width="1"/>
      <line x1="50" y1="139" x2="130" y2="139" stroke="#ccc" stroke-width="1"/>
      <!-- 项目2 -->
      <rect x="15" y="152" width="22" height="52" rx="3" fill="#10b981" opacity="0.25"/>
      <rect x="42" y="152" width="138" height="20" rx="3" fill="#e8f5ed"/>
      <text x="50" y="165" font-size="7.5" fill="#333">项目 B — 主要职责</text>
      <rect x="42" y="176" width="138" height="28" rx="3" fill="#f0f0f0"/>
      <line x1="50" y1="185" x2="115" y2="185" stroke="#ccc" stroke-width="1"/>
      <line x1="50" y1="191" x2="105" y2="191" stroke="#ccc" stroke-width="1"/>
      <!-- 技能 -->
      <rect x="20" y="212" width="160" height="22" rx="3" fill="#f0f0f0"/>
      <text x="28" y="226" font-size="8" fill="#888">专业技能</text>
      <rect x="20" y="240" width="160" height="22" rx="3" fill="#f0f0f0"/>
      <text x="28" y="254" font-size="8" fill="#888">自我评价</text>
    </svg>`,
  },
  {
    id: 'fresh-grad', name: '应届生友好', color: '#ef4444',
    desc: '教育+校园突出放大，适合大一/大二学生',
    preview: `<svg viewBox="0 0 200 280" xmlns="http://www.w3.org/2000/svg">
      <rect x="2" y="2" width="196" height="276" rx="6" fill="#fafafa" stroke="#e0e0e0" stroke-width="1"/>
      <rect x="30" y="18" width="140" height="8" rx="4" fill="#ef4444" opacity="0.5"/>
      <!-- 教育放大 -->
      <rect x="20" y="36" width="160" height="48" rx="4" fill="#fde8e8"/>
      <text x="28" y="52" font-size="9" fill="#ef4444" font-weight="bold">🎓 教育经历</text>
      <rect x="28" y="58" width="144" height="4" rx="2" fill="#f5c6c6" opacity="0.6"/>
      <rect x="28" y="66" width="120" height="4" rx="2" fill="#f5c6c6" opacity="0.4"/>
      <rect x="28" y="74" width="100" height="4" rx="2" fill="#f5c6c6" opacity="0.3"/>
      <!-- 校园经历放大 -->
      <rect x="20" y="92" width="160" height="48" rx="4" fill="#fde8e8" opacity="0.7"/>
      <text x="28" y="108" font-size="9" fill="#ef4444" font-weight="bold">🏫 校园经历</text>
      <rect x="28" y="114" width="144" height="4" rx="2" fill="#f5c6c6" opacity="0.6"/>
      <rect x="28" y="122" width="120" height="4" rx="2" fill="#f5c6c6" opacity="0.4"/>
      <rect x="28" y="130" width="100" height="4" rx="2" fill="#f5c6c6" opacity="0.3"/>
      <!-- 其余紧凑 -->
      <rect x="20" y="148" width="160" height="26" rx="3" fill="#f0f0f0"/>
      <text x="28" y="164" font-size="8" fill="#888">专业技能</text>
      <rect x="20" y="180" width="160" height="26" rx="3" fill="#f0f0f0"/>
      <text x="28" y="196" font-size="8" fill="#888">项目经历</text>
      <rect x="20" y="212" width="160" height="26" rx="3" fill="#f0f0f0"/>
      <text x="28" y="228" font-size="8" fill="#888">荣誉奖项</text>
      <rect x="20" y="244" width="160" height="26" rx="3" fill="#f0f0f0"/>
      <text x="28" y="260" font-size="8" fill="#888">自我评价</text>
    </svg>`,
  },
  {
    id: 'management', name: '管理型', color: '#8b5cf6',
    desc: '成果量化突出，数据条装饰，实习丰富首选',
    preview: `<svg viewBox="0 0 200 280" xmlns="http://www.w3.org/2000/svg">
      <rect x="2" y="2" width="196" height="276" rx="6" fill="#fafafa" stroke="#e0e0e0" stroke-width="1"/>
      <!-- 顶栏装饰条 -->
      <rect x="0" y="12" width="200" height="4" fill="#8b5cf6" opacity="0.3"/>
      <rect x="20" y="24" width="160" height="8" rx="4" fill="#8b5cf6" opacity="0.6"/>
      <!-- 信息条 -->
      <rect x="20" y="38" width="130" height="18" rx="3" fill="#f3eefb"/>
      <text x="28" y="50" font-size="7.5" fill="#8b5cf6">个人信息</text>
      <rect x="156" y="39" width="24" height="16" rx="2" fill="#8b5cf6" opacity="0.4"/>
      <!-- 工作经历带数据条 -->
      <rect x="20" y="62" width="160" height="50" rx="3" fill="#f0f0f0"/>
      <text x="28" y="76" font-size="8" fill="#888" font-weight="bold">工作经历</text>
      <rect x="28" y="82" width="100" height="5" rx="2" fill="#ddd"/>
      <rect x="28" y="82" width="72" height="5" rx="2" fill="#a78bfa" opacity="0.6"/>
      <rect x="28" y="91" width="120" height="5" rx="2" fill="#ddd"/>
      <rect x="28" y="91" width="85" height="5" rx="2" fill="#a78bfa" opacity="0.5"/>
      <rect x="28" y="100" width="80" height="5" rx="2" fill="#ddd"/>
      <rect x="28" y="100" width="55" height="5" rx="2" fill="#a78bfa" opacity="0.5"/>
      <!-- 项目经历 -->
      <rect x="20" y="118" width="160" height="50" rx="3" fill="#f0f0f0"/>
      <text x="28" y="132" font-size="8" fill="#888" font-weight="bold">项目经历</text>
      <rect x="28" y="138" width="100" height="5" rx="2" fill="#ddd"/>
      <rect x="28" y="138" width="68" height="5" rx="2" fill="#a78bfa" opacity="0.6"/>
      <rect x="28" y="147" width="120" height="5" rx="2" fill="#ddd"/>
      <rect x="28" y="147" width="90" height="5" rx="2" fill="#a78bfa" opacity="0.5"/>
      <rect x="28" y="156" width="80" height="5" rx="2" fill="#ddd"/>
      <rect x="28" y="156" width="60" height="5" rx="2" fill="#a78bfa" opacity="0.5"/>
      <!-- 紧凑部分 -->
      <rect x="20" y="174" width="160" height="22" rx="3" fill="#f0f0f0"/>
      <text x="28" y="188" font-size="8" fill="#888">教育经历</text>
      <rect x="20" y="202" width="160" height="22" rx="3" fill="#f0f0f0"/>
      <text x="28" y="216" font-size="8" fill="#888">专业技能</text>
      <rect x="20" y="230" width="160" height="22" rx="3" fill="#f0f0f0"/>
      <text x="28" y="244" font-size="8" fill="#888">荣誉奖项</text>
    </svg>`,
  },
  {
    id: 'minimal', name: '简约现代', color: '#06b6d4',
    desc: '干净清爽大间距，极细分割线，创意岗',
    preview: `<svg viewBox="0 0 200 280" xmlns="http://www.w3.org/2000/svg">
      <rect x="2" y="2" width="196" height="276" rx="6" fill="#fafafa" stroke="#e0e0e0" stroke-width="1"/>
      <line x1="20" y1="18" x2="180" y2="18" stroke="#06b6d4" stroke-width="0.8"/>
      <rect x="30" y="24" width="140" height="8" rx="4" fill="#06b6d4" opacity="0.4"/>
      <rect x="20" y="40" width="160" height="22" rx="2" fill="#f5feff"/>
      <text x="28" y="54" font-size="7.5" fill="#06b6d4" font-weight="bold">个人信息</text>
      <rect x="28" y="62" width="140" height="3" rx="1" fill="#eee"/>
      <line x1="20" y1="72" x2="180" y2="72" stroke="#eee" stroke-width="0.3"/>
      <rect x="20" y="80" width="160" height="22" rx="2" fill="#f5feff"/>
      <text x="28" y="94" font-size="7.5" fill="#06b6d4" font-weight="bold">教育经历</text>
      <rect x="28" y="102" width="140" height="3" rx="1" fill="#eee"/>
      <line x1="20" y1="112" x2="180" y2="112" stroke="#eee" stroke-width="0.3"/>
      <rect x="20" y="120" width="160" height="30" rx="2" fill="#f5feff"/>
      <text x="28" y="134" font-size="7.5" fill="#06b6d4" font-weight="bold">工作经历</text>
      <rect x="28" y="142" width="140" height="3" rx="1" fill="#eee"/>
      <line x1="20" y1="160" x2="180" y2="160" stroke="#eee" stroke-width="0.3"/>
      <rect x="20" y="168" width="160" height="22" rx="2" fill="#f5feff"/>
      <text x="28" y="182" font-size="7.5" fill="#06b6d4" font-weight="bold">项目经历</text>
      <rect x="28" y="190" width="140" height="3" rx="1" fill="#eee"/>
      <line x1="20" y1="200" x2="180" y2="200" stroke="#eee" stroke-width="0.3"/>
      <rect x="20" y="208" width="160" height="22" rx="2" fill="#f5feff"/>
      <text x="28" y="222" font-size="7.5" fill="#888">专业技能</text>
      <rect x="28" y="230" width="140" height="3" rx="1" fill="#eee"/>
      <line x1="20" y1="240" x2="180" y2="240" stroke="#eee" stroke-width="0.3"/>
      <rect x="20" y="248" width="160" height="22" rx="2" fill="#f5feff"/>
      <text x="28" y="262" font-size="7.5" fill="#888">自我评价</text>
    </svg>`,
  },
]

// ── 润色模式 ──
const resumeText = ref('')
const reqText = ref('')
const optLoading = ref(false)
const optResult = ref('')
const isDragging = ref(false)
const uploadedFile = ref('')
const fileInput = ref(null)
const reqFileName = ref('')
const reqFileInput = ref(null)

function triggerFileInput() { fileInput.value?.click() }
function triggerReqInput() { reqFileInput.value?.click() }

async function onDropFile(e) {
  isDragging.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) await uploadFile(file)
}

async function onFileChange(e) {
  const file = e.target?.files?.[0]
  if (file) await uploadFile(file)
}

async function uploadFile(file) {
  const fd = new FormData(); fd.append('file', file)
  try {
    const res = await fetch('/api/resume/upload-file', { method: 'POST', body: fd })
    const data = await res.json()
    uploadedFile.value = data.filename; resumeText.value = data.text
    ElMessage.success(`已读取「${data.filename}」`)
  } catch { ElMessage.error('文件上传失败') }
}

async function onReqFileChange(e) {
  const file = e.target?.files?.[0]; if (!file) return
  const fd = new FormData(); fd.append('file', file)
  try {
    const res = await fetch('/api/resume/upload-file', { method: 'POST', body: fd })
    const data = await res.json()
    reqFileName.value = data.filename; reqText.value = data.text
    ElMessage.success('已读取需求文件')
  } catch { ElMessage.error('文件上传失败') }
}

async function generateWithTemplate() {
  if (!resumeText.value.trim() && !uploadedFile.value) { ElMessage.warning('请先上传或粘贴简历文本'); return }
  optLoading.value = true
  try {
    const res = await fetch('/api/resume/generate-with-template', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        template_id: selectedTemplate.value, mode: 'optimize',
        resume_text: resumeText.value, requirements: reqText.value,
        career: targetCareer.value || '',
      }),
    })
    optResult.value = (await res.json()).resume
  } catch { ElMessage.error('生成失败') } finally { optLoading.value = false }
}

// ── 智能生成模式 ──
const reqTextGen = ref('')
const genReqFileName = ref('')
const genReqFileInput = ref(null)
const photoInput = ref(null)

function triggerPhotoInput() { photoInput.value?.click() }

function onPhotoChange(e) {
  const file = e.target?.files?.[0]
  if (!file) return
  if (!file.type.startsWith('image/')) { ElMessage.warning('请上传图片文件'); return }
  const reader = new FileReader()
  reader.onload = (ev) => { f.photo = ev.target?.result || '' }
  reader.readAsDataURL(file)
}

function triggerGenReqInput() { genReqFileInput.value?.click() }

async function onGenReqFileChange(e) {
  const file = e.target?.files?.[0]; if (!file) return
  const fd = new FormData(); fd.append('file', file)
  try {
    const res = await fetch('/api/resume/upload-file', { method: 'POST', body: fd })
    const data = await res.json()
    genReqFileName.value = data.filename; reqTextGen.value = data.text
    ElMessage.success('已读取需求文件')
  } catch { ElMessage.error('文件上传失败') }
}

function emptyExp() { return { company: '', position: '', period: '', content: '' } }
function emptyPrj() { return { name: '', period: '', role: '', achievement: '' } }
function emptyCampus() { return { name: '', period: '', role: '' } }
function emptyAward() { return { name: '', period: '', issuer: '' } }

const f = reactive({
  name: '', gender: '', age: '', phone: '', email: '', address: '',
  job_intention: '', target_location: '', wechat: '', photo: '',
  edu: { school: '', major: '', degree: '', start_date: '', end_date: '', courses: '' },
  experiences: [emptyExp()], projects: [emptyPrj()],
  skills: { office: '', professional: '', programming: '', certificates: '', languages: '' },
  campus_activities: [], awards: [], self_evaluation: '',
})

function addExperience() { f.experiences.push(emptyExp()) }
function addProject() { f.projects.push(emptyPrj()) }
function addCampus() { f.campus_activities.push(emptyCampus()) }
function addAward() { f.awards.push(emptyAward()) }

const genLoading = ref(false)
const genResult = ref('')
const dlLoading = ref(false)

// ── 简历历史 ──
const showHistory = ref(false)
const historyRecords = ref([])
const historyLoading = ref(false)

async function generateSmart() {
  if (!f.name && !f.phone && !f.edu.school && !f.experiences.some(e => e.company)) {
    ElMessage.warning('请至少填写部分基本信息')
    return
  }
  genLoading.value = true
  try {
    const res = await fetch('/api/resume/generate', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...f,
        career: targetCareer.value || f.job_intention || '',
        template_id: selectedTemplate.value,
        requirements: reqTextGen.value,
        experiences: f.experiences.filter(e => e.company || e.position),
        projects: f.projects.filter(p => p.name),
        campus_activities: f.campus_activities.filter(c => c.name),
        awards: f.awards.filter(a => a.name),
      }),
    })
    genResult.value = (await res.json()).resume
    // 自动保存到历史
    saveHistory(genResult.value)
  } catch { ElMessage.error('生成失败') } finally { genLoading.value = false }
}

async function copyResult(text) {
  try { await navigator.clipboard.writeText(text); ElMessage.success('已复制') }
  catch { ElMessage.warning('复制失败，请手动选择') }
}

async function downloadDocx() {
  if (!genResult.value) { ElMessage.warning('请先生成简历'); return }
  dlLoading.value = true
  try {
    const body = JSON.stringify({
      ...f,
      career: targetCareer.value || f.job_intention || '',
      template_id: selectedTemplate.value,
      requirements: reqTextGen.value,
      experiences: f.experiences.filter(e => e.company || e.position),
      projects: f.projects.filter(p => p.name),
      campus_activities: f.campus_activities.filter(c => c.name),
      awards: f.awards.filter(a => a.name),
    })
    const res = await fetch('/api/resume/download', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body,
    })
    if (!res.ok) { ElMessage.error('下载失败'); return }
    const blob = await res.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    const tpl = templates.find(t => t.id === selectedTemplate.value)
    a.download = `简历_${f.name || '个人'}_${tpl?.name || ''}.docx`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    ElMessage.success('简历已下载，排版格式与所选模板一致')
  } catch { ElMessage.error('下载失败') } finally { dlLoading.value = false }
}

// ── 简历历史 ──

async function saveHistory(generatedText) {
  try {
    const formData = {
      ...f,
      career: targetCareer.value || f.job_intention || '',
      template_id: selectedTemplate.value,
      requirements: reqTextGen.value,
      experiences: f.experiences.filter(e => e.company || e.position),
      projects: f.projects.filter(p => p.name),
      campus_activities: f.campus_activities.filter(c => c.name),
      awards: f.awards.filter(a => a.name),
    }
    await fetch('/api/resume/save', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        form_data: JSON.stringify(formData),
        generated_text: generatedText,
        template_id: selectedTemplate.value,
        career: targetCareer.value || f.job_intention || '',
        name: f.name || '',
      }),
    })
  } catch { /* 静默保存失败不影响用户 */ }
}

async function fetchHistory() {
  historyLoading.value = true
  try {
    const res = await fetch('/api/resume/history')
    historyRecords.value = (await res.json()).records || []
  } catch { ElMessage.error('加载历史失败') } finally { historyLoading.value = false }
}

async function restoreHistory(id) {
  try {
    const res = await fetch(`/api/resume/history/${id}`)
    if (!res.ok) { ElMessage.error('记录不存在'); return }
    const data = await res.json()
    const fd = data.form_data || {}
    // 恢复表单
    Object.keys(fd).forEach(key => {
      if (key === 'edu') { Object.assign(f.edu, fd.edu) }
      else if (key === 'experiences') { f.experiences = fd.experiences?.length ? fd.experiences.map(e => ({...e})) : [emptyExp()] }
      else if (key === 'projects') { f.projects = fd.projects?.length ? fd.projects.map(p => ({...p})) : [emptyPrj()] }
      else if (key === 'skills') { f.skills = fd.skills ? {...fd.skills} : { office: '', professional: '', programming: '', certificates: '', languages: '' } }
      else if (key === 'campus_activities') { f.campus_activities = fd.campus_activities || [] }
      else if (key === 'awards') { f.awards = fd.awards || [] }
      else if (key in f) { f[key] = fd[key] }
    })
    // 恢复模板和预览
    if (data.template_id) selectedTemplate.value = data.template_id
    if (data.career) targetCareer.value = data.career
    if (data.generated_text) genResult.value = data.generated_text
    showHistory.value = false
    ElMessage.success('已恢复该简历')
  } catch { ElMessage.error('恢复失败') }
}

async function deleteHistory(id) {
  try {
    await fetch(`/api/resume/history/${id}`, { method: 'DELETE' })
    historyRecords.value = historyRecords.value.filter(r => r.id !== id)
    ElMessage.success('已删除')
  } catch { ElMessage.error('删除失败') }
}

// 打开历史弹窗时自动加载
watch(showHistory, (v) => { if (v) fetchHistory() })
</script>

<style scoped>
/* ── 页面布局 ── */
.resume-page {
  position: relative;
}
.banner-wrap {
  position: relative;
}
.banner-cat {
  position: absolute;
  bottom: 0px;
  right: 320px;
  width: 60px;
  height: auto;
  pointer-events: none;
  z-index: 0;
  filter: drop-shadow(0 2px 8px rgba(0,0,0,0.18));
  transition: transform 0.3s ease;
}
.page-hint {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin: 4px 0 0;
}

/* ── 收藏条 ── */
.bm-active {
  font-size: 0.82rem;
  color: var(--primary);
  display: inline-flex;
  align-items: center;
}

/* ── 模板选择 ── */
.template-section {
  margin-bottom: 1.2rem;
}
.template-label {
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 0.6rem;
  color: var(--text-body);
  display: flex;
  align-items: center;
  gap: 6px;
}
.template-label i {
  color: var(--primary);
}
.template-track {
  display: flex;
  gap: 0.8rem;
  overflow-x: auto;
  padding-bottom: 0.4rem;
  scrollbar-width: thin;
}
.tpl-card {
  flex: 0 0 200px;
  border: 2px solid var(--border);
  border-radius: var(--radius-md);
  padding: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
  background: var(--bg-card);
}
.tpl-card:hover {
  border-color: var(--accent, var(--primary));
  box-shadow: var(--shadow-md);
}
.tpl-card.active {
  border-color: var(--accent, var(--primary));
  box-shadow: 0 0 0 1.5px var(--accent, var(--primary));
}
.tpl-preview {
  width: 100%;
  margin-bottom: 0.4rem;
}
.tpl-preview :deep(svg) {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 4px;
}
.tpl-name {
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--text-heading);
  margin-bottom: 0.15rem;
}
.tpl-desc {
  font-size: 0.72rem;
  color: var(--text-muted);
  line-height: 1.3;
}

/* ── 润色模式 ── */
.section-card {
  padding: 1.5rem;
  margin-bottom: 1rem;
}
.section-title-sm {
  font-weight: 600;
  font-size: 1rem;
  color: var(--text-heading);
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 0.8rem;
}
.section-title-sm i {
  color: var(--primary);
  font-size: 1.05rem;
}
.upload-zone {
  border: 2px dashed var(--border);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  margin-bottom: 0.8rem;
  background: var(--bg-alt);
}
.upload-zone:hover {
  border-color: var(--primary);
  background: var(--primary-bg);
}
.upload-zone.dragging {
  border-color: var(--primary);
  background: var(--primary-bg);
}
.upload-icon {
  font-size: 2.2rem;
  margin-bottom: 0.3rem;
  color: var(--primary);
  opacity: 0.6;
}
.upload-text {
  font-size: 0.85rem;
  color: var(--text-muted);
}
.upload-text i {
  color: var(--primary);
}
.opt-divider {
  text-align: center;
  color: var(--text-light);
  font-size: 0.8rem;
  margin: 0.5rem 0;
}
.opt-divider i {
  margin: 0 6px;
  font-size: 0.7rem;
}
.resume-input {
  margin-bottom: 1rem;
}
.req-section {
  margin-bottom: 1rem;
}
.req-row {
  display: flex;
  gap: 0.5rem;
  align-items: flex-start;
}
.req-input {
  flex: 1;
}
.req-upload {
  flex: 0 0 auto;
  padding-top: 0.2rem;
}
.req-file-name {
  font-size: 0.82rem;
  color: var(--primary);
  margin-top: 0.3rem;
}
.action-row {
  margin-bottom: 1rem;
}

/* ── 结果 ── */
.result-box {
  background: var(--primary-bg);
  border-radius: var(--radius-md);
  padding: 1.2rem;
  margin-top: 1.5rem;
  border: 1px solid var(--border);
}
.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
}
.result-header h4 {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 1rem;
  color: var(--text-heading);
}
.result-header h4 i {
  color: var(--primary);
}
.result-actions {
  display: flex;
  gap: 0.5rem;
}
.result-pre {
  white-space: pre-wrap;
  font-size: 0.85rem;
  line-height: 1.7;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 1rem;
  max-height: 600px;
  overflow-y: auto;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* ── 智能生成 ── */
.generate-wrap {
  margin-bottom: 1rem;
}
.gen-tip {
  margin-bottom: 1.5rem;
}
.info-card {
  margin-bottom: 1rem;
  border-radius: var(--radius-md);
}
.info-card-header {
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--text-heading);
  padding: 0.8rem 1rem;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  align-items: center;
  gap: 8px;
}
.info-card-header i {
  color: var(--primary);
  width: 18px;
  text-align: center;
}
.card-body {
  padding: 1rem;
}
.field-note {
  color: var(--text-muted);
  font-weight: 400;
  font-size: 0.8rem;
  margin-left: 0.3rem;
}
label {
  display: block;
  font-size: 0.82rem;
  color: var(--text-body);
  margin-bottom: 0.3rem;
}
.field-dense label {
  font-size: 0.82rem;
  color: var(--text-muted);
}
.multi-item {
  background: var(--bg-alt);
  border-radius: var(--radius-sm);
  padding: 0.8rem;
  margin-bottom: 0.8rem;
  border: 1px solid var(--border);
}
.multi-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}
.multi-num {
  font-weight: 600;
  color: var(--primary);
  font-size: 0.85rem;
}
.section-badge {
  font-weight: 700;
  font-size: 0.95rem;
  padding: 0.4rem 0.8rem;
  border-radius: var(--radius-sm);
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin: 1.5rem 0 1rem;
  background: var(--primary-gradient);
  color: white;
}
.section-badge i {
  font-size: 0.9rem;
}
.section-badge.bonus {
  background: var(--accent-gradient);
}
.gen-action {
  text-align: center;
  margin: 2rem 0 1rem;
}

/* ── 照片上传 ── */
.photo-upload-row {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 0.8rem;
  border-top: 1px solid var(--border-light);
}
.photo-upload-area {
  width: 80px;
  height: 110px;
  flex: 0 0 80px;
  border: 2px dashed var(--border);
  border-radius: var(--radius-sm);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.2s;
  background: var(--bg-alt);
}
.photo-upload-area:hover {
  border-color: var(--primary);
  background: var(--primary-bg);
}
.photo-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.photo-placeholder {
  text-align: center;
}
.photo-icon {
  font-size: 1.6rem;
  display: block;
  margin-bottom: 0.2rem;
  color: var(--text-muted);
}
.photo-hint {
  font-size: 0.7rem;
  color: var(--text-light);
  display: block;
}
.photo-info {
  flex: 1;
  padding-top: 0.2rem;
}
.photo-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-heading);
  margin-bottom: 0.2rem;
  display: flex;
  align-items: center;
  gap: 6px;
}
.photo-label i {
  color: var(--primary);
}
.photo-desc {
  font-size: 0.75rem;
  color: var(--text-muted);
  line-height: 1.4;
}

/* ── 简历历史 ── */
.history-dialog :deep(.el-dialog__header) {
  padding: 1rem 1.25rem 0;
}
.dialog-title {
  font-weight: 700;
  font-size: 1rem;
  color: var(--text-heading);
  display: flex;
  align-items: center;
  gap: 8px;
}
.dialog-title i {
  color: var(--primary);
}
.history-list {
  max-height: 400px;
  overflow-y: auto;
}
.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.8rem 0.5rem;
  border-bottom: 1px solid var(--border-light);
  transition: background 0.15s;
}
.history-item:hover {
  background: var(--bg-hover);
}
.history-item:last-child {
  border-bottom: none;
}
.history-info {
  flex: 1;
  min-width: 0;
}
.history-name {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-heading);
  margin-bottom: 0.2rem;
}
.history-meta {
  display: flex;
  gap: 0.6rem;
  align-items: center;
  flex-wrap: wrap;
  font-size: 0.78rem;
  color: var(--text-muted);
}
.history-tpl {
  background: var(--primary-bg);
  padding: 0.1rem 0.5rem;
  border-radius: 10px;
  color: var(--primary);
  font-weight: 500;
}
.history-career {
  color: var(--accent);
  display: inline-flex;
  align-items: center;
  gap: 3px;
}
.history-career i {
  font-size: 0.7rem;
}
.history-date {
  color: var(--text-light);
}
.history-actions {
  flex: 0 0 auto;
  display: flex;
  gap: 0.3rem;
  margin-left: 1rem;
}

/* ── 响应式 ── */
@media (max-width: 768px) {
  .template-track {
    gap: 0.5rem;
  }
  .tpl-card {
    flex: 0 0 160px;
  }
  .info-card .el-row {
    margin: 0 !important;
  }
  .info-card .el-col {
    margin-bottom: 8px;
  }
  .req-row {
    flex-direction: column;
  }
}
</style>