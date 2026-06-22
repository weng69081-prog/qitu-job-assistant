<template>
  <div class="exam-page">
    <!-- ═══════ 顶部栏 ═══════ -->
    <div class="exam-topbar">
      <el-button class="back-circle-btn" @click="backToEntry">
        <i class="fa-solid fa-arrow-left"></i> 返回笔试练习
      </el-button>
      <span class="exam-title">
        <i class="fa-solid fa-pen"></i> 笔试专项练习
      </span>
      <div class="topbar-actions">
        <el-button v-if="phase === 'doing'" size="small" type="danger" plain @click="confirmEndExam">
          <i class="fa-solid fa-stop"></i> 结束
        </el-button>
      </div>
    </div>

    <!-- ════════════════ Phase 1: 设置 ════════════════ -->
    <div v-if="phase === 'ready'" class="section-panel setup-stage">
      <div class="setup-shell">
        <aside class="setup-side">
          <div class="setup-side-kicker">启途笔试舱</div>
          <h1>三步准备好一次练习</h1>
          <p>先选目标岗位，再选练习模式，AI 会为您匹配相应题目。</p>
          <div class="setup-steps">
            <button class="setup-step" :class="{ active: setupStep === 1, done: career }" @click="setupStep = 1">
              <span>01</span><b>选择岗位</b><small>决定出题方向</small>
            </button>
            <button class="setup-step" :class="{ active: setupStep === 2, done: mode }" @click="setupStep = 2" :disabled="!career">
              <span>02</span><b>选择模式</b><small>专项 / 模考 / 错题</small>
            </button>
            <button class="setup-step" :class="{ active: setupStep === 3 }" @click="setupStep = 3" :disabled="!career">
              <span>03</span><b>确认配置</b><small>开始练习</small>
            </button>
          </div>
        </aside>

        <main class="setup-main-card">
          <div class="setup-main-head">
            <div>
              <span class="setup-breadcrumb">步骤 {{ setupStep }} / 3</span>
              <h2>{{ setupStep === 1 ? '告诉启途，你想练哪个岗位' : setupStep === 2 ? '选择练习模式' : '确认题目数量，开始答题' }}</h2>
            </div>
            <div class="setup-mini-badge" v-if="career">{{ career }}</div>
          </div>

          <!-- Step 1: 岗位选择 -->
          <div v-if="setupStep === 1" class="setup-step-content">
            <div class="career-hero">
              <div>
                <span class="custom-kicker">CAREER SELECTION</span>
                <h3>选择目标岗位，系统将匹配对应题目</h3>
                <p>已收藏的岗位会优先显示，也可以从分类中选取。</p>
              </div>
              <div class="custom-paper-mark">EXAM</div>
            </div>

            <el-select v-model="career" placeholder="请选择目标岗位" filterable clearable allow-create style="width:100%" @change="onCareerChange">
              <el-option-group v-if="store.validBookmarks.length" label="⭐ 已收藏">
                <el-option v-for="b in store.validBookmarks" :key="b.career" :label="b.career" :value="b.career" />
              </el-option-group>
              <el-option-group v-for="g in popularCareers" :key="g.label" :label="g.label">
                <el-option v-for="c in g.list" :key="c" :label="c" :value="c" />
              </el-option-group>
            </el-select>

            <div class="setup-nav">
              <el-button type="primary" @click="setupStep = 2" :disabled="!career">
                下一步 <i class="fa-solid fa-arrow-right"></i>
              </el-button>
            </div>
          </div>

          <!-- Step 2: 模式选择 -->
          <div v-if="setupStep === 2" class="setup-step-content">
            <el-form label-position="top">
              <el-form-item>
                <template #label><i class="fa-solid fa-gamepad"></i> 练习模式</template>
                <el-radio-group v-model="mode" class="mode-radio-group">
                  <el-radio-button value="专项练习">
                    <div class="mode-option">
                      <span class="mode-icon"><i class="fa-regular fa-clipboard"></i></span>
                      <div><strong>专项练习</strong><p class="mode-desc">按考点、难度、题型自由筛选</p></div>
                    </div>
                  </el-radio-button>
                  <el-radio-button value="模拟卷练习">
                    <div class="mode-option">
                      <span class="mode-icon"><i class="fa-regular fa-file-lines"></i></span>
                      <div><strong>模拟卷练习</strong><p class="mode-desc">自动混合出题，模拟真实考试</p></div>
                    </div>
                  </el-radio-button>
                  <el-radio-button value="错题重练">
                    <div class="mode-option">
                      <span class="mode-icon"><i class="fa-solid fa-rotate"></i></span>
                      <div><strong>错题重练</strong><p class="mode-desc">从错题本抽题巩固薄弱点</p></div>
                    </div>
                  </el-radio-button>
                </el-radio-group>
              </el-form-item>

              <!-- 模拟卷练习：题数 -->
              <template v-if="mode === '模拟卷练习'">
                <el-form-item>
                  <template #label><i class="fa-regular fa-clock"></i> 题数</template>
                  <el-radio-group v-model="examCount">
                    <el-radio-button :value="5">5 题</el-radio-button>
                    <el-radio-button :value="10">10 题</el-radio-button>
                    <el-radio-button :value="15">15 题</el-radio-button>
                    <el-radio-button :value="20">20 题</el-radio-button>
                  </el-radio-group>
                </el-form-item>
              </template>
            </el-form>

            <div class="setup-nav">
              <el-button @click="setupStep = 1"><i class="fa-solid fa-arrow-left"></i> 上一步</el-button>
              <el-button type="primary" @click="setupStep = 3">下一步 <i class="fa-solid fa-arrow-right"></i></el-button>
            </div>
          </div>

          <!-- Step 3: 确认 + 开始 -->
          <div v-if="setupStep === 3" class="setup-step-content">
            <!-- 专项练习：考点筛选 -->
            <template v-if="mode === '专项练习'">
              <div class="setup-summary">
                <p><i class="fa-solid fa-crosshairs"></i> 目标岗位：<b>{{ career }}</b></p>
                <p><i class="fa-solid fa-gamepad"></i> 练习模式：<b>专项练习</b></p>
              </div>

              <el-divider content-position="left" style="margin: 12px 0">
                <span style="font-size:0.85rem;font-weight:600;color:var(--primary)"><i class="fa-regular fa-circle" style="color:#52c41a"></i> 通用能力题</span>
              </el-divider>
              <div v-if="generalKnowledgePoints.length === 0" class="no-kp-tip">
                <i class="fa-solid fa-info-circle"></i> 暂无通用能力考点数据，请先选择目标岗位
              </div>
              <div v-for="kp in generalKnowledgePoints" :key="kp.id" class="kp-row">
                <el-checkbox v-model="selectedKnowledgePoints" :label="kp.name" :value="kp.name">
                  {{ kp.name }}
                </el-checkbox>
                <div class="kp-filters">
                  <el-select v-model="difficultyMap[kp.name]" placeholder="难度" size="small" clearable style="width:110px">
                    <el-option label="入门" value="easy" />
                    <el-option label="基础" value="medium" />
                    <el-option label="进阶" value="hard" />
                    <el-option label="挑战" value="all" />
                  </el-select>
                  <el-select v-model="typeMap[kp.name]" placeholder="题型" size="small" clearable style="width:110px">
                    <el-option label="单选题" value="single_choice" />
                    <el-option label="多选题" value="multi_choice" />
                    <el-option label="判断题" value="judge" />
                    <el-option label="不限" value="all" />
                  </el-select>
                </div>
              </div>

              <el-divider content-position="left" style="margin: 12px 0">
                <span style="font-size:0.85rem;font-weight:600;color:var(--primary)"><i class="fa-regular fa-circle" style="color:var(--primary)"></i> 专业能力题</span>
              </el-divider>
              <div v-if="professionalKnowledgePoints.length === 0" class="no-kp-tip">
                <i class="fa-solid fa-info-circle"></i> 暂无专业能力考点数据，请先选择目标岗位
              </div>
              <div v-for="kp in professionalKnowledgePoints" :key="kp.id" class="kp-row">
                <el-checkbox v-model="selectedKnowledgePoints" :label="kp.name" :value="kp.name">
                  {{ kp.name }}
                </el-checkbox>
                <div class="kp-filters">
                  <el-select v-model="difficultyMap[kp.name]" placeholder="难度" size="small" clearable style="width:110px">
                    <el-option label="入门" value="easy" />
                    <el-option label="基础" value="medium" />
                    <el-option label="进阶" value="hard" />
                    <el-option label="挑战" value="all" />
                  </el-select>
                  <el-select v-model="typeMap[kp.name]" placeholder="题型" size="small" clearable style="width:110px">
                    <el-option label="单选题" value="single_choice" />
                    <el-option label="多选题" value="multi_choice" />
                    <el-option label="判断题" value="judge" />
                    <el-option label="不限" value="all" />
                  </el-select>
                </div>
              </div>
            </template>

            <!-- 模拟卷练习：确认 -->
            <template v-if="mode === '模拟卷练习'">
              <div class="setup-summary">
                <p><i class="fa-solid fa-crosshairs"></i> 目标岗位：<b>{{ career }}</b></p>
                <p><i class="fa-solid fa-gamepad"></i> 练习模式：<b>模拟卷练习</b></p>
                <p><i class="fa-regular fa-clock"></i> 题数：<b>{{ examCount }} 题</b></p>
              </div>
              <el-alert title="将自动从各考点混合出题，涵盖通用能力和专业知识" type="info" :closable="false" show-icon style="margin-top:8px" />
            </template>

            <!-- 错题重练：确认 -->
            <template v-if="mode === '错题重练'">
              <div class="setup-summary">
                <p><i class="fa-solid fa-crosshairs"></i> 目标岗位：<b>{{ career }}</b></p>
                <p><i class="fa-solid fa-gamepad"></i> 练习模式：<b>错题重练</b></p>
              </div>
              <div v-if="wrongStats" class="wrong-stats-card">
                <div class="wrong-stat-item">
                  <span class="stat-label"><i class="fa-solid fa-triangle-exclamation"></i> 总错题数</span>
                  <span class="stat-value">{{ wrongStats.total }}</span>
                </div>
                <div class="wrong-stat-item">
                  <span class="stat-label"><i class="fa-solid fa-bookmark"></i> 未掌握</span>
                  <span class="stat-value warn">{{ wrongStats.unmastered }}</span>
                </div>
              </div>
              <el-alert title="将从错题本中抽取题目供你重练" type="warning" :closable="false" show-icon style="margin-top:8px" />
            </template>

            <div class="setup-nav final-nav">
              <el-button @click="setupStep = 2"><i class="fa-solid fa-arrow-left"></i> 上一步</el-button>
              <el-button type="primary" size="large" @click="startExam" :loading="startLoading">
                <i class="fa-solid fa-play"></i> {{ startBtnText }}
              </el-button>
            </div>
          </div>
        </main>
      </div>
    </div>

    <!-- ════════════════ Phase 2: 答题中 ════════════════ -->
    <div v-if="phase === 'doing'" class="section-panel exam-phase">
      <!-- 顶部状态栏 -->
      <div class="exam-status-bar">
        <div class="it-left">
          <el-tag size="small" effect="dark" :type="modeTagType">{{ mode }}</el-tag>
          <span class="it-career">{{ career }}</span>
        </div>
        <div class="it-center">
          <div class="countdown-timer">
            <el-icon><Timer /></el-icon>
            <span>{{ formatTime(timer) }}</span>
          </div>
          <span class="round-badge">已答 {{ answeredCount }}/{{ questions.length }}</span>
        </div>
        <div class="it-right">
          <el-button size="small" type="danger" @click="confirmEndExam"><i class="fa-solid fa-stop"></i> 交卷</el-button>
        </div>
      </div>

      <div class="exam-layout">
        <!-- 左侧答题卡 -->
        <aside class="exam-sidebar">
          <div class="sidebar-card">
            <div class="sidebar-title"><i class="fa-solid fa-grid"></i> 答题卡</div>
            <div class="sidebar-stats">
              <div class="sidebar-stat-item">
                <span class="sidebar-stat-num">{{ answeredCount }}</span>
                <span class="sidebar-stat-label">已答</span>
              </div>
              <div class="sidebar-stat-item">
                <span class="sidebar-stat-num">{{ questions.length }}</span>
                <span class="sidebar-stat-label">总题</span>
              </div>
              <div class="sidebar-stat-item">
                <span class="sidebar-stat-num" :style="{color: accuracyColor}">{{ accuracyPercent }}%</span>
                <span class="sidebar-stat-label">正确率</span>
              </div>
            </div>
            <div class="sidebar-grid">
              <div
                v-for="(q, i) in questions"
                :key="i"
                class="sidebar-grid-item"
                :class="{
                  'grid-current': i === currentIndex,
                  'grid-answered': q._result,
                  'grid-correct': q._result?.is_correct,
                  'grid-wrong': q._result && !q._result.is_correct,
                }"
                @click="jumpToQuestion(i)">
                <span>{{ i + 1 }}</span>
              </div>
            </div>
            <div class="sidebar-legend">
              <span class="legend-item"><span class="legend-dot dot-answered"></span> 已答</span>
              <span class="legend-item"><span class="legend-dot dot-current"></span> 当前</span>
              <span class="legend-item"><span class="legend-dot dot-unanswered"></span> 未答</span>
            </div>
            <div class="sidebar-actions">
              <el-button size="small" type="danger" plain @click="confirmEndExam" style="width:100%">
                <i class="fa-solid fa-stop"></i> 交卷
              </el-button>
            </div>
          </div>
        </aside>

        <!-- 主内容区 -->
        <div class="exam-main">
          <!-- 加载动画 -->
          <div v-if="isLoading" class="loading-section">
            <div class="skeleton-card">
              <div class="skeleton-line skeleton-tag"></div>
              <div class="skeleton-line skeleton-title"></div>
              <div class="skeleton-line skeleton-text"></div>
              <div class="skeleton-line skeleton-text"></div>
              <div class="skeleton-line skeleton-text short"></div>
              <div class="skeleton-options">
                <div class="skeleton-line skeleton-option"></div>
                <div class="skeleton-line skeleton-option"></div>
                <div class="skeleton-line skeleton-option"></div>
                <div class="skeleton-line skeleton-option"></div>
              </div>
            </div>
            <div class="loading-text">
              <p><i class="fa-solid fa-hourglass-half"></i> 正在为您生成 {{ career }} 方向的题目…</p>
              <p v-if="loadMsg" class="load-msg">{{ loadMsg }}</p>
              <p v-if="loadError" class="load-error">{{ loadError }}</p>
              <el-button v-if="loadError" type="primary" @click="retryLoad" style="margin-top:8px">
                <i class="fa-solid fa-rotate"></i> 重试
              </el-button>
            </div>
          </div>

          <!-- 题目卡片 -->
          <template v-if="!isLoading && currentQuestion">
            <transition name="exam-fade" mode="out-in">
              <div key="currentQuestion.id" class="card question-card">
                <!-- 标签行 -->
                <div class="q-tags">
                  <span class="tag-pill blue q-type-tag">
                    <i class="fas" :class="questionTypeIcon"></i>
                    {{ questionTypeLabel }}
                  </span>
                  <span v-if="currentQuestion.knowledge_point" class="tag-pill orange">
                    <i class="fa-solid fa-tag"></i>
                    {{ currentQuestion.knowledge_point }}
                  </span>
                  <span v-if="currentQuestion.difficulty" class="tag-pill" :class="difficultyPillClass(currentQuestion.difficulty)">
                    <i class="fa-solid fa-signal"></i>
                    {{ difficultyLabel(currentQuestion.difficulty) }}
                  </span>
                </div>

                <!-- 题目标题 -->
                <div class="q-heading">
                  <i class="fa-regular fa-circle-question"></i>
                  题目 {{ currentIndex + 1 }}
                </div>

                <!-- 题干 -->
                <div class="q-text">{{ currentQuestion.question }}</div>

                <!-- 单选题 -->
                <div v-if="currentQuestion.question_type === 'single_choice'" class="options-wrap">
                  <div
                    v-for="(opt, oi) in parsedOptions"
                    :key="oi"
                    class="option-item"
                    :class="optionClass(opt.key)"
                    @click="submitAnswer(opt.key)">
                    <span class="opt-key">{{ opt.key }}.</span>
                    <span class="opt-text">{{ opt.value }}</span>
                    <span v-if="selectedOption === opt.key && !answerResult" class="opt-check-icon">
                      <i class="fa-regular fa-circle-check"></i>
                    </span>
                  </div>
                </div>

                <!-- 多选题 -->
                <div v-if="currentQuestion.question_type === 'multi_choice'" class="options-wrap">
                  <div
                    v-for="(opt, oi) in parsedOptions"
                    :key="oi"
                    class="option-item"
                    :class="multiOptionClass(opt.key)"
                    @click="toggleMultiSelect(opt.key)">
                    <span class="opt-checkbox">
                      <i v-if="multiSelected.includes(opt.key)" class="fa-regular fa-square-check" style="color:var(--primary)"></i>
                      <i v-else class="fa-regular fa-square" style="color:#ccc"></i>
                    </span>
                    <span class="opt-key">{{ opt.key }}.</span>
                    <span class="opt-text">{{ opt.value }}</span>
                  </div>
                  <div v-if="currentQuestion.question_type === 'multi_choice'" class="multi-submit-row">
                    <el-button
                      type="primary"
                      size="small"
                      :disabled="multiSelected.length === 0 || answerResult !== null"
                      @click="submitMultiAnswer">
                      <i class="fa-regular fa-check"></i> 确认提交
                    </el-button>
                    <span v-if="multiSelected.length > 0" class="multi-hint">
                      <i class="fa-solid fa-layer-group"></i> 已选 {{ multiSelected.length }} 项
                    </span>
                  </div>
                </div>

                <!-- 判断题 -->
                <div v-if="currentQuestion.question_type === 'judge'" class="judge-wrap">
                  <div class="judge-options">
                    <div
                      class="judge-item"
                      :class="judgeClass('对')"
                      @click="submitAnswer('对')">
                      <i class="fa-regular fa-check"></i> 对
                    </div>
                    <div
                      class="judge-item"
                      :class="judgeClass('错')"
                      @click="submitAnswer('错')">
                      <i class="fa-regular fa-xmark"></i> 错
                    </div>
                  </div>
                </div>

                <!-- 结果反馈 -->
                <div v-if="answerResult" class="feedback-section">
                  <el-alert
                    :title="answerResult.is_correct ? '回答正确！' : '回答错误'"
                    :type="answerResult.is_correct ? 'success' : 'error'"
                    :closable="false"
                    show-icon />
                  <div class="feedback-correct" v-if="answerResult.correct_answer">
                    <i class="fa-regular fa-circle-check"></i>
                    正确答案：<b>{{ answerResult.correct_answer }}</b>
                  </div>
                  <div class="analysis-box" v-if="answerResult.analysis">
                    <h4><i class="fa-solid fa-book-open"></i> 解析</h4>
                    <p>{{ answerResult.analysis }}</p>
                  </div>
                  <div class="analysis-box hint-box" v-if="currentQuestion.knowledge_point">
                    <p>
                      <i class="fa-regular fa-lightbulb"></i>
                      本题为 <b>{{ career }}</b> 方向考点，考察 <b>{{ currentQuestion.knowledge_point }}</b>
                    </p>
                  </div>
                </div>

                <!-- 底部操作区 -->
                <div class="q-actions">
                  <el-button
                    size="small"
                    :disabled="!answerResult"
                    :type="isSaved ? 'warning' : 'default'"
                    @click="saveCurrentQuestion">
                    <i :class="isSaved ? 'fa-solid fa-star' : 'fa-regular fa-star'" style="margin-right:4px"></i>
                    {{ isSaved ? '已收藏' : '收藏此题' }}
                  </el-button>
                  <div class="q-actions-right">
                    <el-button
                      v-if="currentIndex < questions.length - 1"
                      type="primary"
                      size="small"
                      :disabled="!answerResult"
                      @click="nextQuestion">
                      下一题 <i class="fa-solid fa-arrow-right"></i>
                    </el-button>
                    <el-button
                      v-if="currentIndex === questions.length - 1"
                      type="success"
                      size="small"
                      :disabled="!answerResult"
                      @click="finishExam">
                      <i class="fa-solid fa-chart-simple"></i> 完成并查看报告
                    </el-button>
                  </div>
                </div>

                <!-- 草稿区 -->
                <el-collapse class="draft-collapse">
                  <el-collapse-item name="draft">
                    <template #title>
                      <span><i class="fa-solid fa-pencil"></i> 草稿区</span>
                    </template>
                    <el-input
                      v-model="draftNote"
                      type="textarea"
                      :rows="4"
                      placeholder="可在此记录计算过程或思路..." />
                  </el-collapse-item>
                </el-collapse>
              </div>
            </transition>
          </template>

          <!-- 没题 -->
          <div v-if="!isLoading && !currentQuestion && !loadError" class="empty-state">
            <div class="empty-icon">
              <i class="fa-solid fa-inbox"></i>
            </div>
            <p style="font-size:1.2rem">暂无可用题目</p>
            <p>请调整筛选条件再试</p>
            <el-button type="primary" @click="backToReady" style="margin-top:12px">
              <i class="fa-solid fa-arrow-left"></i> 返回设置
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- ════════════════ Phase 3: 完成页 ════════════════ -->
    <div v-if="phase === 'done'" class="section-panel">
      <el-card shadow="never" class="report-card">
        <template #header>
          <span style="font-weight:600"><i class="fa-solid fa-chart-simple"></i> 练习报告</span>
          <el-button text size="small" @click="goToWrongQuestions" style="float:right">
            <i class="fa-regular fa-clipboard"></i> 查看错题详情
          </el-button>
        </template>
        <div class="report-top-info">
          <span class="report-job">{{ career }}</span>
          <el-tag size="small" effect="dark" type="primary">{{ mode }}</el-tag>
          <span class="report-rounds">共 {{ questions.length }} 题 · 用时 {{ timeSpent }}</span>
        </div>
        <div class="overall-score-area">
          <el-progress type="circle" :percentage="accuracyPercent" :width="130" :color="scoreColor(accuracyPercent)" />
          <h3>正确率 {{ accuracyPercent }}%</h3>
        </div>
        <div class="report-stats">
          <div class="report-stat-card">
            <div class="report-stat-num">{{ questions.length }}</div>
            <div class="report-stat-label">总题数</div>
          </div>
          <div class="report-stat-card">
            <div class="report-stat-num" style="color:#67c23a">{{ correctCount }}</div>
            <div class="report-stat-label">答对</div>
          </div>
          <div class="report-stat-card">
            <div class="report-stat-num" :style="{color: accuracyColor}">{{ accuracyPercent }}%</div>
            <div class="report-stat-label">正确率</div>
          </div>
          <div class="report-stat-card">
            <div class="report-stat-num">{{ timeSpent }}</div>
            <div class="report-stat-label">用时</div>
          </div>
        </div>

        <!-- 考点统计 -->
        <div v-if="examResult?.knowledge_stats" class="weak-section">
          <el-divider content-position="left">
            <span style="font-weight:600;font-size:0.9rem"><i class="fa-solid fa-chart-pie" style="color:#2563EB"></i> 考点统计</span>
          </el-divider>
          <div class="weak-list">
            <div v-for="(stats, kp) in examResult.knowledge_stats" :key="kp" class="weak-item">
              <span class="weak-name">{{ kp }}</span>
              <span class="weak-rate">{{ stats.correct }}/{{ stats.total }} 正确</span>
              <el-progress :percentage="Math.round(stats.correct/stats.total*100)" :width="80" :stroke-width="6" />
            </div>
          </div>
        </div>

        <!-- 薄弱知识点 -->
        <div v-if="weakPoints.length > 0" class="weak-section">
          <el-divider content-position="left">
            <span style="font-weight:600;font-size:0.9rem"><i class="fa-solid fa-chart-line" style="color:#e6a23c"></i> 薄弱知识点</span>
          </el-divider>
          <div class="weak-list">
            <div v-for="(wp, wi) in weakPoints" :key="wi" class="weak-item">
              <span class="weak-rank">{{ wi + 1 }}</span>
              <span class="weak-name">{{ wp.name }}</span>
              <span class="weak-rate">{{ wp.wrongRate }}% 错误率</span>
            </div>
          </div>
        </div>

        <!-- 学习推荐 -->
        <div v-if="examResult?.learning_tags && examResult.learning_tags.length > 0" class="weak-section">
          <el-divider content-position="left">
            <span style="font-weight:600;font-size:0.9rem"><i class="fa-solid fa-graduation-cap" style="color:#67c23a"></i> 学习推荐</span>
          </el-divider>
          <div class="learning-tag-list">
            <el-tag v-for="tag in examResult.learning_tags" :key="tag" effect="plain" type="success" style="margin:4px" size="medium">{{ tag }}</el-tag>
          </div>
        </div>

        <!-- 每题详情 -->
        <div class="weak-section">
          <el-divider content-position="left">
            <span style="font-weight:600;font-size:0.9rem"><i class="fa-solid fa-list"></i> 题目详情</span>
          </el-divider>
          <div v-for="(q, i) in questions" :key="q.id" class="question-detail-item">
            <div class="qdi-header">
              <span class="qdi-num">{{ i + 1 }}</span>
              <el-tag :type="q._result?.is_correct ? 'success' : 'danger'" size="small" effect="dark">
                {{ q._result?.is_correct ? '✓ 正确' : '✗ 错误' }}
              </el-tag>
            </div>
            <div class="qdi-question">{{ q.question }}</div>
            <div class="qdi-answer" v-if="q._result">
              <span v-if="!q._result.is_correct">你的答案：<b class="wrong-ans">{{ q._userAnswer }}</b> · </span>
              正确答案：<b class="correct-ans">{{ q._result.correct_answer }}</b>
            </div>
            <div class="qdi-analysis" v-if="q.analysis">
              <i class="fa-solid fa-book-open"></i> {{ q.analysis }}
            </div>
          </div>
        </div>

        <div class="report-actions">
          <el-button @click="doAnotherRound"><i class="fa-solid fa-rotate"></i> 再来一组</el-button>
          <el-button type="primary" @click="goToWrongQuestions"><i class="fa-solid fa-chart-simple"></i> 查看错题详情</el-button>
          <el-button @click="backToReady"><i class="fa-solid fa-arrow-left"></i> 返回设置</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Timer } from '@element-plus/icons-vue'
