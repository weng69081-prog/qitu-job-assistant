import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// 安全解析 localStorage 的 JSON，脏数据不崩
function safeParse(key, fallback) {
  try {
    const val = localStorage.getItem(key)
    if (val === null) return fallback
    const parsed = JSON.parse(val)
    // 类型检查：fallback 是数组则 parsed 必须是数组
    if (Array.isArray(fallback) && !Array.isArray(parsed)) return fallback
    if (typeof fallback === 'object' && !Array.isArray(fallback) && typeof parsed !== 'object') return fallback
    return parsed
  } catch {
    return fallback
  }
}

export const useCareerStore = defineStore('career', () => {
  const currentCareer = ref(null)
  const formData = ref({})
  const recommendations = ref([])

  // 收藏的职业列表，从 localStorage 加载
  const rawBookmarks = safeParse('career_bookmarks', [])
  // 自动清理 career 为空/无效的脏数据
  const cleanBookmarks = rawBookmarks.filter(b => b && b.career && b.career.trim())
  if (cleanBookmarks.length !== rawBookmarks.length) {
    localStorage.setItem('career_bookmarks', JSON.stringify(cleanBookmarks))
  }
  const bookmarks = ref(cleanBookmarks)
  
// 已生成成长路线的职业记录
  const generatedPaths = ref(safeParse('career_generated_paths', []))

  // ════════════════════════════════════
  // 📺 视频收藏（新增）
  // ════════════════════════════════════
  const videoBookmarks = ref(safeParse('career_video_bookmarks', []))

  // 📊 视频点击记录（用于优化推荐顺序）
  const videoClickCounts = ref(safeParse('career_video_click_counts', {}))
  
  function saveVideoBookmarks() {
    localStorage.setItem('career_video_bookmarks', JSON.stringify(videoBookmarks.value))
  }
  
  function saveVideoClickCounts() {
    localStorage.setItem('career_video_click_counts', JSON.stringify(videoClickCounts.value))
  }
  
  function addVideoBookmark(video) {
    if (!video || !video.bvid) return false
    if (!videoBookmarks.value.find(v => v.bvid === video.bvid)) {
      videoBookmarks.value.push({
        ...video,
        savedAt: new Date().toISOString(),
      })
      saveVideoBookmarks()
      return true
    }
    return false
  }
  
  function removeVideoBookmark(bvid) {
    videoBookmarks.value = videoBookmarks.value.filter(v => v.bvid !== bvid)
    saveVideoBookmarks()
  }
  
  function isVideoBookmarked(bvid) {
    return videoBookmarks.value.some(v => v.bvid === bvid)
  }
  
  // ════════════════════════════════════
  // 📊 视频点击记录
  // ════════════════════════════════════
  function recordVideoClick(careerName) {
    if (!careerName) return
    videoClickCounts.value[careerName] = (videoClickCounts.value[careerName] || 0) + 1
    saveVideoClickCounts()
  }
  
  function getMostClickedCareer() {
    const entries = Object.entries(videoClickCounts.value)
    if (entries.length === 0) return null
    entries.sort((a, b) => b[1] - a[1])
    return entries[0][0]
  }
  
  function getVideoClickCount(careerName) {
    return videoClickCounts.value[careerName] || 0
  }
  
  function clearVideoClickCounts() {
    videoClickCounts.value = {}
    saveVideoClickCounts()
  }
  
  // ════════════════════════════════════
  // 计算属性：按视频点击排序的收藏列表
  // ════════════════════════════════════
  const bookmarksSortedByClicks = computed(() => {
    const list = [...bookmarks.value]
    list.sort((a, b) => {
      const aClicks = getVideoClickCount(a.career)
      const bClicks = getVideoClickCount(b.career)
      return bClicks - aClicks
    })
    return list
  })
  
  function saveBookmarks() {
    localStorage.setItem('career_bookmarks', JSON.stringify(bookmarks.value))
  }
  
  function saveGeneratedPaths() {
    localStorage.setItem('career_generated_paths', JSON.stringify(generatedPaths.value))
  }
  
  function markPathGenerated(careerName) {
    if (!generatedPaths.value.includes(careerName)) {
      generatedPaths.value.push(careerName)
      saveGeneratedPaths()
    }
  }
  
  function hasGeneratedPath(careerName) {
    return generatedPaths.value.includes(careerName)
  }
  
  function removeGeneratedPath(careerName) {
    generatedPaths.value = generatedPaths.value.filter(n => n !== careerName)
    saveGeneratedPaths()
  }
  
  function addBookmark(career) {
    // 拒绝空 career 的无效条目
    if (!career || !career.career || !career.career.trim()) return false
    if (!bookmarks.value.find(b => b.career === career.career)) {
      bookmarks.value.push(career)
      saveBookmarks()
      return true
    }
    return false
  }
  
  function removeBookmark(careerName) {
    bookmarks.value = bookmarks.value.filter(b => b.career !== careerName)
    saveBookmarks()
  }
  
  function isBookmarked(careerName) {
    return bookmarks.value.some(b => b.career === careerName)
  }

  function setCurrentCareer(career) { currentCareer.value = career }
  function setFormData(data) { formData.value = data; localStorage.setItem('career_form_data', JSON.stringify(data)) }
  function loadFormCache() { try { const raw = localStorage.getItem('career_form_data'); if (raw) formData.value = JSON.parse(raw) } catch {} }
  function setRecommendations(data) { recommendations.value = data }
  function clearAll() {
    currentCareer.value = null; formData.value = {}; recommendations.value = []
    localStorage.removeItem('career_form_data')
  }

  // 安全兜底：返回过滤掉无效条目的书签列表（供模板直接使用）
  const validBookmarks = computed(() => bookmarks.value.filter(b => b && b.career && b.career.trim()))

  return {
    currentCareer, formData, recommendations, bookmarks, generatedPaths, validBookmarks,
    setCurrentCareer, setFormData, loadFormCache, setRecommendations, clearAll,
    addBookmark, removeBookmark, isBookmarked, saveBookmarks,
    markPathGenerated, hasGeneratedPath, removeGeneratedPath,
    // 视频收藏
    videoBookmarks, videoClickCounts,
    addVideoBookmark, removeVideoBookmark, isVideoBookmarked,
    // 视频点击记录
    recordVideoClick, getMostClickedCareer, getVideoClickCount, clearVideoClickCounts,
    // 排序
    bookmarksSortedByClicks,
  }
})