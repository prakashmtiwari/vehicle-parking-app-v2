<script setup>
import UserNavbar from '@/components/UserNavbar.vue'
import UserFooter from '@/components/UserFooter.vue'
import UserParkingHistory from '@/components/UserParkingHistory.vue';   
</script>

<template>
  <div class="dashboard">
    <UserNavbar />

    <main class="content">
      <div id="intro">
      <h1>Welcome, User</h1>
      <p>Here you can see your parking reservation history.</p>
      </div>
      <UserParkingHistory />
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