import axios from 'axios'
import { useCareerStore } from '../stores/career'

const store = useCareerStore()
const router = useRouter()

// ═══════════════════════════════════════════════
// 岗位大类数据
// ═══════════════════════════════════════════════
const popularCareers = [
  { label: '技术类', list: ['前端开发工程师', 'Java开发工程师', 'Python开发工程师', '数据分析师', '算法工程师', '测试开发工程师'] },
  { label: '设计/产品类', list: ['UI/UX设计师', '产品经理'] },
]

// ═══════════════════════════════════════════════
// 阶段与配置
// ═══════════════════════════════════════════════
const setupStep = ref(1)
const phase = ref('ready')
const career = ref('')
const mode = ref('专项练习')
const difficulty = ref('')
const questionType = ref('')
const examCount = ref(10)

// 考点相关
const allKnowledgePoints = ref([])
const generalKnowledgePoints = ref([])
const professionalKnowledgePoints = ref([])
const selectedKnowledgePoints = ref([])
const difficultyMap = ref({})
const typeMap = ref({})

// 错题重练
const wrongStats = ref(null)
const wrongFilterKnowledge = ref('')

// 答题状态
const questions = ref([])
const currentIndex = ref(0)
const selectedOption = ref('')
const multiSelected = ref([])
const answerResult = ref(null)
const answeredCount = ref(0)
const correctCount = ref(0)
const savedQuestions = ref(new Set())

