<template>
  <div class="text-center mt-5">
    <h1>Welcome to the Vehicle Parking App</h1>
    <h2>Book your spots with ease</h2>

    <h4 class="mt-3">What would you like to do?</h4>
    <div class="d-flex justify-content-center gap-4 mt-4">
      <router-link class="btn btn-primary btn-lg px-4 fw-bold" to="/login">
        Login
      </router-link>
      <router-link class="btn btn-success btn-lg px-4 fw-bold" to="/register">
        Register
      </router-link>
    </div>
  </div>
</template>

<style scoped>
  .text-center {
    text-align: center;
  }
  .mt-5 {
    margin-top: 3rem;
  }
  .mt-3 {
    margin-top: 1rem;
  }
  .mt-4 {
    margin-top: 1.5rem;
  }
  .d-flex {
    display: flex;
  }
  .justify-content-center {
    justify-content: center;
  }
  .gap-4 {
    gap: 1.5rem;
  }
  h1 {
    color: #2c3e50;
    font-family: Arial, sans-serif;
  }
  h2 {
    color: #34495e;
    font-family: 'Courier New', Courier, monospace;   
    font-weight: normal;
  }
  h4 {
    color: #7f8c8d; 
    font-family: 'Courier New', Courier, monospace;   
    font-weight: normal;
  }
  .btn {
    text-decoration: none;    
    color: rgb(57, 173, 226);
  }
  .btn:hover { 
    text-decoration: none;
    color: rgb(131, 10, 10);   
    opacity: 0.8;
  }   
</style>  