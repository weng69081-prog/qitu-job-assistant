<template>
  <div class="fm-page">
    <div class="fm-container">
      <button class="back-btn" @click="goBack">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg>
        返回
      </button>

      <h1 class="fm-title">我的收藏</h1>

      <!-- ═══ 分类标签 ═══ -->
      <div class="tab-row">
        <button v-for="t in tabs" :key="t.key" class="tab" :class="{ on: tab === t.key }" @click="tab = t.key">
          {{ t.label }} <span class="tc">({{ t.count }})</span>
        </button>
      </div>

      <!-- 职业 -->
      <div v-if="tab === 'career'">
        <div v-if="careerList.length" class="grid-2">
          <div v-for="c in careerList" :key="c.career" class="gc" @click="go('/career/'+c.career)">
            <div class="gc-n">{{ c.career }}</div>
            <div class="gc-s" v-if="c.salary">{{ c.salary }}</div>
          </div>
        </div>
        <div v-else class="empty">还没有收藏职业方向</div>
      </div>

      <!-- 视频 -->
      <div v-if="tab === 'video'">
        <div v-if="videoList.length" class="list">
          <div v-for="v in videoList" :key="v.bvid" class="lr" @click="openVideo(v)">
            <div class="lr-t">{{ v.title || '视频' }}</div>
            <div class="lr-m" v-if="v.author">{{ v.author }}</div>
          </div>
        </div>
        <div v-else class="empty">还没有收藏视频</div>
      </div>

      <!-- 面试题 -->
      <div v-if="tab === 'interview'">
        <div v-if="iqList.length" class="list">
          <div v-for="(q, i) in iqList" :key="i" class="lr">
            <div class="lr-t">{{ q.question || q.title }}</div>
            <div class="lr-m" v-if="q.career">{{ q.career }}</div>
          </div>
        </div>
        <div v-else class="empty">还没有收藏面试题</div>
      </div>

      <!-- 笔试 -->
      <div v-if="tab === 'exam'">
        <div v-if="eqList.length" class="list">
          <div v-for="(q, i) in eqList" :key="q.id || i" class="lr" @click="toggle(q.id || i)">
            <div class="lr-t">{{ q.question }}</div>
            <div class="lr-m">
              <span class="tag tc" v-if="q.career">{{ q.career }}</span>
              <span class="tag tw" v-if="q.wrong_count">错{{ q.wrong_count }}次</span>
            </div>
            <div v-if="expanded === (q.id || i)" class="detail">
              <div class="dr" v-if="q.user_answer && q.correct_answer" :class="q.user_answer===q.correct_answer?'ok':'no'">
                {{ q.user_answer===q.correct_answer ? '✓ 正确' : '✗ 错误' }}
              </div>
              <div v-if="q.options">
                <div v-for="o in q.options" :key="o.key" class="opt" :class="{ oc: o.key===q.correct_answer, ou: o.key===q.user_answer && o.key!==q.correct_answer }">
                  {{ o.key }}. {{ o.value }}
                </div>
              </div>
              <div v-if="q.analysis" class="an">{{ q.analysis }}</div>
            </div>
          </div>
        </div>
        <div v-else class="empty">还没有收藏笔试题目</div>
      </div>

      <div class="fm-footer">启途 · 向上生长，自有答案</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCareerStore } from '../stores/career'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const store = useCareerStore()
const tab = ref(route.query.tab || 'career')

const iqList = ref([])
const eqList = ref([])
const expanded = ref(null)

const careerList = computed(() => store.validBookmarks || [])
const videoList = computed(() => store.videoBookmarks || [])

const tabs = computed(() => [
  { key: 'career', label: '职业', count: careerList.value.length },
  { key: 'video', label: '视频', count: videoList.value.length },
  { key: 'interview', label: '面试题', count: iqList.value.length },
  { key: 'exam', label: '笔试', count: eqList.value.length },
])

