<template>
  <div class="overlay">
    <div class="card">
      <h2>Register</h2>
      <input v-model="username" placeholder="Username" class="form-control mb-2" />
      <input v-model="email" placeholder="Email" class="form-control mb-2" />
      <input v-model="password" type="password" placeholder="Password" class="form-control mb-2" />
      <button @click="registerUser" class="btn btn-success">Register</button>
      <p class="text-danger mt-2">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import axios from "https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js";

export default {
  data() {
    return { username: "", email: "", password: "", message: "" };
  },
  methods: {
    async registerUser() {
      try {
        const res = await axios.post("http://127.0.0.1:5000/api/auth/register", {
          username: this.username,
          email: this.email,
          password: this.password
        });
        this.$router.push("/login");
      } catch (err) {
        this.message = err.response?.data?.error || "Registration failed";
      }
    }
  }
}
</script>
