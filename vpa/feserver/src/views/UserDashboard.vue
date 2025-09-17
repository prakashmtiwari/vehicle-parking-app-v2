<script setup>
import UserNavbar from '../components/UserNavbar.vue'
import UserFooter from '../components/UserFooter.vue'
</script>

<template>
  <div class="dashboard">
    <UserNavbar />

    <main class="content">
      <h1>Welcome, User</h1>
      <p>Here you can your parking reservations and history.</p>
    </main>

    <UserFooter />
  </div>
</template>

<style scoped>
.content {
  padding: 2rem;
  min-height: calc(100vh - 140px); /* adjust for navbar + footer */
}
</style>
