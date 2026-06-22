<template>
  <div class="session-page">
    <!-- ═══════ 顶部栏 ═══════ -->
    <div class="session-topbar">
      <el-button class="back-circle-btn" @click="backToEntry"><i class="fa-solid fa-arrow-left"></i> 返回面试与笔试</el-button>
      <span class="session-title"><i class="fa-solid fa-video"></i> 多模态模拟面试</span>
      <div class="topbar-actions">
        <el-button v-if="phase === 'chatting'" size="small" type="danger" plain @click="handleEndInterview"><i class="fa-solid fa-stop"></i> 结束面试</el-button>
      </div>
    </div>

    <!-- ═══════ 阶段 1：设置（同屏承托） ═══════ -->
    <div v-if="phase === 'setup'" class="section-panel setup-stage">
      <div class="setup-shell">
        <aside class="setup-side">
          <div class="setup-side-kicker">启途面试舱</div>
          <h1>三步准备好一场正式模拟</h1>
          <p>人只要把岗位、简历和面试模式选好，后面就交给 AI 面试官来追问和复盘。</p>
          <div class="setup-steps">
            <button class="setup-step" :class="{ active: setupStep === 1, done: canProceedJob }" @click="setupStep = 1">
              <span>01</span><b>选择岗位</b><small>也可自定义材料</small>
            </button>
            <button class="setup-step" :class="{ active: setupStep === 2, done: resumeFileName }" @click="setupStep = 2" :disabled="!canProceedJob">
              <span>02</span><b>导入简历</b><small>可选但更贴合</small>
            </button>
            <button class="setup-step" :class="{ active: setupStep === 3 }" @click="setupStep = 3" :disabled="!canProceedJob">
              <span>03</span><b>确认模式</b><small>开始对话练习</small>
            </button>
          </div>
        </aside>

        <main class="setup-main-card">
          <div class="setup-main-head">
            <div>
              <span class="setup-breadcrumb">步骤 {{ setupStep }} / 3</span>
              <h2>{{ setupStep === 1 ? '先告诉启途，人想练哪个岗位' : setupStep === 2 ? '把简历放进来，让问题更像真实面试' : '确认练习方式，准备开口回答' }}</h2>
            </div>
            <div class="setup-mini-badge">{{ interviewTargetLabel }}</div>
          </div>

          <!-- Step 1: 岗位与类别 -->
          <div v-if="setupStep === 1" class="setup-step-content">
            <div class="custom-interview-hero">
              <div>
                <span class="custom-kicker">CUSTOM INTERVIEW</span>
                <h3>两种开始方式：选岗位，或把真实面试材料交给启途</h3>
                <p>适合岗位很特殊、老师布置了题目、或人手里有 JD/面试要求时使用。AI 面试官会按材料追问，不再只走固定模板。</p>
              </div>
              <div class="custom-paper-mark">QITU</div>
            </div>
            <el-form label-position="top">
              <el-form-item>
                <template #label><i class="fa-solid fa-crosshairs"></i> 目标岗位</template>
                <el-select v-model="career" placeholder="选择岗位，或在下方手动输入" style="width:100%" allow-create filterable clearable>
                  <el-option-group v-if="store.validBookmarks.length">
                    <template #label><i class="fa-solid fa-star" style="color:var(--el-color-warning)"></i> 已收藏</template>
                    <el-option v-for="b in store.validBookmarks" :key="b.career" :label="b.career" :value="b.career" />
                  </el-option-group>
                  <el-option label="前端开发工程师" value="前端开发工程师" />
                  <el-option label="后端开发工程师" value="后端开发工程师" />
                  <el-option label="数据分析师" value="数据分析师" />
                  <el-option label="产品经理" value="产品经理" />
                  <el-option label="软件测试工程师" value="软件测试工程师" />
                  <el-option label="UI设计师" value="UI设计师" />
                  <el-option label="运营专员" value="运营专员" />
                  <el-option label="市场营销" value="市场营销" />
                </el-select>
              </el-form-item>
              <div class="custom-form-grid">
                <el-form-item>
                  <template #label><i class="fa-regular fa-pen-to-square"></i> 自定义岗位名称</template>
                  <el-input v-model="customInterview.target" placeholder="例：新媒体运营实习生 / 银行柜员 / 考研复试" clearable />
                </el-form-item>
                <el-form-item>
                  <template #label><i class="fa-regular fa-folder-open"></i> 面试分类</template>
                  <el-select v-model="category" style="width:100%" placeholder="选择分类（默认同岗位）" allow-create filterable clearable>
                    <el-option label="同岗位名称" :value="interviewTargetLabel" />
                    <el-option label="技术基础" value="技术基础" />
                    <el-option label="项目经验" value="项目经验" />
                    <el-option label="行为面试" value="行为面试" />
                    <el-option label="综合面试" value="综合面试" />
                  </el-select>
                </el-form-item>
              </div>
              <el-form-item>
                <template #label><i class="fa-solid fa-scroll"></i> 自定义面试材料（可选）</template>
                <el-input
                  v-model="customInterview.material"
                  type="textarea"
                  :rows="5"
                  maxlength="1200"
                  show-word-limit
                  placeholder="可以粘贴岗位 JD、老师要求、比赛答辩规则、公司面试重点。启途会按这里的内容组织提问。"
                />
              </el-form-item>
            </el-form>
            <div v-if="customInterviewSummary.length" class="custom-summary-strip">
              <span v-for="item in customInterviewSummary" :key="item" class="custom-summary-pill">{{ item }}</span>
            </div>
            <div class="setup-nav">
              <el-button type="primary" @click="setupStep = 2" :disabled="!canProceedJob">下一步 <i class="fa-solid fa-arrow-right"></i></el-button>
            </div>
          </div>

          <!-- Step 2: 简历上传 -->
          <div v-if="setupStep === 2" class="setup-step-content">
            <el-form label-position="top">
              <el-form-item>
                <template #label><i class="fa-regular fa-file"></i> 上传简历（可选）</template>
                <div class="resume-upload-area">
                  <input type="file" ref="resumeInput" accept=".pdf,.doc,.docx,.txt" style="display:none" @change="onResumeUpload" />
                  <el-button size="small" @click="$refs.resumeInput.click()">
                    {{ resumeFileName ? '重新选择' : '选择文件' }}
                  </el-button>
                  <span v-if="resumeFileName" class="resume-file-name">{{ resumeFileName }}</span>
                  <el-tag v-if="resumeFileName" type="success" size="small" effect="plain"><i class="fa-regular fa-check-circle"></i> 已上传</el-tag>
                  <el-button v-if="resumeFileName" size="small" text type="danger" @click="clearResume">移除</el-button>
                </div>
              </el-form-item>
              <div class="resume-hint-card">
                <b>简历驱动模式会怎么用？</b>
                <p>启途会根据简历里的项目、技能和经历追问，不会只问泛泛的固定题。</p>
              </div>
              <el-collapse v-if="resumeParsedText" style="margin-top:12px">
                <el-collapse-item name="preview">
                <template #title><i class="fa-solid fa-book-open"></i> 预览解析内容</template>
                  <pre class="resume-preview">{{ resumeParsedText }}</pre>
                </el-collapse-item>
              </el-collapse>
              <div v-if="resumeUploading" class="resume-uploading">
                <el-progress :percentage="resumeUploadProgress" :stroke-width="6" />
                <span>正在上传并解析简历…</span>
              </div>
            </el-form>
            <div class="setup-nav">
              <el-button @click="setupStep = 1"><i class="fa-solid fa-arrow-left"></i> 上一步</el-button>
              <el-button type="primary" @click="setupStep = 3">下一步 <i class="fa-solid fa-arrow-right"></i></el-button>
            </div>
          </div>

          <!-- Step 3: 模式选择 + 开始 -->
          <div v-if="setupStep === 3" class="setup-step-content">
            <el-form label-position="top">
              <el-form-item>
                <template #label><i class="fa-solid fa-gamepad"></i> 面试模式</template>
                <el-radio-group v-model="mode" class="mode-radio-group">
                  <el-radio-button value="basic"><div class="mode-option"><span class="mode-icon"><i class="fa-regular fa-clipboard"></i></span><div><strong>基础模式</strong><p class="mode-desc">固定问题，覆盖常见面试题</p></div></div></el-radio-button>
                  <el-radio-button value="resume"><div class="mode-option"><span class="mode-icon"><i class="fa-regular fa-file"></i></span><div><strong>简历驱动</strong><p class="mode-desc">基于简历内容生成个性化问题</p></div></div></el-radio-button>
                  <el-radio-button value="stress"><div class="mode-option"><span class="mode-icon"><i class="fa-solid fa-fire"></i></span><div><strong>压力面试</strong><p class="mode-desc">挑战性追问，模拟高压场景</p></div></div></el-radio-button>
                </el-radio-group>
              </el-form-item>
              <el-form-item>
                <template #label><i class="fa-regular fa-clock"></i> 面试时长</template>
                <el-select v-model="interviewDuration" style="width:200px">
                  <el-option label="15 分钟" :value="15" />
                  <el-option label="30 分钟" :value="30" />
                  <el-option label="45 分钟" :value="45" />
                  <el-option label="60 分钟" :value="60" />
                </el-select>
              </el-form-item>
            </el-form>
            <div class="setup-nav final-nav">
              <el-button @click="setupStep = 2"><i class="fa-solid fa-arrow-left"></i> 上一步</el-button>
              <el-button type="primary" size="large" @click="handleStartInterview" :loading="startLoading">
                <i class="fa-solid fa-play"></i> 开始面试
              </el-button>
            </div>
          </div>
        </main>
      </div>
    </div>

    <!-- ═══════ 阶段 2：面试中 ═══════ -->
    <div v-if="phase === 'chatting' || phase === 'loading'" class="section-panel interview-phase">
      <!-- 顶部控制栏 -->
      <div class="interview-topbar">
        <div class="it-left">
          <el-tag :type="modeTagType" size="small" effect="dark">
            {{ modeLabel }}
          </el-tag>
          <span class="it-career">{{ interviewTargetLabel }}</span>
        </div>
        <div class="it-center">
          <div class="countdown-timer" :class="{ 'countdown-warning': remainingSeconds <= 120 }">
            <el-icon><Timer /></el-icon>
            <span>{{ formattedTime }}</span>
          </div>
          <el-button size="small" :icon="paused ? 'VideoPlay' : 'VideoPause'" circle @click="togglePause" :title="paused ? '继续' : '暂停'" />
          <el-button size="small" icon="Right" circle @click="skipQuestion" :disabled="aiLoading" title="跳过本题" />
        </div>
        <div class="it-right">
          <span class="round-badge">第 {{ chatRound }} 轮</span>
          <el-button size="small" type="danger" @click="handleEndInterview"><i class="fa-solid fa-stop"></i> 结束面试</el-button>
        </div>
      </div>

      <div class="chat-layout">
        <!-- 左：对话区 -->
        <div class="chat-main">
          <div class="chat-messages" ref="chatRef">
            <div v-if="startLoading" class="chat-loading-msg">
              <p><i class="fa-solid fa-hourglass-half"></i> AI 面试官正在准备…</p>
            </div>
            <div v-for="(msg, i) in messages" :key="i"
                 :class="['chat-bubble', msg.role === 'assistant' ? 'ai' : 'user']">
              <div class="chat-avatar"><i :class="msg.role === 'assistant' ? 'fa-solid fa-robot' : 'fa-solid fa-user'"></i></div>
              <div class="chat-content">
                <div class="chat-text" v-html="msg.content"></div>
                <div v-if="msg.role === 'assistant'" class="chat-msg-actions">
                  <el-button text size="small" @click="speakText(msg.content)" :disabled="!speechSynthSupported" title="朗读">
                    <i class="fa-solid fa-volume-high"></i>
                  </el-button>
                </div>
              </div>
            </div>
            <div v-if="aiLoading" class="chat-bubble ai">
              <div class="chat-avatar"><i class="fa-solid fa-robot"></i></div>
              <div class="chat-content"><span class="typing-dots">思考中<span>.</span><span>.</span><span>.</span></span></div>
            </div>
          </div>

          <!-- 语音活动指示器 -->
          <div v-if="voiceActive" class="voice-indicator">
            <span class="voice-pulse"></span>
            <span>正在聆听…</span>
          </div>

          <div class="chat-input-bar">
            <div class="chat-input-row">
              <el-input
                v-model="userInput"
                type="textarea"
                :rows="2"
                placeholder="输入你的回答… 也可以用下方语音输入"
                :disabled="aiLoading || paused"
                @keydown.enter.exact.prevent="sendMessage"
              />
            </div>
            <div class="chat-input-actions">
              <div class="cia-left">
                <el-button
                  size="small"
                  :type="isRecording ? 'danger' : 'default'"
                  @click="toggleVoiceInput"
                  :disabled="aiLoading || !speechRecogSupported"
                  :title="isRecording ? '停止录音' : '语音输入'"
                >
                  <template v-if="isRecording"><i class="fa-solid fa-stop"></i> 停止</template>
                  <template v-else><i class="fa-solid fa-microphone"></i></template>
                </el-button>
                <el-button
                  size="small"
                  :type="autoSpeakEnabled ? 'primary' : 'default'"
                  @click="autoSpeakEnabled = !autoSpeakEnabled"
                  title="自动朗读AI回复"
                >
                  <i class="fa-solid fa-volume-high"></i> {{ autoSpeakEnabled ? '已开启' : '已关闭' }}
                </el-button>
              </div>
              <el-button
                type="primary"
                @click="sendMessage"
                :loading="aiLoading"
                :disabled="!userInput.trim() || paused"
              >
                发送
              </el-button>
            </div>
          </div>
        </div>

        <!-- 右：摄像头 + 录制控制 -->
        <div class="chat-sidebar">
          <!-- 摄像头区域 -->
          <div class="camera-card">
            <div class="camera-header">
              <span><i class="fa-solid fa-camera"></i> 实时画面</span>
              <div class="camera-controls">
                <el-switch
                  v-model="cameraOn"
                  :loading="cameraToggling"
                  size="small"
                  active-text="开"
                  inactive-text="关"
                  @change="toggleCamera"
                />
              </div>
            </div>
            <div class="camera-wrapper" v-if="cameraOn && cameraReady">
              <video ref="videoRef" autoplay muted playsinline class="user-video"></video>
              <div class="emotion-overlay" v-if="currentEmotion">
                <div class="emotion-badge" :class="'emo-' + currentEmotion.emotion">
                  {{ currentEmotion.emotion }} {{ currentEmotion.confidence }}%
                </div>
              </div>
              <!-- 录制状态覆盖 -->
              <div v-if="isRecordingVideo" class="recording-badge">
                <span class="rec-dot"></span> REC {{ recordingDuration }}
              </div>
            </div>
            <div class="camera-placeholder" v-else>
              <div class="camera-placeholder-icon"><i class="fa-solid fa-camera"></i></div>
              <p class="camera-placeholder-text">摄像头未开启</p>
              <p class="camera-placeholder-sub">AI 会分析你的表情</p>
            </div>
            <div class="emotion-details" v-if="currentEmotion?.details">
              <div v-for="(val, key) in currentEmotion.details" :key="key" class="ed-row">
                <span class="ed-label">{{ key }}</span>
                <div class="ed-bar-track"><div class="ed-bar-fill" :style="{ width: val + '%', background: edBarColor(key, val) }"></div></div>
                <span class="ed-val">{{ val }}%</span>
              </div>
            </div>
          </div>

          <!-- 录制控制区 -->
          <div class="recording-controls">
            <div class="recording-header">
              <span><i class="fa-solid fa-film"></i> 录制控制</span>
            </div>
            <div class="recording-buttons">
              <div class="rec-btn-group">
                <el-button
                  size="small"
                  :type="micOn ? 'primary' : 'default'"
                  @click="toggleMic"
                  :disabled="!cameraOn"
                  title="麦克风开关"
                >
                  <template v-if="micOn"><i class="fa-solid fa-microphone"></i> 麦克风开</template>
                  <template v-else><i class="fa-solid fa-volume-xmark"></i> 麦克风关</template>
                </el-button>
                <el-button
                  size="small"
                  :type="isRecordingVideo ? 'danger' : 'success'"
                  @click="toggleRecording"
                  :disabled="!cameraOn || !micOn"
                >
                  <template v-if="isRecordingVideo"><i class="fa-solid fa-stop"></i> 停止录制</template>
                  <template v-else><i class="fa-solid fa-circle"></i> 开始录制</template>
                </el-button>
              </div>
            </div>
          </div>

          <!-- 行为观察区 -->
          <div class="risk-watch-card">
            <div class="risk-watch-head">
              <span><i class="fa-solid fa-shield-heart"></i> 行为观察</span>
              <el-tag size="small" :type="riskLevelTag.type" effect="plain">{{ riskLevelTag.label }}</el-tag>
            </div>
            <p class="risk-watch-desc">只做温和记录：离开页面、长时间空白、手动标记等会进入报告，不会直接判定作弊。</p>
            <div class="risk-score-line">
              <span>风险指数</span>
              <el-progress :percentage="riskScore" :stroke-width="7" :color="riskScoreColor" />
            </div>
            <div class="risk-actions">
              <el-button size="small" plain @click="recordManualRisk('候选人主动说明', '候选人主动记录了需要复盘的异常情况。')">
                <i class="fa-regular fa-flag"></i> 手动记录
              </el-button>
              <el-button size="small" text @click="clearRiskEvents" :disabled="!riskEvents.length">清空</el-button>
            </div>
            <div v-if="riskEvents.length" class="risk-mini-list">
              <div v-for="item in riskEvents.slice(-3).reverse()" :key="item.id" class="risk-mini-item">
                <b>{{ item.title }}</b><small>{{ formatRiskTime(item.time) }}</small>
              </div>
            </div>
          </div>

          <!-- 关键词提示（简历驱动模式） -->
          <div v-if="mode === 'resume' && currentKeywords.length" class="keyword-hints">
            <div class="keyword-header"><i class="fa-solid fa-lightbulb"></i> 关键词提示</div>
            <div class="keyword-tags">
              <el-tag
                v-for="(kw, i) in currentKeywords"
                :key="i"
                size="small"
                :type="kw.type || 'info'"
                effect="plain"
                class="kw-tag"
              >
                {{ kw.text }}
              </el-tag>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════ 阶段 3：报告 ═══════ -->
    <div v-if="phase === 'report'" class="section-panel">
      <div v-if="reportLoading" class="report-loading">
        <el-progress type="circle" :percentage="reportLoadProgress" :width="100" status="warning" />
        <p class="report-loading-text"><i class="fa-solid fa-robot"></i> AI 正在分析你的面试表现…</p>
      </div>
      <el-card v-else shadow="never" class="report-card">
        <template #header>
          <span style="font-weight:600"><i class="fa-solid fa-chart-simple"></i> 面试评估报告</span>
          <el-button text size="small" @click="goToHistory" style="float:right"><i class="fa-regular fa-clipboard"></i> 查看面试记录</el-button>
        </template>
        <div class="report-top-info">
          <span class="report-job">{{ interviewTargetLabel }}</span>
          <el-tag :type="modeTagType" size="small" effect="dark">{{ modeLabel }}</el-tag>
          <span class="report-rounds">共 {{ messages.filter(m => m.role === 'assistant').length }} 轮对话</span>
        </div>
        <div v-if="riskEvents.length" class="risk-report-card">
          <div class="risk-report-head">
            <i class="fa-solid fa-shield-heart"></i>
            <div>
              <b>行为观察记录</b>
              <p>这是温和提醒，不直接判定作弊，只记录面试过程中的异常片段，方便复盘。</p>
            </div>
          </div>
          <div class="risk-report-list">
            <div v-for="item in riskEvents" :key="item.id" class="risk-report-item">
              <span>{{ formatRiskTime(item.time) }}</span>
              <b>{{ item.title }}</b>
              <small>{{ item.detail }}</small>
            </div>
          </div>
        </div>
        <div class="report-summary" v-if="report.summary">{{ report.summary }}</div>
        <div class="overall-score-area">
          <el-progress type="circle" :percentage="report.overall_score || 0" :width="130" :color="scoreColor(report.overall_score || 0)" />
          <h3>综合得分 {{ report.overall_score || 0 }}</h3>
        </div>
        <!-- ─── 四维雷达图 ─── -->
        <div class="radar-section" v-if="Object.keys(report.dimensions).length >= 4">
          <div class="radar-wrap">
            <svg viewBox="0 0 300 300" class="radar-svg">
              <!-- 网格（20%/40%/60%/80%） -->
              <polygon v-for="g in radarGrid" :key="g.key" :points="g.points" fill="none" stroke="#e0e4e8" stroke-width="1" />
              <!-- 轴线 -->
              <line v-for="a in radarAxes" :key="a.key" :x1="150" :y1="150" :x2="a.x" :y2="a.y" stroke="#d0d4d8" stroke-width="1" stroke-dasharray="4,3" />
              <!-- 数据多边形 -->
              <polygon :points="radarDataPoints" fill="rgba(37,99,235,0.14)" stroke="#2563EB" stroke-width="2.5" stroke-linejoin="round" />
              <!-- 数据锚点 -->
              <circle v-for="n in radarNodes" :key="n.key" :cx="n.x" :cy="n.y" r="4.5" fill="#2563EB" />
              <!-- 维度标签 -->
              <text v-for="l in radarLabels" :key="l.key" :x="l.x" :y="l.y" text-anchor="middle" dominant-baseline="central" font-size="11" fill="#475569" font-weight="500">{{ l.label }}</text>
              <!-- 分数标签 -->
              <text v-for="s in radarScores" :key="s.key" :x="s.x" :y="s.y" text-anchor="middle" dominant-baseline="central" font-size="10" fill="#64748B" font-weight="600">{{ s.score }}</text>
            </svg>
          </div>
        </div>
        <div class="dimensions-grid" v-if="Object.keys(report.dimensions).length">
          <div v-for="(v, k) in report.dimensions" :key="k" class="dim-card">
            <div class="dim-header"><span>{{ k }}</span><b :style="{color:scoreColor(v.score||0)}">{{ v.score || 0 }}</b></div>
            <el-progress :percentage="v.score || 0" :stroke-width="8" :color="scoreColor(v.score || 0)" />
            <p class="dim-comment">{{ v.comment || '' }}</p>
          </div>
        </div>
        <el-divider />
        <div class="report-lists" v-if="report.strengths?.length">
          <h3><i class="fa-regular fa-check-circle" style="color:var(--el-color-success)"></i> 优点</h3>
          <ul><li v-for="s in report.strengths" :key="s">{{ s }}</li></ul>
        </div>
        <div class="report-lists" v-if="report.weaknesses?.length">
          <h3><i class="fa-solid fa-triangle-exclamation" style="color:var(--el-color-warning)"></i> 待改进</h3>
          <ul><li v-for="w in report.weaknesses" :key="w">{{ w }}</li></ul>
        </div>
        <div class="report-lists" v-if="report.suggestions?.length">
          <h3><i class="fa-solid fa-lightbulb" style="color:var(--el-color-primary)"></i> 建议</h3>
          <ul><li v-for="s in report.suggestions" :key="s">{{ s }}</li></ul>
        </div>
        <div class="report-actions">
          <el-button @click="resetToSetup"><i class="fa-solid fa-rotate"></i> 再来一次</el-button>
          <el-button type="primary" @click="goToHistory"><i class="fa-solid fa-chart-simple"></i> 查看面试记录</el-button>
          <el-button v-if="report.sessionId" text type="info" @click="goToDetail(report.sessionId)"><i class="fa-regular fa-file"></i> 查看完整报告</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Timer } from '@element-plus/icons-vue'
