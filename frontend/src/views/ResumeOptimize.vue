<template>
  <div class="resume-page">
    <!-- ═══ PageBanner（跟笔试题、面试同风格） ═══ -->
    <PageBanner fullwidth
      title="简历优化"
      description="把经历讲清楚，让简历更像你自己"
      :icon="'FileEdit'"
      variant="primary"
      cat-src="/src/assets/resume-cat.png"
      cat-alt="小橘简历"
      :path-items="['上传简历', '优化建议', '版本管理']"
    >
      <template #actions>
        <el-button size="small" @click="showHistory = true" style="background:rgba(255,255,255,0.82);border:1.5px solid #BFDBFE;color:#2563EB;">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg> 简历历史
        </el-button>
      </template>
    </PageBanner>

    <!-- ═══ 收藏岗位快捷选择 ═══ -->
    <div v-if="bookmarks.length" class="bookmark-band">
      <div class="bm-band-header">
        <span class="bm-band-title"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg> 收藏岗位：</span>
        <div v-if="targetCareer" class="bm-active">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
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

    <!-- ═══════════════════ 内容区 ═══════════════════ -->
    <div class="resume-body">

    <!-- ═══ 模板选择 ═══ -->
        <div class="template-section">
          <div class="template-label">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="13.5" cy="6.5" r=".5" fill="#2563EB"/><circle cx="17.5" cy="6.5" r=".5" fill="#2563EB"/><circle cx="21.5" cy="6.5" r=".5" fill="#2563EB"/><path d="M2 7v11a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V7"/><path d="M6 2 4 6l.5 1L2 7v.5l2 1 1 2 1-2 2-1V7l-2.5-1L6 2z"/></svg>
            选择简历模板
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

        <!-- ═══ 双栏布局：左润色 + 右生成 ═══ -->
        <div class="resume-columns">

          <!-- ═══ 左栏：简历润色 ═══ -->
          <div class="resume-col col-optimize">
            <div class="col-header">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
              简历润色
            </div>

            <!-- ════════════════════════════════════════
                 润色模式
                 ════════════════════════════════════════ -->
            <div class="mode-body">
          <!-- 上传区 -->
          <div class="section-block">
            <div class="block-title">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              上传或粘贴简历
            </div>
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
              <div class="upload-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              </div>
              <div class="upload-text">
                <span v-if="!uploadedFile">点击或拖拽上传简历文件（.txt / .pdf / .docx）</span>
                <span v-else style="color:#2563EB"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline;vertical-align:middle;margin-right:4px"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>{{ uploadedFile }}</span>
              </div>
            </div>

            <div class="opt-divider">— 或者直接粘贴文本 —</div>

            <textarea v-model="resumeText" :rows="6" placeholder="请粘贴你的简历文本内容…" class="resume-textarea"></textarea>
          </div>

          <!-- 定制要求 -->
          <div class="section-block">
            <div class="block-title" style="font-size:14px">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14.39A6 6 0 0 0 12 3a6 6 0 0 0-3.09 11.39"/><path d="M12 17v-2.5"/></svg>
              定制要求 <span class="field-note">（可选）</span>
            </div>
            <div class="req-row">
              <textarea v-model="reqText" :rows="3" placeholder="例如：我想突出项目经验，把技能放最后。或者：帮我精简到一页。" class="resume-textarea" style="flex:1"></textarea>
              <div class="req-upload" @click="triggerReqInput">
                <input ref="reqFileInput" type="file" accept=".txt" style="display:none" @change="onReqFileChange" />
                <el-button text size="small">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg> 传文件
                </el-button>
              </div>
            </div>
            <div v-if="reqFileName" class="req-file-name"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline;vertical-align:middle;margin-right:4px"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>{{ reqFileName }}</div>
          </div>

          <!-- 生成按钮 -->
          <div class="action-row">
            <button class="btn-primary" :disabled="optLoading" @click="generateWithTemplate">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:6px"><path d="M12 3l2.18 6.02L20 9.24l-4.57 4.47L16.36 20 12 16.86 7.64 20l.93-6.29L4 9.24l5.82-1.22z"/></svg>
              {{ optLoading ? '生成中…' : '按模板生成简历' }}
            </button>
          </div>

          <!-- 结果 -->
          <div v-if="optResult" class="result-box">
            <div class="result-header">
              <h4><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg> AI 生成的简历</h4>
              <div class="result-actions">
                <button class="btn-outline" @click="copyResult(optResult)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg> 复制全文</button>
              </div>
            </div>
            <pre class="result-pre">{{ optResult }}</pre>
          </div>
        </div>
      </div>
      <!-- ═══ 左栏结束 ═══ -->

      <!-- ═══ 右栏：智能生成 ═══ -->
      <div class="resume-col col-generate">
        <div class="col-header">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.18 6.02L20 9.24l-4.57 4.47L16.36 20 12 16.86 7.64 20l.93-6.29L4 9.24l5.82-1.22z"/></svg>
          智能生成
        </div>

        <!-- ════════════════════════════════════════
             智能生成模式
             ════════════════════════════════════════ -->
        <div class="mode-body">
          <div v-if="targetCareer" class="gen-tip-bar">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>
            🎯 正在为「{{ targetCareer }}」生成简历
          </div>

          <!-- 个性化需求 -->
          <div class="section-block">
            <div class="block-title">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14.39A6 6 0 0 0 12 3a6 6 0 0 0-3.09 11.39"/><path d="M12 17v-2.5"/></svg>
              个性化需求 <span class="field-note">（可选）</span>
            </div>
            <div class="req-row">
              <textarea v-model="reqTextGen" :rows="3" placeholder="例如：在校大学生找前端实习，突出Vue项目。或：要一页纸简历。" class="resume-textarea" style="flex:1"></textarea>
              <div class="req-upload" @click="triggerGenReqInput">
                <input ref="genReqFileInput" type="file" accept=".txt" style="display:none" @change="onGenReqFileChange" />
                <el-button text size="small">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg> 传文件
                </el-button>
              </div>
            </div>
            <div v-if="genReqFileName" class="req-file-name"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline;vertical-align:middle;margin-right:4px"><path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66l-9.2 9.19a2 2 0 0 1-2.83-2.83l8.49-8.48"/></svg>{{ genReqFileName }}</div>
          </div>
          <!-- 基础信息结束 -->

          <div class="form-grid">

          <!-- ① 基础信息 -->
          <div class="section-badge">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            基础信息（必填）
          </div>

          <div class="form-card">
            <div class="form-card-header"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> ① 个人基本信息</div>
            <div class="form-card-body">
              <div class="form-row">
                <input v-model="f.name" placeholder="姓名" />
                <select v-model="f.gender" style="width:100%">
                  <option value="" disabled>性别</option>
                  <option value="男">男</option>
                  <option value="女">女</option>
                </select>
                <input v-model="f.age" placeholder="年龄" type="number" />
              </div>
              <div class="form-row">
                <input v-model="f.phone" placeholder="联系电话" />
                <input v-model="f.email" placeholder="邮箱" />
                <input v-model="f.address" placeholder="现居地址" />
              </div>
              <div class="form-row">
                <input v-model="f.job_intention" placeholder="求职意向岗位" />
                <input v-model="f.target_location" placeholder="期望工作地点" />
                <input v-model="f.wechat" placeholder="微信号（可选）" />
              </div>
              <!-- 照片 -->
              <div class="photo-row">
                <div class="photo-upload-area" @click="triggerPhotoInput">
                  <img v-if="f.photo" :src="f.photo" class="photo-preview" />
                  <div v-else class="photo-placeholder">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
                    <span class="photo-hint">上传证件照</span>
                  </div>
                </div>
                <div class="photo-info">
                  <div class="photo-label"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg> 证件照片</div>
                  <div class="photo-desc">标准证件照，白底/蓝底均可<br/>JPG / PNG，建议 2.5×3.5cm</div>
                  <el-button v-if="f.photo" text size="small" type="danger" @click.stop="f.photo = ''">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v5"/><path d="M14 11v5"/><path d="M9 6V4h6v2"/></svg> 删除照片
                  </el-button>
                </div>
                <input ref="photoInput" type="file" accept="image/*" style="display:none" @change="onPhotoChange" />
              </div>
            </div>
          </div>

          <!-- ② 教育经历 -->
          <div class="form-card">
            <div class="form-card-header"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 2 2.5 3 6 3s6-1 6-3v-5"/></svg> ② 教育经历</div>
            <div class="form-card-body">
              <div class="form-row">
                <input v-model="f.edu.school" placeholder="就读院校" />
                <input v-model="f.edu.major" placeholder="专业" />
                <select v-model="f.edu.degree" style="width:100%">
                  <option value="" disabled>学历</option>
                  <option value="大专">大专</option>
                  <option value="本科">本科</option>
                  <option value="硕士">硕士</option>
                  <option value="博士">博士</option>
                </select>
              </div>
              <div class="form-row">
                <input v-model="f.edu.start_date" placeholder="入学时间" />
                <input v-model="f.edu.end_date" placeholder="毕业时间" />
              </div>
              <div class="field-dense">
                <label>主修课程 <span class="field-note">（选与岗位相关的写）</span></label>
                <input v-model="f.edu.courses" placeholder="如：数据结构、操作系统、计算机网络" style="width:100%;padding:8px 12px;border:1px solid #E2E8F0;border-radius:10px;font-size:13px" />
              </div>
            </div>
          </div>

          <!-- ③ 工作/实习经历 -->
          <div class="form-card">
            <div class="form-card-header"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg> ③ 工作/实习经历</div>
            <div class="form-card-body">
              <div v-for="(e, i) in f.experiences" :key="i" class="multi-item">
                <div class="multi-header">
                  <span class="multi-num">#{{ i + 1 }}</span>
                  <el-button text type="danger" size="small" @click="f.experiences.splice(i, 1)">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v5"/><path d="M14 11v5"/></svg> 删除
                  </el-button>
                </div>
                <div class="form-row">
                  <input v-model="e.company" placeholder="单位名称" />
                  <input v-model="e.position" placeholder="岗位" />
                  <input v-model="e.period" placeholder="时间" />
                </div>
                <div class="field-dense" style="margin-top:8px">
                  <label>内容 + 成果 <span class="field-note">（用数据、短句）</span></label>
                  <textarea v-model="e.content" :rows="3" placeholder="一行一个要点" style="width:100%;padding:8px 12px;border:1px solid #E2E8F0;border-radius:10px;font-size:13px;resize:vertical"></textarea>
                </div>
              </div>
              <el-button text type="primary" @click="addExperience">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg> 添加一条经历
              </el-button>
            </div>
          </div>

          <!-- ④ 项目经历 -->
          <div class="form-card">
            <div class="form-card-header"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="6" y1="3" x2="6" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg> ④ 项目经历</div>
            <div class="form-card-body">
              <div v-for="(p, i) in f.projects" :key="i" class="multi-item">
                <div class="multi-header">
                  <span class="multi-num">#{{ i + 1 }}</span>
                  <el-button text type="danger" size="small" @click="f.projects.splice(i, 1)">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v5"/><path d="M14 11v5"/></svg> 删除
                  </el-button>
                </div>
                <div class="form-row">
                  <input v-model="p.name" placeholder="项目名称" />
                  <input v-model="p.period" placeholder="参与时间" />
                  <input v-model="p.role" placeholder="个人职责" />
                </div>
                <div class="field-dense" style="margin-top:8px">
                  <label>项目成果 / 收获</label>
                  <textarea v-model="p.achievement" :rows="3" placeholder="成果描述，一行一个要点" style="width:100%;padding:8px 12px;border:1px solid #E2E8F0;border-radius:10px;font-size:13px;resize:vertical"></textarea>
                </div>
              </div>
              <el-button text type="primary" @click="addProject">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg> 添加一个项目
              </el-button>
            </div>
          </div>

          <!-- ⑤ 专业技能 -->
          <div class="form-card">
            <div class="form-card-header"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg> ⑤ 专业技能</div>
            <div class="form-card-body">
              <div class="form-row">
                <div class="field-dense"><label>办公软件</label><input v-model="f.skills.office" placeholder="如：Word、Excel、PPT" style="width:100%;padding:8px 12px;border:1px solid #E2E8F0;border-radius:10px;font-size:13px" /></div>
                <div class="field-dense"><label>专业软件</label><input v-model="f.skills.professional" placeholder="如：PS、CAD、Figma" style="width:100%;padding:8px 12px;border:1px solid #E2E8F0;border-radius:10px;font-size:13px" /></div>
              </div>
              <div class="form-row">
                <div class="field-dense"><label>编程语言</label><input v-model="f.skills.programming" placeholder="如：Python、JavaScript、Java" style="width:100%;padding:8px 12px;border:1px solid #E2E8F0;border-radius:10px;font-size:13px" /></div>
                <div class="field-dense"><label>证书</label><input v-model="f.skills.certificates" placeholder="如：CET-4、计算机二级" style="width:100%;padding:8px 12px;border:1px solid #E2E8F0;border-radius:10px;font-size:13px" /></div>
              </div>
              <div class="form-row">
                <div class="field-dense"><label>语言能力</label><input v-model="f.skills.languages" placeholder="如：普通话二甲、CET-6" style="width:100%;padding:8px 12px;border:1px solid #E2E8F0;border-radius:10px;font-size:13px" /></div>
              </div>
            </div>
          </div>

          <!-- ⑥ 校园经历 -->
          <div class="section-badge bonus">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            加分项（可选）
          </div>

          <div class="form-card">
            <div class="form-card-header"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c0 2 2.5 3 6 3s6-1 6-3v-5"/></svg> ⑥ 校园经历 <span class="field-note">（应届生重点）</span></div>
            <div class="form-card-body">
              <div v-for="(c, i) in f.campus_activities" :key="i" class="multi-item">
                <div class="multi-header">
                  <span class="multi-num">#{{ i + 1 }}</span>
                  <el-button text type="danger" size="small" @click="f.campus_activities.splice(i, 1)">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v5"/><path d="M14 11v5"/></svg> 删除
                  </el-button>
                </div>
                <div class="form-row">
                  <input v-model="c.name" placeholder="活动/组织名称" />
                  <input v-model="c.period" placeholder="时间" />
                  <input v-model="c.role" placeholder="职责描述" />
                </div>
              </div>
              <el-button text type="primary" @click="addCampus">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg> 添加校园经历
              </el-button>
            </div>
          </div>

          <!-- ⑦ 荣誉奖项 -->
          <div class="form-card">
            <div class="form-card-header"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5C7 4 7 6 7 6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5C17 4 17 6 17 6"/><path d="M4 22h16"/><path d="M10 22v-5"/><path d="M14 22v-5"/><path d="M6 9v6c0 2 2.5 3 6 3s6-1 6-3V9"/><path d="M10 15h4"/><path d="M10 11h4"/></svg> ⑦ 荣誉奖项</div>
            <div class="form-card-body">
              <div v-for="(a, i) in f.awards" :key="i" class="multi-item">
                <div class="multi-header">
                  <span class="multi-num">#{{ i + 1 }}</span>
                  <el-button text type="danger" size="small" @click="f.awards.splice(i, 1)">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v5"/><path d="M14 11v5"/></svg> 删除
                  </el-button>
                </div>
                <div class="form-row">
                  <input v-model="a.name" placeholder="奖项名称" />
                  <input v-model="a.period" placeholder="获奖时间" />
                  <input v-model="a.issuer" placeholder="颁发单位（可选）" />
                </div>
              </div>
              <el-button text type="primary" @click="addAward">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg> 添加奖项
              </el-button>
            </div>
          </div>

          <!-- ⑧ 自我评价 -->
          <div class="form-card">
            <div class="form-card-header"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg> ⑧ 自我评价 <span class="field-note">（简短，贴合岗位）</span></div>
            <div class="form-card-body">
              <textarea v-model="f.self_evaluation" :rows="4" placeholder="总结个人优势、性格、职业态度，避免空话套话" style="width:100%;padding:10px 14px;border:1px solid #E2E8F0;border-radius:12px;font-size:14px;resize:vertical;line-height:1.6"></textarea>
            </div>
          </div>

          <!-- 生成按钮 -->
          </div>
          <!-- ═══ 表单网格结束 ═══ -->

          <div class="gen-action">
            <button class="btn-primary btn-lg" :disabled="genLoading" @click="generateSmart">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:6px"><path d="M12 3l2.18 6.02L20 9.24l-4.57 4.47L16.36 20 12 16.86 7.64 20l.93-6.29L4 9.24l5.82-1.22z"/></svg>
              {{ genLoading ? '生成中…' : '生成简历' }}
            </button>
          </div>

          <!-- 生成结果 -->
          <div v-if="genResult" class="result-box">
            <div class="result-header">
              <h4><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg> 预览</h4>
              <div class="result-actions">
                <button class="btn-primary" :disabled="dlLoading" @click="downloadDocx"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:4px"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg> {{ dlLoading ? '下载中…' : '下载 Word' }}</button>
                <button class="btn-outline" @click="copyResult(genResult)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg> 复制全文</button>
              </div>
            </div>
            <pre class="result-pre">{{ genResult }}</pre>
          </div>
        </div>
      </div>
      <!-- ═══ 右栏结束 ═══ -->
    </div>
    <!-- ═══ 双栏布局结束 ═══ -->

    <!-- ═══ 品牌 Footer ═══ -->
    </div>
    <!-- ═══════════════════════ 内容区结束 ═══════════════════════ -->

    <div class="brand-footer">
      <div class="bf-brand">启途 · <span class="qitu-up">QITU</span></div>
      <div class="bf-slogan">向上生长，自有答案</div>
    </div>

    <!-- ═══ 简历历史弹窗 ═══ -->
    <el-dialog v-model="showHistory" width="640px" destroy-on-close class="history-dialog">
      <template #header>
        <span class="dialog-title"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z"/><polyline points="13 2 13 9 20 9"/></svg> 简历历史</span>
      </template>
      <div v-if="historyLoading" class="loading-state">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="spin"><line x1="12" y1="2" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="22"/><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"/><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"/><line x1="2" y1="12" x2="6" y2="12"/><line x1="18" y1="12" x2="22" y2="12"/><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"/><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"/></svg> 加载中...
      </div>
      <div v-else-if="historyRecords.length === 0" class="empty-state">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="opacity:.4"><polyline points="21 16 17 12 13 16"/><path d="M17 12v8"/><path d="M3 12h4a2 2 0 0 0 2-2V6"/><path d="M3 6h4a2 2 0 0 1 2 2v4"/></svg>
        <p>暂无保存的简历</p>
        <p class="empty-hint">生成简历后会自动保存到历史中</p>
      </div>
      <div v-else class="history-list">
        <div v-for="r in historyRecords" :key="r.id" class="history-item">
          <div class="history-info">
            <div class="history-name">{{ r.name || '未命名' }}</div>
            <div class="history-meta">
              <span class="history-tpl">{{ r.template_name }}</span>
              <span v-if="r.career" class="history-career"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#0EA5E9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg> {{ r.career }}</span>
              <span class="history-date">{{ r.created_at }}</span>
            </div>
          </div>
          <div class="history-actions">
            <el-button size="small" text @click="restoreHistory(r.id)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg> 恢复
            </el-button>
            <el-button size="small" text type="danger" @click="deleteHistory(r.id)">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v5"/><path d="M14 11v5"/></svg> 删除
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
      <rect x="10" y="34" width="66" height="200" rx="4" fill="#fef7e6"/>
      <text x="20" y="54" font-size="7.5" fill="#d4890b" font-weight="bold">个人信息</text>
      <rect x="16" y="62" width="54" height="4" rx="2" fill="#eee"/>
      <rect x="16" y="70" width="48" height="4" rx="2" fill="#eee"/>
      <text x="20" y="90" font-size="7.5" fill="#d4890b" font-weight="bold">专业技能</text>
      <rect x="16" y="98" width="54" height="24" rx="3" fill="#f5d68a" opacity="0.5"/>
      <rect x="16" y="126" width="54" height="24" rx="3" fill="#f5d68a" opacity="0.5"/>
      <rect x="16" y="154" width="54" height="24" rx="3" fill="#f5d68a" opacity="0.5"/>
      <rect x="16" y="182" width="54" height="24" rx="3" fill="#f5d68a" opacity="0.5"/>
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
      <rect x="15" y="94" width="22" height="52" rx="3" fill="#10b981" opacity="0.25"/>
      <text x="17" y="160" font-size="5" fill="#10b981">2024</text>
      <rect x="42" y="94" width="138" height="20" rx="3" fill="#e8f5ed"/>
      <text x="50" y="107" font-size="7.5" fill="#333">项目 A — 主要职责</text>
      <rect x="42" y="118" width="138" height="28" rx="3" fill="#f0f0f0"/>
      <line x1="50" y1="127" x2="120" y2="127" stroke="#ccc" stroke-width="1"/>
      <line x1="50" y1="133" x2="110" y2="133" stroke="#ccc" stroke-width="1"/>
      <line x1="50" y1="139" x2="130" y2="139" stroke="#ccc" stroke-width="1"/>
      <rect x="15" y="152" width="22" height="52" rx="3" fill="#10b981" opacity="0.25"/>
      <rect x="42" y="152" width="138" height="20" rx="3" fill="#e8f5ed"/>
      <text x="50" y="165" font-size="7.5" fill="#333">项目 B — 主要职责</text>
      <rect x="42" y="176" width="138" height="28" rx="3" fill="#f0f0f0"/>
      <line x1="50" y1="185" x2="115" y2="185" stroke="#ccc" stroke-width="1"/>
      <line x1="50" y1="191" x2="105" y2="191" stroke="#ccc" stroke-width="1"/>
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
      <rect x="20" y="36" width="160" height="48" rx="4" fill="#fde8e8"/>
      <text x="28" y="52" font-size="9" fill="#ef4444" font-weight="bold">🎓 教育经历</text>
      <rect x="28" y="58" width="144" height="4" rx="2" fill="#f5c6c6" opacity="0.6"/>
      <rect x="28" y="66" width="120" height="4" rx="2" fill="#f5c6c6" opacity="0.4"/>
      <rect x="28" y="74" width="100" height="4" rx="2" fill="#f5c6c6" opacity="0.3"/>
      <rect x="20" y="92" width="160" height="48" rx="4" fill="#fde8e8" opacity="0.7"/>
      <text x="28" y="108" font-size="9" fill="#ef4444" font-weight="bold">🏫 校园经历</text>
      <rect x="28" y="114" width="144" height="4" rx="2" fill="#f5c6c6" opacity="0.6"/>
      <rect x="28" y="122" width="120" height="4" rx="2" fill="#f5c6c6" opacity="0.4"/>
      <rect x="28" y="130" width="100" height="4" rx="2" fill="#f5c6c6" opacity="0.3"/>
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
      <rect x="0" y="12" width="200" height="4" fill="#8b5cf6" opacity="0.3"/>
      <rect x="20" y="24" width="160" height="8" rx="4" fill="#8b5cf6" opacity="0.6"/>
      <rect x="20" y="38" width="130" height="18" rx="3" fill="#f3eefb"/>
      <text x="28" y="50" font-size="7.5" fill="#8b5cf6">个人信息</text>
      <rect x="156" y="39" width="24" height="16" rx="2" fill="#8b5cf6" opacity="0.4"/>
      <rect x="20" y="62" width="160" height="50" rx="3" fill="#f0f0f0"/>
      <text x="28" y="76" font-size="8" fill="#888" font-weight="bold">工作经历</text>
      <rect x="28" y="82" width="100" height="5" rx="2" fill="#ddd"/>
      <rect x="28" y="82" width="72" height="5" rx="2" fill="#a78bfa" opacity="0.6"/>
      <rect x="28" y="91" width="120" height="5" rx="2" fill="#ddd"/>
      <rect x="28" y="91" width="85" height="5" rx="2" fill="#a78bfa" opacity="0.5"/>
      <rect x="28" y="100" width="80" height="5" rx="2" fill="#ddd"/>
      <rect x="28" y="100" width="55" height="5" rx="2" fill="#a78bfa" opacity="0.5"/>
      <rect x="20" y="118" width="160" height="50" rx="3" fill="#f0f0f0"/>
      <text x="28" y="132" font-size="8" fill="#888" font-weight="bold">项目经历</text>
      <rect x="28" y="138" width="100" height="5" rx="2" fill="#ddd"/>
      <rect x="28" y="138" width="68" height="5" rx="2" fill="#a78bfa" opacity="0.6"/>
      <rect x="28" y="147" width="120" height="5" rx="2" fill="#ddd"/>
      <rect x="28" y="147" width="90" height="5" rx="2" fill="#a78bfa" opacity="0.5"/>
      <rect x="28" y="156" width="80" height="5" rx="2" fill="#ddd"/>
      <rect x="28" y="156" width="60" height="5" rx="2" fill="#a78bfa" opacity="0.5"/>
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
    Object.keys(fd).forEach(key => {
      if (key === 'edu') { Object.assign(f.edu, fd.edu) }
      else if (key === 'experiences') { f.experiences = fd.experiences?.length ? fd.experiences.map(e => ({...e})) : [emptyExp()] }
      else if (key === 'projects') { f.projects = fd.projects?.length ? fd.projects.map(p => ({...p})) : [emptyPrj()] }
      else if (key === 'skills') { f.skills = fd.skills ? {...fd.skills} : { office: '', professional: '', programming: '', certificates: '', languages: '' } }
      else if (key === 'campus_activities') { f.campus_activities = fd.campus_activities || [] }
      else if (key === 'awards') { f.awards = fd.awards || [] }
      else if (key in f) { f[key] = fd[key] }
    })
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

