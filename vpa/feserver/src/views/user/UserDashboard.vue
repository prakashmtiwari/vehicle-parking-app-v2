<script setup>
import { ref, computed, onMounted } from 'vue'
import UserNavbar from '@/components/UserNavbar.vue'
import UserFooter from '@/components/UserFooter.vue'
import { useAuthStore } from '@/stores/auth'
import reservationService from '@/services/reservationService'
import { useToast } from 'vue-toastification'

const toast = useToast()
const authStore = useAuthStore()
const current_user_name = authStore.user?.username || 'User'

const reservations = ref([])
const loading = ref(true)

// Compute active reservations (parking time has passed, but not yet left)
const activeReservations = computed(() => {
  return reservations.value.filter(r => {
    const now = new Date()
    const parkingTime = new Date(r.parking_timestamp)
    return !r.leaving_timestamp && parkingTime <= now
  })
})

// Compute upcoming reservations (booked but parking time hasn't arrived)
const upcomingReservations = computed(() => {
  return reservations.value.filter(r => {
    const now = new Date()
    const parkingTime = new Date(r.parking_timestamp)
    return !r.leaving_timestamp && parkingTime > now
  })
})

function formatDateTime(timestamp) {
  if (!timestamp) return '—'
  const date = new Date(timestamp)
  return date.toLocaleString(undefined, {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  })
}

function getTimeSince(timestamp) {
  const now = new Date()
  const start = new Date(timestamp)
  const diff = now - start
  
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  
  if (hours > 0) {
    return `${hours}h ${minutes}m`
  }
  return `${minutes}m`
}

async function loadReservations() {
  loading.value = true
  try {
    const res = await reservationService.getUserReservations()
    reservations.value = res.data || []
  } catch (err) {
    console.error('Error loading reservations:', err)
  } finally {
    loading.value = false
  }
}

async function releaseSpot(reservationId) {
  if (confirm('Are you sure you want to release this spot?')) {
    try {
      await reservationService.completeReservation(reservationId)
      toast.success('Spot released successfully!')
      loadReservations()
    } catch (err) {
      toast.error('Failed to release spot')
    }
  }
}

onMounted(loadReservations)
</script>