import axios from 'axios'
import { useCareerStore } from '../stores/career'

const store = useCareerStore()
const $router = useRouter()

// ==================== API Base ====================
const API = '/api'

// ==================== Setup State ====================
const career = ref('')
const category = ref('')
const mode = ref('basic')
const setupStep = ref(1)
const interviewDuration = ref(30) // minutes
const customInterview = reactive({
  target: '',
  material: ''
})
const resumeInput = ref(null)
const resumeFileName = ref('')
const resumeContent = ref('')
const resumeParsedText = ref('')
const resumeFileId = ref('')
const resumeUploading = ref(false)
const resumeUploadProgress = ref(0)

const interviewTargetLabel = computed(() => {
  const target = customInterview.target.trim() || career.value.trim()
  if (target) return target
  if (customInterview.material.trim()) return '自定义面试'
  return '未选择岗位'
})
const canProceedJob = computed(() => interviewTargetLabel.value !== '未选择岗位')
const customInterviewSummary = computed(() => {
  const items = []
  if (customInterview.target.trim()) items.push(`自定义岗位：${customInterview.target.trim()}`)
  if (career.value.trim()) items.push(`岗位库：${career.value.trim()}`)
  if (customInterview.material.trim()) items.push(`已加入材料 ${customInterview.material.trim().length} 字`)
  return items
})

