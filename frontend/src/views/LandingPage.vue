<template>
  <div class="landing">
    <!-- ═══ 第1屏：Hero（正常滚动进入） ═══ -->
    <section class="hero">
<div class="hero-brand">
          <svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>
          <div class="name">启途</div></div>
      <div class="hero-top-right">
        <router-link to="/login" class="login-link">登录</router-link>
        <router-link to="/register" class="btn-reg">免费注册</router-link>
      </div>
      <div class="hero-title"><h1>启途</h1></div>
      <div class="hero-sub1">
        <p>AI驱动的智能面试助手 — 职业探索 · 面试模拟 · 简历优化 · 求职投递助手 · 笔试练习</p>
      </div>
      <div class="hero-sub2"><p>从迷茫到 offer，每一步都有我们帮你</p></div>
      <div class="hero-btn-area"><router-link to="/register" class="btn-start">开始使用</router-link></div>
      <div class="scroll-hint"><div class="mouse"></div><span>SCROLL</span></div>
    </section>

    <!-- ═══ 第2屏：动画区（sticky固定，滚轮控制内容动画） ═══ -->
    <section class="anim-section" ref="animSection">
      <div class="anim-sticky">
        <!-- 蓝色背景 #edf6fd 全程不动 -->

        <!-- 标题（淡出） -->
        <div class="pain-header" ref="painHeader">
          <div class="label">求职路上的那些难题</div>
          <h2>你是否也曾遇到？</h2>
        </div>

        <!-- 左半切片（带卡片左移） — clip-path显示左35% -->
        <div class="slice slice-left" ref="sliceLeft">
          <div class="left-content">
            <div class="pain-cards">
            <div class="pain-card pc-1">
              <div class="pc-num">01</div>
              <div class="pc-body">
                <h3>职业方向迷茫</h3>
                <p>学了四年不知道自己能做什么，招聘网站看花了眼，不知道哪些岗位适合自己</p>
              </div>
              <div class="pc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg></div>
            </div>
            <div class="pain-card pc-2">
              <div class="pc-num">02</div>
              <div class="pc-body">
                <h3>简历石沉大海</h3>
                <p>投了几十份简历都没有回音，不知道简历哪里有问题，HR到底想要什么样的</p>
              </div>
              <div class="pc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div>
            </div>
            <div class="pain-card pc-3">
              <div class="pc-num">03</div>
              <div class="pc-body">
                <h3>面试紧张无措</h3>
                <p>不知道面试会问什么，面完也不知道自己答得怎么样，没机会复盘改进</p>
              </div>
              <div class="pc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18"><rect x="9" y="2" width="6" height="11" rx="3"/><path d="M5 10a7 7 0 0 0 14 0"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg></div>
            </div>
          </div>
          </div>
        </div>

        <!-- 右半切片（人物右移） — clip-path显示右35~95%（人物完整，裁掉右侧空边） -->
        <div class="slice slice-right" ref="sliceRight"></div>

        <!-- 五大功能（爆裂） -->
        <div class="ft-section" ref="ftSection">
          <div class="burst-container" ref="burstContainer">
            <div class="burst-card bc-1" data-angle="-90">
              <div class="bc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="22" height="22"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div>
              <h3>职业探索</h3>
              <p>智能推荐匹配岗位，了解行业趋势、薪资水平，找到最适合你的职业方向</p>
            </div>
            <div class="burst-card bc-2" data-angle="-18">
              <div class="bc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="22" height="22"><rect x="9" y="2" width="6" height="11" rx="3"/><path d="M5 10a7 7 0 0 0 14 0"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg></div>
              <h3>面试模拟</h3>
              <p>AI模拟真实面试场景，多轮对话练习，结束后生成详细评估报告</p>
            </div>
            <div class="burst-card bc-3" data-angle="54">
              <div class="bc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="22" height="22"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg></div>
              <h3>简历优化</h3>
              <p>AI智能分析简历问题，提供针对性修改建议，让HR一眼看到你的亮点</p>
            </div>
            <div class="burst-card bc-4" data-angle="126">
              <div class="bc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="22" height="22"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg></div>
              <h3>求职投递助手</h3>
              <p>管理投递进度，追踪面试反馈，不再错过任何一个机会</p>
            </div>
            <div class="burst-card bc-5" data-angle="198">
              <div class="bc-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="22" height="22"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/></svg></div>
              <h3>笔试练习</h3>
              <p>海量题库覆盖各大公司笔试题型，智能组卷，模拟真实笔试环境</p>
            </div>
          </div>
          <div class="ft-header" ref="ftHeader">
            <div class="label">五大核心功能</div>
            <h2>全方位求职工具</h2>
            <p>从探索到 offer，一站式搞定</p>
          </div>
        </div>

      </div>
    </section>

    <!-- ═══ 第3屏：数据统计（正常滚动接上） ═══ -->
    <section class="stats-section">
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-num">36<span>+</span></div>
          <div class="stat-label">职业方向</div>
        </div>
        <div class="stat-item">
          <div class="stat-num">128<span>+</span></div>
          <div class="stat-label">面试场次</div>
        </div>
        <div class="stat-item">
          <div class="stat-num">85<span>%</span></div>
          <div class="stat-label">通过率提升</div>
        </div>
        <div class="stat-item">
          <div class="stat-num">255<span>+</span></div>
          <div class="stat-label">题库题目</div>
        </div>
      </div>
    </section>

    <!-- ═══ 第4屏：CTA ═══ -->
    <section class="cta-section">
      <div class="container">
        <h2>准备好开启你的求职之旅了吗？</h2>
        <p>注册即可免费使用全部功能</p>
        <router-link to="/register" class="btn-cta">免费注册 →</router-link>
      </div>
    </section>

    <footer>
      <div class="container"><p>启途 QITU · AI求职教育平台 · © 2026</p></div>
    </footer>

