<template>
  <div class="parking-history-component">
    <!-- Header Section -->
    <!-- <div class="history-header">
      <h2 class="history-title">All Users Parking History</h2>
      <p class="history-subtitle">Complete record of all parking reservations and transactions</p>
    </div> -->

    <!-- Error State -->
    <div v-if="error" class="alert-error">
      <span class="alert-icon">⚠️</span>
      <span>{{ error }}</span>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="loading-text">Loading parking history...</p>
    </div>

    <!-- Table Section -->
    <div v-else class="table-card">
      <div class="table-wrapper">
        <table class="history-table">
          <thead>
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
              <td><span class="id-badge">{{ res.id }}</span></td>
              <td class="user-cell">{{ res.user_name || `User #${res.user_id}` }}</td>
              <td class="location-cell">{{ res.lot_name || "—" }}</td>
              <td><span class="spot-badge">{{ res.spot_id }}</span></td>
              <td class="vehicle-cell">{{ res.vehicle_number }}</td>
              <td class="time-cell">{{ formatDateTime(res.parking_timestamp) }}</td>
              <td class="time-cell">{{ formatDateTime(res.leaving_timestamp) }}</td>
              <td>
                <span :class="[
                  'status-badge',
                  !res.leaving_timestamp 
                    ? (new Date(res.parking_timestamp) > new Date() ? 'status-booked' : 'status-active')
                    : 'status-complete'
                ]">
                  {{ res.leaving_timestamp
                     ? "Complete" 
                     : (new Date(res.parking_timestamp) > new Date()
                        ? "Booked"
                        : "Active"                        
                      ) }}
                </span>
              </td>
              <td class="amount-cell">
                <span v-if="res.amount_paid" class="amount-text">₹{{ res.amount_paid }}</span>
                <span v-else class="text-muted">—</span>
                <button
                  v-if="res.amount_paid"
                  class="btn-breakdown"
                  @click="openBreakdownModal(res)"
                  title="View Breakdown"
                >
                  💰
                </button>
              </td>
            </tr>
            <tr v-if="reservations.length === 0">
              <td colspan="9" class="empty-state">
                <div class="empty-content">
                  <p class="empty-text">No reservations found.</p>
                  <p class="empty-subtext">Parking history will appear here once users make reservations.</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Breakdown Modal -->
    <div v-if="selectedReservation" class="modal-overlay" @click.self="closeBreakdownModal">
      <div class="modal-container">
        <div class="modal-header">
          <div>
            <h5 class="modal-title">Payment Breakdown</h5>
            <p class="modal-subtitle">Reservation ID: {{ selectedReservation.id }}</p>
          </div>
          <button type="button" class="btn-close" @click="closeBreakdownModal">×</button>
        </div>
        <div class="modal-body">
          <div class="breakdown-grid">
            <div class="breakdown-item">
              <span class="breakdown-label">Parking Time:</span>
              <span class="breakdown-value">{{ formatDateTime(selectedReservation?.parking_timestamp) || "—" }}</span>
            </div>
            <div class="breakdown-item">
              <span class="breakdown-label">Leaving Time:</span>
              <span class="breakdown-value">{{ formatDateTime(selectedReservation?.leaving_timestamp) || "—" }}</span>
            </div>
            <div class="breakdown-item">
              <span class="breakdown-label">Duration:</span>
              <span class="breakdown-value">{{ selectedReservation?.duration || "—" }}</span>
            </div>
            <div class="breakdown-item">
              <span class="breakdown-label">Price Per Hour:</span>
              <span class="breakdown-value">₹{{ selectedReservation?.price || "—" }}</span>
            </div>
            <div class="breakdown-item highlight">
              <span class="breakdown-label">Amount Paid:</span>
              <span class="breakdown-value amount">₹{{ selectedReservation?.amount_paid }}</span>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn-secondary" @click="closeBreakdownModal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Component Container */
.parking-history-component {
  font-family: 'Poppins', sans-serif;
}

/* Header Section */
.history-header {
  margin-bottom: 2rem;
}

.history-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 0.5rem 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.history-title::before {
  content: '';
  width: 4px;
  height: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
}

.history-subtitle {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
  padding-left: 1rem;
}

/* Alert Error */
.alert-error {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.25rem;
  background: #fee2e2;
  border: 1px solid #fecaca;
  border-radius: 0.5rem;
  color: #991b1b;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

.alert-icon {
  font-size: 1.25rem;
}

/* Loading State */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  gap: 1rem;
}

