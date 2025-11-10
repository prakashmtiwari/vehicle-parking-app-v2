<script setup>
import LogoutButton from '@/components/LogoutButton.vue'
</script>

<template>
  <nav class="navbar">
    <div class="nav-container">
      <div class="navbar-brand">
        <svg class="logo-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17a2 2 0 01-2 2H5a2 2 0 01-2-2v-4a2 2 0 012-2h2a2 2 0 012 2v4zm10 0a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4a2 2 0 012-2h2a2 2 0 012 2v4zM3 9h18v2H3V9zm4-4h10v2H7V5z"/>
        </svg>
        <h2>Admin Dashboard</h2>
      </div>

      <ul class="navbar-links">
        <li>
          <router-link to="/admin" class="nav-link">Home</router-link>
        </li>
        <li>
          <router-link to="/parking-lots" class="nav-link">Parking Lots</router-link>
        </li>
        <li>
          <router-link to="/users" class="nav-link">Users</router-link>
        </li>
        <li>
          <router-link to="/admin-summary" class="nav-link">Reports</router-link>
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
  position: sticky;
  top: 0;
  width: 100%;
  z-index: 50;
  backdrop-filter: blur(12px);
  background: linear-gradient(135deg, rgba(107, 115, 255, 0.95) 0%, rgba(0, 13, 255, 0.95) 100%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.nav-container {
  max-width: 100%;
  padding: 0.75rem 2rem;
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
}

.navbar-links {
  list-style: none;
  display: flex;
  gap: 1rem;
  margin: 0;
  padding-left: 400px;
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