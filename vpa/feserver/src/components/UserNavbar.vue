<script setup>
import LogoutButton from '@/components/LogoutButton.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const current_user_id = auth.user?.id
</script>

<template>
  <nav class="navbar">
    <div class="nav-container">
      <div class="navbar-brand">
        <svg class="logo-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17a2 2 0 01-2 2H5a2 2 0 01-2-2v-4a2 2 0 012-2h2a2 2 0 012 2v4zm10 0a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4a2 2 0 012-2h2a2 2 0 012 2v4zM3 9h18v2H3V9zm4-4h10v2H7V5z"/>
        </svg>
        <h2>User Dashboard</h2>
      </div>

      <ul class="navbar-links">
        <li>
          <router-link :to="`/user/${current_user_id}`" class="nav-link">Home</router-link>
        </li>
        <li>
          <router-link to="/parking-lot-list" class="nav-link">Parking Lots</router-link>
        </li>
        <li>
          <router-link to="/user-summary" class="nav-link">Summary</router-link>
        </li>
        <li class="logout-wrapper">
          <LogoutButton />
        </li>
      </ul>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  z-index: 50;
  backdrop-filter: blur(20px);
  background: rgba(102, 126, 234, 0.95);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  width: 2rem;
  height: 2rem;
  color: white;
}

.navbar-brand h2 {
  margin: 0;
  color: white;
  font-weight: 700;
  font-size: 1.5rem;
  letter-spacing: -0.5px;
  font-family: 'Poppins', sans-serif;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-links {
  list-style: none;
  display: flex;
  gap: 0.5rem;
  margin: 0;
  padding: 0;
  align-items: center;
}

.navbar-links li {
  display: inline-block;
}

.nav-link {
  display: inline-block;
  padding: 0.5rem 1.25rem;
  color: white;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  border-radius: 50px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.3);
  font-weight: 600;
}

/* Style for LogoutButton to match nav links */
.logout-wrapper :deep(button),
.logout-wrapper :deep(a) {
  display: inline-block;
  padding: 0.5rem 1.25rem;
  color: white;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  border-radius: 50px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  font-family: inherit;
}

.logout-wrapper :deep(button):hover,
.logout-wrapper :deep(a):hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* Responsive */
@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .navbar-links {
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem;
  }

  .navbar-brand h2 {
    font-size: 1.25rem;
  }

  .nav-link {
    padding: 0.4rem 1rem;
    font-size: 0.9rem;
  }
}
</style>