function buildInterviewJobPrompt() {
  const target = interviewTargetLabel.value
  const material = customInterview.material.trim()
  const resume = resumeParsedText.value.trim()
  const parts = [`目标岗位：${target}`]
  if (category.value) parts.push(`面试分类：${category.value}`)
  if (material) parts.push(`自定义面试材料：${material.slice(0, 1200)}`)
  if (resume) parts.push(`候选人简历摘录：${resume.slice(0, 1200)}`)
  return parts.join('\n')
}

function clearResume() {
  resumeFileName.value = ''
  resumeContent.value = ''
  resumeParsedText.value = ''
  resumeFileId.value = ''
  if (resumeInput.value) resumeInput.value.value = ''
}

async function onResumeUpload(e) {
  const f = e.target.files?.[0]
  if (!f) return
  resumeFileName.value = f.name
  resumeContent.value = f

  // Try reading as text for preview
  if (f.type === 'text/plain') {
    const reader = new FileReader()
    reader.onload = ev => { resumeParsedText.value = ev.target?.result || '' }
    reader.readAsText(f)
  }

  // Upload to backend
  resumeUploading.value = true
  resumeUploadProgress.value = 10
  try {
    const formData = new FormData()
    formData.append('file', f)
    const { data } = await axios.post(`${API}/interview/upload-resume`, formData, {
      onUploadProgress: (pe) => {
        resumeUploadProgress.value = Math.round((pe.loaded / pe.total) * 80) + 10
      }
    })
    resumeUploadProgress.value = 100
    resumeFileId.value = data.file_id
    if (data.text) resumeParsedText.value = data.text
    ElMessage.success(`简历已上传并解析：${f.name}`)
  } catch (err) {
    ElMessage.error('简历上传失败，可跳过此步')
    resumeParsedText.value = resumeParsedText.value || '（解析失败，无法预览全文）'
  }
  resumeUploading.value = false
}