// 笔试记录结果（finishExam后从后端返回）
const examResult = ref(null)

// 计时
const timer = ref(0)
let timerInterval = null

// 加载状态
const startLoading = ref(false)
const isLoading = ref(false)
const loadError = ref('')
const loadMsg = ref('')

// 草稿
const draftNote = ref('')

// computed
const currentQuestion = computed(() => {
  if (currentIndex.value < questions.value.length) {
    return questions.value[currentIndex.value]
  }
  return null
})

const accuracyPercent = computed(() => {
  if (answeredCount.value === 0) return 0
  return Math.round((correctCount.value / answeredCount.value) * 100)
})

const accuracyColor = computed(() => {
  const pct = accuracyPercent.value
  if (pct >= 70) return '#67c23a'
  if (pct >= 40) return '#e6a23c'
  return '#f56c6c'
})

const timeSpent = computed(() => {
  const m = Math.floor(timer.value / 60)
  const s = timer.value % 60
  return `${m}分${s}秒`
})

const startBtnIcon = computed(() => {
  switch (mode.value) {
    case '专项练习': return 'fa-solid fa-book'
    case '模拟卷练习': return 'fa-solid fa-file-alt'
    case '错题重练': return 'fa-solid fa-rotate'
    default: return 'fa-solid fa-pen'
  }
})

