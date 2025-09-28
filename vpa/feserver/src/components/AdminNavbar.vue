<script setup>
import LogoutButton from '@/components/LogoutButton.vue'
</script>

<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <h2>Admin Dashboard</h2>
    </div>

    <ul class="navbar-links">
      <button class="btn btn-outline-light btn-sm custom-btn"><li><router-link to="/admin" class="text-white">Home</router-link></li></button>
      <button class="btn btn-outline-light btn-sm custom-btn"><li><router-link to="/parking-lots" class="text-white">Parking Lots</router-link></li></button>
      <button class="btn btn-outline-light btn-sm custom-btn"><li><router-link to="/users" class="text-white">Users</router-link></li></button>
      <button class="btn btn-outline-light btn-sm custom-btn"><li><router-link to="/search" class="text-white">Search</router-link></li></button>
      <button class="btn btn-outline-light btn-sm custom-btn"><li><router-link to="/report" class="text-white">Reports</router-link></li></button>
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
  text-decoration: none;
  font-weight: 500;
}

.custom-btn:hover {
  background-color: #f1a978; /* pick your hover background */
  color: white;              /* ensure text stays visible */}
</style>
