<template>
  <div class="page delivery-page">
    <!-- ═══ 页面顶部 Banner ═══ -->
    <div class="banner-wrap">
      <PageBanner fullwidth
        title="投递助手"
        description="记录投递进展，提醒及时跟进"
        :icon="'Send'"
        variant="primary"
        cat-src="/src/assets/delivery-cat.png"
        cat-alt="小橘投递"
        :path-items="['岗位记录', '投递进度', '跟进提醒']"
      />
    </div>
    <!-- ══════════════════════════════════════════════════════════
         一、顶部标题 & 用户求职信息栏
         ══════════════════════════════════════════════════════════ -->
    <section class="zone-header">
      <div class="user-info-bar">
        <div class="uib-top">
          <div class="uib-title">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563EB" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
            <span>求职意向</span>
          </div>
          <div class="uib-hint">点值直接编辑，Enter保存</div>
        </div>
        <div class="uib-fields">
          <div class="uib-field" :class="{ editing: editingField === 'city' }">
            <MapPin :size="14" class="icon-blue" />
            <span class="uib-fname">意向城市</span>
            <template v-if="editingField === 'city'">
              <input v-model="editForm.city" class="uib-input"
                @blur="saveField('city')" @keydown.enter="saveField('city')"
                placeholder="如：北京、上海" />
            </template>
            <span v-else class="uib-fval" @click="startEdit('city')">{{ userProfile.city || '未设置' }}</span>
          </div>
          <div class="uib-field" :class="{ editing: editingField === 'job_targets' }">
            <Crosshair :size="14" class="icon-blue" />
            <span class="uib-fname">目标岗位</span>
            <template v-if="editingField === 'job_targets'">
              <input v-model="editForm.job_targets" class="uib-input"
                @blur="saveField('job_targets')" @keydown.enter="saveField('job_targets')"
                placeholder="如：前端开发、产品经理" />
            </template>
            <span v-else class="uib-fval" @click="startEdit('job_targets')">{{ userProfile.job_targets || '未设置' }}</span>
          </div>
          <div class="uib-field" :class="{ editing: editingField === 'salary' }">
            <Coins :size="14" class="icon-blue" />
            <span class="uib-fname">期望薪资</span>
            <template v-if="editingField === 'salary'">
              <input v-model="editForm.salary" class="uib-input"
                @blur="saveField('salary')" @keydown.enter="saveField('salary')"
                placeholder="如：8k-12k、面议" />
            </template>
            <span v-else class="uib-fval" @click="startEdit('salary')">{{ userProfile.salary || '未设置' }}</span>
          </div>
          <div class="uib-field" :class="{ editing: editingField === 'skills' }">
            <Tags :size="14" class="icon-blue" />
            <span class="uib-fname">技能标签</span>
            <template v-if="editingField === 'skills'">
              <input v-model="editForm.skills" class="uib-input"
                @blur="saveField('skills')" @keydown.enter="saveField('skills')"
                placeholder="如：Vue、Python、PS" />
            </template>
            <span v-else class="uib-fval" @click="startEdit('skills')">{{ userProfile.skills || '未设置' }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════════════════
         二、Tab 切换：推荐岗位 / 我的投递
         ══════════════════════════════════════════════════════════ -->
    <div class="tab-bar">
      <div
        class="tab-item"
        :class="{ active: activeTab === 'recommend' }"
        @click="switchTab('recommend')"
      >
        <Star :size="16" class="icon-blue" /> 推荐岗位
      </div>
      <div
        class="tab-item"
        :class="{ active: activeTab === 'myapps' }"
        @click="switchTab('myapps')"
      >
        <ClipboardCheck :size="16" class="icon-blue" /> 我的投递
        <span v-if="myAppsCount > 0" class="tab-badge">{{ myAppsCount }}</span>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════
         三、推荐岗位 Tab
         ══════════════════════════════════════════════════════════ -->
    <template v-if="activeTab === 'recommend'">
      <section class="agent-search-card">
        <div class="agent-copy">
          <span class="agent-kicker">QITU AGENT</span>
          <h2>让 Agent 按真实目标搜岗位</h2>
          <p>输入目标岗位、城市和个人背景；搜不到精确岗位时自动放宽条件，并给真实招聘搜索入口，不硬塞假岗位。</p>
        </div>
        <div class="agent-form">
          <el-input v-model="agentForm.target" placeholder="目标岗位，如 产品实习 / 新媒体运营 / 银行柜员" clearable />
          <el-input v-model="agentForm.city" placeholder="城市，如 北京 / 上海 / 郑州，可留空" clearable />
          <el-input v-model="agentForm.major" placeholder="专业/学历，如 计算机大一 / 市场营销本科" clearable />
          <el-input v-model="agentForm.skills" placeholder="技能/经历，如 Python、剪辑、社团运营" clearable />
          <el-button type="primary" :loading="agentSearching" @click="runAgentSearch">
            <Search :size="16" class="icon-blue" /> Agent 搜岗位
          </el-button>
        </div>
        <div v-if="agentResult" class="agent-result">
          <div class="agent-result-head">
            <b>{{ agentResult.summary }}</b>
            <el-button v-if="agentResult.external_search_url" size="small" plain @click="openWebsite(agentResult.external_search_url)">打开真实搜索入口</el-button>
          </div>
          <p v-for="step in agentResult.relaxed_steps" :key="step" class="agent-step">{{ step }}</p>
          <p v-if="!agentResult.jobs?.length" class="agent-empty">没有找到精确匹配。建议点开真实搜索入口，或复制 JD 后再做差距分析。</p>
        </div>
      </section>

      <!-- 筛选栏 & 批量操作栏 -->
    <section class="zone-filter">
      <div class="filter-bar">
        <div class="filter-group">
          <span class="filter-label"><Building2 :size="16" class="icon-blue" /> 公司规模</span>
          <el-select v-model="filters.company_size" placeholder="不限" clearable style="width:105px" @change="loadJobs">
            <el-option label="小型" value="小型" />
            <el-option label="中型" value="中型" />
            <el-option label="大型" value="大型" />
            <el-option label="巨头" value="巨头" />
          </el-select>
        </div>
        <div class="filter-group">
          <span class="filter-label"><Briefcase :size="16" class="icon-blue" /> 岗位类型</span>
          <el-select v-model="filters.job_type" placeholder="不限" clearable style="width:105px" @change="loadJobs">
            <el-option label="技术" value="技术" />
            <el-option label="产品" value="产品" />
            <el-option label="运营" value="运营" />
            <el-option label="设计" value="设计" />
            <el-option label="市场" value="市场" />
            <el-option label="职能" value="职能" />
          </el-select>
        </div>
        <div class="filter-group">
          <span class="filter-label"><Building2 :size="16" class="icon-blue" /> 城市</span>
          <el-select v-model="filters.city" placeholder="不限" clearable style="width:115px" @change="loadJobs">
            <el-option v-for="c in filterOptions.cities" :key="c" :label="c" :value="c" />
          </el-select>
        </div>
        <div class="filter-group">
          <span class="filter-label"><Coins :size="16" class="icon-blue" /> 薪资</span>
          <el-select v-model="filters.salary_range" placeholder="不限" clearable style="width:115px" @change="loadJobs">
            <el-option label="8K以下" value="0-8000" />
            <el-option label="8K-15K" value="8000-15000" />
            <el-option label="15K-25K" value="15000-25000" />
            <el-option label="25K-40K" value="25000-40000" />
            <el-option label="40K以上" value="40000-999999" />
          </el-select>
        </div>
        <div class="filter-group">
          <span class="filter-label"><Clock :size="16" class="icon-blue" /> 发布时间</span>
          <el-select v-model="filters.publish_time" placeholder="不限" clearable style="width:115px" @change="loadJobs">
            <el-option label="今天" value="today" />
            <el-option label="近3天" value="3days" />
            <el-option label="近一周" value="week" />
            <el-option label="近一个月" value="month" />
          </el-select>
        </div>
      </div>

      <div class="bulk-actions">
        <el-button size="small" @click="selectAll" :type="allSelected ? 'warning' : 'default'">
          <CheckCheck :size="16" class="icon-blue" />
          全选 {{ selectedCount ? `(${selectedCount})` : '' }}
        </el-button>
        <el-button size="small" @click="invertSelect">
          <ArrowLeftRight :size="16" class="icon-blue" /> 反选
        </el-button>
        <el-button size="small" @click="clearSelect">
          <Eraser :size="16" class="icon-blue" /> 清空
        </el-button>
        <el-button type="primary" size="small" @click="batchApply" :disabled="!selectedCount">
          <Rocket :size="16" class="icon-blue" /> 批量投递
        </el-button>
        <el-button type="success" size="small" @click="batchAddToList" :disabled="!selectedCount">
          <PlusCircle :size="16" class="icon-blue" /> 加入投递清单
        </el-button>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════════════════
         三、主体岗位列表区
         ══════════════════════════════════════════════════════════ -->
    <section class="zone-jobs">
      <div v-if="loading" class="loading-state">
        <Loader :size="28" class="icon-blue" style="margin-bottom:12px" />
        <p>正在加载岗位数据...</p>
      </div>

      <div v-else-if="!jobs.length" class="empty-state">
        <Search :size="16" class="icon-blue" />
        <p>暂无匹配岗位，试试调整筛选条件</p>
        <p class="empty-hint">切换筛选条件或扩大搜索范围</p>
      </div>

      <div v-else class="job-grid">
        <div
          v-for="job in jobs"
          :key="job.id"
          class="job-card card"
          :class="{ 'card-selected': selectedIds.has(job.id) }"
          @click="toggleSelect(job.id)"
        >
          <div class="card-checkbox" @click.stop="toggleSelect(job.id)">
            <el-checkbox :model-value="selectedIds.has(job.id)" />
          </div>
          <div class="card-body">
            <div class="card-header">
              <div class="card-company">
                <img
                  :src="job.company_logo || 'https://img.icons8.com/color/48/company.png'"
                  class="company-logo"
                  alt=""
                >
                <div>
                  <div class="company-name">{{ job.company_name }}</div>
                  <span class="company-size-tag"><Layers :size="16" class="icon-blue" /> {{ job.company_size }}</span>
                </div>
              </div>
              <div class="job-title">{{ job.job_title }}</div>
            </div>

            <div class="card-meta">
              <span class="meta-item">
                <MapPin :size="16" class="icon-blue" />
                {{ job.city }}{{ job.address ? '·' + job.address.replace(job.city, '') : '' }}
              </span>
              <span class="meta-item">
                <Coins :size="16" class="icon-blue" /> {{ job.salary_text }}
              </span>
              <span class="meta-item">
                <CalendarDays :size="16" class="icon-blue" /> {{ job.publish_time }}
              </span>
            </div>

            <div class="card-footer">
              <el-button size="small" type="primary" plain @click.stop="showDetail(job)">
                <Info :size="16" class="icon-blue" /> 查看详情
              </el-button>
              <el-button size="small" plain @click.stop="openWebsite(job.company_website)">
                <Building2 :size="16" class="icon-blue" /> 公司官网
              </el-button>
              <el-button size="small" type="primary" @click.stop="openApplyAndTrack(job)">
                <Rocket :size="16" class="icon-blue" /> 打开投递入口
              </el-button>
              <el-button
                size="small"
                :type="inTracking(job.id) ? 'success' : 'default'"
                @click.stop="addToTracking(job)"
              >
                <CheckCircle :size="16" class="icon-blue" :class="inTracking(job.id) ? 'fas fa-check-circle' : 'fas fa-plus-circle'" />
                {{ inTracking(job.id) ? '已加入' : '加入清单' }}
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="totalPages > 1" class="pagination-wrap">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="totalJobs"
          layout="prev, pager, next"
          @current-change="loadJobs"
        />
      </div>
    </section>

    <!-- ══════════════════════════════════════════════════════════
         四、弹窗模块 — 岗位详情
         ══════════════════════════════════════════════════════════ -->
    <el-dialog
      v-model="detailVisible"
      :title="detailJob?.company_name + ' - ' + detailJob?.job_title"
      width="720px"
      class="detail-dialog"
      destroy-on-close
    >
      <div v-if="detailLoading" class="loading-state">
        <Loader :size="24" class="icon-blue" style="margin-bottom:10px" />
        <p>AI正在解析岗位信息...</p>
      </div>

      <div v-else-if="analysisResult" class="detail-content">
        <!-- 板块1：企业基础信息 -->
        <div class="detail-block card">
          <div class="detail-block-header">
            <Building2 :size="16" class="icon-blue" />
            企业基础信息
          </div>
          <div class="detail-block-body">
            <p class="detail-company-title">
              <strong>{{ detailJob.company_name }}</strong>
              <span class="detail-industry-tag">{{ detailJob.industry }}</span>
            </p>
            <p class="company-intro">{{ analysisResult.company_summary || detailJob.company_intro }}</p>
            <div class="info-grid">
              <div class="info-grid-item">
                <label><Tag :size="16" class="icon-blue" /> 岗位全称</label>
                <span>{{ analysisResult.job_full_title }}</span>
              </div>
              <div class="info-grid-item">
                <label><MapPin :size="16" class="icon-blue" /> 工作地点</label>
                <span>{{ analysisResult.location_detail }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 板块2：岗位核心解读 -->
        <div class="detail-block card">
          <div class="detail-block-header">
            <Crosshair :size="16" class="icon-blue" />
            岗位核心解读
          </div>
          <div class="detail-block-body">
            <div class="skill-section">
              <div class="skill-group">
                <label><Wrench :size="16" class="icon-blue" /> 硬性技能要求</label>
                <div class="skill-tags">
                  <el-tag
                    v-for="s in analysisResult.hard_skills" :key="s" size="small"
                    :type="analysisResult.matched_skills?.includes(s) ? 'success' : 'danger'"
                  >
                    {{ s }}
                    <CheckCircle :size="16" v-if="analysisResult.matched_skills?.includes(s)" class="icon-blue" style="margin-left:3px" />
                    <XCircle :size="16" class="icon-blue" style="margin-left:3px" />
                  </el-tag>
                </div>
              </div>
              <div class="skill-group">
                <label><Hand :size="16" class="icon-blue" /> 软性要求</label>
                <div class="skill-tags">
                  <el-tag v-for="s in analysisResult.soft_skills" :key="s" size="small">{{ s }}</el-tag>
                </div>
              </div>
              <div class="skill-group">
                <label><Star :size="16" class="icon-blue" /> 加分技能</label>
                <div class="skill-tags">
                  <el-tag v-for="s in analysisResult.preferred_skills" :key="s" size="small" type="warning">{{ s }}</el-tag>
                </div>
              </div>
              <div v-if="analysisResult.matched_skills?.length" class="skill-group match-group">
                <label><CheckCircle :size="16" :color="'var(--primary)'" /> 已匹配技能</label>
                <div class="skill-tags">
                  <el-tag v-for="s in analysisResult.matched_skills" :key="s" size="small" type="success">{{ s }}</el-tag>
                </div>
              </div>
              <div v-if="analysisResult.missing_skills?.length" class="skill-group miss-group">
                <label>
                  <XCircle :size="16" :color="'var(--accent)'" /> 缺失技能
                  <span class="miss-hint">（点击可前往笔试练习）</span>
                </label>
                <div class="skill-tags">
                  <el-tag
                    v-for="s in analysisResult.missing_skills" :key="s" size="small" type="danger"
                    style="cursor:pointer" @click="goExam(s)"
                  >
                    {{ s }} <Pen :size="16" class="icon-blue" />
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ══ 板块：差距分析（你 vs 岗位）══ -->
        <div class="detail-block card gap-block">
          <div class="detail-block-header">
            <Target :size="16" class="icon-blue" />
            差距分析 · 你 vs 岗位要求
          </div>
          <div class="detail-block-body">
            <!-- 加载中 -->
            <div v-if="!gapResult" class="gap-loading">
              <Loader :size="16" class="icon-blue" style="animation:spin 1s linear infinite" />
              <span>正在分析你的技能与岗位差距...</span>
            </div>

            <template v-else>
              <!-- 匹配度进度条 -->
              <div class="gap-score-row">
                <div class="gap-score-circle">
                  <el-progress
                    type="circle"
                    :percentage="gapResult.match_score || 0"
                    :width="80"
                    :stroke-width="6"
                    :color="gapResult.match_score >= 70 ? '#67C23A' : gapResult.match_score >= 40 ? '#E6A23C' : '#F56C6C'"
                  />
                </div>
                <div class="gap-score-info">
                  <div class="gap-readiness-badge" :class="'badge-' + (gapResult.readiness_level || 'need_work')">
                    {{ gapResult.readiness_level === 'ready' ? '准备充分' : gapResult.readiness_level === 'nearly_ready' ? '基本达标' : '需要补强' }}
                  </div>
                  <p class="gap-summary">{{ gapResult.summary }}</p>
                </div>
              </div>

              <!-- 优势领域 -->
              <div v-if="gapResult.strength_areas?.length" class="skill-group">
                <label><CheckCircle :size="16" style="color:#67C23A" /> 你的优势领域</label>
                <div class="skill-tags">
                  <el-tag v-for="s in gapResult.strength_areas" :key="s" size="small" type="success">{{ s }}</el-tag>
                </div>
              </div>

              <!-- 待补足领域 -->
              <div v-if="gapResult.missing_skills?.length" class="skill-group">
                <label><XCircle :size="16" style="color:#F56C6C" /> 待补足技能</label>
                <div class="skill-tags">
                  <el-tag
                    v-for="s in gapResult.missing_skills" :key="s" size="small" type="danger"
                    style="cursor:pointer" @click="goExam(s)"
                  >
                    {{ s }} <Pen :size="16" class="icon-blue" />
                  </el-tag>
                </div>
              </div>

              <!-- 优先建议 -->
              <div v-if="gapResult.priority_recommendations?.length" class="skill-group">
                <label><ArrowUpNarrowWide :size="16" style="color:#E6A23C" /> 优先提升建议</label>
                <ul class="gap-recommend-list">
                  <li v-for="(r, i) in gapResult.priority_recommendations" :key="i">
                    <Circle :size="6" style="color:#E6A23C;margin-right:6px" />
                    {{ r }}
                  </li>
                </ul>
              </div>

              <!-- 笔试反馈 -->
              <div v-if="gapResult.exam_feedback" class="gap-exam-feedback">
                <Lightbulb :size="16" style="color:#E6A23C" />
                {{ gapResult.exam_feedback }}
              </div>
            </template>
          </div>
        </div>

        <!-- 板块3：面试专项汇总 -->
        <div class="detail-block card">
          <div class="detail-block-header">
            <Mic :size="16" class="icon-blue" />
            面试专项汇总
          </div>
          <div class="detail-block-body">
            <div class="info-grid">
              <div class="info-grid-item">
                <label><ArrowUpNarrowWide :size="16" class="icon-blue" /> 面试轮次</label>
                <span>{{ analysisResult.interview_rounds }}</span>
              </div>
              <div class="info-grid-item">
                <label><Video :size="16" class="icon-blue" /> 面试形式</label>
                <span>{{ analysisResult.interview_form }}</span>
              </div>
            </div>
            <div class="skill-group" style="margin-top:12px">
              <label><Star :size="16" class="icon-blue" /> 历年面试重点</label>
              <ul class="focus-list">
                <li v-for="(f, i) in analysisResult.interview_focus" :key="i">
                  <Circle :size="6" :color="'var(--primary)'" style="margin-right:6px" />
                  {{ f }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- 板块4：投递须知 -->
        <div class="detail-block card">
          <div class="detail-block-header">
            <ClipboardList :size="16" class="icon-blue" />
            投递须知
          </div>
          <div class="detail-block-body">
            <p class="deadline-highlight">
              <Clock :size="16" class="icon-blue" /> 截止时间：<strong>{{ analysisResult.deadline }}</strong>
            </p>
            <p v-if="analysisResult.has_exam" class="exam-warning">
              <TriangleAlert :size="16" class="icon-blue" /> 该岗位含有笔试环节，建议提前准备
            </p>
            <div v-if="analysisResult.resume_tips?.length" class="resume-tips">
              <label><Lightbulb :size="16" class="icon-blue" /> 简历建议</label>
              <ul class="tips-list">
                <li v-for="(tip, i) in analysisResult.resume_tips" :key="i">
                  <Circle :size="5" :color="'var(--text-muted)'" style="margin-right:6px" />
                  {{ tip }}
                </li>
              </ul>
            </div>
            <p class="assessment-text">
              <Quote :size="16" class="icon-blue" style="margin-right:4px" />
              {{ analysisResult.overall_assessment }}
              <Quote :size="16" class="icon-blue" style="margin-left:4px" />
            </p>
          </div>
        </div>
      </div>

      <template #footer>
        <el-button @click="detailVisible = false">
          <X :size="16" class="icon-blue" /> 关闭
        </el-button>
        <el-button type="primary" @click="goApplyPage">
          <Rocket :size="16" class="icon-blue" /> 跳转官方招聘页
        </el-button>
        <el-button type="success" @click="goInterview">
          <Mic :size="16" class="icon-blue" /> 前往面试练习
        </el-button>
      </template>
    </el-dialog>

    <!-- ══════════════════════════════════════════════════════════
         三(完)、推荐岗位 Tab 结束
         ══════════════════════════════════════════════════════════ -->
    </template>

    <!-- ══════════════════════════════════════════════════════════
         四、我的投递 Tab
         ══════════════════════════════════════════════════════════ -->
    <template v-if="activeTab === 'myapps'">
      <!-- 数据概览条 -->
      <div class="stats-bar">
        <div class="stat-item">
          <div class="stat-value">{{ myStats.total }}</div>
          <div class="stat-label">总投递</div>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <div class="stat-value" style="color:#E6A23C">{{ myStats.pending }}</div>
          <div class="stat-label">待跟进</div>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <div class="stat-value" style="color:#409EFF">{{ myStats.interviewing }}</div>
          <div class="stat-label">面试中</div>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <div class="stat-value" style="color:#67C23A">{{ myStats.offer }}</div>
          <div class="stat-label">已拿 Offer</div>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <div class="stat-value" style="color:#909399">{{ myStats.rejected }}</div>
          <div class="stat-label">已关闭</div>
        </div>
      </div>

      <!-- 筛选栏 -->
      <div class="filter-bar myapps-filter">
        <div class="filter-group">
          <span class="filter-label"><Tag :size="16" class="icon-blue" /> 进度状态</span>
          <el-select v-model="myFilters.status" placeholder="全部状态" clearable style="width:130px" @change="loadMyApps">
            <el-option v-for="s in myFilterOpts.statuses" :key="s" :label="s" :value="s" />
          </el-select>
        </div>
        <div class="filter-group">
          <span class="filter-label"><Layers :size="16" class="icon-blue" /> 公司类型</span>
          <el-select v-model="myFilters.company_size" placeholder="不限" clearable style="width:110px" @change="loadMyApps">
            <el-option v-for="s in myFilterOpts.company_sizes" :key="s" :label="s" :value="s" />
          </el-select>
        </div>
        <div class="filter-group">
          <span class="filter-label"><Clock :size="16" class="icon-blue" /> 投递时间</span>
          <el-select v-model="myFilters.date_range" placeholder="不限" clearable style="width:120px" @change="loadMyApps">
            <el-option label="近7天" value="7d" />
            <el-option label="近30天" value="30d" />
            <el-option label="近90天" value="90d" />
            <el-option label="全部" value="all" />
          </el-select>
        </div>
      </div>

      <!-- 加载状态 -->
      <div v-if="myAppsLoading" class="loading-state" style="padding:50px 0">
        <Loader :size="28" class="icon-blue" />
        <p style="margin-top:10px">加载投递记录...</p>
      </div>

      <!-- 空状态 -->
      <div v-else-if="!myAppsRecords.length" class="empty-state" style="padding:60px 0">
        <Inbox :size="48" class="icon-blue" />
        <p>暂无投递记录</p>
        <p class="empty-hint">在「推荐岗位」中点击「加入投递清单」或「查看详情」即可记录在这里</p>
      </div>

      <!-- 我的投递卡片列表 -->
      <div v-else class="myapps-grid">
        <div
          v-for="rec in myAppsRecords"
          :key="rec.id"
          class="myapps-card card"
          @click="openMyAppDetail(rec)"
        >
          <div class="myapps-card-left">
            <img
              :src="rec.company_logo || 'https://img.icons8.com/color/48/company.png'"
              class="myapps-logo"
              alt=""
            >
          </div>
          <div class="myapps-card-body">
            <div class="myapps-card-top">
              <div>
                <div class="myapps-company">{{ rec.company_name }}</div>
                <div class="myapps-jobtitle">{{ rec.job_title }}</div>
              </div>
              <span
                class="status-tag"
                :class="'status-' + statusClass(rec.status)"
              >
                {{ rec.status }}
              </span>
            </div>
            <div class="myapps-card-meta">
              <span v-if="rec.company_size" class="myapps-meta-item">
                <Building2 :size="16" class="icon-blue" /> {{ rec.company_size }}
              </span>
              <span v-if="rec.industry" class="myapps-meta-item">
                <Tag :size="16" class="icon-blue" /> {{ rec.industry }}
              </span>
              <span class="myapps-meta-item">
                <CalendarDays :size="16" class="icon-blue" /> {{ rec.apply_time }}
              </span>
              <span v-if="rec.interview_time" class="myapps-meta-item">
                <Clock :size="16" class="icon-blue" /> {{ rec.interview_time }}
              </span>
            </div>
            <div v-if="rec.notes" class="myapps-notes">
              <Pencil :size="16" class="icon-blue" /> {{ rec.notes }}
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="myAppsTotalPages > 1" class="pagination-wrap">
        <el-pagination
          v-model:current-page="myAppsPage"
          :page-size="myAppsPageSize"
          :total="myAppsTotal"
          layout="prev, pager, next"
          @current-change="loadMyApps"
        />
      </div>
    </template>

    <!-- ══════════════════════════════════════════════════════════
         五、我的投递详情弹窗（含面试安排）
         ══════════════════════════════════════════════════════════ -->
    <el-dialog
      v-model="myAppDetailVisible"
      :title="myAppDetail?.company_name + ' - ' + myAppDetail?.job_title"
      width="620px"
      class="interview-dialog"
      destroy-on-close
    >
      <div v-if="myAppDetail" class="myapp-detail-body">
        <!-- 状态标签 -->
        <div class="myapp-detail-status">
          <span
            class="status-tag-lg"
            :class="'status-' + statusClass(myAppDetail.status)"
          >
            {{ myAppDetail.status }}
          </span>
        </div>

        <!-- 基础信息 -->
        <div class="detail-block card">
          <div class="detail-block-header">
            <Building2 :size="16" class="icon-blue" /> 基本信息
          </div>
          <div class="detail-block-body">
            <div class="info-grid">
              <div class="info-grid-item">
                <label>公司名称</label>
                <span>{{ myAppDetail.company_name }}</span>
              </div>
              <div class="info-grid-item">
                <label>岗位名称</label>
                <span>{{ myAppDetail.job_title }}</span>
              </div>
              <div class="info-grid-item">
                <label>公司规模</label>
                <span>{{ myAppDetail.company_size || '-' }}</span>
              </div>
              <div class="info-grid-item">
                <label>所属行业</label>
                <span>{{ myAppDetail.industry || '-' }}</span>
              </div>
              <div class="info-grid-item">
                <label>投递时间</label>
                <span>{{ myAppDetail.apply_time }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 面试安排（仅 待面试/面试通过 时显示） -->
        <div v-if="['待面试', '面试通过'].includes(myAppDetail.status)" class="detail-block card">
          <div class="detail-block-header">
            <CalendarCheck :size="16" class="icon-blue" /> 面试安排
          </div>
          <div class="detail-block-body">
            <div class="info-grid">
              <div class="info-grid-item">
                <label><Clock :size="16" class="icon-blue" /> 面试时间</label>
                <el-input
                  v-model="interviewForm.time"
                  placeholder="如：2026-06-15 14:00"
                  size="small"
                />
              </div>
              <div class="info-grid-item">
                <label><MapPin :size="16" class="icon-blue" /> 面试地点</label>
                <el-input
                  v-model="interviewForm.location"
                  placeholder="线上面试/具体地址"
                  size="small"
                />
              </div>
            </div>
            <div style="margin-top:10px">
              <label style="font-size:12px;color:var(--text-muted);font-weight:500">
                <MessageSquare :size="16" class="icon-blue" /> HR反馈备注
              </label>
              <el-input
                v-model="interviewForm.feedback"
                type="textarea"
                :rows="2"
                placeholder="HR的反馈意见或备注..."
                size="small"
                style="margin-top:4px"
              />
            </div>
            <el-button
              type="primary"
              size="small"
              style="margin-top:12px"
              @click="saveInterview"
            >
              <Save :size="16" class="icon-blue" /> 保存面试安排
            </el-button>
            <span v-if="interviewSaved" class="save-tip">
              <CheckCircle :size="16" :color="'#67C23A'" /> 已保存
            </span>
          </div>
        </div>

        <!-- HR反馈 -->
        <div v-if="myAppDetail.hr_feedback" class="detail-block card">
          <div class="detail-block-header">
            <MessageSquare :size="16" class="icon-blue" /> HR反馈
          </div>
          <div class="detail-block-body">
            <p style="color:var(--text-body);font-size:13px;line-height:1.6">{{ myAppDetail.hr_feedback }}</p>
          </div>
        </div>
      </div>

      <template #footer>
        <el-button @click="myAppDetailVisible = false">
          <X :size="16" class="icon-blue" /> 关闭
        </el-button>
        <el-button type="primary" @click="changeMyAppStatus(myAppDetail)">
          <Pen :size="16" class="icon-blue" /> 更新进度状态
        </el-button>
      </template>
    </el-dialog>

    <!-- ══════════════════════════════════════════════════════════
         六、更新进度状态弹窗
         ══════════════════════════════════════════════════════════ -->
    <el-dialog
      v-model="statusChangeVisible"
      title="更新投递进度"
      width="500px"
      destroy-on-close
    >
      <div style="padding:10px 0">
        <p style="font-size:13px;color:var(--text-muted);margin-bottom:14px">
          当前状态：<strong>{{ myAppDetail?.status }}</strong>
        </p>
        <div class="status-options">
          <div
            v-for="s in statusOptions"
            :key="s.value"
            class="status-option"
            :class="{ selected: selectedNewStatus === s.value }"
            @click="selectedNewStatus = s.value"
          >
            <span class="status-dot" :class="'status-' + s.cls"></span>
            <span>{{ s.label }}</span>
          </div>
        </div>
        <div style="margin-top:14px">
          <label style="font-size:12px;color:var(--text-muted);font-weight:500">备注（可选）</label>
          <el-input
            v-model="statusChangeNote"
            type="textarea"
            :rows="2"
            placeholder="填写备注信息..."
            size="small"
            style="margin-top:4px"
          />
        </div>
      </div>
      <template #footer>
        <el-button @click="statusChangeVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmStatusChange" :disabled="!selectedNewStatus">
          <Check :size="16" class="icon-blue" /> 确认更新
        </el-button>
      </template>
    </el-dialog>

    <!-- ══════════════════════════════════════════════════════════
         原区域五：投递台账（已有记录的兜底展示，被我的投递替代，保留不显示）
         ══════════════════════════════════════════════════════════ -->
    <section class="zone-tracking">
      <div class="section-header" style="margin-bottom:16px">
        <div class="section-title">
          <ClipboardCheck :size="16" class="icon-blue" />
          我的投递记录
          <span class="tracking-badge" v-if="trackingRecords.length">{{ trackingRecords.length }}</span>
        </div>
      </div>

      <div v-if="trackingLoading" class="loading-state" style="padding:30px 0">
        <Loader :size="16" class="icon-blue" />
      </div>

      <div v-else-if="!trackingRecords.length" class="empty-state" style="padding:30px 0">
        <Inbox :size="36" class="icon-blue" />
        <p>暂无投递记录，加入岗位到清单后会自动显示在这里</p>
      </div>

      <el-table v-else :data="trackingRecords" style="width:100%" stripe size="small" class="tracking-table">
        <el-table-column prop="company_name" label="公司" min-width="120" />
        <el-table-column prop="job_title" label="岗位" min-width="160" />
        <el-table-column prop="apply_time" label="投递时间" min-width="140" />
        <el-table-column label="当前状态" min-width="130">
          <template #default="{ row }">
            <el-select v-model="row.status" size="small" style="width:120px" @change="updateStatus(row)">
              <el-option label="待投递" value="待投递" />
              <el-option label="已投递" value="已投递" />
              <el-option label="HR已查看" value="HR已查看" />
              <el-option label="邀约面试" value="邀约面试" />
              <el-option label="面试结束" value="面试结束" />
              <el-option label="已拒绝" value="已拒绝" />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="操作" min-width="210">
          <template #default="{ row }">
            <el-button size="small" text @click="openDetailById(row.job_id)">
              <Info :size="16" class="icon-blue" /> 查看岗位
            </el-button>
            <el-button size="small" text type="primary" @click="goInterview">
              <Mic :size="16" class="icon-blue" /> 查看面经
            </el-button>
            <el-button size="small" text type="danger" @click="deleteTracking(row)">
              <Trash2 :size="16" class="icon-blue" /> 删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
</section>
    </div>
    <!-- ═══ 品牌 Footer ═══ -->
    <div class="brand-footer">
      <div>启途 · <span class="qitu-up">QITU</span></div>
      <div class="qitu-sl">向上生长，自有答案</div>
    </div>
</template>

<script setup>
import { ref, computed, reactive, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import PageBanner from '../components/PageBanner.vue'

const router = useRouter()

// ── 数据 ──
const userProfile = ref({})
const jobs = ref([])
const loading = ref(false)
const totalJobs = ref(0)
const currentPage = ref(1)
const pageSize = 20
const totalPages = computed(() => Math.ceil(totalJobs.value / pageSize))

// ── 求职信息行内编辑 ──
const editingField = ref('')
const editForm = reactive({ city: '', job_targets: '', salary: '', skills: '' })

function startEdit(field) {
  editForm[field] = userProfile.value[field] || ''
  editingField.value = field
  // auto-focus needs nextTick
  nextTick(() => {
    const el = document.querySelector('.uib-field.editing input')
    if (el) el.focus()
  })
}

async function saveField(field) {
  const val = editForm[field].trim()
  editingField.value = ''
  const token = getToken()
  if (!token) return
  const params = new URLSearchParams({ token, [field]: val })
  try {
    const resp = await fetch(`/api/user/profile?${params}`, { method: 'POST' })
    if (resp.ok) {
      userProfile.value[field] = val
      if (field === 'city') agentForm.value.city = val
      if (field === 'job_targets') agentForm.value.target = val
      if (field === 'skills') agentForm.value.skills = val
      ElMessage.success('已保存，正在刷新推荐岗位...')
      // 保存后自动按新画像刷新推荐岗位
      currentPage.value = 1
      await loadJobs()
    }
  } catch { /* ignore */ }
}

const filterOptions = ref({ cities: [], job_types: [], company_sizes: [] })
const filters = ref({
  company_size: '',
  job_type: '',
  city: '',
  salary_range: '',
  publish_time: '',
  keyword: '',
})

const agentForm = ref({
  target: '',
  city: '',
  major: '',
  skills: '',
  education: '',
})
const agentSearching = ref(false)
const agentResult = ref(null)

// 选中状态
const selectedIds = ref(new Set())
const selectedCount = computed(() => selectedIds.value.size)
const allSelected = computed(() => selectedCount.value > 0 && selectedCount.value === jobs.value.length)

// 详情弹窗
const detailVisible = ref(false)
const detailJob = ref(null)
const detailLoading = ref(false)
const analysisResult = ref(null)
const gapResult = ref(null)

// ── 投递台账
const trackingRecords = ref([])
const trackingLoading = ref(false)

// ── Tab 切换
const activeTab = ref('recommend')

// ── 我的投递
const myAppsRecords = ref([])
const myAppsLoading = ref(false)
const myAppsTotal = ref(0)
const myAppsPage = ref(1)
const myAppsPageSize = 15
const myAppsTotalPages = computed(() => Math.ceil(myAppsTotal.value / myAppsPageSize))
const myAppsCount = computed(() => myAppsTotal.value)

const myStats = ref({ total: 0, pending: 0, interviewing: 0, offer: 0, rejected: 0 })
const myFilters = ref({ status: '', company_size: '', date_range: '' })
const myFilterOpts = ref({ statuses: [], company_sizes: [], industries: [] })

// 我的投递详情弹窗
const myAppDetailVisible = ref(false)
const myAppDetail = ref(null)
const interviewForm = ref({ time: '', location: '', feedback: '' })
const interviewSaved = ref(false)

// 状态变更弹窗
const statusChangeVisible = ref(false)
const selectedNewStatus = ref('')
const statusChangeNote = ref('')

const statusOptions = [
  { value: '待投递', label: '待投递（已打开入口）', cls: 'pending' },
  { value: '已投递', label: '已投递（已提交简历）', cls: 'applied' },
  { value: 'HR已查看', label: 'HR已查看', cls: 'viewed' },
  { value: '已查看', label: '已查看（浏览过岗位）', cls: 'viewed' },
  { value: '待面试', label: '待面试（已获面试邀请）', cls: 'interview' },
  { value: '面试通过', label: '面试通过', cls: 'passed' },
  { value: '已offer', label: '已拿到 Offer', cls: 'offer' },
  { value: '已拒', label: '已被拒绝', cls: 'rejected' },
  { value: '已关闭', label: '已关闭（放弃跟进）', cls: 'closed' },
]

function statusClass(status) {
  const map = {
    '待投递': 'pending',
    '已投递': 'applied',
    'HR已查看': 'viewed',
    '已查看': 'viewed',
    '待面试': 'interview',
    '面试通过': 'passed',
    '已offer': 'offer',
    '已拒': 'rejected',
    '已关闭': 'closed',
  }
  return map[status] || 'viewed'
}

// ── 工具函数 ──
function getToken() {
  return localStorage.getItem('token') || ''
}

async function apiGet(url) {
  try {
    const resp = await fetch(url)
    if (!resp.ok) return null
    return await resp.json()
  } catch {
    return null
  }
}

async function apiPost(url, body = null) {
  try {
    const options = { method: 'POST' }
    if (body) {
      options.headers = { 'Content-Type': 'application/json' }
      options.body = JSON.stringify(body)
    }
    const resp = await fetch(url, options)
    if (!resp.ok) return null
    return await resp.json()
  } catch {
    return null
  }
}

// ── 初始化 ──
onMounted(async () => {
  // 读取 URL 搜索参数
  const urlParams = new URLSearchParams(window.location.search)
  const searchFromUrl = urlParams.get('search')
  if (searchFromUrl) {
    filters.value.keyword = searchFromUrl
  }

  await Promise.all([
    loadUserProfile(),
    loadFilterOptions(),
    loadJobs(),
    loadTracking(),
  ])
})

async function loadUserProfile() {
  const token = getToken()
  if (!token) return
  const data = await apiGet(`/api/user/profile?token=${token}`)
  if (data) {
    userProfile.value = data.profile || {}
    agentForm.value.target = userProfile.value.job_targets || ''
    agentForm.value.city = userProfile.value.city || ''
    agentForm.value.skills = userProfile.value.skills || ''
    agentForm.value.major = userProfile.value.major || ''
    agentForm.value.education = userProfile.value.education || ''
  }
}

async function loadFilterOptions() {
  const data = await apiGet('/api/delivery/filter-options')
  if (data) {
    filterOptions.value = data
  }
}

async function loadJobs() {
  loading.value = true
  const params = new URLSearchParams()
  params.set('page', currentPage.value)
  params.set('page_size', pageSize)
  // 传token让后端按用户画像自动推荐
  const tok = getToken()
  if (tok) params.set('token', tok)
  // 用户手动筛选参数（覆盖画像推荐）
  if (filters.value.company_size) params.set('company_size', filters.value.company_size)
  if (filters.value.job_type) params.set('job_type', filters.value.job_type)
  if (filters.value.city) params.set('city', filters.value.city)
  if (filters.value.salary_range) {
    const [min, max] = filters.value.salary_range.split('-')
    params.set('salary_min', min)
    params.set('salary_max', max)
  }
  if (filters.value.keyword) params.set('keyword', filters.value.keyword)
  const data = await apiGet(`/api/delivery/jobs?${params}`)
  if (data) {
    jobs.value = data.jobs || []
    totalJobs.value = data.total || 0
  } else {
    jobs.value = []
    totalJobs.value = 0
  }
  loading.value = false
  selectedIds.value = new Set()
}

// ── 批量操作 ──
async function runAgentSearch() {
  if (!agentForm.value.target && !agentForm.value.skills && !agentForm.value.major) {
    ElMessage.warning('先输入目标岗位或个人背景')
    return
  }
  agentSearching.value = true
  const data = await apiPost('/api/delivery/agent-search', agentForm.value)
  agentSearching.value = false
  if (!data) {
    ElMessage.error('Agent 搜索失败，请稍后再试')
    return
  }
  agentResult.value = data
  if (data.jobs?.length) {
    jobs.value = data.jobs
    totalJobs.value = data.jobs.length
    selectedIds.value = new Set()
    ElMessage.success(`Agent 找到 ${data.jobs.length} 个可分析岗位`)
  } else {
    jobs.value = []
    totalJobs.value = 0
    ElMessage.info('没有精确岗位，已给出真实搜索入口')
  }
}

// ── 批量操作 ──
function selectAll() {
  if (allSelected.value) {
    selectedIds.value = new Set()
  } else {
    selectedIds.value = new Set(jobs.value.map(j => j.id))
  }
}

function invertSelect() {
  const current = new Set(selectedIds.value)
  const all = new Set(jobs.value.map(j => j.id))
  selectedIds.value = new Set([...all].filter(x => !current.has(x)))
}

function clearSelect() {
  selectedIds.value = new Set()
}

function toggleSelect(id) {
  const s = new Set(selectedIds.value)
  if (s.has(id)) s.delete(id)
  else s.add(id)
  selectedIds.value = s
}

async function batchApply() {
  const selected = jobs.value.filter(j => selectedIds.value.has(j.id))
  for (const job of selected) {
    await openApplyAndTrack(job, false)
  }
  ElMessage.success(`已打开 ${selected.length} 个真实投递入口，并记录进度`)
}

async function openApplyAndTrack(job, showMessage = true) {
  const url = job.apply_url || job.company_website
  if (url && url.startsWith('http')) {
    window.open(url, '_blank')
    await addToTracking(job, '待投递', false)
    if (showMessage) ElMessage.success('已打开真实投递入口，并记录到投递清单')
  } else {
    ElMessage.info('暂未找到可打开的投递入口')
  }
}

async function batchAddToList() {
  const token = getToken()
  if (!token) {
    ElMessage.warning('请先登录')
    return
  }
  const selected = jobs.value.filter(j => selectedIds.value.has(j.id))
  let count = 0
  for (const job of selected) {
    const result = await apiPost(
      `/api/delivery/tracking?token=${token}&job_id=${job.id}&company_name=${encodeURIComponent(job.company_name)}&job_title=${encodeURIComponent(job.job_title)}&company_logo=${encodeURIComponent(job.company_logo || '')}&company_size=${encodeURIComponent(job.company_size || '')}&industry=${encodeURIComponent(job.industry || '')}&status=已查看`
    )
    if (result) count++
  }
  ElMessage.success(`已将 ${count} 个岗位加入投递清单`)
  await loadTracking()
}

// ── 详情弹窗 ──
async function showDetail(job) {
  detailJob.value = job
  detailVisible.value = true
  detailLoading.value = true
  analysisResult.value = null
  gapResult.value = null

  // 并行获取详情、AI分析、差距分析
  const token = getToken()
  const skills = userProfile.value?.skills || ''

  const [detailData, analysis, gap] = await Promise.all([
    apiGet(`/api/delivery/jobs/${job.id}`),
    apiPost(`/api/delivery/ai-analyze/${job.id}?user_skills=${encodeURIComponent(skills)}`),
    apiGet(`/api/delivery/gap-analysis/${job.id}?user_id=1`).catch(() => null),
  ])

  if (detailData) {
    detailJob.value = { ...detailData }
  }
  if (analysis) {
    analysisResult.value = analysis
  } else {
    // 兜底
    analysisResult.value = {
      company_summary: detailData?.company_intro || '',
      job_full_title: `${job.company_name} - ${job.job_title}`,
      location_detail: job.address,
      hard_skills: detailData?.skills_required || [],
      soft_skills: ['团队协作', '沟通能力', '学习能力'],
      preferred_skills: detailData?.skills_preferred || [],
      matched_skills: [],
      missing_skills: detailData?.skills_required || [],
      interview_focus: [],
      interview_rounds: detailData?.interview_rounds || '3轮',
      interview_form: detailData?.interview_form || '线上面试',
      resume_tips: ['突出项目中相关技术栈经验', '用量化数据展示成果', '提前了解公司业务'],
      deadline: `建议在${job.deadline}前完成投递`,
      has_exam: Boolean(job.has_exam),
      overall_assessment: `该岗位来自${job.company_name}，建议尽快准备投递。`,
    }
  }
  if (gap) {
    gapResult.value = gap
  }
  detailLoading.value = false
}

function openWebsite(url) {
  if (url && url.startsWith('http')) {
    window.open(url, '_blank')
  } else {
    ElMessage.info('官网链接暂不可用')
  }
}

async function goApplyPage() {
  if (detailJob.value) {
    await openApplyAndTrack(detailJob.value)
  }
}

function goInterview() {
  detailVisible.value = false
  // 把岗位数据存起来，面试页面自动填
  const job = detailJob.value
  const analysis = analysisResult.value
  if (job && analysis) {
    const material = [
      `公司：${job.company_name || ''}`,
      `行业：${job.industry || ''}`,
      `官方网站：${job.company_website || ''}`,
      `公司规模：${job.company_size || ''}`,
      `公司简介：${analysis.company_summary || job.company_intro || ''}`,
      ``,
      `岗位：${analysis.job_full_title || job.job_title || ''}`,
      `岗位类型：${job.job_type || ''}`,
      `工作地点：${analysis.location_detail || job.address || ''}`,
      `薪资范围：${job.salary_text || (job.salary_min && job.salary_max ? job.salary_min + 'K-' + job.salary_max + 'K' : '')}`,
      `学历要求：${job.education || ''}`,
      `经验要求：${job.experience || ''}`,
      `岗位职责：${job.job_description || ''}`,
      `截止时间：${analysis.deadline || job.deadline || ''}`,
      `含笔试环节：${analysis.has_exam ? '是' : '否'}`,
      ``,
      `硬性技能要求：${(analysis.hard_skills || job.skills_required || []).join('、')}`,
      `优先条件：${(analysis.preferred_skills || job.skills_preferred || []).join('、')}`,
      `软性技能：${(analysis.soft_skills || []).join('、')}`,
      `已匹配技能：${(analysis.matched_skills || []).join('、')}`,
      `缺失技能：${(analysis.missing_skills || []).join('、')}`,
      ``,
      `面试轮次：${analysis.interview_rounds || ''}`,
      `面试形式：${analysis.interview_form || ''}`,
      `面试重点：`,
      ...(analysis.interview_focus || []).map(f => `  - ${f}`),
      ``,
      `简历建议：`,
      ...(analysis.resume_tips || []).map(t => `  - ${t}`),
      ``,
      `综合评估：${analysis.overall_assessment || ''}`,
    ].filter(Boolean).join('\n')
    sessionStorage.setItem('qitu_interview_job', JSON.stringify({
      target: analysis.job_full_title || job.job_title || job.company_name,
      material: material,
    }))
  }
  router.push('/interview/session')
}

function goExam(skill) {
  detailVisible.value = false
  router.push('/exam-practice')
}

// ── 投递台账 ──
async function loadTracking() {
  const token = getToken()
  if (!token) return
  trackingLoading.value = true
  const data = await apiGet(`/api/delivery/tracking?token=${token}`)
  if (data) {
    trackingRecords.value = data.records || []
  }
  trackingLoading.value = false
}

// ── Tab 切换 ──
function switchTab(tab) {
  activeTab.value = tab
  if (tab === 'myapps') {
    loadMyAppsStats()
    loadMyApps()
    loadMyAppsFilterOpts()
  }
}

// ── 我的投递：加载列表 ──
async function loadMyApps() {
  myAppsLoading.value = true
  const token = getToken()
  if (!token) {
    myAppsLoading.value = false
    return
  }
  const params = new URLSearchParams()
  params.set('token', token)
  params.set('page', myAppsPage.value)
  params.set('page_size', myAppsPageSize)
  if (myFilters.value.status) params.set('status', myFilters.value.status)
  if (myFilters.value.company_size) params.set('company_size', myFilters.value.company_size)
  if (myFilters.value.date_range) params.set('date_range', myFilters.value.date_range)

  const data = await apiGet(`/api/delivery/my-apps?${params}`)
  if (data) {
    myAppsRecords.value = data.records || []
    myAppsTotal.value = data.total || 0
  } else {
    myAppsRecords.value = []
    myAppsTotal.value = 0
  }
  myAppsLoading.value = false
}

// ── 我的投递：加载统计数据 ──
async function loadMyAppsStats() {
  const token = getToken()
  if (!token) return
  const data = await apiGet(`/api/delivery/my-apps/stats?token=${token}`)
  if (data) {
    myStats.value = data
  }
}

// ── 我的投递：加载筛选选项 ──
async function loadMyAppsFilterOpts() {
  const token = getToken()
  if (!token) return
  const data = await apiGet(`/api/delivery/my-apps/filter-options?token=${token}`)
  if (data) {
    myFilterOpts.value = data
  }
}

// ── 我的投递：打开详情 ──
function openMyAppDetail(rec) {
  myAppDetail.value = rec
  interviewForm.value = {
    time: rec.interview_time || '',
    location: rec.interview_location || '',
    feedback: rec.hr_feedback || '',
  }
  interviewSaved.value = false
  myAppDetailVisible.value = true
}

// ── 我的投递：保存面试安排 ──
async function saveInterview() {
  const token = getToken()
  if (!token) return
  const form = interviewForm.value
  const url = `/api/delivery/tracking/${myAppDetail.value.id}/interview?token=${token}` +
    `&interview_time=${encodeURIComponent(form.time)}` +
    `&interview_location=${encodeURIComponent(form.location)}` +
    `&hr_feedback=${encodeURIComponent(form.feedback)}`
  const resp = await fetch(url, { method: 'PUT' })
  if (resp.ok) {
    interviewSaved.value = true
    // 同步更新本地记录
    myAppDetail.value.interview_time = form.time
    myAppDetail.value.interview_location = form.location
    myAppDetail.value.hr_feedback = form.feedback
    loadMyApps()
    loadMyAppsStats()
    ElMessage.success('面试安排已保存')
  }
}

// ── 我的投递：打开状态变更弹窗 ──
function changeMyAppStatus(rec) {
  selectedNewStatus.value = ''
  statusChangeNote.value = ''
  statusChangeVisible.value = true
}

// ── 我的投递：确认状态变更 ──
async function confirmStatusChange() {
  const token = getToken()
  if (!token) return
  const url = `/api/delivery/tracking/${myAppDetail.value.id}` +
    `?token=${token}&status=${encodeURIComponent(selectedNewStatus.value)}` +
    (statusChangeNote.value ? `&notes=${encodeURIComponent(statusChangeNote.value)}` : '')
  const resp = await fetch(url, { method: 'PUT' })
  if (resp.ok) {
    myAppDetail.value.status = selectedNewStatus.value
    if (statusChangeNote.value) {
      myAppDetail.value.notes = statusChangeNote.value
    }
    statusChangeVisible.value = false
    loadMyApps()
    loadMyAppsStats()
    ElMessage.success(`状态已更新为「${selectedNewStatus.value}」`)
  }
}

function inTracking(jobId) {
  return trackingRecords.value.some(r => r.job_id === jobId)
}

async function addToTracking(job, status = '已查看', showMessage = true) {
  const token = getToken()
  if (!token) {
    ElMessage.warning('请先登录')
    return
  }
  const result = await apiPost(
    `/api/delivery/tracking?token=${token}&job_id=${job.id}&company_name=${encodeURIComponent(job.company_name)}&job_title=${encodeURIComponent(job.job_title)}&company_logo=${encodeURIComponent(job.company_logo || '')}&company_size=${encodeURIComponent(job.company_size || '')}&industry=${encodeURIComponent(job.industry || '')}&status=${encodeURIComponent(status)}`
  )
  if (result) {
    if (showMessage) ElMessage.success(result.action === 'updated' ? '已更新投递记录' : '已加入投递清单')
    await loadTracking()
  }
}

async function updateStatus(row) {
  const token = getToken()
  const resp = await fetch(`/api/delivery/tracking/${row.id}?token=${token}&status=${encodeURIComponent(row.status)}`, { method: 'PUT' })
  if (resp.ok) {
    ElMessage.success(`状态已更新为「${row.status}」`)
    await Promise.all([loadTracking(), loadMyAppsStats()])
  } else {
    ElMessage.error('状态更新失败，请稍后再试')
  }
}

async function deleteTracking(row) {
  const token = getToken()
  const result = await fetch(`/api/delivery/tracking/${row.id}?token=${token}`, { method: 'DELETE' })
  if (result.ok) {
    ElMessage.success('已删除投递记录')
    await loadTracking()
  }
}

function openDetailById(jobId) {
  const job = jobs.value.find(j => j.id === jobId)
  if (job) {
    showDetail(job)
  } else {
    // 从后端单独加载
    apiGet(`/api/delivery/jobs/${jobId}`).then(data => {
      if (data) showDetail(data)
    })
  }
}
</script>

<style scoped>
/* ══════════════════════════════════════════════════════════════
   Delivery Assistant — 求职投递助手
   设计系统：轻色在线教育平台风
   ══════════════════════════════════════════════════════════════ */

.delivery-page {
  position: relative;
}
/* ── 区域一：顶部标题 & 用户信息栏 ── */
.zone-header {
  margin-bottom: 20px;
}

.zone-header .section-header {
  margin-bottom: 4px;
}

.page-hint {
  font-size: 14px;
  color: var(--text-muted);
  margin-bottom: 18px;
}

/* ── 求职意向栏（首页横幅风格） ── */
.user-info-bar {
  background: linear-gradient(117deg, #EFF6FF 8.64%, #DBEAFE 87.69%);
  border: 1.5px solid #BFDBFE;
  border-radius: 16px;
  padding: 18px 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  box-shadow: 0 4px 16px rgba(37,99,235,.06);
}
.uib-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.uib-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 800;
  font-size: 16px;
  color: #1E293B;
}
.uib-hint {
  font-size: 12px;
  color: #64748B;
  font-weight: 400;
}
.uib-fields {
  display: flex;
  align-items: center;
  gap: 0;
}
.uib-field {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 14px;
  border-right: 1px solid rgba(37,99,235,.15);
  flex: 1;
  min-width: 0;
  background: rgba(255,255,255,.45);
  border-radius: 0;
}
.uib-field:first-child {
  border-radius: 10px 0 0 10px;
}
.uib-field:last-child {
  border-right: none;
  border-radius: 0 10px 10px 0;
}
.uib-fname {
  font-size: 12px;
  color: #475569;
  white-space: nowrap;
  font-weight: 500;
}
.uib-fval {
  font-size: 13px;
  color: #1E293B;
  font-weight: 700;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 5px;
  transition: all .15s;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  background: rgba(255,255,255,.6);
  border: 1px solid transparent;
}
.uib-fval:hover {
  background: #fff;
  border-color: #BFDBFE;
  color: #2563EB;
}
.uib-input {
  flex: 1;
  min-width: 80px;
  padding: 5px 10px;
  border: 1.5px solid #2563EB;
  border-radius: 6px;
  font-size: 13px;
  font-family: inherit;
  outline: none;
  background: #fff;
  box-shadow: 0 0 0 3px rgba(37,99,235,.1);
}
.uib-field.editing {
  background: rgba(255,255,255,.8);
}

/* ── 真实投递 Agent ── */
.agent-search-card {
  margin: 0 0 16px;
  padding: 16px 18px;
  display: grid;
  grid-template-columns: minmax(260px, 0.9fr) minmax(320px, 1.1fr);
  gap: 22px;
  border-radius: 26px 10px 26px 26px;
  background:
    radial-gradient(circle at 8% 12%, rgba(14,165,233,.13), transparent 24%),
    linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 70%);
  border: 1.5px dashed #BFDBFE;
  box-shadow: 0 18px 40px rgba(37,99,235,.07);
}
.agent-copy {
  position: relative;
  min-height: 150px;
}
.agent-copy::after {
  content: 'QITU';
  position: absolute;
  right: 8px;
  bottom: -4px;
  color: rgba(37,99,235,.08);
  font-size: 50px;
  font-weight: 900;
  letter-spacing: .08em;
}
.agent-kicker {
  color: var(--primary);
  font-size: 13px;
  font-weight: 900;
  letter-spacing: .16em;
}
.agent-copy h2 {
  margin: 9px 0 8px;
  color: var(--text-heading);
  font-size: 25px;
  line-height: 1.25;
  font-weight: 900;
}
.agent-copy p,
.agent-step,
.agent-empty {
  color: var(--text-light);
  line-height: 1.7;
  font-size: 14px;
}
.agent-form {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  align-content: start;
}
.agent-form .el-button {
  min-height: 38px;
  border-radius: 12px;
  box-shadow: 6px 6px 14px rgba(37,99,235,.12), -6px -6px 14px rgba(255,255,255,.88);
}
.agent-result {
  grid-column: 1 / -1;
  padding: 14px 16px;
  border-radius: 18px;
  background: rgba(255,255,255,.78);
  border: 1px solid #DBEAFE;
}
.agent-result-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  color: var(--text-heading);
}
.agent-step {
  margin-top: 6px;
  padding-left: 12px;
  border-left: 3px solid #93C5FD;
}
.agent-empty {
  margin-top: 8px;
  color: #D97706;
}

/* ── 区域二：筛选栏 & 批量操作 ── */
.zone-filter {
  margin-bottom: 20px;
}

.filter-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px 16px;
  margin-bottom: 12px;
  padding: 12px 16px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

.filter-label {
  font-size: 12px;
  color: var(--text-muted);
  white-space: nowrap;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 4px;
}

.filter-label i {
  font-size: 11px;
}

.bulk-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 2px 0;
}

.bulk-actions .el-button i {
  margin-right: 4px;
}

/* ── 区域三：岗位列表 ── */
.zone-jobs {
  min-height: 300px;
}

.job-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 14px;
}

.job-card {
  display: flex;
  gap: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.25s;
  border-radius: var(--radius-md);
  position: relative;
}

.job-card:hover {
  border-color: var(--primary-light);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.card-selected {
  border-color: var(--primary) !important;
  background: var(--primary-bg);
}

.card-checkbox {
  padding-top: 3px;
  flex-shrink: 0;
}

.card-body {
  flex: 1;
  min-width: 0;
}

.card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 10px;
  gap: 8px;
}

.card-company {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  min-width: 0;
}

.company-logo {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  object-fit: contain;
  background: var(--bg-alt);
  padding: 3px;
  flex-shrink: 0;
}

.company-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-heading);
  line-height: 1.3;
}