const startBtnText = computed(() => {
  switch (mode.value) {
    case '专项练习': return '开始专项练习'
    case '模拟卷练习': return '开始模拟卷'
    case '错题重练': return '开始错题重练'
    default: return '开始答题'
  }
})

const isSaved = computed(() => {
  if (!currentQuestion.value) return false
  return savedQuestions.value.has(currentQuestion.value.id)
})

const questionTypeLabel = computed(() => {
  if (!currentQuestion.value) return ''
  switch (currentQuestion.value.question_type) {
    case 'single_choice': return '单选'
    case 'multi_choice': return '多选'
    case 'judge': return '判断'
    default: return ''
  }
})

const questionTypeIcon = computed(() => {
  switch (currentQuestion.value?.question_type) {
    case 'single_choice': return 'fa-dot-circle'
    case 'multi_choice': return 'fa-check-square'
    case 'judge': return 'fa-balance-scale'
    default: return 'fa-question-circle'
  }
})

const modeTagType = computed(() => {
  const map = { '专项练习': 'primary', '模拟卷练习': 'success', '错题重练': 'warning' }
  return map[mode.value] || 'info'
})

// 薄弱知识点
const weakPoints = computed(() => {
  const kpStats = {}
  for (const q of questions.value) {
    if (!q._result) continue
    const kp = q.knowledge_point || '其他'
    if (!kpStats[kp]) {
      kpStats[kp] = { total: 0, wrong: 0 }
    }
    kpStats[kp].total++
    if (!q._result.is_correct) {
      kpStats[kp].wrong++
    }
  }
  const result = Object.entries(kpStats)
    .filter(([, stats]) => stats.wrong > 0)
    .map(([name, stats]) => ({
      name,
      wrongRate: Math.round((stats.wrong / stats.total) * 100),
      wrong: stats.wrong,
      total: stats.total,
    }))
    .sort((a, b) => b.wrongRate - a.wrongRate)
    .slice(0, 3)
  return result
})

// ═══════════════════════════════════════════════
// 生命周期
// ═══════════════════════════════════════════════
onMounted(() => {
  loadFilterPreset()
})

onUnmounted(() => {
  stopTimer()
})

watch(career, (newCareer) => {
  if (newCareer) {
    loadKnowledgePoints(newCareer)
    if (mode.value === '错题重练') {
      loadWrongStats(newCareer)
    }
  }
})

watch(mode, (newMode) => {
  if (newMode === '错题重练' && career.value) {
    loadWrongStats(career.value)
  }
})

// ═══════════════════════════════════════════════
// 岗位选择
// ═══════════════════════════════════════════════
function selectCareer(c) {
  career.value = c
  onCareerChange()
}

// ═══════════════════════════════════════════════
// 解析选项
// ═══════════════════════════════════════════════
function parseOptions(json) {
  try {
    const p = typeof json === 'string' ? JSON.parse(json) : json
    if (Array.isArray(p)) return p
    if (p && typeof p === 'object') {
      return Object.entries(p).map(([k, v]) => ({ key: k, value: v }))
    }
    return []
  } catch {
    return []
  }
}

const parsedOptions = computed(() => {
  if (!currentQuestion.value) return []
  return parseOptions(currentQuestion.value.options_json || currentQuestion.value.options || [])
})

// ═══════════════════════════════════════════════
// 考点加载
// ═══════════════════════════════════════════════
async function loadKnowledgePoints(careerName) {
  try {
    const { data } = await axios.get('/api/exam/career-knowledge', {
      params: { career: careerName },
    })
    const kps = data.knowledge_points || data.data || []
    allKnowledgePoints.value = kps
    generalKnowledgePoints.value = kps.filter(kp => kp.type === 'general' || kp.type === '通用能力')
    professionalKnowledgePoints.value = kps.filter(kp => kp.type === 'professional' || kp.type === '专业能力')
    if (generalKnowledgePoints.value.length === 0 && professionalKnowledgePoints.value.length === 0) {
      allKnowledgePoints.value = kps
    }
  } catch (e) {
    console.error('加载考点失败', e)
    ElMessage.warning('加载考点失败，请稍后重试')
  }
}

// ═══════════════════════════════════════════════
// 错题统计
// ═══════════════════════════════════════════════
async function loadWrongStats(careerName) {
  try {
    const { data } = await axios.get('/api/exam/wrong-questions', {
      params: { career: careerName, page: 1, page_size: 1 },
    })
    const total = data.total || data.count || 0
    const unmastered = data.unmastered || data.unmastered_count || 0
    wrongStats.value = { total, unmastered }
  } catch (e) {
    console.error('加载错题统计失败', e)
    wrongStats.value = null
  }
}

// ═══════════════════════════════════════════════
// 筛选条件持久化
// ═══════════════════════════════════════════════
const PRESET_KEY = 'exam_filter_preset'

