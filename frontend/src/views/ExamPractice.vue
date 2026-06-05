<template>
  <div class="exam-practice-page">
    <!-- ═══ 页面顶部 Banner ═══ -->
    <div class="banner-wrap">
      <PageBanner fullwidth
        title="笔试练习"
        description="海量题库 + AI 智能出题，针对性练习提升笔试通过率"
        :icon="'Pen'"
        variant="primary"
      />
      <img src="/src/assets/exam-cat.png" class="banner-cat" alt="小橘笔试">
    </div>
    <!-- ═══ 笔试模式导航：专项练习 / 模拟考试 / 错题本 ═══ -->
    <div class="exam-mode-nav">
      <router-link to="/exam-practice" class="emn-item" active-class="emn-active">
        <Book :size="16" class="icon-blue" /> 专项练习
      </router-link>
      <router-link to="/exam/session" class="emn-item" active-class="emn-active">
        <FileText :size="16" class="icon-blue" /> 模拟考试
      </router-link>
      <router-link to="/exam/wrong" class="emn-item" active-class="emn-active">
        <Redo :size="16" class="icon-blue" /> 错题重练
      </router-link>
    </div>
    <!-- ═══════ 1. 筛选&选题区 ═══════ -->
    <div class="filter-section">
      <div class="card" style="padding:18px 20px">
        <!-- 第一行：岗位 + 关键词搜索 + 模式切换 -->
        <div class="filter-row-1">
          <div class="filter-group" style="flex:2;min-width:200px">
            <span class="filter-label"><Crosshair :size="16" class="icon-blue" /> 目标岗位</span>
            <el-select v-model="career" placeholder="选择岗位" filterable clearable style="width:100%"
              @change="onCareerChange">
              <el-option-group v-if="store.validBookmarks.length" label="⭐ 已收藏">
                <el-option v-for="b in store.validBookmarks" :key="b.career" :label="b.career" :value="b.career" />
              </el-option-group>
              <el-option-group v-for="g in careerGroups" :key="g.label" :label="g.label">
                <el-option v-for="c in g.list" :key="c" :label="c" :value="c" />
              </el-option-group>
            </el-select>
          </div>
          <div class="filter-group" style="flex:1.5;min-width:160px">
            <span class="filter-label"><Search :size="16" class="icon-blue" /> 关键词搜索</span>
            <el-input v-model="searchKeyword" placeholder="搜索题库..." clearable size="default">
              <template #prefix><Search :size="16" :color="'var(--text-muted)'" /></template>
            </el-input>
          </div>
        </div>

        <!-- 第二行：模式 + 难度 + 题型 -->
        <div class="filter-row-2">
          <div class="filter-group" style="flex:2">
            <span class="filter-label"><Pin :size="16" class="icon-blue" /> 刷题模式</span>
            <el-radio-group v-model="mode" class="mode-radio-group">
              <el-radio-button value="专项练习"><Book :size="16" class="icon-blue" /> 专项练习</el-radio-button>
              <el-radio-button value="计时模考"><Timer :size="16" class="icon-blue" /> 计时模考</el-radio-button>
              <el-radio-button value="随机刷题"><Dice :size="16" class="icon-blue" /> 随机刷题</el-radio-button>
            </el-radio-group>
          </div>
          <div class="filter-group" style="flex:1;min-width:120px">
            <span class="filter-label"><Signal :size="16" class="icon-blue" /> 难度</span>
            <el-select v-model="difficulty" placeholder="不限" clearable style="width:100%">
              <el-option label="不限" value="all" />
              <el-option label="入门" value="easy" />
              <el-option label="基础" value="medium" />
              <el-option label="进阶" value="hard" />
            </el-select>
          </div>
          <div class="filter-group" style="flex:1;min-width:120px">
            <span class="filter-label"><List :size="16" class="icon-blue" /> 题型</span>
            <el-select v-model="questionType" placeholder="不限" clearable style="width:100%">
              <el-option label="不限" value="all" />
              <el-option label="单选题" value="single_choice" />
              <el-option label="多选题" value="multi_choice" />
              <el-option label="判断题" value="judge" />
            </el-select>
          </div>
        </div>

        <!-- 第三行：题库预览 + 开始按钮 -->
        <div class="filter-row-3">
          <div class="library-preview">
            <div class="preview-stat">
              <span class="preview-label"><Database :size="16" class="icon-blue" /> 总题量</span>
              <span class="preview-value">{{ libraryStats.total }}<small> 题</small></span>
            </div>
            <el-divider direction="vertical" />
            <div class="preview-stat">
              <span class="preview-label"><Clock :size="16" class="icon-blue" /> 预估用时</span>
              <span class="preview-value">{{ libraryStats.estimatedTime }}<small> min</small></span>
            </div>
            <el-divider direction="vertical" />
            <div class="preview-stat">
              <span class="preview-label"><Crosshair :size="16" class="icon-blue" /> 历史正确率</span>
              <span class="preview-value" :style="{ color: libraryStats.historyAccuracy > 70 ? 'var(--primary)' : libraryStats.historyAccuracy > 40 ? 'var(--accent)' : 'var(--accent)' }">
                {{ libraryStats.historyAccuracy }}<small>%</small>
              </span>
            </div>
          </div>
          <button class="btn-primary" style="padding:10px 28px;font-size:0.95rem" @click="startPractice"
            :disabled="!career || loadingAI" :class="{ loading: loading }">
            <Rocket :size="16" class="icon-blue" />
            {{ loadingAI ? 'AI正在生成题库...' : loading ? '加载中...' : '开始刷题' }}
          </button>
        </div>
      </div>
    </div>

    <!-- ═══════ 2. 核心数据看板（粘性定位） ═══════ -->
    <div class="dashboard-sticky-wrap" ref="dashboardWrap">
      <div class="dashboard-section" :class="{ 'is-stuck': isStuck }">
        <div class="section-header" style="margin-bottom:12px;padding:0">
          <div class="section-title" style="font-size:0.95rem">
            <BarChart :size="16" class="icon-blue" /> 练习统计看板
          </div>
          <span class="section-more" style="font-size:0.72rem;color:var(--text-muted)">一页看尽近况</span>
        </div>

        <div class="dash-cards">
          <!-- 卡1：总刷题量 + 迷你趋势折线 -->
          <div class="stat-card dash-card-hover" @mouseenter="dashHover=0" @mouseleave="dashHover=-1">
            <div class="stat-icon"><Pen :size="16" class="icon-blue" /></div>
            <div class="stat-num">{{ dashData.totalQuestions }}</div>
            <div class="stat-label">总刷题量</div>
            <div class="dc-mini-chart">
              <svg viewBox="0 0 100 36" class="mini-trend" v-if="dashTrendData.length > 1">
                <path :d="dashTrendPath" fill="none" stroke="var(--primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <div v-else class="mini-empty">暂无</div>
            </div>
            <!-- hover tooltip -->
            <div class="dc-tooltip" v-if="dashHover === 0">
              <div v-for="d in dashTrendData.slice(-7)" :key="d.date" class="tt-row">
                <span class="tt-date">{{ d.date.slice(5) }}</span>
                <span class="tt-val">{{ d.questions }}题</span>
              </div>
            </div>
          </div>

          <!-- 卡2：近7天正确率 + 环形进度 -->
          <div class="stat-card dash-card-hover" @mouseenter="dashHover=1" @mouseleave="dashHover=-1">
            <div class="stat-icon"><Crosshair :size="16" class="icon-blue" /></div>
            <div class="stat-num">{{ dashData.weekAccuracy }}</div>
            <div class="stat-label">近7天正确率</div>
            <div class="dc-mini-chart chart-ring">
              <svg viewBox="0 0 40 40" class="ring-svg">
                <circle cx="20" cy="20" r="16" fill="none" stroke="var(--border-light)" stroke-width="4" />
                <circle cx="20" cy="20" r="16" fill="none" stroke="var(--primary)" stroke-width="4"
                  :stroke-dasharray="circumference" :stroke-dashoffset="ringOffset"
                  stroke-linecap="round" transform="rotate(-90 20 20)" />
                <text x="20" y="20" text-anchor="middle" dominant-baseline="central"
                  font-size="9" font-weight="700" :fill="dashData.weekAccuracy > 70 ? 'var(--primary)' : 'var(--accent)'">
                  {{ dashData.weekAccuracy }}%
                </text>
              </svg>
            </div>
          </div>

          <!-- 卡3：连续打卡天数 + 火焰图标 -->
          <div class="stat-card dash-card-hover" @mouseenter="dashHover=2" @mouseleave="dashHover=-1">
            <div class="stat-icon"><Flame :size="16" :color="'var(--accent)'" /></div>
            <div class="stat-num">{{ dashData.streakDays }}</div>
            <div class="stat-label">连续打卡</div>
            <div class="dc-mini-chart streak-vis">
              <div v-for="i in 7" :key="i" class="streak-dot"
                :class="{ active: i <= dashData.streakDays, max: i === dashData.streakDays && dashData.streakDays > 0 }"
                :style="{ opacity: i <= dashData.streakDays ? 0.4 + (i / 7) * 0.6 : 0.15 }">
              </div>
              <span class="streak-suffix" v-if="dashData.streakDays > 0"><Flame :size="16" class="icon-blue" /> {{ dashData.streakDays }}天连击</span>
            </div>
          </div>

          <!-- 卡4：本周完成率 + 横向进度条 -->
          <div class="stat-card dash-card-hover" @mouseenter="dashHover=3" @mouseleave="dashHover=-1">
            <div class="stat-icon"><Footprints :size="16" class="icon-blue" /></div>
            <div class="stat-num">{{ dashData.weekCompletion }}</div>
            <div class="stat-label">本周完成率</div>
            <div class="dc-mini-chart completion-bar-wrap">
              <div class="completion-track">
                <div class="completion-fill" :style="{ width: dashData.weekCompletion + '%' }"></div>
              </div>
              <span class="completion-hint">{{ dashData.weekDone }}/{{ dashData.weekGoal }}天</span>
            </div>
          </div>
        </div>

        <!-- 薄弱模块提示 -->
        <div class="dash-weak-tip" v-if="dashWeakModules.length">
          <TriangleAlert :size="16" class="icon-blue" style="margin-right:6px" />
          近3天薄弱模块：<b>{{ dashWeakModules }}</b>
        </div>
      </div>
    </div>

    <!-- ═══════ 3. 主内容区 Tabs ═══════ -->
    <el-tabs v-model="activeTab" class="main-tabs" @tab-click="onTabClick">
      <!-- ─── Tab 1: 刷题 ─── -->
      <el-tab-pane label="刷题" name="practice">
        <template #label>
          <span><Pen :size="16" class="icon-blue" /> 刷题</span>
        </template>
        <!-- 设置（选题数） -->
        <div v-if="practicePhase === 'setup'" class="practice-setup">
          <div class="card" style="padding:16px 20px">
            <div class="setup-inner">
              <div class="setup-icon"><Book :size="2" :color="'var(--primary)'" /></div>
              <div class="setup-text">
                <h3>准备好了吗？</h3>
                <p v-if="career">当前选择：<strong>{{ career }}</strong> ｜ 模式：{{ mode }}</p>
                <p v-else>请先在上方选择目标岗位</p>
              </div>
              <div class="setup-action">
                <div class="count-select">
                  <span class="filter-label" style="margin-bottom:4px">题目数量</span>
                  <el-select v-model="questionCount" style="width:120px">
                    <el-option label="5题" :value="5" />
                    <el-option label="10题" :value="10" />
                    <el-option label="15题" :value="15" />
                    <el-option label="20题" :value="20" />
                  </el-select>
                </div>
                <button class="btn-primary" @click="beginAnswering" :disabled="!career || !totalQuestions">
                  <Crosshair :size="16" class="icon-blue" /> 开始作答
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 答题中 -->
        <div v-if="practicePhase === 'doing'" class="practice-doing">
          <!-- 顶部状态栏 -->
          <div class="answer-statusbar">
            <div class="status-left">
              <span class="status-progress">{{ currentIdx + 1 }} / {{ questions.length }}</span>
              <span class="status-mode">{{ mode }}</span>
              <span class="status-timer" v-if="timerRunning"><Timer :size="16" class="icon-blue" /> {{ formatTime(elapsedSeconds) }}</span>
            </div>
            <div class="status-right">
              <span class="status-accuracy"><Check :size="16" class="icon-blue" /> {{ correctCount }}/{{ answeredCount }}</span>
              <button class="btn-outline" style="padding:4px 12px;font-size:0.8rem;color:var(--accent)" @click="confirmEndPractice"><StopCircle :size="16" class="icon-blue" /> 结束</button>
            </div>
          </div>

          <!-- 题目卡片 -->
          <div class="card" style="padding:18px 20px;margin-bottom:12px" v-if="currentQuestion">
            <div class="q-header">
              <span class="q-number">#{{ currentIdx + 1 }}</span>
              <span :class="['tag-pill', 'tag-pill-' + (currentQuestion.question_type === 'judge' ? 'green' : currentQuestion.question_type === 'multi_choice' || currentQuestion.question_type === 'multi' ? 'orange' : 'blue')]">
                {{ typeLabel(currentQuestion.question_type) }}
              </span>
              <span :class="['tag-pill', currentQuestion.difficulty === 'easy' ? 'tag-pill-green' : currentQuestion.difficulty === 'hard' ? 'tag-pill-red' : 'tag-pill-orange']">
                {{ diffLabel(currentQuestion.difficulty) }}
              </span>
              <span class="q-kp" v-if="currentQuestion.knowledge_point">{{ currentQuestion.knowledge_point }}</span>
              <div class="q-header-actions">
                <button class="btn-outline" style="padding:2px 10px;font-size:0.78rem" :class="{ 'is-warning': isSaved(currentQuestion) }" @click="toggleSave(currentQuestion)">
                  <Star :size="16" class="icon-blue" :class="[isSaved(currentQuestion) ? 'fas' : 'far', 'fa-star']" />
                  {{ isSaved(currentQuestion) ? '已收藏' : '收藏' }}
                </button>
                <button class="btn-outline" style="padding:2px 10px;font-size:0.78rem;color:var(--accent)" v-if="isHard(currentQuestion)" @click="toggleHard(currentQuestion)">
                  <Circle :size="16" :color="'var(--accent)'" /> 已标难
                </button>
                <button class="btn-outline" style="padding:2px 10px;font-size:0.78rem" v-else @click="toggleHard(currentQuestion)">
                  <Circle :size="16" class="icon-blue" /> 标难
                </button>
              </div>
            </div>

            <div class="q-content">
              <div class="q-stem">{{ currentQuestion.question }}</div>
              <div v-if="currentQuestion.question_type !== 'judge'" class="q-options">
                <div v-for="(opt, oi) in optionsList" :key="oi"
                  :class="['q-option', {
                    selected: selectedAnswer === opt.label,
                    correct: answered && opt.label === currentQuestion.answer,
                    wrong: answered && selectedAnswer === opt.label && opt.label !== currentQuestion.answer
                  }]"
                  @click="!answered && selectAnswer(opt.label)">
                  <span class="opt-label">{{ opt.label }}</span>
                  <span class="opt-text">{{ opt.text }}</span>
                </div>
              </div>
              <div v-else class="q-options judge-options">
                <div v-for="val in ['对', '错']" :key="val"
                  :class="['q-option', {
                    selected: selectedAnswer === val,
                    correct: answered && val === currentQuestion.answer,
                    wrong: answered && selectedAnswer === val && val !== currentQuestion.answer
                  }]"
                  @click="!answered && selectAnswer(val)">
                  <span class="opt-text">{{ val }}</span>
                </div>
              </div>
            </div>

            <!-- 解析区 -->
            <transition name="fade">
              <div v-if="answered" class="q-analysis">
                <el-divider />
                <div class="analysis-header">
                  <span v-if="isCorrect" class="result-correct"><CheckCircle :size="16" class="icon-blue" /> 回答正确！</span>
                  <span v-else class="result-wrong"><XCircle :size="16" class="icon-blue" /> 回答错误</span>
                  <span class="correct-answer" v-if="!isCorrect">正确答案：<strong>{{ currentQuestion.answer }}</strong></span>
                </div>
                <div class="analysis-body" v-if="currentQuestion.analysis">
                  <div class="analysis-title"><BookOpen :size="16" class="icon-blue" /> 解析</div>
                  <p>{{ currentQuestion.analysis }}</p>
                </div>
                <!-- 个人笔记 -->
                <div class="note-area">
                  <el-input v-model="noteText" placeholder="记笔记..." size="small" style="width:100%;margin-top:8px">
                    <template #prefix><Pen :size="16" class="icon-blue" /></template>
                  </el-input>
                </div>
              </div>
            </transition>

            <!-- 导航按钮 -->
            <div class="q-nav" v-if="answered">
              <button class="btn-outline" @click="prevQuestion" :disabled="currentIdx === 0"><ArrowLeft :size="16" class="icon-blue" /> 上一题</button>
              <button v-if="currentIdx < questions.length - 1" class="btn-primary" @click="nextQuestion">
                下一题 <ArrowRight :size="16" class="icon-blue" />
              </button>
              <button v-else class="btn-primary" style="background:var(--primary)" @click="finishPractice"><BarChart :size="16" class="icon-blue" /> 查看报告</button>
            </div>
          </div>

          <!-- 题目缩略图导航 -->
          <div class="question-thumbnails" v-if="questions.length > 5">
            <div v-for="(q, i) in questions" :key="q.id || i"
              :class="['thumb-item', {
                active: i === currentIdx,
                correct: q._answered && q._correct,
                wrong: q._answered && !q._correct,
                skipped: q._answered === false,
                current: i === currentIdx
              }]"
              @click="goToQuestion(i)">
              {{ i + 1 }}
            </div>
          </div>
        </div>

        <!-- 报告 -->
        <div v-if="practicePhase === 'report'" class="practice-report">
          <div class="card" style="padding:24px 20px;text-align:center">
            <div class="report-icon"><BarChart :size="3" :color="'var(--primary)'" /></div>
            <div class="section-header" style="justify-content:center;margin-bottom:20px;padding:0">
              <div class="section-title" style="font-size:1.2rem">练习报告</div>
            </div>
            <p class="report-subtitle" style="color:var(--text-muted);font-size:0.85rem;margin:-10px 0 20px">{{ career }} · {{ mode }} · {{ formatDate(reportDate) }}</p>
            <div class="report-stats">
              <div class="report-stat-card">
                <div class="stat-num" :style="{ color: reportAccuracy > 70 ? 'var(--primary)' : reportAccuracy > 40 ? 'var(--accent)' : 'var(--accent)' }">
                  {{ reportAccuracy }}%
                </div>
                <div class="stat-label">正确率</div>
              </div>
              <div class="report-stat-card">
                <div class="stat-num">{{ reportCorrect }}/{{ reportTotal }}</div>
                <div class="stat-label">答对/总数</div>
              </div>
              <div class="report-stat-card">
                <div class="stat-num">{{ formatTime(reportTime) }}</div>
                <div class="stat-label">用时</div>
              </div>
            </div>
            <div class="report-detail" v-if="reportErrors.length > 0">
              <h3 style="font-size:0.95rem;margin-bottom:10px"><X :size="16" :color="'var(--accent)'" /> 错题回顾</h3>
              <div v-for="(e, i) in reportErrors" :key="i" class="report-error-item">
                <div class="re-q">{{ i + 1 }}. {{ e.question }}</div>
                <div class="re-answer">你的答案：<span class="wrong-text">{{ e.userAnswer }}</span></div>
                <div class="re-answer">正确答案：<span class="correct-text">{{ e.correctAnswer }}</span></div>
              </div>
            </div>
            <div class="report-actions" style="margin-top:20px">
              <button class="btn-outline" @click="resetPractice"><RotateCw :size="16" class="icon-blue" /> 再来一次</button>
              <button class="btn-primary" @click="goToWrongTab"><Book :size="16" class="icon-blue" /> 查看错题本</button>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <!-- ─── Tab 2: 错题本 ─── -->
      <el-tab-pane name="wrong">
        <template #label>
          <span><Book :size="16" class="icon-blue" /> 错题本</span>
        </template>
        <div class="wrong-section" v-loading="wrongLoading">
          <div class="filter-bar" style="background:var(--bg-card);padding:14px 16px;border-radius:var(--radius-md);border:1px solid var(--border);margin-bottom:16px">
            <div style="display:flex;flex-wrap:wrap;gap:10px;width:100%">
              <div class="filter-group" style="flex:1;min-width:160px">
                <span class="filter-label"><Briefcase :size="16" class="icon-blue" /> 岗位</span>
                <el-select v-model="wrongCareerFilter" placeholder="全部岗位" clearable style="width:100%" @change="fetchWrong">
                  <el-option label="全部岗位" value="" />
                  <el-option v-for="c in allCareerNames" :key="c" :label="c" :value="c" />
                </el-select>
              </div>
              <div class="filter-group" style="flex:1;min-width:120px">
                <span class="filter-label"><Flag :size="16" class="icon-blue" /> 状态</span>
                <el-select v-model="wrongMasteredFilter" placeholder="全部" clearable style="width:100%" @change="fetchWrong">
                  <el-option label="全部" value="" />
                  <el-option label="未掌握" value="0" />
                  <el-option label="已掌握" value="1" />
                </el-select>
              </div>
            </div>
          </div>
          <div class="empty-state" v-if="wrongQuestions.length === 0">
            <div class="empty-icon"><Smile :size="16" class="icon-blue" /></div>
            <p>太棒了，没有错题！</p>
          </div>
          <div v-for="wq in wrongQuestions" :key="wq.id" class="wrong-item">
            <div class="wi-header">
              <span class="wi-source"><Briefcase :size="16" class="icon-blue" /> {{ wq.career || '笔试' }}</span>
              <span :class="['tag-pill', wq.difficulty === 'easy' ? 'tag-pill-green' : wq.difficulty === 'hard' ? 'tag-pill-red' : 'tag-pill-orange']">{{ diffLabel(wq.difficulty) }}</span>
              <span class="wi-status" :class="{ mastered: wq.mastered }">
                <CheckCircle :size="16" class="icon-blue" :class="[wq.mastered ? 'fas fa-check-circle' : 'fas fa-xmark-circle']" />
                {{ wq.mastered ? '已掌握' : '未掌握' }}
              </span>
              <button class="btn-outline" style="margin-left:auto;padding:2px 10px;font-size:0.78rem" @click="reviewWrong(wq)"><RotateCw :size="16" class="icon-blue" /> 重做</button>
            </div>
            <div class="wi-question">{{ wq.question }}</div>
            <div class="wi-answers">
              <span class="wi-wrong"><X :size="16" class="icon-blue" /> 你的答案：<strong>{{ wq.user_answer }}</strong></span>
              <span class="wi-correct"><Check :size="16" class="icon-blue" /> 正确答案：<strong>{{ wq.correct_answer }}</strong></span>
            </div>
            <div class="wi-actions" style="margin-top:8px;display:flex;gap:8px">
              <button class="btn-outline" style="padding:2px 10px;font-size:0.78rem;color:var(--primary)" @click="markMastered(wq)" v-if="!wq.mastered"><CheckCircle :size="16" class="icon-blue" /> 标记已掌握</button>
              <button class="btn-outline" style="padding:2px 10px;font-size:0.78rem;color:var(--accent)" @click="removeWrong(wq)"><Trash2 :size="16" class="icon-blue" /> 移除</button>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <!-- ─── Tab 3: 收藏夹 ─── -->
      <el-tab-pane name="saved">
        <template #label>
          <span><Star :size="16" class="icon-blue" /> 收藏夹</span>
        </template>
        <div class="saved-section" v-loading="savedLoading">
          <div class="filter-bar" style="background:var(--bg-card);padding:14px 16px;border-radius:var(--radius-md);border:1px solid var(--border);margin-bottom:16px">
            <div style="display:flex;flex-wrap:wrap;gap:10px;width:100%;align-items:center">
              <div class="filter-group" style="flex:1;min-width:160px">
                <span class="filter-label"><Briefcase :size="16" class="icon-blue" /> 岗位</span>
                <el-select v-model="savedCareerFilter" placeholder="全部岗位" clearable style="width:100%" @change="fetchSaved">
                  <el-option label="全部岗位" value="" />
                  <el-option v-for="c in allCareerNames" :key="c" :label="c" :value="c" />
                </el-select>
              </div>
              <span class="saved-total" style="font-size:0.82rem;color:var(--text-muted)" v-if="savedQuestions.length > 0">共 {{ savedQuestions.length }} 题</span>
            </div>
          </div>
          <div class="empty-state" v-if="savedQuestions.length === 0">
            <div class="empty-icon"><Star :size="16" class="icon-blue" /></div>
            <p>还没有收藏题目，刷题时点收藏按钮即可</p>
          </div>
          <div v-for="sq in savedQuestions" :key="sq.id" class="saved-item">
            <div class="si-header">
              <span class="si-source"><Briefcase :size="16" class="icon-blue" /> {{ sq.career || '笔试' }}</span>
              <span :class="['tag-pill', sq.difficulty === 'easy' ? 'tag-pill-green' : sq.difficulty === 'hard' ? 'tag-pill-red' : 'tag-pill-orange']">{{ diffLabel(sq.difficulty) }}</span>
              <button class="btn-outline" style="margin-left:auto;padding:2px 10px;font-size:0.78rem;color:var(--accent)" @click="removeSaved(sq)"><Trash2 :size="16" class="icon-blue" /> 取消收藏</button>
            </div>
            <div class="si-question">{{ sq.question }}</div>
            <div class="si-note" v-if="sq.note"><Pen :size="16" class="icon-blue" /> 备注：{{ sq.note }}</div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- ═══════ 4. 详细数据分析（折叠面板） ═══════ -->
    <div class="detail-collapse-wrap">
      <el-collapse v-model="detailCollapseOpen" class="detail-collapse" @change="onDetailCollapseChange">
        <el-collapse-item title="详细数据分析（雷达图/错题分布/时段分析/成长对比）" name="stats">
          <template #title>
            <span style="font-weight:600"><BarChart :size="16" class="icon-blue" style="margin-right:8px" /> 详细数据分析（雷达图/错题分布/时段分析/成长对比）</span>
          </template>
          <div class="detail-stats-section">
            <!-- 趋势图 + 雷达图并列 -->
            <div class="chart-row-2">
              <div class="card" style="padding:0">
                <div class="chart-header" style="padding:12px 16px;border-bottom:1px solid var(--border-light)">
                  <span><ChartLine :size="16" class="icon-blue" /> 刷题量趋势</span>
                  <el-radio-group v-model="trendDays" size="small" @change="fetchTrend">
                    <el-radio-button :value="7">近7日</el-radio-button>
                    <el-radio-button :value="30">近30日</el-radio-button>
                  </el-radio-group>
                </div>
                <div class="chart-body" style="padding:10px 16px 16px">
                  <svg :viewBox="'0 0 ' + trendSvgWidth + ' 220'" class="trend-svg" v-if="trendData.length > 0">
                    <line v-for="gy in gridY" :key="gy" :x1="paddingLeft" :y1="gy" :x2="trendSvgWidth - 20" :y2="gy" stroke="var(--border-light)" stroke-width="1" />
                    <path :d="trendAreaPath" fill="rgba(61,90,128,0.1)" stroke="none" />
                    <path :d="trendLinePath" fill="none" stroke="var(--primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
                    <circle v-for="(pt, pi) in trendPoints" :key="pi" :cx="pt.x" :cy="pt.y" r="4"
                      fill="var(--primary)" stroke="white" stroke-width="2"
                      @mouseenter="trendHover = pi" @mouseleave="trendHover = -1"
                      @click="showDayDetail(trendData[pi])" style="cursor:pointer" />
                    <g v-if="trendHover >= 0 && trendHover < trendData.length">
                      <rect :x="trendPoints[trendHover].x - 50" :y="trendPoints[trendHover].y - 38" width="100" height="30" rx="4" fill="#333" />
                      <text :x="trendPoints[trendHover].x" :y="trendPoints[trendHover].y - 18" fill="white" font-size="11" text-anchor="middle">{{ trendData[trendHover].questions }}题 / {{ trendData[trendHover].accuracy }}%</text>
                    </g>
                    <text v-for="(pt, pi) in trendPoints" :key="'xl-' + pi"
                      v-show="trendData.length <= 7 || pi % Math.ceil(trendData.length / 7) === 0"
                      :x="pt.x" :y="210" fill="var(--text-muted)" font-size="10" text-anchor="middle">{{ trendData[pi].date.slice(5) }}</text>
                  </svg>
                  <div v-else class="empty-state"><p>暂无趋势数据，先去刷题吧！</p></div>
                </div>
              </div>

              <div class="card" style="padding:0">
                <div class="chart-header" style="padding:12px 16px;border-bottom:1px solid var(--border-light)">
                  <span><Network :size="16" class="icon-blue" /> 能力分析</span>
                  <el-select v-model="radarCareer" size="small" placeholder="选择岗位" clearable style="width:140px" @change="fetchRadar">
                    <el-option v-for="c in allCareerNames" :key="c" :label="c" :value="c" />
                  </el-select>
                </div>
                <div class="chart-body radar-body" style="padding:10px 16px">
                  <svg :viewBox="'0 0 280 280'" class="radar-svg" v-if="radarData.length > 0">
                    <polygon :points="radarGridPoints(0.25)" fill="var(--bg-hover)" stroke="var(--border-light)" stroke-width="1" />
                    <polygon :points="radarGridPoints(0.5)" fill="#f0f0ff" stroke="var(--border-light)" stroke-width="1" />
                    <polygon :points="radarGridPoints(0.75)" fill="#ebebff" stroke="var(--border-light)" stroke-width="1" />
                    <polygon :points="radarGridPoints(1.0)" fill="none" stroke="var(--border)" stroke-width="1" />
                    <polygon :points="radarDataPoints" fill="rgba(61,90,128,0.25)" stroke="var(--primary)" stroke-width="2" />
                    <circle v-for="(rd, ri) in radarData" :key="ri" :cx="radarPoint(ri)[0]" :cy="radarPoint(ri)[1]" r="3.5" fill="var(--primary)" stroke="white" stroke-width="2"
                      @mouseenter="radarHover = ri" @mouseleave="radarHover = -1" />
                    <text v-for="(rd, ri) in radarData" :key="'rl-' + ri" :x="radarLabelPoint(ri)[0]" :y="radarLabelPoint(ri)[1]"
                      fill="var(--text-body)" font-size="10" text-anchor="middle" dominant-baseline="central">{{ rd.name.length > 6 ? rd.name.slice(0, 6) + '..' : rd.name }}</text>
                    <g v-if="radarHover >= 0 && radarHover < radarData.length">
                      <rect :x="radarLabelPoint(radarHover)[0] - 40" :y="radarLabelPoint(radarHover)[1] - 8" width="80" height="20" rx="4" fill="#333" />
                      <text :x="radarLabelPoint(radarHover)[0]" :y="radarLabelPoint(radarHover)[1] + 4" fill="white" font-size="10" text-anchor="middle">{{ radarData[radarHover].mastery }}%掌握</text>
                    </g>
                  </svg>
                  <div v-else class="empty-state"><p>暂无能力数据<br/>刷题后自动生成分析</p></div>
                </div>
              </div>
            </div>

            <!-- 错题分布 + 时段分析 -->
            <div class="chart-row-2">
              <div class="card" style="padding:0">
                <div class="chart-header" style="padding:12px 16px;border-bottom:1px solid var(--border-light)">
                  <span><X :size="16" :color="'var(--accent)'" /> 错题分布（按知识点）</span>
                </div>
                <div class="chart-body bar-body" style="padding:10px 16px" v-if="errorDistData.length > 0">
                  <div v-for="(ed, ei) in errorDistData.slice(0, 8)" :key="ei" class="bar-item" @click="goToWrongWithKp(ed.name)" style="cursor:pointer">
                    <div class="bar-label" :title="ed.name">{{ ed.name.length > 8 ? ed.name.slice(0, 8) + '..' : ed.name }}</div>
                    <div class="bar-track"><div class="bar-fill" :style="{ width: barPercent(ed.count) + '%' }"></div></div>
                    <div class="bar-value">{{ ed.count }}</div>
                  </div>
                  <div v-if="errorDistData.length > 8" class="show-all-wrong" @click="goToWrongTab">查看全部 {{ errorDistData.length }} 个知识点 <ArrowRight :size="16" class="icon-blue" /></div>
                </div>
                <div v-else class="empty-state" style="padding:30px 0"><p>暂无错题数据</p></div>
              </div>

              <div class="card" style="padding:0">
                <div class="chart-header" style="padding:12px 16px;border-bottom:1px solid var(--border-light)">
                  <span><Clock :size="16" class="icon-blue" /> 练习时段分布</span>
                </div>
                <div class="chart-body pie-body" style="padding:10px 16px" v-if="timeDistData.length > 0">
                  <svg :viewBox="'0 0 280 200'" class="pie-svg">
                    <g v-for="(td, ti) in timeDistData" :key="ti">
                      <path :d="pieSlice(ti)" :fill="pieColors[ti % pieColors.length]" stroke="white" stroke-width="2"
                        @mouseenter="pieHover = ti" @mouseleave="pieHover = -1" style="cursor:pointer" />
                    </g>
                    <text x="140" y="85" text-anchor="middle" font-size="22" font-weight="700" fill="var(--text-heading)">{{ totalTimeDist }}</text>
                    <text x="140" y="102" text-anchor="middle" font-size="11" fill="var(--text-muted)">总题量</text>
                  </svg>
                  <div class="pie-legend">
                    <div v-for="(td, ti) in timeDistData" :key="'l-' + ti" class="legend-item"
                      @mouseenter="pieHover = ti" @mouseleave="pieHover = -1">
                      <span class="legend-dot" :style="{ background: pieColors[ti % pieColors.length] }"></span>
                      <span class="legend-label">{{ td.name }}</span>
                      <span class="legend-value">{{ td.value }}题</span>
                      <span class="legend-pct">({{ piePercent(td.value) }}%)</span>
                    </div>
                  </div>
                </div>
                <div v-else class="empty-state" style="padding:30px 0"><p>暂无练习记录</p></div>
              </div>
            </div>

            <!-- 成长对比 -->
            <div class="card" style="padding:0">
              <div class="chart-header" style="padding:12px 16px;border-bottom:1px solid var(--border-light)">
                <span><BarChart :size="16" class="icon-blue" /> 成长对比</span>
              </div>
              <div class="growth-body" style="padding:16px" v-if="growthData.this_week">
                <div class="growth-comparison">
                  <div class="growth-column" v-if="growthData.last_week">
                    <div class="gw-label">上周</div>
                    <div class="gw-value">{{ growthData.last_week.questions }}题</div>
                    <div class="gw-accuracy">{{ growthData.last_week.accuracy }}%</div>
                  </div>
                  <div class="growth-vs">
                    <div class="vs-arrow" :class="growthArrowClass"><ArrowUp :size="16" class="icon-blue" :class="['fas', growthArrowClass === 'up' ? 'fa-arrow-up' : growthArrowClass === 'down' ? 'fa-arrow-down' : 'fa-minus']" /></div>
                    <div class="vs-text" :class="growthArrowClass">{{ growthChangeText }}</div>
                  </div>
                  <div class="growth-column this-week">
                    <div class="gw-label">本周</div>
                    <div class="gw-value">{{ growthData.this_week.questions }}题</div>
                    <div class="gw-accuracy">{{ growthData.this_week.accuracy }}%</div>
                  </div>
                </div>
                <div class="growth-detail" v-if="growthData.this_week.questions > 0 || growthData.last_week.questions > 0">
                  <div class="gd-row">
                    <span class="gd-label">刷题量变化</span>
                    <span class="gd-value" :class="growthData.change.questions >= 0 ? 'up' : 'down'">{{ growthData.change.questions >= 0 ? '+' : '' }}{{ growthData.change.questions }}题 ({{ growthData.change.questions_percent }}%)</span>
                  </div>
                  <div class="gd-row">
                    <span class="gd-label">正确率变化</span>
                    <span class="gd-value" :class="growthData.change.accuracy >= 0 ? 'up' : 'down'">{{ growthData.change.accuracy >= 0 ? '+' : '' }}{{ growthData.change.accuracy }}%</span>
                  </div>
                </div>
              </div>
              <div v-else class="empty-state" style="padding:30px 0"><p>暂无跨周数据</p></div>
            </div>
          </div>
        </el-collapse-item>
      </el-collapse>
    </div>

    <!-- ═══════ 5. 新手指引浮层 ═══════ -->
    <transition name="guide-fade">
      <div class="guide-overlay" v-if="showGuide" @click="dismissGuide">
        <div class="guide-card">
          <div class="guide-close" @click.stop="dismissGuide"><X :size="16" class="icon-blue" /></div>
          <div class="guide-title"><Crosshair :size="16" class="icon-blue" /> 欢迎来到笔试练习</div>
          <div class="guide-body">
            <div class="guide-step">
              <span class="guide-num">1</span>
              <span>上方筛选区选择<strong>岗位和模式</strong>，点击「开始刷题」</span>
            </div>
            <div class="guide-step">
              <span class="guide-num">2</span>
              <span><strong>练习统计看板</strong>实时展示刷题量、正确率、连续打卡</span>
            </div>
            <div class="guide-step">
              <span class="guide-num">3</span>
              <span>展开下方<strong>详细数据分析</strong>，看雷达图、错题分布和成长趋势</span>
            </div>
          </div>
          <div class="guide-btn" @click.stop="dismissGuide">我明白了，开始练习 <ArrowRight :size="16" class="icon-blue" /></div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useCareerStore } from '../stores/career.js'