</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const animSection = ref(null)
const sliceLeft = ref(null)
const sliceRight = ref(null)
const painHeader = ref(null)
const ftHeader = ref(null)
const burstContainer = ref(null)

const CARD_CONFIG = [
  { angle: -90 }, { angle: -18 }, { angle: 54 },
  { angle: 126 }, { angle: 198 },
]

const easeOutCubic = t => 1 - Math.pow(1 - t, 3)
let ticking = false
let burstCards = []

function updateAll() {
  const vh = window.innerHeight
  const vw = window.innerWidth

  const el = animSection.value
  if (!el) { console.warn('animSection ref is null'); return }
  const rect = el.getBoundingClientRect()
  const scrollable = el.offsetHeight - vh
  let p = 0
  if (rect.top < 0) {
    p = Math.min(1, -rect.top / scrollable)
  }
  p = Math.max(0, Math.min(1, p))

  // Phase 1 (p=0~0.35): 左右分开（人物初始偏移12vw+动画右移，让人物更靠右）
  const splitP = Math.max(0, Math.min(1, p / 0.35))
  const easedSplit = easeOutCubic(splitP)
  const splitDist = Math.max(window.innerWidth * 0.65, 800)
  const rightBase = window.innerWidth * 0.12  // 初始偏移12vw，让人物一上来就更靠右
  if (sliceLeft.value) {
    sliceLeft.value.style.transform = 'translate3d(' + (-splitDist * easedSplit) + 'px, 0, 0)'
  }
  if (sliceRight.value) {
    // 右切片初始偏移rightBase + 动画右移1.6倍 → 人物永远比原来靠右
    sliceRight.value.style.transform = 'translate3d(' + (rightBase + splitDist * 1.6 * easedSplit) + 'px, 0, 0)'
  }
  if (painHeader.value) {
    painHeader.value.style.opacity = '' + (1 - easedSplit)
  }

  // Phase 2: 五大功能从中心出来
  const burstStart = 0.28
  const burstEnd = 0.65
  const bRaw = Math.max(0, Math.min(1, (p - burstStart) / (burstEnd - burstStart)))
  const burstRadius = Math.min(vw, vh) * 0.35

  burstCards.forEach(function(card, i) {
    const cfg = CARD_CONFIG[i]
    const staggerDelay = i * 0.12
    const cp = Math.max(0, Math.min(1, (bRaw - staggerDelay) / (1 - staggerDelay)))

    if (cp <= 0) {
      card.style.opacity = '0'
      card.style.transform = 'translate(-50%, -50%) scale(0)'
      return
    }

    const eased = easeOutCubic(cp)
    const angle = cfg.angle * Math.PI / 180
    const rx = Math.cos(angle) * burstRadius
    const ry = Math.sin(angle) * burstRadius
    const scaleVal = 0.1 + 0.9 * eased

    card.style.opacity = Math.min(1, cp * 2.5)
    card.style.transform = 'translate(-50%, -50%) translate3d(' + (rx * eased) + 'px, ' + (ry * eased) + 'px, 0) scale(' + scaleVal + ')'
  })

  // Phase 3: 标题文字
  const textStart = 0.50
  const textEnd = 0.75
  const textP = Math.max(0, Math.min(1, (p - textStart) / (textEnd - textStart)))
  const easedText = easeOutCubic(textP)

  if (ftHeader.value) {
    ftHeader.value.style.opacity = easedText
    ftHeader.value.style.transform = 'translateY(' + (20 - 20 * easedText) + 'px)'
  }

  if (p >= 1) {
    if (sliceLeft.value) sliceLeft.value.style.transform = 'translate3d(-3000px, 0, 0)'
    if (sliceRight.value) sliceRight.value.style.transform = 'translate3d(5000px, 0, 0)'
    if (painHeader.value) painHeader.value.style.opacity = '0'
    burstCards.forEach(function(c) { c.style.opacity = '1' })
    if (ftHeader.value) {
      ftHeader.value.style.opacity = '1'
      ftHeader.value.style.transform = 'translateY(0)'
    }
  }
}