function saveFilterPreset() {
  const preset = {
    career: career.value,
    mode: mode.value,
    difficulty: difficulty.value,
    questionType: questionType.value,
    selectedKnowledgePoints: selectedKnowledgePoints.value,
    examCount: examCount.value,
    difficultyMap: difficultyMap.value,
    typeMap: typeMap.value,
  }
  try {
    localStorage.setItem(PRESET_KEY, JSON.stringify(preset))
  } catch (e) {
    // ignore
  }
}

function loadFilterPreset() {
  try {
    const raw = localStorage.getItem(PRESET_KEY)
    if (raw) {
      const preset = JSON.parse(raw)
      if (preset.career) career.value = preset.career
      if (preset.mode) mode.value = preset.mode
      if (preset.difficulty) difficulty.value = preset.difficulty
      if (preset.questionType) questionType.value = preset.questionType
      if (preset.selectedKnowledgePoints) selectedKnowledgePoints.value = preset.selectedKnowledgePoints
      if (preset.examCount) examCount.value = preset.examCount
      if (preset.difficultyMap) difficultyMap.value = preset.difficultyMap
      if (preset.typeMap) typeMap.value = preset.typeMap
    }
  } catch (e) {
    // ignore
  }
}

// ═══════════════════════════════════════════════
// 计时器
// ═══════════════════════════════════════════════
function startTimer() {
  timer.value = 0
  timerInterval = setInterval(() => {
    timer.value++
  }, 1000)
}

function stopTimer() {
  if (timerInterval) {
    clearInterval(timerInterval)
    timerInterval = null
  }
}

function formatTime(seconds) {
  const m = String(Math.floor(seconds / 60)).padStart(2, '0')
  const s = String(seconds % 60).padStart(2, '0')
  return `${m}:${s}`
}

// ═══════════════════════════════════════════════
// 难度/题型辅助
// ═══════════════════════════════════════════════
function difficultyPillClass(diff) {
  switch (diff) {
    case 'easy': return 'green'
    case 'medium': return 'orange'
    case 'hard': return 'red'
    default: return 'gray'
  }
}

function difficultyLabel(diff) {
  switch (diff) {
    case 'easy': return '简单'
    case 'medium': return '中等'
    case 'hard': return '困难'
    default: return diff
  }
}

function scoreColor(v) {
  return v >= 80 ? '#67c23a' : v >= 60 ? '#e6a23c' : '#f56c6c'
}

// ═══════════════════════════════════════════════
// 岗位变更
// ═══════════════════════════════════════════════
function onCareerChange() {
  selectedKnowledgePoints.value = []
  difficultyMap.value = {}
  typeMap.value = {}
}

// ═══════════════════════════════════════════════
// 跳转题目
// ═══════════════════════════════════════════════
function jumpToQuestion(index) {
  if (index >= 0 && index < questions.value.length) {
    currentIndex.value = index
    selectedOption.value = ''
    multiSelected.value = []
    answerResult.value = null
    const q = questions.value[index]
    if (q._result) {
      answerResult.value = q._result
      selectedOption.value = q._userAnswer || ''
    }
  }
}

// ═══════════════════════════════════════════════
// 开始答题
// ═══════════════════════════════════════════════
async function startExam() {
  if (!career.value) {
    ElMessage.warning('请先选择目标岗位')
    return
  }

  saveFilterPreset()

  startLoading.value = true
  isLoading.value = true
  loadError.value = ''
  loadMsg.value = ''
  answeredCount.value = 0
  correctCount.value = 0
  currentIndex.value = 0
  answerResult.value = null
  selectedOption.value = ''
  multiSelected.value = []
  questions.value = []
  draftNote.value = ''

  phase.value = 'doing'
  startTimer()

  try {
    if (mode.value === '错题重练') {
      await loadWrongQuestions()
    } else {
      await loadGeneratedQuestions()
    }
  } catch (e) {
    console.error('加载题目失败', e)
    loadError.value = '加载题目失败：' + (e.message || '请检查网络连接')
    ElMessage.error('获取题目失败')
  } finally {
    startLoading.value = false
    isLoading.value = false
  }
}

async function loadGeneratedQuestions() {
  loadMsg.value = '正在加载第 1 题…'

  let kp = ''
  if (mode.value === '专项练习') {
    kp = selectedKnowledgePoints.value.join(',')
    if (!kp) {
      kp = allKnowledgePoints.value.map(p => p.name).join(',')
    }
  }

  let params = {
    career: career.value,
    mode: mode.value,
    count: mode.value === '模拟卷练习' ? examCount.value : 10,
  }

  if (mode.value === '专项练习') {
    params.knowledge_point = kp
    if (selectedKnowledgePoints.value.length > 0) {
      const firstKp = selectedKnowledgePoints.value[0]
      params.difficulty = difficultyMap.value[firstKp] || difficulty.value || ''
      params.question_type = typeMap.value[firstKp] || questionType.value || ''
    } else {
      params.difficulty = difficulty.value || ''
      params.question_type = questionType.value || ''
    }
  } else if (mode.value === '模拟卷练习') {
    params.difficulty = difficulty.value || ''
    params.question_type = 'all'
  }

  const { data } = await axios.get('/api/exam/generate', { params })

  let rawQuestions = data.questions || data.data || []
  if (!Array.isArray(rawQuestions)) rawQuestions = []

  if (rawQuestions.length === 0) {
    questions.value = []
    loadMsg.value = ''
    return
  }

  questions.value = rawQuestions.map(q => ({
    ...q,
    _result: null,
    _userAnswer: null,
  }))

  loadMsg.value = ''
}

async function loadWrongQuestions() {
  loadMsg.value = '正在拉取错题…'

  const params = {
    career: career.value,
    page: 1,
    page_size: 20,
  }
  if (wrongFilterKnowledge.value) {
    params.knowledge_point = wrongFilterKnowledge.value
  }
  if (difficulty.value) {
    params.difficulty = difficulty.value
  }

  const { data } = await axios.get('/api/exam/wrong-questions', { params })

  let rawQuestions = data.questions || data.data || data.items || []
  if (!Array.isArray(rawQuestions)) rawQuestions = []

  if (rawQuestions.length === 0) {
    questions.value = []
    ElMessage.info('暂无错题，试试其他筛选条件')
    loadMsg.value = ''
    return
  }

  questions.value = rawQuestions.map(q => ({
    ...q,
    _result: null,
    _userAnswer: null,
  }))

  loadMsg.value = ''
}

function retryLoad() {
  loadError.value = ''
  isLoading.value = true
  startExam()
}

// ═══════════════════════════════════════════════
// 提交答案
// ═══════════════════════════════════════════════
async function submitAnswer(selected) {
  if (answerResult.value || !currentQuestion.value) return

  selectedOption.value = selected
  const q = currentQuestion.value

  try {
    const { data } = await axios.post('/api/exam/submit', {
      question_id: q.id,
      user_answer: selected,
      career: career.value,
      question: q.question,
      options_json: q.options_json || '',
      analysis: q.analysis || '',
      question_type: q.question_type,
      difficulty: q.difficulty || 'medium',
    })

    answerResult.value = data
    q._result = data
    q._userAnswer = selected
    answeredCount.value++
    if (data.is_correct) {
      correctCount.value++
      ElMessage.success('回答正确！')
    } else {
      ElMessage.warning('回答错误，查看解析')
    }

    if (mode.value === '错题重练' && q.id) {
      try {
        await axios.post(`/api/exam/wrong-questions/reanswer/${q.id}`, {
          is_correct: data.is_correct,
          user_answer: selected,
        })
      } catch (e) {
        // 可选失败，不阻塞
      }
    }
  } catch (e) {
    ElMessage.error('提交答案失败')
    selectedOption.value = ''
  }
}

function toggleMultiSelect(key) {
  if (answerResult.value) return
  const idx = multiSelected.value.indexOf(key)
  if (idx >= 0) {
    multiSelected.value.splice(idx, 1)
  } else {
    multiSelected.value.push(key)
  }
}

async function submitMultiAnswer() {
  if (answerResult.value || !currentQuestion.value || multiSelected.value.length === 0) return
  const answer = multiSelected.value.sort().join(',')
  await submitAnswer(answer)
}

// ═══════════════════════════════════════════════
// CSS 类辅助
// ═══════════════════════════════════════════════
function optionClass(key) {
  if (!answerResult.value) {
    return { selected: selectedOption.value === key }
  }
  const correct = answerResult.value.correct_answer || ''
  const correctKeys = correct.split(',').map(k => k.trim())
  return {
    selected: selectedOption.value === key,
    correct: correctKeys.includes(key),
    wrong: selectedOption.value === key && !correctKeys.includes(key),
  }
}