import { ElMessage, ElMessageBox } from 'element-plus'
import PageBanner from '../components/PageBanner.vue'

const router = useRouter()
const store = useCareerStore()

// ─── 状态变量 ───
const activeTab = ref('practice')
const career = ref('')
const mode = ref('专项练习')
const difficulty = ref('all')
const questionType = ref('all')
const searchKeyword = ref('')
const questionCount = ref(10)
const practicePhase = ref('setup')  // setup | doing | report
const questions = ref([])
const currentIdx = ref(0)
const selectedAnswer = ref('')
const answered = ref(false)
const isCorrect = ref(false)
const noteText = ref('')
const loading = ref(false)
const loadingAI = ref(false)

// 计时器
const timerRunning = ref(false)
const elapsedSeconds = ref(0)
let timerInterval = null

// 报告
const reportDate = ref('')
const reportAccuracy = ref(0)
const reportCorrect = ref(0)
const reportTotal = ref(0)
const reportTime = ref(0)
const reportErrors = ref([])

// 统计
const statsLoading = ref(false)
const statsData = ref({ total_questions: 0, avg_accuracy: 0, streak_days: 0, total_hours: 0, total_minutes: 0 })
const trendDays = ref(7)
const trendData = ref([])
const trendHover = ref(-1)
const radarData = ref([])
const radarCareer = ref('')
const radarHover = ref(-1)
const errorDistData = ref([])
const timeDistData = ref([])
const growthData = ref({ this_week: null, last_week: null, change: {} })
const pieHover = ref(-1)
const allCareerNames = ref([])

