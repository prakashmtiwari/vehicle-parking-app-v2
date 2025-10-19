<script setup>
import UserNavbar from '@/components/UserNavbar.vue'
import UserFooter from '@/components/UserFooter.vue'
import { useAuthStore } from '@/stores/auth'
import { Doughnut } from 'vue-chartjs'

const authStore = useAuthStore()
const current_user_name = authStore.user?.username

</script>

<template>
  <div class="dashboard">
    <UserNavbar />

    <main class="content">
      <div id="intro">
      <h1>Welcome to the parking app</h1>
      </div>
       
      <div class="reserve-button">
        <RouterLink to="/parking-lot-list">
          <button type="button" class="btn btn-lg">Reserve a Parking Spot?</button>
        </RouterLink>
      </div>
    </main>

    

    <UserFooter />
  </div>
</template>

<style scoped>
.content {
  padding: 2rem; 
}

#intro {
  padding-left: 24rem;
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
}

.reserve-button {
  margin-top: 2rem;
  padding-left: 30rem;
}

.reserve-button .btn {
  background-color: rgb(218, 47, 218);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1.25rem;
  border-radius: 5rem;
  cursor: pointer;
}
</style>
