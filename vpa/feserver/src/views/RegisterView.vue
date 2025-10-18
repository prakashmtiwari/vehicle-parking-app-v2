<script setup>
import { reactive, ref } from 'vue'
import axios from 'axios'

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

const registerUser = async () => {
  message.value = ''

  if (form.password !== form.confirmPassword) {
    message.value = 'Passwords do not match!'
    messageType.value = 'error'
    return
  }

  try {
    const res = await axios.post('http://127.0.0.1:5000/auth/register', form)
    message.value = res.data.message
    messageType.value = res.data.success ? 'success' : 'error'
  } catch (err) {
    message.value = err.response?.data?.message || 'Something went wrong'
    messageType.value = 'error'
  }
}
</script>

<template>
  <div class="register-container">
    <div class="card">
      <h2>Register User</h2>

      <div class="form-group">
        <label>Email</label>
        <input v-model="form.email" type="email" placeholder="Enter email" />
      </div>

      <div class="form-group">
        <label>Username</label>
        <input v-model="form.username" placeholder="Choose a username" />
      </div>

      <div class="form-group">
        <label>Password</label>
        <input v-model="form.password" type="password" placeholder="Enter password" />
      </div>

      <div class="form-group">
        <label>Confirm Password</label>
        <input v-model="form.confirmPassword" type="password" placeholder="Re-enter password" />
      </div>

      <div class="form-group">
        <label>First Name</label>
        <input v-model="form.first_name" placeholder="Enter first name" />
      </div>

      <div class="form-group">
        <label>Last Name</label>
        <input v-model="form.last_name" placeholder="Enter last name" />
      </div>

      <button class="btn" @click="registerUser">Register</button>

      <div v-if="message" :class="['message', messageType]">
        {{ message }}
      </div>

      <router-link class="link" to="/login">Already have an account? Login</router-link><br />
      <router-link class="link" to="/">Home</router-link>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f9f9f9;
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

.btn {
  background-color: rgb(218, 47, 218);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1.25rem;
  border-radius: 5rem;
  cursor: pointer;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  font-family: sans-serif;
}
</style>