// 错题本
const wrongLoading = ref(false)
const wrongQuestions = ref([])
const wrongCareerFilter = ref('')
const wrongMasteredFilter = ref('')

// 收藏夹
const savedLoading = ref(false)
const savedQuestions = ref([])
const savedCareerFilter = ref('')

// 硬题标记（localStorage 存 ID 列表）
let hardSet
try {
  const raw = localStorage.getItem('exam_hard_ids')
  const parsed = raw ? JSON.parse(raw) : []
  hardSet = Array.isArray(parsed) ? new Set(parsed) : new Set()
} catch { hardSet = new Set() }
const hardQuestions = ref(hardSet)

// ═══════ 数据看板 ═══════
const dashData = reactive({
  totalQuestions: 0,
  weekAccuracy: 0,
  streakDays: 0,
  weekCompletion: 0,
  weekDone: 0,
  weekGoal: 7
})
const dashHover = ref(-1)
const dashTrendData = ref([])
const isStuck = ref(false)
const showGuide = ref(false)
const detailCollapseOpen = ref('')

// 新手指引
function checkGuide() {
  const seen = localStorage.getItem('exam_guide_done')
  if (!seen) { showGuide.value = true }
}
function dismissGuide() {
  showGuide.value = false
  localStorage.setItem('exam_guide_done', '1')
}

