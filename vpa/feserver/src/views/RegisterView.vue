<script setup>
import { reactive, ref } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'
import { useRouter } from 'vue-router'
import { API_HOST } from '@/services/apiConfig'

const toast = useToast()
const router = useRouter()

const form = reactive({
  email: '',
  username: '',
  password: '',
  confirmPassword: '',
  first_name: '',
  last_name: ''
})

const message = ref('')
const messageType = ref('') // "success" or "error"
const emailError = ref('')

function validateEmail() {
  const email = form.email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  emailError.value = email && !emailRegex.test(email)
    ? 'Please enter a valid email address'
    : ''
}

const registerUser = async () => {
  message.value = ''

  validateEmail()
  if (emailError.value) {
    message.value = emailError.value
    messageType.value = 'error'
    toast.error(emailError.value)
    return
  }

  if (form.password !== form.confirmPassword) {
    message.value = 'Passwords do not match!'
    messageType.value = 'error'
    toast.error(message.value)
    return
  }

  try {
    const res = await axios.post(`${API_HOST}/auth/register`, form)
    message.value = res.data.message
    messageType.value = res.data.success ? 'success' : 'error'
    if (res.data.success) {
      toast.success(message.value)
      router.push('/login')  
    } else {
      toast.error(message.value)
    }
  } catch (err) {
    message.value = err.response?.data?.message || 'Something went wrong'
    messageType.value = 'error'
    toast.error(message.value)
  }
}
</script>

<template>
  <div class="register-page">
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
    <div class="register-container">
      <div class="register-card">
        <div class="card-header">
          <div class="header-badge">
            <span class="badge-icon">✨</span>
            Get Started
          </div>
          <h2 class="card-title">Create Your Account</h2>
          <p class="card-subtitle">Join thousands of happy parkers today</p>
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

        <form @submit.prevent="registerUser" class="register-form">
          <div class="form-row">
            <div class="form-group">
              <label for="first_name" class="form-label">
                <svg class="label-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
                First Name
              </label>
              <input 
                v-model="form.first_name" 
                type="text" 
                id="first_name" 
                class="form-input" 
                placeholder="John"
                required 
              />
            </div>

            <div class="form-group">
              <label for="last_name" class="form-label">
                <svg class="label-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
                Last Name
              </label>
              <input 
                v-model="form.last_name" 
                type="text" 
                id="last_name" 
                class="form-input" 
                placeholder="Doe"
                required 
              />
            </div>
          </div>

          <div class="form-group">
            <label for="email" class="form-label">
              <svg class="label-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
              Email Address
            </label>
            <input 
              v-model="form.email" 
              type="email" 
              id="email" 
              class="form-input" 
              placeholder="john.doe@example.com"
              @input="validateEmail"
              required 
            />
            <p v-if="emailError" class="error-text">
              <svg class="error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              {{ emailError }}
            </p>
          </div>

          <div class="form-group">
            <label for="username" class="form-label">
              <svg class="label-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              Username
            </label>
            <input 
              v-model="form.username" 
              type="text" 
              id="username" 
              class="form-input" 
              placeholder="johndoe"
              required 
            />
          </div>

          <div class="form-row">
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
                placeholder="••••••••"
                required 
              />
            </div>

            <div class="form-group">
              <label for="confirmPassword" class="form-label">
                <svg class="label-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                </svg>
                Confirm Password
              </label>
              <input 
                v-model="form.confirmPassword" 
                type="password" 
                id="confirmPassword" 
                class="form-input" 
                placeholder="••••••••"
                required 
              />
            </div>
          </div>

          <button 
            type="submit" 
            class="btn-submit" 
            :disabled="!form.email || !form.password || !form.username"
          >
            <span>Create Account</span>
            <svg class="btn-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
            </svg>
          </button>
        </form>

        <div class="divider">
          <span class="divider-text">or</span>
        </div>

        <div class="login-section">
          <p class="login-text">Already have an account?</p>
          <router-link to="/login" class="login-link">
            Sign in here
            <svg class="link-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
            </svg>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

.register-page {
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

/* Register Container */
.register-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6rem 2rem 3rem;
  position: relative;
  z-index: 1;
}

.register-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1.5rem;
  padding: 2.5rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 600px;
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
.register-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
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

.error-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #fecaca;
  margin: 0;
  font-weight: 500;
}

.error-icon {
  width: 1rem;
  height: 1rem;
  flex-shrink: 0;
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

.btn-submit:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
}

.btn-submit:active:not(:disabled) {
  transform: translateY(-1px);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-arrow {
  width: 1.25rem;
  height: 1.25rem;
  transition: transform 0.3s ease;
}

.btn-submit:hover:not(:disabled) .btn-arrow {
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

/* Login Section */
.login-section {
  text-align: center;
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.login-text {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 0.5rem 0;
}

.login-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: white;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.login-link:hover {
  gap: 0.75rem;
}

.link-arrow {
  width: 1.125rem;
  height: 1.125rem;
  transition: transform 0.3s ease;
}

.login-link:hover .link-arrow {
  transform: translateX(4px);
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

  .register-container {
    padding: 5rem 1.5rem 2rem;
  }

  .register-card {
    padding: 2rem 1.5rem;
  }

  .card-title {
    font-size: 1.75rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .back-link span {
    display: none;
  }

  .register-card {
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
}
</style>