<template>
  <AdminNavbar />

<div class="container my-5" style="width: 80%; overflow-y: auto; overflow-x: hidden;">
    <h2 class="mb-4 custom-text">
      {{ isEdit ? "Edit Parking Lot" : "Add Parking Lot" }}
    </h2>

  <div class="card custom-outline p-4 d-flex flex-column" style="max-height: 80vh; overflow-y: auto;">

   <form @submit.prevent="handleSubmit">
  <!-- Prime Location -->
  <div class="mb-3">
    <label for="primeLocation" class="form-label">Prime Location</label>
    <input
      type="text"
      class="form-control"
      id="primeLocation"
      v-model="form.prime_location_name"
      placeholder="Enter location"
      required
    >
  </div>

  <!-- Price -->
  <div class="mb-3">
    <label for="price" class="form-label">Price</label>
    <input
      type="number"
      class="form-control"
      id="price"
      v-model.number="form.price"
      placeholder="Enter price"
      required
    >
  </div>

  <!-- Address -->
  <div class="mb-3">
    <label for="address" class="form-label">Address</label>
    <input
      type="text"
      class="form-control"
      id="address"
      v-model="form.address"
      placeholder="Enter address"
      required
    >
  </div>

  <!-- Pin Code -->
  <div class="mb-3">
    <label for="pinCode" class="form-label">Pin Code</label>
    <input
      type="text"
      class="form-control"
      id="pinCode"
      v-model="form.pin_code"
      placeholder="Enter pin code"
    >
  </div>

  <!-- Max Spots -->
  <div class="mb-3">
    <label for="maxSpots" class="form-label">Maximum Number of Spots</label>
    <input
      type="number"
      class="form-control"
      id="maxSpots"
      v-model.number="form.maximum_number_of_spots"
      placeholder="Enter number of spots"
      min="1"
      required
    >
  </div>

  <!-- Actions -->
  <div class="text-end mt-4">
    <button type="button" class="btn btn-light me-2" @click="cancelForm">Cancel</button>
    <button type="submit" class="btn btn-success">
      {{ isEdit ? "Update" : "Create" }}
    </button>
  </div>
</form>

</div>
</div>

<AdminFooter />
</template>


<style scoped>
.custom-outline {
  border: 2px solid rgb(218, 47, 218); 
}

.custom-outline:focus {
  outline: none;
  border-color: rgb(245, 99, 245); 
  box-shadow: 0 0 4px rgb(245, 99, 245);
}


.custom-text {
  color: rgb(218, 47, 218);
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  font-weight: bold;
  text-align: center;
}

.container{
  padding-bottom: 80px;
  align-items: center;
  background:   white;
  padding: 1rem 2rem;
  overflow-x: hidden;
  padding: 1rem 2rem;
}
</style>




<script setup>
import { reactive, ref, onMounted, computed } from "vue"
import { useRoute, useRouter } from "vue-router"
import parkingLotService from "@/services/parkingLotService"
import AdminNavbar from "@/components/AdminNavbar.vue"
import AdminFooter from "@/components/AdminFooter.vue"
import { useToast } from "vue-toastification";


const toast = useToast();


// Router hooks
const route = useRoute()
const router = useRouter()
const lotId = route.params.id

// Determine if we're in Edit mode
const isEdit = computed(() => !!route.params.id)

// Form state
const form = reactive({
  prime_location_name: "",
  price: null,
  address: "",
  pin_code: "",
  maximum_number_of_spots: null
})

// Loading state
const loading = ref(false)
const error = ref("")

// Fetch existing lot if editing
onMounted(async () => {
  if (lotId) { // only fetch if editing
    loading.value = true
    try {
      const res = await parkingLotService.getLot(lotId)
      // copy data into form
      Object.assign(form, {
        prime_location_name: res.data.prime_location_name,
        price: res.data.price,
        address: res.data.address,
        pin_code: res.data.pin_code,
        maximum_number_of_spots: res.data.maximum_number_of_spots
      })
    } catch (err) {
      console.error(err)
      error.value = err.response?.data?.message || err.message || "Failed to load lot"
    } finally {
      loading.value = false
    }
  }
})

// Submit handler
async function handleSubmit() {
  loading.value = true
  try {
    // Validation (optional)
    if (!form.prime_location_name || !form.price || !form.address || !form.maximum_number_of_spots) {
      toast.error("Please fill all required fields.")
      return
    }

    if (isEdit.value) {
      // Update existing lot
      await parkingLotService.updateLot(route.params.id, form)
    } else {
      // Create new lot
      await parkingLotService.createLot(form)
    }

    // Navigate back to parking lot list
    router.push("/parking-lots")
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.message || err.message || "Failed to save lot"
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

// Cancel handler
function cancelForm() {
  router.push("/parking-lots")
}
</script>
