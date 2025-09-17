<template>
  <div class="overlay">
    <div class="card">
      <h1>Vehicle Parking App</h1>
      <p>Welcome! Please choose an option:</p>
      <router-link to="/login">Login</router-link>
      <router-link to="/register">Register</router-link>
    </div>
  </div>
</template>

<script>
export default {
  mounted() {
    const token = localStorage.getItem("authToken");
    if (token) this.$router.push("/dashboard");
  }
}
</script>
