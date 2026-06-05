<template>
  <div class="exam-page">
    <!-- ═══════ 顶部栏 ═══════ -->
    <div class="exam-topbar">
      <el-button text @click="backToEntry">
        <ArrowLeft :size="16" class="icon-blue" /> 返回
      </el-button>
      <span class="exam-title">
        <Pen :size="16" class="icon-blue" /> 笔试专项练习
      </span>
      <span v-if="phase === 'doing'" class="topbar-end">
        <el-button size="small" type="danger" plain @click="confirmEndExam">
          <StopCircle :size="16" class="icon-blue" /> 结束
        </el-button>
      </span>
    </div>

    <!-- ════════════════ Phase 1: 设置页 ════════════════ -->
    <div v-if="phase === 'ready'" class="phase-ready">
      <div class="card setup-card">
        <div class="setup-header">
          <div class="section-header">
            <h3 class="section-title">
              <Settings :size="16" class="icon-blue" /> 笔试设置
            </h3>
          </div>
          <el-alert
            title="先选目标岗位，再选练习模式，AI 会为您匹配相应题目"
            type="info"
            :closable="false"
            show-icon
            style="margin-top:8px;font-size:0.8rem" />
        </div>

        <el-form label-position="top" class="setup-form">
          <!-- 第一层：目标岗位 -->
          <el-form-item label="目标岗位（必填）">
            <template #label>
              <span><Crosshair :size="16" class="icon-blue" /> 目标岗位（必填）</span>
            </template>
            <el-select
              v-model="career"
              placeholder="选择目标岗位，决定出题方向"
              style="width:100%"
              @change="onCareerChange"
              filterable>
              <el-option-group v-if="store.validBookmarks.length" label="已收藏">
                <template #label>
                  <span><Star :size="16" :color="'#e6a23c'" /> 已收藏</span>
                </template>
                <el-option
                  v-for="b in store.validBookmarks"
                  :key="b.career"
                  :label="b.career"
                  :value="b.career" />
              </el-option-group>
              <el-option-group
                v-for="group in careerGroups"
                :key="group.label"
                :label="group.label">
                <el-option
                  v-for="c in group.list"
                  :key="c"
                  :label="c"
                  :value="c" />
              </el-option-group>
            </el-select>
          </el-form-item>

          <!-- 第二层：练习模式 -->
          <el-form-item label="练习模式">
            <template #label>
              <span><Pin :size="16" class="icon-blue" /> 练习模式</span>
            </template>
            <el-radio-group v-model="mode" class="mode-radio-group">
              <el-radio-button value="专项练习">
                <Book :size="16" class="icon-blue" /> 专项练习
              </el-radio-button>
              <el-radio-button value="模拟卷练习">
                <FileText :size="16" class="icon-blue" /> 模拟卷练习
              </el-radio-button>
              <el-radio-button value="错题重练">
                <Redo :size="16" class="icon-blue" /> 错题重练
              </el-radio-button>
            </el-radio-group>
          </el-form-item>

          <!-- 第三层：筛选条件（动态） -->

          <!-- ─── 专项练习 ‐ 考点+难度+题型 ─── -->
          <template v-if="mode === '专项练习'">
            <el-divider content-position="left">
              <span class="divider-title fa-green">
                <Circle :size="0" :color="'#52c41a'" style="vertical-align:middle" /> 通用能力题
              </span>
            </el-divider>
            <div v-if="generalKnowledgePoints.length === 0" class="no-kp-tip">
              <Info :size="16" class="icon-blue" /> 暂无通用能力考点数据，请先选择目标岗位
            </div>
            <div v-for="kp in generalKnowledgePoints" :key="kp.id" class="kp-row">
              <el-checkbox v-model="selectedKnowledgePoints" :label="kp.name" :value="kp.name">
                {{ kp.name }}
              </el-checkbox>
              <div class="kp-filters">
                <el-select
                  v-model="difficultyMap[kp.name]"
                  placeholder="难度"
                  size="small"
                  clearable
                  style="width:110px">
                  <el-option label="入门" value="easy" />
                  <el-option label="基础" value="medium" />
                  <el-option label="进阶" value="hard" />
                  <el-option label="挑战" value="all" />
                </el-select>
                <el-select
                  v-model="typeMap[kp.name]"
                  placeholder="题型"
                  size="small"
                  clearable
                  style="width:110px">
                  <el-option label="单选题" value="single_choice" />
                  <el-option label="多选题" value="multi_choice" />
                  <el-option label="判断题" value="judge" />
                  <el-option label="不限" value="all" />
                </el-select>
              </div>
            </div>

            <el-divider content-position="left">
              <span class="divider-title fa-blue">
                <Circle :size="0" :color="'#3D5A80'" style="vertical-align:middle" /> 专业能力题
              </span>
            </el-divider>
            <div v-if="professionalKnowledgePoints.length === 0" class="no-kp-tip">
              <Info :size="16" class="icon-blue" /> 暂无专业能力考点数据，请先选择目标岗位
            </div>
            <div v-for="kp in professionalKnowledgePoints" :key="kp.id" class="kp-row">
              <el-checkbox v-model="selectedKnowledgePoints" :label="kp.name" :value="kp.name">
                {{ kp.name }}
              </el-checkbox>
              <div class="kp-filters">
                <el-select
                  v-model="difficultyMap[kp.name]"
                  placeholder="难度"
                  size="small"
                  clearable
                  style="width:110px">
                  <el-option label="入门" value="easy" />
                  <el-option label="基础" value="medium" />
                  <el-option label="进阶" value="hard" />
                  <el-option label="挑战" value="all" />
                </el-select>
                <el-select
                  v-model="typeMap[kp.name]"
                  placeholder="题型"
                  size="small"
                  clearable
                  style="width:110px">
                  <el-option label="单选题" value="single_choice" />
                  <el-option label="多选题" value="multi_choice" />
                  <el-option label="判断题" value="judge" />
                  <el-option label="不限" value="all" />
                </el-select>
              </div>
            </div>
          </template>

          <!-- ─── 模拟卷练习 ‐ 整体难度+题数 ─── -->
          <template v-if="mode === '模拟卷练习'">
            <el-form-item label="整体难度">
              <el-select v-model="difficulty" placeholder="选择整体难度" clearable style="width:200px">
                <el-option label="简单" value="easy" />
                <el-option label="中等" value="medium" />
                <el-option label="困难" value="hard" />
              </el-select>
            </el-form-item>
            <el-form-item label="题数">
              <el-radio-group v-model="examCount">
                <el-radio-button :value="5">5 题</el-radio-button>
                <el-radio-button :value="10">10 题</el-radio-button>
                <el-radio-button :value="15">15 题</el-radio-button>
                <el-radio-button :value="20">20 题</el-radio-button>
              </el-radio-group>
            </el-form-item>
            <el-alert
              title="将自动从各考点混合出题，涵盖通用能力和专业知识"
              type="info"
              :closable="false"
              show-icon
              style="margin-top:4px" />
          </template>

          <!-- ─── 错题重练 ‐ 统计+筛选 ─── -->
          <template v-if="mode === '错题重练'">
            <div v-if="wrongStats" class="wrong-stats-card">
              <div class="wrong-stat-item">
                <span class="stat-label"><TriangleAlert :size="16" class="icon-blue" /> 总错题数</span>
                <span class="stat-value">{{ wrongStats.total }}</span>
              </div>
              <div class="wrong-stat-item">
                <span class="stat-label"><Bookmark :size="16" class="icon-blue" /> 未掌握</span>
                <span class="stat-value warn">{{ wrongStats.unmastered }}</span>
              </div>
            </div>
            <el-form-item label="按考点筛选">
              <el-select
                v-model="wrongFilterKnowledge"
                placeholder="全部考点"
                clearable
                style="width:200px">
                <el-option
                  v-for="kp in allKnowledgePoints"
                  :key="kp.name"
                  :label="kp.name"
                  :value="kp.name" />
              </el-select>
            </el-form-item>
            <el-form-item label="按难度筛选">
              <el-select
                v-model="difficulty"
                placeholder="全部难度"
                clearable
                style="width:200px">
                <el-option label="简单" value="easy" />
                <el-option label="中等" value="medium" />
                <el-option label="困难" value="hard" />
              </el-select>
            </el-form-item>
            <el-alert
              title="将从错题本中抽取题目供你重练"
              type="warning"
              :closable="false"
              show-icon
              style="margin-top:4px" />
          </template>
        </el-form>

        <!-- 开始按钮 -->
        <div class="setup-actions">
          <el-button
            type="primary"
            size="large"
            :loading="startLoading"
            class="btn-primary start-btn"
            @click="startExam">
            <i :class="startBtnIcon"></i> {{ startBtnText }}
          </el-button>
        </div>
      </div>
    </div>

    <!-- ════════════════ Phase 2: 答题中 ════════════════ -->
    <div v-if="phase === 'doing'" class="phase-doing">
      <!-- 顶部状态栏（固定） -->
      <div class="exam-status-bar">
        <div class="status-left">
          <ListOrdered :size="16" class="icon-blue" />
          第 <b>{{ currentIndex + 1 }}</b>/{{ questions.length }} 题
        </div>
        <div class="status-center">
          <CheckCircle :size="16" class="icon-blue" />
          已答 <b>{{ answeredCount }}</b> 题
          <span class="status-divider">|</span>
          <Percent :size="16" class="icon-blue" />
          正确率 <b :style="{color: accuracyColor}">{{ accuracyPercent }}%</b>
        </div>
        <div class="status-right">
          <Clock :size="16" class="icon-blue" />
          {{ formatTime(timer) }}
          <el-button
            size="small"
            type="danger"
            plain
            class="status-end-btn"
            @click="confirmEndExam">
            <StopCircle :size="16" class="icon-blue" />
          </el-button>
        </div>
      </div>

      <div class="exam-body">
        <!-- 主内容区 -->
        <div class="exam-main">
          <!-- 加载动画（骨架屏） -->
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
              <p><Hourglass :size="16" class="icon-blue" /> 正在为您生成 {{ career }} 方向的题目…</p>
              <p v-if="loadMsg" class="load-msg">{{ loadMsg }}</p>
              <p v-if="loadError" class="load-error">{{ loadError }}</p>
              <el-button v-if="loadError" type="primary" @click="retryLoad" style="margin-top:8px">
                <Redo :size="16" class="icon-blue" /> 重试
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
                  <span
                    v-if="currentQuestion.knowledge_point"
                    class="tag-pill orange">
                    <Tag :size="16" class="icon-blue" />
                    {{ currentQuestion.knowledge_point }}
                  </span>
                  <span
                    v-if="currentQuestion.difficulty"
                    class="tag-pill"
                    :class="difficultyPillClass(currentQuestion.difficulty)">
                    <Signal :size="16" class="icon-blue" />
                    {{ difficultyLabel(currentQuestion.difficulty) }}
                  </span>
                </div>

                <!-- 题目标题 -->
                <div class="q-heading">
                  <CircleHelp :size="16" class="icon-blue" />
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
                      <CheckCircle :size="16" class="icon-blue" />
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
                      <CheckSquare :size="16" v-if="multiSelected.includes(opt.key)" class="icon-blue" />
                      <Square :size="16" class="icon-blue" />
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
                      <Check :size="16" class="icon-blue" /> 确认提交
                    </el-button>
                    <span v-if="multiSelected.length > 0" class="multi-hint">
                      <Layers :size="16" class="icon-blue" /> 已选 {{ multiSelected.length }} 项
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
                      <Check :size="16" class="icon-blue" /> 对
                    </div>
                    <div
                      class="judge-item"
                      :class="judgeClass('错')"
                      @click="submitAnswer('错')">
                      <X :size="16" class="icon-blue" /> 错
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
                    <CheckCircle :size="16" class="icon-blue" />
                    正确答案：<b>{{ answerResult.correct_answer }}</b>
                  </div>
                  <div class="analysis-box" v-if="answerResult.analysis">
                    <h4><BookOpen :size="16" class="icon-blue" /> 解析</h4>
                    <p>{{ answerResult.analysis }}</p>
                  </div>
                  <div class="analysis-box hint-box" v-if="currentQuestion.knowledge_point">
                    <p>
                      <Lightbulb :size="16" class="icon-blue" />
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
                    <Star :size="16" class="icon-blue" :class="isSaved ? 'fas fa-star' : 'far fa-star'" />
                    {{ isSaved ? '已收藏' : '收藏此题' }}
                  </el-button>
                  <div class="q-actions-right">
                    <el-button
                      v-if="currentIndex < questions.length - 1"
                      type="primary"
                      size="small"
                      :disabled="!answerResult"
                      @click="nextQuestion">
                      下一题 <ArrowRight :size="16" class="icon-blue" />
                    </el-button>
                    <el-button
                      v-if="currentIndex === questions.length - 1"
                      type="success"
                      size="small"
                      :disabled="!answerResult"
                      @click="finishExam">
                      <BarChart :size="16" class="icon-blue" /> 完成并查看报告
                    </el-button>
                  </div>
                </div>

                <!-- 草稿区 -->
                <el-collapse class="draft-collapse">
                  <el-collapse-item name="draft">
                    <template #title>
                      <span><Pencil :size="16" class="icon-blue" /> 草稿区</span>
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
              <Inbox :size="16" class="icon-blue" />
            </div>
            <p style="font-size:1.2rem">暂无可用题目</p>
            <p>请调整筛选条件再试</p>
            <el-button type="primary" @click="backToReady" style="margin-top:12px">
              <ArrowLeft :size="16" class="icon-blue" /> 返回设置
            </el-button>
          </div>
        </div>

        <!-- 答题卡侧边栏 -->
        <aside class="exam-sidebar">
          <div class="sidebar-card">
            <div class="sidebar-title">
              <Grid :size="16" class="icon-blue" /> 答题卡
            </div>
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
              <el-button
                size="small"
                type="danger"
                plain
                @click="confirmEndExam"
                style="width:100%">
                <StopCircle :size="16" class="icon-blue" /> 交卷
              </el-button>
            </div>
          </div>
        </aside>
      </div>
    </div>

    <!-- ════════════════ Phase 3: 完成页 ════════════════ -->
    <div v-if="phase === 'done'" class="phase-done">
      <div class="card report-card">
        <div class="report-header">
          <div class="report-emoji">
            <Trophy :size="3" :color="'#e6a23c'" />
          </div>
          <h2>练习完成！</h2>
        </div>
        <div class="report-meta">
          <span class="tag-pill blue"><Briefcase :size="16" class="icon-blue" /> {{ career }}</span>
          <span class="tag-pill green"><ListTodo :size="16" class="icon-blue" /> {{ mode }}</span>
        </div>
        <el-divider />
        <div class="report-stats grid-4">
          <div class="stat-card">
            <div class="stat-icon">
              <FileText :size="16" class="icon-blue" />
            </div>
            <div class="stat-num">{{ questions.length }}</div>
            <div class="stat-label">总题数</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon" style="color:#67c23a">
              <CheckCircle :size="16" class="icon-blue" />
            </div>
            <div class="stat-num" style="color:#67c23a">{{ correctCount }}</div>
            <div class="stat-label">答对</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon" :style="{color: accuracyColor}">
              <Percent :size="16" class="icon-blue" />
            </div>
            <div class="stat-num" :style="{color: accuracyColor}">{{ accuracyPercent }}%</div>
            <div class="stat-label">正确率</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <Hourglass :size="16" class="icon-blue" />
            </div>
            <div class="stat-num">{{ timeSpent }}</div>
            <div class="stat-label">用时</div>
          </div>
        </div>

        <!-- 薄弱知识点 -->
        <div v-if="weakPoints.length > 0" class="weak-section">
          <el-divider content-position="left">
            <span><ChartLine :size="16" :color="'#e6a23c'" /> 薄弱知识点</span>
          </el-divider>
          <div class="weak-list">
            <div v-for="(wp, wi) in weakPoints" :key="wi" class="weak-item">
              <span class="weak-rank">{{ wi + 1 }}</span>
              <span class="weak-name">{{ wp.name }}</span>
              <span class="weak-rate">{{ wp.wrongRate }}% 错误率</span>
            </div>
          </div>
        </div>

        <div class="report-actions">
          <el-button type="primary" size="large" @click="doAnotherRound">
            <Redo :size="16" class="icon-blue" /> 再来一组
          </el-button>
          <el-button size="large" @click="goToWrongQuestions">
            <List :size="16" class="icon-blue" /> 查看错题详情
          </el-button>
          <el-button size="large" @click="backToReady">
            <ArrowLeft :size="16" class="icon-blue" /> 返回设置
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import { useCareerStore } from '../stores/career'

