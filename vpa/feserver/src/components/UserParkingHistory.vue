<script setup>
import { ref, onMounted } from "vue"
import reservationService from "@/services/reservationService" 
import ExportButton from "@/components/ExportButton.vue"
import { useAuthStore } from "@/stores/auth"
import { Tooltip, Modal } from "bootstrap"



const authStore = useAuthStore()
const userId = authStore.user?.id

const reservations = ref([])
const loading = ref(false)
const error = ref("")

const selectedReservation = ref(null)
const breakdownModalRef = ref(null)
let breakdownModalInstance = null

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


function initializeTooltips() {
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
  tooltipTriggerList.forEach(el => new Tooltip(el))
}


async function triggerExport() {
  const res = await reservationService.exportUserHistory()
  if (res.ok) alert("Export started! You’ll get an email when it’s ready.");
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
      initializeTooltips()
    } catch (err) {
      alert("Failed to release spot.")
    }
  }
}

// Modal functions
function openBreakdownModal(res) {
  selectedReservation.value = res
  breakdownModalInstance = new Modal(breakdownModalRef.value)
  breakdownModalInstance.show()
}

function closeBreakdownModal() {
  if (breakdownModalInstance) breakdownModalInstance.hide()
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

      <!-- Export Button aligned to the right -->
      <div class="mb-3 text-end"> 
        <ExportButton />
      </div>


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
                  <td>{{ res.vehicle_number || '—' }}</td>
                  <td>{{ formatDateTime(res.parking_timestamp) }}</td>
                  <td>{{ formatDateTime(res.leaving_timestamp) || '-' }}</td>
                  <td>
                    <span :class="(!res.leaving_timestamp) ? 'badge bg-success' : 'badge bg-secondary'">
                        {{ (!res.leaving_timestamp)  ? 'Active' : 'Completed' }}
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
                <td>{{ res.amount_paid ? `₹${res.amount_paid}` : '-' }}
                 <button
                      v-if="res.amount_paid"
                      class="btn btn-sm btn-outline-info ms-2"
                      @click="openBreakdownModal(res)"
                      data-bs-toggle="tooltip"
                      title="View Breakdown"
                    >
                      💰
                    </button>
                </td>

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


    <!-- Breakdown Modal -->
    <div
      class="modal fade"
      id="breakdownModal"
      tabindex="-1"
      aria-labelledby="breakdownModalLabel"
      aria-hidden="true"
      ref="breakdownModalRef"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="breakdownModalLabel">Payment Breakdown</h5>
            <button type="button" class="btn-close" @click="closeBreakdownModal"></button>
          </div>
          <div class="modal-body">
            <p><strong>Parking Time:</strong> {{ `${formatDateTime(selectedReservation?.parking_timestamp)}` || "-" }}</p>
            <p><strong>Leaving Time:</strong> {{ `${formatDateTime(selectedReservation?.leaving_timestamp)}` || "-" }}</p>
            <p><strong>Duration:</strong> {{ `${selectedReservation?.duration}` || "-" }}</p>
            <p><strong>Price Per Hour:</strong> {{  `₹ ${selectedReservation?.spot?.lot?.price || '—'}` }}</p>
            <p><strong>Amount Paid:</strong> ₹{{ ` ${selectedReservation?.amount_paid}` }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeBreakdownModal">Close</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Payment Confirmation Modal -->
<div
  class="modal fade"
  tabindex="-1"
  :class="{ show: showPaymentModal }"
  style="display: block;"
  v-if="showPaymentModal"
>
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">Confirm Payment</h5>
        <button type="button" class="btn-close" @click="showPaymentModal = false"></button>
      </div>
      <div class="modal-body">
        <p>
          Are you sure you want to release this spot?<br>
          Payment Amount: <strong>₹{{ selectedReservation?.amount_paid || 0 }}</strong>
        </p>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="showPaymentModal = false">Cancel</button>
        <button class="btn btn-success" @click="confirmPayment">Confirm & Pay</button>
      </div>
    </div>
  </div>
</div>


  </div>
</template>

<style scoped>

</style>