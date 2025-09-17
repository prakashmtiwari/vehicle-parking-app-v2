<script setup>
import LogoutButton from '@/components/LogoutButton.vue'
</script>

<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <h2>Admin Dashboard</h2>
    </div>

    <ul class="navbar-links">
      <li><router-link to="/admin">Home</router-link></li>
      <li><router-link to="/users">Users</router-link></li>
      <li><router-link to="/search">Search</router-link></li>
      <li><router-link to="/report">Reports</router-link></li>
      <LogoutButton />
    </ul>
  </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #2c3e50;
  padding: 1rem 2rem;
  color: white;
}

.navbar-brand h2 {
  margin: 0;
  color: #ecf0f1;
}

.navbar-links {
  list-style: none;
  display: flex;
  gap: 1.5rem;
  margin: 0;
  padding: 0;
}

.navbar-links a {
  color: #ecf0f1;
  text-decoration: none;
  font-weight: 500;
}

.navbar-links a:hover {
  color: #1abc9c;
}
</style>