// 加载看板数据
async function loadDashboard() {
  try {
    const [overview, trend, errorDist] = await Promise.all([
      axios.get('/api/exam/stats/overview').then(r => r.data),
      axios.get('/api/exam/stats/trend', { params: { days: 7 } }).then(r => r.data),
      axios.get('/api/exam/stats/error-distribution').then(r => r.data),
    ])
    // 更新看板
    dashData.totalQuestions = overview.total_questions || 0
    dashData.weekAccuracy = overview.avg_accuracy || 0
    dashData.streakDays = overview.streak_days || 0
    // 本周完成率 = 本周已练天数 / 7
    const grow = await axios.get('/api/exam/stats/growth').then(r => r.data).catch(() => null)
    if (grow && grow.this_week) {
      dashData.weekDone = Math.min(grow.this_week.days || 0, 7)
      dashData.weekGoal = 7
      dashData.weekCompletion = Math.round((dashData.weekDone / 7) * 100)
    } else {
      dashData.weekDone = 0
      dashData.weekCompletion = 0
    }
    // 趋势数据
    dashTrendData.value = (trend.trend || []).slice(-7)
    // 本周完成天数：从趋势数据中统计最近7天有刷题的天数
    const weekDaysWithPractice = dashTrendData.value.filter(d => (d.questions || 0) > 0).length
    dashData.weekDone = Math.min(weekDaysWithPractice, 7)
    dashData.weekGoal = 7
    dashData.weekCompletion = Math.round((weekDaysWithPractice / 7) * 100)
    // 薄弱模块
    if (errorDist.distribution && errorDist.distribution.length > 0) {
      const top3 = errorDist.distribution.slice(0, 3).map(d => d.name)
      dashWeakModules.value = top3.join('、')
    }
  } catch { /* ignore */ }
}

