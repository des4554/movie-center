import { createRouter, createWebHistory } from 'vue-router'
import BasicLayout from '@/layouts/BasicLayout.vue'
import LogView from '@/views/LogView.vue'
import RegisterView from '@/views/RegisterView.vue'
import TestView from '@/views/TestView.vue'
import MovieDetail from '@/views/MovieDetail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: BasicLayout,
    },
    {
      path: '/login',
      name: 'login',
      component: LogView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/test',
      name: 'test',
      component: TestView
    },
    {
      path: '/movie/:id',
      name: 'MovieDetail',
      component: MovieDetail,
    },
  ],
})

export default router
