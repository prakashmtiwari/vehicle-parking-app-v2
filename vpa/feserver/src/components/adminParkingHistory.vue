<template>
  <div class="dashboard">
    <main class="content container my-5">
      <h2 class="mb-4 text-custom">All Users Parking History</h2>

      <div v-if="error" class="alert alert-danger">{{ error }}</div>

      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else>
        <div class="card shadow-sm">
          <div class="card-body custom-outline">
            <table class="table table-hover align-middle table-responsive table-sm">
              <thead class="table-head">
                <tr>
                  <th>ID</th>
                  <th>User</th>
                  <th>Lot Location</th>
                  <th>Spot ID</th>
                  <th>Vehicle</th>
                  <th>Start Time</th>
                  <th>End Time</th>
                  <th>Status</th>
                  <th>Amount Paid</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="res in reservations" :key="res.id">
                  <td>{{ res.id }}</td>
                  <td>{{ res.user_name || `User #${res.user_id}` }}</td>
                  <td>{{ res.lot_name || "—" }}</td>
                  <td>{{ res.spot_id }}</td>
                  <td>{{ res.vehicle_number }}</td>
                  <td>{{ formatDateTime(res.parking_timestamp) }}</td>
                  <td>{{ formatDateTime(res.leaving_timestamp) }}</td>
                  <td>
                    <span :class="!res.leaving_timestamp ? 'badge bg-success' : 'badge bg-secondary'">
                      {{ !res.leaving_timestamp ? "Active" : "Inactive" }}
                    </span>
                  </td>
                  <td>
                    {{ res.amount_paid ? `₹${res.amount_paid}` : "-" }}
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
                  <td colspan="10" class="text-center text-muted">
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
            <p><strong>Price Per Hour:</strong> {{ `₹${selectedReservation?.price}` || "-" }}</p>
            <p><strong>Amount Paid:</strong> ₹{{ selectedReservation?.amount_paid }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeBreakdownModal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>  

.text-custom {
  color: rgb(218, 47, 218);
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  font-weight: bold;
  text-align: center;
}

.table-head {
  background-color: rgb(245, 99, 245);
  color: white;
}

.custom-outline {
  border: 1px solid rgb(218, 47, 218); 
}

.custom-outline:focus {
  outline: none;
  border-color: rgb(245, 99, 245); 
  box-shadow: 0 0 4px rgb(245, 99, 245);
}

</style>



<script setup>
import { ref, onMounted, nextTick } from "vue"
import reservationService from "@/services/reservationService"
import { Tooltip, Modal } from "bootstrap"
import { useToast } from "vue-toastification";


const toast = useToast();


const reservations = ref([])
const loading = ref(false)
const error = ref("")

const selectedReservation = ref(null)
const breakdownModalRef = ref(null)
let breakdownModalInstance = null

function formatDateTime(timestamp) {
  if (!timestamp) return "—"
  const date = new Date(timestamp)
  return date.toLocaleString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true
  })
}

async function load_reservations() {
  loading.value = true
  try {
    const res = await reservationService.getAllReservations()
    reservations.value = res.data
    await nextTick()
    initializeTooltips()
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to load reservations"
  } finally {
    loading.value = false
  }
}

function initializeTooltips() {
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
  tooltipTriggerList.forEach(el => new Tooltip(el))
}

async function releaseReservation(reservationId) {
  if (confirm("Release this spot now?")) {
    try {
      await reservationService.completeReservation(reservationId)
      toast.success("Spot released successfully.")
      load_reservations()
    } catch (err) {
      toast.error("Failed to release spot.")
    }
  }
}

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

// Modal functions
function openBreakdownModal(res) {
  selectedReservation.value = res
  breakdownModalInstance = new Modal(breakdownModalRef.value)
  breakdownModalInstance.show()
}

function closeBreakdownModal() {
  if (breakdownModalInstance) breakdownModalInstance.hide()
}

onMounted(load_reservations)
</script>
