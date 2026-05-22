import { createRouter, createWebHistory } from 'vue-router'
import CareerExplore from '../views/CareerExplore.vue'
import InterviewSim from '../views/InterviewSim.vue'
import ResumeOptimize from '../views/ResumeOptimize.vue'
import JobMatch from '../views/JobMatch.vue'

const routes = [
  { path: '/', redirect: '/career' },
  { path: '/career', component: CareerExplore },
  { path: '/interview', component: InterviewSim },
  { path: '/resume', component: ResumeOptimize },
  { path: '/jobmatch', component: JobMatch },
]

export default createRouter({
  history: createWebHistory(),
  routes
})