// ==================== Phase & Session ====================
const phase = ref('setup') // setup | chatting | loading | report
const startLoading = ref(false)
const sessionId = ref('')
const messages = ref([])
const userInput = ref('')
const aiLoading = ref(false)
const chatRound = ref(0)
const chatRef = ref(null)
const paused = ref(false)
const report = reactive({
  overall_score: 0,
  dimensions: {},
  strengths: [],
  weaknesses: [],
  suggestions: [],
  summary: '',
  sessionId: ''
})
const reportLoading = ref(false)
const reportLoadProgress = ref(0)

// ==================== Countdown Timer ====================
const remainingSeconds = ref(0)
let countdownInterval = null
const riskEvents = ref([])
let lastInputAt = Date.now()
let silenceTimer = null

const riskScore = computed(() => Math.min(100, riskEvents.value.length * 18))
const riskScoreColor = computed(() => riskScore.value >= 60 ? '#F97316' : riskScore.value >= 30 ? '#0EA5E9' : '#2563EB')
const riskLevelTag = computed(() => {
  if (riskScore.value >= 60) return { label: '需复盘', type: 'warning' }
  if (riskScore.value >= 30) return { label: '有记录', type: 'primary' }
  return { label: '平稳', type: 'success' }
})

function addRiskEvent(title, detail) {
  if (phase.value !== 'chatting') return
  const latest = riskEvents.value[riskEvents.value.length - 1]
  if (latest && latest.title === title && Date.now() - latest.time < 15000) return
  riskEvents.value.push({ id: `${Date.now()}-${Math.random().toString(16).slice(2)}`, title, detail, time: Date.now() })
}

function recordManualRisk(title, detail) {
  addRiskEvent(title, detail)
  ElMessage.info('已记录到本场面试报告')
}

function clearRiskEvents() {
  riskEvents.value = []
}

function formatRiskTime(ts) {
  const d = new Date(ts)
  return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

function startRiskWatch() {
  lastInputAt = Date.now()
  stopRiskWatch()
  document.addEventListener('visibilitychange', handleVisibilityRisk)
  silenceTimer = setInterval(() => {
    if (phase.value === 'chatting' && !paused.value && Date.now() - lastInputAt > 90000) {
      addRiskEvent('长时间未作答', '超过 90 秒没有输入或发送回答，建议复盘是否卡顿、离席或需要降低难度。')
      lastInputAt = Date.now()
    }
  }, 15000)
}

function stopRiskWatch() {
  document.removeEventListener('visibilitychange', handleVisibilityRisk)
  if (silenceTimer) {
    clearInterval(silenceTimer)
    silenceTimer = null
  }
}

function handleVisibilityRisk() {
  if (document.hidden && phase.value === 'chatting') {
    addRiskEvent('离开面试页面', '面试过程中页面切到后台或失去可见性，系统仅记录供复盘参考。')
  }
}

watch(userInput, (val) => {
  if (val.trim()) lastInputAt = Date.now()
})

const formattedTime = computed(() => {
  const m = Math.floor(remainingSeconds.value / 60)
  const s = remainingSeconds.value % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
})

function startCountdown() {
  remainingSeconds.value = interviewDuration.value * 60
  countdownInterval = setInterval(() => {
    if (paused.value) return
    if (remainingSeconds.value > 0) {
      remainingSeconds.value--
    } else {
      // Time's up — auto-end interview
      ElMessage.warning('⏰ 面试时间到！')
      handleEndInterview()
    }
  }, 1000)
}

function stopCountdown() {
  if (countdownInterval) {
    clearInterval(countdownInterval)
    countdownInterval = null
  }
}

function togglePause() {
  paused.value = !paused.value
  ElMessage.info(paused.value ? '⏸️ 面试已暂停' : '▶️ 面试继续')
}

// ==================== Camera ====================
const videoRef = ref(null)
const cameraOn = ref(false)
const cameraReady = ref(false)
const cameraToggling = ref(false)
let cameraStream = null
const currentEmotion = ref(null)
const allExpressions = ref([])
let captureTimer = null
let captureCanvas = null

async function toggleCamera(val) {
  if (val && !window.__cameraPrivacyConsented) {
    try {
      await ElMessageBox.confirm(
        '开启摄像头后，系统会定时截取画面发送到 AI 服务器进行表情分析（紧张/自信/困惑等），' +
        '用于提升面试评分准确度。<br><br>' +
        '<b>• 画面数据仅用于当前面试评分</b><br>' +
        '<b>• 不会保存或外传你的视频</b><br>' +
        '<b>• 可随时关闭摄像头</b>',
        '使用摄像头须知',
        { confirmButtonText: '我知道了，开始', cancelButtonText: '暂不使用',
          dangerouslyUseHTMLString: true, type: 'info' }
      )
      window.__cameraPrivacyConsented = true
    } catch {
      cameraOn.value = false
      return
    }
  }
  cameraToggling.value = true
  try {
    if (val) {
      await startCamera()
    } else {
      stopCamera()
    }
  } catch (err) {
    ElMessage.warning('摄像头操作失败')
    cameraOn.value = false
  }
  cameraToggling.value = false
}

async function startCamera() {
  try {
    // 先渲染 video 元素（v-if 需要 cameraOn && cameraReady）
    cameraOn.value = true
    cameraReady.value = true
    await nextTick()
    // 此时 videoRef 已挂载，获取流并绑定
    cameraStream = await navigator.mediaDevices.getUserMedia({
      video: { width: 320, height: 240, facingMode: 'user' },
      audio: false
    })
    if (videoRef.value) {
      videoRef.value.srcObject = cameraStream
    }
    // Start emotion capture
    captureTimer = setInterval(captureAndAnalyze, 10000)
  } catch (err) {
    ElMessage.warning('无法开启摄像头：' + (err.message || '权限被拒绝'))
    // 恢复状态
    cameraOn.value = false
    cameraReady.value = false
    throw err
  }
}

function stopCamera() {
  if (captureTimer) {
    clearInterval(captureTimer)
    captureTimer = null
  }
  if (cameraStream) {
    cameraStream.getTracks().forEach(t => t.stop())
    cameraStream = null
  }
  cameraOn.value = false
  cameraReady.value = false
  currentEmotion.value = null
}

async function captureAndAnalyze() {
  if (!videoRef.value || !cameraOn.value) return
  try {
    if (!captureCanvas) captureCanvas = document.createElement('canvas')
    captureCanvas.width = 320
    captureCanvas.height = 240
    const ctx = captureCanvas.getContext('2d')
    ctx.drawImage(videoRef.value, 0, 0, 320, 240)
    const base64 = captureCanvas.toDataURL('image/jpeg', 0.7).split(',')[1]
    const { data } = await axios.post(`${API}/interview/analyze-expression`, { image: base64 })
    currentEmotion.value = data
    allExpressions.value.push({ ...data, time: Date.now(), round: chatRound.value })
  } catch { /* silent */ }
}

// ==================== Microphone + Recording ====================
const micOn = ref(false)
let micStream = null

async function toggleMic() {
  if (micOn.value) {
    if (micStream) {
      micStream.getAudioTracks().forEach(t => t.stop())
      micStream = null
    }
    micOn.value = false
    return
  }
  try {
    micStream = await navigator.mediaDevices.getUserMedia({ audio: true })
    micOn.value = true
    ElMessage.success('🎙️ 麦克风已开启')
  } catch {
    ElMessage.warning('无法开启麦克风')
  }
}

// ==================== Video Recording ====================
const isRecordingVideo = ref(false)
const recordingDuration = ref('00:00')
let mediaRecorder = null
let recordedChunks = []
let recordingTimer = null
let recordingStartTime = 0

async function toggleRecording() {
  if (isRecordingVideo.value) {
    stopRecording()
  } else {
    startRecording()
  }
}

async function startRecording() {
  if (!cameraStream) {
    ElMessage.warning('请先开启摄像头')
    return
  }
  if (!micOn.value) {
    ElMessage.warning('请先开启麦克风')
    return
  }
  try {
    // Create combined stream from camera (already includes audio if available)
    recordedChunks = []
    let combinedStream = cameraStream // cameraStream already has audio from getUserMedia

    // Check if we need to add microphone audio separately
    const audioTracks = cameraStream.getAudioTracks()
    if (!audioTracks.length && micStream) {
      // If camera stream has no audio, try to combine
      const tracks = [...cameraStream.getVideoTracks(), ...micStream.getAudioTracks()]
      combinedStream = new MediaStream(tracks)
    }

    const mimeType = MediaRecorder.isTypeSupported('video/webm;codecs=vp9,opus')
      ? 'video/webm;codecs=vp9,opus'
      : MediaRecorder.isTypeSupported('video/webm;codecs=vp8,opus')
        ? 'video/webm;codecs=vp8,opus'
        : 'video/webm'

    mediaRecorder = new MediaRecorder(combinedStream, { mimeType })

    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) recordedChunks.push(e.data)
    }

    mediaRecorder.onstop = async () => {
      await uploadRecording()
    }

    mediaRecorder.onerror = () => {
      ElMessage.error('录制出错')
      isRecordingVideo.value = false
    }

    mediaRecorder.start(1000) // collect data every second
    isRecordingVideo.value = true
    recordingStartTime = Date.now()

    // Start timer
    recordingTimer = setInterval(() => {
      const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000)
      const m = String(Math.floor(elapsed / 60)).padStart(2, '0')
      const s = String(elapsed % 60).padStart(2, '0')
      recordingDuration.value = `${m}:${s}`
    }, 1000)

    ElMessage.success('⏺️ 开始录制')
  } catch (err) {
    ElMessage.error('启动录制失败：' + (err.message || '未知错误'))
  }
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== 'inactive') {
    mediaRecorder.stop()
  }
  isRecordingVideo.value = false
  if (recordingTimer) {
    clearInterval(recordingTimer)
    recordingTimer = null
  }
}

