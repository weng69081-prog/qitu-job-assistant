<template>
  <section class="page-banner" :class="[`banner-${variant}`, { 'banner-fullwidth': fullwidth, 'has-actions': $slots.actions }]">
    <div class="banner-content">
      <div class="paper-title-card">
        <div class="banner-icon-wrap" aria-hidden="true">
          <svg class="icon-symbol" viewBox="0 0 36 36">
            <template v-if="iconKind === 'career'">
              <path class="fill" d="M7 8.5h9.5c2.2 0 4 1.8 4 4v15H11c-2.2 0-4-1.8-4-4z"/>
              <path class="fill" d="M20.5 12.5c0-2.2 1.8-4 4-4H29v15c0 2.2-1.8 4-4 4h-4.5z"/>
              <path d="M20.5 12v16M11 15h5M11 20h5M24 15h3M24 20h3"/>
              <path d="M9 6.5h8c1.5 0 2.8.8 3.5 2 .7-1.2 2-2 3.5-2h3" stroke="#93C5FD"/>
            </template>
            <template v-else-if="iconKind === 'interview'">
              <path class="fill" d="M8 13c0-3 2.4-5.4 5.4-5.4h9.2C25.6 7.6 28 10 28 13v5.5c0 3-2.4 5.4-5.4 5.4h-3.2L14 28.5v-4.6h-.6C10.4 23.9 8 21.5 8 18.5z"/>
              <path d="M13 15h10M13 19h6"/>
              <circle cx="25" cy="25" r="4.8" stroke="#0EA5E9"/>
              <path d="M23 25l1.4 1.3 3-3" stroke="#0EA5E9"/>
            </template>
            <template v-else-if="iconKind === 'exam'">
              <path class="fill" d="M10 8h15l4 4v16H10z"/>
              <path d="M25 8v5h5M14 16h10M14 21h8M14 26h5"/>
              <path d="M8 12H6v18h18v-2" stroke="#93C5FD"/>
            </template>
            <template v-else-if="iconKind === 'resume'">
              <rect class="fill" x="8" y="7" width="20" height="22" rx="5"/>
              <path d="M12 14h12M12 19h8M12 24h5"/>
              <path d="M25 23l4 4M29 23l-4 4" stroke="#0EA5E9"/>
              <path d="M14 5h8" stroke="#93C5FD"/>
            </template>
            <template v-else-if="iconKind === 'delivery'">
              <path class="fill" d="M8 10h20v17H8z"/>
              <path d="M12 15h12M12 20h8"/>
              <path d="M8 10l10 8 10-8" stroke="#93C5FD"/>
              <path d="M26 25l4 4M30 25l-4 4" stroke="#0EA5E9"/>
            </template>
            <template v-else>
              <path class="fill" d="M7 8.5h9.5c2.2 0 4 1.8 4 4v15H11c-2.2 0-4-1.8-4-4z"/>
              <path class="fill" d="M20.5 12.5c0-2.2 1.8-4 4-4H29v15c0 2.2-1.8 4-4 4h-4.5z"/>
              <path d="M20.5 12v16M11 15h5M11 20h5M24 15h3M24 20h3"/>
            </template>
          </svg>
        </div>
        <div class="banner-text">
          <h2 class="banner-title">{{ title }}</h2>
          <p class="banner-desc">{{ description }}</p>
        </div>
      </div>

      <div class="banner-right" :class="{ 'with-cat': Boolean(catSrc), 'has-cat-right': catRight }">
        <template v-if="$slots.actions">
          <div class="bc-right"><slot name="actions"></slot></div>
        </template>
        <span class="qitu-watermark">QITU</span>
        <div v-if="catSrc" class="cat-spot" aria-hidden="true"></div>
        <img v-if="catSrc" :src="catSrc" :class="['banner-cat-sticker', catClass]" :alt="catAlt || `${title}小猫贴纸`">
        <div class="path-text" aria-label="页面路径">{{ displayPath }}</div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' },
  icon: { type: String, default: 'Circle' },
  variant: { type: String, default: 'primary' },
  fullwidth: { type: Boolean, default: false },
  catSrc: { type: String, default: '' },
  catAlt: { type: String, default: '' },
  pathItems: { type: Array, default: () => [] },
})

