<template>
  <div class="overlay">
    <div class="card">
      <h2>Login</h2>
      <input v-model="email" placeholder="Email" class="form-control mb-2" />
      <input v-model="password" type="password" placeholder="Password" class="form-control mb-2" />
      <button @click="loginUser" class="btn btn-primary">Login</button>
      <p class="text-danger mt-2">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import axios from "https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js";

export default {
  data() {
    return { email: "", password: "", message: "" };
  },
  methods: {
    async loginUser() {
      try {
        const res = await axios.post("http://127.0.0.1:5000/api/auth/login", {
          email: this.email,
          password: this.password
        });
        localStorage.setItem("authToken", res.data.access_token);
        localStorage.setItem("role", res.data.role);
        this.$router.push("/dashboard");
      } catch (err) {
        this.message = err.response?.data?.error || "Login failed";
      }
    }
  }
}
</script>
