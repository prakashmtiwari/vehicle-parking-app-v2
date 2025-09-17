import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Views
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import UserDashboard from '@/views/UserDashboard.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },

  // protected routes
  { path: '/user', name: 'UserDashboard', component: UserDashboard, meta: { requiresAuth: true, role: 'user' } },
  { path: '/admin', name: 'AdminDashboard', component: AdminDashboard, meta: { requiresAuth: true, role: 'admin' } },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth) {
    if (!auth.isAuthenticated) {
      return next('/login')
    }

    // role-based access
    if (to.meta.role === 'admin' && !auth.isAdmin) {
      return next('/user')
    }

    if (to.meta.role === 'user' && auth.isAdmin) {
      return next('/admin')
    }
  }

  next()
})

export default router
