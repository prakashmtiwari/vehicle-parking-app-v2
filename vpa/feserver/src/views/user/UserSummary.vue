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
      <p>Here you can see your parking reservation history charts and summary.</p>
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
</style>
