import { createRouter, createWebHistory } from 'vue-router'
import CareerExplore from '../views/CareerExplore.vue'
import CareerDetail from '../views/CareerDetail.vue'
import CareerPath from '../views/CareerPath.vue'
import InterviewSim from '../views/InterviewSim.vue'
import InterviewSession from '../views/InterviewSession.vue'
import InterviewSessionDetail from '../views/InterviewSessionDetail.vue'
import InterviewHistory from '../views/InterviewHistory.vue'
import InterviewWrongList from '../views/InterviewWrongList.vue'
import InterviewSavedList from '../views/InterviewSavedList.vue'
import ExamHistory from '../views/ExamHistory.vue'
import ExamPractice from '../views/ExamPractice.vue'
import ExamSession from '../views/ExamSession.vue'
import ExamWrong from '../views/ExamWrong.vue'
import ResumeOptimize from '../views/ResumeOptimize.vue'
import JobMatch from '../views/JobMatch.vue'
import DeliveryAssistant from '../views/DeliveryAssistant.vue'
import FavoritesManage from '../views/FavoritesManage.vue'
import Auth from '../views/Auth.vue'
import Settings from '../views/Settings.vue'
import ProfileSetup from '../views/ProfileSetup.vue'
import LandingPage from '../views/LandingPage.vue'
import Dashboard from '../views/Dashboard.vue'

const routes = [
  { path: '/', component: LandingPage, meta: { public: true } },
  { path: '/landing', component: LandingPage, meta: { title: '启途首页' } },
  { path: '/login', component: Auth, meta: { guest: true } },
  { path: '/dashboard', component: Dashboard, meta: { title: '首页' } },
  { path: '/register', component: Auth, meta: { guest: true } },
  { path: '/profile-setup', component: ProfileSetup, meta: { standalone: true } },
  { path: '/career', component: CareerExplore },
  { path: '/career/path/:careerId?', component: CareerPath, props: true },
  { path: '/career/:careerId', component: CareerDetail, props: true },
  { path: '/interview', component: InterviewSim },
  { path: '/interview/session', component: InterviewSession, meta: { standalone: true } },
  { path: '/interview/history', component: InterviewHistory, meta: { standalone: true } },
  { path: '/interview/history/:id', component: InterviewSessionDetail, props: true },
  { path: '/interview/wrong-questions', component: InterviewWrongList, meta: { standalone: true } },
  { path: '/interview/saved-questions', component: InterviewSavedList, meta: { standalone: true } },
  { path: '/exam/session', component: ExamSession, meta: { standalone: true } },
  { path: '/exam/wrong', component: ExamWrong, meta: { standalone: true } },
  { path: '/exam/history', component: ExamHistory, meta: { standalone: true } },
  { path: '/exam/history/:recordId', component: ExamHistory, meta: { standalone: true } },
  { path: '/exam-practice', component: ExamPractice },
  { path: '/resume', component: ResumeOptimize },
  { path: '/jobmatch', component: JobMatch },
  { path: '/delivery-assistant', component: DeliveryAssistant },
  { path: '/favorites', component: FavoritesManage, meta: { standalone: true } },
  { path: '/settings', component: Settings },
]

// 404 兜底
import NotFound from '../views/NotFound.vue'
routes.push({ path: '/:pathMatch(.*)*', component: NotFound })

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  // 公开页（如首页介绍页）：已登录则跳仪表盘
  if (to.meta.public) {
    if (token) {
      return next('/dashboard')
    }
    return next()
  }

  // 登录/注册页 — 已登录则跳走
  if (to.meta.guest) {
    if (token) {
      return next('/dashboard')
    }
    return next()
  }

  // 未登录 → 去首页介绍页
  if (!token) return next('/')

  next()
})

export default router