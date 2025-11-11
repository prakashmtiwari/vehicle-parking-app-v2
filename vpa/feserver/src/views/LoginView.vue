<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast as UseToast } from 'vue-toastification'
import axios from 'axios'

const router = useRouter()
const auth = useAuthStore()
const Toast = UseToast()

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
      Toast.success("Login successful!")

      // role-based redirect
      if (res.data.user.roles.includes('admin')) {
        router.push('/admin')
      } else {
        router.push(`/user/${res.data.user.id}`) // redirect to user dashboard
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
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <div class="card-header">
          <svg class="logo-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17a2 2 0 01-2 2H5a2 2 0 01-2-2v-4a2 2 0 012-2h2a2 2 0 012 2v4zm10 0a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4a2 2 0 012-2h2a2 2 0 012 2v4zM3 9h18v2H3V9zm4-4h10v2H7V5z"/>
          </svg>
          <h2 class="card-title">Welcome Back</h2>
          <p class="card-subtitle">Login to access your parking dashboard</p>
        </div>

        <div v-if="message" class="alert" :class="messageType === 'success' ? 'alert-success' : 'alert-error'">
          {{ message }}
        </div>

        <form @submit.prevent="loginUser" class="login-form">
          <div class="form-group">
            <label for="username" class="form-label">Username</label>
            <input 
              v-model="form.username" 
              type="text" 
              id="username" 
              class="form-input" 
              placeholder="Enter your username"
              required 
            />
          </div>

          <div class="form-group">
            <label for="password" class="form-label">Password</label>
            <input 
              v-model="form.password" 
              type="password" 
              id="password" 
              class="form-input"
              placeholder="Enter your password" 
              required 
            />
          </div>

          <button type="submit" class="btn-submit">Login</button>
        </form>

        <p class="register-link">
          Don't have an account? <router-link to="/register" class="link">Register here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #6b73ff 0%, #000dff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  font-family: 'Poppins', sans-serif;
}

.login-container {
  width: 100%;
  max-width: 450px;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 1.5rem;
  padding: 2.5rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.card-header {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-icon {
  width: 3rem;
  height: 3rem;
  color: #6b73ff;
  margin: 0 auto 1rem;
}

.card-title {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.5px;
}

.card-subtitle {
  font-size: 0.95rem;
  color: #64748b;
  margin: 0;
}

.alert {
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  font-weight: 500;
}

.alert-success {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.alert-error {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: #334155;
}

.form-input {
  width: 100%;
  padding: 0.875rem 1.25rem;
  font-size: 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.75rem;
  background: white;
  color: #1e293b;
  transition: all 0.3s ease;
  font-family: 'Poppins', sans-serif;
}

.form-input:focus {
  outline: none;
  border-color: #6b73ff;
  box-shadow: 0 0 0 3px rgba(107, 115, 255, 0.1);
}

.form-input::placeholder {
  color: #94a3b8;
}

.btn-submit {
  width: 100%;
  padding: 0.875rem 1.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: white;
  background: linear-gradient(135deg, #6b73ff 0%, #000dff 100%);
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
  font-family: 'Poppins', sans-serif;
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(107, 115, 255, 0.4);
}

.btn-submit:active {
  transform: translateY(0);
}

.register-link {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.95rem;
  color: #64748b;
}

.link {
  color: #6b73ff;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.link:hover {
  color: #000dff;
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 640px) {
  .login-page {
    padding: 1rem;
  }

  .login-card {
    padding: 2rem 1.5rem;
  }

  .card-title {
    font-size: 1.5rem;
  }

  .logo-icon {
    width: 2.5rem;
    height: 2.5rem;
  }
}
</style>