const store = useCareerStore()
const router = useRouter()

// ═══════════════════════════════════════════════
// 岗位大类数据
// ═══════════════════════════════════════════════
const careerGroups = [
  {
    label: '计算机类',
    list: [
      '前端开发工程师', '后端开发工程师', '全栈开发工程师',
      '数据分析师', '软件测试工程师', '网络安全工程师',
      '运维工程师', 'AI算法工程师', '产品经理',
    ],
  },
  {
    label: '机电土木类',
    list: [
      '机械工程师', '电气工程师', '土木工程师', '建筑设计师',
      '自动化工程师', '结构工程师',
    ],
  },
  {
    label: '经管财会类',
    list: [
      '财务经理', '审计师', '会计', '市场营销',
      '运营专员', '人力资源', '企业管理咨询',
    ],
  },
  {
    label: '医疗医药类',
    list: [
      '临床医生', '护士', '药师', '生物医药研究员',
      '医疗器械工程师',
    ],
  },
  {
    label: '教育科研类',
    list: [
      '教师', '科研助理', '培训师', '教育产品经理',
    ],
  },
  {
    label: '法律合规类',
    list: [
      '法务专员', '合规专员', '律师', '知识产权顾问',
    ],
  },
  {
    label: '设计创意类',
    list: [
      'UI设计师', '视觉设计师', '产品设计师', '插画师',
    ],
  },
  {
    label: '媒体公关类',
    list: [
      '新媒体运营', '内容编辑', '公关专员', '品牌策划',
    ],
  },
]

