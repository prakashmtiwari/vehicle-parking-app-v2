<script setup>
import AdminNavbar from '@/components/AdminNavbar.vue'
import AdminFooter from '@/components/AdminFooter.vue'
import AdminCharts from '@/components/AdminCharts.vue';

</script>

<template>
  <div class="dashboard">
    <AdminNavbar />

    <main class="content">
      <p>Here you can see reports of parking history and revenue collected.</p>

        <AdminCharts />
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
