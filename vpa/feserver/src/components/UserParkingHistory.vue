<script setup>
import { ref, onMounted } from "vue"
import reservationService from "@/services/reservationService" 
import { useAuthStore } from "@/stores/auth"

const authStore = useAuthStore()
const userId = authStore.user?.id

const reservations = ref([])
const loading = ref(false)
const error = ref("")


function formatDateTime(timestamp) {
  if (!timestamp) return '—'
  const date = new Date(timestamp)
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  })
}

async function cancelReservation(reservationId) {
  if (confirm("Are you sure you want to cancel this reservation?")) {
    try {
      await reservationService.cancelReservation(reservationId)
      alert("Reservation cancelled successfully.")
      load_reservations()
    } catch (err) {
      alert("Failed to cancel reservation.")
    }
  }
}

async function releaseReservation(reservationId) {
  if (confirm("Release this spot now?")) {
    try {
      await reservationService.completeReservation(reservationId)
      alert("Spot released successfully.")
      load_reservations()
    } catch (err) {
      alert("Failed to release spot.")
    }
  }
}

async function load_reservations (){
  if (!userId) {
    error.value = "User ID not found"
    return
  }

  loading.value = true
  try {
    const res = await reservationService.getUserReservations()
    reservations.value = res.data
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to load history"
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  load_reservations()
})

</script>

<template>
  <div class="dashboard">

    <main class="content container my-5">
      <h2 class="mb-4 text-primary">Your Parking History (User Id {{ userId }})</h2>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else>
        <div class="card shadow-sm">
          <div class="card-body">
            <table class="table table-hover align-middle">
              <thead class="table-dark">
                <tr>
                  <th scope="col">ID</th>
                  <th scope="col">Lot Location</th>
                  <th scope="col">Spot ID</th>
                  <th scope="col">Vehicle</th>
                  <th scope="col">Start Time</th>
                  <th scope="col">End Time</th>
                  <th scope="col">Status</th>
                  <th scope="col">Actions</th>
                  <th col scope="col">Amount Paid</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="res in reservations" :key="res.id">
                  <td>{{ res.id }}</td>
                  <td>{{ res.spot?.lot?.prime_location_name || '—' }}</td>
                  <td>{{ res.spot_id || '—' }}</td>
                  <td>{{ res.vehicle_number || '—' }}</td>
                  <td>{{ formatDateTime(res.parking_timestamp) }}</td>
                  <td>{{ formatDateTime(res.leaving_timestamp) || '-' }}</td>
                  <td>
                    <span :class="res.spot?.status === 'O' ? 'badge bg-success' : 'badge bg-secondary'">
                        {{ res.spot?.status === 'O' ? 'Active' : 'Inactive' }}
                    </span>
                   </td>
                  <td>
                  <!-- Cancel Reservation -->
                  <button
                    v-if="new Date(res.parking_timestamp) > new Date()" 
                    class="btn btn-sm btn-outline-warning me-2"
                    @click="cancelReservation(res.id)"
                  >
                    Cancel Reservation
                  </button>

                  <!-- Release Spot -->
                  <button
                    v-else-if="!res.leaving_timestamp"
                    class="btn btn-sm btn-outline-danger"
                    @click="releaseReservation(res.id)"
                  >
                    Release Spot
                  </button>
                </td>
                <td>{{ res.amount_paid ? `₹${res.amount_paid}` : '-' }}</td>

                </tr>
                <tr v-if="reservations.length === 0">
                  <td colspan="7" class="text-center text-muted">
                    No reservations found.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>

  </div>
</template>

<style scoped>

</style>