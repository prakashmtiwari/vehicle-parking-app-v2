 <template>
  <AdminNavbar />

  <div class="container my-5">
    <h2 class="mb-4 text-custom">Parking Lot Management</h2>

    <div class="d-flex justify-content-center align-items-center mb-3">
      <div>
        <router-link to="/parking-lots/new" class="btn custom-outline add-lot ">+ Add Parking Lot</router-link>
      </div>
      <!-- <div v-if="error" class="text-danger">{{ error }}</div> -->
    </div>

    <div class="card custom-outline p-3">
      <h3 class="text-custom">Parking Lots</h3>

      <div v-if="loading" class="py-4 text-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-else>
        <table class="table table-hover mt-3">
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
              <td>{{ lot.id }}</td>
              <td>{{ lot.prime_location_name }}</td>
              <td>{{ lot.price }}</td>
              <td>{{ lot.pin_code }}</td>
              <td>{{ lot.maximum_number_of_spots }}</td>
              <td>
                <router-link
                  :to="`/parking-lots/${lot.id}/edit`"
                  class="btn btn-sm btn-warning me-2"
                >Edit</router-link>
                <button
                  class="btn btn-sm btn-danger me-2"
                  @click="deleteLot(lot.id)"
                >Delete</button>
                <button
                  class="btn btn-sm btn-info"
                  @click="viewSpots(lot.id)"
                >View Spots</button>
                <button
                  class="btn btn-sm btn-secondary ms-2"
                  @click="viewAddress(lot.id)"
                >View Address</button>
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

  <!-- Spots Modal -->
  <div v-if="selectedLotSpots" class="modal fade show d-block overlay">
    <div class="modal-dialog custom-outline modal-lg">
      <div class="modal-content p-3">
        <div class="modal-header">
          <h5 class="modal-title text-custom">Parking Spots for Lot ID: {{ selectedLotId }}</h5>
          <button type="button" class="btn-close" @click="closeSpotsModal"></button>
        </div>
        <div class="modal-body">
          <table class="table">
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
                <td>{{ spot.id }}</td>
                <td>
                  <span :class="spot.status === 'O' ? 'text-warning' : 'text-success'">
                    {{ 
                      spot.active_reservation 
                        ? (
                           (new Date(spot.active_reservation.parking_timestamp) > new Date() 
                                  ? 'Booked' 
                                  : 'Active')
                          )
                        : 'Available' 
                    }}                  
                  </span>
                </td>
                <td>
                  <span v-if="spot.status === 'O'">{{ spot.active_reservation?.vehicle_number || '—' }}</span>
                  <span v-else>-</span>
                </td>
                <td>
                  <span v-if="spot.status === 'O'">{{ formatDateTime(spot.active_reservation?.parking_timestamp) || '—' }}</span>
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

  <!-- Address Modal -->
<div v-if="showAddressModal" class="modal fade show d-block overlay">
  <div class="modal-dialog custom-outline">
    <div class="modal-content p-3">
      <div class="modal-header">
        <h5 class="modal-title text-custom">Address for Parking Lot Id - {{ selectedLotName }}</h5>
      </div>
      <div class="modal-body">
        <p>{{ selectedLotAddress }}</p>
      </div>
      <div class="modal-footer">
        <button class="btn btn-secondary" @click="closeAddressModal">Close</button>
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
      // backend should return helpful message if cannot delete
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
    // update UI after releasing
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

  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6); /* dark backdrop */
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1050; /* above most content */
  }

  .modal-container {
    background: white;
    border-radius: 0.5rem;
    max-width: 700px;
    width: 90%;
    box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.25);
    overflow: hidden;
  }

.text-custom {
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

.add-lot:hover{
  background-color:rgb(56, 53, 206, 0.74);
}

  </style>
