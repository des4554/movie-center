import { createRouter, createWebHistory } from 'vue-router'
import BasicLayout from '@/layouts/BasicLayout.vue'
import LogView from '@/views/LogView.vue'
import RegisterView from '@/views/RegisterView.vue'
import TestView from '@/views/TestView.vue'
import MovieDetail from '@/views/MovieDetail.vue'
import { useAuthStore } from '@/stores/authStore.ts'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: BasicLayout,
      meta: {
        requiresAuth: true
      }
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
      meta: {
        requiresAuth: true
      }
    },
  ],
})
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const user = authStore.user;
  if (to.meta.requiresAuth && !user) {
    next('/login')
  } else {
    next()
  }
})
export default router