.company-size-tag {
  font-size: 11px;
  color: var(--text-muted);
  background: var(--bg-alt);
  border-radius: 4px;
  padding: 1px 7px;
  display: inline-flex;
  align-items: center;
  gap: 3px;
  margin-top: 2px;
}

.company-size-tag i {
  font-size: 10px;
}

.job-title {
  font-size: 13px;
  color: var(--primary);
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
}

.card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 14px;
  margin-bottom: 12px;
}

.meta-item {
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 4px;
}

.meta-item i {
  font-size: 11px;
  width: 14px;
  text-align: center;
}

.card-footer {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.card-footer .el-button i {
  margin-right: 3px;
}

.pagination-wrap {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

/* ── 区域四：详情弹窗 ── */
.detail-dialog :deep(.el-dialog__body) {
  padding: 16px 24px;
  max-height: 65vh;
  overflow-y: auto;
}

.detail-block {
  margin-bottom: 16px;
  border-radius: var(--radius-md);
  overflow: hidden;
}

.detail-block-header {
  padding: 12px 16px;
  background: var(--bg-alt);
  font-size: 15px;
  font-weight: 600;
  color: var(--text-heading);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-block-header i {
  color: var(--primary);
  font-size: 15px;
}

.detail-block-body {
  padding: 14px 16px;
}

.detail-company-title {
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.detail-company-title strong {
  font-size: 15px;
  color: var(--text-heading);
}

.detail-industry-tag {
  font-size: 12px;
  color: var(--text-muted);
  background: var(--bg-alt);
  padding: 2px 10px;
  border-radius: 4px;
}

.company-intro {
  color: var(--text-body);
  font-size: 13px;
  line-height: 1.6;
  margin: 6px 0 10px;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.info-grid-item label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 3px;
  font-weight: 500;
}

.info-grid-item label i {
  font-size: 11px;
}

.info-grid-item span {
  font-size: 13px;
  color: var(--text-heading);
  font-weight: 500;
}

.skill-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skill-group label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-body);
  margin-bottom: 6px;
  font-weight: 500;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.match-group {
  background: var(--primary-bg);
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid var(--border-light);
}

.miss-group {
  background: var(--accent-bg);
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid var(--border-light);
}

.miss-hint {
  font-size: 11px;
  color: var(--text-muted);
  font-weight: normal;
  margin-left: 4px;
}

.focus-list {
  list-style: none;
  margin: 6px 0 0 0;
  padding: 0;
}

.focus-list li {
  font-size: 13px;
  color: var(--text-body);
  margin-bottom: 5px;
  display: flex;
  align-items: flex-start;
}

.deadline-highlight {
  font-size: 14px;
  color: var(--accent);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
}

.deadline-highlight i {
  color: var(--accent);
}

.exam-warning {
  color: var(--accent);
  font-size: 13px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 8px;
}

.resume-tips {
  margin-top: 12px;
}

.resume-tips label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--text-body);
  margin-bottom: 6px;
  font-weight: 500;
}

.tips-list {
  list-style: none;
  margin: 4px 0 0 0;
  padding: 0;
}

.tips-list li {
  font-size: 13px;
  color: var(--text-body);
  margin-bottom: 4px;
  display: flex;
  align-items: flex-start;
}

.assessment-text {
  margin-top: 12px;
  padding: 12px 14px;
  background: var(--primary-bg);
  border-radius: 8px;
  font-size: 13px;
  color: var(--text-body);
  line-height: 1.6;
  font-style: italic;
}

.assessment-text i {
  color: var(--primary-light);
  font-size: 12px;
}

/* ── 区域五：投递台账 ── */
.zone-tracking {
  margin-top: 32px;
  border-top: 1px solid var(--border);
  padding-top: 20px;
}

.tracking-badge {
  background: var(--primary-gradient);
  color: #fff;
  font-size: 11px;
  padding: 1px 9px;
  border-radius: 10px;
  font-weight: 600;
}

.tracking-table {
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--border);
}

