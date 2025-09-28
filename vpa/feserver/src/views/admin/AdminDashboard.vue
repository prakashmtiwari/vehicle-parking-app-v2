<script setup>
import AdminNavbar from '@/components/AdminNavbar.vue'
import AdminFooter from '@/components/AdminFooter.vue'
</script>

<template>
  <div class="dashboard">
    <AdminNavbar />

    <main class="content">
      <h1>Welcome, Admin</h1>
      <p>Here you can manage users, view reports, and configure settings.</p>
    </main>
   
    <AdminFooter />
  </div>
</template>

<style scoped>
.content {
  padding: 2rem;
  min-height: calc(100vh - 140px); /* adjust for navbar + footer */
}
</style>