watch(showHistory, (v) => { if (v) fetchHistory() })
</script>

<style scoped>
/* ═══════════════════════════════════════════════
   页面基础
   ═══════════════════════════════════════════════ */
.resume-page {
  position: relative;
  min-height: 100vh;
  background: #F5F7FF;
  margin-left: calc(0px - var(--main-pad-x, 28px));
  margin-right: calc(0px - var(--main-pad-x, 28px));
}

/* ═══ 内容区 ═══ */
.resume-body {
  padding: 0 0 32px;
}

/* ═══ 收藏岗位条 ═══ */
.bookmark-band {
  background: transparent;
  border: none;
  border-radius: 0;
  padding: 10px 0;
  margin-bottom: 0;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid #E2E8F0;
}
.bm-band-header {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.bm-band-title {
  font-weight: 600;
  font-size: 13px;
  color: #1E293B;
  display: flex;
  align-items: center;
  gap: 4px;
}
.bm-active {
  font-size: 12px;
  color: #2563EB;
  display: inline-flex;
  align-items: center;
}
.bm-band-scroll {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* ═══ 模式切换（润色/生成） ═══ */
/* ═══ 双栏布局 ═══ */
.resume-columns {
  display: flex;
  gap: 24px;
  align-items: stretch;
  max-height: calc(100vh - 280px);
  overflow: hidden;
}
.resume-col {
  flex: 1;
  min-width: 0;
  padding: 20px;
  background: #fff;
  border: 1.5px dashed #BFDBFE;
  border-radius: 18px;
  display: flex;
  flex-direction: column;
}
.resume-col .mode-body {
  flex: 1;
}
.col-generate .mode-body {
  overflow-y: auto;
  padding-right: 4px;
}
.col-header {
  font-weight: 700;
  font-size: 16px;
  color: #1E293B;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 18px;
  padding-left: 12px;
  border-left: 3px solid #2563EB;
  line-height: 1.4;
}
.col-header svg { flex-shrink: 0; }

/* ═══ 模板选择 ═══ */
.template-section {
  margin-bottom: 24px;
  background: #fff;
  border-radius: 18px;
  padding: 20px 22px;
  border: 1.5px dashed #BFDBFE;
  position: relative;
}
.template-section::before {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, transparent 50%, #EFF6FF 50%);
  border-radius: 0 18px 0 0;
}
.template-label {
  font-weight: 700;
  font-size: 15px;
  margin-bottom: 12px;
  color: #1E293B;
  display: flex;
  align-items: center;
  gap: 8px;
  padding-left: 12px;
  border-left: 3px solid #2563EB;
  line-height: 1.4;
}
.template-track {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 6px;
  scrollbar-width: thin;
}
.tpl-card {
  flex: 0 0 180px;
  border: 2px solid #E2E8F0;
  border-radius: 14px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.2s;
  background: #fff;
}
.tpl-card:hover {
  border-color: var(--accent, #0EA5E9);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}
.tpl-card.active {
  border-color: var(--accent, #0EA5E9);
  box-shadow: 0 0 0 2px var(--accent, #0EA5E9);
}
.tpl-preview { width: 100%; margin-bottom: 6px; }
.tpl-preview :deep(svg) { display: block; width: 100%; height: auto; border-radius: 4px; }
.tpl-name { font-weight: 700; font-size: 14px; color: #1E293B; margin-bottom: 2px; }
.tpl-desc { font-size: 11px; color: #94A3B8; line-height: 1.3; }

/* ═══ 模式内容区 ═══ */
.mode-body { }

/* ═══ 区块标题 ═══ */
.section-block {
  margin-bottom: 22px;
  background: #fff;
  border-radius: 18px;
  padding: 18px 20px 20px;
  border: 1.5px dashed #BFDBFE;
}

/* 自带蓝色顶部边框 */
.block-title {
  font-weight: 700;
  font-size: 15px;
  color: #1E293B;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  padding-left: 12px;
  border-left: 3px solid #2563EB;
  line-height: 1.4;
}
.block-title svg { flex-shrink: 0; }

/* ═══ 上传区 ═══ */
.upload-zone {
  border: 2px dashed #BFDBFE;
  border-radius: 14px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: #F8FAFF;
  margin-bottom: 10px;
}
.upload-zone:hover {
  border-color: #2563EB;
  background: #EFF6FF;
}
.upload-zone.dragging {
  border-color: #2563EB;
  background: #DBEAFE;
}
.upload-icon { font-size: 32px; margin-bottom: 6px; color: #2563EB; opacity: 0.6; }
.upload-text { font-size: 13px; color: #94A3B8; }

/* ═══ 分割线 ═══ */
.opt-divider {
  text-align: center;
  color: #94A3B8;
  font-size: 12px;
  margin: 8px 0;
}

/* ═══ 文本域 ═══ */
.resume-textarea {
  width: 100%;
  padding: 10px 14px;
  border: 1.5px solid #E2E8F0;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  resize: vertical;
  font-family: inherit;
  box-sizing: border-box;
  transition: border-color 0.2s;
}
.resume-textarea:focus {
  outline: none;
  border-color: #2563EB;
  box-shadow: 0 0 0 3px rgba(37,99,235,0.1);
}

/* ═══ 需求行 ═══ */
.req-row {
  display: flex;
  gap: 8px;
  align-items: flex-start;
}
.req-upload { flex-shrink: 0; padding-top: 2px; }
.req-file-name {
  font-size: 12px;
  color: #2563EB;
  margin-top: 4px;
  display: flex;
  align-items: center;
}

/* ═══ 按钮 ═══ */
.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 10px 24px;
  border: none;
  border-radius: 14px;
  background: #2563EB;
  color: #fff;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(37,99,235,0.2);
}
.btn-primary:hover:not(:disabled) {
  background: #1D4ED8;
  box-shadow: 0 6px 16px rgba(37,99,235,0.3);
  transform: translateY(-1px);
}
.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.btn-primary.btn-lg {
  padding: 14px 40px;
  font-size: 16px;
}
.btn-outline {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 18px;
  border: 1.5px solid #BFDBFE;
  border-radius: 12px;
  background: transparent;
  color: #2563EB;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-outline:hover {
  background: #EFF6FF;
  border-color: #2563EB;
}

/* ═══ 操作行 ═══ */
.action-row {
  margin-bottom: 16px;
}

/* ═══ 结果框 ═══ */
.result-box {
  background: #F8FAFF;
  border-radius: 16px;
  padding: 18px;
  margin-top: 20px;
  border: 1px solid #DBEAFE;
}
.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.result-header h4 {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  color: #1E293B;
}
.result-actions {
  display: flex;
  gap: 8px;
}
.result-pre {
  white-space: pre-wrap;
  font-size: 13px;
  line-height: 1.7;
  background: #fff;
  border: 1px solid #E2E8F0;
  border-radius: 12px;
  padding: 14px;
  max-height: 600px;
  overflow-y: auto;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* ═══ 表单双列网格 ═══ */
.form-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ═══ 生成模式提示条 ═══ */
.gen-tip-bar {
  background: #EFF6FF;
  border: 1px solid #BFDBFE;
  border-radius: 14px;
  padding: 12px 16px;
  margin-bottom: 20px;
  font-size: 14px;
  color: #1E293B;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ═══ 标题徽章 ═══ */
.section-badge {
  font-weight: 700;
  font-size: 14px;
  padding: 8px 16px;
  border-radius: 12px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin: 16px 0 12px;
  background: linear-gradient(135deg, #2563EB, #0EA5E9);
  color: white;
  box-shadow: 0 2px 8px rgba(37,99,235,0.2);
}
.section-badge.bonus {
  background: linear-gradient(135deg, #0EA5E9, #06B6D4);
}

/* ═══ 表单卡片 ═══ */
.form-card {
  border: 1.5px dashed #BFDBFE;
  border-radius: 16px;
  background: #fff;
  margin-bottom: 16px;
  overflow: hidden;
}
.form-card-header {
  font-weight: 700;
  font-size: 14px;
  color: #1E293B;
  padding: 12px 16px;
  border-bottom: 1px solid #EFF6FF;
  display: flex;
  align-items: center;
  gap: 8px;
  background: #F8FAFF;
  padding-left: 16px;
  border-left: 3px solid #2563EB;
}
.form-card-body {
  padding: 14px 16px;
}
.form-row {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
  flex-wrap: wrap;
}
.form-row input,
.form-row select {
  flex: 1;
  min-width: 120px;
  padding: 8px 12px;
  border: 1px solid #E2E8F0;
  border-radius: 10px;
  font-size: 13px;
  transition: border-color 0.2s;
  background: #fff;
  box-sizing: border-box;
}
.form-row input:focus,
.form-row select:focus {
  outline: none;
  border-color: #2563EB;
  box-shadow: 0 0 0 3px rgba(37,99,235,0.1);
}
.field-note {
  color: #94A3B8;
  font-weight: 400;
  font-size: 12px;
  margin-left: 4px;
}
.field-dense label {
  display: block;
  font-size: 12px;
  color: #64748B;
  margin-bottom: 4px;
}
.multi-item {
  background: #FAFBFC;
  border-radius: 12px;
  padding: 12px;
  margin-bottom: 10px;
  border: 1px solid #E2E8F0;
}
.multi-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.multi-num {
  font-weight: 700;
  color: #2563EB;
  font-size: 13px;
}

/* ═══ 照片上传 ═══ */
.photo-row {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid #F1F5F9;
}
.photo-upload-area {
  width: 80px;
  height: 110px;
  flex-shrink: 0;
  border: 2px dashed #BFDBFE;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.2s;
  background: #F8FAFF;
}
.photo-upload-area:hover {
  border-color: #2563EB;
  background: #EFF6FF;
}
.photo-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.photo-placeholder { text-align: center; }
.photo-hint { font-size: 10px; color: #94A3B8; display: block; margin-top: 4px; }
.photo-info { flex: 1; }
.photo-label {
  font-size: 13px;
  font-weight: 600;
  color: #1E293B;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.photo-desc {
  font-size: 11px;
  color: #94A3B8;
  line-height: 1.4;
}

/* ═══ 生成按钮居中 ═══ */
.gen-action {
  text-align: center;
  margin: 24px 0 8px;
}

/* ═══ 品牌 Footer ═══ */
.brand-footer {
  text-align: center;
  padding: 24px 0 32px;
  color: #94A3B8;
  font-size: 13px;
}
.bf-brand { font-weight: 700; margin-bottom: 4px; color: #64748B; }
.qitu-up { color: #2563EB; font-weight: 700; letter-spacing: 2px; }
.bf-slogan { font-size: 12px; color: #94A3B8; }

/* ═══ 简历历史弹窗 ═══ */
.history-dialog :deep(.el-dialog__header) {
  padding: 16px 20px 0;
}
.dialog-title {
  font-weight: 700;
  font-size: 15px;
  color: #1E293B;
  display: flex;
  align-items: center;
  gap: 8px;
}
.history-list {
  max-height: 400px;
  overflow-y: auto;
}
.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 8px;
  border-bottom: 1px solid #F1F5F9;
  transition: background 0.15s;
}
.history-item:hover { background: #F8FAFF; }
.history-item:last-child { border-bottom: none; }
.history-info { flex: 1; min-width: 0; }
.history-name { font-weight: 600; font-size: 14px; color: #1E293B; margin-bottom: 3px; }
.history-meta {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
  font-size: 12px;
  color: #94A3B8;
}
.history-tpl {
  background: #EFF6FF;
  padding: 2px 8px;
  border-radius: 10px;
  color: #2563EB;
  font-weight: 600;
  font-size: 11px;
}
.history-career {
  color: #0EA5E9;
  display: inline-flex;
  align-items: center;
  gap: 3px;
}
.history-date { color: #94A3B8; }
.history-actions {
  flex-shrink: 0;
  display: flex;
  gap: 4px;
  margin-left: 12px;
}

/* ═══ 加载/空状态 ═══ */
.loading-state {
  text-align: center;
  padding: 24px;
  color: #94A3B8;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.spin { animation: rSpin 1s linear infinite; }
@keyframes rSpin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
.empty-state {
  text-align: center;
  padding: 32px 20px;
  color: #94A3B8;
}
.empty-state p { margin: 8px 0 0; font-size: 14px; }
.empty-hint { font-size: 12px; color: #CBD5E1; margin-top: 4px !important; }

/* ═══ 响应式 ═══ */
@media (max-width: 768px) {
  .template-track { gap: 6px; }
  .tpl-card { flex: 0 0 140px; }
  .form-row { flex-direction: column; }
  .form-row input,
  .form-row select { min-width: auto; }
  .req-row { flex-direction: column; }
  .result-actions { flex-direction: column; gap: 6px; }
}
</style>