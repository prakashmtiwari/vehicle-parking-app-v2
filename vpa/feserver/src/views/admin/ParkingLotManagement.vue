<template>
  <div class="parking-lot-page">
    <AdminNavbar />

    <main class="content-wrapper">
      <div class="admin-container">
        <div class="admin-card">
          <!-- Header Section -->
          <div class="card-header">
            <h2 class="card-title">Parking Lot Management</h2>
            <p class="card-subtitle">Manage and monitor all parking lots in your system.</p>
          </div>

          <!-- Add Button Section -->
          <div class="action-section">
            <router-link to="/parking-lots/new" class="btn-add">
              <span class="btn-icon">+</span>
              Add Parking Lot
            </router-link>
          </div>

          <!-- Table Section -->
          <div class="table-container">
            <div v-if="loading" class="loading-state">
              <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <p class="loading-text">Loading parking lots...</p>
            </div>

            <div v-else>
              <div class="table-wrapper">
                <table class="custom-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Prime Location</th>
                      <th>Price</th>
                      <th>Pin Code</th>
                      <th>Max Spots</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="lot in lots" :key="lot.id">
                      <td><span class="id-badge">{{ lot.id }}</span></td>
                      <td class="location-cell">{{ lot.prime_location_name }}</td>
                      <td class="price-cell">₹{{ lot.price }}</td>
                      <td>{{ lot.pin_code }}</td>
                      <td><span class="spots-badge">{{ lot.maximum_number_of_spots }}</span></td>
                      <td>
                        <div class="action-buttons">
                          <router-link
                            :to="`/parking-lots/${lot.id}/edit`"
                            class="btn-action btn-edit"
                            title="Edit"
                          >Edit</router-link>
                          <button
                            class="btn-action btn-delete"
                            @click="deleteLot(lot.id)"
                            title="Delete"
                          >Delete</button>
                          <button
                            class="btn-action btn-info"
                            @click="viewSpots(lot.id)"
                            title="View Spots"
                          >Spots</button>
                          <button
                            class="btn-action btn-secondary"
                            @click="viewAddress(lot.id)"
                            title="View Address"
                          >Address</button>
                        </div>
                      </td>
                    </tr>
                    <tr v-if="lots.length === 0">
                      <td colspan="6" class="empty-state">
                        <div class="empty-content">
                          <p class="empty-text">No parking lots available.</p>
                          <p class="empty-subtext">Create your first parking lot to get started.</p>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Spots Modal -->
    <div v-if="selectedLotSpots" class="modal-overlay" @click.self="closeSpotsModal">
      <div class="modal-container">
        <div class="modal-header">
          <div>
            <h5 class="modal-title">Parking Spots</h5>
            <p class="modal-subtitle">Lot ID: {{ selectedLotId }}</p>
          </div>
          <button type="button" class="btn-close" @click="closeSpotsModal">×</button>
        </div>
        <div class="modal-body">
          <div class="table-wrapper">
            <table class="custom-table modal-table">
              <thead>
                <tr>
                  <th>Spot ID</th>
                  <th>Status</th>
                  <th>Vehicle</th>
                  <th>Parking Start Time</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="spot in selectedLotSpots" :key="spot.id">
                  <td><span class="id-badge">{{ spot.id }}</span></td>
                  <td>
                    <span :class="[
                      'status-badge',
                      spot.active_reservation 
                        ? (new Date(spot.active_reservation.parking_timestamp) > new Date() 
                            ? 'status-booked' 
                            : 'status-occupied')
                        : 'status-available'
                    ]">
                      {{ 
                        spot.active_reservation 
                          ? (new Date(spot.active_reservation.parking_timestamp) > new Date() 
                              ? 'Booked' 
                              : 'Occupied')
                          : 'Available' 
                      }}
                    </span>
                  </td>
                  <td>
                    <span v-if="spot.status === 'O'">{{ spot.active_reservation?.vehicle_number || '—' }}</span>
                    <span v-else class="text-muted">—</span>
                  </td>
                  <td>
                    <span v-if="spot.status === 'O'">{{ formatDateTime(spot.active_reservation?.parking_timestamp) || '—' }}</span>
                    <span v-else class="text-muted">—</span>
                  </td>
                </tr>
                <tr v-if="selectedLotSpots.length === 0">
                  <td colspan="4" class="empty-state">
                    <p class="empty-text">No spots found</p>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Address Modal -->
    <div v-if="showAddressModal" class="modal-overlay" @click.self="closeAddressModal">
      <div class="modal-container modal-small">
        <div class="modal-header">
          <div>
            <h5 class="modal-title">Parking Lot Address</h5>
            <p class="modal-subtitle">ID: {{ selectedLotName }}</p>
          </div>
          <button type="button" class="btn-close" @click="closeAddressModal">×</button>
        </div>
        <div class="modal-body">
          <div class="address-content">
            <p>{{ selectedLotAddress }}</p>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-action btn-secondary" @click="closeAddressModal">Close</button>
        </div>
      </div>
    </div>

    <AdminFooter />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue"
import parkingLotService from "@/services/parkingLotService"
import AdminNavbar from '@/components/AdminNavbar.vue'
import AdminFooter from '@/components/AdminFooter.vue'
import { useToast } from "vue-toastification";

const toast = useToast()
const lots = ref([])
const loading = ref(false)
const error = ref("")

const form = reactive({
  id: null,
  prime_location_name: "",
  price: null,
  address: "",
  pin_code: "",
  maximum_number_of_spots: null
})

const showAddressModal = ref(false)
const selectedLotAddress = ref("")
const selectedLotName = ref("")