function multiOptionClass(key) {
  if (!answerResult.value) {
    return { selected: multiSelected.value.includes(key) }
  }
  const correct = answerResult.value.correct_answer || ''
  const correctKeys = correct.split(',').map(k => k.trim())
  return {
    selected: multiSelected.value.includes(key),
    correct: correctKeys.includes(key),
    wrong: multiSelected.value.includes(key) && !correctKeys.includes(key),
  }
}

function judgeClass(value) {
  if (!answerResult.value) {
    return { selected: selectedOption.value === value }
  }
  const correct = answerResult.value.correct_answer || ''
  return {
    selected: selectedOption.value === value,
    correct: correct === value,
    wrong: selectedOption.value === value && correct !== value,
  }
}

// ═══════════════════════════════════════════════
// 下一题 / 收藏
// ═══════════════════════════════════════════════
function nextQuestion() {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
    selectedOption.value = ''
    multiSelected.value = []
    answerResult.value = null
  }
}

async function saveCurrentQuestion() {
  if (!currentQuestion.value) return
  const q = currentQuestion.value
  if (savedQuestions.value.has(q.id)) return

  try {
    await axios.post('/api/exam/saved-questions', {
      question_id: q.id,
      career: career.value,
      question: q.question,
      options_json: q.options_json || '',
      analysis: q.analysis || '',
      question_type: q.question_type,
      difficulty: q.difficulty || 'medium',
      source: 'exam',
      knowledge_point: q.knowledge_point || '',
    })
    savedQuestions.value.add(q.id)
    ElMessage.success('已收藏')
  } catch (e) {
    ElMessage.error('收藏失败')
  }
}

