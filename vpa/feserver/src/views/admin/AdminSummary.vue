<script setup>
import AdminNavbar from '@/components/AdminNavbar.vue'
import AdminFooter from '@/components/AdminFooter.vue'
import AdminCharts from '@/components/AdminCharts.vue';
import AdminParkingHistory from '@/components/adminParkingHistory.vue';


</script>

<template>
  <div class="dashboard">
    <AdminNavbar />

    <main class="content">
      <h6>Here you can see reports of parking history and the collected revenue</h6>
        <AdminParkingHistory /> <br>

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

h6 {
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  text-align: center;
  font-weight: 500;
  font-size:large;
} 
</style>