.loading-text {
  color: #64748b;
  font-size: 0.95rem;
  margin: 0;
}

/* Table Card */
.table-card {
  background: white;
  border-radius: 0.5rem;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.table-wrapper {
  overflow-x: auto;
}

/* Table Styles */
.history-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

.history-table thead {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.history-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: white;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.history-table tbody tr {
  border-bottom: 1px solid #f1f5f9;
  transition: background-color 0.2s ease;
}

.history-table tbody tr:hover {
  background-color: #f8fafc;
}

.history-table tbody tr:last-child {
  border-bottom: none;
}

.history-table td {
  padding: 1rem;
  color: #334155;
  vertical-align: middle;
}

/* Table Cell Styling */
.id-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #f1f5f9;
  color: #475569;
  border-radius: 0.375rem;
  font-weight: 500;
  font-size: 0.8rem;
}

.spot-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #dbeafe;
  color: #1e40af;
  border-radius: 0.375rem;
  font-weight: 600;
  font-size: 0.8rem;
}

.user-cell {
  font-weight: 500;
  color: #1e293b;
}

.location-cell {
  color: #475569;
}

.vehicle-cell {
  font-weight: 500;
  color: #0f172a;
  font-family: 'Courier New', monospace;
}

.time-cell {
  color: #64748b;
  font-size: 0.8rem;
  white-space: nowrap;
}

.amount-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.amount-text {
  font-weight: 600;
  color: #059669;
  font-size: 0.9rem;
}

/* Status Badges */
.status-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 0.375rem;
  font-weight: 500;
  font-size: 0.75rem;
  text-transform: capitalize;
}

.status-active {
  background: #d1fae5;
  color: #065f46;
}

.status-complete {
  background: #e2e8f0;
  color: #475569;
}

.status-booked {
  background: #dbeafe;
  color: #1e40af;
}

/* Breakdown Button */
.btn-breakdown {
  padding: 0.25rem 0.5rem;
  background: #fef3c7;
  border: 1px solid #fde68a;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.85rem;
}

.btn-breakdown:hover {
  background: #fde68a;
  transform: scale(1.1);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem 2rem !important;
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.empty-text {
  color: #64748b;
  font-size: 1rem;
  font-weight: 500;
  margin: 0;
}

.empty-subtext {
  color: #94a3b8;
  font-size: 0.85rem;
  margin: 0;
}

.text-muted {
  color: #94a3b8;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
  padding: 1rem;
}

.modal-container {
  background: white;
  border-radius: 1rem;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
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

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #94a3b8;
  cursor: pointer;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.375rem;
  transition: all 0.2s ease;
}

.btn-close:hover {
  background: #f1f5f9;
  color: #475569;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: flex-end;
}

.btn-secondary {
  padding: 0.5rem 1.25rem;
  background: #f1f5f9;
  color: #475569;
  border: none;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: #e2e8f0;
}

/* Breakdown Grid */
.breakdown-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.breakdown-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
}

.breakdown-item.highlight {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border-color: #667eea;
}

.breakdown-label {
  font-weight: 500;
  color: #475569;
  font-size: 0.9rem;
}

.breakdown-value {
  font-weight: 600;
  color: #1e293b;
  font-size: 0.95rem;
}

.breakdown-value.amount {
  color: #059669;
  font-size: 1.1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .history-title {
    font-size: 1.25rem;
  }

  .history-subtitle {
    font-size: 0.85rem;
  }

  .history-table {
    font-size: 0.75rem;
  }

  .history-table th,
  .history-table td {
    padding: 0.75rem 0.5rem;
  }

  .amount-cell {
    flex-direction: column;
    align-items: flex-start;
  }

  .breakdown-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .modal-container {
    max-width: 95%;
  }
}
</style>

<script setup>
import { ref, onMounted, nextTick } from "vue"
import reservationService from "@/services/reservationService"
import { useToast } from "vue-toastification";

const toast = useToast();

const reservations = ref([])
const loading = ref(false)
const error = ref("")

const selectedReservation = ref(null)

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
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to load reservations"
  } finally {
    loading.value = false
  }
}

function openBreakdownModal(res) {
  selectedReservation.value = res
}

function closeBreakdownModal() {
  selectedReservation.value = null
}

onMounted(load_reservations)
</script>