<script setup>
import LogoutButton from '@/components/LogoutButton.vue'
</script>

<template>
  <nav class="navbar navbar-expand-md">
    <div class="container-fluid">
    <div class="navbar-brand">
      <h2>Admin Dashboard</h2>
    </div>

    <ul class="navbar-links">
      <button class="btn  btn-sm custom-btn"><li><router-link to="/admin" class="text-black">Home</router-link></li></button>
      <button class="btn  btn-sm custom-btn"><li><router-link to="/parking-lots" class="text-black">Parking Lots</router-link></li></button>
      <button class="btn  btn-sm custom-btn"><li><router-link to="/users" class="text-black">Users</router-link></li></button>
      <button class="btn  btn-sm custom-btn"><li><router-link to="/admin-summary" class="text-black">Reports</router-link></li></button>
      <LogoutButton />
    </ul>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background:   white;
  padding: 1rem 2rem; 
}


.navbar-brand h2 {
  margin: 0;
  color: rgb(56, 53, 206, 0.74);
  font-weight: bold;
  letter-spacing: -1px;
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

.navbar-links a {
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
