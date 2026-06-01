<template>
  <div class="page-banner" :class="[`banner-${variant}`, { 'banner-fullwidth': fullwidth }]">
    <!-- 发光装饰：同首页风格 -->
    <div class="banner-glow glow-top-right"></div>
    <div class="banner-glow glow-bottom-left"></div>
    <div class="banner-bg-pattern"></div>
    <div class="banner-content">
      <div class="bc-left">
        <div class="banner-icon-wrap">
          <i class="fas" :class="icon"></i>
        </div>
        <div class="banner-text">
          <h2 class="banner-title">{{ title }}</h2>
          <p class="banner-desc">{{ description }}</p>
        </div>
      </div>
      <div class="bc-right" v-if="$slots.actions">
        <slot name="actions"></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  description: { type: String, default: '' },
  icon: { type: String, default: 'fa-circle' },
  variant: { type: String, default: 'primary' },
  fullwidth: { type: Boolean, default: false },
})
</script>

<style scoped>
.page-banner {
  position: relative;
  border-radius: 14px;
  padding: 22px 28px;
  margin-bottom: 22px;
  overflow: hidden;
  color: #fff;
}
/* ── 全宽模式：与首页欢迎横幅完全一致 ── */
.page-banner.banner-fullwidth {
  width: 100vw;
  margin-left: calc(-50vw + 50%);
  margin-top: -28px;
  border-radius: 0;
  border-bottom: 1px solid rgba(255,255,255,.06);
  padding: 28px 0;
  margin-bottom: 24px;
}
.page-banner.banner-fullwidth .banner-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
}
@media (max-width: 900px) {
  .page-banner.banner-fullwidth .banner-content { padding: 0 20px; }
}
@media (max-width: 640px) {
  .page-banner.banner-fullwidth .banner-content { padding: 0 14px; }
}
/* ── 发光装饰（同首页 Dashboard welcome-banner 风格） ── */
.banner-glow {
  position: absolute;
  border-radius: 50%;
  pointer-events: none;
}
.glow-top-right {
  top: -40%;
  right: -5%;
  width: 450px;
  height: 450px;
  background: radial-gradient(circle, rgba(61,90,128,.12) 0%, transparent 70%);
}
.glow-bottom-left {
  bottom: -30%;
  left: -5%;
  width: 350px;
  height: 350px;
  background: radial-gradient(circle, rgba(200,90,32,.06) 0%, transparent 70%);
}
.banner-bg-pattern {
  position: absolute;
  inset: 0;
  opacity: 0.08;
  background-image:
    radial-gradient(circle at 20% 50%, rgba(255,255,255,0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255,255,255,0.2) 0%, transparent 40%);
  pointer-events: none;
}
/* ── 内容布局：与首页 wb-inner/wb-left/wb-right 一致 ── */
.banner-content {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 1;
}
.bc-left {
  display: flex;
  align-items: center;
  gap: 16px;
}
.banner-icon-wrap {
  width: 46px; height: 46px;
  border-radius: 50%;
  background: rgba(255,255,255,0.12);
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255,255,255,.08);
}
.banner-text { }
.banner-title { font-size: 18px; font-weight: 700; margin: 0; }
.banner-desc { font-size: 13px; margin: 2px 0 0; opacity: 0.65; }
.bc-right { display: flex; gap: 10px; flex-shrink: 0; }

/* ── 变体：primary 改用首页同款深色渐变 ── */
.banner-primary  { background: var(--primary-gradient); }
.banner-accent   { background: linear-gradient(135deg, #C85A20 0%, #DA7530 100%); }
.banner-secondary { background: linear-gradient(135deg, #8EA0B8 0%, #A0B4CC 100%); }
.banner-coffee   { background: linear-gradient(135deg, #BFA895 0%, #CDB8A5 100%); }
.banner-mixed    { background: linear-gradient(135deg, #3D5A80 0%, #8EA0B8 50%, #BFA895 100%); }

@media (max-width: 600px) {
  .page-banner { padding: 16px 18px; }
  .banner-icon-wrap { width: 40px; height: 40px; font-size: 18px; }
  .banner-title { font-size: 15px; }
}
</style>