function onScroll() {
  if (!ticking) {
    requestAnimationFrame(function() {
      updateAll()
      ticking = false
    })
    ticking = true
  }
}

onMounted(() => {
  console.log('LandingPage mounted, animSection:', animSection.value)
  // Collect burst card elements
  if (burstContainer.value) {
    burstCards = Array.from(burstContainer.value.querySelectorAll('.burst-card'))
    console.log('burstCards count:', burstCards.length)
  }
  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', updateAll)
  updateAll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', updateAll)
})
</script>

<style scoped>
* { margin: 0; padding: 0; box-sizing: border-box; }

.landing {
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
  background: #f0f2f6;
  color: #1a2744;
}

/* ═══ 第1屏：Hero（正常滚动） ═══ */
.hero {
  width: 100vw; height: 100vh;
  position: relative;
  background: url('/ea0a3fbb3b02d2ac3e95a8c6d6085339.jpg') center center / cover no-repeat;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute; inset: 0;
  background: rgba(0,0,0,.12);
}
.hero-brand {
  position: absolute; left: 5%; top: 6%; z-index: 10; display: flex; align-items: center; gap: 8px;
}
.hero-brand .icon { font-size: 2vw; color: #fff; text-shadow: 0 2px 8px rgba(0,0,0,.3); }
.hero-brand .name { font-size: 1.4vw; font-weight: 800; color: #fff; letter-spacing: 6px; text-shadow: 0 2px 12px rgba(0,0,0,.35); }
.hero-top-right {
  position: absolute; right: 12%; top: 6%; z-index: 10; display: flex; align-items: center; gap: 0;
}
.hero-top-right .login-link {
  font-size: 1.1vw; color: rgba(255,255,255,.85); text-decoration: none;
  padding: 0 1.2vw; text-shadow: 0 1px 6px rgba(0,0,0,.2); transition: color .2s;
}
.hero-top-right .login-link:hover { color: #fff; }
.hero-top-right .btn-reg {
  display: inline-flex; align-items: center; justify-content: center;
  width: 11vw; height: 4vh;
  background: linear-gradient(135deg,#C85A20,#DA7530); color: #fff;
  font-size: 1vw; font-weight: 600; text-decoration: none;
  border-radius: 6px; box-shadow: 0 4px 14px rgba(200,90,32,.35);
  transition: all .25s;
}
.hero-top-right .btn-reg:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(200,90,32,.45); }
.hero-title {
  position: absolute; left: 50%; top: 40%;
  transform: translate(-50%,-50%); z-index: 10; text-align: center;
}
.hero-title h1 {
  font-size: 7vw; font-weight: 900; color: #fff;
  letter-spacing: 18px; text-shadow: 0 4px 24px rgba(0,0,0,.35); line-height: 1;
}
.hero-sub1 {
  position: absolute; left: 50%; top: 56%;
  transform: translateX(-50%); width: 72vw; z-index: 10; text-align: center;
}
.hero-sub1 p {
  font-size: 1.7vw; font-weight: 500; color: #fff;
  letter-spacing: 4px; text-shadow: 0 2px 12px rgba(0,0,0,.25);
}
.hero-sub2 {
  position: absolute; left: 50%; top: 66%;
  transform: translateX(-50%); width: 52vw; z-index: 10; text-align: center;
}
.hero-sub2 p {
  font-size: 1.1vw; font-weight: 300; color: rgba(255,255,255,.75);
  letter-spacing: 2px; line-height: 1.6; text-shadow: 0 1px 8px rgba(0,0,0,.2);
}
.hero-btn-area {
  position: absolute; left: 50%; top: 74%;
  transform: translateX(-50%); width: 32vw; height: 7vh; z-index: 10;
}
.hero-btn-area .btn-start {
  display: flex; align-items: center; justify-content: center;
  width: 100%; height: 100%;
  background: linear-gradient(135deg,#3D5A80,#2C4460); color: #fff;
  font-size: 1.3vw; font-weight: 600; text-decoration: none;
  border-radius: 10px; box-shadow: 0 6px 24px rgba(61,90,128,.4);
  transition: all .3s; letter-spacing: 4px;
}
.hero-btn-area .btn-start:hover {
  transform: translateY(-2px); box-shadow: 0 10px 32px rgba(61,90,128,.5);
}
.scroll-hint {
  position: absolute; bottom: 24px; left: 50%; transform: translateX(-50%);
  z-index: 10; display: flex; flex-direction: column; align-items: center; gap: 4px;
}
.scroll-hint .mouse {
  width: 18px; height: 28px; border: 2px solid rgba(255,255,255,.4); border-radius: 10px;
  position: relative;
}
.scroll-hint .mouse::after {
  content: ''; position: absolute; top: 5px; left: 50%; transform: translateX(-50%);
  width: 3px; height: 6px; background: rgba(255,255,255,.5); border-radius: 2px;
  animation: scrollDot 2s infinite;
}
@keyframes scrollDot {
  0%{opacity:1;transform:translateX(-50%) translateY(0)}
  100%{opacity:0;transform:translateX(-50%) translateY(12px)}
}
.scroll-hint span { font-size: 11px; color: rgba(255,255,255,.3); letter-spacing: 2px; }

/* ════════════════════════════════════
   动画区 - 用 sticky 固定住，滚轮控制动画
   ════════════════════════════════════ */
.anim-section {
  height: 400vh;
  position: relative;
  background: #edf6fd;
}

.anim-sticky {
  position: sticky;
  top: 0;
  height: 100vh;
  width: 100%;
  overflow: hidden;
  background: #edf6fd;
}

/* ---- 所有动画元素 absolute 叠在 sticky 里 ---- */

/* 标题 */
.pain-header {
  position: absolute;
  top: 6%; left: 0; width: 100%;
  text-align: center; z-index: 10;
  pointer-events: none;
  will-change: opacity;
}
.pain-header .label {
  display: inline-block; padding: 6px 16px; background: rgba(255,255,255,.85);
  backdrop-filter: blur(6px);
  color: #3D5A80; font-size: 13px; font-weight: 600; border-radius: 20px;
  letter-spacing: 1px; margin-bottom: 8px;
}
.pain-header h2 {
  font-size: 30px; font-weight: 800; color: #1a2744;
  text-shadow: 0 1px 4px rgba(255,255,255,.8);
  margin: 0;
}

/* 左右切片 — 各占100%宽，clip-path控制显示比例（左35%，右35~95%=60%，裁掉右5%空边） */
.slice {
  position: absolute;
  top: 0; bottom: 0;
  width: 100%;
  height: 100%;
  will-change: transform;
  z-index: 2;
}
.slice-left {
  left: 0;
  clip-path: inset(0 65% 0 0);  /* 显示左侧35% */
  background: url('/pain-illustration.jpg') left top / auto 100% no-repeat;
}
.slice-right {
  left: 0;
  clip-path: inset(0 5% 0 35%);  /* 显示35%~95%（裁掉右侧5%空边，人物完整） */
  background: url('/pain-illustration.jpg') center top / auto 82% no-repeat;
}

/* 左半内容区 - 宽27%保持卡片不缩，右移8%让卡片靠中间 */
.left-content {
  position: absolute;
  left: 8%; top: 0;
  width: 27%;
  height: 100%;
}

/* 左侧卡片 */
.pain-cards {
  position: relative; z-index: 5;
  padding: 46% 0 6% 10%;
  width: 80%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.pain-card {
  display: flex; align-items: flex-start; gap: 16px;
  background: rgba(255,255,255,.92);
  backdrop-filter: blur(6px);
  border-radius: 14px; padding: 20px 22px;
  box-shadow: 0 2px 16px rgba(0,0,0,.06);
  border-left: 4px solid transparent;
}
.pain-card.pc-1 { border-left-color: #3D5A80; }
.pain-card.pc-2 { border-left-color: #8EA0B8; margin-left: 20px; }
.pain-card.pc-3 { border-left-color: #C85A20; margin-left: 40px; }
.pain-card .pc-num {
  flex-shrink: 0; font-size: 28px; font-weight: 800;
  color: rgba(61,90,128,.1); line-height: 1;
  margin-top: 0; min-width: 30px;
}
.pain-card .pc-body { flex: 1; }
.pain-card .pc-body h3 { font-size: 16px; font-weight: 700; color: #1a2744; margin-bottom: 4px; }
.pain-card .pc-body p { font-size: 12.5px; color: #5a6a7a; line-height: 1.55; margin: 0; }
.pain-card .pc-icon {
  flex-shrink: 0; width: 36px; height: 36px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 10px; font-size: 16px;
}
.pain-card.pc-1 .pc-icon { background: rgba(61,90,128,.1); color: #3D5A80; }
.pain-card.pc-2 .pc-icon { background: rgba(142,160,184,.15); color: #8EA0B8; }
.pain-card.pc-3 .pc-icon { background: rgba(200,90,32,.1); color: #C85A20; }

/* ── 五大功能（在蓝色背景内爆裂） ── */
.ft-section {
  position: absolute;
  inset: 0;
  z-index: 20;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.ft-header {
  text-align: center;
  opacity: 0;
  transform: translateY(20px);
  will-change: transform, opacity;
}
.ft-header .label {
  display: inline-block; padding: 6px 16px; background: rgba(61,90,128,.08);
  color: #3D5A80; font-size: 13px; font-weight: 600; border-radius: 20px;
  letter-spacing: 1px; margin-bottom: 12px;
}
.ft-header h2 { font-size: 32px; font-weight: 800; color: #1a2744; }
.ft-header p { font-size: 14px; color: #5a6a7a; margin-top: 10px; }

.burst-container {
  position: absolute;
  inset: 0;
}

.burst-card {
  position: absolute;
  width: 280px;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%) scale(0);
  opacity: 0;
  background: rgba(255,255,255,.95);
  border-radius: 14px;
  padding: 28px 22px;
  will-change: transform, opacity;
  z-index: 5;
  box-shadow: 0 4px 20px rgba(0,0,0,.08);
}
.burst-card .bc-icon {
  width: 48px; height: 48px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 12px; font-size: 20px; margin-bottom: 14px;
}
.bc-1 .bc-icon { background: rgba(61,90,128,.1); color: #3D5A80; }
.bc-2 .bc-icon { background: rgba(200,90,32,.1); color: #C85A20; }
.bc-3 .bc-icon { background: rgba(142,160,184,.15); color: #8EA0B8; }
.bc-4 .bc-icon { background: rgba(191,168,149,.15); color: #BFA895; }
.bc-5 .bc-icon { background: rgba(61,90,128,.08); color: #3D5A80; }
.burst-card h3 { font-size: 17px; font-weight: 700; color: #1a2744; margin-bottom: 8px; }
.burst-card p { font-size: 13px; color: #5a6a7a; line-height: 1.6; margin: 0; }

/* ═══ 第3屏：数据统计 ═══ */
.stats-section {
  background: #3D5A80; padding: 70px 0;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  max-width: 1100px; margin: 0 auto; padding: 0 24px; gap: 24px;
}
.stat-item { text-align: center; }
.stat-item .stat-num {
  font-size: 42px; font-weight: 800; color: #fff; line-height: 1;
}
.stat-item .stat-num span { color: rgba(255,255,255,.5); font-size: 24px; }
.stat-item .stat-label { font-size: 13px; color: rgba(255,255,255,.6); margin-top: 8px; letter-spacing: 1px; }

/* ═══ 第4屏：CTA ═══ */
.cta-section {
  padding: 70px 0;
  background: linear-gradient(135deg,#1a2744,#2C4460);
  text-align: center;
}
.cta-section h2 { font-size: 30px; font-weight: 800; color: #fff; margin-bottom: 10px; }
.cta-section p { font-size: 14px; color: rgba(255,255,255,.6); margin-bottom: 28px; }
.cta-section .btn-cta {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 14px 40px; background: linear-gradient(135deg,#C85A20,#DA7530);
  color: #fff; font-size: 16px; font-weight: 600; text-decoration: none;
  border-radius: 10px; box-shadow: 0 6px 20px rgba(200,90,32,.3);
  transition: all .3s;
}
.cta-section .btn-cta:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(200,90,32,.4); }

footer {
  padding: 30px 0; background: #1a2744; text-align: center;
}
footer p { font-size: 12px; color: rgba(255,255,255,.3); letter-spacing: 1px; }

@media(max-width:1024px) {
  .burst-card { width: 220px; padding: 22px 18px; }
  .stats-grid { grid-template-columns: repeat(2,1fr); gap: 30px; }
}
@media(max-width:600px) {
  .pain-cards { padding: 28% 0 4% 6%; width: 90%; }
  .pain-card { padding: 14px 16px; }
  .pain-card.pc-2 { margin-left: 10px; }
  .pain-card.pc-3 { margin-left: 20px; }
  .pain-card .pc-num { font-size: 22px; min-width: 24px; }
  .pain-card .pc-body h3 { font-size: 14px; }
  .pain-card .pc-body p { font-size: 11px; }
  .stats-grid { grid-template-columns: repeat(2,1fr); gap: 24px; }
  .stat-item .stat-num { font-size: 32px; }
  .burst-card { width: 180px; padding: 16px 14px; }
  .burst-card h3 { font-size: 14px; }
  .burst-card p { font-size: 11px; }
}
</style>