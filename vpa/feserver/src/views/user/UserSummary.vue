<script setup>
import UserNavbar from '@/components/UserNavbar.vue'
import UserFooter from '@/components/UserFooter.vue'
import UserParkingHistory from '@/components/UserParkingHistory.vue';   
import UserCharts from '@/components/UserCharts.vue';
</script>

<template>
  <div class="dashboard">
    <UserNavbar />

    <main class="content">
      <div id="intro">
      <h6>Here you can see your parking reservation history charts and summary.</h6>
      </div>
      <UserParkingHistory />
      <UserCharts />
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

h6 {
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  text-align: center;
}
</style>