const iconKind = computed(() => {
  const key = String(props.icon || '').toLowerCase()
  if (key.includes('mic')) return 'interview'
  if (key.includes('pen')) return 'exam'
  if (key.includes('file')) return 'resume'
  if (key.includes('send')) return 'delivery'
  if (key.includes('compass')) return 'career'
  return 'career'
})

const displayPath = computed(() => {
  if (props.pathItems.length) return props.pathItems.join('、')
  return '启程、练习、成长'
})

const catClass = computed(() => iconKind.value)
const catRight = computed(() => ['interview', 'resume'].includes(iconKind.value))
</script>

<style scoped>
.page-banner {
  position: relative;
  border-radius: 18px;
  padding: 22px 28px;
  margin-bottom: 22px;
  overflow: hidden;
  color: var(--text-heading);
  background: #FFFFFF;
  border: 1px solid #DCEBFF;
  box-shadow: 0 18px 34px rgba(37, 99, 235, 0.055);
}

.page-banner::before {
  content: '';
  position: absolute;
  inset: 0;
  background: #FFFFFF;
  pointer-events: none;
}

.page-banner::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, #BFDBFE 18%, #93C5FD 50%, #BFDBFE 82%, transparent);
  opacity: .9;
}

/* ── 全宽模式：纸张折角顶栏，铺满内容区，无残留虚线/白条 ── */
.page-banner.banner-fullwidth {
  width: calc(100% + var(--sidebar-width) + var(--main-pad-x, 28px) + var(--main-pad-x, 28px));
  margin-left: calc(0px - var(--sidebar-width) - var(--main-pad-x, 28px));
  margin-top: 0;
  border-radius: 0;
  border: 0;
  box-shadow: none;
  padding: 22px 0;
  margin-bottom: 24px;
  background: #FFFFFF;
  overflow: visible;
}

.page-banner.banner-fullwidth::after {
  content: '';
  display: block;
  position: absolute;
  left: 0;
  right: 0;
  bottom: -30px;
  height: 60px;
  background: linear-gradient(
    to bottom,
    rgba(255, 255, 255, 0) 0%,
    rgba(191, 219, 254, 0.10) 26%,
    rgba(147, 197, 253, 0.22) 50%,
    rgba(191, 219, 254, 0.10) 74%,
    rgba(255, 255, 255, 0) 100%
  );
  pointer-events: none;
}

.page-banner.banner-fullwidth .banner-content {
  max-width: none;
  margin: 0;
  padding: 0 32px;
}

.banner-content {
  position: relative;
  display: grid;
  grid-template-columns: minmax(500px, 42%) 1fr;
  align-items: center;
  gap: 0;
  z-index: 1;
  min-height: 122px;
}

.paper-title-card {
  position: relative;
  min-height: 122px;
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 24px 34px;
  border-radius: 22px 22px 8px 22px;
  background: #EFF6FF;
  border: 1px solid #CFE4FF;
  box-shadow: 0 12px 24px rgba(37,99,235,.06);
  overflow: visible;
}

