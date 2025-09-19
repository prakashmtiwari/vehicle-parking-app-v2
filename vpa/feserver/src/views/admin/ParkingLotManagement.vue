<template>
  <AdminNavbar />

  <div class="container my-5">
    <h2 class="mb-4">Parking Lot Management</h2>

    <div class="d-flex justify-content-between align-items-center mb-3">
      <div>
        <button class="btn btn-success" @click="openAddModal">+ Add Parking Lot</button>
      </div>
      <div v-if="error" class="text-danger">{{ error }}</div>
    </div>

    <div class="card p-3">
      <h5>Parking Lots</h5>

      <div v-if="loading" class="py-4 text-center">
        <div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div>
      </div>

      <div v-else>
        <table class="table table-bordered mt-3">
          <thead>
            <tr>
              <th>ID</th>
              <th>Prime Location</th>
              <th>Price</th>
              <th>Address</th>
              <th>Pin Code</th>
              <th>Max Spots</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lot in lots" :key="lot.id">
              <td>{{ lot.id }}</td>
              <td>{{ lot.prime_location_name }}</td>
              <td>{{ lot.price }}</td>
              <td>{{ lot.address }}</td>
              <td>{{ lot.pin_code }}</td>
              <td>{{ lot.maximum_number_of_spots }}</td>
              <td>
                <button class="btn btn-sm btn-primary me-2" @click="openEditModal(lot)">Edit</button>
                <button class="btn btn-sm btn-danger me-2" @click="deleteLot(lot.id)">Delete</button>
                <button class="btn btn-sm btn-info" @click="viewSpots(lot.id)">View Spots</button>
              </td>
            </tr>
            <tr v-if="lots.length === 0">
              <td colspan="7" class="text-center">No parking lots available.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Add Lot Modal -->
  <div v-if="showAddModal" class="modal fade show d-block overlay">
    <div class="modal-dialog modal-lg modal-top">
      <div class="modal-content">
        <div class="modal-header bg-success text-white">
          <h5 class="modal-title">Add Parking Lot</h5>
          <button class="btn-close btn-close-white" @click="closeAddModal"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="createLot">
            <div class="row g-3">
              <div class="col-md-6">
                <input v-model="form.prime_location_name" class="form-control" placeholder="Prime Location Name" required />
              </div>
              <div class="col-md-6">
                <input v-model.number="form.price" type="number" class="form-control" placeholder="Price" required />
              </div>
              <div class="col-md-6">
                <input v-model="form.address" class="form-control" placeholder="Address" required />
              </div>
              <div class="col-md-6">
                <input v-model="form.pin_code" class="form-control" placeholder="Pin Code" />
              </div>
              <div class="col-md-6">
                <input v-model.number="form.maximum_number_of_spots" type="number" class="form-control" placeholder="Max Spots" required min="1" />
              </div>
            </div>

            <div class="text-end mt-3">
              <button type="button" class="btn btn-secondary me-2" @click="closeAddModal">Cancel</button>
              <button type="submit" class="btn btn-success" :disabled="creating">Create</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <!-- Edit Lot Modal -->
  <div v-if="showEditModal" class="modal fade show d-block overlay">
    <div class="modal-dialog modal-lg modal-top">
      <div class="modal-content">
        <div class="modal-header bg-primary text-white">
          <h5 class="modal-title">Edit Parking Lot</h5>
          <button class="btn-close btn-close-white" @click="closeEditModal"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="updateLot">
            <div class="row g-3">
              <div class="col-md-6">
                <input v-model="form.prime_location_name" class="form-control" placeholder="Prime Location Name" required />
              </div>
              <div class="col-md-6">
                <input v-model.number="form.price" type="number" class="form-control" placeholder="Price" required />
              </div>
              <div class="col-md-6">
                <input v-model="form.address" class="form-control" placeholder="Address" required />
              </div>
              <div class="col-md-6">
                <input v-model="form.pin_code" class="form-control" placeholder="Pin Code" />
              </div>
              <div class="col-md-6">
                <input v-model.number="form.maximum_number_of_spots" type="number" class="form-control" placeholder="Max Spots" required min="1" />
              </div>
            </div>

            <div class="text-end mt-3">
              <button type="button" class="btn btn-secondary me-2" @click="closeEditModal">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="updating">Update</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>

  <!-- Spots Modal -->
  <div v-if="selectedLotSpots" class="modal fade show d-block overlay">
    <div class="modal-dialog modal-lg">
      <div class="modal-content p-3">
        <div class="modal-header">
          <h5 class="modal-title">Parking Spots for Lot {{ selectedLotId }}</h5>
          <button type="button" class="btn-close" @click="closeSpotsModal"></button>
        </div>
        <div class="modal-body">
          <table class="table">
            <thead>
              <tr>
                <th>Spot ID</th>
                <th>Status</th>
                <th>Vehicle</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="spot in selectedLotSpots" :key="spot.id">
                <td>{{ spot.id }}</td>
                <td>
                  <span :class="spot.status === 'O' ? 'text-danger' : 'text-success'">
                    {{ spot.status === 'O' ? 'Occupied' : 'Empty' }}
                  </span>
                </td>
                <td>
                  <span v-if="spot.status === 'O'">{{ spot.reservation?.vehicle_number || '—' }}</span>
                  <span v-else>-</span>
                </td>
              </tr>
              <tr v-if="selectedLotSpots.length === 0">
                <td colspan="3" class="text-center">No spots found</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>

  <AdminFooter />
