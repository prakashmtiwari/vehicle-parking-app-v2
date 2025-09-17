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
  <button class="btn btn-outline-light btn-sm" @click="handleLogout">
    Logout
  </button>
</template>