.paper-title-card::after {
  content: '';
  position: absolute;
  right: -18px;
  bottom: -1px;
  width: 34px;
  height: 34px;
  background: linear-gradient(135deg,#DBEAFE 0,#fff 58%);
  border: 1px solid #CFE4FF;
  clip-path: polygon(0 0,100% 100%,0 100%);
}

.banner-icon-wrap {
  position: relative;
  width: 56px;
  height: 56px;
  border-radius: 18px;
  background: #FFFFFF;
  border: 1.5px solid #BFDBFE;
  display: grid;
  place-items: center;
  flex: none;
  color: var(--primary);
  box-shadow: 0 10px 22px rgba(37,99,235,.08);
}
.icon-symbol {
  width: 35px;
  height: 35px;
  fill: none;
  stroke: #2563EB;
  stroke-width: 1.75;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.icon-symbol .fill {
  fill: #EFF6FF;
}

.banner-text { min-width: 0; position: relative; z-index: 1; }
.banner-title {
  font-size: 28px;
  font-weight: 900;
  margin: 0;
  color: #2563EB;
  letter-spacing: .06em;
  line-height: 1.05;
}
.banner-desc {
  font-size: 15px;
  margin: 9px 0 0;
  color: #3B6EA8;
  opacity: 1;
  font-weight: 900;
  line-height: 1.45;
}

.banner-right {
  position: relative;
  min-height: 122px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 78px 0 48px;
  isolation: isolate;
  min-width: 0;
}
.cat-spot {
  display: none;
}
.banner-cat-sticker {
  position: relative;
  z-index: 3;
  width: 82px;
  max-height: 104px;
  object-fit: contain;
  flex: none;
  margin-right: 22px;
  pointer-events: none;
  filter: drop-shadow(0 10px 15px rgba(37,99,235,.12));
}
.banner-cat-sticker.career { width: 84px; transform: translateX(-8px); }
.banner-cat-sticker.interview { width: 82px; }
.banner-cat-sticker.exam { width: 86px; transform: translateX(-10px); }
.banner-cat-sticker.resume { width: 80px; }
.banner-cat-sticker.delivery { width: 84px; transform: translateX(-8px); }
.banner-right.has-cat-right {
  justify-content: center;
  padding-right: 96px;
}
.banner-right.has-cat-right .banner-cat-sticker {
  position: absolute;
  right: 92px;
  bottom: 10px;
  width: 88px;
  opacity: .98;
  margin-right: 0;
}
.banner-right.has-cat-right .banner-cat-sticker.resume {
  width: 82px;
  right: 96px;
  bottom: 12px;
}
.banner-right.has-cat-right .path-text {
  margin-right: 120px;
}
.path-text {
  position: relative;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 360px;
  min-height: 54px;
  margin-left: 0;
  padding: 0 24px;
  color: #2563EB;
  font-size: 23px;
  font-weight: 900;
  letter-spacing: .055em;
  white-space: nowrap;
}
.path-text::before,
.path-text::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 38px;
  height: 2px;
  background-image: linear-gradient(to right, #93C5FD 55%, transparent 0);
  background-size: 9px 2px;
  background-repeat: repeat-x;
  opacity: .68;
}
.path-text::before { right: calc(100% + 10px); }
.path-text::after { left: calc(100% + 10px); }
.qitu-watermark {
  position: absolute;
  right: 16px;
  top: 10px;
  font-size: 30px;
  font-weight: 900;
  letter-spacing: .1em;
  color: rgba(37,99,235,.075);
  line-height: 1;
  z-index: 0;
  pointer-events: none;
}
.bc-right {
  position: absolute;
  right: 210px;
  bottom: 2px;
  z-index: 4;
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}

.banner-accent,
.banner-secondary,
.banner-coffee,
.banner-mixed,
.banner-primary { background: #FFFFFF; }

@media (max-width: 1100px) {
  .banner-content { grid-template-columns: 1fr; gap: 14px; }
  .banner-right { justify-content: flex-start; min-height: 112px; padding: 10px 28px 22px; }
  .banner-right.has-cat-right { justify-content: flex-start; padding-right: 28px; }
  .banner-right.has-cat-right .banner-cat-sticker { position: relative; right: auto; bottom: auto; width: 76px; }
  .banner-right.has-cat-right .path-text { margin-right: 0; }
  .path-text { margin-right: 0; white-space: normal; }
  .path-text::before,
  .path-text::after { display: none; }
  .qitu-watermark,
  .cat-spot { display: none; }
  .bc-right { right: 28px; bottom: 8px; }
}

@media (max-width: 900px) {
  .page-banner.banner-fullwidth .banner-content { padding: 0 20px; }
  .paper-title-card { padding: 18px 22px; min-height: 104px; }
  .banner-title { font-size: 24px; }
  .banner-desc { font-size: 14px; }
}

@media (max-width: 640px) {
  .page-banner.banner-fullwidth .banner-content { padding: 0 14px; }
  .paper-title-card { gap: 12px; }
  .banner-icon-wrap { width: 48px; height: 48px; border-radius: 15px; }
  .icon-symbol { width: 30px; height: 30px; }
  .banner-title { font-size: 20px; }
  .banner-desc { font-size: 13px; }
  .banner-right { display: none; }
}
</style>