async function loadIQ() {
  try { const { data } = await axios.get('/api/interview/saved-questions'); iqList.value = data.items || [] } catch {}
}
async function loadEQ() {
  try { const { data } = await axios.get('/api/exam/wrong-questions', { params: { page: 1, page_size: 50 } }); eqList.value = data.wrong_questions || [] } catch {}
}

function toggle(id) { expanded.value = expanded.value === id ? null : id }
function goBack() { window.history.length > 1 ? router.back() : router.push('/dashboard') }
function go(p) { router.push(p) }
function openVideo(v) { if(v.bvid) window.open('https://www.bilibili.com/video/'+v.bvid, '_blank') }

onMounted(() => { loadIQ(); loadEQ() })
</script>

<style scoped>
.fm-page { width: 100%; display: flex; justify-content: center; padding: 28px 0; }
.fm-container { width: min(740px, calc(100vw - 60px)); padding: 36px 28px 24px; background: #fff; border-radius: 22px; box-shadow: 0 16px 36px rgba(37,99,235,.06); position: relative; }
.back-btn {
  position: absolute; left: 0; top: 4px;
  display: inline-flex; align-items: center; gap: 4px; padding: 6px 14px;
  border: 2px solid #2563EB; border-radius: 999px; background: #fff;
  color: #2563EB; font-size: 13px; font-weight: 700; cursor: pointer;
}
.back-btn:hover { background: #EFF6FF; }
.fm-title { font-size: 22px; font-weight: 900; color: #1e293b; margin-bottom: 16px; }
.tab-row { display: flex; gap: 6px; margin-bottom: 18px; flex-wrap: wrap; }
.tab {
  padding: 5px 14px; border-radius: 999px; border: 1.5px solid #DBEAFE;
  background: #fff; color: #475569; font-size: 13px; font-weight: 600;
  cursor: pointer; transition: all .2s;
}
.tab.on { background: #2563EB; color: #fff; border-color: #2563EB; }
.tc { font-weight: 400; opacity: .65; }
.empty { text-align: center; padding: 40px 0; color: #94a3b8; font-size: 14px; }

.grid-2 { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px,1fr)); gap: 10px; }
.gc { padding: 14px; border: 1px solid #E2E8F0; border-radius: 14px; cursor: pointer; }
.gc:hover { box-shadow: 0 4px 12px rgba(37,99,235,.08); }
.gc-n { font-size: 14px; font-weight: 700; color: #1e293b; margin-bottom: 3px; }
.gc-s { font-size: 12px; color: #2563EB; }

.list { display: flex; flex-direction: column; gap: 6px; }
.lr { padding: 10px 12px; border: 1px solid #E2E8F0; border-radius: 12px; cursor: pointer; }
.lr:hover { box-shadow: 0 3px 10px rgba(37,99,235,.05); }
.lr-t { font-size: 13px; font-weight: 600; color: #1e293b; line-height: 1.5; }
.lr-m { display: flex; gap: 6px; margin-top: 3px; flex-wrap: wrap; }
.tag { font-size: 11px; padding: 1px 7px; border-radius: 99px; font-weight: 600; }
.tag.tc { background: #EFF6FF; color: #2563EB; }
.tag.tw { background: #FEF2F2; color: #DC2626; }

.detail { margin-top: 8px; padding: 10px; background: #F8FAFF; border-radius: 10px; border: 1px solid #DBEAFE; }
.dr { padding: 5px 8px; border-radius: 6px; font-weight: 700; font-size: 12px; margin-bottom: 6px; }
.dr.ok { background: #F0FDF4; color: #16A34A; }
.dr.no { background: #FEF2F2; color: #DC2626; }
.opt { padding: 2px 5px; margin-bottom: 2px; border-radius: 4px; font-size: 12px; color: #475569; }
.opt.oc { background: #F0FDF4; }
.opt.ou { background: #FEF2F2; }
.an { margin-top: 6px; padding-top: 6px; border-top: 1px solid #DBEAFE; font-size: 12px; color: #64748b; line-height: 1.6; }

.fm-footer { text-align: center; margin-top: 24px; padding-top: 12px; border-top: 1px solid #E2E8F0; font-size: 11px; color: #94a3b8; }
</style>