<script setup>
import UserNavbar from '@/components/UserNavbar.vue'
import UserFooter from '@/components/UserFooter.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const current_user_name = authStore.user?.username || 'User'
</script>

<template>
  <div class="dashboard">
    <!-- Background Effects -->
    <div class="background-effects"></div>

    <UserNavbar />

    <main class="content">
      <div class="content-wrapper">
        <!-- Hero Section -->
        <div class="hero-section">
          <div class="welcome-badge">
            <span class="badge-icon">👋</span>
            Welcome Back
          </div>
          <h1 class="hero-title">
            Hello, <span class="highlight-text">{{ current_user_name }}</span>
          </h1>
          <p class="hero-subtitle">
            Ready to find your perfect parking spot? Let's get started!
          </p>

          <!-- CTA Button -->
          <RouterLink to="/parking-lot-list" class="cta-button">
            <span class="btn-icon">🚗</span>
            <span>Reserve a Parking Spot</span>
            <svg class="btn-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
            </svg>
          </RouterLink>
        </div>

        <!-- Quick Actions Grid -->
        <!-- <div class="quick-actions">
          <h2 class="section-title">Quick Actions</h2>
          <div class="actions-grid">
            <RouterLink to="/parking-lot-list" class="action-card">
              <div class="action-icon find">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
                </svg>
              </div>
              <div class="action-content">
                <h3 class="action-title">Find Parking</h3>
                <p class="action-description">Search available spots near you</p>
              </div>
              <svg class="action-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </RouterLink>

            <RouterLink to="/my-bookings" class="action-card">
              <div class="action-icon bookings">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div class="action-content">
                <h3 class="action-title">My Bookings</h3>
                <p class="action-description">View your reservations</p>
              </div>
              <svg class="action-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </RouterLink>

            <RouterLink to="/payment-history" class="action-card">
              <div class="action-icon payment">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"/>
                </svg>
              </div>
              <div class="action-content">
                <h3 class="action-title">Payment History</h3>
                <p class="action-description">Track your transactions</p>
              </div>
              <svg class="action-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </RouterLink>

            <RouterLink to="/profile" class="action-card">
              <div class="action-icon profile">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
              </div>
              <div class="action-content">
                <h3 class="action-title">My Profile</h3>
                <p class="action-description">Manage your account</p>
              </div>
              <svg class="action-arrow" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
              </svg>
            </RouterLink>
          </div>
        </div> -->

        <!-- Features Section -->
        <div class="features-section">
          <h2 class="section-title">Why Park With Us?</h2>
          <div class="features-grid">
            <div class="feature-card">
              <div class="feature-icon instant">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                </svg>
              </div>
              <h3 class="feature-title">Instant Booking</h3>
              <p class="feature-description">Reserve your spot in seconds with real-time availability</p>
            </div>

            <div class="feature-card">
              <div class="feature-icon secure">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
                </svg>
              </div>
              <h3 class="feature-title">Secure Payment</h3>
              <p class="feature-description">Your payments are protected with bank-level encryption</p>
            </div>

            <div class="feature-card">
              <div class="feature-icon support">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z"/>
                </svg>
              </div>
              <h3 class="feature-title">24/7 Support</h3>
              <p class="feature-description">We're here to help you anytime, anywhere</p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <UserFooter />
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

.dashboard {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Poppins', sans-serif;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow-x: hidden;
}

.background-effects {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}

/* Content */
.content {
  flex: 1;
  position: relative;
  z-index: 1;
  padding: 6rem 2rem 3rem;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

/* Hero Section */
.hero-section {
  text-align: center;
  margin-bottom: 4rem;
}

.welcome-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.2);
  padding: 0.5rem 1.25rem;
  border-radius: 50px;
  color: white;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
}

.badge-icon {
  font-size: 1.1rem;
}

.hero-title {
  font-size: 3rem;
  font-weight: 800;
  color: white;
  margin: 0 0 1rem 0;
  line-height: 1.2;
  letter-spacing: -1px;
}

.highlight-text {
  background: linear-gradient(90deg, #fff 0%, rgba(255, 255, 255, 0.9) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.9);
  margin: 0 0 2.5rem 0;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

/* CTA Button */
.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem 2.5rem;
  background: white;
  color: #667eea;
  text-decoration: none;
  border-radius: 1rem;
  font-size: 1.125rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.cta-button:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
}

.btn-icon {
  font-size: 1.5rem;
}

.btn-arrow {
  width: 1.25rem;
  height: 1.25rem;
  transition: transform 0.3s ease;
}

.cta-button:hover .btn-arrow {
  transform: translateX(4px);
}

/* Section Title */
.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  text-align: center;
  margin: 0 0 2rem 0;
  letter-spacing: -0.5px;
}

/* Quick Actions */
.quick-actions {
  margin-bottom: 4rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.action-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1.25rem;
  padding: 1.75rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  text-decoration: none;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.action-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s ease;
}

.action-card:hover::before {
  left: 100%;
}

.action-card:hover {
  transform: translateY(-6px);
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
}

.action-icon {
  width: 3.5rem;
  height: 3.5rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: transform 0.3s ease;
}

.action-card:hover .action-icon {
  transform: scale(1.1) rotate(5deg);
}

.action-icon svg {
  width: 2rem;
  height: 2rem;
  color: white;
}

.action-icon.find {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.action-icon.bookings {
  background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
}

.action-icon.payment {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.action-icon.profile {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.action-content {
  flex: 1;
}

.action-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: white;
  margin: 0 0 0.25rem 0;
}

.action-description {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

.action-arrow {
  width: 1.5rem;
  height: 1.5rem;
  color: rgba(255, 255, 255, 0.6);
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.action-card:hover .action-arrow {
  color: white;
  transform: translateX(4px);
}

/* Features Section */
.features-section {
  margin-bottom: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1.25rem;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-8px);
  background: rgba(255, 255, 255, 0.2);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
}

.feature-icon {
  width: 4rem;
  height: 4rem;
  margin: 0 auto 1.5rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon {
  transform: scale(1.1) rotate(5deg);
}

.feature-icon svg {
  width: 2rem;
  height: 2rem;
  color: white;
}

.feature-icon.instant {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
}

.feature-icon.secure {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
}

.feature-icon.support {
  background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
  margin: 0 0 0.75rem 0;
}

.feature-description {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.85);
  margin: 0;
  line-height: 1.6;
}

/* Responsive */
@media (max-width: 968px) {
  .content {
    padding: 5rem 1.5rem 2rem;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }

  .section-title {
    font-size: 1.75rem;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .content {
    padding: 4.5rem 1rem 1.5rem;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .welcome-badge {
    font-size: 0.85rem;
    padding: 0.4rem 1rem;
  }

  .cta-button {
    padding: 1rem 2rem;
    font-size: 1rem;
  }

  .section-title {
    font-size: 1.5rem;
  }

  .action-card {
    padding: 1.5rem;
  }

  .action-icon {
    width: 3rem;
    height: 3rem;
  }

  .action-icon svg {
    width: 1.75rem;
    height: 1.75rem;
  }

  .feature-card {
    padding: 1.5rem;
  }

  .feature-icon {
    width: 3.5rem;
    height: 3.5rem;
  }

  .feature-icon svg {
    width: 1.75rem;
    height: 1.75rem;
  }
}
</style>