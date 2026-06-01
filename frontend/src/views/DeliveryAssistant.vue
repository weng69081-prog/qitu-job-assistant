<template>
  <div class="page delivery-page">
    <!-- ═══ 页面顶部 Banner ═══ -->
    <div class="banner-wrap">
      <PageBanner fullwidth
        title="求职投递助手"
        description="智能匹配岗位、一键投递、追踪面试全流程进度"
        icon="fa-paper-plane"
        variant="primary"
      />
      <img src="/src/assets/delivery-cat.png" class="banner-cat" alt="小橘投递">
    </div>
    <!-- ══════════════════════════════════════════════════════════
         一、顶部标题 & 用户求职信息栏
         ══════════════════════════════════════════════════════════ -->
    <section class="zone-header">
      <div class="user-info-bar card">
        <div class="info-item">
          <i class="fas fa-map-marker-alt info-icon"></i>
          <span class="info-label">意向城市</span>
          <span class="info-value">{{ userProfile.city || '未设置' }}</span>
        </div>
        <div class="info-divider"></div>
        <div class="info-item">
          <i class="fas fa-bullseye info-icon"></i>
          <span class="info-label">目标岗位</span>
          <span class="info-value">{{ userProfile.job_targets || '未设置' }}</span>
        </div>
        <div class="info-divider"></div>
        <div class="info-item">
          <i class="fas fa-coins info-icon"></i>
          <span class="info-label">期望薪资</span>
          <span class="info-value">{{ userProfile.salary || '未设置' }}</span>
        </div>
        <div class="info-divider"></div>
        <div class="info-item">
          <i class="fas fa-tags info-icon"></i>
          <span class="info-label">技能标签</span>
          <span class="info-value tag-value">{{ userProfile.skills || '未设置' }}</span>
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
        <i class="fas fa-star"></i> 推荐岗位
      </div>
      <div
        class="tab-item"
        :class="{ active: activeTab === 'myapps' }"
        @click="switchTab('myapps')"
      >
        <i class="fas fa-clipboard-check"></i> 我的投递
        <span v-if="myAppsCount > 0" class="tab-badge">{{ myAppsCount }}</span>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════════════
         三、推荐岗位 Tab
         ══════════════════════════════════════════════════════════ -->
    <template v-if="activeTab === 'recommend'">
      <!-- 筛选栏 & 批量操作栏 -->
    <section class="zone-filter">
      <div class="filter-bar">
        <div class="filter-group">
          <span class="filter-label"><i class="fas fa-building"></i> 公司规模</span>
          <el-select v-model="filters.company_size" placeholder="不限" clearable style="width:105px" @change="loadJobs">
            <el-option label="小型" value="小型" />
            <el-option label="中型" value="中型" />
            <el-option label="大型" value="大型" />
            <el-option label="巨头" value="巨头" />
          </el-select>
        </div>
        <div class="filter-group">
          <span class="filter-label"><i class="fas fa-briefcase"></i> 岗位类型</span>
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
          <span class="filter-label"><i class="fas fa-city"></i> 城市</span>
          <el-select v-model="filters.city" placeholder="不限" clearable style="width:115px" @change="loadJobs">
            <el-option v-for="c in filterOptions.cities" :key="c" :label="c" :value="c" />
          </el-select>
        </div>
        <div class="filter-group">
          <span class="filter-label"><i class="fas fa-coins"></i> 薪资</span>
          <el-select v-model="filters.salary_range" placeholder="不限" clearable style="width:115px" @change="loadJobs">
            <el-option label="8K以下" value="0-8000" />
            <el-option label="8K-15K" value="8000-15000" />
            <el-option label="15K-25K" value="15000-25000" />
            <el-option label="25K-40K" value="25000-40000" />
            <el-option label="40K以上" value="40000-999999" />
          </el-select>
        </div>
        <div class="filter-group">
          <span class="filter-label"><i class="fas fa-clock"></i> 发布时间</span>
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
          <i class="fas fa-check-double"></i>
          全选 {{ selectedCount ? `(${selectedCount})` : '' }}
        </el-button>
        <el-button size="small" @click="invertSelect">
          <i class="fas fa-exchange-alt"></i> 反选
        </el-button>
        <el-button size="small" @click="clearSelect">
          <i class="fas fa-eraser"></i> 清空
        </el-button>
        <el-button type="primary" size="small" @click="batchApply" :disabled="!selectedCount">
          <i class="fas fa-rocket"></i> 批量投递
        </el-button>
        <el-button type="success" size="small" @click="batchAddToList" :disabled="!selectedCount">
          <i class="fas fa-plus-circle"></i> 加入投递清单
        </el-button>
      </div>
    </section>

    <!-- ══════════════════════════════════════════════════════════
         三、主体岗位列表区
         ══════════════════════════════════════════════════════════ -->
    <section class="zone-jobs">
      <div v-if="loading" class="loading-state">
        <i class="fas fa-spinner fa-pulse" style="font-size:28px;margin-bottom:12px"></i>
        <p>正在加载岗位数据...</p>
      </div>

      <div v-else-if="!jobs.length" class="empty-state">
        <i class="fas fa-search empty-icon"></i>
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
                  <span class="company-size-tag"><i class="fas fa-layer-group"></i> {{ job.company_size }}</span>
                </div>
              </div>
              <div class="job-title">{{ job.job_title }}</div>
            </div>

            <div class="card-meta">
              <span class="meta-item">
                <i class="fas fa-map-marker-alt"></i>
                {{ job.city }}{{ job.address ? '·' + job.address.replace(job.city, '') : '' }}
              </span>
              <span class="meta-item">
                <i class="fas fa-coins"></i> {{ job.salary_text }}
              </span>
              <span class="meta-item">
                <i class="fas fa-calendar-alt"></i> {{ job.publish_time }}
              </span>
            </div>

            <div class="card-footer">
              <el-button size="small" type="primary" plain @click.stop="showDetail(job)">
                <i class="fas fa-info-circle"></i> 查看详情
              </el-button>
              <el-button size="small" plain @click.stop="openWebsite(job.company_website)">
                <i class="fas fa-building"></i> 公司官网
              </el-button>
              <el-button
                size="small"
                :type="inTracking(job.id) ? 'success' : 'default'"
                @click.stop="addToTracking(job)"
              >
                <i :class="inTracking(job.id) ? 'fas fa-check-circle' : 'fas fa-plus-circle'"></i>
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
        <i class="fas fa-spinner fa-pulse" style="font-size:24px;margin-bottom:10px"></i>
        <p>AI正在解析岗位信息...</p>
      </div>

      <div v-else-if="analysisResult" class="detail-content">
        <!-- 板块1：企业基础信息 -->
        <div class="detail-block card">
          <div class="detail-block-header">
            <i class="fas fa-building"></i>
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
                <label><i class="fas fa-tag"></i> 岗位全称</label>
                <span>{{ analysisResult.job_full_title }}</span>
              </div>
              <div class="info-grid-item">
                <label><i class="fas fa-map-pin"></i> 工作地点</label>
                <span>{{ analysisResult.location_detail }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 板块2：岗位核心解读 -->
        <div class="detail-block card">
          <div class="detail-block-header">
            <i class="fas fa-bullseye"></i>
            岗位核心解读
          </div>
          <div class="detail-block-body">
            <div class="skill-section">
              <div class="skill-group">
                <label><i class="fas fa-tools"></i> 硬性技能要求</label>
                <div class="skill-tags">
                  <el-tag
                    v-for="s in analysisResult.hard_skills" :key="s" size="small"
                    :type="analysisResult.matched_skills?.includes(s) ? 'success' : 'danger'"
                  >
                    {{ s }}
                    <i v-if="analysisResult.matched_skills?.includes(s)" class="fas fa-check-circle" style="margin-left:3px"></i>
                    <i v-else class="fas fa-times-circle" style="margin-left:3px"></i>
                  </el-tag>
                </div>
              </div>
              <div class="skill-group">
                <label><i class="fas fa-hand-peace"></i> 软性要求</label>
                <div class="skill-tags">
                  <el-tag v-for="s in analysisResult.soft_skills" :key="s" size="small">{{ s }}</el-tag>
                </div>
              </div>
              <div class="skill-group">
                <label><i class="fas fa-star"></i> 加分技能</label>
                <div class="skill-tags">
                  <el-tag v-for="s in analysisResult.preferred_skills" :key="s" size="small" type="warning">{{ s }}</el-tag>
                </div>
              </div>
              <div v-if="analysisResult.matched_skills?.length" class="skill-group match-group">
                <label><i class="fas fa-check-circle" style="color:var(--primary)"></i> 已匹配技能</label>
                <div class="skill-tags">
                  <el-tag v-for="s in analysisResult.matched_skills" :key="s" size="small" type="success">{{ s }}</el-tag>
                </div>
              </div>
              <div v-if="analysisResult.missing_skills?.length" class="skill-group miss-group">
                <label>
                  <i class="fas fa-times-circle" style="color:var(--accent)"></i> 缺失技能
                  <span class="miss-hint">（点击可前往笔试练习）</span>
                </label>
                <div class="skill-tags">
                  <el-tag
                    v-for="s in analysisResult.missing_skills" :key="s" size="small" type="danger"
                    style="cursor:pointer" @click="goExam(s)"
                  >
                    {{ s }} <i class="fas fa-pen"></i>
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 板块3：面试专项汇总 -->
        <div class="detail-block card">
          <div class="detail-block-header">
            <i class="fas fa-microphone"></i>
            面试专项汇总
          </div>
          <div class="detail-block-body">
            <div class="info-grid">
              <div class="info-grid-item">
                <label><i class="fas fa-sort-numeric-up-alt"></i> 面试轮次</label>
                <span>{{ analysisResult.interview_rounds }}</span>
              </div>
              <div class="info-grid-item">
                <label><i class="fas fa-video"></i> 面试形式</label>
                <span>{{ analysisResult.interview_form }}</span>
              </div>
            </div>
            <div class="skill-group" style="margin-top:12px">
              <label><i class="fas fa-star"></i> 历年面试重点</label>
              <ul class="focus-list">
                <li v-for="(f, i) in analysisResult.interview_focus" :key="i">
                  <i class="fas fa-circle" style="font-size:6px;color:var(--primary);margin-right:6px"></i>
                  {{ f }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- 板块4：投递须知 -->
        <div class="detail-block card">
          <div class="detail-block-header">
            <i class="fas fa-clipboard-list"></i>
            投递须知
          </div>
          <div class="detail-block-body">
            <p class="deadline-highlight">
              <i class="fas fa-clock"></i> 截止时间：<strong>{{ analysisResult.deadline }}</strong>
            </p>
            <p v-if="analysisResult.has_exam" class="exam-warning">
              <i class="fas fa-exclamation-triangle"></i> 该岗位含有笔试环节，建议提前准备
            </p>
            <div v-if="analysisResult.resume_tips?.length" class="resume-tips">
              <label><i class="fas fa-lightbulb"></i> 简历建议</label>
              <ul class="tips-list">
                <li v-for="(tip, i) in analysisResult.resume_tips" :key="i">
                  <i class="fas fa-circle" style="font-size:5px;color:var(--text-muted);margin-right:6px"></i>
                  {{ tip }}
                </li>
              </ul>
            </div>
            <p class="assessment-text">
              <i class="fas fa-quote-left" style="margin-right:4px"></i>
              {{ analysisResult.overall_assessment }}
              <i class="fas fa-quote-right" style="margin-left:4px"></i>
            </p>
          </div>
        </div>
      </div>

      <template #footer>
        <el-button @click="detailVisible = false">
          <i class="fas fa-times"></i> 关闭
        </el-button>
        <el-button type="primary" @click="goApplyPage">
          <i class="fas fa-rocket"></i> 跳转官方招聘页
        </el-button>
        <el-button type="success" @click="goInterview">
          <i class="fas fa-microphone"></i> 前往面试练习
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
          <span class="filter-label"><i class="fas fa-tag"></i> 进度状态</span>
          <el-select v-model="myFilters.status" placeholder="全部状态" clearable style="width:130px" @change="loadMyApps">
            <el-option v-for="s in myFilterOpts.statuses" :key="s" :label="s" :value="s" />
          </el-select>
        </div>
        <div class="filter-group">
          <span class="filter-label"><i class="fas fa-layer-group"></i> 公司类型</span>
          <el-select v-model="myFilters.company_size" placeholder="不限" clearable style="width:110px" @change="loadMyApps">
            <el-option v-for="s in myFilterOpts.company_sizes" :key="s" :label="s" :value="s" />
          </el-select>
        </div>
        <div class="filter-group">
          <span class="filter-label"><i class="fas fa-clock"></i> 投递时间</span>
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
        <i class="fas fa-spinner fa-pulse" style="font-size:28px"></i>
        <p style="margin-top:10px">加载投递记录...</p>
      </div>

      <!-- 空状态 -->
      <div v-else-if="!myAppsRecords.length" class="empty-state" style="padding:60px 0">
        <i class="fas fa-inbox empty-icon" style="font-size:48px"></i>
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
                <i class="fas fa-building"></i> {{ rec.company_size }}
              </span>
              <span v-if="rec.industry" class="myapps-meta-item">
                <i class="fas fa-tag"></i> {{ rec.industry }}
              </span>
              <span class="myapps-meta-item">
                <i class="fas fa-calendar-alt"></i> {{ rec.apply_time }}
              </span>
              <span v-if="rec.interview_time" class="myapps-meta-item">
                <i class="fas fa-clock"></i> {{ rec.interview_time }}
              </span>
            </div>
            <div v-if="rec.notes" class="myapps-notes">
              <i class="fas fa-pencil-alt"></i> {{ rec.notes }}
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
            <i class="fas fa-building"></i> 基本信息
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
            <i class="fas fa-calendar-check"></i> 面试安排
          </div>
          <div class="detail-block-body">
            <div class="info-grid">
              <div class="info-grid-item">
                <label><i class="fas fa-clock"></i> 面试时间</label>
                <el-input
                  v-model="interviewForm.time"
                  placeholder="如：2026-06-15 14:00"
                  size="small"
                />
              </div>
              <div class="info-grid-item">
                <label><i class="fas fa-map-pin"></i> 面试地点</label>
                <el-input
                  v-model="interviewForm.location"
                  placeholder="线上面试/具体地址"
                  size="small"
                />
              </div>
            </div>
            <div style="margin-top:10px">
              <label style="font-size:12px;color:var(--text-muted);font-weight:500">
                <i class="fas fa-comment"></i> HR反馈备注
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
              <i class="fas fa-save"></i> 保存面试安排
            </el-button>
            <span v-if="interviewSaved" class="save-tip">
              <i class="fas fa-check-circle" style="color:#67C23A"></i> 已保存
            </span>
          </div>
        </div>

        <!-- HR反馈 -->
        <div v-if="myAppDetail.hr_feedback" class="detail-block card">
          <div class="detail-block-header">
            <i class="fas fa-comment-dots"></i> HR反馈
          </div>
          <div class="detail-block-body">
            <p style="color:var(--text-body);font-size:13px;line-height:1.6">{{ myAppDetail.hr_feedback }}</p>
          </div>
        </div>
      </div>

      <template #footer>
        <el-button @click="myAppDetailVisible = false">
          <i class="fas fa-times"></i> 关闭
        </el-button>
        <el-button type="primary" @click="changeMyAppStatus(myAppDetail)">
          <i class="fas fa-edit"></i> 更新进度状态
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
          <i class="fas fa-check"></i> 确认更新
        </el-button>
      </template>
    </el-dialog>

    <!-- ══════════════════════════════════════════════════════════
         原区域五：投递台账（已有记录的兜底展示，被我的投递替代，保留不显示）
         ══════════════════════════════════════════════════════════ -->
    <section class="zone-tracking">
      <div class="section-header" style="margin-bottom:16px">
        <div class="section-title">
          <i class="fas fa-clipboard-check"></i>
          我的投递记录
          <span class="tracking-badge" v-if="trackingRecords.length">{{ trackingRecords.length }}</span>
        </div>
      </div>

      <div v-if="trackingLoading" class="loading-state" style="padding:30px 0">
        <i class="fas fa-spinner fa-pulse"></i>
      </div>

      <div v-else-if="!trackingRecords.length" class="empty-state" style="padding:30px 0">
        <i class="fas fa-inbox empty-icon" style="font-size:36px"></i>
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
              <i class="fas fa-info-circle"></i> 查看岗位
            </el-button>
            <el-button size="small" text type="primary" @click="goInterview">
              <i class="fas fa-microphone"></i> 查看面经
            </el-button>
            <el-button size="small" text type="danger" @click="deleteTracking(row)">
              <i class="fas fa-trash-alt"></i> 删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
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

const filterOptions = ref({ cities: [], job_types: [], company_sizes: [] })
const filters = ref({
  company_size: '',
  job_type: '',
  city: '',
  salary_range: '',
  publish_time: '',
  keyword: '',
})

// 选中状态
const selectedIds = ref(new Set())
const selectedCount = computed(() => selectedIds.value.size)
const allSelected = computed(() => selectedCount.value > 0 && selectedCount.value === jobs.value.length)

// 详情弹窗
const detailVisible = ref(false)
const detailJob = ref(null)
const detailLoading = ref(false)
const analysisResult = ref(null)

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
  { value: '已查看', label: '已查看（浏览过岗位）', cls: 'viewed' },
  { value: '待面试', label: '待面试（已获面试邀请）', cls: 'interview' },
  { value: '面试通过', label: '面试通过', cls: 'passed' },
  { value: '已offer', label: '已拿到 Offer', cls: 'offer' },
  { value: '已拒', label: '已被拒绝', cls: 'rejected' },
  { value: '已关闭', label: '已关闭（放弃跟进）', cls: 'closed' },
]

function statusClass(status) {
  const map = {
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

async function apiPost(url) {
  try {
    const resp = await fetch(url, { method: 'POST' })
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
    window.open(job.company_website, '_blank')
  }
  ElMessage.success(`已打开 ${selected.length} 个岗位投递链接`)
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

  // 并行获取详情和AI分析
  const token = getToken()
  const skills = userProfile.value?.skills || ''

  const [detailData, analysis] = await Promise.all([
    apiGet(`/api/delivery/jobs/${job.id}`),
    apiPost(`/api/delivery/ai-analyze/${job.id}?user_skills=${encodeURIComponent(skills)}`),
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
  detailLoading.value = false
}

function openWebsite(url) {
  if (url && url.startsWith('http')) {
    window.open(url, '_blank')
  } else {
    ElMessage.info('官网链接暂不可用')
  }
}

function goApplyPage() {
  if (detailJob.value?.apply_url) {
    window.open(detailJob.value.apply_url, '_blank')
  }
}

function goInterview() {
  detailVisible.value = false
  router.push('/interview')
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

async function addToTracking(job) {
  const token = getToken()
  if (!token) {
    ElMessage.warning('请先登录')
    return
  }
  const result = await apiPost(
    `/api/delivery/tracking?token=${token}&job_id=${job.id}&company_name=${encodeURIComponent(job.company_name)}&job_title=${encodeURIComponent(job.job_title)}&company_logo=${encodeURIComponent(job.company_logo || '')}&company_size=${encodeURIComponent(job.company_size || '')}&industry=${encodeURIComponent(job.industry || '')}&status=已查看`
  )
  if (result) {
    ElMessage.success(result.action === 'updated' ? '已更新投递记录' : '已加入投递清单')
    await loadTracking()
  }
}

async function updateStatus(row) {
  const token = getToken()
  await apiPost(`/api/delivery/tracking/${row.id}?token=${token}&status=${encodeURIComponent(row.status)}`)
  ElMessage.success(`状态已更新为「${row.status}」`)
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

.user-info-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0;
  padding: 14px 20px;
  border-radius: var(--radius-md);
  background: var(--bg-alt);
  border: 1px solid var(--border-light);
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 16px;
  font-size: 13px;
}

.info-item:first-child {
  padding-left: 0;
}

.info-icon {
  width: 16px;
  color: var(--primary);
  font-size: 14px;
  text-align: center;
}

.info-label {
  color: var(--text-muted);
  white-space: nowrap;
  font-weight: 500;
}

.info-value {
  color: var(--text-heading);
  font-weight: 600;
}

.tag-value {
  color: var(--primary);
}

.info-divider {
  width: 1px;
  height: 20px;
  background: var(--border);
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
</style>