<script setup>
import { reactive, ref } from 'vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'
import { useRouter } from 'vue-router'

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
    const res = await axios.post('http://127.0.0.1:5000/auth/register', form)
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
    <div class="register-container">
      <div class="register-card">
        <div class="card-header">
          <svg class="logo-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17a2 2 0 01-2 2H5a2 2 0 01-2-2v-4a2 2 0 012-2h2a2 2 0 012 2v4zm10 0a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4a2 2 0 012-2h2a2 2 0 012 2v4zM3 9h18v2H3V9zm4-4h10v2H7V5z"/>
          </svg>
          <h2 class="card-title">Create Account</h2>
          <p class="card-subtitle">Join us to start parking smarter</p>
        </div>

        <div v-if="message" class="alert" :class="messageType === 'success' ? 'alert-success' : 'alert-error'">
          {{ message }}
        </div>

        <form @submit.prevent="registerUser" class="register-form">
          <div class="form-row">
            <div class="form-group">
              <label for="first_name" class="form-label">First Name</label>
              <input 
                v-model="form.first_name" 
                type="text" 
                id="first_name" 
                class="form-input" 
                placeholder="Enter first name"
                required 
              />
            </div>

            <div class="form-group">
              <label for="last_name" class="form-label">Last Name</label>
              <input 
                v-model="form.last_name" 
                type="text" 
                id="last_name" 
                class="form-input" 
                placeholder="Enter last name"
                required 
              />
            </div>
          </div>

          <div class="form-group">
            <label for="email" class="form-label">Email</label>
            <input 
              v-model="form.email" 
              type="email" 
              id="email" 
              class="form-input" 
              placeholder="Enter email address"
              @input="validateEmail"
              required 
            />
            <p v-if="emailError" class="error-text">{{ emailError }}</p>
          </div>

          <div class="form-group">
            <label for="username" class="form-label">Username</label>
            <input 
              v-model="form.username" 
              type="text" 
              id="username" 
              class="form-input" 
              placeholder="Choose a username"
              required 
            />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="password" class="form-label">Password</label>
              <input 
                v-model="form.password" 
                type="password" 
                id="password" 
                class="form-input" 
                placeholder="Enter password"
                required 
              />
            </div>

            <div class="form-group">
              <label for="confirmPassword" class="form-label">Confirm Password</label>
              <input 
                v-model="form.confirmPassword" 
                type="password" 
                id="confirmPassword" 
                class="form-input" 
                placeholder="Re-enter password"
                required 
              />
            </div>
          </div>

          <button 
            type="submit" 
            class="btn-submit" 
            :disabled="!form.email || !form.password || !form.username"
          >
            Register
          </button>
        </form>

        <div class="links-section">
          <p class="login-link">
            Already have an account? <router-link to="/login" class="link">Login here</router-link>
          </p>
          <router-link to="/" class="link-home">← Back to Home</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #6b73ff 0%, #000dff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  font-family: 'Poppins', sans-serif;
}

.register-container {
  width: 100%;
  max-width: 550px;
}

.register-card {
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

.register-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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
  font-size: 0.9rem;
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

.error-text {
  font-size: 0.85rem;
  color: #dc2626;
  margin: 0;
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

.btn-submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(107, 115, 255, 0.4);
}

.btn-submit:active:not(:disabled) {
  transform: translateY(0);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.links-section {
  margin-top: 1.5rem;
  text-align: center;
}

.login-link {
  font-size: 0.95rem;
  color: #64748b;
  margin-bottom: 0.75rem;
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

.link-home {
  display: inline-block;
  margin-top: 0.5rem;
  color: #64748b;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.link-home:hover {
  color: #6b73ff;
}

/* Responsive */
@media (max-width: 640px) {
  .register-page {
    padding: 1rem;
  }

  .register-card {
    padding: 2rem 1.5rem;
  }

  .card-title {
    font-size: 1.5rem;
  }

  .logo-icon {
    width: 2.5rem;
    height: 2.5rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>