.tracking-table :deep(.el-button) i {
  margin-right: 3px;
}

/* ══════════════════════════════════════════════════════════════
   我的投递 — Tab 栏 + 概览 + 卡片 + 状态标签 + 弹窗
   ══════════════════════════════════════════════════════════════ */

/* ── Tab 切换栏 ── */
.tab-bar {
  display: flex;
  gap: 0;
  margin-bottom: 20px;
  border-bottom: 2px solid var(--border);
}

.tab-item {
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-muted);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: all 0.25s;
  display: flex;
  align-items: center;
  gap: 6px;
  user-select: none;
}

.tab-item:hover {
  color: var(--primary);
}

.tab-item.active {
  color: var(--primary);
  border-bottom-color: var(--primary);
  font-weight: 600;
}

.tab-item i {
  font-size: 13px;
}

.tab-badge {
  background: var(--primary-gradient);
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  padding: 1px 7px;
  border-radius: 9px;
  min-width: 18px;
  text-align: center;
  line-height: 16px;
}

/* ── 数据概览条 ── */
.stats-bar {
  display: flex;
  align-items: center;
  gap: 0;
  padding: 16px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  margin-bottom: 14px;
}

.stat-item {
  flex: 1;
  text-align: center;
  padding: 4px 0;
}

.stat-value {
  font-size: 26px;
  font-weight: 700;
  color: var(--text-heading);
  line-height: 1.2;
}

