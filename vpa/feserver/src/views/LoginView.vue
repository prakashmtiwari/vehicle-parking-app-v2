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
    <!-- Background Effects -->
    <div class="background-effects"></div>

    <!-- Navigation -->
    <nav class="nav-bar">
      <div class="nav-container">
        <router-link to="/" class="logo-section">
          <div class="logo-icon-wrapper">
            <svg class="logo-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17a2 2 0 01-2 2H5a2 2 0 01-2-2v-4a2 2 0 012-2h2a2 2 0 012 2v4zm10 0a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4a2 2 0 012-2h2a2 2 0 012 2v4zM3 9h18v2H3V9zm4-4h10v2H7V5z"/>
            </svg>
          </div>
          <span class="logo-text">ParkApp</span>
        </router-link>
        <router-link to="/" class="back-link">
          <svg class="back-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
          </svg>
          Back to Home
        </router-link>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="login-container">
      <div class="login-card">
        <div class="card-header">
          <div class="header-badge">
            <span class="badge-icon">👋</span>
            Welcome Back
          </div>
          <h2 class="card-title">Sign In</h2>
          <p class="card-subtitle">Access your parking dashboard</p>
        </div>

        <div v-if="message" class="alert" :class="messageType === 'success' ? 'alert-success' : 'alert-error'">
          <svg v-if="messageType === 'success'" class="alert-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <svg v-else class="alert-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          {{ message }}
        </div>

        <form @submit.prevent="loginUser" class="login-form">
          <div class="form-group">
            <label for="username" class="form-label">
              <svg class="label-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
              </svg>
              Username
            </label>
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
            <label for="password" class="form-label">
              <svg class="label-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
              </svg>
              Password
            </label>
            <input 
              v-model="form.password" 
              type="password" 
              id="password" 
              class="form-input"
              placeholder="Enter your password" 
              required 
            />
          </div>

          <div class="form-footer">
            <a href="#" class="forgot-link">Forgot password?</a>
          </div>

          <button type="submit" class="btn-submit">
            <span>Sign In</span>
            <svg class="btn-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
            </svg>
          </button>
        </form>

        <div class="divider">
          <span class="divider-text">or</span>
        </div>

        <div class="register-section">
          <p class="register-text">Don't have an account?</p>
          <router-link to="/register" class="register-link">
            Create account
            <svg class="link-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
            </svg>
          </router-link>
        </div>
      </div>

      <!-- Quick Stats -->
      <div class="quick-stats">
        <div class="stat-card">
          <div class="stat-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">24/7</div>
            <div class="stat-label">Available</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">10k+</div>
            <div class="stat-label">Users</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
          </div>
          <div class="stat-content">
            <div class="stat-value">Secure</div>
            <div class="stat-label">Payments</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Poppins', sans-serif;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow-x: hidden;
}

.background-effects {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

/* Navigation */
.nav-bar {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 50;
  backdrop-filter: blur(12px);
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
  transition: transform 0.3s ease;
}

.logo-section:hover {
  transform: translateY(-2px);
}

.logo-icon-wrapper {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.5rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: white;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  letter-spacing: -0.5px;
}

.back-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: white;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.95rem;
  padding: 0.6rem 1.25rem;
  border-radius: 0.75rem;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.3);
  transition: all 0.3s ease;
}

.back-link:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
}

.back-icon {
  width: 1.25rem;
  height: 1.25rem;
}

/* Login Container */
.login-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 6rem 2rem 3rem;
  position: relative;
  z-index: 1;
  gap: 2rem;
}

.login-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1.5rem;
  padding: 2.5rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 480px;
}

/* Card Header */
.card-header {
  text-align: center;
  margin-bottom: 2rem;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.2);
  padding: 0.5rem 1.25rem;
  border-radius: 50px;
  color: white;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.badge-icon {
  font-size: 1.1rem;
}

.card-title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.5px;
}

