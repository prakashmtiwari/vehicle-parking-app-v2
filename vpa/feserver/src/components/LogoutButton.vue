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

.custom-btn {
  color: white !important;
  border: none;
  background: transparent;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

</style>