<script setup>
import AdminNavbar from '@/components/AdminNavbar.vue'
import AdminFooter from '@/components/AdminFooter.vue'
import AdminSearch from '@/components/AdminSearch.vue';
</script>

<template>
  <div class="dashboard">
    <AdminNavbar />

    <main class="content">
      <h6>Welcome to the Admin Dashboard. Search below to find parking lots, spots, or users.</h6><br></br>
        <AdminSearch />

    </main>
    

    <AdminFooter />
  </div>
</template>

<style scoped>
.content {
  padding: 2rem;
  min-height: calc(100vh - 140px); /* adjust for navbar + footer */
  padding-bottom: 80px; 
}

h6 {
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  text-align: center;
}

.dashboard{
  background:   white;
  width: 100%;
}
</style>