</template>

<script setup>
import { ref, reactive, onMounted } from "vue"
import parkingLotService from "@/services/parkingLotService"
import AdminNavbar from '@/components/AdminNavbar.vue'
import AdminFooter from '@/components/AdminFooter.vue'

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

const showAddModal = ref(false)
const showEditModal = ref(false)
const creating = ref(false)
const updating = ref(false)

const selectedLotSpots = ref(null)
const selectedLotId = ref(null)

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

function openAddModal() {
  Object.assign(form, { id: null, prime_location_name: "", price: null, address: "", pin_code: "", maximum_number_of_spots: null })
  showAddModal.value = true
}

function closeAddModal() {
  showAddModal.value = false
}

function openEditModal(lot) {
  // copy fields into form
  Object.assign(form, {
    id: lot.id,
    prime_location_name: lot.prime_location_name,
    price: lot.price,
    address: lot.address,
    pin_code: lot.pin_code,
    maximum_number_of_spots: lot.maximum_number_of_spots
  })
  showEditModal.value = true
}

function closeEditModal() {
  showEditModal.value = false
}

async function createLot() {
  creating.value = true
  try {
    // validation
    if (!form.prime_location_name || !form.price || !form.address || !form.maximum_number_of_spots) {
      throw new Error("Please fill required fields")
    }
    const payload = {
      prime_location_name: form.prime_location_name,
      price: Number(form.price),
      address: form.address,
      pin_code: form.pin_code,
      maximum_number_of_spots: Number(form.maximum_number_of_spots)
    }
    await parkingLotService.createLot(payload)
    await loadLots()
    closeAddModal()
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to create lot"
  } finally {
    creating.value = false
  }
}

async function updateLot() {
  if (!form.id) return
  updating.value = true
  try {
    const payload = {
      prime_location_name: form.prime_location_name,
      price: Number(form.price),
      address: form.address,
      pin_code: form.pin_code,
      maximum_number_of_spots: Number(form.maximum_number_of_spots)
    }
    await parkingLotService.updateLot(form.id, payload)
    await loadLots()
    closeEditModal()
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to update lot"
  } finally {
    updating.value = false
  }
}

async function deleteLot(id) {
  if (!confirm("Are you sure you want to delete this lot?")) return
  try {
    await parkingLotService.deleteLot(id)
    await loadLots()
  } catch (err) {
    console.error(err)
    // backend should return helpful message if cannot delete
    error.value = err.response?.data?.message || err.message || "Failed to delete lot"
    alert(error.value)
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

function closeSpotsModal() {
  selectedLotSpots.value = null
  selectedLotId.value = null
}

onMounted(loadLots)
</script>

<style scoped>
.table th, .table td { vertical-align: middle; }

/* modal overlay & top placement */
.overlay {
  background: rgba(0,0,0,0.5);
  position: fixed;
  inset: 0;
  z-index: 1050;
  display: flex;
  align-items: flex-start; /* top-ish */
  justify-content: center;
  padding-top: 4vh; /* moves modal slightly down from very top */
}
.modal-top .modal-dialog {
  max-width: 800px;
}
.modal-content {
  border-radius: 0.5rem;
}
</style>