.stat-label {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 3px;
  font-weight: 500;
}

.stat-divider {
  width: 1px;
  height: 36px;
  background: var(--border);
  flex-shrink: 0;
}

/* ── 我的投递筛选栏 ── */
.myapps-filter {
  margin-bottom: 14px;
}

/* ── 我的投递卡片列表 ── */
.myapps-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}

.myapps-card {
  display: flex;
  gap: 14px;
  padding: 14px 16px;
  cursor: pointer;
  transition: all 0.25s;
  border-radius: var(--radius-md);
  align-items: flex-start;
}

.myapps-card:hover {
  border-color: var(--primary-light);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.myapps-card-left {
  flex-shrink: 0;
}

.myapps-logo {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  object-fit: contain;
  background: var(--bg-alt);
  padding: 3px;
}

.myapps-card-body {
  flex: 1;
  min-width: 0;
}

.myapps-card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 6px;
}

.myapps-company {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-heading);
}

.myapps-jobtitle {
  font-size: 13px;
  color: var(--primary);
  font-weight: 500;
  margin-top: 1px;
}

.myapps-card-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 14px;
  margin-top: 4px;
}

.myapps-meta-item {
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 4px;
}

.myapps-meta-item i {
  font-size: 11px;
  color: var(--primary-light);
}

