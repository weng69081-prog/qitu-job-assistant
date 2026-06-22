<template>
  <!-- 启途 Logo SVG -->
  <svg :width="width" :height="height" viewBox="0 0 120 32" xmlns="http://www.w3.org/2000/svg">
    <!-- 图标：重叠的书脊/阶梯意象 -->
    <rect x="2" y="10" width="7" height="18" rx="1.5" fill="#3D5A80"/>
    <rect x="10" y="6" width="7" height="22" rx="1.5" fill="#54759C"/>
    <rect x="18" y="2" width="7" height="26" rx="1.5" fill="#C85A20"/>
    <!-- 顶部光点 -->
    <circle cx="21.5" cy="4" r="2.5" fill="#F5F0E8" opacity="0.6"/>
    <!-- 问号元素（探索） -->
    <text x="3" y="27" font-size="9" fill="#F5F0E8" font-weight="bold" font-family="Arial" opacity="0.4">?</text>
    <!-- 文字部分 -->
    <text x="32" y="18" font-size="16" font-weight="700" fill="#3D5A80" font-family="'PingFang SC','Microsoft YaHei',sans-serif" letter-spacing="3">启途</text>
    <!-- 小点分隔 -->
    <circle cx="73" cy="14" r="1.5" fill="#8EA0B8"/>
    <!-- 英文副标题 -->
    <text x="80" y="18" font-size="10" fill="#8EA0B8" font-family="Arial,sans-serif" letter-spacing="2" font-weight="500">QITU</text>
    <!-- 底部装饰线 -->
    <line x1="80" y1="24" x2="110" y2="24" stroke="#BFA895" stroke-width="1" stroke-linecap="round" opacity="0.5"/>
  </svg>
</template>

<script setup>
defineProps({
  width: { type: [Number, String], default: 120 },
  height: { type: [Number, String], default: 32 }
})
</script>