const selectedLotSpots = ref(null)
const selectedLotId = ref(null)

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

async function loadLots() {
  loading.value = true
  error.value = ""
  try {
    const res = await parkingLotService.getLots()
    lots.value = res.data
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to load lots"
  } finally {
    loading.value = false
  }
}

async function deleteLot(id) {
  if (!confirm("Are you sure you want to delete this parking lot?")) return
  try {
    await parkingLotService.deleteLot(id)
    toast.success("Parking lot deleted successfully.")
    await loadLots()
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to delete lot"
    toast.error(error.value)
  }
}

async function viewSpots(lotId) {
  selectedLotSpots.value = null
  selectedLotId.value = lotId
  try {
    const res = await parkingLotService.getSpots(lotId)
    selectedLotSpots.value = res.data
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to load spots"
    selectedLotSpots.value = []
  }
}

function viewAddress(lotId) {
  const lot = lots.value.find(l => l.id === lotId)
  if (lot) {
    selectedLotAddress.value = lot.address || "No address available"
    selectedLotName.value = lot.id
    showAddressModal.value = true
  } else {
    error.value = "Lot not found"
  }
}

function closeAddressModal() {
  showAddressModal.value = false
  selectedLotAddress.value = ""
  selectedLotName.value = ""
}

function closeSpotsModal() {
  selectedLotSpots.value = null
  selectedLotId.value = null
}

async function releaseSpot(spotId) {
  if (!confirm(`Are you sure you want to free spot ${spotId}?`)) return
  try {
    await parkingLotService.releaseSpot(spotId)
    const spot = selectedLotSpots.value.find(s => s.id === spotId)
    if (spot) {
      spot.status = "E"
      spot.reservation = null
    }
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to release spot"
    toast.error(error.value)
  }
}

onMounted(loadLots)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Global Styles */
.parking-lot-page {
  font-family: 'Poppins', sans-serif;
  min-height: 100vh;
  background-color: #f8fafc;
}

.content-wrapper {
  padding: 2rem;
  min-height: calc(100vh - var(--navbar-height, 60px) - var(--footer-height, 80px));
  padding-bottom: 3rem;
}

.admin-container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

/* Card Styling */
.admin-card {
  background: white;
  border-radius: 1rem;
  padding: 2.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.card-header {
  text-align: left;
  margin-bottom: 2rem;
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 1.5rem;
}

.card-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.card-subtitle {
  font-size: 1rem;
  color: #64748b;
  margin: 0.5rem 0 0 0;
}

/* Action Section */
.action-section {
  margin-bottom: 2rem;
  display: flex;
  justify-content: flex-start;
}

.btn-add {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.btn-add:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  color: white;
}

.btn-icon {
  font-size: 1.2rem;
  font-weight: bold;
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

/* Table Styles */
.table-container {
  margin-top: 1.5rem;
}

.table-wrapper {
  overflow-x: auto;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
}

.custom-table {
  width: 100%;
  border-collapse: collapse;
  background: white;
  font-size: 0.9rem;
}

.custom-table thead {
  background: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
}

.custom-table th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #475569;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.custom-table tbody tr {
  border-bottom: 1px solid #f1f5f9;
  transition: background-color 0.2s ease;
}

.custom-table tbody tr:hover {
  background-color: #f8fafc;
}

.custom-table td {
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
  font-size: 0.85rem;
}

.location-cell {
  font-weight: 500;
  color: #1e293b;
}

.price-cell {
  font-weight: 600;
  color: #059669;
}

.spots-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #dbeafe;
  color: #1e40af;
  border-radius: 0.375rem;
  font-weight: 600;
  font-size: 0.85rem;
}

/* Action Buttons */
.action-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn-action {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 0.375rem;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  display: inline-block;
}

.btn-edit {
  background: #fef3c7;
  color: #92400e;
}

.btn-edit:hover {
  background: #fde68a;
  color: #92400e;
}

.btn-delete {
  background: #fee2e2;
  color: #991b1b;
}

.btn-delete:hover {
  background: #fecaca;
}

.btn-info {
  background: #dbeafe;
  color: #1e40af;
}

.btn-info:hover {
  background: #bfdbfe;
}

.btn-secondary {
  background: #f1f5f9;
  color: #475569;
}

.btn-secondary:hover {
  background: #e2e8f0;
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
  font-size: 0.9rem;
  margin: 0;
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
  max-width: 900px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.modal-small {
  max-width: 500px;
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
  font-size: 0.9rem;
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

.modal-table {
  font-size: 0.85rem;
}

/* Status Badges */
.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 0.375rem;
  font-weight: 500;
  font-size: 0.8rem;
  text-transform: capitalize;
}

.status-available {
  background: #d1fae5;
  color: #065f46;
}

.status-occupied {
  background: #fee2e2;
  color: #991b1b;
}

.status-booked {
  background: #dbeafe;
  color: #1e40af;
}

/* Address Content */
.address-content {
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
}

.address-content p {
  margin: 0;
  color: #334155;
  line-height: 1.6;
}

.text-muted {
  color: #94a3b8;
}

/* Responsive Design */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 1rem;
  }

  .admin-card {
    padding: 1.5rem;
  }

  .card-title {
    font-size: 1.5rem;
  }

  .card-subtitle {
    font-size: 0.9rem;
  }

  .custom-table {
    font-size: 0.8rem;
  }

  .custom-table th,
  .custom-table td {
    padding: 0.75rem 0.5rem;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn-action {
    width: 100%;
    text-align: center;
  }

  .modal-container {
    max-width: 95%;
    margin: 1rem;
  }
}
</style>