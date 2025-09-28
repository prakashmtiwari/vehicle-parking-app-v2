<script setup>
import LogoutButton from '@/components/LogoutButton.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

</script>

<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <h2>User Dashboard</h2>
    </div>

    <ul class="navbar-links">
      <button class="btn btn-outline-light btn-sm custom-btn"><li><router-link to="`/user/${auth.user?.id}`" class="text-white">Home</router-link></li></button>
      <button class="btn btn-outline-light btn-sm custom-btn"><li><router-link to="/parking-lot-list" class="text-white">Parking Lots</router-link></li></button>
      <button class="btn btn-outline-light btn-sm custom-btn"><li><router-link to="/summary" class="text-white">Summary</router-link></li></button>
      <button class="btn btn-outline-light btn-sm custom-btn"><li><router-link to="/settings" class="text-white">Edit Profile</router-link></li></button>
      <li><LogoutButton /></li>
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

.navbar-links a{
  text-decoration: none;
  font-weight: 500;
}

.custom-btn:hover {
  background-color: #f1a978; /* pick your hover background */
  color: white;              /* ensure text stays visible */}

</style>
