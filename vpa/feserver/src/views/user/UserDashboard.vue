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
      <h1>Welcome {{ current_user_name }} to the parking app.</h1>
      </div>
       
      <div id="intro">
        <RouterLink to="/parking-lot-list">
          <button type="button" class="btn btn-primary btn-lg btn-block">Reserve a Parking Spot?</button>
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
  padding-left: 4rem;
}
</style>