// 薄弱模块
const dashWeakModules = ref('')

// ═══════ 计算属性 ═══════

const paddingLeft = 40
const trendSvgWidth = computed(() => Math.max(400, trendData.value.length * 40 + 60))

const gridY = computed(() => {
  const ys = []
  for (let y = 30; y <= 190; y += 40) ys.push(y)
  return ys
})

const trendPoints = computed(() => {
  if (!trendData.value.length) return []
  const maxQ = Math.max(...trendData.value.map(d => d.questions), 1)
  const w = trendSvgWidth.value - paddingLeft - 20
  const step = trendData.value.length > 1 ? w / (trendData.value.length - 1) : w / 2
  return trendData.value.map((d, i) => ({
    x: paddingLeft + i * step,
    y: 185 - (d.questions / maxQ) * 150
  }))
})

const trendLinePath = computed(() => {
  if (trendPoints.value.length < 2) return ''
  return trendPoints.value.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x},${p.y}`).join(' ')
})

const trendAreaPath = computed(() => {
  if (trendPoints.value.length < 2) return ''
  const pts = trendPoints.value
  let d = pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x},${p.y}`).join(' ')
  d += ` L${pts[pts.length - 1].x},185 L${pts[0].x},185 Z`
  return d
})

function radarPointAngle(idx, total) {
  const angle = (Math.PI * 2 * idx) / total - Math.PI / 2
  return angle
}

const radarCenter = [140, 135]
const radarRadius = 95

function radarGridPoints(scale) {
  if (!radarData.value.length) return ''
  return radarData.value.map((_, i) => {
    const angle = radarPointAngle(i, radarData.value.length)
    const x = radarCenter[0] + radarRadius * scale * Math.cos(angle)
    const y = radarCenter[1] + radarRadius * scale * Math.sin(angle)
    return `${x.toFixed(1)},${y.toFixed(1)}`
  }).join(' ')
}

const radarDataPoints = computed(() => {
  if (!radarData.value.length) return ''
  return radarData.value.map((rd, i) => {
    const angle = radarPointAngle(i, radarData.value.length)
    const scale = Math.min(rd.mastery / 100, 1)
    const x = radarCenter[0] + radarRadius * scale * Math.cos(angle)
    const y = radarCenter[1] + radarRadius * scale * Math.sin(angle)
    return `${x.toFixed(1)},${y.toFixed(1)}`
  }).join(' ')
})

function radarPoint(idx) {
  const angle = radarPointAngle(idx, radarData.value.length)
  const scale = Math.min(radarData.value[idx].mastery / 100, 1)
  return [
    radarCenter[0] + radarRadius * scale * Math.cos(angle),
    radarCenter[1] + radarRadius * scale * Math.sin(angle)
  ]
}

function radarLabelPoint(idx) {
  const angle = radarPointAngle(idx, radarData.value.length)
  return [
    radarCenter[0] + (radarRadius + 25) * Math.cos(angle),
    radarCenter[1] + (radarRadius + 25) * Math.sin(angle)
  ]
}

// 饼图
const pieColors = ['#3D5A80', '#67c23a', '#C85A20', '#B54E1A', '#8EA0B8', '#54759C']
const totalTimeDist = computed(() => timeDistData.value.reduce((s, d) => s + d.value, 0))

// 环形进度条
const circumference = Math.PI * 32  // r=16 → 2*PI*16 = 100.53
const ringOffset = computed(() => {
  const pct = Math.min(dashData.weekAccuracy, 100)
  return circumference - (circumference * pct / 100)
})

// 看板迷你趋势折线
const dashTrendPath = computed(() => {
  const data = dashTrendData.value
  if (data.length < 2) return ''
  const maxQ = Math.max(...data.map(d => d.questions), 1)
  const w = data.length > 1 ? 98 / (data.length - 1) : 49
  const pts = data.map((d, i) => ({
    x: 1 + i * w,
    y: 34 - (d.questions / maxQ) * 28
  }))
  return pts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ')
})

function piePercent(val) {
  return totalTimeDist.value > 0 ? ((val / totalTimeDist.value) * 100).toFixed(1) : '0'
}

function pieSlice(idx) {
  const total = totalTimeDist.value
  if (total === 0) return ''
  let startAngle = 0
  for (let i = 0; i < idx; i++) {
    startAngle += (timeDistData.value[i].value / total) * 360
  }
  const sliceAngle = (timeDistData.value[idx].value / total) * 360
  const startRad = (startAngle - 90) * Math.PI / 180
  const endRad = (startAngle + sliceAngle - 90) * Math.PI / 180
  const r = 70
  const cx = 140, cy = 72
  const x1 = cx + r * Math.cos(startRad)
  const y1 = cy + r * Math.sin(startRad)
  const x2 = cx + r * Math.cos(endRad)
  const y2 = cy + r * Math.sin(endRad)
  const large = sliceAngle > 180 ? 1 : 0
  return `M${cx},${cy} L${x1.toFixed(1)},${y1.toFixed(1)} A${r},${r} 0 ${large} 1 ${x2.toFixed(1)},${y2.toFixed(1)} Z`
}

// 错题分布柱状图最大值
const maxErrorCount = computed(() => Math.max(...errorDistData.value.map(d => d.count), 1))

function barPercent(count) {
  return (count / maxErrorCount.value) * 100
}

// 题库预览
const libraryStats = computed(() => {
  const total = questions.value.length
  const est = Math.ceil(total * 1.5)
  return { total, estimatedTime: est, historyAccuracy: statsData.value.avg_accuracy }
})

// 当前题目
const currentQuestion = computed(() => questions.value[currentIdx.value] || null)
const optionsList = computed(() => {
  if (!currentQuestion.value) return []
  try {
    return typeof currentQuestion.value.options_json === 'string'
      ? JSON.parse(currentQuestion.value.options_json)
      : currentQuestion.value.options_json || []
  } catch { return [] }
})
const answeredCount = computed(() => questions.value.filter(q => q._answered).length)
const correctCount = computed(() => questions.value.filter(q => q._correct).length)

// ═══════ 方法 ═══════

function typeLabel(t) {
  const map = { single_choice: '单选题', multi_choice: '多选题', judge: '判断题', single: '单选题', multi: '多选题' }
  return map[t] || t || '未知'
}

function diffLabel(d) {
  const map = { easy: '入门', medium: '基础', hard: '进阶' }
  return map[d] || d || '未知'
}

function formatTime(sec) {
  const m = Math.floor(sec / 60)
  const s = sec % 60
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
}

function formatDate(d) {
  if (!d) return ''
  try { return new Date(d).toLocaleDateString('zh-CN') } catch { return d }
}

// ─── 题库加载 ───

async function loadQuestions() {
  if (!career.value) return
  loading.value = true
  try {
    const params = { career: career.value }
    if (difficulty.value !== 'all') params.difficulty = difficulty.value
    if (questionType.value !== 'all') params.question_type = questionType.value
    const { data } = await axios.get('/api/exam/generate', { params })
    if (data.questions && data.questions.length > 0) {
      questions.value = data.questions.map(q => ({ ...q, _answered: false, _correct: false }))
    } else if (data.message && data.message.includes('AI')) {
      // AI自动补充
      ElMessage.info('AI正在生成题目，请稍候...')
      await loadQuestionsAI()
    } else {
      questions.value = []
      ElMessage.warning('暂无可用的题目')
    }
  } catch (e) {
    console.error('加载题库失败:', e)
    ElMessage.error('加载题库失败，请重试')
  } finally {
    loading.value = false
  }
}