async function uploadRecording() {
  if (!recordedChunks.length || !sessionId.value) {
    recordedChunks = []
    return
  }
  try {
    const blob = new Blob(recordedChunks, { type: 'video/webm' })
    const formData = new FormData()
    formData.append('file', blob, `interview_${sessionId.value}_${Date.now()}.webm`)
    formData.append('session_id', sessionId.value)
    await axios.post(`${API}/interview/upload-recording`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    ElMessage.success('✅ 录制已上传')
  } catch {
    ElMessage.warning('录制上传失败')
  }
  recordedChunks = []
}

// ==================== Voice Input (SpeechRecognition) ====================
const isRecording = ref(false)
const voiceActive = ref(false)
let recognition = null
const speechRecogSupported = computed(() => {
  return !!(window.SpeechRecognition || window.webkitSpeechRecognition)
})

function toggleVoiceInput() {
  if (isRecording.value) {
    stopVoiceInput()
  } else {
    startVoiceInput()
  }
}

function startVoiceInput() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition
  if (!SR) {
    ElMessage.warning('当前浏览器不支持语音输入')
    return
  }
  if (isRecording.value) return

  recognition = new SR()
  recognition.lang = 'zh-CN'
  recognition.interimResults = true
  recognition.continuous = true

  isRecording.value = true
  voiceActive.value = true

  recognition.onresult = (e) => {
    let finalTranscript = ''
    let interimTranscript = ''
    for (let i = e.resultIndex; i < e.results.length; i++) {
      if (e.results[i].isFinal) {
        finalTranscript += e.results[i][0].transcript
      } else {
        interimTranscript += e.results[i][0].transcript
      }
    }
    if (finalTranscript) {
      userInput.value += (userInput.value ? ' ' : '') + finalTranscript
    }
    if (interimTranscript) {
      // 显示临时结果让用户看到实时转写
      userInput.value = userInput.value.replace(/\s*\(.*?\)$/, '')
      userInput.value += ' (' + interimTranscript + ')'
    }
  }

  recognition.onerror = (evt) => {
    console.warn('SpeechRecognition error:', evt.error)
    if (evt.error === 'not-allowed') {
      ElMessage.warning('麦克风权限被拒绝，请使用文字输入')
    }
    isRecording.value = false
    voiceActive.value = false
  }

  recognition.onend = () => {
    isRecording.value = false
    voiceActive.value = false
  }

  try {
    recognition.start()
  } catch {
    isRecording.value = false
    voiceActive.value = false
    ElMessage.warning('语音输入启动失败')
  }
}

function stopVoiceInput() {
  if (recognition) {
    try { recognition.stop() } catch { /* ignore */ }
    recognition = null
  }
  isRecording.value = false
  voiceActive.value = false
}

// ==================== SpeechSynthesis (TTS) ====================
const autoSpeakEnabled = ref(true)
const speechSynthSupported = computed(() => {
  return !!window.speechSynthesis
})

// Pick the best Chinese voice available on macOS
let cachedBestVoice = null
let availableVoices = []
function getBestChineseVoice() {
  if (cachedBestVoice) return cachedBestVoice
  const voices = window.speechSynthesis.getVoices()
  availableVoices = voices
  if (!voices.length) return null

  // Better-sounding Chinese voices on modern macOS, in preference order
  const preferredNames = [
    // Any enhanced/premium/neural voice
    v => /zh(-CN)?/.test(v.lang) && /(premium|enhanced|neural|high quality)/i.test(v.name),
    // Apple's newer neural-capable voices (generally sound more natural)
    v => /zh(-CN)?/.test(v.lang) && ['Eddy','Flo','Sandy','Reed','Shelley','Rocko'].includes(v.name),
    // Fall back to Tingting (standard Chinese voice)
    v => v.name === 'Tingting',
    // Any Chinese voice
    v => /zh(-CN)?/.test(v.lang),
    // Any voice with Chinese support
    v => /zh/.test(v.lang),
  ]
  for (const matcher of preferredNames) {
    const hit = voices.find(matcher)
    if (hit) { cachedBestVoice = hit; return hit }
  }
  return null
}

// Expose available voices for UI switching
function getAvailableChineseVoices() {
  const voices = window.speechSynthesis.getVoices()
  return voices.filter(v => /zh/.test(v.lang))
}

// Try pre-load voices (they load async)
if (window.speechSynthesis) {
  window.speechSynthesis.getVoices() // trigger
  window.speechSynthesis.onvoiceschanged = () => {
    cachedBestVoice = null // reset so next call picks it up
  }
}

function speakText(text) {
  if (!window.speechSynthesis) return
  // Clean HTML tags from text
  const cleanText = text.replace(/<[^>]*>/g, '')
  const bestVoice = getBestChineseVoice()

  function createUtterance(t) {
    const u = new SpeechSynthesisUtterance(t)
    u.lang = 'zh-CN'
    u.rate = 1.0
    u.pitch = 1.0
    if (bestVoice) u.voice = bestVoice
    return u
  }

  // Split into smaller chunks for better handling
  const maxLen = 200
  if (cleanText.length <= maxLen) {
    window.speechSynthesis.speak(createUtterance(cleanText))
  } else {
    const chunks = []
    for (let i = 0; i < cleanText.length; i += maxLen) {
      chunks.push(cleanText.slice(i, i + maxLen))
    }
    let idx = 0
    function speakNext() {
      if (idx >= chunks.length) return
      const u = createUtterance(chunks[idx])
      u.onend = () => { idx++; speakNext() }
      window.speechSynthesis.speak(u)
    }
    speakNext()
  }
}

// ==================== Resume-driven keywords ====================
const currentKeywords = ref([])
const resumeQuestions = ref([])
let resumeQuestionIndex = 0

// ==================== Computed ====================
const modeLabel = computed(() => {
  const map = { basic: '基础模式', resume: '简历驱动', stress: '压力面试' }
  return map[mode.value] || mode.value
})
const modeTagType = computed(() => {
  const map = { basic: 'primary', resume: 'success', stress: 'danger' }
  return map[mode.value] || 'info'
})

function scoreColor(v) {
  return v >= 80 ? '#67c23a' : v >= 60 ? '#e6a23c' : '#f56c6c'
}

// ==================== Radar Chart Computed ====================
const cx = 150, cy = 150, R = 120
const radarKeys = ['专业知识掌握度', '语言表达与逻辑', '临场应变能力', '岗位匹配度']
const angles = [-Math.PI / 2, 0, Math.PI / 2, Math.PI] // top, right, bottom, left

function polar(angle, r) {
  return { x: cx + r * Math.cos(angle), y: cy + r * Math.sin(angle) }
}

const radarGrid = computed(() => [20, 40, 60, 80].map(level => {
  const pct = level / 100
  const pts = angles.map(a => {
    const p = polar(a, R * pct)
    return `${p.x.toFixed(1)},${p.y.toFixed(1)}`
  }).join(' ')
  return { key: `grid-${level}`, points: pts }
}))

const radarAxes = computed(() => radarKeys.map((_, i) => {
  const p = polar(angles[i], R)
  return { key: `axis-${i}`, x: p.x.toFixed(1), y: p.y.toFixed(1) }
}))

const radarDataPoints = computed(() => {
  const dims = report.dimensions || {}
  return angles.map((a, i) => {
    const k = radarKeys[i]
    const score = (dims[k]?.score || 0) / 100
    const p = polar(a, R * Math.min(score, 1))
    return `${p.x.toFixed(1)},${p.y.toFixed(1)}`
  }).join(' ')
})

