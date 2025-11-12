<template>
  <div class="parking-lots-page">
    <UserNavbar />

    <main class="content">
      <div class="content-wrapper">
        <!-- Page Header -->
        <div class="page-header">
          <h1 class="page-title">Available Parking Lots</h1>
          <p class="page-subtitle">Find and reserve your perfect parking spot</p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="loading-container">
          <div class="spinner"></div>
          <p class="loading-text">Loading parking lots...</p>
        </div>

        <!-- Parking Lots Grid -->
        <div v-else-if="lots.length > 0" class="lots-grid">
          <div v-for="lot in lots" :key="lot.id" class="lot-card">
            <div class="card-header">
              <h3 class="lot-name">{{ lot.prime_location_name }}</h3>
            </div>

            <div class="card-body">
              <div class="lot-info">
                <div class="info-item">
                  <span class="info-label">Price:</span>
                  <span class="info-value">₹{{ lot.price }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">Total Spots:</span>
                  <span class="info-value">{{ lot.maximum_number_of_spots }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">Occupied:</span>
                  <span class="info-value">{{ lot.spots.filter(s => s.status === 'O').length }} / {{ lot.maximum_number_of_spots }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">Address:</span>
                  <button
                    class="btn-address"
                    @click="viewAddress(lot)"
                    title="View Address"
                  >
                    View Address
                  </button>
                </div>
              </div>
              
              <div class="availability-badge" :class="hasAvailableSpot(lot) ? 'available' : 'unavailable'">
                <span class="badge-dot"></span>
                {{ hasAvailableSpot(lot) ? 'Spots Available' : 'Fully Booked' }}
              </div>

              <button
                class="reserve-btn"
                :class="{ 'disabled': !hasAvailableSpot(lot) }"
                :disabled="!hasAvailableSpot(lot)"
                @click="openReservationModal(lot)"
              >
                <svg v-if="hasAvailableSpot(lot)" class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                {{ hasAvailableSpot(lot) ? 'Reserve Now' : 'No Spots Available' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <div class="empty-icon">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/>
            </svg>
          </div>
          <h3 class="empty-title">No Parking Lots Available</h3>
          <p class="empty-description">Check back later for available parking spots</p>
        </div>
      </div>
    </main>

    <!-- Address Modal -->
    <div v-if="showAddressModal" class="modal-overlay" @click.self="closeAddressModal">
      <div class="modal-container modal-small">
        <div class="modal-header">
          <div>
            <h5 class="modal-title">Parking Lot Address</h5>
            <p class="modal-subtitle">{{ selectedLotName }}</p>
          </div>
          <button type="button" class="close-btn" @click="closeAddressModal">×</button>
        </div>
        <div class="modal-body">
          <div class="address-content">
            <p>{{ selectedLotAddress }}</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-secondary" @click="closeAddressModal">Close</button>
        </div>
      </div>
    </div>

    <!-- Reservation Modal -->
    <div v-if="showReservationModal" class="modal-overlay" @click="closeReservationModal">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">Reserve Parking Spot</h3>
          <button class="close-btn" @click="closeReservationModal">
            <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <div class="modal-body">
          <div class="location-badge">
            <svg class="badge-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
            </svg>
            {{ selectedLot?.prime_location_name }}
          </div>

          <form @submit.prevent="confirmReservation" class="reservation-form">
            <FormatVehicleNumber v-model="vehicleNumber" />

            <div class="form-group">
              <label class="form-label">Reservation Start Time</label>
              <input 
                type="datetime-local" 
                v-model="reservationTime" 
                class="form-input" 
                required 
              />
            </div>

            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="closeReservationModal">
                Cancel
              </button>
              <button type="submit" class="btn-primary" :disabled="creating">
                <span v-if="!creating">Confirm Reservation</span>
                <span v-else class="btn-loading">
                  <span class="loading-spinner"></span>
                  Reserving...
                </span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <UserFooter />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import parkingLotService from "@/services/parkingLotService"
import reservationService from "@/services/reservationService"
import UserNavbar from '@/components/UserNavbar.vue'
import UserFooter from '@/components/UserFooter.vue'
import FormatVehicleNumber from "@/components/formatVehicleNumber.vue"
import { useToast } from "vue-toastification";

const toast = useToast();

const lots = ref([])
const loading = ref(false)
const error = ref("")

// Reservation Modal
const showReservationModal = ref(false)
const selectedLot = ref(null)
const vehicleNumber = ref("")
const reservationTime = ref("")
const creating = ref(false)

// Address Modal
const showAddressModal = ref(false)
const selectedLotName = ref("")
const selectedLotAddress = ref("")

async function loadLots() {
  loading.value = true
  try {
    const res = await parkingLotService.getLotsWithSpots()
    lots.value = res.data
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to load parking lots"
  } finally {
    loading.value = false
  }
}

function hasAvailableSpot(lot) {
  return lot.spots.some(s => s.status === "A")
}

function viewAddress(lot) {
  selectedLotName.value = lot.prime_location_name
  selectedLotAddress.value = lot.address
  showAddressModal.value = true
}

function closeAddressModal() {
  showAddressModal.value = false
  selectedLotName.value = ""
  selectedLotAddress.value = ""
}

function openReservationModal(lot) {
  selectedLot.value = lot
  vehicleNumber.value = ""
  const now = new Date()
  now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
  reservationTime.value = now.toISOString().slice(0,16)
  showReservationModal.value = true
}

function closeReservationModal() {
  showReservationModal.value = false
  selectedLot.value = null
  vehicleNumber.value = ""
  reservationTime.value = ""
}

async function confirmReservation() {
  if (!selectedLot.value) return
  
  // Trim and validate vehicle number
  const trimmedVehicleNumber = vehicleNumber.value?.trim()
  
  if (!trimmedVehicleNumber) {
    toast.error("Please enter a valid vehicle number!")
    return
  }
  
  console.log('Vehicle Number:', trimmedVehicleNumber)
  
  creating.value = true

  try {
    const user_reservations = await reservationService.getUserReservations()
    const hasActive = user_reservations.data.some(r => 
      !r.leaving_timestamp && 
      new Date(r.parking_timestamp) <= new Date() && 
      r.vehicle_number === trimmedVehicleNumber
    )
    
    if (hasActive) {  
      toast.error("This vehicle already has an active reservation!")
      creating.value = false
      return
    }

    const availableSpot = selectedLot.value.spots.find(s => s.status === "A")
    if (!availableSpot) {
      toast.info("No available spots!")
      creating.value = false
      return
    }
    
    const payload = {
      spot_id: availableSpot.id,
      vehicle_number: trimmedVehicleNumber,
      parking_timestamp: reservationTime.value
    }
    
    console.log('Payload being sent:', payload)

    await reservationService.createReservation(payload)
    toast.success("Reservation successful!")

    closeReservationModal()
    loadLots()
  } catch (err) {
    console.error(err)
    toast.error(err.response?.data?.message || err.message || "Failed to reserve spot")
  } finally {
    creating.value = false
  }
}

onMounted(loadLots)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

.parking-lots-page {
  padding-top: 100px;
  min-height: 100vh;
  background-color: #f8fafc;
  font-family: 'Poppins', sans-serif;
  display: flex;
  flex-direction: column;
}

.content {
  flex: 1;
  padding: 2rem;
  min-height: calc(100vh - var(--navbar-height, 60px) - var(--footer-height, 80px));
  padding-bottom: 3rem;
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
}

/* Page Header */
.page-header {
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.page-subtitle {
  font-size: 1rem;
  color: #64748b;
  margin: 0;
}

/* Loading State */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 1rem;
  border: 1px solid #e2e8f0;
}

.spinner {
  width: 3rem;
  height: 3rem;
  border: 3px solid #e2e8f0;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-text {
  margin-top: 1rem;
  color: #64748b;
  font-size: 0.95rem;
}

/* Parking Lots Grid */
.lots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;
}

.lot-card {
  background: white;
  border-radius: 1rem;
  border: 1px solid #e2e8f0;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.lot-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  border-color: #cbd5e1;
}

.card-header {
  background: #667eea;
  padding: 1.25rem 1.5rem;
}

.lot-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: white;
  margin: 0;
}

.card-body {
  padding: 1.5rem;
}

.lot-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-label {
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 500;
}

.info-value {
  font-size: 0.95rem;
  color: #1e293b;
  font-weight: 600;
}

.btn-address {
  padding: 0.4rem 0.875rem;
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Poppins', sans-serif;
}

.btn-address:hover {
  background: #e2e8f0;
  border-color: #cbd5e1;
  transform: translateY(-1px);
}

.availability-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
  margin-bottom: 1.25rem;
}

.availability-badge.available {
  background: #dcfce7;
  color: #15803d;
}

.availability-badge.unavailable {
  background: #fee2e2;
  color: #991b1b;
}

.badge-dot {
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  background: currentColor;
}

.reserve-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.reserve-btn:hover:not(.disabled) {
  background: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.reserve-btn.disabled {
  background: #e2e8f0;
  color: #94a3b8;
  cursor: not-allowed;
}

.btn-icon {
  width: 1.25rem;
  height: 1.25rem;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 1rem;
  border: 1px solid #e2e8f0;
}

.empty-icon {
  width: 4rem;
  height: 4rem;
  margin: 0 auto 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  border-radius: 50%;
}

.empty-icon svg {
  width: 2rem;
  height: 2rem;
  color: #94a3b8;
}

.empty-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
}

.empty-description {
  font-size: 0.95rem;
  color: #64748b;
  margin: 0;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-container {
  background: white;
  border-radius: 1rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
  animation: modalSlideIn 0.3s ease-out;
}

.modal-container.modal-small {
  max-width: 450px;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.modal-subtitle {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0.25rem 0 0 0;
}

.close-btn {
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  border-radius: 0.375rem;
  transition: all 0.2s ease;
  font-size: 1.5rem;
}

.close-btn:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.close-btn svg {
  width: 1.25rem;
  height: 1.25rem;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
}

.address-content {
  color: #475569;
  line-height: 1.6;
}

.address-content p {
  margin: 0;
  font-size: 0.95rem;
}

.location-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #ede9fe;
  color: #6d28d9;
  padding: 0.625rem 1rem;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.badge-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.reservation-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1e293b;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  color: #1e293b;
  transition: all 0.2s ease;
  font-family: 'Poppins', sans-serif;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input::placeholder {
  color: #94a3b8;
}

.form-actions {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;
}

.btn-secondary,
.btn-primary {
  flex: 1;
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Poppins', sans-serif;
}

.btn-secondary {
  background: #f1f5f9;
  color: #475569;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

.btn-primary {
  background: #667eea;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #5568d3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-primary:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
  transform: none;
}

.btn-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.loading-spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

/* Responsive */
@media (max-width: 768px) {
  .content {
    padding: 1.5rem;
  }

  .page-title {
    font-size: 1.75rem;
  }

  .lots-grid {
    grid-template-columns: 1fr;
  }

  .modal-container {
    max-width: calc(100% - 2rem);
  }

  .form-actions {
    flex-direction: column;
  }
}

@media (max-width: 640px) {
  .content {
    padding: 1rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .page-subtitle {
    font-size: 0.9rem;
  }

  .modal-header {
    padding: 1.25rem;
  }

  .modal-body {
    padding: 1.25rem;
  }
}
</style>