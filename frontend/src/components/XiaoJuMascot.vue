<template>
  <div class="xj" :style="{ width: s, height: s }">
    <div class="xj-inner">
      <Cat :size="32" color="#3D5A80" />
      <!-- 小橘签名 -->
      <span class="xj-label">小橘</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ size: { type: [Number, String], default: 120 } })
const s = computed(() => typeof props.size === 'number' ? `${props.size}px` : props.size)
</script>

<style scoped>
.xj {
  display: flex;
  align-items: center;
  justify-content: center;
}
.xj-inner {
  width: 80%;
  height: 80%;
  border-radius: 50%;
  background: rgba(61, 90, 128, 0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px solid rgba(61, 90, 128, 0.2);
  position: relative;
  transition: all 0.2s;
}
.xj-inner:hover {
  background: rgba(61, 90, 128, 0.14);
  border-color: rgba(61, 90, 128, 0.35);
}
.xj-inner :deep(Cat) {
  font-size: 1.6em;
  color: #3D5A80;
  line-height: 1;
}
.xj-label {
  position: absolute;
  bottom: -4px;
  font-size: 0.5em;
  color: #8EA0B8;
  font-weight: 500;
  letter-spacing: 1px;
}
</style>