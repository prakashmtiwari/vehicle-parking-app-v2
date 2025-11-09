<template>
  <UserNavbar />

  <div class="container my-5">
    <h2 class="mb-4 custom-text text-center">All Available Parking Lots</h2>

    <div v-if="loading" class="text-center py-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else class="row g-4">
      <div v-for="lot in lots" :key="lot.id" class="col-md-6 col-lg-4">
        <div class="card custom-outline lot-card h-100 shadow-sm">
          <!-- Header -->
          <div class="card-header text-white text-center">
            <h5 class="mb-0">{{ lot.prime_location_name }}</h5>
          </div>

          <!-- Body -->
          <div class="card-body">
            <p class="card-text">
              <strong>Price:</strong> ₹{{ lot.price }} <br>
              <strong>Maximum Spots:</strong> {{ lot.maximum_number_of_spots }}
            </p>

            <p>
              <strong>Occupied/Reserved Spots:</strong> {{ lot.spots.filter(s => s.status === 'O').length }} /
              {{ lot.maximum_number_of_spots }}
            </p>

            <button
              class="btn btn-success w-100"
              :disabled="!hasAvailableSpot(lot)"
              @click="openReservationModal(lot)"
            >
              Reserve Next Available Spot
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="lots.length === 0 && !loading" class="text-center mt-4">
      <p>No parking lots available.</p>
    </div>
  </div>

  <!-- Reservation Modal -->
  <div v-if="showReservationModal" class="modal fade show d-block overlay">
    <div class="modal-dialog custom-outline modal-md">
      <div class="modal-content p-3">
        <div class="modal-header">
          <h5 class="modal-title custom-text">Reserve Spot in {{ selectedLot?.prime_location_name }}</h5>
          <button type="button" class="btn-close" @click="closeReservationModal"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="confirmReservation">
            <div class="mb-3">
              <label class="form-label">Vehicle Number</label>
              <input
                type="text"
                v-model="vehicleNumber"
                class="form-control"
                placeholder="Enter your vehicle number"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label">Reservation Start Time</label>
              <input type="datetime-local" v-model="reservationTime" class="form-control" required />
            </div>

            <div class="text-end">
              <button type="button" class="btn btn-light me-2" @click="closeReservationModal">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="creating">
                {{ creating ? "Reserving..." : "Confirm Reservation" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <UserFooter />
</template>

<script setup>
import { ref, onMounted } from "vue"
import parkingLotService from "@/services/parkingLotService"
import reservationService from "@/services/reservationService"
import UserNavbar from '@/components/UserNavbar.vue'
import UserFooter from '@/components/UserFooter.vue'
import { useToast } from "vue-toastification";


const toast = useToast();


const lots = ref([])
const loading = ref(false)
const error = ref("")

const showReservationModal = ref(false)
const selectedLot = ref(null)
const vehicleNumber = ref("")
const reservationTime = ref("")
const creating = ref(false)

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

function openReservationModal(lot) {
  selectedLot.value = lot
  vehicleNumber.value = ""
  const now = new Date()
  now.setMinutes(now.getMinutes() - now.getTimezoneOffset()) // adjust to local
  reservationTime.value = now.toISOString().slice(0,16)
  showReservationModal.value = true
}

function closeReservationModal() {
  showReservationModal.value = false
  selectedLot.value = null
}

async function confirmReservation() {
  if (!selectedLot.value) return
  creating.value = true

  try {
    //check if the user already has a reservation with an active reservation
    const user_reservations = await reservationService.getUserReservations()
    const hasActive = user_reservations.data.some(r => !r.leaving_timestamp && new Date(r.parking_timestamp) <= new Date())
    if (hasActive) {  
      toast.error("This vehicle already has an active reservation!")
      creating.value = false
      return
    }

    // find next available spot
    const availableSpot = selectedLot.value.spots.find(s => s.status === "A")
    if (!availableSpot) {
      toast.info("No available spots!")
      return
    }
    
    console.log("Reserving spot:", availableSpot.id, vehicleNumber.value, reservationTime.value)
    const payload = {
      spot_id: availableSpot.id,
      vehicle_number: vehicleNumber.value,
      parking_timestamp: reservationTime.value
    }

    await reservationService.createReservation(payload)
    toast.success("Reservation successful!")

    closeReservationModal()
    loadLots() // refresh spots
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
.lot-card {
  border-radius: 0.75rem;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.lot-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 0.75rem 1.5rem rgba(0,0,0,0.15);
}

.overlay {
  background: rgba(0,0,0,0.5);
  position: fixed;
  inset: 0;
  z-index: 1050;
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  border-radius: 0.5rem;
}

.custom-text{
  color: rgb(218, 47, 218);
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  font-weight: bold;
  text-align: center;
}

.custom-outline {
  border: 1px solid rgb(218, 47, 218); 
  margin-bottom: 20px;
 
}

.custom-outline:focus {
  outline: none;
  border-color: rgb(245, 99, 245); 
  box-shadow: 0 0 4px rgb(245, 99, 245);
}

.card-header{
  background-color: #5C3E94;
}

.container{
padding-bottom: 80px;
}
</style>