.myapps-notes {
  margin-top: 6px;
  font-size: 12px;
  color: var(--text-muted);
  background: var(--bg-alt);
  padding: 4px 10px;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

/* ── 进度状态标签（卡片上的小标签） ── */
.status-tag {
  display: inline-flex;
  align-items: center;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
}

.status-viewed {
  background: #ecf5ff;
  color: #409EFF;
  border: 1px solid #d9ecff;
}

.status-pending {
  background: #EFF6FF;
  color: #2563EB;
  border: 1px solid #BFDBFE;
}

.status-applied {
  background: #F0F9FF;
  color: #0EA5E9;
  border: 1px solid #BAE6FD;
}

.status-interview {
  background: #fdf6ec;
  color: #E6A23C;
  border: 1px solid #faecd8;
}

.status-passed {
  background: #e8f4fd;
  color: #409EFF;
  border: 1px solid #c6e2ff;
}

.status-offer {
  background: #f0f9eb;
  color: #67C23A;
  border: 1px solid #e1f3d8;
}

.status-rejected {
  background: #f4f4f5;
  color: #909399;
  border: 1px solid #e4e4e7;
}

.status-closed {
  background: #f4f4f5;
  color: #909399;
  border: 1px solid #e4e4e7;
}

/* ── 详情弹窗中的大状态标签 ── */
.status-tag-lg {
  display: inline-flex;
  align-items: center;
  padding: 4px 16px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 600;
}

.myapp-detail-status {
  margin-bottom: 16px;
}

.myapp-detail-body .detail-block {
  margin-bottom: 14px;
}

.myapp-detail-body .detail-block-body {
  padding: 14px 16px;
}

.save-tip {
  margin-left: 10px;
  font-size: 12px;
  color: #67C23A;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

/* ── 状态变更弹窗选项 ── */
.status-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.status-option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.2s;
  font-size: 13px;
  color: var(--text-body);
}

.status-option:hover {
  border-color: var(--primary-light);
  background: var(--primary-bg);
}

.status-option.selected {
  border-color: var(--primary);
  background: var(--primary-bg);
  font-weight: 600;
  color: var(--primary);
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-dot.status-viewed {
  background: #409EFF;
}

.status-dot.status-pending {
  background: #2563EB;
}

.status-dot.status-applied {
  background: #0EA5E9;
}

@media (max-width: 900px) {
  .agent-search-card {
    grid-template-columns: 1fr;
    padding: 18px;
  }
  .agent-form {
    grid-template-columns: 1fr;
  }
  .job-grid {
    grid-template-columns: 1fr;
  }
}

.status-dot.status-interview {
  background: #E6A23C;
}

.status-dot.status-passed {
  background: #409EFF;
}

.status-dot.status-offer {
  background: #67C23A;
}

.status-dot.status-rejected {
  background: #909399;
}

.status-dot.status-closed {
  background: #909399;
}

/* ── 面试详情弹窗微调 ── */
.interview-dialog :deep(.el-dialog__body) {
  padding: 16px 24px;
  max-height: 65vh;
  overflow-y: auto;
}

.interview-dialog :deep(.el-input__inner) {
  font-size: 13px;
}

/* ── Element Plus 微调 ── */
:deep(.el-table) {
  font-size: 13px;
}

:deep(.el-tag) {
  margin: 0;
}

:deep(.el-button--small i) {
  margin-right: 2px;
}

/* ── 差距分析板块 ── */
.gap-block {
  border-left: 3px solid #E6A23C;
}
.gap-score-row {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 16px;
}
.gap-score-circle {
  flex-shrink: 0;
}
.gap-score-info {
  flex: 1;
}
.gap-readiness-badge {
  display: inline-block;
  padding: 3px 12px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 700;
  margin-bottom: 6px;
}
.gap-readiness-badge.badge-ready {
  background: #f0f9eb;
  color: #67C23A;
}
.gap-readiness-badge.badge-nearly_ready {
  background: #fdf6ec;
  color: #E6A23C;
}
.gap-readiness-badge.badge-need_work {
  background: #fef0f0;
  color: #F56C6C;
}
.gap-summary {
  font-size: 14px;
  color: #606266;
  margin: 0;
  line-height: 1.5;
}
.gap-recommend-list {
  list-style: none;
  padding: 0;
  margin: 8px 0 0;
}
.gap-recommend-list li {
  display: flex;
  align-items: center;
  font-size: 13px;
  color: #606266;
  padding: 4px 0;
}
.gap-exam-feedback {
  margin-top: 12px;
  padding: 10px 14px;
  background: #fdf6ec;
  border-radius: 8px;
  font-size: 13px;
  color: #7c6a2e;
  display: flex;
  align-items: center;
  gap: 6px;
}
.gap-loading {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 0;
  font-size: 14px;
  color: #909399;
}
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>