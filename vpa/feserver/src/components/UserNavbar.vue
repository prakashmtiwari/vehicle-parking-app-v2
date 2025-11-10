<script setup>
import LogoutButton from '@/components/LogoutButton.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const current_user_id = auth.user?.id

</script>

<template>
  <nav class="navbar navbar-expand-md">
    <div class="navbar-brand">
      <h2>User Dashboard</h2>
    </div>

    <ul class="navbar-links">
      <button class="btn custom-button btn-sm custom-btn"><li><router-link :to="`/user/${current_user_id}`" class="text-black">Home</router-link></li></button>
      <button class="btn custom-button btn-sm custom-btn"><li><router-link to="/parking-lot-list" class="text-black">Parking Lots</router-link></li></button>
      <button class="btn custom-button btn-sm custom-btn"><li><router-link to="/user-summary" class="text-black">Summary</router-link></li></button>
      <li><LogoutButton /></li>
    </ul>
  </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  padding: 1rem 2rem;
}

.navbar-brand h2 {
  margin: 0;
  color: rgb(56, 53, 206, 0.74);
  letter-spacing: -1px;
  font-weight: bold;  
  font-family: sans-serif;
  font-style: italic;
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

.custom-btn{
  background: transparent;
  border: none;
  color: #ecf0f1;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
</style>