const radarNodes = computed(() => {
  const dims = report.dimensions || {}
  return angles.map((a, i) => {
    const k = radarKeys[i]
    const score = (dims[k]?.score || 0) / 100
    const p = polar(a, R * Math.min(score, 1))
    return { key: `node-${i}`, x: p.x.toFixed(1), y: p.y.toFixed(1) }
  })
})

const radarLabels = computed(() => radarKeys.map((k, i) => {
  const p = polar(angles[i], R + 18)
  return { key: `label-${i}`, label: k, x: p.x.toFixed(1), y: p.y.toFixed(1) }
}))

const radarScores = computed(() => {
  const dims = report.dimensions || {}
  return radarKeys.map((k, i) => {
    const score = dims[k]?.score || 0
    const p = polar(angles[i], R - 14)
    return { key: `score-${i}`, score, x: p.x.toFixed(1), y: p.y.toFixed(1) }
  })
})

function emotionTagType(e) {
  const m = { '开心': 'success', '自信': 'success', '平静': 'info', '困惑': 'warning', '紧张': 'danger', '焦虑': 'danger' }
  return m[e] || 'info'
}

function edBarColor(k, v) {
  if (['开心', '自信', '平静'].includes(k)) return `rgba(103,194,58,${0.4 + v / 150})`
  return `rgba(245,108,108,${0.4 + v / 150})`
}

// ==================== Chat Core ====================
function scrollToBottom() {
  nextTick(() => {
    if (chatRef.value) {
      chatRef.value.scrollTop = chatRef.value.scrollHeight
    }
  })
}

function backToEntry() {
  cleanupAll()
  window.location.href = '/interview'
}

function goToHistory() {
  cleanupAll()
  $router.push('/interview/history')
}

function goToDetail(id) {
  cleanupAll()
  $router.push(`/interview/history/${id}`)
}

// ==================== Start Interview ====================
async function handleStartInterview() {
  if (!canProceedJob.value) {
    ElMessage.warning('请先选择或填写目标岗位')
    return
  }

  startLoading.value = true
  messages.value = []
  phase.value = 'chatting'
  chatRound.value = 0
  paused.value = false
  riskEvents.value = []
  startRiskWatch()

  // If resume mode and we have a resume, fetch resume questions first
  if (mode.value === 'resume' && resumeParsedText.value) {
    try {
      const { data } = await axios.post(`${API}/interview/resume-questions`, {
        resume_text: resumeParsedText.value,
        count: 10
      })
      resumeQuestions.value = data.questions || []
      resumeQuestionIndex = 0
    } catch {
      ElMessage.warning('简历问题生成失败，将使用默认问题')
      resumeQuestions.value = []
    }
  }

  try {
    const { data } = await axios.post(`${API}/interview/chat/start`, {
      job: buildInterviewJobPrompt(),
      category: category.value || interviewTargetLabel.value,
      mode: mode.value,
      custom_material: customInterview.material.trim()
    })
    sessionId.value = data.session_id
    // 使用后端实时生成的第一句话（压力/普通模式完全不同），而非硬编码固定文案
    const firstMsg = data.message || buildOpeningMessage()
    messages.value.push({ role: 'assistant', content: firstMsg, time: Date.now() })

    // Auto-speak the first message
    if (autoSpeakEnabled.value) {
      speakText(firstMsg)
    }

    // Extract keywords from first message for resume mode
    updateKeywords(firstMsg)

    // Start camera automatically
    try {
      await startCamera()
      // Also open mic
      if (!micOn.value) await toggleMic()
    } catch { /* optional */ }

    // Start countdown
    startCountdown()

    scrollToBottom()
  } catch (err) {
    ElMessage.error('启动面试失败：' + (err.response?.data?.detail || err.message || '未知错误'))
    phase.value = 'setup'
    stopRiskWatch()
  }
  startLoading.value = false
}

function buildOpeningMessage() {
  const jobName = interviewTargetLabel.value || '目标岗位'
  const modeName = modeLabel.value || '模拟'
  const materialHint = customInterview.material.trim() ? '我已经读取了你提供的自定义面试材料，后面会按材料里的要求追问。' : ''
  return `你好，我是启途 AI 面试官。今天我们按「${jobName}」做一场${modeName}面试。${materialHint}先别着急介绍项目，我会先用一两个基础问题帮你进入状态；如果后面需要聊项目，我会提前说明。第一个问题：你为什么想了解或尝试「${jobName}」这个方向？`
}

