<template>
  <div class="homepage">
    <!-- Navigation -->
    <nav class="nav-bar">
      <div class="nav-container">
        <div class="logo-section">
          <svg class="logo-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17a2 2 0 01-2 2H5a2 2 0 01-2-2v-4a2 2 0 012-2h2a2 2 0 012 2v4zm10 0a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4a2 2 0 012-2h2a2 2 0 012 2v4zM3 9h18v2H3V9zm4-4h10v2H7V5z"/>
          </svg>
          <span class="logo-text">ParkApp</span>
        </div>
        <div class="nav-buttons">
          <router-link to="/login" class="nav-btn nav-btn-login">Login</router-link>
          <router-link to="/register" class="nav-btn nav-btn-register">Register</router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="main-content">
      <div class="welcome-card">
        <h1 class="title">🚗 Welcome to ParkApp</h1>
        <h2 class="subtitle">Find and book your parking spot with ease</h2>

        <!-- Parking Preview -->
        <div class="parking-preview">
          <div
            v-for="i in 4"
            :key="i"
            class="parking-spot"
          >
            <svg 
              :class="['spot-icon', i % 2 === 0 ? 'available' : 'occupied']" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17a2 2 0 01-2 2H5a2 2 0 01-2-2v-4a2 2 0 012-2h2a2 2 0 012 2v4zm10 0a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4a2 2 0 012-2h2a2 2 0 012 2v4zM3 9h18v2H3V9zm4-4h10v2H7V5z"/>
            </svg>
            <p class="spot-status">{{ i % 2 === 0 ? 'Available' : 'Occupied' }}</p>
          </div>
        </div>

        <!-- <h4 class="prompt">What would you like to do?</h4>

        <div class="button-group">
          <router-link class="btn login" to="/login">Login</router-link>
          <router-link class="btn register" to="/register">Register</router-link>
        </div> -->
      </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
      <p>© {{ new Date().getFullYear()}} ParkApp  | All Rights Reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

.homepage {
  min-height: 100vh;
  background: linear-gradient(135deg, #6b73ff 0%, #000dff 100%);
  color: white;
  font-family: 'Poppins', sans-serif;
  display: flex;
  flex-direction: column;
}

/* Navigation */
.nav-bar {
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 50;
  backdrop-filter: blur(12px);
  background: rgba(0, 13, 255, 0.3);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0.75rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.logo-icon {
  width: 1.75rem;
  height: 1.75rem;
  color: #fff;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
}

.nav-buttons {
  display: flex;
  gap: 0.75rem;
}

.nav-btn {
  padding: 0.4rem 1.25rem;
  border-radius: 50px;
  font-weight: 500;
  font-size: 0.95rem;
  text-decoration: none;
  transition: all 0.3s ease;
}

.nav-btn-login {
  border: 1px solid rgba(255, 255, 255, 0.6);
  color: white;
  background: transparent;
}

.nav-btn-login:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

.nav-btn-register {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.nav-btn-register:hover {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

/* Main Content */
.main-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5rem 1.5rem 2rem;
}

.welcome-card {
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 2rem;
  padding: 2.5rem;
  max-width: 650px;
  width: 90%;
  text-align: center;
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.welcome-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
}

.title {
  font-size: 2.25rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
}

.subtitle {
  font-size: 1.2rem;
  color: #e2e8f0;
  margin-bottom: 1.5rem;
}

/* Parking Preview */
.parking-preview {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin: 1.5rem 0;
  padding: 1.5rem;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.parking-spot {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  padding: 1rem;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.parking-spot:hover {
  transform: scale(1.05);
  background: rgba(255, 255, 255, 0.15);
}

.spot-icon {
  width: 2.5rem;
  height: 2.5rem;
  margin: 0 auto 0.5rem;
}

.spot-icon.available {
  color: #22c55e;
}

.spot-icon.occupied {
  color: #94a3b8;
}

.spot-status {
  font-size: 0.75rem;
  margin-top: 0.5rem;
}

.prompt {
  font-size: 1.1rem;
  color: #cbd5e1;
  margin-bottom: 1.5rem;
}

.button-group {
  display: flex;
  justify-center: center;
  gap: 1.25rem;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 50px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn.login {
  background: #3b82f6;
  color: white;
}

.btn.register {
  background: #22c55e;
  color: white;
}

.btn.login:hover {
  background: #2563eb;
  transform: scale(1.05);
}

.btn.register:hover {
  background: #16a34a;
  transform: scale(1.05);
}

/* Footer */
.footer {
  padding: 1rem;
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Responsive */
@media (max-width: 640px) {
  .parking-preview {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .title {
    font-size: 1.75rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
  
  .welcome-card {
    padding: 2rem 1.5rem;
  }
}
</style>