// ═══════════════════════════════════════════════
// 阶段与配置
// ═══════════════════════════════════════════════
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

// 当前题目
const currentQuestion = computed(() => {
  if (currentIndex.value < questions.value.length) {
    return questions.value[currentIndex.value]
  }
  return null
})

// 进度与统计
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
    case '专项练习': return 'fas fa-book'
    case '模拟卷练习': return 'fas fa-file-alt'
    case '错题重练': return 'fas fa-redo'
    default: return 'fas fa-pen'
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

// 薄弱知识点
const weakPoints = computed(() => {
  // 统计每个知识点的错误率
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
    // 按类型分组
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
function difficultyTagType(diff) {
  switch (diff) {
    case 'easy': return 'success'
    case 'medium': return 'warning'
    case 'hard': return 'danger'
    default: return 'info'
  }
}

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
    // 如果该题已答过，恢复结果
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

  // 保存筛选条件
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
      // 如果没有选择具体考点，使用全部
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
    // 使用第一个选中的知识点的难度和题型，或者整体设置
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

  // 更新加载消息
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

    // 错题重练模式：提交 reanswer
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

// 多选题
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

  // 保存练习记录
  try {
    await axios.post('/api/exam/record', {
      career: career.value,
      mode: mode.value,
      total: questions.length,
      answered: answeredCount.value,
      correct: correctCount.value,
      time_seconds: timer.value,
      questions: questions.value.map(q => ({
        id: q.id,
        question: q.question,
        user_answer: q._userAnswer,
        is_correct: q._result ? q._result.is_correct : null,
      })),
    })
  } catch (e) {
    console.error('保存记录失败', e)
  }

  phase.value = 'done'
}

// ═══════════════════════════════════════════════
// 完成页操作
// ═══════════════════════════════════════════════
function doAnotherRound() {
  // 重置状态，回到 ready 但保留之前的选择
  phase.value = 'ready'
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
  router.push('/interview/history')
}

function backToEntry() {
  router.push('/interview')
}

function backToReady() {
  doAnotherRound()
}
</script>

<style scoped>
/* ═══════════════════════════════════════════════
   页面基础 — 全宽布局（独立页面）
   ═══════════════════════════════════════════════ */
.exam-page {
  min-height: 100vh;
  background: var(--bg-body, #f5f7fa);
  padding-bottom: 3rem;
}

/* 顶部栏 */
.exam-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1.5rem;
  position: sticky;
  top: 0;
  z-index: 100;
  background: var(--bg-card, #ffffff);
  border-bottom: 1px solid var(--border-light, #e8e8e8);
  box-shadow: var(--shadow-sm, 0 1px 3px rgba(0,0,0,0.06));
}
.exam-title {
  font-weight: 600;
  font-size: 1.05rem;
  color: var(--text-heading, #333);
}
.exam-title i {
  margin-right: 6px;
  color: var(--primary, #3D5A80);
}

/* ═══════════════════════════════════════════════
   Phase 1: 设置
   ═══════════════════════════════════════════════ */
.phase-ready {
  max-width: 720px;
  margin: 2rem auto;
  padding: 0 1rem;
}
.setup-card {
  border-radius: var(--radius-lg, 12px);
}
.setup-header {
  width: 100%;
  margin-bottom: 0.5rem;
}
.setup-form {
  padding: 0.2rem 0;
}

/* 模式选择 */
.mode-radio-group {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.mode-radio-group .el-radio-button__inner {
  padding: 8px 16px;
  font-size: 0.9rem;
}

/* 考点行 */
.kp-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 8px;
  border-radius: var(--radius-sm, 8px);
  transition: background 0.2s;
  margin-bottom: 4px;
}
.kp-row:hover {
  background: var(--primary-bg, #f5f3ff);
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

.divider-title {
  font-weight: 600;
  font-size: 0.9rem;
}
.divider-title i {
  margin-right: 6px;
}

/* 错题统计 */
.wrong-stats-card {
  display: flex;
  gap: 2rem;
  padding: 12px 16px;
  background: #fff7e6;
  border-radius: var(--radius-md, 10px);
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
  color: var(--primary, #3D5A80);
}
.stat-value.warn {
  color: #e6a23c;
}

/* 开始按钮 */
.setup-actions {
  text-align: center;
  padding-top: 1.2rem;
}
.start-btn {
  padding: 12px 48px;
  font-size: 1rem;
}

/* ═══════════════════════════════════════════════
   Phase 2: 答题中
   ═══════════════════════════════════════════════ */
.phase-doing {
  min-height: calc(100vh - 60px);
  padding: 0 1.5rem;
}

/* 顶部状态栏 */
.exam-status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 1.2rem;
  background: var(--bg-card, #ffffff);
  border-radius: var(--radius-md, 10px);
  margin: 0.8rem 0;
  box-shadow: var(--shadow-sm, 0 1px 6px rgba(0,0,0,0.06));
  font-size: 0.88rem;
  position: sticky;
  top: 56px;
  z-index: 99;
  border: 1px solid var(--border-light, #e8e8e8);
}
.status-left i,
.status-center i,
.status-right i {
  margin-right: 6px;
  color: var(--primary, #3D5A80);
}
.status-left b,
.status-center b {
  color: var(--primary, #3D5A80);
}
.status-center {
  text-align: center;
}
.status-divider {
  margin: 0 8px;
  color: var(--border, #ddd);
}
.status-right {
  font-variant-numeric: tabular-nums;
  font-weight: 600;
  color: var(--text-heading, #333);
  display: flex;
  align-items: center;
  gap: 8px;
}
.status-end-btn {
  padding: 4px 10px;
}

/* 主内容 + 侧边栏布局 */
.exam-body {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}
.exam-main {
  flex: 1;
  min-width: 0;
}

/* 骨架屏 */
.loading-section {
  padding: 1rem 0;
}
.skeleton-card {
  background: var(--bg-card, #ffffff);
  border-radius: var(--radius-lg, 12px);
  padding: 1.5rem;
  border: 1px solid var(--border-light, #eee);
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
.skeleton-option { height: 44px; width: 100%; border-radius: var(--radius-md, 10px); }
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

/* 题目卡片 */
.question-card {
  border-radius: var(--radius-lg, 12px);
  padding: 1.5rem;
}

/* 标签行 */
.q-tags {
  display: flex;
  gap: 6px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
.q-type-tag {
  font-weight: 600;
}

/* 题目标题 */
.q-heading {
  font-size: 1rem;
  font-weight: 600;
  color: var(--primary, #3D5A80);
  margin-bottom: 8px;
}
.q-heading i {
  margin-right: 6px;
}

/* 题干 */
.q-text {
  font-size: 0.95rem;
  line-height: 1.7;
  color: var(--text-body, #333);
  margin-bottom: 1rem;
  white-space: pre-wrap;
}

/* 选项 */
.options-wrap {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}
.option-item {
  padding: 0.7rem 1rem;
  border: 2px solid var(--border-light, #e8e8e8);
  border-radius: var(--radius-md, 10px);
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  position: relative;
}
.option-item:hover {
  border-color: var(--primary, #3D5A80);
  background: var(--primary-bg, #f5f3ff);
}
.option-item.selected {
  border-color: var(--primary, #3D5A80);
  background: var(--primary-bg, #f0f0ff);
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
  color: var(--primary, #3D5A80);
  min-width: 24px;
}
.opt-text {
  font-size: 0.9rem;
  flex: 1;
}
.opt-check-icon {
  margin-left: auto;
  color: var(--primary, #3D5A80);
}
.opt-checkbox {
  min-width: 20px;
  font-size: 1rem;
}
.checkbox-checked {
  color: var(--primary, #3D5A80);
}
.checkbox-empty {
  color: #ccc;
}

/* 多选题提交 */
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
.multi-hint i {
  margin-right: 4px;
}

/* 判断题 */
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
  border: 2px solid var(--border-light, #e8e8e8);
  border-radius: var(--radius-lg, 12px);
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
  border-color: var(--primary, #3D5A80);
  background: var(--primary-bg, #f5f3ff);
}
.judge-item.selected {
  border-color: var(--primary, #3D5A80);
  background: var(--primary-bg, #f0f0ff);
}
.judge-item.correct {
  border-color: #67c23a;
  background: #f0fff0;
}
.judge-item.wrong {
  border-color: #f56c6c;
  background: #fff0f0;
}

/* 反馈 */
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
  background: var(--bg-alt, #f8f9fa);
  border-radius: var(--radius-md, 10px);
  padding: 0.8rem;
  margin-top: 8px;
}
.analysis-box h4 {
  margin: 0 0 0.4rem 0;
  font-size: 0.9rem;
  color: var(--primary, #3D5A80);
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
  background: #f0f5ff;
  border-left: 3px solid var(--primary, #3D5A80);
}
.hint-box p {
  color: var(--text-heading, #333);
}
.hint-box i {
  margin-right: 4px;
  color: var(--primary, #3D5A80);
}

/* 底部操作 */
.q-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 0.8rem;
  border-top: 1px solid var(--border-light, #f0f0f0);
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

/* 草稿区 */
.draft-collapse {
  margin-top: 12px;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 3rem 0;
  color: var(--text-muted, #999);
}

/* ═══════════════════════════════════════════════
   答题卡侧边栏
   ═══════════════════════════════════════════════ */
.exam-sidebar {
  width: 200px;
  flex-shrink: 0;
  position: sticky;
  top: 120px;
}
.sidebar-card {
  background: var(--bg-card, #ffffff);
  border-radius: var(--radius-lg, 12px);
  padding: 1rem;
  border: 1px solid var(--border-light, #e8e8e8);
  box-shadow: var(--shadow-sm, 0 1px 6px rgba(0,0,0,0.06));
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
  color: var(--primary, #3D5A80);
}
.sidebar-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 0.8rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid var(--border-light, #eee);
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
  border-radius: var(--radius-sm, 6px);
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  background: var(--bg-alt, #f5f5f5);
  color: var(--text-muted, #999);
  border: 2px solid transparent;
  transition: all 0.15s ease;
}
.sidebar-grid-item:hover {
  border-color: var(--primary, #3D5A80);
  color: var(--primary, #3D5A80);
}
.sidebar-grid-item.grid-current {
  border-color: var(--primary, #3D5A80);
  background: var(--primary-bg, #f0f0ff);
  color: var(--primary, #3D5A80);
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
  border-color: var(--primary, #3D5A80);
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
.dot-current { background: var(--primary-bg, #f0f0ff); border: 2px solid var(--primary, #3D5A80); }
.dot-unanswered { background: var(--bg-alt, #f5f5f5); border: 1px solid #ddd; }
.sidebar-actions {
  margin-top: 0.5rem;
}

/* ═══════════════════════════════════════════════
   Phase 3: 完成页
   ═══════════════════════════════════════════════ */
.phase-done {
  max-width: 640px;
  margin: 2rem auto;
  padding: 0 1rem;
}
.report-card {
  border-radius: var(--radius-lg, 12px);
  text-align: center;
  padding: 2rem 1.5rem;
}
.report-header {
  padding: 0 0 0.5rem;
}
.report-emoji {
  display: block;
  margin-bottom: 0.5rem;
}
.report-header h2 {
  margin: 0;
  color: var(--text-heading, #333);
  font-size: 1.4rem;
}
.report-meta {
  display: flex;
  gap: 8px;
  justify-content: center;
  margin-top: 8px;
}
.report-stats {
  display: flex;
  justify-content: center;
  gap: 1rem;
  padding: 0.5rem 0;
}

/* 薄弱知识点 */
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
  border-radius: var(--radius-sm, 8px);
}
.weak-rank {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--primary, #3D5A80);
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

/* 操作按钮 */
.report-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  padding: 1.5rem 0 0.5rem;
}

/* ═══════════════════════════════════════════════
   过渡动画
   ═══════════════════════════════════════════════ */
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

/* ═══════════════════════════════════════════════
   响应式
   ═══════════════════════════════════════════════ */
@media (max-width: 768px) {
  .exam-sidebar {
    display: none;
  }
  .phase-doing {
    padding: 0 0.75rem;
  }
  .exam-status-bar {
    font-size: 0.78rem;
    padding: 0.5rem 0.8rem;
    flex-wrap: wrap;
    gap: 4px;
  }
}
@media (max-width: 640px) {
  .exam-topbar {
    padding: 0.6rem 0.75rem;
  }
  .phase-ready {
    margin: 1rem auto;
    padding: 0 0.5rem;
  }
  .setup-card {
    border-radius: var(--radius-sm, 8px);
  }
  .mode-radio-group .el-radio-button__inner {
    padding: 6px 10px;
    font-size: 0.8rem;
  }
  .kp-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
  }
  .kp-filters {
    width: 100%;
    display: flex;
    gap: 6px;
  }
  .kp-filters .el-select {
    flex: 1;
  }
  .exam-status-bar {
    font-size: 0.75rem;
    padding: 0.4rem 0.6rem;
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
  .report-stats {
    gap: 0.5rem;
  }
  .report-actions {
    flex-direction: column;
    align-items: center;
  }
  .report-actions .el-button {
    width: 100%;
    max-width: 280px;
  }
  .wrong-stats-card {
    gap: 1rem;
  }
}
</style>