async function loadQuestionsAI() {
  loadingAI.value = true
  try {
    const params = { career: career.value, count: questionCount.value, use_ai: true }
    const { data } = await axios.get('/api/exam/generate', { params })
    if (data.questions && data.questions.length > 0) {
      questions.value = data.questions.map(q => ({ ...q, _answered: false, _correct: false }))
      ElMessage.success('AI已生成题目！')
    } else {
      ElMessage.warning('AI暂无法生成题目')
    }
  } catch (e) {
    console.error('AI补题失败:', e)
    ElMessage.error('AI补题失败')
  } finally {
    loadingAI.value = false
  }
}

// 从断点恢复（localStorage 存上次进行中的练习）
function loadSession() {
  try {
    const saved = JSON.parse(localStorage.getItem('exam_practice_session'))
    if (saved && saved.career === career.value && saved.mode === mode.value) {
      questions.value = saved.questions || []
      currentIdx.value = saved.currentIdx || 0
      if (questions.value.some(q => q._answered)) {
        practicePhase.value = 'doing'
        ElMessage.info('已恢复上次练习进度')
        if (saved.elapsedSeconds) {
          elapsedSeconds.value = saved.elapsedSeconds
          startTimer()
        }
      }
    }
  } catch {}
}

function saveSession() {
  try {
    localStorage.setItem('exam_practice_session', JSON.stringify({
      career: career.value,
      mode: mode.value,
      questions: questions.value,
      currentIdx: currentIdx.value,
      elapsedSeconds: elapsedSeconds.value
    }))
  } catch {}
}

function clearSession() {
  localStorage.removeItem('exam_practice_session')
}

// ─── 答题流程 ───

function startPractice() {
  if (!career.value) return
  practicePhase.value = 'setup'
  loadQuestions().then(() => {
    loadSession()
  })
}

function beginAnswering() {
  if (questions.value.length === 0) { ElMessage.warning('当前筛选条件下没有题目'); return }
  practicePhase.value = 'doing'
  currentIdx.value = 0
  selectedAnswer.value = ''
  answered.value = false
  noteText.value = ''
  // 重新加载前一题没答的
  if (!questions.value[0]._answered) {
    resetTimer()
    startTimer()
  }
}

function selectAnswer(val) {
  selectedAnswer.value = val
  answered.value = true
  const q = currentQuestion.value
  // 判断对错
  if (q.question_type === 'multi_choice' || q.question_type === 'multi') {
    isCorrect.value = val.split('').sort().join('') === q.answer.split('').sort().join('')
  } else {
    isCorrect.value = val === q.answer
  }
  q._answered = true
  q._correct = isCorrect.value
  q._userAnswer = val
  noteText.value = q._note || ''
  saveSession()
}

function prevQuestion() {
  if (currentIdx.value > 0) {
    currentIdx.value--
    restoreQuestion()
  }
}

function nextQuestion() {
  if (currentIdx.value < questions.value.length - 1) {
    currentIdx.value++
    restoreQuestion()
  }
}

function goToQuestion(i) {
  currentIdx.value = i
  restoreQuestion()
}

function restoreQuestion() {
  const q = currentQuestion.value
  selectedAnswer.value = q._userAnswer || ''
  answered.value = q._answered || false
  isCorrect.value = q._correct || false
  noteText.value = q._note || ''
}

// 收藏/标硬
function isSaved(q) {
  return savedQuestions.value.some(s => s.question_id === q.id)
}

async function toggleSave(q) {
  if (isSaved(q)) {
    try {
      const sq = savedQuestions.value.find(s => s.question_id === q.id)
      if (sq) await axios.delete(`/api/exam/saved-questions/${sq.id}`)
      ElMessage.success('已取消收藏')
      fetchSaved()
    } catch { ElMessage.error('操作失败') }
  } else {
    try {
      await axios.post('/api/exam/saved-questions', {
        question_id: q.id,
        career: career.value,
        question: q.question,
        options_json: JSON.stringify(optionsList.value),
        source: career.value,
        difficulty: q.difficulty,
        note: noteText.value || ''
      })
      ElMessage.success('已收藏')
      fetchSaved()
    } catch { ElMessage.error('收藏失败') }
  }
}

function isHard(q) {
  return hardQuestions.value.has(q.id)
}

function toggleHard(q) {
  const set = hardQuestions.value
  if (set.has(q.id)) set.delete(q.id)
  else set.add(q.id)
  hardQuestions.value = new Set(set)
  localStorage.setItem('exam_hard_ids', JSON.stringify([...set]))
}

// 计时器
function startTimer() {
  timerRunning.value = true
  timerInterval = setInterval(() => { elapsedSeconds.value++ }, 1000)
}

function resetTimer() {
  timerRunning.value = false
  if (timerInterval) clearInterval(timerInterval)
  elapsedSeconds.value = 0
}

function stopTimer() {
  timerRunning.value = false
  if (timerInterval) clearInterval(timerInterval)
}

// 结束练习
function confirmEndPractice() {
  ElMessageBox.confirm('确定要结束本次练习吗？已答题目会记入记录。', '确认', {
    confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'
  }).then(() => finishPractice()).catch(() => {})
}

function finishPractice() {
  stopTimer()
  saveSession()
  const total = questions.value.length
  const correct = questions.value.filter(q => q._correct).length
  const wrong = total - correct
  const errors = questions.value.filter(q => q._answered && !q._correct).map(q => ({
    question: q.question,
    userAnswer: q._userAnswer || '',
    correctAnswer: q.answer
  }))

  reportTotal.value = total
  reportCorrect.value = correct
  reportAccuracy.value = total > 0 ? Math.round((correct / total) * 100) : 0
  reportTime.value = elapsedSeconds.value
  reportErrors.value = errors
  reportDate.value = new Date().toISOString()

  // 提交记录到后端
  submitRecord({ total, correct, wrong, errors })

  practicePhase.value = 'report'
  clearSession()
}

async function submitRecord(data) {
  try {
    await axios.post('/api/exam/record', {
      career: career.value,
      mode: mode.value,
      total_questions: data.total,
      correct_count: data.correct,
      wrong_count: data.wrong,
      accuracy: data.total > 0 ? Math.round(data.correct / data.total * 1000) / 10 : 0,
      duration_seconds: elapsedSeconds.value,
      // 记录每题详情
      answers_json: JSON.stringify(questions.value.filter(q => q._answered).map(q => ({
        id: q.id,
        answer: q._userAnswer || '',
        correct: q._correct
      })))
    })
  } catch (e) {
    console.error('提交记录失败:', e)
  }
}

function resetPractice() {
  practicePhase.value = 'setup'
  questions.value = []
  currentIdx.value = 0
  selectedAnswer.value = ''
  answered.value = false
  resetTimer()
}

function onCareerChange() {
  if (activeTab.value === 'practice') {
    loadQuestions()
  }
  fetchRadar()
  fetchErrorDist()
}

// ─── 统计 ───

async function fetchAllStats() {
  statsLoading.value = true
  try {
    const [overview, trend, errorDist, timeDist, growth] = await Promise.all([
      axios.get('/api/exam/stats/overview').then(r => r.data),
      axios.get('/api/exam/stats/trend', { params: { days: trendDays.value } }).then(r => r.data),
      axios.get('/api/exam/stats/error-distribution').then(r => r.data),
      axios.get('/api/exam/stats/time-distribution').then(r => r.data),
      axios.get('/api/exam/stats/growth').then(r => r.data),
    ])
    statsData.value = overview
    trendData.value = trend.trend || []
    errorDistData.value = errorDist.distribution || []
    timeDistData.value = timeDist.distribution || []
    growthData.value = growth
  } catch (e) {
    console.error('获取统计数据失败:', e)
  } finally {
    statsLoading.value = false
  }
}

async function fetchTrend() {
  try {
    const { data } = await axios.get('/api/exam/stats/trend', { params: { days: trendDays.value } })
    trendData.value = data.trend || []
  } catch {}
}

async function fetchRadar() {
  try {
    const { data } = await axios.get('/api/exam/stats/radar', { params: { career: radarCareer.value || career.value } })
    radarData.value = data.radar || []
  } catch {}
}

async function fetchErrorDist() {
  try {
    const { data } = await axios.get('/api/exam/stats/error-distribution', { params: { career: career.value } })
    errorDistData.value = data.distribution || []
  } catch {}
}

// ─── 错题本 ───

async function fetchWrong() {
  wrongLoading.value = true
  try {
    const params = { question_type: 'exam' }
    if (wrongCareerFilter.value) params.career = wrongCareerFilter.value
    if (wrongMasteredFilter.value !== '') params.mastered = wrongMasteredFilter.value
    const { data } = await axios.get('/api/exam/wrong-questions', { params })
    wrongQuestions.value = data.wrong_questions || data || []
  } catch { wrongQuestions.value = [] }
  finally { wrongLoading.value = false }
}

function reviewWrong(wq) {
  ElMessageBox.confirm(`重做此题：${wq.question.slice(0, 50)}...`, '重做', {
    confirmButtonText: '开始重做', cancelButtonText: '取消'
  }).then(() => {
    activeTab.value = 'practice'
    practicePhase.value = 'setup'
    questions.value = [formatWrongForReview(wq)]
    questionCount.value = 1
    nextTick(() => {
      practicePhase.value = 'doing'
      currentIdx.value = 0
      restoreQuestion()
    })
  }).catch(() => {})
}

function formatWrongForReview(wq) {
  let opts = []
  try { opts = typeof wq.options_json === 'string' ? JSON.parse(wq.options_json) : (wq.options_json || []) } catch {}
  return {
    id: wq.question_id || wq.id,
    question: wq.question,
    options_json: opts,
    answer: wq.correct_answer,
    difficulty: wq.difficulty || 'medium',
    question_type: 'single_choice',
    knowledge_point: '',
    analysis: wq.analysis || '',
    _answered: false,
    _correct: false
  }
}

async function markMastered(wq) {
  try {
    await axios.put(`/api/exam/wrong-questions/${wq.id}/master`)
    ElMessage.success('已标记为掌握')
    fetchWrong()
  } catch { ElMessage.error('操作失败') }
}

async function removeWrong(wq) {
  try {
    await axios.delete(`/api/exam/wrong-questions/${wq.id}`)
    ElMessage.success('已移除')
    fetchWrong()
  } catch { ElMessage.error('操作失败') }
}

// ─── 收藏夹 ───