.card-subtitle {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
}

/* Alert */
.alert {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  border-radius: 0.75rem;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  backdrop-filter: blur(10px);
}

.alert-icon {
  width: 1.25rem;
  height: 1.25rem;
  flex-shrink: 0;
}

.alert-success {
  background: rgba(34, 197, 94, 0.2);
  color: white;
  border: 1px solid rgba(34, 197, 94, 0.4);
}

.alert-error {
  background: rgba(239, 68, 68, 0.2);
  color: white;
  border: 1px solid rgba(239, 68, 68, 0.4);
}

/* Form */
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
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: white;
}

.label-icon {
  width: 1.125rem;
  height: 1.125rem;
  color: rgba(255, 255, 255, 0.8);
}

.form-input {
  width: 100%;
  padding: 0.875rem 1.25rem;
  font-size: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 0.75rem;
  background: rgba(255, 255, 255, 0.9);
  color: #1e293b;
  transition: all 0.3s ease;
  font-family: 'Poppins', sans-serif;
}

.form-input:focus {
  outline: none;
  border-color: white;
  background: white;
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.2);
}

.form-input::placeholder {
  color: #94a3b8;
}

.form-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: -0.5rem;
}

.forgot-link {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: color 0.3s ease;
}

.forgot-link:hover {
  color: white;
  text-decoration: underline;
}

/* Submit Button */
.btn-submit {
  width: 100%;
  padding: 1rem 1.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: #667eea;
  background: white;
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
  font-family: 'Poppins', sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-submit:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

.btn-submit:active {
  transform: translateY(-1px);
}

.btn-arrow {
  width: 1.25rem;
  height: 1.25rem;
  transition: transform 0.3s ease;
}

.btn-submit:hover .btn-arrow {
  transform: translateX(4px);
}

/* Divider */
.divider {
  position: relative;
  text-align: center;
  margin: 1.5rem 0;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: rgba(255, 255, 255, 0.3);
}

.divider-text {
  position: relative;
  background: transparent;
  padding: 0 1rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  font-weight: 500;
}

/* Register Section */
.register-section {
  text-align: center;
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.register-text {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 0.5rem 0;
}

.register-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: white;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.register-link:hover {
  gap: 0.75rem;
}

.link-arrow {
  width: 1.125rem;
  height: 1.125rem;
  transition: transform 0.3s ease;
}

.register-link:hover .link-arrow {
  transform: translateX(4px);
}

/* Quick Stats */
.quick-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  max-width: 480px;
  width: 100%;
}

.stat-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.stat-icon {
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.75rem;
  background: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg {
  width: 1.5rem;
  height: 1.5rem;
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 1.125rem;
  font-weight: 700;
  color: white;
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-container {
    padding: 1rem 1.5rem;
  }

  .logo-text {
    font-size: 1.25rem;
  }

  .back-link {
    font-size: 0.85rem;
    padding: 0.5rem 1rem;
  }

  .login-container {
    padding: 5rem 1.5rem 2rem;
  }

  .login-card {
    padding: 2rem 1.5rem;
  }

  .card-title {
    font-size: 1.75rem;
  }

  .quick-stats {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .back-link span {
    display: none;
  }

  .login-card {
    padding: 1.5rem 1.25rem;
  }

  .card-title {
    font-size: 1.5rem;
  }

  .header-badge {
    font-size: 0.8rem;
    padding: 0.4rem 1rem;
  }

  .form-input {
    padding: 0.75rem 1rem;
  }

  .btn-submit {
    padding: 0.875rem 1.25rem;
    font-size: 1rem;
  }

  .stat-card {
    padding: 1rem;
  }

  .stat-icon {
    width: 2rem;
    height: 2rem;
  }

  .stat-icon svg {
    width: 1.25rem;
    height: 1.25rem;
  }

  .stat-value {
    font-size: 1rem;
  }
}
</style>