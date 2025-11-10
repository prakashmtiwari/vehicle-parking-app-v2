<script setup>
import { ref, onMounted } from "vue"
import reservationService from "@/services/reservationService" 
import ExportButton from "@/components/ExportButton.vue"
import { useAuthStore } from "@/stores/auth"
import { Tooltip, Modal } from "bootstrap"
import { useToast } from "vue-toastification";


const toast = useToast();
const authStore = useAuthStore()
const userId = authStore.user?.id

const reservations = ref([])
const loading = ref(false)
const error = ref("")

const selectedReservation = ref(null)
const selectedReservationID = ref(null)
const breakdownModalRef = ref(null)
const showPaymentModal = ref(false)
const parkingCost = ref(0)

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


// function initializeTooltips() {
//   const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
//   tooltipTriggerList.forEach(el => new Tooltip(el))
// }


// async function triggerExport() {
//   const res = await reservationService.exportUserHistory()
//   if (res.ok) toast.info("Export started! You’ll get an email when it’s ready.");
// }


async function cancelReservation(reservationId) {
  if (confirm("Are you sure you want to cancel this reservation?")) {
    try {
      await reservationService.cancelReservation(reservationId)
      toast.info("Reservation cancelled successfully.")
      load_reservations()
    } catch (err) {
      toast.error("Failed to cancel reservation.")
    }
  }
}

async function confirmPayment() {
  try {
    //  call your backend payment/complete endpoint
    await reservationService.completeReservation(selectedReservationID.value)
    toast.success('Spot released successfully.')
    showPaymentModal.value = false
    load_reservations()
  } catch (err) {
    toast.error('Failed to release spot.')
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


async function openPaymentModal(res_id) {
  try{
    selectedReservationID.value = res_id
    const res = await reservationService.getParkingAmount(res_id)
    console.log('Sucessfully completed the parking cost')  
    parkingCost.value = res.data.parking_cost
    console.log(parkingCost)
  }
  catch (err){
    toast.error('Error Calculating the amount to be paid')
  }
  finally{
  showPaymentModal.value = true
  }
}


// Load user reservations
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
      
      <h2 class="mb-4 custom-text">My Parking History</h2>

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
          <div class="card-body custom-outline">
            <table class="table table-hover table-sm align-middle">
              <thead>
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
                    <span :class="(!res.leaving_timestamp) ? 'badge bg-success' : 'badge bg-primary'">
                        {{ res.leaving_timestamp 
                            ? 'Complete' 
                            : (new Date(res.parking_timestamp) > new Date() 
                                ? 'Booked' 
                                : 'Active') 
                        }}                    
                    </span>
                   </td>
                  <td>
                  <!-- Cancel Reservation -->
                  <div v-if="!res.leaving_timestamp">
                  <button
                    v-if="new Date(res.parking_timestamp) > new Date()" 
                    class="btn btn-sm btn-outline-warning me-2"
                    @click="cancelReservation(res.id)"
                  >
                    Cancel Reservation
                  </button>

                  <!-- Release Spot -->
                  <button v-else class="btn btn-warning btn-sm" @click="openPaymentModal(res.id)">
                    Release Spot
                  </button>
                  </div>
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
      <div class="modal-dialog custom-outline">
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
  <div class="modal-dialog  modal-dialog-centered">
    <div class="modal-content custom-outline">
      <div class="modal-header">
        <h5 class="modal-title">Confirm Payment</h5>
        <button type="button" class="btn-close" @click="showPaymentModal = false"></button>
      </div>
      <div class="modal-body">
        <p>
          Are you sure you want to release this spot?<br>
          Payment Amount: <strong>₹{{ parkingCost?.toFixed(2) || '0.00' }}</strong>
        </p>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="showPaymentModal = false">Cancel</button>
        <button class="btn btn-success" @click="confirmPayment()">Confirm & Pay</button>
      </div>
    </div>
  </div>
</div>


  </div>
</template>

<style scoped>
.custom-text {
  color: rgb(56, 53, 206, 0.74);
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  font-weight: bold;
  text-align: center;
}

.custom-outline {
  border: 1px solid rgb(56, 53, 206, 0.74); 
  margin-bottom: 20px;
}

.custom-outline:focus {
  outline: none;
  border-color: rgb(56, 53, 206, 0.74); 
  box-shadow: 0 0 4px rgb(56, 53, 206, 0.74);
}

.modal {
  background: rgba(0, 0, 0, 0.5);
  transition: opacity 0.3s ease;
}

.modal.show .modal-dialog {
  transform: scale(1.02);
}

</style>