<template>
  <div class="dashboard">
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

        <!-- Active Reservations Section -->
        <div v-if="!loading && activeReservations.length > 0" class="active-reservations-section">
          <div class="section-header">
            <h2 class="section-title">
              <span class="pulse-dot"></span>
              Active Parking
            </h2>
            <span class="active-count">{{ activeReservations.length }} active</span>
          </div>

          <div class="reservations-grid">
            <div v-for="reservation in activeReservations" :key="reservation.id" class="reservation-card active">
              <div class="card-header-ribbon">
                <span class="ribbon-badge">ACTIVE NOW</span>
              </div>
              
              <div class="card-content">
                <div class="location-section">
                  <div class="location-icon">
                    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                    </svg>
                  </div>
                  <div>
                    <h3 class="location-name">{{ reservation.spot?.lot?.prime_location_name || 'Parking Lot' }}</h3>
                    <p class="spot-number">Spot #{{ reservation.spot?.id || '—' }}</p>
                  </div>
                </div>

                <div class="details-grid">
                  <div class="detail-item">
                    <span class="detail-label">Vehicle</span>
                    <span class="detail-value">{{ reservation.vehicle_number }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Started</span>
                    <span class="detail-value">{{ formatDateTime(reservation.parking_timestamp) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Duration</span>
                    <span class="detail-value duration">{{ getTimeSince(reservation.parking_timestamp) }}</span>
                  </div>
                  <div class="detail-item">
                    <span class="detail-label">Rate</span>
                    <span class="detail-value">₹{{ reservation.spot?.lot?.price || '—' }}/hr</span>
                  </div>
                </div>

                <button class="release-button" @click="releaseSpot(reservation.id)">
                  <svg class="button-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                  </svg>
                  Release Spot
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Upcoming Reservations Section -->
        <div v-if="!loading && upcomingReservations.length > 0" class="upcoming-reservations-section">
          <div class="section-header">
            <h2 class="section-title-simple">Upcoming Reservations</h2>
            <span class="upcoming-count">{{ upcomingReservations.length }} booked</span>
          </div>

          <div class="upcoming-grid">
            <div v-for="reservation in upcomingReservations" :key="reservation.id" class="upcoming-card">
              <div class="upcoming-badge">BOOKED</div>
              <div class="upcoming-content">
                <h4 class="upcoming-location">{{ reservation.spot?.lot?.prime_location_name || 'Parking Lot' }}</h4>
                <div class="upcoming-details">
                  <span class="upcoming-vehicle">{{ reservation.vehicle_number }}</span>
                  <span class="upcoming-time">{{ formatDateTime(reservation.parking_timestamp) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Features Section -->
        <div class="features-section">
          <h2 class="section-title-simple">Why Park With Us?</h2>
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
  padding-top: 100px;
  min-height: 100vh;
  background-color: #f8fafc;
  font-family: 'Poppins', sans-serif;
  display: flex;
  flex-direction: column;
  position: relative;
}

/* Content */
.content {
  flex: 1;
  position: relative;
  padding: 2rem;
  min-height: calc(100vh - var(--navbar-height, 60px) - var(--footer-height, 80px));
  padding-bottom: 3rem;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

/* Hero Section */
.hero-section {
  background: white;
  border-radius: 1rem;
  padding: 2.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  text-align: left;
}

.welcome-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #f1f5f9;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  color: #64748b;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 1rem;
  border: 1px solid #e2e8f0;
}

.badge-icon {
  font-size: 1.1rem;
}

.hero-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  line-height: 1.3;
}

.highlight-text {
  color: #667eea;
}

.hero-subtitle {
  font-size: 1rem;
  color: #64748b;
  margin: 0 0 1.5rem 0;
}

/* CTA Button */
.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  background: #667eea;
  color: white;
  text-decoration: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.cta-button:hover {
  background: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-icon {
  font-size: 1.25rem;
}

.btn-arrow {
  width: 1.25rem;
  height: 1.25rem;
  transition: transform 0.3s ease;
}

.cta-button:hover .btn-arrow {
  transform: translateX(4px);
}

/* Active Reservations Section */
.active-reservations-section {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.pulse-dot {
  width: 0.75rem;
  height: 0.75rem;
  background: white;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.5;
    transform: scale(1.2);
  }
}

.active-count {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
}

/* Reservation Cards */
.reservations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.reservation-card {
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
}

.reservation-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.card-header-ribbon {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  padding: 0.5rem;
  text-align: center;
}

.ribbon-badge {
  color: white;
  font-weight: 700;
  font-size: 0.75rem;
  letter-spacing: 1px;
}

.card-content {
  padding: 1.5rem;
}

.location-section {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f1f5f9;
}

.location-icon {
  width: 3rem;
  height: 3rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.location-icon svg {
  width: 1.5rem;
  height: 1.5rem;
  color: white;
}

.location-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
}

.spot-number {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-label {
  font-size: 0.75rem;
  color: #94a3b8;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 0.95rem;
  color: #1e293b;
  font-weight: 600;
}

.detail-value.duration {
  color: #10b981;
  font-size: 1.1rem;
}

.release-button {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.release-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.button-icon {
  width: 1.25rem;
  height: 1.25rem;
}

/* Upcoming Reservations Section */
.upcoming-reservations-section {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.section-title-simple {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.upcoming-count {
  background: #dbeafe;
  color: #1e40af;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
}

.upcoming-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.upcoming-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.25rem;
  transition: all 0.3s ease;
}

.upcoming-card:hover {
  background: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.upcoming-badge {
  display: inline-block;
  background: #dbeafe;
  color: #1e40af;
  padding: 0.25rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.5px;
  margin-bottom: 0.75rem;
}

.upcoming-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.upcoming-location {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.upcoming-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
}

.upcoming-vehicle {
  color: #475569;
  font-weight: 500;
}

.upcoming-time {
  color: #64748b;
}

/* Features Section */
.features-section {
  background: white;
  border-radius: 1rem;
  padding: 2.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.feature-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #cbd5e1;
}

.feature-icon {
  width: 3.5rem;
  height: 3.5rem;
  margin: 0 auto 1rem;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon {
  transform: scale(1.05);
}

.feature-icon svg {
  width: 1.75rem;
  height: 1.75rem;
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
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.feature-description {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
  line-height: 1.6;
}

/* Responsive */
@media (max-width: 968px) {
  .content {
    padding: 1.5rem;
  }

  .hero-section {
    padding: 2rem;
  }

  .hero-title {
    font-size: 1.75rem;
  }

  .reservations-grid {
    grid-template-columns: 1fr;
  }

  .upcoming-grid {
    grid-template-columns: 1fr;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .content {
    padding: 1rem;
  }

  .hero-section {
    padding: 1.5rem;
  }

  .hero-title {
    font-size: 1.5rem;
  }

  .active-reservations-section,
  .upcoming-reservations-section,
  .features-section {
    padding: 1.5rem;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .section-title {
    font-size: 1.25rem;
  }

  .details-grid {
    grid-template-columns: 1fr;
  }
}
</style>