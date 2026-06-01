import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// ═══ 全局错误捕获 ═══
window.addEventListener('error', (e) => {
  fetch('/api/debug-log', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      type: 'window.error',
      message: e.message,
      stack: e.error?.stack || '',
      filename: e.filename,
      lineno: e.lineno,
      colno: e.colno,
      time: new Date().toISOString(),
    }),
  }).catch(() => {})
})
window.addEventListener('unhandledrejection', (e) => {
  fetch('/api/debug-log', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      type: 'unhandledrejection',
      message: e.reason?.message || String(e.reason),
      stack: e.reason?.stack || '',
      time: new Date().toISOString(),
    }),
  }).catch(() => {})
})

const app = createApp(App)
app.config.errorHandler = (err, vm, info) => {
  fetch('/api/debug-log', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      type: 'vue.error',
      message: err.message,
      stack: err.stack || '',
      info,
      time: new Date().toISOString(),
    }),
  }).catch(() => {})
  console.error('[Vue Error]', err, info)
}
app.use(ElementPlus)
app.use(createPinia())
app.use(router)
app.mount('#app')