// ═══════════════════════════════════════════════
// 结束答题
// ═══════════════════════════════════════════════
function confirmEndExam() {
  ElMessageBox.confirm(
    '确定要结束本次练习吗？已答的题目将会保存记录。',
    '确认结束',
    { confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning' }
  ).then(() => {
    finishExam()
  }).catch(() => {})
}

async function finishExam() {
  stopTimer()

  // 构建带有完整信息的答题记录
  const answers = questions.value.map(q => ({
    question_id: q.id,
    question: q.question,
    knowledge_point: q.knowledge_point || '',
    difficulty: q.difficulty || '',
    question_type: q.question_type || '',
    options_json: q.options_json || '',
    user_answer: q._userAnswer || '',
    correct_answer: q._result ? q._result.correct_answer : '',
    correct: q._result ? q._result.is_correct : false,
    analysis: q.analysis || (q._result ? q._result.analysis : ''),
  }))

  let recordResult = null
  try {
    const { data } = await axios.post('/api/exam/record', {
      career: career.value,
      mode: mode.value,
      answers,
      duration_seconds: timer.value,
    })
    recordResult = data
  } catch (e) {
    console.error('保存记录失败', e)
  }

  examResult.value = recordResult
  phase.value = 'done'
}

// ═══════════════════════════════════════════════
// 完成页操作
// ═══════════════════════════════════════════════
function doAnotherRound() {
  phase.value = 'ready'
  setupStep.value = 1
  questions.value = []
  currentIndex.value = 0
  answerResult.value = null
  selectedOption.value = ''
  multiSelected.value = []
  answeredCount.value = 0
  correctCount.value = 0
  timer.value = 0
  savedQuestions.value = new Set()
  draftNote.value = ''
}

function goToWrongQuestions() {
  router.push('/exam/wrong')
}

function backToEntry() {
  router.push('/exam-practice')
}

function backToReady() {
  doAnotherRound()
}
</script>

<style scoped>
/* ==================== CSS Variables ==================== */
.exam-page {
  --exam-bg: linear-gradient(135deg, #EEF2FF, #F8FAFF);
  --exam-card-bg: #ffffff;
  --exam-border: #BFDBFE;
  --exam-text: #475569;
  --exam-text-muted: #94A3B8;
  --exam-shadow: 0 12px 30px rgba(37,99,235,.07);
  --exam-radius: 18px;
}

/* ==================== Full-width Layout ==================== */
.exam-page {
  width: 100%;
  min-height: 100vh;
  padding: 0 0 2rem;
  background: var(--exam-bg);
}
.exam-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 1.2rem 0.8rem;
  color: var(--text-heading);
}
.back-circle-btn {
  display: inline-flex !important;
  align-items: center;
  gap: 6px;
  padding: 8px 18px 8px 14px !important;
  border: 2px solid #BFDBFE !important;
  border-radius: 999px !important;
  background: #fff !important;
  color: var(--primary) !important;
  font-weight: 800 !important;
  font-size: 0.95rem !important;
  box-shadow: 0 2px 6px rgba(37,99,235,.08) !important;
  transition: all 0.2s !important;
}
.back-circle-btn:hover {
  border-color: var(--primary) !important;
  box-shadow: 0 4px 12px rgba(37,99,235,.14) !important;
}
.exam-topbar :deep(.el-button) {
  color: var(--primary);
  font-weight: 800;
}
.exam-title {
  font-weight: 600;
  font-size: 1rem;
  color: var(--text-heading, #333);
}
.exam-title i {
  margin-right: 6px;
  color: var(--primary, #2563EB);
}
.topbar-actions {
  display: flex;
  gap: 8px;
}
.section-panel {
  min-height: 200px;
}

/* ==================== Setup Stage ==================== */
.setup-stage {
  padding: 4px 0 18px;
  background: linear-gradient(180deg, #EFF6FF 0%, #F8FAFC 120px);
  min-height: calc(100vh - 64px);
  display: flex;
  align-items: center;
  justify-content: center;
}
.setup-shell {
  width: min(1280px, calc(100vw - 48px));
  margin: 0 auto;
  display: grid;
  grid-template-columns: 360px minmax(0, 1fr);
  gap: 28px;
  align-items: stretch;
}
.setup-side {
  position: relative;
  overflow: hidden;
  padding: 28px 24px;
  border-radius: 26px 10px 26px 26px;
  background: linear-gradient(155deg, #EFF6FF 0%, #FFFFFF 72%);
  border: 1.5px dashed #93C5FD;
  box-shadow: 0 18px 40px rgba(37,99,235,.08);
}
.setup-side::after {
  content: '';
  position: absolute;
  right: -42px;
  bottom: -42px;
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: rgba(37,99,235,.08);
}
.setup-side-kicker {
  color: var(--primary);
  font-size: 15px;
  font-weight: 900;
  letter-spacing: .12em;
}
.setup-side h1 {
  margin: 14px 0 10px;
  color: var(--text-heading);
  font-size: 31px;
  line-height: 1.24;
  font-weight: 900;
}
.setup-side p {
  color: var(--text-light);
  font-size: 15px;
  line-height: 1.75;
}
.setup-steps {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 28px;
}
.setup-step {
  display: grid;
  grid-template-columns: 42px minmax(0,1fr);
  grid-template-areas: 'num title' 'num desc';
  gap: 0 12px;
  width: 100%;
  padding: 14px;
  border: 1px solid #DBEAFE;
  border-radius: 18px;
  background: rgba(255,255,255,.78);
  text-align: left;
  font: inherit;
  cursor: pointer;
}
.setup-step:disabled {
  cursor: not-allowed;
  opacity: .55;
}
.setup-step span {
  grid-area: num;
  width: 42px;
  height: 42px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  background: #EFF6FF;
  color: var(--primary);
  font-weight: 900;
}
.setup-step b {
  grid-area: title;
  color: var(--text-heading);
  font-size: 17px;
  font-weight: 900;
}
.setup-step small {
  grid-area: desc;
  color: var(--text-muted);
  font-size: 13px;
}
.setup-step.active {
  border-color: #93C5FD;
  background: #fff;
  box-shadow: 8px 8px 18px rgba(147,197,253,.16), -8px -8px 18px rgba(255,255,255,.86);
}
.setup-step.done span {
  background: var(--primary);
  color: #fff;
}
.setup-main-card {
  min-height: 540px;
  padding: 32px 36px;
  border-radius: 10px 26px 26px 26px;
  background: #fff;
  border: 1.5px dashed #BFDBFE;
  box-shadow: 0 18px 40px rgba(37,99,235,.06);
}
.setup-main-head {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  align-items: flex-start;
  margin-bottom: 24px;
  padding-bottom: 18px;
  border-bottom: 1px dashed #DBEAFE;
}
.setup-breadcrumb {
  color: var(--primary);
  font-size: 13px;
  font-weight: 900;
  letter-spacing: .08em;
}
.setup-main-head h2 {
  margin-top: 7px;
  color: var(--text-heading);
  font-size: 26px;
  line-height: 1.35;
  font-weight: 900;
}
.setup-mini-badge {
  flex: none;
  max-width: 170px;
  padding: 9px 14px;
  border-radius: 999px;
  background: var(--primary-light);
  border: 1px solid #BFDBFE;
  color: var(--primary);
  font-size: 14px;
  font-weight: 900;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.setup-step-content {
  min-height: 370px;
  display: flex;
  flex-direction: column;
}

/* ─── Career Hero ─── */
.career-hero {
  position: relative;
  overflow: hidden;
  margin-bottom: 18px;
  padding: 20px 22px;
  border-radius: 22px 8px 22px 22px;
  background:
    radial-gradient(circle at 14% 18%, rgba(14,165,233,.13), transparent 28%),
    linear-gradient(135deg, #EFF6FF 0%, #FFFFFF 72%);
  border: 1.5px dashed #BFDBFE;
}
.custom-kicker {
  color: var(--primary);
  font-size: 12px;
  font-weight: 900;
  letter-spacing: .16em;
}
.career-hero h3 {
  margin: 8px 0 6px;
  color: var(--text-heading);
  font-size: 22px;
  line-height: 1.35;
  font-weight: 900;
}
.career-hero p {
  max-width: 680px;
  color: var(--text-light);
  font-size: 14px;
  line-height: 1.7;
}
.custom-paper-mark {
  position: absolute;
  right: 18px;
  bottom: -8px;
  color: rgba(37,99,235,.08);
  font-size: 54px;
  font-weight: 900;
  letter-spacing: .08em;
}

/* ─── Setup Form ─── */
.setup-nav {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: auto;
  padding-top: 1.2rem;
}
.final-nav {
  border-top: 1px dashed #DBEAFE;
  margin-top: 14px;
}

/* ─── Mode Radio ─── */
.mode-radio-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}
.mode-radio-group :deep(.el-radio-button) {
  width: 100%;
}
.mode-radio-group :deep(.el-radio-button__inner) {
  width: 100%;
  text-align: left;
  border-radius: 8px !important;
  padding: 12px 16px;
  height: auto;
  border-left: 1px solid var(--border, #dcdfe6);
}
.mode-option {
  display: flex;
  align-items: center;
  gap: 12px;
}
.mode-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
  width: 32px;
  text-align: center;
  color: var(--primary, #2563EB);
}
.mode-desc {
  font-size: 0.75rem;
  color: var(--text-muted, #999);
  margin: 2px 0 0;
  font-weight: 400;
}

/* ─── Setup Summary ─── */
.setup-summary {
  background: #F8FBFF;
  border-radius: 14px;
  padding: 16px 18px;
  margin-bottom: 12px;
  border: 1px solid #DBEAFE;
}
.setup-summary p {
  margin: 4px 0;
  font-size: 0.9rem;
  color: var(--text-body);
}
.setup-summary p i {
  margin-right: 6px;
  color: var(--primary);
  width: 18px;
}
.setup-summary b {
  color: var(--text-heading);
}

/* ─── KP Rows ─── */
.kp-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 8px;
  border-radius: 8px;
  transition: background 0.2s;
  margin-bottom: 4px;
}
.kp-row:hover {
  background: #EFF6FF;
}
.kp-filters {
  display: flex;
  gap: 6px;
}
.no-kp-tip {
  color: var(--text-muted, #999);
  font-size: 0.85rem;
  padding: 8px 0;
}
.no-kp-tip i {
  margin-right: 4px;
}

/* ─── Wrong Stats ─── */
.wrong-stats-card {
  display: flex;
  gap: 2rem;
  padding: 12px 16px;
  background: #fff7e6;
  border-radius: 12px;
  margin-bottom: 12px;
}
.wrong-stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.stat-label {
  font-size: 0.8rem;
  color: var(--text-muted, #999);
}
.stat-label i {
  margin-right: 4px;
}
.stat-value {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--primary);
}
.stat-value.warn {
  color: #e6a23c;
}

/* ==================== Exam Phase (Doing) ==================== */
.exam-phase {
  width: min(1280px, calc(100vw - 48px));
  margin: 0 auto;
  padding: 20px 12px;
  position: relative;
}

/* ═══ Decorative background elements ═══ */
.exam-phase::before {
  content: '';
  position: absolute;
  right: -80px;
  top: 60px;
  width: 260px;
  height: 260px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(37,99,235,.05) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}
.exam-phase::after {
  content: '';
  position: absolute;
  left: -60px;
  bottom: 80px;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(191,219,254,.12) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* ─── Exam Status Bar ─── */
.exam-status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: rgba(255,255,255,.9);
  border-radius: 18px;
  margin-bottom: 0.9rem;
  box-shadow: 0 16px 36px rgba(37,99,235,.06);
  gap: 12px;
  border: 1.5px dashed #bfdbfe;
}
.it-left {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}
.it-career {
  font-weight: 600;
  font-size: 0.85rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 120px;
}
.it-center {
  display: flex;
  align-items: center;
  gap: 8px;
}
.countdown-timer {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 1rem;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  color: var(--text-heading, #333);
  padding: 2px 10px;
  background: #EFF6FF;
  border: 1px solid #DBEAFE;
  border-radius: 999px;
}
.round-badge {
  font-size: 0.78rem;
  color: var(--exam-text-muted);
  background: #EFF6FF;
  border: 1px solid #DBEAFE;
  padding: 3px 10px;
  border-radius: 999px;
}
.it-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

/* ─── Exam Layout ─── */
.exam-layout {
  flex: 1;
  display: flex;
  gap: 16px;
  min-height: 0;
  overflow: hidden;
}
.exam-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* ─── Skeleton ─── */
.loading-section {
  padding: 1rem 0;
}
.skeleton-card {
  background: #fff;
  border-radius: 18px;
  padding: 1.5rem;
  border: 1.5px dashed #bfdbfe;
  box-shadow: 0 16px 36px rgba(37, 99, 235, 0.06);
}
.skeleton-line {
  background: linear-gradient(90deg, #f0f0f0 25%, #e8e8e8 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 6px;
  margin-bottom: 12px;
}
.skeleton-tag { height: 22px; width: 60px; }
.skeleton-title { height: 16px; width: 35%; }
.skeleton-text { height: 13px; width: 85%; }
.skeleton-text.short { width: 55%; }
.skeleton-options { margin-top: 16px; }
.skeleton-option { height: 44px; width: 100%; border-radius: 10px; }
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
.loading-text {
  text-align: center;
  margin-top: 1.5rem;
  color: var(--text-muted, #999);
}
.load-msg {
  margin-top: 6px;
  font-size: 0.85rem;
  color: var(--text-muted, #999);
}
.load-error {
  color: #f56c6c;
  margin-top: 12px;
}

/* ─── Question Card ─── */
.question-card {
  border-radius: 18px;
  padding: 1.5rem;
  background: #fff;
  border: 1.5px dashed #bfdbfe;
  box-shadow: 0 16px 36px rgba(37, 99, 235, 0.06);
  position: relative;
}
.question-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #2563EB, #93C5FD, transparent);
  border-radius: 18px 18px 0 0;
  pointer-events: none;
}

/* Tags */
.q-tags {
  display: flex;
  gap: 6px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
.q-type-tag {
  font-weight: 600;
}
.tag-pill {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 600;
}
.tag-pill.blue { background: #EFF6FF; color: var(--primary); }
.tag-pill.orange { background: #fff7e6; color: #e6a23c; }
.tag-pill.green { background: #f0fff0; color: #67c23a; }
.tag-pill.red { background: #fff0f0; color: #f56c6c; }
.tag-pill.gray { background: #f5f5f5; color: #999; }
.tag-pill i {
  font-size: 0.75rem;
}

.q-heading {
  font-size: 1rem;
  font-weight: 600;
  color: var(--primary);
  margin-bottom: 8px;
}
.q-heading i {
  margin-right: 6px;
}
.q-text {
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--text-body, #333);
  margin-bottom: 1rem;
  white-space: pre-wrap;
}

/* Options */
.options-wrap {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}
.option-item {
  padding: 0.7rem 1rem;
  border: 2px solid #DBEAFE;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
}
.option-item:hover {
  border-color: var(--primary);
  background: #EFF6FF;
}
.option-item.selected {
  border-color: var(--primary);
  background: #EFF6FF;
}
.option-item.correct {
  border-color: #67c23a;
  background: #f0fff0;
}
.option-item.wrong {
  border-color: #f56c6c;
  background: #fff0f0;
}
.opt-key {
  font-weight: 700;
  color: var(--primary);
  min-width: 24px;
}
.opt-text {
  font-size: 0.9rem;
  flex: 1;
}
.opt-check-icon {
  margin-left: auto;
  color: var(--primary);
}
.opt-checkbox {
  min-width: 20px;
  font-size: 1rem;
}

/* Multi submit */
.multi-submit-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
  padding-left: 4px;
}
.multi-hint {
  font-size: 0.8rem;
  color: var(--text-muted, #999);
}

/* Judge */
.judge-wrap {
  margin-top: 0.5rem;
}
.judge-options {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
}
.judge-item {
  padding: 1rem 2.5rem;
  border: 2px solid #DBEAFE;
  border-radius: 14px;
  cursor: pointer;
  font-size: 1.1rem;
  font-weight: 600;
  transition: all 0.2s;
  min-width: 120px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}
.judge-item:hover {
  border-color: var(--primary);
  background: #EFF6FF;
}
.judge-item.selected {
  border-color: var(--primary);
  background: #EFF6FF;
}
.judge-item.correct {
  border-color: #67c23a;
  background: #f0fff0;
}
.judge-item.wrong {
  border-color: #f56c6c;
  background: #fff0f0;
}

/* Feedback */
.feedback-section {
  margin-top: 1rem;
}
.feedback-correct {
  margin-top: 8px;
  font-size: 0.9rem;
  color: #67c23a;
}
.feedback-correct i {
  margin-right: 4px;
}
.analysis-box {
  background: #F8FBFF;
  border-radius: 12px;
  padding: 0.8rem;
  margin-top: 8px;
}
.analysis-box h4 {
  margin: 0 0 0.4rem 0;
  font-size: 0.9rem;
  color: var(--primary);
}
.analysis-box h4 i {
  margin-right: 6px;
}
.analysis-box p {
  font-size: 0.85rem;
  color: var(--text-body, #555);
  line-height: 1.6;
  margin: 0;
}
.hint-box {
  background: #EFF6FF;
  border-left: 3px solid var(--primary);
}
.hint-box p {
  color: var(--text-heading, #333);
}
.hint-box i {
  margin-right: 4px;
  color: var(--primary);
}

/* Actions */
.q-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 0.8rem;
  border-top: 1px solid #DBEAFE;
}
.q-actions-right {
  display: flex;
  gap: 8px;
}
.q-actions i {
  margin-right: 4px;
}
.q-actions-right i {
  margin-left: 4px;
  margin-right: 0;
}

/* Draft */
.draft-collapse {
  margin-top: 12px;
}

/* Empty state */
.empty-state {
  text-align: center;
  padding: 3rem 0;
  color: var(--text-muted, #999);
}

/* ==================== Sidebar ==================== */
.exam-sidebar {
  width: 200px;
  flex-shrink: 0;
}
.sidebar-card {
  background: #fff;
  border-radius: 20px;
  padding: 1rem;
  border: 1.5px dashed #bfdbfe;
  box-shadow: 0 16px 36px rgba(37, 99, 235, 0.06);
}
.sidebar-title {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-heading, #333);
  margin-bottom: 0.8rem;
  text-align: center;
}
.sidebar-title i {
  margin-right: 6px;
  color: var(--primary);
}
.sidebar-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 0.8rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid #DBEAFE;
}
.sidebar-stat-item {
  text-align: center;
}
.sidebar-stat-num {
  display: block;
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-heading, #333);
}
.sidebar-stat-label {
  font-size: 0.7rem;
  color: var(--text-muted, #999);
}
.sidebar-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 4px;
  margin-bottom: 0.8rem;
}
.sidebar-grid-item {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  background: #f5f5f5;
  color: var(--text-muted, #999);
  border: 2px solid transparent;
  transition: all 0.15s ease;
}
.sidebar-grid-item:hover {
  border-color: var(--primary);
  color: var(--primary);
}
.sidebar-grid-item.grid-current {
  border-color: var(--primary);
  background: #EFF6FF;
  color: var(--primary);
}
.sidebar-grid-item.grid-answered {
  background: #e8f5e9;
  color: #67c23a;
  border-color: #c8e6c9;
}
.sidebar-grid-item.grid-correct {
  background: #e8f5e9;
  color: #67c23a;
  border-color: #c8e6c9;
}
.sidebar-grid-item.grid-wrong {
  background: #ffebee;
  color: #f56c6c;
  border-color: #ffcdd2;
}
.sidebar-grid-item.grid-current.grid-answered {
  border-color: var(--primary);
}
.sidebar-legend {
  display: flex;
  gap: 8px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 0.8rem;
}
.legend-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 0.7rem;
  color: var(--text-muted, #999);
}
.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
}
.dot-answered { background: #e8f5e9; border: 1px solid #c8e6c9; }
.dot-current { background: #EFF6FF; border: 2px solid var(--primary); }
.dot-unanswered { background: #f5f5f5; border: 1px solid #ddd; }
.sidebar-actions {
  margin-top: 0.5rem;
}

/* ==================== Report ==================== */
.report-card {
  border-radius: var(--exam-radius);
  max-width: 960px;
  margin: 0 auto;
  border: 1.5px dashed var(--exam-border) !important;
  box-shadow: var(--exam-shadow) !important;
}
.report-top-info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 0.5rem;
  font-size: 0.85rem;
}
.report-job {
  font-weight: 600;
}
.report-rounds {
  color: var(--text-muted, #999);
  font-size: 0.78rem;
}
.overall-score-area {
  text-align: center;
  padding: 1rem 0;
}
.overall-score-area h3 {
  margin-top: 0.6rem;
}
.report-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.8rem;
  margin: 1rem 0;
}
.report-stat-card {
  background: #F8FBFF;
  border-radius: 12px;
  padding: 0.8rem;
  text-align: center;
  border: 1px solid #DBEAFE;
}
.report-stat-num {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--text-heading);
}
.report-stat-label {
  font-size: 0.78rem;
  color: var(--text-muted, #999);
  margin-top: 4px;
}

/* Weak points */
.weak-section {
  text-align: left;
}
.weak-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 0 0.5rem;
}
.weak-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: #fff7e6;
  border-radius: 12px;
  border: 1px solid #ffe58f;
}
.weak-rank {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
}
.weak-name {
  flex: 1;
  font-weight: 500;
}
.weak-rate {
  font-size: 0.85rem;
  color: #e6a23c;
  font-weight: 600;
}

/* Report actions */
.report-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  padding-top: 1.5rem;
}

/* ==================== Transitions ==================== */
.exam-fade-enter-active,
.exam-fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.exam-fade-enter-from {
  opacity: 0;
  transform: translateY(12px);
}
.exam-fade-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}

/* ==================== Responsive ==================== */
@media (max-width: 900px) {
  .setup-shell {
    width: calc(100vw - 32px);
    grid-template-columns: 1fr;
  }
  .setup-side h1 { font-size: 26px; }
  .exam-layout {
    flex-direction: column;
  }
  .exam-sidebar {
    width: 100%;
    order: 2;
  }
  .exam-main {
    order: 1;
  }
}
@media (max-width: 768px) {
  .exam-topbar {
    padding: 0.6rem 0.75rem;
  }
  .exam-status-bar {
    font-size: 0.78rem;
    padding: 0.5rem 0.8rem;
    flex-wrap: wrap;
    gap: 4px;
  }
  .report-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  .report-actions {
    flex-direction: column;
    align-items: center;
  }
  .report-actions .el-button {
    width: 100%;
    max-width: 280px;
  }
  .judge-options {
    flex-direction: column;
    gap: 0.8rem;
  }
  .judge-item {
    padding: 0.8rem 1.5rem;
    min-width: unset;
  }
  .q-actions {
    flex-direction: column;
    gap: 8px;
  }
  .q-actions-right {
    width: 100%;
  }
  .q-actions-right .el-button {
    flex: 1;
  }
  .exam-sidebar {
    width: 100%;
  }
  .sidebar-grid {
    grid-template-columns: repeat(10, 1fr);
  }
}

/* ═══════ 报告页新元素 ═══════ */
.learning-tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.question-detail-item {
  border: 1px dashed #e2e8f0;
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 8px;
  background: #fafbfc;
}
.qdi-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}
.qdi-num {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #2563eb;
  color: #fff;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 600;
}
.qdi-question {
  font-size: 14px;
  color: #1e293b;
  margin-bottom: 6px;
  line-height: 1.5;
}
.qdi-answer {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 6px;
}
.wrong-ans { color: #ef4444; }
.correct-ans { color: #10b981; }
.qdi-analysis {
  font-size: 13px;
  color: #475569;
  background: #f1f5f9;
  padding: 8px 10px;
  border-radius: 6px;
  line-height: 1.5;
}
</style>