function updateKeywords(aiMsg) {
  if (mode.value !== 'resume') {
    currentKeywords.value = []
    return
  }
  // Extract meaningful keywords from AI message for hints
  const commonWords = ['的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '他', '她', '它', '们', '那', '什么', '怎么', '为什么', '请', '可以', '能', '吗', '吧', '呢', '啊']
  const words = aiMsg.split(/[\s,，。、；：！？?()（）\[\]【】""''"《》\n]+/).filter(w => w.length > 1 && !commonWords.includes(w))
  const uniqueWords = [...new Set(words)].slice(0, 6)
  currentKeywords.value = uniqueWords.map(w => ({
    text: w,
    type: 'info'
  }))

  // Also add resume-related keywords if available
  if (resumeParsedText.value) {
    const resumeWords = resumeParsedText.value.split(/[\s,，。、；：\n]+/).filter(w => w.length > 1 && w.length <= 10)
    const resumeKeywords = resumeWords.filter(w => !commonWords.includes(w))
    const selectedResume = [...new Set(resumeKeywords)].slice(0, 4)
    selectedResume.forEach(w => {
      if (!currentKeywords.value.find(k => k.text === w)) {
        currentKeywords.value.push({ text: w, type: 'success' })
      }
    })
    // Limit total
    if (currentKeywords.value.length > 10) {
      currentKeywords.value = currentKeywords.value.slice(0, 10)
    }
  }
}

// ==================== Send Message ====================
async function sendMessage() {
  const msg = userInput.value.trim()
  if (!msg || aiLoading.value || !sessionId.value || paused.value) return

  userInput.value = ''
  messages.value.push({ role: 'user', content: msg, time: Date.now() })
  lastInputAt = Date.now()
  aiLoading.value = true
  scrollToBottom()

  try {
    // For resume mode, if we have pre-generated questions, use them
    if (mode.value === 'resume' && resumeQuestions.value.length > 0 && resumeQuestionIndex < resumeQuestions.value.length) {
      // Normal chat but the AI handles it
    }

    const { data } = await axios.post(`${API}/interview/chat`, {
      session_id: sessionId.value,
      message: msg
    })

    if (data.error) {
      ElMessage.error(data.error)
      aiLoading.value = false
      return
    }

    const aiMsg = data.message || '好的，让我们继续。'
    messages.value.push({ role: 'assistant', content: aiMsg, time: Date.now() })
    chatRound.value = data.round || chatRound.value + 1

    // Auto-speak
    if (autoSpeakEnabled.value) {
      speakText(aiMsg)
    }

    // Update keyword hints
    updateKeywords(aiMsg)
  } catch (err) {
    ElMessage.error('发送失败，请重试')
  }
  aiLoading.value = false
  scrollToBottom()
}

// ==================== Skip Question ====================
async function skipQuestion() {
  if (aiLoading.value || !sessionId.value) return
  aiLoading.value = true
  addRiskEvent('跳过题目', '候选人主动跳过了一道题，报告中仅作为练习节奏参考。')
  try {
    const { data } = await axios.post(`${API}/interview/chat`, {
      session_id: sessionId.value,
      message: '跳过本题，请换一个问题'
    })
    if (data.error) {
      ElMessage.error(data.error)
      aiLoading.value = false
      return
    }
    const aiMsg = data.message || '好的，我们换一个问题。'
    messages.value.push({ role: 'assistant', content: aiMsg, time: Date.now() })
    chatRound.value = data.round || chatRound.value + 1
    if (autoSpeakEnabled.value) speakText(aiMsg)
    updateKeywords(aiMsg)
  } catch {
    ElMessage.error('操作失败')
  }
  aiLoading.value = false
  scrollToBottom()
}

// ==================== End Interview ====================
async function handleEndInterview() {
  if (!sessionId.value) return

  try {
    await ElMessageBox.confirm('确定要结束当前面试吗？结束后将生成评估报告。', '确认结束', {
      confirmButtonText: '结束面试',
      cancelButtonText: '继续面试',
      type: 'warning'
    })
  } catch {
    return // cancelled
  }

  // Stop recording if active
  if (isRecordingVideo.value) {
    stopRecording()
  }

  stopCountdown()
  aiLoading.value = true
  phase.value = 'loading'
  reportLoading.value = true
  reportLoadProgress.value = 0

  // Progress animation
  const progressInterval = setInterval(() => {
    if (reportLoadProgress.value < 90) {
      reportLoadProgress.value += Math.random() * 8 + 2
    }
  }, 300)

  try {
    const { data } = await axios.post(`${API}/interview/chat/end`, {
      session_id: sessionId.value
    })

    clearInterval(progressInterval)
    reportLoadProgress.value = 100

    if (data.error) {
      ElMessage.error(data.error)
      aiLoading.value = false
      phase.value = 'chatting'
      reportLoading.value = false
      return
    }

    Object.assign(report, data)
    report.sessionId = sessionId.value
    stopCamera()
    stopVoiceInput()
    if (micOn.value) await toggleMic()

    // Save to database
    try {
      const scores = Object.values(data.dimensions || {}).map(d => d.score || 0)
      await axios.post(`${API}/interview/save-session`, {
        job: data.job || interviewTargetLabel.value,
        category: category.value || interviewTargetLabel.value,
        mode: mode.value,
        total_questions: data.total_questions || Math.floor(messages.value.filter(m => m.role === 'user').length),
        average_score: String(data.overall_score || 0),
        highest_score: String(Math.max(...scores, data.overall_score || 0)),
        lowest_score: String(Math.min(...scores, data.overall_score || 0)),
        answers_json: JSON.stringify(messages.value.map(m => ({ role: m.role, content: m.content }))),
        dimensions_json: JSON.stringify(data.dimensions || {}),
        strengths_json: JSON.stringify(data.strengths || []),
        weaknesses_json: JSON.stringify(data.weaknesses || []),
        suggestions_json: JSON.stringify([
          ...(data.suggestions || []),
          ...(riskEvents.value.length ? [`行为观察：本场记录 ${riskEvents.value.length} 条异常片段，仅供复盘，不作为作弊结论。`] : [])
        ]),
        emotions_json: JSON.stringify(allExpressions.value)
      })
    } catch { /* silent */ }

    // Small delay to show 100%
    await new Promise(r => setTimeout(r, 500))
    phase.value = 'report'
  } catch (err) {
    clearInterval(progressInterval)
    ElMessage.error('生成报告失败')
    phase.value = 'chatting'
  }
  aiLoading.value = false
  reportLoading.value = false
}

// ==================== Reset ====================
function resetToSetup() {
  cleanupAll()
  phase.value = 'setup'
  setupStep.value = 1
  messages.value = []
  sessionId.value = ''
  report.overall_score = 0
  report.dimensions = {}
  report.strengths = []
  report.weaknesses = []
  report.suggestions = []
  report.summary = ''
  report.sessionId = ''
  currentKeywords.value = []
  resumeQuestions.value = []
  resumeQuestionIndex = 0
  riskEvents.value = []
  stopRiskWatch()
}

// ==================== Cleanup ====================
function cleanupAll() {
  stopCamera()
  stopVoiceInput()
  stopCountdown()
  stopRiskWatch()
  if (isRecordingVideo.value) stopRecording()
  if (micOn.value && micStream) {
    micStream.getAudioTracks().forEach(t => t.stop())
    micStream = null
    micOn.value = false
  }
  if (window.speechSynthesis) {
    window.speechSynthesis.cancel()
  }
}

onUnmounted(() => {
  cleanupAll()
})
</script>

<style scoped>
/* ==================== Global CSS Variables ==================== */
:root {
  --session-bg: linear-gradient(180deg, #F8FBFF 0%, #FFFFFF 46%);
  --session-card-bg: var(--bg-card, #ffffff);
  --session-border: #BFDBFE;
  --session-text: var(--text-body, #475569);
  --session-text-muted: var(--text-muted, #94A3B8);
  --session-shadow: 0 12px 30px rgba(37,99,235,.07);
  --session-radius: 18px;
}

/* ==================== Full-width Layout ==================== */
.session-page {
  width: 100%;
  min-height: 100vh;
  padding: 0 0 2rem;
  background: var(--session-bg);
}
.session-topbar {
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
.session-topbar :deep(.el-button) {
  color: var(--primary);
  font-weight: 800;
}
.session-title {
  font-weight: 600;
  font-size: 1rem;
  color: var(--text-heading, #333);
}
.session-title i {
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
.custom-interview-hero {
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
.custom-interview-hero h3 {
  margin: 8px 0 6px;
  color: var(--text-heading);
  font-size: 22px;
  line-height: 1.35;
  font-weight: 900;
}
.custom-interview-hero p {
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
.custom-form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}
.custom-summary-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 4px;
}
.custom-summary-pill {
  padding: 7px 11px;
  border-radius: 999px;
  background: #EFF6FF;
  border: 1px solid #BFDBFE;
  color: var(--primary);
  font-size: 13px;
  font-weight: 800;
}
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
.resume-hint-card {
  padding: 16px 18px;
  margin: 4px 0 6px;
  border-radius: 16px;
  background: var(--primary-light);
  border: 1px solid #BFDBFE;
}
.resume-hint-card b {
  color: var(--primary);
  font-size: 17px;
  font-weight: 900;
}
.resume-hint-card p {
  margin-top: 4px;
  color: var(--text-light);
  font-size: 14px;
}
@media (max-width: 900px) {
  .setup-shell {
    width: calc(100vw - 32px);
    grid-template-columns: 1fr;
  }
  .setup-side h1 { font-size: 26px; }
  .custom-form-grid { grid-template-columns: 1fr; }
  .risk-report-item { grid-template-columns: 1fr; }
}
.resume-upload-area {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}
.resume-file-name {
  font-size: 0.85rem;
  color: var(--session-text);
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.resume-preview {
  font-size: 0.78rem;
  color: var(--text-body, #444);
  background: #F8FBFF;
  padding: 0.8rem;
  border-radius: var(--radius-sm, 8px);
  max-height: 200px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
}
.resume-uploading {
  text-align: center;
  padding: 0.5rem 0;
  color: var(--session-text-muted);
  font-size: 0.85rem;
}
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
  border-radius: var(--radius-sm, 8px) !important;
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

/* ==================== Interview Topbar ==================== */
.interview-topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 1rem;
  background: rgba(255,255,255,.9);
  border-radius: 18px;
  margin-bottom: 0.9rem;
  box-shadow: var(--session-shadow);
  gap: 12px;
  border: 1.5px dashed var(--session-border);
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
  background: var(--primary-light);
  border: 1px solid #DBEAFE;
  border-radius: 999px;
}
.countdown-warning {
  color: #C85A20 !important;
  background: #fef0f0 !important;
  animation: pulse 1s infinite;
}
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
.it-right {
  display: flex;
  align-items: center;
  gap: 8px;
}
.round-badge {
  font-size: 0.78rem;
  color: var(--session-text-muted);
  background: var(--primary-light);
  border: 1px solid #DBEAFE;
  padding: 3px 10px;
  border-radius: 999px;
}

/* ==================== Chat Layout ==================== */
.interview-phase {
  height: calc(100vh - 150px);
  display: flex;
  flex-direction: column;
}
.chat-layout {
  flex: 1;
  display: flex;
  gap: 16px;
  min-height: 0;
  overflow: hidden;
}
.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--session-card-bg);
  border-radius: 22px;
  box-shadow: var(--session-shadow);
  overflow: hidden;
  border: 1.5px dashed var(--session-border);
}
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
}
.chat-loading-msg {
  text-align: center;
  padding: 3rem;
  color: var(--session-text-muted);
}
.chat-bubble {
  display: flex;
  gap: 10px;
  margin-bottom: 1rem;
  max-width: 85%;
}
.chat-bubble.user {
  flex-direction: row-reverse;
  margin-left: auto;
}
.chat-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  background: #E6EDF5;
  flex-shrink: 0;
  color: var(--text-body, #555);
}
.chat-bubble.ai .chat-avatar {
  background: var(--primary-light);
  color: var(--primary);
}
.chat-bubble.user .chat-avatar {
  background: #DBEAFE;
  color: var(--primary);
}
.chat-content {
  padding: 0.6rem 1rem;
  border-radius: 12px;
  font-size: 0.9rem;
  line-height: 1.7;
  position: relative;
}
.chat-bubble.ai .chat-content {
  background: #F8FBFF;
  color: var(--text-body, #333);
  border: 1px solid #DBEAFE;
  border-top-left-radius: 2px;
}
.chat-bubble.user .chat-content {
  background: linear-gradient(145deg, #0EA5E9, #2563EB);
  color: white;
  border-top-right-radius: 2px;
}
.chat-msg-actions {
  margin-top: 4px;
  display: flex;
  gap: 4px;
}
.chat-msg-actions .el-button {
  font-size: 0.75rem;
  padding: 2px 6px;
  min-height: auto;
  color: var(--text-muted, #999);
}

/* Voice indicator */
.voice-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 6px;
  background: #fef0f0;
  color: #C85A20;
  font-size: 0.8rem;
  font-weight: 500;
}
.voice-pulse {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #C85A20;
  animation: voicePulse 1s infinite;
}
@keyframes voicePulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.4); opacity: 0.5; }
}

/* Input bar */
.chat-input-bar {
  border-top: 1px solid var(--session-border);
  padding: 0.6rem;
  background: #F8FBFF;
}
.chat-input-row {
  margin-bottom: 6px;
}
.chat-input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.cia-left {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  min-width: 0;
}
.chat-input-actions > .el-button {
  flex: none;
  min-width: 92px;
}

/* Typing animation */
.typing-dots span {
  animation: dotPulse 1.2s infinite;
  opacity: 0;
}
.typing-dots span:nth-child(2) {
  animation-delay: 0.4s;
}
.typing-dots span:nth-child(3) {
  animation-delay: 0.8s;
}
@keyframes dotPulse {
  0%, 60%, 100% { opacity: 0; }
  30% { opacity: 1; }
}

/* ==================== Sidebar ==================== */
.chat-sidebar {
  flex: 0 0 300px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
}

/* Camera */
.camera-card {
  background: var(--session-card-bg);
  border-radius: var(--session-radius);
  overflow: hidden;
  box-shadow: var(--session-shadow);
  border: 1.5px dashed var(--session-border);
}
.camera-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: var(--primary-light);
  font-size: 0.8rem;
  font-weight: 600;
}
.camera-header i {
  margin-right: 6px;
  color: var(--primary, #2563EB);
}
.camera-controls {
  display: flex;
  align-items: center;
  gap: 6px;
}
.camera-wrapper {
  position: relative;
  background: #000;
  aspect-ratio: 4/3;
  overflow: hidden;
}
.user-video {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}
.emotion-overlay {
  position: absolute;
  top: 6px;
  right: 6px;
}
.emotion-badge {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.72rem;
  font-weight: 700;
  backdrop-filter: blur(4px);
}
.recording-badge {
  position: absolute;
  top: 6px;
  left: 6px;
  display: flex;
  align-items: center;
  gap: 4px;
  background: rgba(245, 108, 108, 0.85);
  color: white;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 700;
}
.rec-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #fff;
  animation: recPulse 1s infinite;
}
@keyframes recPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}
.camera-placeholder {
  background: #F8FBFF;
  aspect-ratio: 4/3;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
}
.camera-placeholder-icon {
  font-size: 2.5rem;
  opacity: 0.5;
  color: var(--text-muted, #999);
}
.camera-placeholder-text {
  font-size: 0.85rem;
  color: var(--text-muted, #bbb);
}
.camera-placeholder-sub {
  font-size: 0.75rem;
  color: var(--text-muted, #bbb);
}

/* 行为观察 */
.risk-watch-card {
  padding: 12px;
  border-radius: var(--session-radius);
  background: linear-gradient(145deg, #FFFFFF, #EFF6FF);
  border: 1.5px dashed #BFDBFE;
  box-shadow: var(--session-shadow);
}
.risk-watch-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  color: var(--text-heading);
  font-size: .86rem;
  font-weight: 900;
}
.risk-watch-head i {
  color: var(--primary);
  margin-right: 5px;
}
.risk-watch-desc {
  margin: 8px 0 10px;
  color: var(--session-text-muted);
  font-size: .76rem;
  line-height: 1.6;
}
.risk-score-line {
  display: grid;
  grid-template-columns: 58px 1fr 34px;
  align-items: center;
  gap: 8px;
  font-size: .74rem;
  color: var(--session-text-muted);
}
.risk-actions {
  margin-top: 10px;
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.risk-mini-list {
  margin-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.risk-mini-item {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  padding: 7px 9px;
  border-radius: 10px;
  background: rgba(255,255,255,.78);
  border: 1px solid #DBEAFE;
  font-size: .76rem;
}
.risk-mini-item b { color: var(--text-heading); }
.risk-mini-item small { color: var(--session-text-muted); }
.emotion-details {
  padding: 8px 12px;
}
.ed-row {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 2px;
}
.ed-label {
  font-size: 0.7rem;
  color: var(--text-muted, #888);
  width: 28px;
  text-align: right;
  flex-shrink: 0;
}
.ed-bar-track {
  flex: 1;
  height: 5px;
  background: #E6EDF5;
  border-radius: 3px;
}
.ed-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}
.ed-val {
  font-size: 0.65rem;
  color: var(--text-muted, #888);
  width: 26px;
  text-align: right;
}
.emo-开心, .emo-自信 {
  background: rgba(103, 194, 58, 0.8);
  color: white;
}
.emo-平静 {
  background: rgba(144, 147, 153, 0.7);
  color: white;
}
.emo-困惑 {
  background: rgba(230, 162, 60, 0.8);
  color: white;
}
.emo-紧张, .emo-焦虑, .emo-未知 {
  background: rgba(245, 108, 108, 0.85);
  color: white;
}

/* Recording controls */
.recording-controls {
  background: var(--session-card-bg);
  border-radius: var(--session-radius);
  padding: 10px 12px;
  box-shadow: var(--session-shadow);
  border: 1.5px dashed var(--session-border);
}
.recording-header {
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 8px;
}
.recording-header i {
  margin-right: 6px;
  color: var(--primary, #2563EB);
}
.recording-buttons {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.rec-btn-group {
  display: flex;
  gap: 6px;
}

/* Keyword hints */
.keyword-hints {
  background: var(--session-card-bg);
  border-radius: var(--session-radius);
  padding: 10px 12px;
  box-shadow: var(--session-shadow);
  border: 1.5px dashed var(--session-border);
}
.keyword-header {
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--primary, #2563EB);
}
.keyword-header i {
  margin-right: 6px;
}
.keyword-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}
.kw-tag {
  margin: 0;
}

/* ==================== Report ==================== */
.report-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
}
.report-loading-text {
  margin-top: 1rem;
  color: var(--text-muted, #888);
}
.report-loading-text i {
  margin-right: 6px;
}
.report-card {
  border-radius: var(--session-radius);
  max-width: 960px;
  margin: 0 auto;
  border: 1.5px dashed var(--session-border);
  box-shadow: var(--session-shadow);
}
/* ─── 四维雷达图 ─── */
.radar-section {
  display: flex;
  justify-content: center;
  padding: 1rem 0 0.5rem;
}
.radar-wrap {
  width: 240px;
  height: 240px;
}
.radar-svg {
  width: 100%;
  height: 100%;
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
.risk-report-card {
  margin: 12px 0 16px;
  padding: 16px;
  border-radius: 18px;
  background: #F8FBFF;
  border: 1.5px dashed #BFDBFE;
}
.risk-report-head {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  color: var(--text-heading);
}
.risk-report-head i {
  color: var(--primary);
  margin-top: 3px;
}
.risk-report-head b {
  font-size: 16px;
  font-weight: 900;
}
.risk-report-head p {
  margin-top: 3px;
  color: var(--text-muted);
  font-size: 13px;
}
.risk-report-list {
  margin-top: 12px;
  display: grid;
  gap: 8px;
}
.risk-report-item {
  display: grid;
  grid-template-columns: 88px 120px 1fr;
  gap: 10px;
  padding: 9px 11px;
  border-radius: 12px;
  background: #fff;
  border: 1px solid #DBEAFE;
  font-size: 13px;
}
.risk-report-item span { color: var(--text-muted); }
.risk-report-item b { color: var(--primary); }
.risk-report-item p { color: var(--text-body); }
.report-summary {
  text-align: center;
  font-size: 0.9rem;
  color: var(--primary, #2563EB);
  padding: 0.5rem 0;
  font-weight: 500;
}
.overall-score-area {
  text-align: center;
  padding: 1rem 0;
}
.overall-score-area h3 {
  margin-top: 0.6rem;
}
.dimensions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.8rem;
  margin: 1rem 0;
}
.dim-card {
  background: #F8FBFF;
  border-radius: var(--radius-sm, 10px);
  padding: 0.8rem;
}
.dim-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.4rem;
  font-size: 0.85rem;
}
.dim-comment {
  font-size: 0.78rem;
  color: var(--text-muted, #888);
  margin-top: 4px;
}
.report-lists {
  margin: 1rem 0;
}
.report-lists ul {
  padding-left: 1.2rem;
  color: var(--text-body, #555);
  line-height: 1.8;
  font-size: 0.9rem;
}
.report-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  padding-top: 1.5rem;
}

/* ==================== Responsive ==================== */
@media (max-width: 960px) {
  .chat-layout {
    flex-direction: column;
    overflow-y: auto;
  }
  .chat-sidebar {
    flex: 0 0 auto;
    flex-direction: row;
    flex-wrap: wrap;
  }
  .chat-sidebar > * {
    flex: 1 1 200px;
    min-width: 0;
  }
  .interview-topbar {
    flex-wrap: wrap;
    gap: 6px;
  }
  .it-left {
    flex: 1;
  }
  .it-center {
    order: 3;
    width: 100%;
    justify-content: center;
  }
}
</style>