async function fetchSaved() {
  savedLoading.value = true
  try {
    const params = { question_type: 'exam' }
    if (savedCareerFilter.value) params.career = savedCareerFilter.value
    const { data } = await axios.get('/api/exam/saved-questions', { params })
    savedQuestions.value = data.saved_questions || data || []
  } catch { savedQuestions.value = [] }
  finally { savedLoading.value = false }
}

async function removeSaved(sq) {
  try {
    await axios.delete(`/api/exam/saved-questions/${sq.id}`)
    ElMessage.success('已取消收藏')
    fetchSaved()
  } catch { ElMessage.error('操作失败') }
}

// ─── 职业列表 ───

const careerGroups = computed(() => {
  const groups = []
  for (const [cat, majors] of Object.entries(CAREER_CAT_MAP)) {
    groups.push({ label: cat, list: majors })
  }
  return groups
})

// ─── Tab 切换 ───

function onDetailCollapseChange(activeNames) {
  if (activeNames && activeNames.includes('stats')) {
    // 折叠面板打开时加载详细数据
    if (errorDistData.value.length === 0) fetchErrorDist()
    if (timeDistData.value.length === 0) {
      axios.get('/api/exam/stats/time-distribution').then(r => { timeDistData.value = r.data.distribution || [] }).catch(() => {})
    }
    if (!growthData.value.this_week) {
      axios.get('/api/exam/stats/growth').then(r => { growthData.value = r.data }).catch(() => {})
    }
    fetchRadar()
  }
}

function onTabClick(tab) {
  if (tab.props.name === 'wrong') fetchWrong()
  else if (tab.props.name === 'saved') fetchSaved()
}

function goToWrongTab() {
  activeTab.value = 'wrong'
  fetchWrong()
}

function goToWrongWithKp(kp) {
  activeTab.value = 'wrong'
  fetchWrong()
}

function showDayDetail(day) {
  ElMessage.info(`${day.date}：${day.questions}题 正确${day.correct} 错误${day.wrong} 正确率${day.accuracy}%`)
}

// 成长箭头
const growthArrowIcon = computed(() => {
  const c = growthData.value.change
  if (!c) return '—'
  return c.questions > 0 ? '↑' : c.questions < 0 ? '↓' : '→'
})

const growthArrowClass = computed(() => {
  const c = growthData.value.change
  if (!c) return ''
  return c.questions > 0 ? 'up' : c.questions < 0 ? 'down' : 'same'
})

const growthChangeText = computed(() => {
  const c = growthData.value.change
  if (!c) return '暂无变化'
  return c.questions > 0 ? '进步了！' : c.questions < 0 ? '加油！' : '持平'
})

// ═══════ 生命周期 ═══════

onMounted(() => {
  fetchCareerNames()
  loadDashboard()
  checkGuide()
  if (career.value) loadQuestions()
})

async function fetchCareerNames() {
  try {
    const { data } = await axios.get('/api/exam/career-knowledge')
    if (data.careers) allCareerNames.value = Object.keys(data.careers)
  } catch {}
}

// ─── CAREER_CAT_MAP (复用于岗位选择) ───

const CAREER_CAT_MAP = {
  "技术开发": ["前端开发工程师", "后端开发工程师", "全栈开发工程师", "算法工程师"],
  "数据与测试": ["数据分析师", "软件测试工程师"],
  "安全与运维": ["网络安全工程师", "运维工程师"],
  "产品与设计": ["产品经理", "UI/UX设计师"],
  "市场与运营": ["运营专员", "市场营销"],
}

// 监听筛选条件变化 → 重新加载题库
watch([difficulty, questionType, searchKeyword], () => {
  if (career.value && practicePhase.value !== 'doing') loadQuestions()
})

watch(career, () => {
  if (practicePhase.value !== 'doing') {
    questions.value = []
    practicePhase.value = 'setup'
  }
})
</script>

<style scoped>
.exam-practice-page {
  padding: 0;
}
.banner-wrap {
  position: relative;
}
.banner-cat {
  position: absolute;
  bottom: 0px;
  right: 320px;
  width: 80px;
  height: auto;
  pointer-events: none;
  z-index: 0;
  filter: drop-shadow(0 2px 8px rgba(0,0,0,0.18));
  transition: transform 0.3s ease;
}

/* ═══════ 筛选区 ═══════ */
.filter-section { margin-bottom: 10px; }
.filter-row-1, .filter-row-2 {
  display: flex;
  gap: 16px;
  margin-bottom: 14px;
  flex-wrap: wrap;
}
.filter-row-3 {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--border-light);
}
.filter-label {
  display: block;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-body);
  margin-bottom: 6px;
}
.filter-label i {
  margin-right: 6px;
  color: var(--primary);
  width: 14px;
}
.library-preview {
  display: flex;
  align-items: center;
  gap: 14px;
}
.preview-stat { text-align: center; }
.preview-label {
  display: block;
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-bottom: 2px;
}
.preview-label i {
  margin-right: 4px;
  color: var(--primary);
}
.preview-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-heading);
}
.preview-value small {
  font-size: 0.75rem;
  font-weight: 400;
}
.mode-radio-group .el-radio-button__inner {
  font-size: 0.82rem;
  padding: 6px 14px;
}
.mode-radio-group .el-radio-button__inner i {
  margin-right: 4px;
}

/* ═══════ 数据看板（粘性定位） ═══════ */
.dashboard-sticky-wrap {
  position: sticky;
  top: 0;
  z-index: 10;
  margin: 10px 0 16px;
  transition: box-shadow 0.2s;
}
.dashboard-sticky-wrap.is-stuck {
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}
.dashboard-section {
  background: linear-gradient(135deg, var(--primary-bg), var(--bg-alt));
  border: 1px solid rgba(61,90,128,0.12);
  border-radius: var(--radius-lg);
  padding: 16px 20px 12px;
  transition: all 0.2s;
}
.dash-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}
.dash-card-hover {
  position: relative;
  cursor: default;
  transition: all 0.2s;
}
.dash-card-hover:hover {
  border-color: var(--primary);
  box-shadow: 0 2px 8px rgba(61,90,128,0.1);
}
.dc-mini-chart {
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 4px;
}
.mini-trend { width: 100%; height: 36px; }
.mini-empty { font-size: 0.7rem; color: var(--text-muted); }
.chart-ring { padding: 0; }
.ring-svg { width: 44px; height: 44px; }

/* 连续打卡 dots */
.streak-vis {
  flex-direction: row;
  gap: 4px;
  flex-wrap: wrap;
  padding: 6px 0;
}
.streak-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent-gradient);
  transition: transform 0.2s;
}
.streak-dot.active { transform: scale(1.2); }
.streak-dot.max { box-shadow: 0 0 0 3px rgba(200,90,32,0.2); }
.streak-suffix {
  width: 100%;
  text-align: center;
  font-size: 0.68rem;
  color: var(--accent);
  font-weight: 600;
  margin-top: 2px;
}

/* 完成率进度条 */
.completion-bar-wrap {
  flex-direction: column;
  gap: 4px;
  padding: 0;
}
.completion-track {
  width: 100%;
  height: 8px;
  background: var(--border-light);
  border-radius: 4px;
  overflow: hidden;
}
.completion-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary), var(--primary-dark));
  border-radius: 4px;
  transition: width 0.4s;
}
.completion-hint { font-size: 0.68rem; color: var(--text-muted); }

/* hover tooltip */
.dc-tooltip {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: #333;
  color: white;
  padding: 6px 10px;
  border-radius: 8px;
  font-size: 0.72rem;
  z-index: 20;
  white-space: nowrap;
  margin-top: 6px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.15);
}
.tt-row { display: flex; justify-content: space-between; gap: 10px; padding: 2px 0; }
.tt-date { color: #aaa; }
.tt-val { font-weight: 600; }

/* 薄弱模块提示 */
.dash-weak-tip {
  margin-top: 10px;
  padding: 6px 12px;
  background: var(--accent-bg);
  border-radius: 8px;
  font-size: 0.78rem;
  color: var(--accent);
}
.dash-weak-tip b { color: var(--accent); }

/* ═══════ 折叠面板（详细数据分析） ═══════ */
.detail-collapse-wrap {
  margin-bottom: 16px;
}
.detail-collapse :deep(.el-collapse-item__header) {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--primary);
  padding: 10px 8px;
  border-radius: 10px;
  background: var(--bg-card);
}
.detail-collapse :deep(.el-collapse-item__content) {
  padding: 16px 0;
}
.detail-stats-section { padding: 0 4px; }

/* ═══════ 新手指引浮层 ═══════ */
.guide-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.45);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
}
.guide-card {
  background: var(--bg-card);
  border-radius: 20px;
  padding: 32px 28px 24px;
  max-width: 400px;
  width: 90%;
  position: relative;
  text-align: center;
  box-shadow: var(--shadow-lg);
}
.guide-close {
  position: absolute;
  top: 14px;
  right: 18px;
  font-size: 1.2rem;
  color: var(--text-muted);
  cursor: pointer;
}
.guide-close:hover { color: var(--text-body); }
.guide-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-heading);
  margin-bottom: 18px;
}
.guide-title i {
  margin-right: 8px;
  color: var(--primary);
}
.guide-body { text-align: left; }
.guide-step {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 14px;
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--text-body);
}
.guide-num {
  width: 26px;
  height: 26px;
  min-width: 26px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  font-size: 0.8rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 2px;
}
.guide-btn {
  margin-top: 18px;
  padding: 10px 28px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  border-radius: 30px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
  border: none;
}
.guide-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(61,90,128,0.3); }

.guide-fade-enter-active { transition: opacity 0.3s; }
.guide-fade-leave-active { transition: opacity 0.2s; }
.guide-fade-enter-from,
.guide-fade-leave-to { opacity: 0; }

