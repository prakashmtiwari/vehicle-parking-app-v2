import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Views
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import UserDashboard from '@/views/user/UserDashboard.vue'
import AdminDashboard from '@/views/admin/AdminDashboard.vue'
import ParkingLotManagement from '@/views/admin/ParkingLotManagement.vue'
import ParkingLotForm from '@/views/admin/ParkingLotForm.vue'
import UserManagement from '@/views/admin/UserManagement.vue'
import updateUser from '@/views/admin/updateUser.vue' 
import parkingLotList from '@/views/user/ParkingLotsList.vue'
import UserSummary from '@/views/user/UserSummary.vue'
import ReportView from '@/views/admin/AdminSummary.vue' 

const routes = [  
  { path: '/', name: 'Home', component: HomeView },
  { path: '/login', name: 'Login', component: LoginView },
  { path: '/register', name: 'Register', component: RegisterView },

  // admin routes
  { path: '/admin', name: 'AdminDashboard', component: AdminDashboard, meta: { requiresAuth: true, role: 'admin' } },
  //parking lot management
  { path: '/parking-lots', name: 'ParkingLotManagement', component: ParkingLotManagement, meta: { requiresAuth: true, roles: ['admin', 'user']  } },
  { path: "/parking-lots/new", name: "ParkingLotAdd", component: ParkingLotForm, meta: { requiresAuth: true, role: 'admin' } },
  { path: "/parking-lots/:id/edit", name: "ParkingLotEdit", component: ParkingLotForm, meta: { requiresAuth: true, role: 'admin' }, props: true },
  // reports
  { path: "/admin-summary", name: "AdminSummary", component: ReportView, meta: { requiresAuth: true, role: 'admin' } },

  // user management by admin
  { path: "/users", name: "UserManagement", component: UserManagement, meta: { requiresAuth: true, role: 'admin' } },
  { path: "/users/:id/edit", name: "UserEdit", component: updateUser, meta: { requiresAuth: true, role: 'admin' }, props: true },

  // user dashboard and other user routes
  { path: '/user/:id', name: 'UserDashboard', component: UserDashboard, meta: { requiresAuth: true, role: 'user' } },
  { path: '/parking-lot-list', name: 'parkingLotList', component: parkingLotList, meta: { requiresAuth: true, role: 'user' } },
  { path: '/user-summary', name: 'UserSummary', component: UserSummary, meta: { requiresAuth: true, role: 'user' } },
] 


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})


// Navigation Guard
router.beforeEach((to, from, next) => {
  console.log("Navigating from:", from.fullPath, "to:", to.fullPath, "with meta:", to.meta)

  const auth = useAuthStore()

  const userRoles = auth.user?.roles || []
  console.log("User roles from store:", userRoles)


  if (to.meta.requiresAuth) {
    if (!auth.isAuthenticated) {
      console.log("Not authenticated, redirecting to login")

      return next('/login')
    }

    // role-based access

    if (to.meta.roles){
      const allowed = to.meta.roles.some(role => userRoles.includes(role))
      console.log("User roles:", userRoles, "Allowed roles:", to.meta.roles, "Access allowed:", allowed)
      if (!allowed) {
        // Redirect depending on user role
        return next('/login') 
      }
    }

    if (to.meta.role === 'admin' && !auth.isAdmin) {
      return next('/login')  // redirect non-admin trying to access admin page
    }

    if (to.meta.role === 'user' && auth.isAdmin) {
      return next('/login') // redirect admin trying to access user page  
    }
  }

  next()
})

export default router
