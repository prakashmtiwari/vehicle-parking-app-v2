<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const router = useRouter()
const auth = useAuthStore()

const form = reactive({
  username: '',
  password: ''
})

const message = ref('')
const messageType = ref('') // "success" | "error"

const loginUser = async () => {
  message.value = ''

  if (!form.username || !form.password) {
    message.value = 'Username and password are required!'
    messageType.value = 'error'
    return
  }

  try {
    const res = await axios.post('http://127.0.0.1:5000/auth/login', form)

    if (res.data.success) {
      auth.login(res.data.access_token, res.data.user)

      message.value = res.data.message
      messageType.value = 'success'

      // role-based redirect
      if (res.data.user.roles.includes('admin')) {
        router.push('/admin')
      } else {
        router.push('/user')
      }
    } else {
      message.value = res.data.message
      messageType.value = 'error'
    }
  } catch (err) {
    message.value = err.response?.data?.message || 'Something went wrong'
    messageType.value = 'error'
  }
}
</script>

<template>
    <div class="login-container">    
    <div class="container my-5" style="max-width: 400px;">
    <h2 class="mb-4 text-center">Login</h2>

    <div v-if="message" class="alert" :class="messageType === 'success' ? 'alert-success' : 'alert-danger'">
      {{ message }}
    </div>

    <form @submit.prevent="loginUser">
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input v-model="form.username" type="text" id="username" class="form-control" required />
      </div>

      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input v-model="form.password" type="password" id="password" class="form-control" required />
      </div>

      <button type="submit" class="btn btn-primary w-100">Login</button>
    </form>

    <p class="mt-3 text-center">
      Don't have an account? <router-link to="/register">Register</router-link>
    </p>
  </div>
  </div>    
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background: #f4f6f9;
}

.card {
  width: 400px;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 1rem;
}

input {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 6px;
}

button {
  width: 100%;
  margin-top: 1rem;
}

.message {
  margin-top: 1rem;
  font-weight: bold;
  text-align: center;
}
.message.success {
  color: green;
}
.message.error {
  color: red;
}
.link {
  display: block;
  margin-top: 1rem;
  text-align: center;
  color: #3498db;
}
.link:hover {
  text-decoration: underline;
}
</style>
