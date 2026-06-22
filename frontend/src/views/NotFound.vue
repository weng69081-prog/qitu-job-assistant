<template>
  <div class="not-found-page">
    <div class="nf-card">
      <div class="nf-icon">
        <Compass :size="16" class="icon-blue" />
      </div>
      <h1 class="nf-code">404</h1>
      <p class="nf-text">这个页面好像迷路了……</p>
      <p class="nf-hint">可能是地址输错了，或者页面已转移</p>
      <router-link to="/dashboard" class="btn-primary" style="display:inline-flex;align-items:center;gap:8px;padding:10px 28px;margin-top:20px;border-radius:8px;text-decoration:none">
        <Home :size="16" class="icon-blue" /> 回首页
      </router-link>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-body, #f0f2f6);
  padding: 20px;
}
.nf-card {
  text-align: center;
  background: white;
  border-radius: 16px;
  padding: 60px 48px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  max-width: 420px;
}
.nf-icon {
  font-size: 3rem;
  color: var(--primary, #3D5A80);
  margin-bottom: 12px;
  opacity: 0.6;
}
.nf-code {
  font-size: 4rem;
  font-weight: 800;
  color: var(--primary, #3D5A80);
  margin: 0 0 8px;
  line-height: 1;
}
.nf-text {
  font-size: 1.1rem;
  color: var(--text-primary, #2c3e50);
  margin: 0 0 4px;
}
.nf-hint {
  font-size: 0.85rem;
  color: var(--text-muted, #8EA0B8);
  margin: 0;
}
</style>