/* ─── 刷题 ─── */
.practice-setup { margin-top: 10px; }
.setup-inner {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 10px 0;
}
.setup-text { flex: 1; }
.setup-text h3 { margin: 0 0 4px; font-size: 1.1rem; color: var(--text-heading); }
.setup-text p { margin: 0; color: var(--text-body); font-size: 0.88rem; }
.setup-action {
  display: flex;
  align-items: center;
  gap: 14px;
}
.count-select label {
  display: block;
  font-size: 0.75rem;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.answer-statusbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 16px;
  background: var(--bg-card);
  border-radius: var(--radius-md);
  margin-bottom: 12px;
  border: 1px solid var(--border);
}
.status-left, .status-right {
  display: flex;
  align-items: center;
  gap: 10px;
}
.status-progress { font-weight: 700; color: var(--primary); font-size: 0.95rem; }
.status-mode { font-size: 0.78rem; background: var(--primary-bg); padding: 2px 8px; border-radius: 4px; color: var(--primary); }
.status-timer { font-size: 0.85rem; color: var(--accent); font-weight: 600; }
.status-timer i { margin-right: 4px; }
.status-accuracy { font-size: 0.82rem; color: #059669; }
.status-accuracy i { margin-right: 4px; }

.q-header {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 14px;
}
.q-number { font-weight: 700; color: var(--primary); font-size: 0.9rem; }
.q-kp {
  font-size: 0.75rem;
  background: var(--primary-bg);
  padding: 2px 8px;
  border-radius: 4px;
  color: var(--primary);
}
.q-header-actions { margin-left: auto; display: flex; gap: 6px; }

.q-content { margin: 0; }
.q-stem { font-size: 0.95rem; line-height: 1.6; color: var(--text-heading); margin-bottom: 16px; }

.q-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.q-option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border: 1.5px solid var(--border);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s;
}
.q-option:hover:not(.correct):not(.wrong) { border-color: var(--primary); background: var(--bg-hover); }
.q-option.selected { border-color: var(--primary); background: var(--primary-bg); }
.q-option.correct { border-color: #059669; background: #f0f9eb; }
.q-option.wrong { border-color: #dc2626; background: #fef0f0; }
.opt-label {
  width: 24px; height: 24px; border-radius: 50%;
  background: #f5f5f5; display: flex; align-items: center; justify-content: center;
  font-size: 0.8rem; font-weight: 600; color: #555; flex-shrink: 0;
}
.opt-text { font-size: 0.9rem; color: var(--text-heading); }

.judge-options { flex-direction: row; gap: 16px; }
.judge-options .q-option { flex: 1; justify-content: center; padding: 14px; }

.q-analysis { margin-top: 8px; }
.analysis-header { display: flex; align-items: center; gap: 12px; margin-bottom: 10px; }
.result-correct { color: #059669; font-weight: 600; font-size: 0.95rem; }
.result-wrong { color: #dc2626; font-weight: 600; font-size: 0.95rem; }
.correct-answer { font-size: 0.85rem; color: var(--text-body); }
.analysis-title { font-weight: 600; color: var(--text-body); font-size: 0.82rem; margin-bottom: 6px; }
.analysis-title i { margin-right: 4px; }
.analysis-body p { font-size: 0.88rem; color: var(--text-body); line-height: 1.6; }

.q-nav { display: flex; justify-content: space-between; margin-top: 16px; padding-top: 14px; border-top: 1px solid var(--border-light); }

.question-thumbnails {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 10px 0;
}
.thumb-item {
  width: 30px; height: 30px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 6px; font-size: 0.75rem; cursor: pointer;
  background: #f5f5f5; color: #666;
  transition: all 0.15s;
}
.thumb-item.current { border: 2px solid var(--primary); }
.thumb-item.correct { background: #f0f9eb; color: #059669; }
.thumb-item.wrong { background: #fef0f0; color: #dc2626; }
.thumb-item.active { font-weight: 700; }

/* ─── 报告 ─── */
.practice-report { margin-top: 10px; }
.report-icon { margin-bottom: 10px; }
.report-subtitle { color: var(--text-muted); font-size: 0.82rem; margin: 0 0 20px; }
.report-stats {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 24px;
}
.report-stat-card { text-align: center; }
.report-detail { text-align: left; max-width: 500px; margin: 0 auto 20px; }
.report-error-item {
  background: var(--bg-alt);
  border-radius: 8px;
  padding: 10px 14px;
  margin-bottom: 8px;
}
.re-q { font-size: 0.88rem; margin-bottom: 4px; color: var(--text-heading); }
.re-answer { font-size: 0.8rem; }
.wrong-text { color: #dc2626; font-weight: 600; }
.correct-text { color: #059669; font-weight: 600; }
.report-actions { display: flex; justify-content: center; gap: 14px; }

/* ─── 统计图表区 ─── */
.chart-row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-bottom: 16px;
}
.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 0.88rem;
}
.chart-header i { margin-right: 6px; color: var(--primary); }
.chart-body { min-height: 200px; display: flex; align-items: center; justify-content: center; }
.trend-svg, .radar-svg, .pie-svg { width: 100%; max-height: 220px; }
.radar-body { min-height: 280px; }
.radar-svg { max-height: 280px; }

/* 错题分布柱状图 */
.bar-body {
  flex-direction: column;
  padding: 10px 0;
  min-height: 180px;
}
.bar-item {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  margin-bottom: 6px;
  transition: background 0.15s;
  padding: 3px 6px;
  border-radius: 4px;
}
.bar-item:hover { background: var(--bg-hover); }
.bar-label {
  width: 80px;
  font-size: 0.75rem;
  color: var(--text-body);
  text-align: right;
  flex-shrink: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.bar-track {
  flex: 1;
  height: 14px;
  background: var(--border-light);
  border-radius: 7px;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--primary), var(--primary-dark));
  border-radius: 7px;
  transition: width 0.3s;
}
.bar-value {
  width: 24px;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--primary);
  text-align: center;
}
.show-all-wrong {
  text-align: center;
  font-size: 0.8rem;
  color: var(--primary);
  cursor: pointer;
  padding: 6px 0;
}
.show-all-wrong:hover { text-decoration: underline; }

/* 时段分析饼图 */
.pie-body {
  flex-direction: column;
  gap: 12px;
}
.pie-legend { width: 100%; }
.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.78rem;
}
.legend-item:hover { background: var(--bg-hover); }
.legend-dot {
  width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0;
}
.legend-label { flex: 1; color: var(--text-body); }
.legend-value { color: var(--text-heading); font-weight: 600; }
.legend-pct { color: var(--text-muted); }

/* 成长对比 */
.growth-body { padding: 10px 0; }
.growth-comparison {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
  margin-bottom: 16px;
}
.growth-column { text-align: center; }
.gw-label { font-size: 0.8rem; color: var(--text-muted); margin-bottom: 4px; }
.gw-value { font-size: 1.3rem; font-weight: 700; color: var(--text-heading); }
.gw-accuracy { font-size: 0.85rem; color: var(--text-body); }
.growth-column.this-week .gw-value { color: var(--primary); }
.growth-column.this-week .gw-accuracy { color: var(--primary); }
.growth-vs { text-align: center; }
.vs-arrow { font-size: 2rem; font-weight: 700; }
.vs-arrow.up { color: #059669; }
.vs-arrow.down { color: #dc2626; }
.vs-arrow.same { color: var(--text-muted); }
.vs-text { font-size: 0.82rem; font-weight: 600; }
.vs-text.up { color: #059669; }
.vs-text.down { color: #dc2626; }
.growth-detail { max-width: 300px; margin: 0 auto; }
.gd-row { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid var(--border-light); }
.gd-label { color: var(--text-body); font-size: 0.82rem; }
.gd-value { font-weight: 600; font-size: 0.85rem; }
.gd-value.up { color: #059669; }
.gd-value.down { color: #dc2626; }

/* ─── 错题本 ─── */
.wrong-section, .saved-section { padding: 10px 0; }
.wrong-item, .saved-item {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  margin-bottom: 10px;
}
.wi-header, .si-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}
.wi-source, .si-source {
  font-size: 0.75rem;
  background: var(--primary-bg);
  color: var(--primary);
  padding: 2px 8px;
  border-radius: 4px;
}
.wi-source i, .si-source i { margin-right: 4px; }
.wi-status { font-size: 0.75rem; margin-left: auto; }
.wi-status.mastered { color: #059669; }
.wi-question, .si-question { font-size: 0.9rem; color: var(--text-heading); margin-bottom: 6px; line-height: 1.5; }
.wi-answers { display: flex; gap: 16px; font-size: 0.82rem; margin-bottom: 6px; }
.wi-wrong { color: #dc2626; }
.wi-correct { color: #059669; }
.wi-actions { display: flex; gap: 8px; }
.si-note { font-size: 0.8rem; color: var(--text-body); padding: 4px 8px; background: var(--bg-alt); border-radius: 4px; }

/* ─── Button overrides ─── */
.btn-outline.is-warning {
  color: var(--accent);
  border-color: var(--accent);
}

/* ─── 动画 ─── */
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* ─── 笔试模式导航 ─── */
.exam-mode-nav {
  display: flex;
  gap: 0;
  margin: -1px 0 16px;
  background: #fff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  border: 1px solid #e8ecf0;
}
.emn-item {
  flex: 1;
  text-align: center;
  padding: 12px 0;
  font-size: 0.92rem;
  font-weight: 500;
  color: #6b7a8f;
  text-decoration: none;
  transition: all 0.2s;
  border-bottom: 3px solid transparent;
  position: relative;
}
.emn-item i { margin-right: 6px; }
.emn-item:hover { color: #3D5A80; background: #f6f8fa; }
.emn-active {
  color: #3D5A80;
  border-bottom-color: #3D5A80;
  background: #f0f4f8;
}

/* ─── 响应式 ─── */
@media (max-width: 768px) {
  .exam-practice-page { padding: 0 10px 30px; }
  .dash-cards { grid-template-columns: repeat(2, 1fr); }
  .chart-row-2 { grid-template-columns: 1fr; }
  .filter-row-1, .filter-row-2 { flex-direction: column; }
  .filter-row-3 { flex-direction: column; gap: 12px; }
  .setup-inner { flex-direction: column; text-align: center; }
  .setup-action { flex-direction: column; }
  .report-stats { gap: 16px; }
  .growth-comparison { gap: 16px; }
  .library-preview { gap: 8px; }
  .judge-options { flex-direction: column; }
}
</style>