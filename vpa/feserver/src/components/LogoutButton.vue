<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <button class="btn btn-outline-light btn-sm custom-btn" @click="handleLogout">
    Logout
  </button>
</template>

<style scoped>
.btn {
  font-weight: 500;
}

.custom-btn:hover {
  background-color: #ff6600; /* pick your hover background */
  color: white;              /* ensure text stays visible */}
  
</style>