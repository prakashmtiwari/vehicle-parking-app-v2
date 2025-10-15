<script setup>
import AdminNavbar from '@/components/AdminNavbar.vue'
import AdminFooter from '@/components/AdminFooter.vue'
import AdminSearch from '@/components/AdminSearch.vue';
</script>

<template>
  <div class="dashboard">
    <AdminNavbar />

    <main class="content">
      <p>Welcome to the Admin Dashboard. Use the search below to find parking lots, spots, or users.</p>
        <AdminSearch />

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
