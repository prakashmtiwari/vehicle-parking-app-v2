import { createRouter, createWebHistory } from "https://unpkg.com/vue-router@4/dist/vue-router.esm-browser.js";

import Landing from "./views/Landing.vue";
import Login from "./views/Login.vue";
import Register from "./views/Register.vue";
import Dashboard from "./views/Dashboard.vue";

const routes = [
  { path: "/", component: Landing },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/dashboard", component: Dashboard, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Navigation guard to protect dashboard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("authToken");
  if (to.meta.requiresAuth && !token) return next("/login");
  next();
});

export default router;
